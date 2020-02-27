import os
from mojo.UI import HelpWindow
baseFolder = os.path.dirname(os.path.dirname(__file__))
devDocsIndexPath = os.path.join(baseFolder, 'html', 'dev', 'build', 'html', 'index.html')
print(devDocsIndexPath, os.path.exists(devDocsIndexPath))
HelpWindow(devDocsIndexPath)
