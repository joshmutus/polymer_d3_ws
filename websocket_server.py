"""WebSocket Echo.

Install: pip install twisted txws

run as python websocket_server.py

Connect to at localhost:8076/
"""
from twisted.application import strports # pip install twisted
from twisted.application.service import Application
from twisted.internet.protocol import Factory, Protocol
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from txws import WebSocketFactory # pip install txws
import numpy as np
from ast import literal_eval
import json

class CxnFactory(Factory):
    '''
    This is a factory but with a client connection
    '''
    def __init__(self,cxn):
        self.cxn = cxn


def parse_dir(resp):
    dir_list_parsed = []
    for ent in resp[0]:
        dir_list_parsed.append({"name":str(ent),"type":"folder"})
    for ent in resp[1]:
        dir_list_parsed.append({"name":str(ent),"type":"data"})
    return dir_list_parsed

def find_limits(data):
    x_min, x_max  = data[:,0][0], data[:,0][-1]
    y_min, y_max = data.min(),data.max
    return {"x_min":str(x_min),"x_max":str(x_max), "y_min": str(y_min),"y_max": str(y_max)}

def parse_line_data(data):
    superArr = []
    for col, ent in enumerate(data[0]):
        arr =[]
        for row, ent in enumerate(data[:,0]):
            arr.append([data[:,0][row],data[:,col][row]])
        superArr.append([arr])
    return superArr

def parse_axis_labels(variables):
    x_label = str(dv.variables()[0][0][0])+" ("+ str(dv.variables()[0][0][1])+")"
    y_label = str(dv.variables()[1][0][0])+" ("+ str(dv.variables()[1][0][1])+")"
    return {"x_label" : x_label,"y_label" : y_label}

class DataVaultProtocol(Protocol):
    """Protocol for handling request to the data_vault server"""

    def connectionMade(self):
        log.msg("Connection made, connected to: ",self.factory.cxn)
        self.cxn = self.factory.cxn
        self.dv = self.cxn.data_vault

    @inlineCallbacks
    def dataReceived(self, data):
        log.msg(data)
        parsed = data.split('.')
        if parsed[0] == "cd":
            log.msg("Got a dv cd request")
            pv = yield self.dv.cd(literal_eval(parsed[1]))
            self.transport.write("Current Directory: " + str(pv))
        elif parsed[0] == "get_dirs":
            log.msg("Got a request for dv dir")
            dir_list = yield self.dv.dir()
            dir_list_parsed = parse_dir(dir_list)
            self.transport.write(json.dumps(dir_list_parsed))
        elif parsed[0] =="get_data":
            log.msg("sending in response to get_data")
            self.transport.write(json.dumps([[[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15], [16, 16], [17, 17], [18, 18], [19, 19], [20, 20], [21, 21], [22, 22], [23, 23], [24, 24], [25, 25], [26, 26], [27, 27], [28, 28], [29, 29], [30, 30], [31, 31], [32, 32], [33, 33], [34, 34], [35, 35], [36, 36], [37, 37], [38, 38], [39, 39], [40, 40], [41, 41], [42, 42], [43, 43], [44, 44], [45, 45], [46, 46], [47, 47], [48, 48], [49, 49], [50, 50], [51, 49], [52, 48], [53, 47], [54, 46], [55, 45], [56, 44], [57, 43], [58, 42], [59, 41], [60, 40], [61, 39], [62, 38], [63, 37], [64, 36], [65, 35], [66, 34], [67, 33], [68, 32], [69, 31], [70, 30], [71, 29], [72, 28], [73, 27], [74, 26], [75, 25], [76, 24], [77, 23], [78, 22], [79, 21], [80, 20], [81, 19], [82, 18], [83, 17], [84, 16], [85, 15], [86, 14], [87, 13], [88, 12], [89, 11], [90, 10], [91, 9], [92, 8], [93, 7], [94, 6], [95, 5], [96, 4], [97, 3], [98, 2], [99, 1]],[[0, 79], [1, 73], [2, 81], [3, 76], [4, 21], [5, 16], [6, 84], [7, 64], [8, 39], [9, 8], [10, 45], [11, 27], [12, 19], [13, 3], [14, 33], [15, 34], [16, 50], [17, 23], [18, 23], [19, 99], [20, 45], [21, 43], [22, 80], [23, 16], [24, 6], [25, 24], [26, 73], [27, 85], [28, 74], [29, 84], [30, 94], [31, 53], [32, 66], [33, 91], [34, 4], [35, 75], [36, 6], [37, 18], [38, 25], [39, 42], [40, 7], [41, 58], [42, 50], [43, 43], [44, 50], [45, 14], [46, 14], [47, 57], [48, 10], [49, 71], [50, 70], [51, 64], [52, 83], [53, 99], [54, 76], [55, 94], [56, 29], [57, 66], [58, 70], [59, 15], [60, 60], [61, 37], [62, 24], [63, 88], [64, 3], [65, 92], [66, 45], [67, 40], [68, 38], [69, 8], [70, 19], [71, 38], [72, 71], [73, 41], [74, 97], [75, 44], [76, 25], [77, 88], [78, 62], [79, 13], [80, 26], [81, 59], [82, 31], [83, 8], [84, 42], [85, 41], [86, 94], [87, 59], [88, 67], [89, 40], [90, 80], [91, 63], [92, 53], [93, 31], [94, 72], [95, 50], [96, 44], [97, 16], [98, 54], [99, 55]]]))

        elif parsed[0] == "get":
            log.msg("Got a request for dv get")
        elif parsed[0] == "open":
            log.msg("Got a request for dv open")
        else:
            log.msg("Got an unsupported request")
            self.transport.write("I'm sorry, I can't do that")

from labrad.server import LabradServer, setting

class WebSocketServer(LabradServer):
    name = "Web Socket Server"    # Will be labrad name of server

    def initServer(self):
        application = Application("ws-streamer")
        data_vaultfactory = CxnFactory(self.client)
        data_vaultfactory.protocol = DataVaultProtocol
        reactor.listenTCP(8076, WebSocketFactory(data_vaultfactory))

__server__ = WebSocketServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)
