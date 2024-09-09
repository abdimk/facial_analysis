import subprocess
from time import sleep

commands = [
    'sudo systemctl start elasticsearch.service',
    'sudo systemctl start kibana',
    'sudo systemctl start zookeeper',
    'sudo systemctl start kafka'

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






