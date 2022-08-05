import os
import importlib.machinery
import inspect


class Common(object):
    @staticmethod
    def get_class_name():
        cls_list = []
        dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modules')
        file_list = [f for f in os.listdir(dir_path) if '.py' in f]
        file_name_list = [f[:-3] for f in file_list]
        module = ''
        for file in file_list:
            file = os.path.join(dir_path, file)
            module = importlib.machinery.SourceFileLoader('all_module', file).load_module()
        for cls in inspect.getmembers(module, inspect.isclass):
            if cls[0].lower() in file_name_list:
                cls_list.append(cls)
        return cls_list
