#!/usr/bin/python

import sys, getopt
from subprocess import run, call
import urllib.request, json, csv 
import urllib.parse
from collections import OrderedDict

transtable = "vicTransTable.csv"
mark_name =''

def get_smes (nine_fig):
	print(nine_fig)
	link = "https://maps.land.vic.gov.au/lvis/services/smesDataDelivery/getMarkInformation?searchType=NineFigureNumber&nineFigureNumber="+nine_fig
	with urllib.request.urlopen(link) as url:
		s = url.read()
	print(link)
	get_smes.mark_name = json.loads(s.decode())["data"]["name"]
	get_smes.mark_latitude = json.loads(s.decode())["data"]["latitude"]
	get_smes.mark_longitude = json.loads(s.decode())["data"]["longitude"]
	get_smes.markPostExists = json.loads(s.decode())["data"]["markPostExists"]
	get_smes.coverExists = json.loads(s.decode())["data"]["coverExists"]
	get_smes.markType = json.loads(s.decode())["data"]["markType"]
	get_smes.gnssSuitability = json.loads(s.decode())["data"]["gnssSuitability"]
	get_smes.groundToMarkOffset = json.loads(s.decode())["data"]["groundToMarkOffset"]
	get_smes.status = json.loads(s.decode())["data"]["status"]
	get_smes.scn = json.loads(s.decode())["data"]["scn"]
	get_smes.easting = json.loads(s.decode())["data"]["easting"]
	get_smes.northing = json.loads(s.decode())["data"]["northing"]
	get_smes.zone = json.loads(s.decode())["data"]["zone"]
	get_smes.ahdHeight = json.loads(s.decode())["data"]["ahdHeight"]
	get_smes.ellipsoidHeight = json.loads(s.decode())["data"]["ellipsoidHeight"]
	get_smes.hUncertainty = json.loads(s.decode())["data"]["hUncertainty"]
	get_smes.vUncertainty = json.loads(s.decode())["data"]["vUncertainty"]
	get_smes.hOrder = json.loads(s.decode())["data"]["hOrder"]
	get_smes.vOrder = json.loads(s.decode())["data"]["vOrder"]
	get_smes.gda94PublishedDate = json.loads(s.decode())["data"]["gda94PublishedDate"]
	get_smes.gda94Technique = json.loads(s.decode())["data"]["gda94Technique"]
	get_smes.gda94Measurements = json.loads(s.decode())["data"]["gda94Measurements"]
	get_smes.gda94Source = json.loads(s.decode())["data"]["gda94Source"]
	get_smes.ahdLevelSection = json.loads(s.decode())["data"]["ahdLevelSection"]
	get_smes.ahdPublishedDate = json.loads(s.decode())["data"]["ahdPublishedDate"]
	get_smes.ahdTechnique = json.loads(s.decode())["data"]["ahdTechnique"]
	get_smes.ahdSource = json.loads(s.decode())["data"]["ahdSource"]
	return;

def get_char4 (nine_fig):
  with open('vicTransTable.csv', mode='r') as infile:
    get_char4.reader = csv.reader(infile)
    get_char4.mydict = {rows[0]:rows[1] for rows in get_char4.reader}
    #print(get_char4.mydict)
    for get_char4.x, get_char4.y in get_char4.mydict.items():
    	if get_char4.y == nine_fig:
    		get_char4.char4 = get_char4.x

def t0_runpk (inputfile):
   com_runpk = 'runpkr00 -d -g \"'+inputfile+'\"'
   print(com_runpk)
   run(com_runpk)
   
def call_teqc (char4, nine_fig, ant_hgt,ant_code, observer,mark_name, mark_latitude, mark_longitude, filename):
   com_teqc = 'teqc -tr d +obs + -tbin 1d '+char4+' -O.mo '+char4+' -O.mn '+nine_fig+' -O.sl '+ant_hgt+' 0.3396 -0.0444 -O.an '+ant_code+' -O.o '+observer+' +O.c "Original BoN measurement of '+ant_hgt+'" +O.c "Mark Name: '+mark_name+'" +O.c "GDA94: '+str(mark_latitude)+' '+str(mark_longitude)+'" -O.ag OSGV '+filename+'.tgd'
   print(com_teqc)
   call(com_teqc)


def smes_logout (server,sessionKey):
   if server == 'PROD':
     smes_connect.domain = 'https://maps.land.vic.gov.au/'
   elif server == 'UAT':
     smes_connect.domain = 'https://maps.test.land.vic.gov.au/'
   elif server == 'SYSTEST':
     smes_connect.domain = 'https://maps.sys.test.land.vic.gov.au/'
   print(server)
   link = smes_connect.domain+'lvis/services/smesSurveyMarkDataDelivery/smesUserLogout?sessionKey='+sessionKey
   print(link)
   with urllib.request.urlopen(link) as url:
      s = url.read()
   print(s)


def smes_connect (server, username, password,nine_fig, markerPostExists, checkBoxMp, coverExists, checkBoxCvr, markType, checkBoxMt, gnssSuitability, checkBoxGnss, groundToMarkOffset, checkBoxGroundLevel,smesComment):
   if server == 'PROD':
     smes_connect.domain = 'https://maps.land.vic.gov.au/'
   elif server == 'UAT':
     smes_connect.domain = 'https://maps.test.land.vic.gov.au/'
   elif server == 'SYSTEST':
     smes_connect.domain = 'https://maps.sys.test.land.vic.gov.au/'
   print(server)
   link = smes_connect.domain+'lvis/services/smesSurveyMarkDataDelivery/smesUserLogin?userName='+username+'&password='+password
   print(link)
   with urllib.request.urlopen(link) as url:
      s = url.read()
   print(s)
   smes_connect.sessionKey = json.loads(s.decode())["data"]["sessionKey"]
   print(smes_connect.sessionKey)
   
   #nine_fig = window.lineEdit_ninefig.text()
   #coverExists = window.comboBoxCvr.currentText()
   #smesComment = window.smesComment.text()
   smes_update(smes_connect.sessionKey, nine_fig, markerPostExists, checkBoxMp, coverExists, checkBoxCvr, markType, checkBoxMt, gnssSuitability, checkBoxGnss, groundToMarkOffset, checkBoxGroundLevel ,smesComment)
   
   
   
