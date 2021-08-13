rem @echo off
set BASE_DIR=D:\GladiusISOWorkingExtracted\python-gc\
set OUTPUT_DIR=%BASE_DIR%\gc\data\config\
set EXTRACTED_DIR=%BASE_DIR%\gc\
set BEC_FILE=%BASE_DIR%\repack\gladius.bec
set ISO_FOLDER=%BASE_DIR%\repack\
set ISO_OUTPUT_FILE=%BASE_DIR%\GladiusMODDED.iso

py -3 bec-tool-gc.py -pack %EXTRACTED_DIR% %BEC_FILE% %EXTRACTED_DIR%/FileList.txt
py -3 ngciso-tool.py -pack %ISO_FOLDER% %ISO_FOLDER%fst.bin %ISO_FOLDER%repack_FileList.txt %ISO_OUTPUT_FILE%
