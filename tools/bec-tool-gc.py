# -*- coding: utf-8 -*-

import os
import sys
import struct
import operator
import argparse
import time
import hashlib
import gcnamehashes

import queue
import threading
from collections import namedtuple
from os import listdir,walk
from os.path import isfile, join, relpath,basename,commonpath,abspath,realpath,normpath,dirname

separator = ','
fileAtEnd = 0xC0000000

headerFile = "filelist.txt"

###########################################################################################################################################################

class RomSection():
    def __init__(self, name, hash, address, size,checksum):
        self.FileName = name.replace("\\","/").lower()
        
        self.PathHash = int(hash)
        if self.PathHash == 0 :        
            self.PathHash = computeFileHash(self.FileName)
            
        
        self.DataOffset = int(address)
        self.OriginalDataOffset = self.DataOffset
        self.DataSize = int(size)
        self.CheckSum = int(checksum)
        if self.CheckSum > 0 :
           self.CheckSum = 0x2000000

        self.IsNew = False
        #if self.CheckSum > 0 :        
        #    print(self.FileName + " "+str(self.CheckSum)+"\n")
    
    
    @classmethod
    def fromList(cls,data):
        return cls(data[0],data[1],data[2],data[3],data[4])
    

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
            if name.lower() == headerFile :
                print("Skipping "+headerFile)
                continue
                
            #print(relpath(os.path.join(root,name),dir))
            fullName = relpath(os.path.join(root,name),dir)
            romSection = RomSection.fromList([fullName,"0",str(fileAtEnd),"0","0"])
            scannedRomMap.append(romSection)

    return scannedRomMap
    

def readFileList(becmap):
    dir = os.path.dirname(becmap)
    scannedData = scanFiles(dir)
    
    fileListData = []
    
    with open(becmap) as fin:
        lineCount = 0
        for line in fin:
            if line[0] == '#':
               continue
               
            words = line.split(separator)
            
            # header
            if lineCount == 0:
                fileAlignment = int(words[0])
                nrOfFiles = int(words[1])
                headerMagic = int(words[2])
                print("FA : "+str(fileAlignment)+" : "+words[0])
            else:
                romSection = RomSection.fromList(words)
                fileListData.append(romSection)
                #print(romSection.FileName)
            lineCount += 1
    
    #print(romSections)
    diffList = diffFiles(fileListData,scannedData)
    
  
    #print("fileListData "+str(len(fileListData))+" scannedData "+str(len(scannedData))+"  diffList "+str(len(diffList)))
    print ("Files : "+str(len(fileListData)))
    return [fileListData,fileAlignment,headerMagic,diffList]

def diffFiles(fileListData,scannedData):
    fileListDataDictionary = {}
    scannedDataDictionary = {}
    for romData in fileListData:
        fileListDataDictionary[romData.FileName] = romData
    for romData in scannedData:
        scannedDataDictionary[romData.FileName] = romData


    scannedSet = set(scannedDataDictionary.keys())
    fileListSet = set(fileListDataDictionary.keys())

    scannedList = list(scannedDataDictionary)
    fileListList = list(fileListDataDictionary)
    
    scannedList.sort()
    fileListList.sort()

    #writeListToFile("scanned.txt",scannedList)
    #writeListToFile("fileListSet.txt",fileListList)

    newFiles = scannedSet - fileListSet
    
    returnList = []
    for file in newFiles : 
        romSection = RomSection.fromList([file,"0",str(fileAtEnd),"0","0"])    
        romSection.IsNew = True
        returnList.append(romSection)
    
    #for file in newFiles :
        #print(file)
    return returnList

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


def getFilename(hashcode, count):
      if hashcode in gcnamehashes.filenameHashes:
          return gcnamehashes.filenameHashes[hashcode]
      else:
        return str(count)+".bin"

def unpackBecArchive(filename, filedir, demobec,debug=False):

    print("Filename : "+filename)
    print("Filedir : "+filedir)
    file = open(filename, "rb+")
    header_output = unpackBecArchive2(file, filedir,demobec,debug)
    
    headerfilename = filedir + headerFile
    if not os.path.exists(os.path.dirname(headerfilename)) and os.path.dirname(headerfilename):
        os.makedirs(os.path.dirname(headerfilename))
    fheader = open(headerfilename, 'w')
    fheader.write(header_output)

