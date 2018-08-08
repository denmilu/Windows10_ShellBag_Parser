from winreg import *
from datetime import datetime, timedelta
import struct

cut = 0

def Win_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp//10, hours=9)

def loop_Sub_Parser(Var_Key, Path, Sub_Key_Cut, cut):
	for i in range(Sub_Key_Cut):
		try:
			name, data, x = EnumValue(Var_Key, i)
			if not name in ("MRUListEx", "NodeSlot"):
				Key_Path = Path + r'\\' + name 
				loop_Sub_Key = OpenKey(Var_Hive, Key_Path)
				ts = QueryInfoKey(loop_Sub_Key)[2]
				print(' '*cut +'{} {} {} {}'.format(Key_Path, name, Win_ts(ts), cut))
				if(QueryInfoKey(loop_Sub_Key)[1] != 2):
					cut+=1
					loop_Sub_Parser(loop_Sub_Key, Key_Path, QueryInfoKey(Var_Key)[1], cut)
					cut-=1
				else:
					break

		except WindowsError:
			pass

BagMRU_Path = r'Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU'
Var_Hive = ConnectRegistry(None, HKEY_CURRENT_USER)
Var_Key = OpenKey(Var_Hive, BagMRU_Path) 
BagMRU_Cut = QueryInfoKey(Var_Key)[0] # BagMRU의 요소 개수

for i in range(BagMRU_Cut):
	try:
		cut=0
		name, data, x = EnumValue(Var_Key, i)
		if not name in ("MRUListEx", "NodeSlot", "NodeSlots"):
			Sub_BagMRU_Path = BagMRU_Path + r'\\' + name
			Sub_Var_Key = OpenKey(Var_Hive, Sub_BagMRU_Path)
			ts = QueryInfoKey(Sub_Var_Key)[2]
			print(Sub_BagMRU_Path, name, Win_ts(ts), cut)

			if(QueryInfoKey(Sub_Var_Key)[1] != 2):
				cut+=1
				loop_Sub_Parser(Sub_Var_Key, Sub_BagMRU_Path, QueryInfoKey(Sub_Var_Key)[1], cut)
				cut-=1

	except WindowsError:
		pass

# c = QueryInfoKey(Var_Key)[1]
# print(c)

# try:
# 	cut = 0
# 	while True:
# 		Data = QueryValueEx(Wininfo_Key, str(cut))[0]
# 		print(struct.unpack_from("<B",Data[14:21])[0])
# 		cut += 1
# except WindowsError:
# 	pass
