import os
import subprocess

executable = ['./user.sh']

fileStat = os.stat(executable[0])
sudo = ['sudo', '-u', '#' + str(fileStat.st_uid)]

out = subprocess.Popen(sudo + executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = out.communicate()
stdout = stdout.decode('utf-8')
print(stdout)
