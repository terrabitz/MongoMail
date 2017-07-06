import signal
import sys
import time
from mongomail.mail_app import controller

if __name__ == '__main__':
    controller.start()
    print('Mail server started.')
    print('Press Ctrl+C to stop')

    def stop_service():
        print('Ctrl+C pressed. Exiting...')
        controller.stop()
        sys.exit(0)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_service()
    # def signal_handler(signal, frame):
    #   stop_service()
    #
    # signal.signal(signal.SIGINT, signal_handler)
    #
    # signal.pause()
