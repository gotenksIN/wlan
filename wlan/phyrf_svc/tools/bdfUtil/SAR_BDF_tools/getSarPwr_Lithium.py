
import sys, argparse, re,csv 
import os

regDict = {
      '1'  : 'FCC',
      '4'  : 'MKK',
      '3'  : 'ETSI',
      'E'  : 'SD_NO_CTL',
      'F'  : 'NO_CTL',
      '0'  : 'None',
    }
	
#---------- CSV file mapping ------------------------------------------------------------------------------------------------------	
PwrTableOffsets2GCsv = [54,131,208,286,363,440]
PwrTableOffsets5GCsv = [70,147,224,302,379,456]
PwrTableOffsets6GCsv = [106,183,260,338,415,492]
PwrTableOffsets5G160Csv = [100,177,254,332,409,486]

#-----------------------------------------------------------------------------------------------------------------------------------
def getSARConfigValues(listVal,BdfFileStr):
	
	#--------Get SAR Version-------------------------------
	sarVer = re.findall("uint8	SAR_TABLES.SARVersion.*", BdfFileStr)
	if not sarVer:
		print ("SAR Version 1 values not found")
		sys.exit()
	sarVer = sarVer[0].split(' ')[1]
	if sarVer not in ['0','00','1','01','2','02']:
		print ("Invalid SARVersion value "+ sarVer)
		sys.exit()
	else:
		#print("sar version %d" % sarVer)
		listVal[0][1] = sarVer
	
	#--------Get SAR Flags-------------------------------
	sarFlagsBdf = re.findall("uint8	SAR_TABLES.SARFlags.*", BdfFileStr)
	sarFlags = sarFlagsBdf[0].split(' ')[1]
	listVal[1][1] = sarFlags

	#--------Get SAR_BW_RU Flags-------------------------------
	sarBwRuConfigBdf = re.findall("uint32	SAR_TABLES.SAR_BW_RU_Config_L.*", BdfFileStr)
	sarBwRuConfig = sarBwRuConfigBdf[0].split(' ')[1]
	listVal[9][1] = sarBwRuConfig
	
	sarBwRuConfigBdf = re.findall("uint32	SAR_TABLES.SAR_BW_RU_Config_U.*", BdfFileStr)
	sarBwRuConfig = sarBwRuConfigBdf[0].split(' ')[1]
	listVal[10][1] = sarBwRuConfig

	#--------Get SAR_BW_RU_Mapping Flags-----------------------		
	sarBwRuMappingBdf = re.findall("uint8	SAR_TABLES.SAR_BW_RU_Mapping\[.*", BdfFileStr)
	for x in range(len(sarBwRuMappingBdf)):
		sarBwRuMapping = sarBwRuMappingBdf[x].split(' ')[1]
		listVal[12+x][1] = sarBwRuMapping
		
	#--------Get SAR Channels----------------------------------	
	sarChannels2GBdf = re.findall("uint16	SAR_TABLES.SAR2GChannels.*", BdfFileStr)
	for x in range(0,4):
		sarChannels2G = sarChannels2GBdf[x].split(' ')[1]
		if sarChannels2G not in ['0','00']:
			listVal[3][x+1] = int(sarChannels2G)
		else:
			listVal[3][x+1] = 2555
	
	sarChannels5GBdf = re.findall("uint16	SAR_TABLES.SAR5GChannels.*", BdfFileStr)
	for x in range(0,10):
		sarChannels5G = sarChannels5GBdf[x].split(' ')[1]
		if sarChannels5G not in ['0','00']:
			listVal[4][x+1] = int(sarChannels5G)
		else:
			listVal[4][x+1] = 5815

	sarChannels5G160Bdf = re.findall("uint16	SAR_TABLES.SAR5G160Channels.*", BdfFileStr)
	for x in range(0,2):
		sarChannels5G160 = sarChannels5G160Bdf[x].split(' ')[1]
		if sarChannels5G160 not in ['0','00']:
			listVal[5][x+1] = int(sarChannels5G160)
		else:
			listVal[5][x+1] = 5815
	
	sarChannels6GBdf = re.findall("uint16	SAR_TABLES_6G.SAR6GChannels.*", BdfFileStr)
	for x in range(0,5):
		sarChannels6G = sarChannels6GBdf[x].split(' ')[1]
		if sarChannels6G not in ['0','00']:
			listVal[6][x+1] = int(sarChannels6G)
		else:
			listVal[6][x+1] = 7115
	

	#--------Get SAR CTL List-------------------------------	

	CtlListBdf = re.findall("uint8	SAR_TABLES.SARCtlList.*", BdfFileStr)
	for x in range(0,6):
		CtlList = CtlListBdf[x].split(' ')[1]
		if CtlList in ["0","1","3","4","E","F"]:
			listVal[7][x+1] = regDict[CtlList]
	return listVal
	
