Run the tool as below: 
	
	python RegDB_excel2bin.py <excel file>
	ex: py -3 RegDB_excel2bin.py Regulatory_BDF_6G_In_Data.xlsx

-Supports new 6G format. 
- Only one excel file required (no need of RegDB_Out_Data.xlsx)
-Script will generate RegDB.bin and RegDB_new.txt in the local location. It uses RegDB_txt2bin.py and RegDB_bin2txt.py
-By default, RegDB BDF will be enabled via flag regDbEnable (i.e. regulatory database values will be taken from RegDB BDF values). To disable, change the enable flag(regDbEnable) to 0 in txt and convert txt<->bin

NOTE: Runs with Python 3.7 and above. openpyxl 2.5.11 module is required. 