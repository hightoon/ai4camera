import time
import subprocess


ONGOING_TASKS = []
# all task starter commands
FACE_RECOGNITION = [
    'python',
    '/home/haitong/machinelearning/py-faster-rcnn/tools/main.py'
]
PVA_DETECT = [
    'python',
    '/home/haitong/machinelearning/other_nets/pva-faster-rcnn/tools/main.py',
    '--cfg',
    '/home/haitong/machinelearning/other_nets/pva-faster-rcnn/models/pvanet/cfgs/submit_160715.yml'
]
PVA_MATCH

def main():
    p = subprocess.Popen(PVA_DETECT)
    ONGOING_TASKS.append(p)
    print ONGOING_TASKS
    time.sleep(15)
    try:
        p = ONGOING_TASKS.pop()
    except:
        print 'no task ongoing'
    else:
        p.terminate()
        print p, 'is dead'

if __name__ == '__main__':
    main()
