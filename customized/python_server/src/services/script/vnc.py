import time

from src.pkg.utils.common import run_command
import uuid


def restart():
    uid = uuid.uuid4().hex
    run_command('kill $(ps aux | grep \'x11vnc -storepasswd\' | awk \'{print $2}\')')
    time.sleep(3)
    run_command('x11vnc -storepasswd '+uid+' /home/seluser/.vnc/passwd')
    return uid
