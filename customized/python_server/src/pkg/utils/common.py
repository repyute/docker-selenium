import datetime as dt
import errno
import json
import os
import re
import pprint
import logging
import subprocess
import time
from typing import List, Dict


def myprint(msg, head=None):
    if msg is None:
        return
    if head == 1:
        logging.info('\n\n=================================================================== ')
        logging.info(Colors.HEADER + Colors.BOLD + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 2:
        logging.info('\n')
        logging.info(Colors.OKBLUE + ((pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC))
    elif head == 3:
        logging.info(Colors.OKBLUE + "- " + ((pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC))
    elif head == 4:
        logging.info("- " + (pprint.pformat(msg) if not isStr(msg) else msg))
    elif head == 11:
        logging.info(Colors.WARNING + "- " + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 12:
        logging.info(Colors.OKGREEN + "- " + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 13:
        logging.info(Colors.FAIL + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    else:
        logging.info("- " + (pprint.pformat(msg) if not isStr(msg) else msg))


def getTimestamp(seconds_offset=None):
    '''
    Current TS.
    Format: 2019-02-14T12:40:59.768Z  (UTC)
    '''
    delta = dt.timedelta(days=0)
    if seconds_offset is not None:
        delta = dt.timedelta(seconds=seconds_offset)

    ts = dt.datetime.utcnow() + delta
    ms = ts.strftime('%f')[0:3]
    s = ts.strftime('%Y-%m-%dT%H:%M:%S') + '.%sZ' % ms
    return s


def init_logger(log_file):
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    root_logger.addHandler(console_handler)


def get_json_file(path):
    if os.path.isfile(path):
        with open(path, 'r') as file:
            return json.loads(file.read())
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)


def get_json_file_cls(path, c):
    if os.path.isfile(path):
        with open(path, 'r') as file:
            return json.loads(file.read(), object_hook=lambda d: c(**d))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)


def jsonToClass(s: str, c):
    return json.loads(s, object_hook=lambda d: c(**d))


def jsonToDict(data):
    return json.loads(data)


def write_json_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def dict_to_json(data):
    return json.dumps(data)


def get_file_extension(file):
    filename, extension = os.path.splitext(file)
    return extension


def readFileAsString(file):
    with open(file, 'r') as file:
        return file.read()


def writeFileFromString(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()


def keyExists(key, d):
    if key in d.keys():
        return True
    else:
        return False


def isJson(s: str):
    try:
        json.loads(s)
    except ValueError:
        return False
    return True


def parseJson(s: str):
    try:
        return json.loads(s)
    except ValueError:
        return False


def isStr(s):
    return isinstance(s, str)


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def Pprint(s):
    return s if isinstance(s, str) else pprint.pformat(s)


def Wait(t):
    myprint("Waiting for " + Pprint(t) + " seconds")
    time.sleep(t)


def Command(command: List, ignore_exit_code=False, working_directory='.'):
    myprint("Command: " + ' '.join(command))
    ds = subprocess.Popen(command, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd=working_directory)
    rc = ds.returncode
    myprint(ds.stderr, 13)
    while True:
        output = ds.stdout.readline()
        if output == b'' and ds.poll() is not None:
            break
        if output:
            myprint("Console: " + output.strip().decode("utf-8"))
    rc = ds.returncode

    if rc == 0:
        myprint("Command return code: " + str(rc), 11)
    elif ignore_exit_code:
        myprint("Command failed with return code: " + str(rc) + ". Continuing as ignore_exit_code is true", 11)
    else:
        myprint("Command failed with return code: " + str(rc), 13)
        raise RuntimeError("Command failed with return code: " + str(rc) + ". For more details check above logs")
    return rc


def CommandOutput(command: str, working_directory='.'):
    myprint("Command: " + command)
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory).stdout
    return res.decode("utf-8") if isinstance(res, bytes) else res


def getRepoNameFromUrl(repo: str):
    return os.path.splitext(os.path.basename(repo))[0]


def getGitDirAndWorkTree(repo_path):
    git_dir = '--git-dir=' + repo_path + '/.git'
    git_work_tree = '--work-tree=' + repo_path
    return git_dir, git_work_tree


def match(reg, st):
    regex = r".*(%s).*" % re.escape(reg)
    m = re.match(regex, st, re.DOTALL)
    return True if m else False


def getTimeInSec():
    return round(time.time() * 1000)


def timeDiff(prev_millis):
    curr_millis = getTimeInSec()
    diff = curr_millis - prev_millis
    seconds, milliseconds = divmod(diff, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return curr_millis, pPrint(hours) + " hours, " + pPrint(minutes) + " minutes, " + pPrint(
        round(seconds + milliseconds / 1000, 2)) + " seconds"


def pPrint(s):
    return s if isinstance(s, str) else pprint.pformat(s)


def getValue(s: str, d: Dict):
    if s in d:
        return d[s]
    else:
        return None


def run_command(cmd):
    result = subprocess.Popen(cmd, shell=True, check=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)
