#from devices import Device

class ManagerClient(object):

    def __init__(self):
        pass

    def onConfigureMessage(self, message):

        for a in message['adts']:
            pass
            #Device(cbid=a['id'], name=a['name'], friendlyName=a['friendly_name'])

    def onAdaptorService(self, message):
        for p in message["service"]:
            if p["characteristic"] == "temperature":
                pass

    def requestService(self):
        request = {"id": self.id,
                   "request": "service",
                   "service": [
                                {"characteristic": "temperature",
                                 "interval": 600
                                }
                              ]
                   }
        self.sendMessage(request, message["id"])

    def onAdaptorData(self, message):
        pass
