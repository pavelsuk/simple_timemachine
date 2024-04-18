import logging
import time


from appconfig import AppConfig
from appconfig import app_config  # global variable, singleton

class MonitorFolder(object):

    def __init__(self, logger):
        self.logger = logger
        self.config_default = None
        self.config_bank = None
        self._gc = None
        self._sh_rules = None
        self._sh_output = None

    def __init__(self, logger, config_default, config_folder):
        self.logger = logger
        self.config_default = config_default
        self.config_4_folder = config_folder

    def check_folder(self):
        self.logger.debug('check_folder - BEGIN')

class MonitorFolders(object):
    def __init__(self) -> None:
        pass

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.config_default = config["default"]
        self.sleep_time = config["sleep_time"]
        self._monitored_folders = list()

    def init_all_folders(self):
        self.logger.debug('init_all_folders - BEGIN')
        folders = self.config["folders"]
        self.logger.debug(f'all_folders {folders}')

        for one_folder in folders:
            config_folder = self.config[one_folder]
            monitored_folder = MonitorFolder(self.logger, self.config_default, config_folder)
            self._monitored_folders.append(monitored_folder)

    def check_all_folders(self):
        self.logger.debug(f'check_all_folders - BEGIN')
        for monitored_folder in self._monitored_folders:
            monitored_folder.check_folder()

    def monitor(self):
        self.init_all_folders()
        while True:
            self.check_all_folders()
            time.sleep(self.sleep_time)
