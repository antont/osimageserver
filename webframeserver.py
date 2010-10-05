import clr
clr.AddReference('OpenSim.Framework')
clr.AddReference('OpenSim.Region.Framework')
clr.AddReference('System.Drawing')
clr.AddReference('OpenMetaverseTypes')

from System import Convert
from System.Collections import Hashtable
from System.IO import MemoryStream
from System.Drawing.Imaging import Encoder, EncoderParameters, EncoderParameter, ImageCodecInfo

from OpenMetaverse import Vector3, Quaternion

from OpenSim.Region.Framework.Interfaces import IRegionModule
from OpenSim.Framework import MainServer

from math import *
import regionmodule

URL = "/renderimg/"

class WebFrameserverModule(regionmodule.RegionModule):
    def Initialise(self, scene, configsource):
        self.scene = scene

        print self.render() #to test upon opensim console py-reload without doing anything else

        server = MainServer.Instance
        server.AddHTTPHandler(URL, self.onHTTPGetImage)

    def Close(self):
        print "pois"
        MainServer.Instance.RemoveHTTPHandler("GET", URL)

    def render(self, campos=Vector3(80, 127.5, 50), camdir=-Vector3.UnitZ):
        imagemod = self.scene.Modules['Warp3DImageModule']
        bmp = imagemod.CreateViewImage(campos, camdir, 60, 700, 700)

        imgstream = MemoryStream()
        encparams = EncoderParameters()
        encparams.Param[0] = EncoderParameter(Encoder.Quality, 95)
        bmp.Save(imgstream, getEncoderInfo("image/jpeg"), encparams)
        return imgstream

    def onHTTPGetImage(self, params):
        print params

        for entry in params:
            print entry.Key, entry.Value

        camposx = maybefloat(params['camposx']) or 127.5
        camposy = maybefloat(params['camposy']) or 127.5
        camposz = maybefloat(params['camposz']) or 60
        #print camposx, camposy, camposz
        campos = Vector3(camposx, camposy, camposz)

        #camortx = maybefloat(params['camortx'])
        #camorty = maybefloat(params['camorty'])
        #camortz = maybefloat(params['camortz'])
        #camortw = maybefloat(params['camortw'])
        #if None in [camortx, camorty, camortz, camortw]:
        #    camdir = -Vector3.UnitY
        #else:
        #    camdir = Vector3.UnitX * Quaternion(camortx, camorty, camortz, camortw)
        camyaw = maybefloat(params['camyaw'])
        campitch = maybefloat(params['campitch'])
        camroll = maybefloat(params['camroll'])
        if None in [camyaw, campitch, camroll]:
            camdir = -Vector3.UnitZ
        else:
            dx = sin(radians(camyaw)) * cos(radians(campitch))
            dy = sin(radians(-campitch))
            dz = cos(radians(camyaw)) * cos(radians(campitch))
            camdir = Vector3(dx, dy, dz)
        
        img = self.render(campos, camdir)
        jpeg = img.ToArray()

        return Hashtable({
            "int_response_code": 200,
            "str_response_string": Convert.ToBase64String(jpeg),
            "content_type": "image/jpeg"
            })

def getEncoderInfo(mimetype): #ported to py from the c# example on msdn, which is also in WorldMapModule
    encoders = ImageCodecInfo.GetImageEncoders()
    for e in encoders:
        if e.MimeType == mimetype:
            return e

def maybefloat(s):
    try:
        return float(s)
    except: #ValueError, TypeError:
        return None