def smes_update (sessionKey, nine_fig, markerPostExists, checkBoxMp, coverExists, checkBoxCvr, markType, checkBoxMt, gnssSuitability, checkBoxGnss, groundToMarkOffset, checkBoxGroundLevel ,smesComment):
   #post = "{\"sessionKey\":"+sessionKey+",\"nineFigureNumber\":"+nine_fig+",\"coverExists\":"+coverExists+",\"comments\":"+smesComment+"}"
   postStart = "{\"sessionKey\":"+sessionKey+",\"nineFigureNumber\":"+nine_fig
   postEnd = ",\"comments\":"+smesComment+"}"
   post =postStart
   
   if (checkBoxMp.isChecked() and markerPostExists != ''):
     post = post+",\"markerPostExists\":"+markerPostExists

   if (checkBoxCvr.isChecked() and coverExists != ''):
     post = post+",\"coverExists\":"+coverExists
     
   if (checkBoxMt.isChecked() and markType != ''):
     post = post+",\"markType\":"+markType
     
   if (checkBoxGnss.isChecked() and gnssSuitability != ''):
     post = post+",\"gnssSuitability\":"+gnssSuitability
     
   if (checkBoxGroundLevel.isChecked() and groundToMarkOffset != ''):
     post = post+",\"groundToMarkOffset\":"+groundToMarkOffset
     
   post = post+postEnd
   
   link = smes_connect.domain+'lvis/services/smesSurveyMarkDataDelivery/updateMarkDetailsSubmission'
   print(post)
   print(link)
   #data = urllib.parse.urlencode(post)
   #print(data)
   #h = httplib.HTTPConnection(link)
   headers = {"Content-type": "application/json", "Accept": "text/plain,application/json"}
   #headers = '{}'
   #h.request('POST', '', data, headers)
   req = urllib.request.Request(link,post.encode("utf-8"),headers)
   response = urllib.request.urlopen(req)
   print(response.read())
   #r = h.getresponse()
   #print(r.read())
   

   
   
   
#{"sessionKey":<value>,
#"nineFigureNumber":<value>,
#"markStatus ":<value>,
#"planNumber ":<value>,
#"groundToMarkOffset":<value>,
#"coverExists":<value>,
#"markerPostExists":<value>,
#"gnssSuitability":<value>,
#"markType":<value>,
#"comments":<value>,
#"supportingFiles":{
# "files":[ {
# "file": <base 64 encoded byte stream>,
# "fileName": <value>,
# "fileExtension": <value>,
# "fileCategory": <value>
# }]
#}}




def main (argv):
   print(argv)
   inputfile = ''
   #outputfile = ''
   nine_fig = ''
   ant_hgt = ''
   ant_code = ''
#   char4 = '00VB'
   observer = ''
   try:
 #     opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
      opts, args = getopt.getopt(argv,"f:9:a:c:o:",["file=","ninefig=","ant_hgt=","ant_code=","observer="])
   except getopt.GetoptError:
      print('rinex_preprocess.py -file <inputfile> -ninefig <nine_figure> -ant_hgt <slope to antenna> -ant_code <IGS antenna code>')
      sys.exit(2)
   print( opts)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-f","--file"):
         inputfile = arg
      elif opt in ("-9", "--ninefig"):
         nine_fig = arg
      elif opt in ("-a", "--ant_hgt"):
         ant_hgt = arg
      elif opt in ("-c", "--ant_code"):
         ant_code = arg
      elif opt in ("-o", "--observer"):
         observer = arg
   print(inputfile)
   #get_smes(nine_fig)
   #get_char4(nine_fig)
   print('Input file is ', inputfile)
   print('Nine_Fig is ', nine_fig)
   print('Ant Hgt is ', ant_hgt)
   print('Ant Code is ', ant_code)
   print ('Mark name is ',get_smes.mark_name)
   print ('Mark Latitude is ',get_smes.mark_latitude)
   print ('Mark Longitude is ',get_smes.mark_longitude)
   print ('Observer is',observer)
   print ('Four character ID is',get_char4.char4)

   input_st = inputfile.split('.')
   t0_runpk(inputfile)
   #com_runpk = 'runpkr00 -d -g '+inputfile
   com_teqc = 'teqc -tr d +obs + -tbin 1d '+get_char4.char4+' -O.mo '+get_char4.char4+' -O.mn '+nine_fig+' -O.sl '+ant_hgt+' 0.3396 -0.0444 -O.an 12345 -O.o '+observer+' +O.c "Original BoN measurement of '+ant_hgt+'" +O.c "Mark Name: '+get_smes.mark_name+'" +O.c "GDA94: '+str(get_smes.mark_latitude)+' '+str(get_smes.mark_longitude)+'" -O.ag OSGV '+input_st[0]+'.tgd'
   #print(com_runpk)
   print(com_teqc)
   #run(com_runpk)
   #call(com_teqc, stdout=f)
   call(com_teqc)
   
   

if __name__ == "__main__":
   print(sys.argv[2:])
   main(arguement)
   
   
   
