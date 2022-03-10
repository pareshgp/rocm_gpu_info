import subprocess
import re
import time
import argparse

parser = argparse.ArgumentParser(description="gpu_current_system_information")
parser.add_argument("-t", "--time",nargs='?', default=None,help="Enter time in seconds")
parser.add_argument("-f","--format",nargs='?', default=None,help="Enter output format as json or csv")

class curr_sys_info:
    def __init__(self, tm, fmt):
        self.timer = tm
        self.format = fmt
        self.outputfile = "system_info.%s"%self.format
	
    def start(self):
        #print("inside start")
        t = int(self.timer)
        cmd = '/opt/rocm/bin/rocm-smi --showpids -tgfpPu --showmemuse --%s'%(self.format)
        with open(self.outputfile,'a+') as file_ptr:
            while t > 0:
                p = subprocess.Popen('%s'%cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
                if (t != int(self.timer) and self.format != "json"):
                    for line in p.stdout:
                        if not re.search(r"\bTemperature\b",line.decode(), re.M):
                            file_ptr.write(line.decode())
                else:
                    for line in p.stdout:
                        file_ptr.write(line.decode())
                t = t-1
                time.sleep(1)
        file_ptr.close()


if __name__ == '__main__':
    args = parser.parse_args()
    t = 1
    f = "csv"
    if args.time:
        t=args.time
    if args.format:
        f=args.format
    get_info = curr_sys_info(t,f)
    try:
        get_info.start()
    except KeyboardInterrupt:
        print(" Capturing of current System Information Stopped by use in between!!!")
    except:
        print(" Capturing of current System Information failed!!!")


