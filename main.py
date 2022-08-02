from code.setting import Setting
from code.parse import case
import os


if __name__ == '__main__':
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, case)
    Setting.test_run(file_path)