def unpackBecArchive2(file, filedir,demobec,debug=False):
    output = ""

    RomSections = []
    

    BecHeader = namedtuple('BecHeader', ['FileAlignment', 'NrOfFiles', 'HeaderMagic'])
    
    print("DemoBec == "+str(demobec))
    
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
    output += str(header.FileAlignment) + separator + str(header.NrOfFiles) + separator + str(header.HeaderMagic) + "\n"

    count = 0
    
    FileEntry = namedtuple('FileEntry', ['PathHash', 'DataOffset', 'CompDataSize', 'DataSize'])
    for i in range(header.NrOfFiles):
        data = file.read(0x10) # file.seek(0x10+0x10*i)
        fileEntry = FileEntry._make(struct.unpack('<IIII', data))
        filename = getFilename(fileEntry.PathHash,count)
        romSection = RomSection(filename,str(fileEntry.PathHash),str(fileEntry.DataOffset),str(fileEntry.DataSize),str(fileEntry.CompDataSize))
        RomSections.append(romSection)
        count += 1

    for romSection in RomSections:
        romSection.FileByteArray = ReadSection(file, romSection.DataOffset, romSection.DataSize)
        WriteSectionInFile(romSection.FileByteArray, filedir, romSection.FileName, romSection.DataOffset, romSection.DataSize)
        
        #if romSection.CheckSum != 0:
        #    dataLine = "#"
        #    dataLine += "  Compressed Size : "+(romSection.CheckSum & 0xFFFFFF00)
        #    dataLine += "  Cached : "+ +(romSection.CheckSum & 0x000000F0)
        #    dataLine += "  Instanced : "+ +(romSection.CheckSum & 0x00000080)
        #    dataLine += "\n"
        #    output += dataLine
            
        dataLine =  romSection.FileName + separator
        dataLine += str(romSection.PathHash) + separator
        dataLine += str(romSection.DataOffset) + separator
        dataLine += str(romSection.DataSize) + separator 
        dataLine += str(romSection.CheckSum) + "\n"
        output += dataLine

    for i in range(MAX_NR_OF_THREADS):
        file_queue.put(None)
        
    return output



# UNPACK BEC-ARCHIVE
###########################################################################################################################################################

RomMap = []


def alignFileSizeWithZeros(file, pos, alignment):
    target = (pos + alignment - 1) & (0x100000000-alignment)
    amount = target - pos
    file.write(b'\0' * amount)

###########################################################################################################################################################

