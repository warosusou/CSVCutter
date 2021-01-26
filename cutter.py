import csv
import os
import datetime
import sys
from os import makedirs, path


def main() -> None:
    _CSVDIR = 'CSV'
    if(not path.exists(_CSVDIR)):
        makedirs(_CSVDIR)
    while(True):
        files = list(filter((lambda f :  os.path.isfile(os.path.join(_CSVDIR, f)) and f.endswith('.csv')),os.listdir(_CSVDIR)))
        if(len(files) == 0):
            print("No CSV files found")
            exit(0)
        print('Choose a CSVfile\n----')
        for f in files:
            print(f)
        print('----')
        userInput = input()
        if(userInput == 'exit'):
            exit(0)
        fileName = os.path.join(_CSVDIR,userInput.strip())
        if(os.path.exists(fileName) and path.isfile(fileName) and fileName.endswith('.csv')):
            break
        else:
            print('Error! Enter correct file name')
    operate(fileName,24*60*60)
    return

def operate(targetFile : str,duration : int) -> None:
    with open(targetFile,'r') as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
    if(len(lines) == 0 or len(lines[0]) == 0):
        print('Can\'t handle this file')
        exit(1)
    if(len(sys.argv) == 2 and sys.argv[1] == '--ig' and len(lines) > 1):
        lines.remove(lines[0])
    print(len(lines))
    print('begin ' + str(datetime.datetime.fromtimestamp(int(lines[0][0]))))
    print('end ' + str(datetime.datetime.fromtimestamp(int(lines[len(lines) - 1][0]))))
    #Start output
    targetFileBaseName = path.splitext(path.basename(targetFile))[0]
    dirName = targetFile[:targetFile.rfind('.')]
    makedirs(name=dirName,exist_ok=True)
    start = int(lines[0][0])
    end = start + duration
    writingFile = None
    filesWrote = -1
    for line in lines:
        if(filesWrote > 50):
            break
        if(writingFile == None):
            filesWrote += 1
            writingFile = open(path.join(dirName , targetFileBaseName + '_' + str(filesWrote) + '.csv'),'w')
        if(int(line[0]) <= end):
            writeline = ''
            for data in line:
                writeline += (str(data) + ',')
            writingFile.write(writeline[:writeline.rfind(',')] + '\n')
        else:
            writingFile.close()
            writingFile = None
            start = int(line[0])
            end = start + duration
    if(writingFile != None):
        writingFile.close()
    print(str(filesWrote + 1) + ' files created')
    return


if (__name__ == "__main__"):
    main()
