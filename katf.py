#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib
import requests
import re, sys
from optparse import OptionParser
from time import strftime

class config:
	s_keywords = {'m':'movies', 't': 'tv', 'mu': 'music','g': 'games', 'a': 'applications','an': 'anime', 
			'b': 'books', 'lm': 'loseless', 's': 'usearch'}
	d_keywords = {'m':'Movies', 't': 'TV Shows', 'mu': 'Music','g': 'Games', 'a': 'Applications','an': 'Anime', 
			'b': 'Books', 'lm': 'Loseless Music'}
	URL = "https://kat.cr/"
	HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	DEFAULT_LINES = 20

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(parser, argv):
	parser.add_option("-l", "--latest", dest="lcategory", help="Get latest torrents")
	parser.add_option("-s", "--search", dest="search", help="Search for a torrent")
	parser.add_option("-n", "--number", dest="number", help="Specify the number of items")
	parser.add_option("-c", "--category", dest="category", help="Specify a category")
	parser.add_option("-m", "--magnet", dest="magnet", help="Retrieve magnet link from an URL")
	(options, args) = parser.parse_args()
	if options.lcategory:
		try:
			print "Sending a request to the site"
			r = requests.get(config.URL+config.s_keywords[options.lcategory],headers=config.HEADERS)
			soup = get_html(r)
			category = options.lcategory
			number = options.number
			if number > 0:
				get_latest(soup, number, r, options.lcategory)
			else:
				get_latest(soup, config.DEFAULT_LINES, r, options.lcategory)
		except KeyError:
			print bcolors.FAIL + "Unknown option"
		except requests.ConnectionError:
			print bcolors.FAIL + "Network problem"
	elif options.magnet:
		get_magnet(options.magnet)
	elif options.search:
		search(options.search, options)
	else:
		print "No option specified. Try -h or --help."

def get_html(r):
	html = r.content
	soup = BeautifulSoup(html, 'lxml')
	soup.prettify()
	return soup

def updateFile():
	f = open('latest', 'w')
	details = str(raw_input("Enter latest episode details: "))
	f.write(details)
	print "Done"
	f.close()

def checkflag(flag):
	if flag == 1:
		print bcolors.FAIL + "Nope not out yet :/"
	if flag == 0:
		prompt = str(raw_input("Update latest episode details? (y/n): "))
		if prompt == 'y':
			updateFile()

def get_latest(soup, number, r, category):
	counter = 0;
	try:
		desc = config.d_keywords[category]
		print "* Sending request to:", r.url, "with headers", config.HEADERS['user-agent']
		print "* Getting latest", desc, "torrents"
	except:
		print "error"
	for tag in soup.find_all('a', class_='cellMainLink'):
		print bcolors.OKBLUE + "[+] " + tag.get_text() + bcolors.ENDC
		print "Link: https://kat.cr" + tag['href']
		counter = counter + 1
		if counter >= int(number): break

def get_latest_search(soup, number, r, category, search):
	counter = 0;
	try:
		desc = config.d_keywords[category]
	except:
		desc = category
	try:
		print bcolors.OKBLUE+"* Sending request to:", r.url, "with headers", config.HEADERS['user-agent'], "at", strftime("%Y-%m-%d %H:%M:%S")
		print bcolors.OKBLUE+"* Getting latest", desc + ' ' + search, "torrents"
	except requests.ConnectionError:
		print bcolors.FAIL + "Network problem"
	flag = 1
	for tag in soup.find_all('a', class_='cellMainLink'):
		term = str(tag.get_text())
		if term.find(search) != -1:
			flag = 0
			print bcolors.OKBLUE + "[+] " + tag.get_text() + bcolors.ENDC
			print "Link: https://kat.cr" + tag['href']
		counter = counter + 1
		if counter >= int(number): break
	checkflag(flag)

def get_magnet(url):
	print "* Getting magnet link of", url
	r = requests.get(url,headers=config.HEADERS)
	soup = get_html(r)
	test = str(soup.find_all('a', class_='kaGiantButton '))
	print test[45:-55]


def search(keyword, options):
	try:
		r = requests.get(config.URL+config.s_keywords['s']+'/'+keyword,headers=config.HEADERS)
		f = open('latest', 'rw')
		search = f.readline().strip()
		f.close()
		soup = get_html(r)
		number = options.number
		if number > 0:
			get_latest_search(soup, number, r, options.search, search)
		else:
			get_latest_search(soup, config.DEFAULT_LINES, r, options.search, search)
	except KeyError:
			print bcolors.FAIL + "Unknown option"
	except requests.ConnectionError:
			print bcolors.FAIL + "Network problem"
	

def info():
	print bcolors.HEADER + "Is it out yet? v0.1" + bcolors.ENDC
	
if __name__ == '__main__':
	info()
	parser = OptionParser()
	main(parser, sys.argv[1:])
