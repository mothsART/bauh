import os
import shutil
import subprocess
import sys
import traceback
from typing import List

from PyQt5.QtCore import QCoreApplication
from colorama import Fore

from bauh import __app_name__
from bauh.api.abstract.controller import SoftwareManager
from bauh.api.constants import CACHE_PATH, CONFIG_PATH
from bauh.commons.system import run_cmd
from bauh.view.util import resource


def notify_user(msg: str, icon_path: str = resource.get_path('img/logo.svg')):
    os.system("notify-send -a {} {} '{}'".format(__app_name__, "-i {}".format(icon_path) if icon_path else '', msg))


def restart_app(show_panel: bool):
    """
    :param show_panel: if the panel should be displayed after the app restart
    :return:
    """
    restart_cmd = [sys.executable, *sys.argv]

    if show_panel:
        restart_cmd.append('--show-panel')

    subprocess.Popen(restart_cmd)
    QCoreApplication.exit()


def get_distro():
    if os.path.exists('/etc/arch-release'):
        return 'arch'

    if os.path.exists('/proc/version'):
        if 'ubuntu' in run_cmd('cat /proc/version').lower():
            return 'ubuntu'

    return 'unknown'


def clean_app_files(managers: List[SoftwareManager]):
    print('[bauh] Cleaning configuration and cache files')
    for path in (CACHE_PATH, CONFIG_PATH):
        print('[bauh] Deleting directory {}'.format(path))
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print('{}[bauh] Directory {} deleted{}'.format(Fore.YELLOW, path, Fore.RESET))
            except:
                print('{}[bauh] An exception has happened when deleting {}{}'.format(Fore.RED, path, Fore.RESET))
                traceback.print_exc()

    if managers:
        for m in managers:
            m.clear_data()

    print('[bauh] Cleaning finished')
