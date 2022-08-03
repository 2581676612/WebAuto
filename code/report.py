import os
import time


class Report(object):
    def __init__(self):
        report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report')
        current_day = str(time.strftime('%y_%m_%d_%H_%M_%S', time.localtime()))
        self.report_path = os.path.join(report_dir, current_day)
        self.report_screen = os.path.join(self.report_path, 'screen')
        if not os.path.exists(self.report_screen):
            os.makedirs(self.report_screen)


Report = Report()
