import subprocess
from time import sleep

commands = [
    'sudo systemctl stop elasticsearch.service',
    'sudo systemctl stop kibana',
    'sudo systemctl stop zookeeper',
    'sudo systemctl stop kafka',
    'free -h && sudo sysctl -w vm.drop_caches=3 && sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches && free -h'

]


for command in commands:
    try:
        result = subprocess.run(command, shell=True,check=True,text=True,capture_output=True)
        sleep(3)

        print(f"Running {command}\n{result}")
    except subprocess.CalledProcessError as error:
        print('Error happend while running command\nerror [{error}]')
    finally:
        print('completed .....')






