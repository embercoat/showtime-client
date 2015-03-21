import SocketServer
import json
import sys
import ConfigParser
import psutil
import time
import sh
import logging
import signal



class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()

        if(self.data == "status"):
            logging.info("Statusrequest from {}".format(self.client_address[0]))
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
            logging.debug("{} wrote:".format(self.client_address[0]))
            logging.debug(str(self.data))
            # just send back the same data, but upper-cased
            self.request.sendall("your string in caps: {}".format(self.data.upper()))


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

def sigint(signum, frame):    
    logging.info("User interrupt Exiting gracefully.")
    sys.exit(0)
    
def sigterm(signum, frame):    
    logging.info("Termination. Exiting gracefully.")
    sys.exit(0)

if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, sigint)
    signal.signal(signal.SIGTERM, sigterm)
    
    config = ConfigParser.RawConfigParser()
    config.read('/etc/showtime/showtime.conf')
    logging.basicConfig(level=logging.DEBUG,
                    filename=config.get('sentinel', 'logfile'),
                    format='%(asctime)s [%(levelname)8s] %(filename)12s:%(lineno)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    logging.info("Initializing Sentinel")
    logging.info("Listening on: {0}:{1}".format(config.get('sentinel', 'listen'),config.getint('sentinel', 'port')))
    processcheck('viewer')
    server = SocketServer.TCPServer((config.get('sentinel', 'listen'), config.getint('sentinel', 'port')), MyTCPHandler)

    logging.debug("Running Forever")
    server.serve_forever()
