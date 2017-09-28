#!/usr/bin/python

import sys, getopt
from subprocess import run, call
import urllib.request, json, csv
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
   
   
   
