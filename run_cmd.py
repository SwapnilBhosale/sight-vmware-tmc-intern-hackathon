import subprocess

command = './darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()
output = process.stdout.read()
print(output)
