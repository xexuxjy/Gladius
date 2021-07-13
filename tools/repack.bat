set OUTPUT_DIR=D:\GladiusISOWorkingExtracted\python3\gc\data\config\
set EXTRACTED_DIR=D:\GladiusISOWorkingExtracted\python3\gc\
set BEC_FILE=D:\GladiusISOWorkingExtracted\python3\repack\gladius.bec
set ISO_FOLDER=D:\GladiusISOWorkingExtracted\python3\repack\
set ISO_OUTPUT_FILE=D:\GladiusISOWorkingExtracted\GladiusMODDED.iso

py -3 bec-tool.py --gc -pack %EXTRACTED_DIR% %BEC_FILE% %EXTRACTED_DIR%/FileList.txt
py -3 ngciso-tool.py -pack %ISO_FOLDER% %ISO_FOLDER%fst.bin %ISO_FOLDER%repack_FileList.txt %ISO_OUTPUT_FILE%
