import subprocess


if __name__ == '__main__':
    sys_cmd = 'start /wait cmd.exe cmd /k python main.py'
    subprocess.Popen(sys_cmd, shell=True)
