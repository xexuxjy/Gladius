rem @echo off
set BASE_DIR=D:\GladiusModding\GC\
set OUTPUT_DIR=%BASE_DIR%\gc\data\config\
set BEC_UNPACK_DIR=%BASE_DIR%\UNPACK

set BEC_FILE=%BASE_DIR%\REPACK\gladius.bec
set ISO_FOLDER=%BASE_DIR%\ISO\unpack\
set ISO_OUTPUT_FILE=%BASE_DIR%\ISO\GladiusMODDED.iso

py -3 bec-tool-gc.py -pack %BEC_UNPACK_DIR% %BEC_FILE% %BEC_UNPACK_DIR%/FileList.txt
rem copy %BEC_FILE% %ISO_FOLDER%
rem py -3 ngciso-tool.py -pack %ISO_FOLDER% %ISO_FOLDER%fst.bin %ISO_FOLDER%GladiusISO_FileList.txt %ISO_OUTPUT_FILE%




