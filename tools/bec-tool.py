# -*- coding: utf-8 -*-

import os
import sys
import struct
import operator
import argparse
import time
import hashlib
import gladiushashes
import queue
import threading
from collections import namedtuple
from os import listdir,walk
from os.path import isfile, join, relpath,basename,commonpath,abspath,realpath,normpath,dirname

###########################################################################################################################################################


CRCTable =[
0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,
0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988, 0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,
0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,
0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172, 0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,
0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,
0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924, 0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,
0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,
0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e, 0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,
0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,
0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0, 0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,
0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,
0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a, 0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,
0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,
0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc, 0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,
0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,
0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236, 0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,
0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,
0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38, 0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,
0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,
0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2, 0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,
0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,
0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94, 0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d,
]

    
def computeFileHash(name):
    length = len(name)
    hashVal = 0
    i = 0
    while (length > 0):
        currentChar = ord(name[i])
        lookupKey = (hashVal ^ (currentChar))& 0xff         
        hashVal = CRCTable[lookupKey] ^ (hashVal >> 8)
        length -= 1
        i+=1;
 
    return hashVal
    

    


###########################################################################################################################################################

def scanFiles(dir):
    scannedRomMap = []
    for root, directories, files in os.walk(dir, topdown=False):
        for name in files:
            #print(relpath(os.path.join(root,name),dir))
            fullName = relpath(os.path.join(root,name),dir)
            romSection = RomSection.fromList([fullName,"nothing","0","0",0,0,0,0,0])
            scannedRomMap.append(romSection)

    return scannedRomMap
    

def readFileList(becmap):
    dir = os.path.dirname(becmap)
    scannedData = scanFiles(dir)
    fileListData = []
    
    with open(becmap) as fin:
        for line in fin:
            words = line.split()
            if len(words) == 3:
                fileAlignment = int(words[0], 16)
                nrOfFiles = int(words[1], 16)
                headerMagic = int(words[2], 16)
            else:
                words_temp = line.split("\"") # filename, filename2
                words = [words_temp[1]] + [words_temp[3]] + words_temp[4].split() # ?, offset, flags?, filesize
                if len(words) == 9:
                    romSection = RomSection.fromList(words)
                    #print(romSection.name)
                    fileListData.append(romSection)
                      
    #print(romSections)
    diffList = diffFiles(fileListData,scannedData)
    print("fileListData "+str(len(fileListData))+" scannedData "+str(len(scannedData))+"  diffList "+str(len(diffList)))

def diffFiles(fileListData,scannedData):
    fileListDataDictionary = {}
    scannedDataDictionary = {}
    for romData in fileListData:
        fileListDataDictionary[romData.name] = romData
    for romData in scannedData:
        scannedDataDictionary[romData.name] = romData


    scannedSet = set(scannedDataDictionary.keys())
    fileListSet = set(fileListDataDictionary.keys())

    #scannedList = list(scannedDataDictionary.keys()).sort()
    #fileListList = list(fileListDataDictionary.keys()).sort()

    scannedList = list(scannedDataDictionary)
    fileListList = list(fileListDataDictionary)
    
    scannedList.sort()
    fileListList.sort()


    writeListToFile("scanned.txt",scannedList)
    writeListToFile("fileListSet.txt",fileListList)

    newFiles = scannedSet - fileListSet
    #for file in newFiles :
        #print(file)
    return newFiles

def writeListToFile(name,data):
        outFile = open(name, 'w')
        for item in data:
            outFile.write(str(item))
            outFile.write("\n")       
            
        outFile.flush()
        outFile.close()



# PACK BEC-ARCHIVE
###########################################################################################################################################################

MAX_NR_OF_THREADS = 1
file_queue = queue.Queue()


def ReadSection(file, addr, size, debug=False):
    file.seek(addr)
    return file.read(size)

def WriteSectionInFile(fByteArray, dirname, filename, addr, size, debug=False):
    filename2 = dirname + filename
    if not os.path.exists(os.path.dirname(filename2)):
        os.makedirs(os.path.dirname(filename2))
    outFile = open(filename2, 'wb')
    outFile.write(fByteArray)
    outFile.flush()
    outFile.close()

    #print("Write out file " + filename2)

def file_worker():
    while True:
        item = file_queue.get()
        if item is None:
            break
        fByteArray, dirname, filename, addr, size = item
        WriteSectionInFile(fByteArray, dirname, filename, addr, size)
        file_queue.task_done()

