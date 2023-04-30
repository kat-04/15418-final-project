#!/usr/bin/env python3
import sys
import os
import re
import difflib

def main():
    os.system("rm -rf /tmp/output-files/")
    os.system("mkdir /tmp/output-files/")
    os.system("mkdir /tmp/output-files/logs/")

    args = sys.argv[1:]

    if (len(args) != 4):
        print("Usage: ./checker testCase version numFrames sideLen\n")
        return 1


    log_file = f'logOutput.txt'

    testCase = args[0]
    version = args[1]
    numFrames = args[2]
    sideLen = args[3]

    cmdSeq = f'./GOL3D {testCase} {numFrames} {sideLen} seq check'
    print(cmdSeq)
    seqRet = os.system(cmdSeq)
    assert seqRet == 0, 'ERROR -- seq GOL exited with errors'

    cmdPar = f'./GOL3D {testCase} {numFrames} {sideLen} {version} check'
    parRet = os.system(cmdPar)
    assert parRet == 0, 'ERROR -- par GOL exited with errors'

    # seq output already sorted first by x, then y, then z

    # sort par output for each frame and compare
    for i in range(1, int(numFrames) + 1):
        # open frame files
        parFrame = open(f'/tmp/output-files/{version}/frame{i}.txt')
        seqFrame = open(f'/tmp/output-files/seq/frame{i}.txt')

        parTuples = []
        parSortedLines = []
        parLines = parFrame.readlines()
        seqLines = seqFrame.readlines()
        for l in parLines:
            parTuples.append(l.split(' '))
        
        res = sorted(parTuples, key = lambda sub: (int(sub[0]), int(sub[1]), int(sub[2])))
        for l in res:
            parSortedLines.append(l[0] + " " + l[1] + " " + l[2])


        errorFlag = False
        diff = difflib.unified_diff(seqLines, parSortedLines, fromfile=f'seqFrame{i}', tofile=f'parFrame{i}')
        if (diff): 
            errorFlag = True
            log = open(f'/tmp/output-files/logs/frame{i}.txt', "w")
            log.writelines(diff)

        seqFrame.close()
        parFrame.close()


    if (errorFlag):
        print("CHECKER RESULT: issues detected, check log files")
    else: 
        print("CHECKER RESULT: correct")
    return 0

if __name__ == "__main__":
    main()