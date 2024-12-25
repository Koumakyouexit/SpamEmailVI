import subprocess
from subprocess import call
import sys

file_path = 'kome/miku.py'

def install_requirements(requirements_file):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install" ,"-r", requirements_file])
        print('Thành công')
    except subprocess.CalledProcessError as e:
        print('lỗi!')

subprocess.run(['python', file_path])

if __name__ == "__main__":
    requirements_file = "requirements.txt"
    install_requirements(requirements_file)
