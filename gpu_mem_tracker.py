import subprocess
import re

class mem_tracker:
    def __init__(self):
        self.init_total_mem = 0
        self.init_used_mem = 0
        self.total_mem = 0
        self.used_mem = 0
        self.test_name = ""

    def start(self):
        p = subprocess.Popen('/opt/rocm/bin/rocm-smi --showmeminfo vram', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            if re.search(r"\bTotal Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.init_total_mem = searchObj[1]
            if re.search(r"\bTotal Used Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.init_used_mem = searchObj[1]
        print('total mem', self.init_total_mem, 'Used mem', self.init_used_mem)


    def stop(self):
        p = subprocess.Popen('/opt/rocm/bin/rocm-smi --showmeminfo vram', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            if re.search(r"\bTotal Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.total_mem = searchObj[1]
            if re.search(r"\bTotal Used Memory\b",line.decode(), re.M):
                searchObj = re.findall(\
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line.decode())
                if (len(searchObj) > 1):
                    self.used_mem = searchObj[1]
        print('total mem', self.total_mem, 'Used mem', self.used_mem)

    def validate(self, test_name):
        with open("gpu_memory_leak_report.txt",'a+') as f:
            print("self.init_used_mem %s self.used_mem %s"%(self.init_used_mem, self.used_mem))
            if int(self.init_used_mem) == int(self.used_mem):
                f.write("%s : %s, "%(test_name, "PASS"))
                f.write("No memory leak %s \n"%(test_name))
            else:
                f.write("%s : %s, "%(test_name, "FAIL"))
                leak_bytes = int(self.used_mem) - int(self.init_used_mem)
                f.write("Total leak bytes for %s is %s\n"%(test_name, leak_bytes))
            f.close()
