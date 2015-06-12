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
            self.transport.write(json.dumps(["remoteDir 1", "remoteDir 2","remoteDir 3"]))
        elif data =="remoteDir 1":
            self.transport.write(json.dumps(["newDir 1"]))
        elif data =="get_data":
            log.msg("sending in response to get_data")
            self.transport.write(json.dumps([[0, 79], [1, 73], [2, 81], [3, 76], [4, 21], [5, 16], [6, 84], [7, 64], [8, 39], [9, 8], [10, 45], [11, 27], [12, 19], [13, 3], [14, 33], [15, 34], [16, 50], [17, 23], [18, 23], [19, 99], [20, 45], [21, 43], [22, 80], [23, 16], [24, 6], [25, 24], [26, 73], [27, 85], [28, 74], [29, 84], [30, 94], [31, 53], [32, 66], [33, 91], [34, 4], [35, 75], [36, 6], [37, 18], [38, 25], [39, 42], [40, 7], [41, 58], [42, 50], [43, 43], [44, 50], [45, 14], [46, 14], [47, 57], [48, 10], [49, 71], [50, 70], [51, 64], [52, 83], [53, 99], [54, 76], [55, 94], [56, 29], [57, 66], [58, 70], [59, 15], [60, 60], [61, 37], [62, 24], [63, 88], [64, 3], [65, 92], [66, 45], [67, 40], [68, 38], [69, 8], [70, 19], [71, 38], [72, 71], [73, 41], [74, 97], [75, 44], [76, 25], [77, 88], [78, 62], [79, 13], [80, 26], [81, 59], [82, 31], [83, 8], [84, 42], [85, 41], [86, 94], [87, 59], [88, 67], [89, 40], [90, 80], [91, 63], [92, 53], [93, 31], [94, 72], [95, 50], [96, 44], [97, 16], [98, 54], [99, 55]]))
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
