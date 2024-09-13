set BASE_DIR=D:\GladiusModding\XBOX
set BEC_FILE=%BASE_DIR%\REPACK\gladius.bec
set BEC_UNPACK_DIR=%BASE_DIR%\unpack\

py -3 bec-tool-all.py -pack %BEC_UNPACK_DIR% %BEC_FILE% %BEC_UNPACK_DIR%/FileList.txt --platform=XBOX
