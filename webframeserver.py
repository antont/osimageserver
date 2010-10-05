import clr
clr.AddReference('OpenSim.Framework')
clr.AddReference('OpenSim.Region.Framework')
clr.AddReference('System.Drawing')

from System import Convert
from System.Collections import Hashtable
from System.IO import MemoryStream
from System.Drawing.Imaging import Encoder, EncoderParameters, EncoderParameter, ImageCodecInfo
from OpenSim.Region.Framework.Interfaces import IRegionModule
from OpenSim.Framework import MainServer

import regionmodule

URL = "/myurl3/"

class WebFrameserverModule(regionmodule.RegionModule):
    def Initialise(self, scene, configsource):
        self.scene = scene

        print "jee", MainServer
        server = MainServer.Instance
        server.AddHTTPHandler(URL, self.onHTTPGetImage)

        print self.render() #to test upon opensim console py-reload without doing anything else

    def Close(self):
        print "pois"
        MainServer.Instance.RemoveHTTPHandler("GET", URL)

    def render(self):
        imagemod = self.scene.Modules['Warp3DImageModule']
        bmp = imagemod.CreateMapTile()
        print type(bmp)

        imgstream = MemoryStream()
        encparams = EncoderParameters()
        encparams.Param[0] = EncoderParameter(Encoder.Quality, 95)
        bmp.Save(imgstream, getEncoderInfo("image/jpeg"), encparams)
        return imgstream

    def onHTTPGetImage(self, params):
        print params

        img = self.render()
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
