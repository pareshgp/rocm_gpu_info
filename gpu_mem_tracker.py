import subprocess
import re
from datetime import datetime

def get_num_of_devices():
        nDev = 0
        p = subprocess.Popen('/opt/rocm/bin/rocm-smi -i', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            if "GPU ID" in line.decode():
                nDev += 1
            #print('nDev',nDev)
        return nDev

class mem_tracker:
    def __init__(self):
        self.init_total_mem = []
        self.init_used_mem = []
        self.total_mem = []
        self.used_mem = []
        self.test_name = ""
        self.num_devices = get_num_of_devices()
	
    def start(self):
        p = subprocess.Popen('/opt/rocm/bin/rocm-smi --showmeminfo vram', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            if re.search(r"\bTotal Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.init_total_mem.append(searchObj[1])
            if re.search(r"\bTotal Used Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.init_used_mem.append(searchObj[1])
        print('total mem', self.init_total_mem, 'Used mem', self.init_used_mem)


    def stop(self):
        p = subprocess.Popen('/opt/rocm/bin/rocm-smi --showmeminfo vram', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            if re.search(r"\bTotal Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.total_mem.append(searchObj[1])
            if re.search(r"\bTotal Used Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.used_mem.append(searchObj[1])
        print('total mem', self.total_mem, 'Used mem', self.used_mem)

    def validate(self, test_name):
        with open("gpu_memory_leak_report.txt",'a+') as f:
            print("self.init_used_mem %s self.used_mem %s"%(self.init_used_mem, self.used_mem))
            i = 0
            while (i < self.num_devices):
                if int(self.init_used_mem[i]) == int(self.used_mem[i]):
                    f.write("%s : %s, "%(test_name, "PASS"))
                    f.write("%s No memory leak %s \n"%(datetime.now(),test_name))
                else:
                    f.write("%s : %s, "%(test_name, "FAIL"))
                    leak_bytes = int(self.used_mem[i]) - int(self.init_used_mem[i])
                    f.write("%s Total leak bytes for %s is %s on device %s \n"%(datetime.now(), test_name, leak_bytes, i+1))
                i = i+1
            f.close()
