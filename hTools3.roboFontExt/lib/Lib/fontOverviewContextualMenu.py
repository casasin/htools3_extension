import os
from mojo.events import addObserver

libFolder = os.getcwd()
menusFolder = os.path.join(libFolder, 'menus')

def collectScripts(path):
    if os.path.split(path)[-1].startswith('.'):
        return
    if os.path.isdir(path):
        d = []
        for name in os.listdir(path):
            if name.startswith('.'):
                continue
            p = os.path.join(path, name)
            if os.path.isfile(p):                
                with open(p, mode='r', encoding='utf-8') as F:
                    lines = F.readlines()
                firstLine = lines[0]
                name = firstLine.split(':')[-1].strip()
            d.append([name, collectScripts(p)])
    else:
        d = path
    return d

class FontOverviewContextualMenu:

    def __init__(self):
        addObserver(self, "fontOverviewAdditionContextualMenuItems", "fontOverviewAdditionContextualMenuItems")
        self.scripts = collectScripts(menusFolder)

    def fontOverviewAdditionContextualMenuItems(self, notification):
        menuItems = self.collectMenuItems(menusFolder)
        notification["additionContextualMenuItems"].extend(menuItems)

    def collectMenuItems(self, path):
        if os.path.split(path)[-1].startswith('.'):
            return
        if os.path.isdir(path):
            d = []
            for name in os.listdir(path):
                if name.startswith('.'):
                    continue
                p = os.path.join(path, name)
                if os.path.isfile(p):                
                    with open(p, mode='r', encoding='utf-8') as F:
                        lines = F.readlines()
                    firstLine = lines[0]
                    name = firstLine.split(':')[-1].strip()
                d.append([name, self.collectMenuItems(p)])
        else:
            d = self.optionCallback
        return d

    def optionCallback(self, sender):
        print(sender, sender.get())

if __name__ == '__main__':

    FontOverviewContextualMenu()
