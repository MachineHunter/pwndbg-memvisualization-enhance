import sys
import time
import interface
import threading

def snapshot():
    print('snap!')

if __name__ == '__main__':
    app = interface.MemoryApp()
    th_app = threading.Thread(target=interface.app_run, args=(app,))
    th_app.start()
    
    '''
    time.sleep(4)
    dic = {
            '.text': [],
            '.data': [],
            '.bss': [],
            'heap': [],
            'stack': [100, 100]
        }
    interface.set_address(app, dic)
    time.sleep(1)
    dic = {
            '.text': [],
            '.data': [],
            '.bss': [],
            'heap': [],
            'stack': []
        }
    interface.set_address(app, dic)
    '''