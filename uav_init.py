#!/usr/bin/env python3

import os
import socket
import subprocess

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error: {e}"

def get_ssh_info():
    user = os.getlogin()
    ip = get_ip_address()
    return f"{user}@{ip}"

def print_system_status():
    print("========== UAV System Initialization ==========")
    print(f"User         : {os.getlogin()}")
    print(f"Hostname     : {socket.gethostname()}")
    print(f"IP Address   : {get_ip_address()}")
    print(f"SSH Access   : ssh {get_ssh_info()}")
    print("ROS Version  : Noetic Ninjemys")
    print("Starting ROS master (if not already running)...")
    subprocess.run(["roscore"], shell=True, check=False)

def run_custom_commands():
    print("\nRunning custom setup...")
    # Add any startup commands here (edit to fit your setup)
    os.system("source ~/catkin_ws/devel/setup.bash")
    os.system("export ROS_MASTER_URI=http://localhost:11311")
    os.system("export ROS_IP=" + get_ip_address())
    # Optionally launch camera nodes or others
    # os.system("roslaunch my_package my_launchfile.launch")

if __name__ == "__main__":
    print_system_status()
    run_custom_commands()
