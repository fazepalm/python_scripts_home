import sys
import os
import traceback
import time
import datetime
import shutil

def getSelectedFolder():
    inFolder = ""
    if len(sys.argv) > 1:
        inFolder = sys.argv[1]
    else:
        print "No Input Folder Specified"
    return inFolder

def createArchiveFolder(inFolder):
    rootFolder = os.path.dirname(inFolder)
    archiveFolderPath = os.path.join(rootFolder, "_archive")
    if not os.path.exists(archiveFolderPath):
        os.makedirs(archiveFolderPath)
    return archiveFolderPath

def createDateFolder(archiveFolderPath):
    count = 1
    today = time.strftime("%Y%m%d")
    todayFolder = "%s-%s" % (today, "%03d" % (count))
    dateFolderPath = os.path.join(archiveFolderPath, todayFolder)
    while os.path.exists(dateFolderPath):
        count += 1
        todayFolder = "%s-%s" % (today, "%03d" % (count))
        dateFolderPath = os.path.join(archiveFolderPath, todayFolder)
    if not os.path.exists(dateFolderPath):
        os.makedirs(dateFolderPath)
    return dateFolderPath

def getLatestArchive(archiveFolderPath):
    folderList = [os.path.join(archiveFolderPath, d) for d in os.listdir(archiveFolderPath)]
    newestFolder = max(folderList, key=os.path.getmtime)
    return newestFolder

def createBackupDirectory(inFolder, dateFolderPath):
    print inFolder
    print dateFolderPath
    # if os.path.isdir()
    inFolderName = os.path.basename(inFolder)
    backupFolderPath = os.path.join(dateFolderPath, inFolderName)
    if not os.path.isdir(backupFolderPath):
        print "Copy %s to %s" % (inFolder, backupFolderPath)
        shutil.copytree(inFolder, backupFolderPath)
    else:
        print "%s Already Exists!" % (backupFolderPath)
    return backupFolderPath

if __name__ == "__main__":
    try:
        inFolder = getSelectedFolder()
        archiveFolderPath = createArchiveFolder(inFolder)
        dateFolderPath = createDateFolder(archiveFolderPath)
        backupDirectoryPath = createBackupDirectory(inFolder, dateFolderPath)
        print backupDirectoryPath
        latestArchiveFolder = getLatestArchive(archiveFolderPath)
        time.sleep(100)

    except:
        traceback.print_exc()
        time.sleep(100)
