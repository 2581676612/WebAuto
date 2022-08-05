import os
import time
import core.base.parse as parse


class Report(object):
    def __init__(self):
        report_dir = os.path.join(parse.main_path, 'report')
        current_day = str(time.strftime('%y_%m_%d_%H_%M_%S', time.localtime()))
        self.report_path = os.path.join(report_dir, current_day)
        self.report_screen = os.path.join(self.report_path, 'screen')
        if not os.path.exists(self.report_screen):
            os.makedirs(self.report_screen)


Report = Report()
