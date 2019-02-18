from ctypes import *
from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCWSTR, UINT
from ctypes.util import find_library
import os
import os.path


FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
FILE_ATTRIBUTE_DIRECTORY = 16
FILE_ATTRIBUTE_ARCHIVE = 32
FILE_ATTRIBUTE_DEVICE = 64
FILE_ATTRIBUTE_NORMAL = 128
FILE_ATTRIBUTE_TEMPORARY = 256
FILE_ATTRIBUTE_SPARSE_FILE = 512
FILE_ATTRIBUTE_REPARSE_POINT = 1024
FILE_ATTRIBUTE_COMPRESSED = 2048
FILE_ATTRIBUTE_OFFLINE = 4096
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192
FILE_ATTRIBUTE_ENCRYPTED = 16384
FILE_ATTRIBUTE_VIRTUAL = 65536
# These FILE_ATTRIBUTE_* flags  are apparently old definitions from Windows 95
# and conflict with current values above - but they live on for b/w compat...
FILE_ATTRIBUTE_ATOMIC_WRITE = 512
FILE_ATTRIBUTE_XACTION_WRITE = 1024

# 方式一
#ctypes.windll.user32.MessageBoxA(None, 'message', 'title', 0)
# 方式二
#ctypes.WinDLL('user32.dll').MessageBoxA(None, 'message', 'title', 0)
''' 
find_library("m")
'''
prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", "Hello from ctypes"), (1, "flags", 0)
MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)
MessageBox()
MessageBox(text="Spam, spam, spam")
MessageBox(flags=1, text="foo bar")
 
to_set_icon_dir = input("Input DIR to set icon : ") # "D:\\do\\ctypes_call_dll\\tt"
if os.path.isdir(to_set_icon_dir):
    to_set_icon_dir = os.path.abspath(to_set_icon_dir)
else:
    print("Need directory at all !")
    exit(0)
for cur_dir  in os.listdir(to_set_icon_dir):
    if cur_dir.find(".idea") > 0 : #忽略
        continue
    if os.path.islink(cur_dir) or os.path.isfile(cur_dir):
        continue 
    icon = "D:\\do\\ctypes_call_dll\\book.ico"
    desktop_ini = "%s\\%s\\%s"%(to_set_icon_dir,cur_dir,"Desktop.ini")
    print("desktop_ini = %s" % desktop_ini)
    
    prototype2 = WINFUNCTYPE(c_int,LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR)
    paramflags2 = (1,"sectionName",".ShellClassInfo"), (1, "keyName", "IconFile"), \
                  (1, "keyValue", "%SystemRoot%\\system32\\SHELL32.dll,186"), (1, "fileName", "You must have setted")
    WritePrivateProfileString = prototype2(("WritePrivateProfileStringW",windll.kernel32),paramflags2) 
    WritePrivateProfileString(keyValue= icon ,fileName=desktop_ini)
    WritePrivateProfileString(keyName="IconIndex",keyValue="0",fileName=desktop_ini)

    #  SetFileAttributes Lib "kernel32" Alias "SetFileAttributesA"     (ByVal lpFileName As String, ByVal dwFileAttributes As Long) As Long
    prototype3 = WINFUNCTYPE(c_int,LPCWSTR,c_int)
    paramflags3 = (1,"fileName", "You must have setted"), (1, "fileAttributes",FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
    SetFileAttributes = prototype3(("SetFileAttributesW",windll.kernel32),paramflags3)
    SetFileAttributes(fileName=desktop_ini)
    #SetFileAttributes(fileName = to_set_icon_dir ,fileAttributes =  FILE_ATTRIBUTE_READONLY )  # FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_READONLY

    print("set over")

