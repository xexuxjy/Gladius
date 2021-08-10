set EXTRACTED_DIR=D:\GladiusISOWorkingExtracted\python-gc-old\gc\
set BEC_FILE=D:\GladiusISOWorking\GameCube\root\gladius.bec

py -3 bec-tool-old.py -unpack %BEC_FILE% %EXTRACTED_DIR% %EXTRACTED_DIR%\FileList.txt --gc
