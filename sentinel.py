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
            processes = ('xloader', '')
            statuses = {}
            for proc in processes:
                statuses[proc] = processcheck(proc)
            
            self.request.sendall(json.dumps(statuses))
            
        elif self.data == "killview":
                sh.killall('omxplayer.bin', _ok_code=[1])
                sh.killall('mplayer', _ok_code=[1])
		sh.kill(find_pid('python', 'viewer.py'))
                self.request.sendall(json.dumps("OK"))
                
        else:
            print "{} wrote:".format(self.client_address[0])
            print self.data
            # just send back the same data, but upper-cased
            self.request.sendall("your string in caps: {}".format(self.data.upper()))
            
        print
        print


def find_pid(name, cmdline):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        if name in pinfo['name']:
            for arg in pinfo['cmdline']:
                if cmdline in arg:
		    return pinfo['pid']

    return False

def processcheck(seekitem):
    plist = psutil.process_iter()
    str1=" ".join(str(x) for x in plist)
    if seekitem in str1:
        return True
    else:
        return False

if __name__ == "__main__":
    
    config = ConfigParser.RawConfigParser()
    config.read('/etc/showtime/showtime.conf')
    print("Initializing Sentinel")
    print("Listening on: {0}:{1}".format(config.get('Sentinel', 'listen'),config.getint('Sentinel', 'port')))
    processcheck('viewer')
    server = SocketServer.TCPServer((config.get('Sentinel', 'listen'), config.getint('Sentinel', 'port')), MyTCPHandler)

    print("Running Forever")
    print
    print
    server.serve_forever()
