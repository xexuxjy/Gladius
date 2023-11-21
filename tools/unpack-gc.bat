@echo off
set BASE_DIR=F:\GladiusGCPacking
set ORIGINAL_ISO_FILE=%BASE_DIR%\ISO\Gladius.nkit.iso
set ISO_UNPACK_DIR=%BASE_DIR%\ISO\unpack\
set BEC_FILE=%ISO_UNPACK_DIR%\gladius.bec
set BEC_UNPACK_DIR=%BASE_DIR%\BEC\unpack\

rem py -3 ngciso-tool-gc.py -unpack %ORIGINAL_ISO_FILE% %ISO_UNPACK_DIR% GladiusISO_FileList.txt
py -3 bec-tool-gc.py -unpack %BEC_FILE% %BEC_UNPACK_DIR% 



