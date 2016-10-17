import subprocess
import time

def main(self):
    subprocess('irsend SEND_ONCE RGBLED power', shell=True)
    time.sleep(3)
    subprocess('irsend SEND_ONCE RGBLED white0', shell=True)

if __name__ == '__main__':
    main()
