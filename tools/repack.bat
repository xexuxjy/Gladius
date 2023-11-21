set OUTPUT_DIR=F:\GladiusISOWorkingExtracted\gc\data\config\
set EXTRACTED_DIR=F:\GladiusISOWorkingExtracted\gc\
set BEC_FILE=F:\GladiusISORepack\gc\gladius.bec
set ISO_FOLDER=F:\GladiusISORepack\gc\
set ISO_OUTPUT_FILE=F:\GladiusISORepack\gc-iso\GladiusModded.iso

py -3 bec-tool.py --gc -pack %EXTRACTED_DIR% %BEC_FILE% %EXTRACTED_DIR%FileList.txt
rem py -3 ngciso-tool.py -pack %ISO_FOLDER% %ISO_FOLDER%fst.bin %ISO_FOLDER%repack_FileList.txt %ISO_OUTPUT_FILE%
