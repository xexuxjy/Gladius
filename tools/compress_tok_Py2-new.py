# -*- coding: utf-8 -*-

import os
import sys
import struct
import operator
import binascii


def compressTok(filename, filename2, filename3, inputfile, debug=False):
    dic_strings = {} # dictionary with string and nr of appearances
    dic_lines = {} # dictionary with lines and nr of appearances
    list_file = []
    output = ""
	
    stringsDebugName = "./python3/stringsdebug.txt"
    if os.path.dirname(stringsDebugName) != "":
        if not os.path.exists(os.path.dirname(stringsDebugName)):
            os.makedirs(os.path.dirname(stringsDebugName))
    stringsdebug = open(stringsDebugName, 'w')

    with open(inputfile) as fin:
        for line in fin:
            if line.strip() == "":
                continue
            if line.startswith("//"):
                continue
    
            newline = ""
            words = line.split()
            for word in words:
                #stringsdebug.write(word)
                word = word.strip().rstrip(",")
                #stringsdebug.write(word)
                if word == "//": # skip rest of line after a comment
                    break
                if (word in dic_strings):
                    dic_strings[word] += 1
                else:
                    dic_strings[word] = 1
                newline += word + " "
            if newline in dic_lines:
                dic_lines[newline] += 1
            else:
                dic_lines[newline] = 1
            list_file += [newline]

    #stringsdebug.write("LF : "+str(list_file))

    absoffset = 0
    nrofStrings = 0
    sorted_strings = sorted(dic_strings.items(), key=operator.itemgetter(1,0), reverse=True)
    #sorted_strings = dic_strings.items()
    #stringsdebug.write(sorted_strings)
    for key, val in sorted_strings:
        dic_strings[key] = nrofStrings
        stringsdebug.write(key + " , "+str(val)+  " => " + hex(dic_strings[key]) + "\r")
        absoffset += len(key)
        nrofStrings += 1
    #print("nrofStrings*3: " + hex(nrofStrings*3))
    #print("absoffset: " + hex(absoffset))
        
    if os.path.dirname(filename) != "":
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
    output_rom = open(filename, 'wb')
	# write strings in file
    offset = nrofStrings*3
    for key, val in sorted_strings:
        output_rom.write(struct.pack('<H', int(offset)))
        offset += len(key)
        output_rom.write(struct.pack('<B', int(0)))
    for key, val in sorted_strings:
        string = key[:-1]
        
        ba1 = bytearray(string.encode('UTF-8'))
        ba1.append(ord(key[len(key)-1])+0x80)
        
        output_rom.write(ba1)
        

    linesDebugName = "./python3/linedebug.txt"
    if os.path.dirname(linesDebugName) != "":
        if not os.path.exists(os.path.dirname(linesDebugName)):
            os.makedirs(os.path.dirname(linesDebugName))
    linedebug = open(linesDebugName, 'w')
    absoffset = 0
    nrofLines = 0
    linesInByts = []
    sorted_lines = sorted(dic_lines.items(), key=operator.itemgetter(1,0), reverse=True)
    #print(sorted_lines)
    for key, val in sorted_lines:
        dic_lines[key] = nrofLines
        #print key, "=>", nrofLines
        linedebug.write(key + " => " + hex(dic_lines[key]) + "\r")
        #linedebug.write(key + " => " + str(dic_lines[key]) + "\r")
        lineInBytes = []
        words = key.split()
        for word in words:
            #print(word)
            byte1 = dic_strings[word] % 0x80
            if dic_strings[word] >= 0x80:
                byte1 += 0x80
                lineInBytes += [byte1]
                byte2 = dic_strings[word] >> 7
                lineInBytes += [byte2]
            else:
                lineInBytes += [byte1]
        absoffset += len(lineInBytes)
        nrofLines += 1
        linesInByts += [lineInBytes]
    #print("nrofLines*4: " + hex(nrofLines*4))
    #print("absoffset: " + hex(absoffset))
        
    if os.path.dirname(filename2) != "":
        if not os.path.exists(os.path.dirname(filename2)):
            os.makedirs(os.path.dirname(filename2))
    output_rom2 = open(filename2, 'wb')
	# write strings in file
    offset = nrofLines*4
    i = 0
    for key, val in sorted_lines:
        output_rom2.write(struct.pack('<H', int(offset)))
        words = key.split()
        line = linesInByts[i]
        offset += len(line)
        output_rom2.write(struct.pack('<B', int(0)))
        output_rom2.write(struct.pack('<B', int(len(words))))
        i += 1

	
    for bytes in linesInByts:
        output_rom2.write(bytearray(bytes))
        
		

    if os.path.dirname(filename3) != "":
        if not os.path.exists(os.path.dirname(filename3)):
            os.makedirs(os.path.dirname(filename3))
    output_rom3 = open(filename3, 'wb')
	# write line nrs in file
    i = 0
    data = []
    byte1 = 0
    byte2 = 0
    for line in list_file:
        byte2 = 0
        testvalue = dic_lines[line]
        byte1 = testvalue % 0x80
        if testvalue >= 128:
            byte1 += 0x80
            data += [byte1]
            byte2 = testvalue >> 7
            data += [byte2]
        else:
            data += [byte1]
        i += 1
        #print dic_lines[line], line, byte1, byte2

	
    output_rom3.write(bytearray(data))
	
    return output


if __name__ == "__main__":
    filename = ''
    filename2 = ''
    filename3 = ''
    inputfile = ''
    debugFlag = False

   
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-i":
            inputfile = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "-o":
            filename = sys.argv[i+1]
            filename2 = sys.argv[i+2]
            filename3 = sys.argv[i+3]
            i += 4
        elif sys.argv[i] == "-debug":
            filelist_on = 0
            debugFlag = True
            i += 2
        else:
            i += 1

    output = compressTok(filename, filename2, filename3, inputfile)
	
    print(output)
