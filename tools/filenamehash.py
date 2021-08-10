# -*- coding: utf-8 -*-

import os
import sys
import struct
import hashlib

# 802096b0 called at 8020909c
# 804a0748


# Function_0x802096b0 on GC version
# r3: ptr to string
# r4: length of string
'''
.globl Function_0x802096b0
Function_0x802096b0: # 0x802096b0
    cmplwi  r4, 0x0
    lis     r5, unk_803096c0@ha
    addi    r5, r5, unk_803096c0@l
    li      r8, 0x0
    beq-    branch_0x80209764
    srwi.   r0, r4, 2
    mtctr   r0
    beq-    branch_0x80209740
branch_0x802096d0:
    lbz     r6, 0x0(r3)
    srwi    r7, r8, 8
    xor     r0, r8, r6
    lbz     r6, 0x1(r3)
    clrlslwi  r0, r0, 24, 2
    lwzx    r0, r5, r0
    xor     r8, r7, r0
    xor     r0, r8, r6
    lbz     r6, 0x2(r3)
    clrlslwi  r0, r0, 24, 2
    srwi    r7, r8, 8
    lwzx    r0, r5, r0
    xor     r8, r7, r0
    xor     r0, r8, r6
    lbz     r6, 0x3(r3)
    clrlslwi  r0, r0, 24, 2
    srwi    r7, r8, 8
    lwzx    r0, r5, r0
    addi    r3, r3, 0x4
    xor     r8, r7, r0
    xor     r0, r8, r6
    clrlslwi  r0, r0, 24, 2
    srwi    r7, r8, 8
    lwzx    r0, r5, r0
    xor     r8, r7, r0
    bdnz+      branch_0x802096d0
    andi.   r4, r4, 0x3
    beq-    branch_0x80209764
branch_0x80209740:
    mtctr   r4
branch_0x80209744:
    lbz     r6, 0x0(r3)
    srwi    r7, r8, 8
    addi    r3, r3, 0x1
    xor     r0, r8, r6
    clrlslwi  r0, r0, 24, 2
    lwzx    r0, r5, r0
    xor     r8, r7, r0
    bdnz+      branch_0x80209744
branch_0x80209764:
    mr      r3, r8
    blr
'''

ValueDic = {
    0x64: 0x646ba8c0,
    0x70: 0x14015c4f,
    0x78: 0xfa0f3d63,
    0x80: 0x3b6e20c8,
    0xac: 0xacbcf940,
    0xb4: 0x45df5c75,
    0xc0: 0x26d930ac,
    0xd0: 0x21b4f4b5,
    0x100: 0x76dc4190,
    0x108: 0x98d220bc,
    0x110: 0x71b18589,
    0x11c: 0xe8b8d433,
    0x124: 0x0f00f934,
    0x138: 0x91646c97,
    0x140: 0x6b6b51f4, # 0x80309800
    0x154: 0x1b01a57b,
    0x178: 0x8cd37cf3,
    0x190: 0x4adfa541,
    0x1b4: 0x33031de5,
    0x1d0: 0x5768b525,
    0x1e8: 0xb0d09822,
    0x1f8: 0xb7bd5c3b,
    0x234: 0x9309ff9d,
    0x244: 0x8708a3d2,
    0x254: 0x806567cb,
    0x2dc: 0x5505262f,
    0x2ec: 0x5cb36a04,
    0x358: 0x6fb077e1,
    0x368: 0x66063bca,
    0x378: 0x616bffd3,
    0x3a8: 0x40df0b66,
    0x3e0: 0xb3667a2e,
}
# get values in memory at r5 = 0x803096c0
def getValues(offset, file):
    file.seek(0x3066c0+offset)
    data = file.read(4)
    value, = struct.unpack(">I", data)
    return value

    #if offset in ValueDic:
    #    return ValueDic[offset]
    #else:
    #    print "No value at offset: " + hex(0x803096c0+offset) + " - " + hex(offset)

    #return 0

def getPathHash(string):
    stringlow = string.lower()
    r0 = 0
    r8 = 0
    i = 0
    blocks = len(stringlow) >> 2

    for c in stringlow:
        if ((i%4) == 0) & ((i/4) < blocks):
            r6 = ord(c)
            r7 = r8 >> 8
            r0 = r8 ^ r6
        elif ((i%4) == 1) & ((i/4) < blocks):
            r6 = ord(c)
            r0 &= 0xff
            r0 = r0 << 2
            r0 = getValues(r0, file)
            #if r0 == 0:
            #    break
            r8 = r7 ^ r0
            r0 = r8 ^ r6
        elif ((i%4) == 2) & ((i/4) < blocks):
            r6 = ord(c)
            r0 &= 0xff
            r0 = r0 << 2
            r7 = r8 >> 8
            r0 = getValues(r0, file)
            #if r0 == 0:
            #    break
            r8 = r7 ^ r0
            r0 = r8 ^ r6
        elif ((i%4) == 3) & ((i/4) < blocks):
            r6 = ord(c)
            r0 &= 0xff
            r0 = r0 << 2
            r7 = r8 >> 8
            r0 = getValues(r0, file)
            #if r0 == 0:
            #    break
            r8 = r7 ^ r0
            r0 = r8 ^ r6

            r0 &= 0xff
            r0 = r0 << 2
            r7 = r8 >> 8
            r0 = getValues(r0, file)
            #if r0 == 0:
            #    break
            r8 = r7 ^ r0

        elif ((i/4) >= blocks):
            r6 = ord(c)
            r7 = r8 >> 8
            r0 = r8 ^ r6
            r0 &= 0xff
            r0 = r0 << 2
            r0 = getValues(r0, file)
            #if r0 == 0:
            #    break
            r8 = r7 ^ r0
	
        i += 1
    #print "string: " + string
    #print "r0: " + hex(r0)
    #print "r6: " + hex(r6)
    #print "r7: " + hex(r7)
    #print "r8 (Endresult): " + hex(r8)
    return r8
