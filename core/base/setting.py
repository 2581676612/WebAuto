import os
import pytest
import core.base.parse as parse
from core.base.report import Report


class Setting(object):
    @staticmethod
    def test_run(file=''):
        file_name = file.split('\\')[-1].split('.')[0].split('/')[-1]
        # 记录详细日志、生成HTML文件、日志显示颜色、报告显示控制台输出
        cmd_line = ['-sv', '--self-contained-html', '--color=yes', '--capture=sys']
        if '.txt' in file:
            with open(file, 'r') as f:
                test_file_list = f.readlines()
                for t in test_file_list:
                    t = t.strip()
                    if t[0] != '#':
                        cmd_line.append(os.path.join(parse.main_path, t))
        else:
            cmd_line.append(file)
        report_dir = os.path.join(Report.report_path, f'{file_name}.html')
        print(report_dir)
        cmd_line.append(f'--html={report_dir}')
        print(cmd_line)
        pytest.main(cmd_line)


Setting = Setting()