def GetFilenameOfFile(file, addr, size, pathhash, i, debug=False):
    if pathhash in gladiushashes.pathhashes:
        outfilename = gladiushashes.pathhashes[pathhash]
    else:
        file.seek(addr)
        fByteArray = file.read(size)
        m = hashlib.md5()
        m.update(fByteArray)
        md5 = m.hexdigest()
        if md5 in gladiushashes.hashes:
            outfilename = gladiushashes.hashes[md5]
        else:
            outfilename = GetNumberedFilenameOfFile(file, addr, i)
	
    return outfilename

def GetNumberedFilenameOfFile(file, Offset, i):
    filename = ""
    if ReadHWord(file, Offset) == 0x2f2f:
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x0D0A2F2F):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x0D0A0D0A) and (ReadHWord(file, Offset+4) == 0x2F2F):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x436F7079) and (ReadWord(file, Offset+4) == 0x72696768):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x56455253):
        filename = str(i) + ".vers"
    elif (ReadWord(file, Offset) == 0x50545450):
        filename = str(i) + ".pttp"
    elif (ReadWord(file, Offset) == 0x50414B31):
        filename = str(i) + ".pak1"
    elif (ReadWord(file, Offset) == 0x23233832) and (ReadWord(file, Offset+4) == 0x32300D0A):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x1D200000):
        filename = str(i) + ".bin"
    elif (ReadWord(file, Offset) == 0x504D5332):
        filename = str(i) + ".pms2"
    elif (ReadWord(file, Offset) == 0x40656368) and (ReadWord(file, Offset+4) == 0x6F206F66):
        filename = str(i) + ".bat"
        
    elif (ReadWord(file, Offset) == 0x504F5309):
        filename = str(i) + ".pos"
    elif (ReadWord(file, Offset) == 0x0D0A6675):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x4C4F4341) and (ReadWord(file, Offset+4) == 0x544F5253):
        filename = str(i) + ".locators"
    elif (ReadWord(file, Offset) == 0x312C2242) and (ReadWord(file, Offset+4) == 0x6174746C):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x66756E63) and (ReadWord(file, Offset+4) == 0x74696F6E):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x52454D20) and (ReadWord(file, Offset+4) == 0x2D2D2047):
        filename = str(i) + ".bat"
    elif (ReadWord(file, Offset) == 0x53554254) and (ReadWord(file, Offset+4) == 0x49544C45):
        filename = str(i) + ".subs.txt"
    elif (ReadWord(file, Offset) == 0x53474F44):
        filename = str(i) + ".sgod"
    elif (ReadWord(file, Offset) == 0x0D0A0D0A):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x4E554D45) and (ReadWord(file, Offset+4) == 0x44474553):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x4E554D43) and (ReadWord(file, Offset+4) == 0x52454449):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x01000000):
        filename = str(i) + ".bin"
    elif (ReadWord(file, Offset) == 0x02000000):
        filename = str(i) + ".bin"
    elif (ReadWord(file, Offset) == 0x4E414D45):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x200D0A2F):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x50415448):
        filename = str(i) + ".bat"
    elif (ReadWord(file, Offset) == 0x0D0A4E41):
        filename = str(i) + ".txt"
    elif (ReadHWord(file, Offset) == 0x2E2E) and (ReadByte(file, Offset+2) == 0x5C):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x54494E54) and (ReadWord(file, Offset+4) == 0x494E473A):
        filename = str(i) + ".tinting.txt"
    elif (ReadWord(file, Offset) == 0x0D0A2066):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x4D4F4449) and (ReadWord(file, Offset+4) == 0x54454D53):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x5343454E) and (ReadWord(file, Offset+4) == 0x453A0909):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x496E7465) and (ReadWord(file, Offset+4) == 0x72666163):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x4C656167) and (ReadWord(file, Offset+4) == 0x75655374):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x5C70726F) and (ReadWord(file, Offset+4) == 0x6A656374):
        filename = str(i) + ".txt"
    elif (ReadHWord(file, Offset) == 0x0D0A):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x5041583A):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x3A204765):
        filename = str(i) + ".bat"
    elif (ReadWord(file, Offset) == 0x6275696C) and (ReadWord(file, Offset+4) == 0x6470616B):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x5363686F) and (ReadWord(file, Offset+4) == 0x6F6C5374):
        filename = str(i) + ".txt"
    elif (ReadWord(file, Offset) == 0x40000000):
        filename = str(i) + ".mih"
    else:
        filename = str(i) + ".bin"

    return filename

