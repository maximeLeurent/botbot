import json
import os

class UserPreference():

    def __init__(self, mainWindow, pathPreference):
        self.jsonData = {}
        self.pathPreference = pathPreference
        self.loadFile(pathPreference)

    def saveFile(self):
        with open(self.pathPreference, "w") as filePref:
            filePref.write(json.dumps(self.jsonData))

    def loadFile(self, pathPreference):
        if os.path.isfile(pathPreference):
            self.pathPreference = pathPreference
            with open(pathPreference, "r") as filePref:
                data = filePref.read()
                self.jsonData = json.loads(data)

    def loadGeoWidget(self,widget):
        keyGeo = "geo_"+str(type(widget))
        if keyGeo in self.jsonData:
            geo = widget.geometry()
            geo.setRect(*self.jsonData[keyGeo])
            widget.setGeometry(geo)


    def loadSubWindow(self, subWindow):
        widget = subWindow.widget()
        keyGeo = "geoSubWin_"+str(type(widget))
        if keyGeo in self.jsonData:
            geo = subWindow.geometry()
            geo.setRect(*self.jsonData[keyGeo])
            subWindow.setGeometry(geo)

    def saveWidget(self,widget):
        if hasattr(widget, "getUserPrefs"):
            for keyPref, info in widget.getUserPrefs():
                self.jsonData[keyPref] = info

    def loadWidget(self, widget):
        if hasattr(widget, "getUserPrefsKeysFunc"):
            for keyPref, funcSet in widget.getUserPrefsKeysFunc():
                if keyPref in self.jsonData:
                    funcSet(self.jsonData[keyPref])

    def dumpGeometry(self, geometry):
        return geometry.getRect()

    def saveSubWindow(self, subWindow):
        widget = subWindow.widget()
        keyGeo = "geoSubWin_"+str(type(widget))
        self.jsonData[keyGeo] = self.dumpGeometry(subWindow.geometry())

    def saveGeoWidget(self, widget):
        self.jsonData["geo_"+ str(type(widget))] = self.dumpGeometry(widget.geometry())
