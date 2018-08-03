from winreg import *

Wininfo_Key = OpenKey(HKEY_CURRENT_USER,r'Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU')

ITEMPOS,FileSize,FileName,CreateDate,ModifiedDate,Unicode_FileName = [],[],[],[],[],[]

try:
    cut = 0
    while True:
    	Data = (QueryValueEx(Wininfo_Key, str(cut))[0])
    	print(Data[0])
    	print(ITEMPOS[cut])
    	cut+=1
except:
	print(cut)