def ReadWord(file, Offset):
    file.seek(Offset)
    data = file.read(4)
    word, = struct.unpack(">I", data)
    return word

def ReadHWord(file, Offset):
    file.seek(Offset)
    data = file.read(2)
    word,  = struct.unpack(">H", data)
    return word

def ReadByte(file, Offset):
    file.seek(Offset)
    data = file.read(1)
    word,  = struct.unpack("<B", data)
    return word

###########################################################################################################################################################


def diagnose(filename, filedir, outFileList, gc,demobec,debug=False):
    file = open(filename, "rb+")
    header_output = diagnose2(file, filedir, gc,demobec,debug)
    
    headerfilename = filedir + outFileList
    if not os.path.exists(os.path.dirname(headerfilename)) and os.path.dirname(headerfilename):
        os.makedirs(os.path.dirname(headerfilename))
    fheader = open(headerfilename, 'w')
    fheader.write(header_output)

def diagnose2(file, filedir, gc,demobec,debug=False):
    output = ""

    BecHeader = namedtuple('BecHeader', ['FileAlignment', 'NrOfFiles', 'HeaderMagic'])
    
    if demobec == 1 :
       file.seek(0x4) # bec
       data = file.read(4)
       numFiles = struct.unpack('<I', data)[0]
       makeData = [0,numFiles,0]
       header = BecHeader._make(makeData)
    else:
        file.seek(0x6)
        data = file.read(10)
        header = BecHeader._make(struct.unpack('<HII', data))

    print("Nr of Files in the bec-file: " + str(header.NrOfFiles))
    print("File Alignment: " + str(header.FileAlignment))
    print("IsGC : "+str(gc)+" IsDemo: "+str(demobec))
    output += hex(header.FileAlignment) + " " + hex(header.NrOfFiles) + " " + hex(header.HeaderMagic) + "\n"
    
    PathHash = []
    DataOffset = []
    OffsetCorrection = []
    Data3 = []
    DataSize = []
    CheckSums1 = []
    CheckSums2 = []
    FileEntry = namedtuple('FileEntry', ['PathHash', 'DataOffset', 'correction0', 'correction1', 'correction2', 'Data3', 'DataSize'])
    for i in range(header.NrOfFiles):
        data = file.read(0x10) # file.seek(0x10+0x10*i)
        entry = FileEntry._make(struct.unpack('<IIBBBBI', data))

        PathHash += [entry.PathHash]
        DataOffset += [entry.DataOffset]
        correction = (entry.correction2 << 16) + (entry.correction1 << 8) + (entry.correction0 << 0)
        OffsetCorrection += [correction]
        Data3 += [entry.Data3] # 0 or 2
        DataSize += [entry.DataSize]
	
    for i in range(header.NrOfFiles):
        if OffsetCorrection[i] > 0: # PS2 version (checksum after zlib file)
            Offset = DataOffset[i] + OffsetCorrection[i]
        else: # GC version (checksum after uncompressed file)
            Offset = DataOffset[i] + (header.FileAlignment - 1)
            Offset &= (0x100000000 - header.FileAlignment)
            Offset += DataSize[i]
        file.seek(Offset)
        data = file.read(8)
        CheckSum1, CheckSum2 = struct.unpack("<II", data)
        CheckSums1 += [CheckSum1]
        CheckSums2 += [CheckSum2]
    
    for i in range(header.NrOfFiles):
        Offset = DataOffset[i] + OffsetCorrection[i] + (header.FileAlignment - 1)
        if OffsetCorrection[i] > 0:
            Offset += 8
        Offset &= (0x100000000 - header.FileAlignment)
		
        filename = GetFilenameOfFile(file, Offset, DataSize[i], PathHash[i], i)
        fByteArray = ReadSection(file, Offset, DataSize[i])
        WriteSectionInFile(fByteArray, filedir, filename, Offset, DataSize[i])
        #file_queue.put((fByteArray, filedir, filename, Offset, DataSize[i],))
		
        filename2 = "zlib/" + filename + ".zlib"
        if OffsetCorrection[i] > 0:
            fByteArray = ReadSection(file, DataOffset[i], OffsetCorrection[i])
            WriteSectionInFile(fByteArray, filedir, filename2, DataOffset[i], OffsetCorrection[i])
            #file_queue.put((fByteArray, filedir, filename2, DataOffset[i], OffsetCorrection[i],))
        else:
            filename2 = "nothing"
	
        output += "\"" + filename + "\" " + "\"" + filename2 + "\" " + hex(PathHash[i]).rstrip("L") + " " + hex(DataOffset[i]).rstrip("L") + " " + hex(OffsetCorrection[i]).rstrip("L") + " " + hex(Data3[i]).rstrip("L") + " " + hex(DataSize[i]).rstrip("L") + " " + hex(CheckSums1[i]).rstrip("L") + " " + hex(CheckSums2[i]).rstrip("L") + "\n"

    for i in range(MAX_NR_OF_THREADS):
        file_queue.put(None)
        
    return output



