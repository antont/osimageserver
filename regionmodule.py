import clr
clr.AddReference('OpenSim.Framework')
clr.AddReference('OpenSim.Region.Framework')

from OpenSim.Region.Framework.Interfaces import IRegionModule

class RegionModule(IRegionModule):
    autoload = True

    def Initialise(self, scene, configsource):
        print "jee"

    def PostInitialise(self):
        print "pois"

    def getname(self):
        return self.__class__.__name__
    Name = property(getname)

    def isshared(self):
        return False
    IsSharedModule = property(isshared)

    def Close(self):
        pass


