import clr
clr.AddReference('OpenSim.Framework')
clr.AddReference('OpenSim.Region.Framework')

from System.Collections import Hashtable
from OpenSim.Region.Framework.Interfaces import IRegionModule
from OpenSim.Framework import MainServer

import regionmodule

class WebFrameserverModule(regionmodule.RegionModule):
    def Initialise(self, scene, configsource):
        self.scene = scene

        print "jee", MainServer
        server = MainServer.Instance
        server.AddHTTPHandler("/myurl/", self.onHTTPGetImage)

    def Close(self):
        print "pois"
        MainServer.Instance.RemoveHTTPHandler("GET", "/myurl/")

    def onHTTPGetImage(self, params):
        print params

        imagemod = self.scene.Modules['Warp3DImageModule']
        img = imagemod.CreateMapTile()
        print type(img)

        return Hashtable({
            "int_response_code": 200,
            "str_response_string": "terve",
            "content_type": "text/plain"
            })
