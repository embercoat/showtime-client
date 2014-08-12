import SocketServer
import json
import sys
import ConfigParser
import psutil
import time
import sh

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        if(self.data == "status"):
            print "Statusrequest from {}".format(self.client_address[0])
            processes = ('xloader',  '/usr/sbin/apache2', '/usr/sbin/zabbix_server', 'zabbix_server')
            statuses = {}
            for proc in processes:
                statuses[proc] = processcheck(proc)
            
#            for iter in psutil.process_iter():
#                print iter
            
            
            self.request.sendall(json.dumps(statuses))
            
        elif self.data == "killview":
                sh.killall('omxplayer.bin', _ok_code=[1])
                sh.killall('mplayer', _ok_code=[1])
                self.request.sendall(json.dumps("OK"))
                
        else:
            print "{} wrote:".format(self.client_address[0])
            print self.data
            # just send back the same data, but upper-cased
            self.request.sendall("your string in caps: {}".format(self.data.upper()))
            
        print
        print

def processcheck(seekitem):
    plist = psutil.process_iter()
    str1=" ".join(str(x) for x in plist)
    if seekitem in str1:
        return True
    else:
        return False

if __name__ == "__main__":
    
    config = ConfigParser.RawConfigParser()
    config.read('/etc/showtime/showtime.cfg')
    print("Initializing Sentinel")
    print("Listening on: {0}:{1}".format(config.get('Sentinel', 'listen'),config.getint('Sentinel', 'port')))
    server = SocketServer.TCPServer((config.get('Sentinel', 'listen'), config.getint('Sentinel', 'port')), MyTCPHandler)

    print("Running Forever")
    print
    print
    server.serve_forever()
