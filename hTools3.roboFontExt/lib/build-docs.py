import os
import shutil
import subprocess

def buildDocsHTML(sourceFolder, buildFolder, incremental=True, verbose=True):

    htmlFolder     = os.path.join(buildFolder, 'html')
    doctreesFolder = os.path.join(buildFolder, 'doctrees')

    # see `sphinx-build -h` for docs on sphinx options
    commands = ['/usr/local/bin/sphinx-build']

    # build all files (not just new and changed)
    if not incremental:
        commands += ['-a']

    # builder: html / pdf / epub / text / etc.
    commands += ['-b', 'html']

    # supress console warnings and errors
    if not verbose:
        commands += ['-Q']

    # define source and output folders
    commands += ['-d', doctreesFolder]
    commands += [sourceFolder, htmlFolder]

    # delete build folder
    if os.path.exists(buildFolder):
        shutil.rmtree(buildFolder)

    # run sphinx command
    p = subprocess.Popen(commands)
    stdout, stderr = p.communicate()

    if verbose:
        if stdout: print(stdout)
        if stderr: print(stderr)

# ----------
# build docs
# ----------

if __name__ == '__main__':

    baseFolder   = '/_code/hTools3' # os.path.dirname(__file__)
    docsFolder   = os.path.join(baseFolder, 'Docs')
    sourceFolder = os.path.join(docsFolder, 'source')
    buildFolder  = os.path.join(docsFolder, 'build')

    buildDocsHTML(sourceFolder, buildFolder, incremental=True, verbose=True)
