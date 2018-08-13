from winreg import *
from datetime import datetime, timedelta
import struct
import csv

def Win_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp//10, hours=9)

def loop_Sub_Parser(Sub_Var_Key, Sub_Key_Path, Sub_Key_Cut, cut):
	for i in range(Sub_Key_Cut):
		try:
			name, data, x = EnumValue(Sub_Var_Key, i)
			if not name in ("MRUListEx", "NodeSlot"):
				loop_Key_Path = Sub_Key_Path + r'\\' + name # 서브키에 하위 키 경로를 추가 해준다.
				loop_Sub_Key = OpenKey(Var_Hive, loop_Key_Path) # 서브키 핸들러 생성
				ts = QueryInfoKey(loop_Sub_Key)[2] # 작성된 시간
				print(' '*cut +'{} {} {} {}'.format(loop_Key_Path, name, Win_ts(ts).strftime('%Y:%m:%d_%H:%M:%S.%f'), cut))
				print(' '*cut + 'Itempos_Size : {} File_Size : {} Created_Date : {} Modified_Date : {} File_Name : {}'.format(Itempos_Size(data), File_Size(data), Created_Date(data), Modified_Date(data), File_Name(data)))
				
				wr.writerow([loop_Key_Path, Win_ts(ts).strftime('%Y:%m:%d_%H:%M:%S.%f'), Itempos_Size(data), File_Size(data), Created_Date(data), Modified_Date(data) ,File_Name(data)])

				if(QueryInfoKey(loop_Sub_Key)[1] != 2): # 하위키의 값이 더 있을 경우
					cut+=1
					loop_Sub_Parser(loop_Sub_Key, loop_Key_Path, QueryInfoKey(loop_Sub_Key)[1], cut) # 한번더 loop_Sub_Parser 실행
					cut-=1
				else: # 하위키의 값이 없을 경우 for문 종료
					break

		except WindowsError:
			pass

def BagMRU_Parser():
	for i in range(BagMRU_Cut): # BagMRU 값 개수
		try:
			cut = 0 # 하위키의 값을 보기 편하게 하기 위해 카운트
			name, data, x = EnumValue(Var_Key, i)

			if not name in ("MRUListEx", "NodeSlot", "NodeSlots"):
				Sub_BagMRU_Path = BagMRU_Path + r'\\' + name # 하위키의 값 경로 만들기
				Sub_Var_Key = OpenKey(Var_Hive, Sub_BagMRU_Path) # 하위키 핸들러
				ts = QueryInfoKey(Sub_Var_Key)[2]
				print(Sub_BagMRU_Path, name, Win_ts(ts).strftime('%Y:%m:%d_%H:%M:%S.%f') , cut)
				print('Itempos_Size : {} File_Size : {} Created_Date : {} Modified_Date : {} File_Name : {}'.format(Itempos_Size(data), File_Size(data), Created_Date(data), Modified_Date(data),File_Name(data)))
				
				wr.writerow([Sub_BagMRU_Path, Win_ts(ts).strftime('%Y:%m:%d_%H:%M:%S.%f'), Itempos_Size(data), File_Size(data), Created_Date(data), Modified_Date(data) ,File_Name(data)])
				
				if(QueryInfoKey(Sub_Var_Key)[1] != 2): # 하위키의 값이 2개가 아닐 경우 (2개보다 많을 경우)
					cut+=1
					loop_Sub_Parser(Sub_Var_Key, Sub_BagMRU_Path, QueryInfoKey(Sub_Var_Key)[1], cut) # loop_Sub_Parser 호출
					cut-=1

		except WindowsError:
			pass

def Itempos_Size(data):
	try:
		return abs(struct.unpack_from('b', data[0:2].replace(b"\x00",b""))[0])
	except:
		return abs(struct.unpack_from('h', data[0:2].replace(b"\x00",b""))[0])

def File_Size(data):
	return data[4:8].replace(b"\x00", b"")

def Created_Date(data):
	try:
		return Win_ts(struct.unpack_from('<L', data[32:36])[0])
	except:
		return data[32:36]

def Modified_Date(data):
	try:
		return Win_ts(struct.unpack_from('<L', data[36:40])[0])
	except:
		return data[36:40]

def File_Name(data):
	return data[0x0E:0x22].replace(b'\x00', b'')

f = open('Shellbag_info.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(["Reg_Path", "Reg_Modified_Time", "Itempos_Size", "File_Size", "Created_Date", "Modified_Time", "File_Name"])

BagMRU_Path = r'Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU'
Var_Hive = ConnectRegistry(None, HKEY_CURRENT_USER)
Var_Key = OpenKey(Var_Hive, BagMRU_Path) # BagMRU 핸들러
BagMRU_Cut = QueryInfoKey(Var_Key)[1] # BagMRU의 요소 개수

BagMRU_Parser()

f.close()

print('Created_Csv')
