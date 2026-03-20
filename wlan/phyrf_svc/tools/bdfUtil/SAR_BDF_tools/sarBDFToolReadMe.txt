/*********************************************************************************************************************************/

setSarPwr_helium and getSarPwr_helium are csv to BDF txt file conversion scripts designed to work with sarBDFTool.csv file.
sarBDFTool.csv contains power value tables for all configurable values for SAR V1.

CSV file contains power values in dBm 
BDF file contains power values in step 4 i.e 4*CSV power value

/*********************************************************************************************************************************/
Usage 
$ python setSarPwr_helium.py -bdf <bdf file path>

$ python getSarPwr_helium.py -bdf <bdf file path>

Default value for bdf: bdwlan.txt
