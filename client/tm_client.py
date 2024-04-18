import logging
import time
import shutil

from datetime import datetime

from pathlib import Path

from appconfig import AppConfig
from appconfig import app_config  # global variable, singleton

class MonitorFolder(object):

    def __init__(self, logger, config_default, config_section):
        self.logger: logging.Logger = logger
        # self.config_default = config_default
        # self.config_section = config_section
        self._monitored_pattern = config_section.get("monitored_pattern", config_default.get("monitored_pattern"))
        self._monitored_folder = config_section.get("monitored_folder", config_default.get("monitored_folder"))
        self._backup_folder = config_section.get("backup_folder", config_default.get("backup_folder"))
        self.logger.debug(self)

    def __str__(self) -> str:
        ret = f'_monitored_pattern: {self._monitored_pattern}, '
        ret += f'_monitored_folder: {self._monitored_folder}, '
        ret += f'_backup_folder: {self._backup_folder}'
        return ret

    def get_fnames_in_backup(self):
        path_backup = Path(self._backup_folder)
        return [f.name for f in path_backup.glob(self._monitored_pattern)]

    def get_files_in_monitored(self):
        path_backup = Path(self._monitored_folder)
        return list(path_backup.glob(self._monitored_pattern))

    def backup_file(self, f_from, backup_fname):
        self.logger.info(f'Backuping file {f_from.name} to {backup_fname}')
        full_path_backup = Path(self._backup_folder).joinpath(backup_fname)
        shutil.copyfile(f_from, full_path_backup)

    def check_folder(self):
        self.logger.debug('check_folder - BEGIN')
        fnames_in_backup = self.get_fnames_in_backup()
        self.logger.debug(f'fnames_in_backup: {fnames_in_backup }')
        files_to_be_checked = self.get_files_in_monitored()
        for f in files_to_be_checked:
            mtime_str = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y%m%d_%H%M%S")
            backup_fname = f'{f.stem}_{mtime_str}{f.suffix}'
            if backup_fname not in fnames_in_backup:
                self.backup_file(f, backup_fname)

class MonitorFolders(object):

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
        self.logger.debug('check_all_folders - BEGIN')
        for monitored_folder in self._monitored_folders:
            monitored_folder.check_folder()

    def monitor(self):
        self.init_all_folders()
        while True:
            self.check_all_folders()
            time.sleep(self.sleep_time)
