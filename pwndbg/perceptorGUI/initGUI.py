import sys
import threading
import pwndbg.perceptorGUI.memGUI
import logging

logging.getLogger("kivy").disabled = True


def init():
    global app    
    app = pwndbg.perceptorGUI.memGUI.MemoryApp()    
    th_app = threading.Thread(target=pwndbg.perceptorGUI.memGUI.app_run, args=(app,), daemon=True)
    th_app.start()

def get_instance():
    global app
    return app
