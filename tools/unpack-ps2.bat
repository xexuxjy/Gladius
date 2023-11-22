set BASE_DIR=D:\GladiusModding\PS2
set BEC_FILE=%BASE_DIR%\ISO\unpack\data.bec
set BEC_UNPACK_DIR=%BASE_DIR%\unpack\

py -3 bec-tool-all.py -unpack %BEC_FILE% %BEC_UNPACK_DIR% --platform=PS2
