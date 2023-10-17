#!/usr/bin/python3
# dedomil downloader
# powered by hdtune2k

import os
import sys
import urllib
import requests
import shutil
from lxml import etree
from fnmatch import fnmatch
from os.path import basename

# user interface
gameid = input("gameid> ")

# define target url
target_url = 'http://d*mil.net/games/' + gameid + '/screens' # fill the website url while using
fore_add = 'http://d*mil.net' # fill the website url while using

# generate workdir
defpath = os.path.dirname(__file__)
outpath = str(defpath) + '/output'
tmppath = str(defpath) + '/tmp'
os.makedirs(outpath)
os.makedirs(tmppath)

# check os
curr_os = sys.platform

# extract the href content
req = requests.get(target_url, 'html.parser')
req.encoding = 'utf-8'
html = etree.HTML(req.text)
linklist = html.xpath("//a/@href")
reslist = html.xpath("//a/text()")
req.close()

# handles the data
restor = []
res_counter = 0
link_counter = 0
errcount = 0
dledcount = 0

# store resolutions info
for res in reslist:
	if fnmatch(res,'*x*') :
		restor.append(res)
		res_counter = res_counter + 1

print("download started")
for item in linklist:
	if fnmatch(item,'/games/' + gameid + '/screen/*') :
		# create dir for each resolution
		os.makedirs(str(outpath) + '/' + str(restor[link_counter]))
		# fetches all jars from address
		reallink = fore_add + item
		req = requests.get(reallink, 'html.parser')
		req.encoding = 'utf-8'
		html = etree.HTML(req.text)
		dllist = html.xpath("//a/@href")
		req.close()
		# batch download
		for dlitem in dllist:
			if fnmatch(dlitem,'/games/' + gameid + '/download*') :
				os.system('cd ' + str(tmppath) + ' && ' + 'curl -OJ ' + fore_add + dlitem + ' 2>>../status.log')
				# duplicate file handler
				tmpfn = os.listdir(tmppath)[0] # it should be only one file
				existlist = os.listdir(str(outpath) + '/' + str(restor[link_counter]))
				for efname in existlist:
					if efname == tmpfn :
						foren = tmpfn.split('.', 1)[0]
						suffixn = tmpfn.split('.', 1)[1]
						foren = str(foren) + '-1'
						fullname = str(foren) + '.' + str(suffixn)
						shutil.move(os.path.join(str(tmppath) + '/' + str(tmpfn)), os.path.join(str(outpath) + '/' + str(restor[link_counter]) + '/' + str(fullname)))
				if len(os.listdir(tmppath)) == 0 :
					# already moved to output skipping
					print('saving a duplicate file using another name')
				else:
					shutil.move(os.path.join(str(tmppath) + '/' + str(tmpfn)), os.path.join(str(outpath) + '/' + str(restor[link_counter]) + '/' + tmpfn))
				# error checks
				logpath = str(defpath) + '/status.log'
				f = open(logpath, "r")
				logdat = f.read()
				if fnmatch(logdat, '*curl: (*)*') :
					print("network error caused abortation")
					if fnmatch(curr_os, '*win*') :
						input("press any key to exit...")
					quit()
				else:
					dledcount = dledcount + 1
					if dledcount == 1 :
						inditext = ' file'
					else:
						inditext = ' files'
					print("downloaded " + str(dledcount) + str(inditext))
		# removes jads
		jads = os.listdir(str(outpath) + '/' + str(restor[link_counter]))
		for file in jads:
			if '.' in file:
				suffix = file.split('.')[-1]
				if suffix == 'jad' :
					os.remove(os.path.join(str(outpath) + '/' + str(restor[link_counter]), file))

		link_counter = link_counter + 1

# removes log
f.close()
os.remove(os.path.join(str(defpath) + '/status.log'))

print("operation completed")
if fnmatch(curr_os, '*win*') :
	input("press any key to exit...")
quit()
