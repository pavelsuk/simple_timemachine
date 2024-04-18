import argparse
import logging

from appconfig import app_config  # global variable, singleton
# pip install appconfig-json
# Alternatively, use test channel
# pip install -i https://test.pypi.org/simple appconfig-json -U --no-cache-dir

class TimeMachineApp(object):

    PGM_VERSION = '0.0.1'

    def __init__(self):
        pass

    def parse_args(self):
        retVal = True

        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser(description='Description of the program')

        # TODO: change the default command to something meaningful
        ap.add_argument(
            "command",
            choices=['run'], nargs='?',
            help="command (run) Default: run",
            default='run')

        ap.add_argument(
            "-f",
            "--file",
            help="config file (either full path or relative to the current dir)",
            default=None)

        ap.add_argument(
            "-l",
            "--logconfig",
            help="path to logging config file",
            default=None)

        ap.add_argument(
            "-g",
            "--group",
            help="section group in the config file that should be used",
            default=None)

        ap.add_argument(
            "-x",
            "--xyz",
            help="specific argument should be processed",
            default=None)

        ap.add_argument(
            "-v",
            "--verbosity",
            help="level of verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) Default: DEBUG",
            default='DEBUG')

        args = ap.parse_args()

        verb_choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        verbose_lvl = 'DEBUG'
        self._verbose_lvl = verbose_lvl
        if (args.verbosity):
            verbose_lvl = args.verbosity.upper()
            if (verbose_lvl in verb_choices):
                self._verbose_lvl = verbose_lvl
            else:
                print('Verbosity must be one of the following values: DEBUG, INFO, WARNING, ERROR, CRITICAL')
                retVal = False

        self._command = args.command
        self._file = args.file
        self._logconfig = args.logconfig
        self._group = args.group
        self._xyz = args.xyz

        app_config.init(
            logger_config_file=self._logconfig,
            config_file=self._file,
            config_group=self._group,
            logger_verbosity=self._verbose_lvl)

        self.config = app_config.config
        self.logger = app_config.logger

        if (not retVal):
            ap.print_help()

        return retVal

    def run(self):
        pass

    def main(self):
        if (self.parse_args()):
            if (self._command == 'run'):
                self.run()
            else:
                self.logger.warning('Unknown command : {}'.format(self._command))

            self.logger.info('Job finished')


if __name__ == "__main__":
    runner = TimeMachineApp()
    runner.main()