#-----------------------------------------------------------------------------------------------------------------------------------
def getSARPwrValues(listVal, BdfFileStr):
	print ("Generating CSV file ...")
	for ctl in range(0,6):
		for sarSet in range(0,6):
			sarSetPwrBdfStr = re.findall("int8	SAR_TABLES.SARPwrLimits2G\["+str(ctl)+"]\["+str(sarSet)+"].*", BdfFileStr)
			for values in range(len(sarSetPwrBdfStr)):
				powerDBm = float(sarSetPwrBdfStr[values].split(' ')[1])
				powerDBm = powerDBm/4.0
				listVal[PwrTableOffsets2GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)] = powerDBm
		
	for ctl in range(0,6):
		for sarSet in range(0,6):
			sarSetPwrBdfStr = re.findall("int8	SAR_TABLES.SARPwrLimits5G\["+str(ctl)+"]\["+str(sarSet)+"].*", BdfFileStr)
			for values in range(len(sarSetPwrBdfStr)):
				powerDBm = float(sarSetPwrBdfStr[values].split(' ')[1])
				powerDBm = powerDBm/4.0
				listVal[PwrTableOffsets5GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)] = powerDBm
	
	for ctl in range(0,6):
		for sarSet in range(0,6):
			sarSetPwrBdfStr = re.findall("int8	SAR_TABLES.SARPwrLimits5G160\["+str(ctl)+"]\["+str(sarSet)+"].*", BdfFileStr)
			for values in range(len(sarSetPwrBdfStr)):
				powerDBm = float(sarSetPwrBdfStr[values].split(' ')[1])
				powerDBm = powerDBm/4.0
				listVal[PwrTableOffsets5G160Csv[ctl]+(values/4)][(sarSet*6)+2+(values%4)] = powerDBm
		
	for ctl in range(0,6):
		for sarSet in range(0,6):
			sarSetPwrBdfStr = re.findall("int8	SAR_TABLES_6G.SARPwrLimits6G\["+str(ctl)+"]\["+str(sarSet)+"].*", BdfFileStr)
			for values in range(len(sarSetPwrBdfStr)):
				powerDBm = float(sarSetPwrBdfStr[values].split(' ')[1])
				powerDBm = powerDBm/4.0
				listVal[PwrTableOffsets6GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)] = powerDBm
		
				
	return listVal
	
	
#-----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	cmdParser = argparse.ArgumentParser(description="CSV to BDF text conversion tool for SAR powers")
	cmdParser.add_argument('-csv', action="store", dest="CsvFilePath", default="sarBDFTool.csv", help="CSV file name")
	cmdParser.add_argument('-bdf', action="store", dest="BdfFilePath", default="bdwlan.txt", help="BDF txt file name")
	args = cmdParser.parse_args()
	SARPwrFile = open(args.CsvFilePath,'rb')
	if SARPwrFile is None:
		print ("No input file %s found" % (args.CsvFilePath))
	else:
		SARPwrStr = SARPwrFile.read()
	
	newBDFFilePath = open(args.BdfFilePath,'r') #handle errono 2
	if newBDFFilePath is None:
		print ("No input file %s found" % (args.BdfFilePath))
	else:
		BdfFileStr = newBDFFilePath.read()
		
	with open ("sarBDFTool.csv","rb") as f:
		readCsv = csv.reader(f)
		listVal = list(readCsv)
		
	listVal = getSARConfigValues(listVal,BdfFileStr)
	listVal = getSARPwrValues(listVal, BdfFileStr)
	
	i = 0
	while os.path.exists("getSarPwr_helium%s.csv" % i):
		i += 1
	op = open("getSarPwr_helium%s.csv" % i,'wb')
	writeCsv = csv.writer(op)
	for x in range(len(listVal)):
		writeCsv.writerow(listVal[x])
	
		
	
	
	
