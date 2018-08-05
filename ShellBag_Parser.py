from winreg import *
import struct

BagMRU_Path = r'Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU'
Var_Hive = ConnectRegistry(None, HKEY_CURRENT_USER)
Var_Key = OpenKey(Var_Hive, BagMRU_Path)

BagMRU_Cut = QueryInfoKey(Var_Key)[0]

for i in range(BagMRU_Cut):
	try:
		name, data, x = EnumValue(Var_Key, i)
		if not name in ("MRULISTEX", "NodeSlot", "NodeSlots"):
			a = Var_Key + '//' + i
			ts = QueryInfoKey(a)[2]
			print(ts)
	
	except:
		pass

# try:
# 	cut = 0
# 	while True:
# 		Data = QueryValueEx(Wininfo_Key, str(cut))[0]
# 		print(struct.unpack_from("<B",Data[14:21])[0])
# 		cut += 1
# except WindowsError:
# 	pass
