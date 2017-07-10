import signal
import sys
from mongomail.mail_app import controller

def stop_service():
    print('Ctrl+C pressed. Exiting...')
    controller.stop()
    sys.exit(0)

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     stop_service()
def signal_handler(signal, frame):
    stop_service()


controller.start()
print('Mail server started.')
print('Press Ctrl+C to stop')

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
