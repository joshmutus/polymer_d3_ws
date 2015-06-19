# -*- test-case-name: test_streamer -*-
"""WebSocket Echo.

Install: pip install twisted txws

Run: twistd -ny streamer.py

Visit http://localhost:8080/
"""
from twisted.application         import strports # pip install twisted
from twisted.application.service import Application
from twisted.internet.protocol   import Factory, Protocol
from twisted.python              import log

from txws import WebSocketFactory # pip install txws
import json
import time

class EchoUpper(Protocol):
    """Echo uppercased."""
    def dataReceived(self, data):
        log.msg("Got %r" % (data,))
        if data == "get_dirs":
            #self.transport.write(json.dumps(["remoteDir 1", "remoteDir 2","remoteDir 3"]))
            self.transport.write(json.dumps([{"name": "remoteDir 1", "type": "folder"},{"name": "remoteDir 2", "type": "folder"}]))
        elif data =="remoteDir 1":
            self.transport.write(json.dumps([{"name": "newDir 1", "type": "folder"},{"name": "newDat 1", "type": "data"}]))
        elif data =="get_data":
            log.msg("sending in response to get_data")
            self.transport.write(json.dumps([[[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15], [16, 16], [17, 17], [18, 18], [19, 19], [20, 20], [21, 21], [22, 22], [23, 23], [24, 24], [25, 25], [26, 26], [27, 27], [28, 28], [29, 29], [30, 30], [31, 31], [32, 32], [33, 33], [34, 34], [35, 35], [36, 36], [37, 37], [38, 38], [39, 39], [40, 40], [41, 41], [42, 42], [43, 43], [44, 44], [45, 45], [46, 46], [47, 47], [48, 48], [49, 49], [50, 50], [51, 49], [52, 48], [53, 47], [54, 46], [55, 45], [56, 44], [57, 43], [58, 42], [59, 41], [60, 40], [61, 39], [62, 38], [63, 37], [64, 36], [65, 35], [66, 34], [67, 33], [68, 32], [69, 31], [70, 30], [71, 29], [72, 28], [73, 27], [74, 26], [75, 25], [76, 24], [77, 23], [78, 22], [79, 21], [80, 20], [81, 19], [82, 18], [83, 17], [84, 16], [85, 15], [86, 14], [87, 13], [88, 12], [89, 11], [90, 10], [91, 9], [92, 8], [93, 7], [94, 6], [95, 5], [96, 4], [97, 3], [98, 2], [99, 1]],[[0, 79], [1, 73], [2, 81], [3, 76], [4, 21], [5, 16], [6, 84], [7, 64], [8, 39], [9, 8], [10, 45], [11, 27], [12, 19], [13, 3], [14, 33], [15, 34], [16, 50], [17, 23], [18, 23], [19, 99], [20, 45], [21, 43], [22, 80], [23, 16], [24, 6], [25, 24], [26, 73], [27, 85], [28, 74], [29, 84], [30, 94], [31, 53], [32, 66], [33, 91], [34, 4], [35, 75], [36, 6], [37, 18], [38, 25], [39, 42], [40, 7], [41, 58], [42, 50], [43, 43], [44, 50], [45, 14], [46, 14], [47, 57], [48, 10], [49, 71], [50, 70], [51, 64], [52, 83], [53, 99], [54, 76], [55, 94], [56, 29], [57, 66], [58, 70], [59, 15], [60, 60], [61, 37], [62, 24], [63, 88], [64, 3], [65, 92], [66, 45], [67, 40], [68, 38], [69, 8], [70, 19], [71, 38], [72, 71], [73, 41], [74, 97], [75, 44], [76, 25], [77, 88], [78, 62], [79, 13], [80, 26], [81, 59], [82, 31], [83, 8], [84, 42], [85, 41], [86, 94], [87, 59], [88, 67], [89, 40], [90, 80], [91, 63], [92, 53], [93, 31], [94, 72], [95, 50], [96, 44], [97, 16], [98, 54], [99, 55]]]))
        else:
            self.transport.write(data.upper())

application = Application("ws-streamer")

echofactory = Factory()
echofactory.protocol = EchoUpper # use Factory.buildProtocol()
service = strports.service("tcp:8076:interface=127.0.0.1",
                           WebSocketFactory(echofactory))
service.setServiceParent(application)

from twisted.web.server   import Site
from twisted.web.static   import File

resource = File('.') # serve current directory
webservice = strports.service("tcp:8080:interface=127.0.0.1",
                              Site(resource))
webservice.setServiceParent(application)

