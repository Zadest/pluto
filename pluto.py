#! /usr/bin/env python3
# -*- coding:utf8 -*-

import logging, time, os, json, time
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler

class Pluto:
    config = {} 
    def __init__(self):
        self.observer = Observer()
        with open('./pluto.cf') as f:
            self.config = json.load(f)

    def run(self):
        event_handler = Handler()
        event_handler.setConfig(self.config)
        self.observer.schedule(event_handler, self.config['DIR'], recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nProgramm beendet : Manuell abgebrochen.")
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    Config = {}

    def setConfig(self,pConfig):
        logging.basicConfig(filename="pluto.log",level=logging.INFO,format='%(asctime)s [%(levelname)s] : %(message)s')
        logging.info('Pluto started')
        self.Config = pConfig
        logging.info(self.Config)

    def on_modified(self,event):
        if event.is_directory:
            return None
        logging.info( f'Recieved modified event - {event.src_path}')
        file_type = event.src_path.split('.')[-1].lower()
        if self.Config.get(file_type):
            newFullPath = self.Config.get(file_type)+'/'+event.src_path.split('/')[-1]
            logging.info(f'move {event.src_path} to {newFullPath}')
            historicalSize = -1
            while (historicalSize != os.path.getsize(event.src_path)):
                historicalSize = os.path.getsize(event.src_path)
                time.sleep(1)

            os.rename(event.src_path, newFullPath)
        elif file_type != 'swp' and file_type != 'part':
            with open("unknown-endings.json", "r") as f:
                lines = f.readlines()
            if len(lines) <= 2:
                lines.append('{\n')
                lines.append('\"'+file_type+'\" : \" \"')
                lines.append('}')
            else :
                lines.pop()
                lines.append('\"'+file_type+'\" : \" \"')
                lines.append('}')
            newLines = []
            for line in lines:
                newLines.append(line.replace(',',''))
            with open("unknown-endings.json","w") as f:
                f.write(newLines[0])
                for line in newLines[1:-2]:
                    if line != '\n':
                        f.write(line.strip()+',\n')
                f.write(newLines[-2]+'\n')
                f.write(newLines[-1]+'\n')

if __name__ == '__main__':
    pluto = Pluto()
    pluto.run()
    
