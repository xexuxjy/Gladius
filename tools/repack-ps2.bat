set BASE_DIR=D:\GladiusModding\PS2\
set BEC_FILE=%BASE_DIR%\REPACK\data.bec
set BEC_UNPACK_DIR=%BASE_DIR%\unpack\

py -3 bec-tool-all.py -pack %BEC_UNPACK_DIR% %BEC_FILE% %BEC_UNPACK_DIR%/FileList.txt --platform=PS2
