#!/usr/bin/python3
import subprocess
import pathlib
import sys

# Expected order of arguments SECONDS MINUTES HOURS DAYS


def set_timer():
    currentPath = str(pathlib.Path(__file__).parent.absolute())
    out = subprocess.Popen([currentPath + '/calculateTime.sh'] + sys.argv[1:], stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    stdout = stdout.decode('utf-8')

    if stdout == "Invalid timer parameters":
        return stdout

    strSplit = stdout.split(':', 1)
    seconds = strSplit[0]
    returnMessage = strSplit[1]

    # Run in background
    subprocess.Popen([currentPath + '/timeout.sh', seconds],
                     cwd="/",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

    return returnMessage.strip()


if __name__ == '__main__':
    print(set_timer())