def createBecArchive(dir, filename, becmap, gc, demobec,ignorechecksum,debug=False):
    print("createBecArchive")
    FileAlignment = 0x0
    NrOfFiles = 0x0
    HeaderMagic = 0x0

    readfileListResults = readFileList(becmap)
    FileAlignment = readfileListResults[1]
    HeaderMagic = readfileListResults[2]

    RomMap.extend(readfileListResults[0])

    print("*** : "+str(readfileListResults[3]))
    # include any new files
    RomMap.extend(readfileListResults[3])
        
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

    NrOfFiles= len(RomMap)
   
    print("Creating file with : "+str(NrOfFiles)+" entries")
   
    output_rom.write(struct.pack('<4sHHII', b" ceb", int(version), int(FileAlignment), int(NrOfFiles), int(HeaderMagic)))

    
    addr = 0x10 + NrOfFiles*0x10 + (FileAlignment - 1)
    addr &= (0x100000000 - FileAlignment)

    print("After header position : "+str(output_rom.tell()))
    print("Start address : "+str(addr))


    baseAddr = addr
    currentAddr = baseAddr

    RomMap.sort(key=operator.attrgetter('DataOffset')) # address
    
    print("Sorted Offset")

    count = 0
    lastItem = None
    
    for item in RomMap:
        duplicate = False
        
        oldSize = item.DataSize
        item.OldSize = oldSize
        item.DataSize = os.path.getsize(dir + "/" + item.FileName)
        if oldSize != item.DataSize:
            print(item.FileName + " size changed : "+str(oldSize) + " / "+str(item.DataSize))
        
        
        if lastItem is not None:
           if lastItem.OriginalDataOffset == item.OriginalDataOffset and item.IsNew == False:
               duplicate = True
        
        if duplicate :
            lastItem.Checksum = 0x2000000
            item.Checksum = 0x2000000
            item.DataOffset = lastItem.DataOffset
        else:
            if item.IsNew :
               print("Adding new item "+item.FileName+" at position "+str(currentAddr))
               
            item.DataOffset = currentAddr
            currentAddr += item.DataSize
            currentAddr += (FileAlignment - 1)
            # checksum
            currentAddr += 8
            currentAddr &= (0x100000000 - FileAlignment)
        
        lastItem = item



    RomMap.sort(key=operator.attrgetter('PathHash')) # address
    #RomMap.sort(key=operator.attrgetter('DataOffset')) # address
    for item in RomMap:
        output_rom.write(struct.pack('<I', item.PathHash))
        output_rom.write(struct.pack('<I', item.DataOffset))
        output_rom.write(struct.pack('<I', item.CheckSum))
        output_rom.write(struct.pack('<I', item.DataSize))


    alignFileSizeWithZeros(output_rom, output_rom.tell(), FileAlignment)

    print("After header write and align : "+str(output_rom.tell()))

    print("Sorted DataOffset")

    print("RomMap Size : "+str(len(RomMap)))
    
    RomMap.sort(key=operator.attrgetter('DataOffset')) # address
    i = 0
    for item in RomMap:
        #handle items that had the same offset in the file
        if item.DataOffset < output_rom.tell():
            #print("Skipping duplicate "+item.FileName)
            continue
            
        filepath = dir + "/" + item.FileName
        filepath = normpath(filepath)
        file = open(filepath, "rb")
        filedata = bytearray(file.read())
        file.close()
        output_rom.write(filedata)
        if (item.DataSize > 0):
            output_rom.write(struct.pack('<II', item.CheckSum, 0)) 
	
        if (item.OldSize != item.DataSize):
            print("Adding new file "+item.FileName+" hash "+str(item.PathHash)+ " with dataoffset + "+str(item.DataOffset)+" size "+str(item.DataSize))
	
        alignFileSizeWithZeros(output_rom, output_rom.tell(), FileAlignment)
        #print("After data write and align : "+str(output_rom.tell()))
		
        output_rom.flush()
        
        i += 1
        if (i % 2500) == 0:
            print("write progress... " + str(i) + "/" + str(len(RomMap)))


###########################################################################################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-pack', action='store', nargs=3, type=str, metavar=("inputDir", "outputFile", "becFilelist"), help="pack files into a bec-archive")
    group.add_argument('-unpack', action='store', nargs=2, type=str, metavar=("inputFile", "outputDir"), help="unpack files from a bec-archive")
    #group.add_argument('-scan', action='store', nargs=1, type=str, metavar=("inputDir", ), help="scan files in archive")
    group.add_argument('-readfilelist', action='store', nargs=1, type=str, metavar=("inputFile", ), help="read file list and package extra files")

    parser.add_argument("--demobec", action="store_true", help="demo file mode for bec") # switch between demo and non demo formats as they differ
    parser.add_argument("--ignorechecksum", action="store_true", help="test ignore checksum for repack") # 
    
    args = parser.parse_args()

    start = time.time()
    debug = True
    demobec = 0
    ignorechecksum = 0	
	
    if args.demobec:
        demobec = 1

    if args.ignorechecksum:
        ignorechecksum = 1

    print("Main demobec "+str(demobec))
    
    if args.pack:
        createBecArchive(args.pack[0], args.pack[1], args.pack[2], demobec,ignorechecksum,debug)
    if args.unpack:
        unpackBecArchive(args.unpack[0], args.unpack[1], demobec,debug)
    #if args.scan:
    #    scanFiles(args.scan[0])
    if args.readfilelist:
        readFileList(args.readfilelist[0])

    if debug:
        elapsed_time_fl = (time.time() - start)
        print("passed time: " + str(elapsed_time_fl))

