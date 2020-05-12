import subprocess

out = subprocess.Popen(['./script.sh'], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)

stdout, stderr = out.communicate()
stdout = stdout.decode('utf-8')
print(stdout)
