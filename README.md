# rocm_gpu_info
This repository contains tools for AMD GPU ROCm platform.

gpu_mem_tracker.py contain class and methods to trace memory leaks from GPU. mem_usage_example.py contains example on how to use developed class and its API. To use mem_usage_example.py, replace your app execution and run same with python3. 

gpu_current_system_information.py contains utility to get current GPU system information while running workloads. This will fetch Temperature, GPU clk, fan data, Current package power, VRAM usage, GPU usage information. To use this utilty run command as 'python3 gpu_current_system_information.py --time/-t 5 --format-f csv'
