rem @echo off
set BASE_DIR=F:\GladiusGCPacking
set OUTPUT_DIR=%BASE_DIR%\gc\data\config\
set BEC_UNPACK_DIR=%BASE_DIR%\BEC\unpack\

set BEC_FILE=%BASE_DIR%\BEC\repack\gladius.bec
set ISO_FOLDER=%BASE_DIR%\ISO\repack\
set ISO_OUTPUT_FILE=%BASE_DIR%\ISO\GladiusMODDED.iso

py -3 bec-tool-gc.py -pack %BEC_UNPACK_DIR% %BEC_FILE% %BEC_UNPACK_DIR%/FileList.txt
copy %BEC_FILE% %ISO_FOLDER%
py -3 ngciso-tool.py -pack %ISO_FOLDER% %ISO_FOLDER%fst.bin %ISO_FOLDER%GladiusISO_FileList.txt %ISO_OUTPUT_FILE%




