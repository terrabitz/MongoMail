import signal
import sys
from mongomail.mail_app import controller

if __name__ == '__main__':
    controller.start()
    print('Mail server started.')
    def signal_handler(signal, frame):
        print('Ctrl+C pressed. Exiting...')
        controller.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()