import launch
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
# import asyncio
# import threading
import time
from multiprocessing import Process
import os
import psutil

def start_launch_service(launch_file):

    # launch_file_path option is using FindPackageShare and composing for whole path
    # here I use only the absolute path for testing
    ls = launch.LaunchService()
    # package_share = FindPackageShare(package=package_name).find(package_name)
    # launch_file_path = f"{package_share}/launch/{launch_file}"
    launch_file_path = '/home/doraoliver/Studium/ros_study/fishros/ros2bookcode/chapt4/chapt4_ws/install/learning_launch/share/learning_launch/launch/remapping.launch.py'
    ld = launch.LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_file_path)
        )
    ])
    
    # Describing the launch file
    ls.include_launch_description(ld)

    
    # Starting the launch program
    ls.run()
    
    '''
    This block failed, because ls starts running, it will get stuck here.
    # print("close launch node")
    # ls.shutdown()
    # print("task process terminate")
    # task.terminate()
    # task.join()
    
    test option:
    # task = Process(target=ls.run)
    # task.start()

    #ls.shutdown
    result:
    actually no effect
    '''

def main():
    # 指定 launch 文件路径 Specify the launch file path
    package_name = 'learning_launch'  # 替换为你的包名 Replace your package name
    launch_file = 'remapping.launch.py'  # 替换为你的 launch 文件名 Repalce your launch python file

    # starting the children process
    p = Process(target=start_launch_service, args=(launch_file,))
    p.start()

    # launch_service.run()
    # asyncio.run(launch_service.run_async())
    # print("Launch service is running in a separate thread.")
    # for i in range(5):
    #     print(f"Main thread doing something else... {i}")

    print("start successfully")
    time.sleep(2)
    pproc_pid = os.getpid()
    print("Parent pid:", pproc_pid) 
    print("child pid:", p.pid)

    # Get the all started new processes in child's process
    all_childpid = psutil.Process(p.pid).children(recursive=True)
    proc_kill_list = []
    print(all_childpid)
    # Get the processes need to be killed which started by launch program
    for proc in all_childpid:
        if proc.name() != "python3":
            proc_kill_list.append(proc.pid)
    # print(all_childpid)
    print(proc_kill_list)

    # check the child process if it is still running
    if p.is_alive():
        print("launch is alive")
        time.sleep(2)
    
    '''
    This block is to use os api to run command line:

    # with os.popen('ros2 node list') as pipe:
    #     output = pipe.read()
    #     print(output)
    '''

    # according to the pid list to stop the pid, recommand to use terminate, for safety
    for i in range(len(proc_kill_list)):
        # load the process class
        kill_proc = psutil.Process(proc_kill_list[i])
        kill_proc.terminate()

    # while p.is_alive():
    #     print("launch is alive")
    #     time.sleep(2)
        
    print("Launched nodes are killed.")
    # close the child process, but actually when all of the launch started node processess are killed
    # the child process will close self, because it is not already "alive"
    p.terminate() 
    p.join()

if __name__=="__main__":
    main()