# UNPACK BEC-ARCHIVE
###########################################################################################################################################################

RomMap = []

class RomSection():
    def __init__(self, name, name2, hash, address, size2, flags, size, checksum, checksum2):
        self.name = name.replace("\\","/").lower()
        self.name2 = name2.replace("\\","/").lower()
        
        #print("name : "+name+" hash : "+hash)
        self.hash = int(hash, 16)
        
        computedHash = computeFileHash(self.name)
        if self.hash == computedHash :
            print("hashes match : "+str(self.hash) + " / "+str(computedHash))
        
        
        self.address = address
        self.new_address = address
        self.flags = flags
        self.size = size
        self.size2 = size2
        self.checksum = checksum
        self.checksum2 = checksum2
    
    @classmethod
    def fromList(cls,data):
        return cls(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
    

def alignFileSizeWithZeros(file, pos, alignment):
    target = (pos + alignment - 1) & (0x100000000-alignment)
    amount = target - pos
    file.write(b'\0' * amount)

###########################################################################################################################################################

def createBecArchive(dir, filename, becmap, gc, demobec,ignorechecksum,debug=False):
    filealignment = 0x0
    NrOfFiles = 0x0
    HeaderMagic = 0x0
	
    with open(becmap) as fin:
        for line in fin:
            words = line.split()
            if len(words) == 3:
                filealignment = int(words[0], 16)
                NrOfFiles = int(words[1], 16)
                HeaderMagic = int(words[2], 16)
            else:
                words_temp = line.split("\"") # filename, filename2
                words = [words_temp[1]] + [words_temp[3]] + words_temp[4].split() # ?, offset, flags?, filesize
                #print(words)
                if len(words) == 9:
                    becLine = readBecLine(words)
                    FileSize = os.path.getsize(dir + "/" + becLine.Name)
                    FileSize2 = 0
                    if becLine.Name2 != "nothing":
                        FileSize2 = os.path.getsize(dir + "/" + becLine.Name)
                    romSection = RomSection(words,FileSize,FileSize2)    
                    RomMap.append(romSection)
        
    if os.path.dirname(filename) != "":
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
    output_rom = open(filename, 'wb')

	# write header
    
    ignoreChecksumVersion = 0x1
    useChecksumVersion = 0x3
    version = useChecksumVersion
    if ignorechecksum :
      version = ignoreChecksumVersion
    
    output_rom.write(struct.pack('<4sHHII', b" ceb", int(version), int(filealignment), int(NrOfFiles), int(HeaderMagic)))

    # updated the filesizes
    RomMap.sort(key=operator.attrgetter('address')) # address
    #addr = RomMap[0].address
    addr = 0x10 + NrOfFiles*0x10 + (filealignment - 1)
    addr &= (0x100000000 - filealignment)
    diffaddr = 0
    oldaddr = addr
	
    for item in RomMap:
        if item.flags != 0:
            continue
        
        #item.size = os.path.getsize(dir + "/" + item.name)
        if item.address != addr and diffaddr == 0:
            print("Adr diff: org: " + hex(item.address) + ", new: " + hex(addr) + ", prevaddr: " + hex(oldaddr))
            diffaddr = 1
        oldaddr = addr
        item.new_address = addr
        if item.size2 > 0:
            addr += item.size2 + 8 + (filealignment - 1)
            addr &= (0x100000000 - filealignment)
        addr += item.size + (filealignment - 1)
        if ((item.size2 == 0) and (item.size > 0)) or (gc == 1):
            addr += 8 # GCExclusive + 8 for checksum being saved here
        addr &= (0x100000000 - filealignment)
        if (item.size2 == 0) and (item.size == 0) and (gc == 0): # PS2Exclusive
            addr += filealignment

    # fix the second instant of some file entries
    for i in range(len(RomMap)):
        if RomMap[i].flags != 0:
            for j in range(len(RomMap)):
                if (i != j) and (RomMap[j].flags == 0) and (RomMap[i].address == RomMap[j].address):
                    RomMap[i].new_address = RomMap[j].new_address
                    RomMap[i].size = RomMap[j].size
    
    RomMap.sort(key=operator.attrgetter('hash')) # address
    for item in RomMap:
        output_rom.write(struct.pack('<II', int(item.hash), int(item.new_address)))
        output_rom.write(struct.pack('<BBB', int((item.size2 >> 0) & 0xff), int((item.size2 >> 8) & 0xff), int((item.size2 >> 16) & 0xff)))
        output_rom.write(struct.pack('<BI', int(item.flags), int(item.size)))

    alignFileSizeWithZeros(output_rom, output_rom.tell(), filealignment)
    
    RomMap.sort(key=operator.attrgetter('address')) # address
    i = 0
    for item in RomMap:
        if item.flags != 0: # skip files where flag == 2
            continue

        if item.size2 > 0:
            filepath2 = dir + "/" + item.name2
            filedata2 = bytearray(open(filepath2, "rb").read())
            output_rom.write(filedata2)
            output_rom.write(struct.pack('<II', int(item.checksum), int(item.checksum2))) # checksum? PS2Exclusive
            alignFileSizeWithZeros(output_rom, output_rom.tell(), filealignment)
		
        filepath = dir + "/" + item.name
        file = open(filepath, "rb")
        filedata = bytearray(file.read())
        file.close()
        output_rom.write(filedata)
        if ((item.size2 == 0) and (item.size > 0)) or (gc == 1):
            output_rom.write(struct.pack('<II', item.checksum, item.checksum2)) # checksum? GCExclusive
		
        alignFileSizeWithZeros(output_rom, output_rom.tell(), filealignment)
			
        if (item.size2 == 0) and (item.size == 0) and (gc == 0):
            output_rom.write(b'\0' * filealignment) # write dvd filler material into archive PS2Exclusive

        output_rom.flush()
        
        i += 1
        if (i % 2500) == 0:
            print("write progress... " + str(i) + "/" + str(len(RomMap)))

###########################################################################################################################################################
###########################################################################################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-pack', action='store', nargs=3, type=str, metavar=("inputDir", "outputFile", "becFilelist"), help="pack files into a bec-archive")
    group.add_argument('-unpack', action='store', nargs=3, type=str, metavar=("inputFile", "outputDir", "becFilelist"), help="unpack files from a bec-archive")
    group.add_argument('-scan', action='store', nargs=1, type=str, metavar=("inputDir", ), help="scan files in archive")
    group.add_argument('-readbec', action='store', nargs=1, type=str, metavar=("inputFile", ), help="read bec file")

    parser.add_argument("--gc", action="store_true", help="activate GC mode") # switch between PS2 and GC Mode, the bec-formats they use don't seem completely compatible
    parser.add_argument("--demobec", action="store_true", help="demo file mode for bec") # switch between demo and non demo formats as they differ
    parser.add_argument("--ignorechecksum", action="store_true", help="test ignore checksum for repack") # 
    
    args = parser.parse_args()

    start = time.time()
    debug = True
    gc = 0
    demobec = 0
    ignorechecksum = 0	
	
    if args.gc:
        gc = 1

    if args.demobec:
        demobec = 1

    if args.ignorechecksum:
        ignorechecksum = 1

    if args.pack:
        createBecArchive(args.pack[0], args.pack[1], args.pack[2], gc, demobec,ignorechecksum,debug)
    if args.unpack:
        diagnose(args.unpack[0], args.unpack[1], args.unpack[2], gc,demobec,debug)
    if args.scan:
        scanFiles(args.scan[0])
    if args.readbec:
        readFileList(args.readbec[0])

    if debug:
        elapsed_time_fl = (time.time() - start)
        print("passed time: " + str(elapsed_time_fl))
