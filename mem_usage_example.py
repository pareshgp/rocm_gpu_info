import subprocess
import gpu_mem_tracker
from gpu_mem_tracker import mem_tracker

# First create memory tracking object
mem_obj = mem_tracker()
# Call start method from memory tracking object
mem_obj.start()
# Run the Application you want to track
p = subprocess.Popen('/opt/rocm/bin/rocminfo', shell=True)
p.wait()
# Call stop method from memory tracking object
mem_obj.stop()
# Call validate method from memory tracking object
mem_obj.validate("rocminfo")
