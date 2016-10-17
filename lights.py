import subprocess
import sys
import time

def main():
    if (sys.argv[1] and sys.argv[1] == 'sleep'):
        wakeup()
    else:
        sleep()

def wakeup():
    subprocess.call('irsend SEND_ONCE RGBLED power', shell=True)
    time.sleep(1)
    subprocess.call('irsend SEND_ONCE RGBLED white0', shell=True)

def sleep():
    subprocess.call('irsend SEND_ONCE RGBLED power', shell=True)
    time.sleep(1)
    subprocess.call('irsend SEND_ONCE RGBLED red1', shell=True)

if __name__ == '__main__':
    main()
