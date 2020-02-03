#!/usr/bin/env python3
import sys, time, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests import *

r = '\033[031m'
g = '\033[032m'
b = '\033[036m'
k = '\033[030m'
n = '\033[00m'

banner = """
		 {r} ____{b} ____    __ {n}     __          
		 {r}/ / /{b}/ __/__ / /{n}_____/ /  ___ {g}____
		{r}/_  _/{b} _// -_) __{n}/ __/ _ \/ -_){g} __/{n}
		 {r}/_/{b}/_/  \__/\__/{n}\__/_//_/\__/{g}_/{n}
		 {r}MSF{n}{b}: http://www.{n}mmsecurity.n{g}et/forum/member.php?action=register&referrer=9450{n}
		                 		{r}v1.0{n}
""".format(r=r,b=b,n=n,g=g)
def main(banner, bl):
	print(banner)
	if bl:
		url = sys.argv[1]
		if 'http://' not in url:
			url = 'http://'+url
		elif 'https://' not in url:
			url = 'https://'+url
		else:
			print('[%s ERROR %s] No schema supplied. Perhaps you meant http://%s' % (r, n, url))
			sys.exit(1)
		header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4'}
		print('[%s*%s] Requesting to server...' % (g, n))
		t = time.time()
		try:
			rq = get(url, headers=header)
		except ConnectionError:
			print('[ %sFAILED%s ] Failed to establish a new connection' % (r,n))
			sys.exit(1)
		if rq.status_code == 200:
			print('\t[ %sOK%s ] DONE! -> %ss(%smins)' % (g, n, round(time.time() - t, 2), round((time.time() -t)/60, 4)))
			rf = input('[ %sINFO%s ] Folder name to save[Default: out]: ' % (b, n))
			out = '%s_%s' % (rf,time.strftime('%I%M%S')) if rf != '' else 'out_%s' % time.strftime('%I%M%S')
			os.system('mkdir %s' % out)
			os.chdir(out)
			print('\t[%s*%s] Saving Index...' % (g, n))
			with open('index.html', 'b+w') as file:
				file.write(rq.content)
				file.close()
				print('\t\t[ %sOK%s ] DONE! -> %ss(%smins)' % (g, n, round(time.time() - t, 2), round((time.time() -t)/60, 4)))
			print('\t[%s*%s] Saving Headers...' % (g,n))
			f = open('replied_headers.txt', 'w+')
			for key in rq.headers:
				headers_ = '%s: %s\n' % (key, rq.headers[key])
				f.write(headers_)
			f.close()
			print('\t\t[ %sOK%s ] DONE! -> %ss(%smins)' % (g, n, round(time.time() - t, 2), round((time.time() -t)/60, 4)))
			bs4 = BeautifulSoup(rq.text, 'lxml')
			link = bs4.findAll('link')
			script = bs4.findAll('script')
			img = bs4.findAll('img')
			if len(link) > 0 or len(script) > 0 or len(img) > 0:
				print('[{b}%{n}] Downloading the assets...\n'.format(b=b, n=n))
				for l in link:
					if l['rel'][0] == 'stylesheet':
						if l['href'].split('.')[1]:
							os.system('mkdir -p %s' % l['href'].split(l['href'].split('/')[-1::][0])[0])
							if 'http://' not in l['href'] or 'https://' not in l['href']:
								if url[-1::] == '/':
									os.system('cd %s && wget %s%s' % (l['href'].split(l['href'].split('/')[-1::][0])[0], url, l['href']))
								else:
									os.system('cd %s && wget %s/%s' % (l['href'].split(l['href'].split('/')[-1::][0])[0], url, l['href']))
							else:
								os.system('cd %s && wget %s' % (l['href'].split(l['href'].split('/')[-1::][0])[0], l['href']))
					if l['href'].split('.')[-1] == 'ico':
						fav = l['href'].split('/')[-1]
						if '/' in l['href']:
							mkdir('mkdir -p %s' % s['src'].split(s['src'].split('/')[-1::][0])[0])
							if 'http://' not in l['href'] or 'https://' not in l['href']:

									if url[-1::] == '/':
										os.system('cd %s && wget %s%s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], url, l['href']))
									else:
										os.system('cd %s && wget %s/%s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], url, l['href']))
							else:
								os.system('cd %s && wget %s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], l['href']))
						else:
							if 'http://' not in l['href'] or 'https://' not in l['href']:

									if url[-1::] == '/':
										os.system('wget %s%s' % (url, l['href']))
									else:
										os.system('wget %s/%s' % (url, l['href']))
							else:
								os.system('wget %s' % (l['href']))
				for s in script:
					if s.has_attr('src'):
						if '/' in s['src']:
							fav = s['src'].split('/')[-1]
							if '/' not in s['src'][:1:]:
								os.system('mkdir -p %s' % s['src'].split(s['src'].split('/')[-1::][0])[0])
							else:
								os.system('mkdir -p %s' % s['src'].split(s['src'].split('/')[-1::][0])[0][1::])
							if 'http://' not in s['src'] or 'https://' not in s['src']:
								if url[-1::] == '/' and s['src'][:1:] != '/':
									os.system('cd %s && wget %s%s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], url, s['src']))
								else:
									if '/' == s['src'][:1:]:
										os.system('cd %s && wget %s/%s' % (s['src'].split(s['src'].split('/')[-1::][0])[0][1::], url, s['src']))
									else:
										os.system('cd %s && wget %s/%s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], url, s['src']))
							else:
								os.system('cd %s && wget %s' % (s['src'].split(s['src'].split('/')[-1::][0])[0], s['src']))
						else:
							if 'http://' not in s['src'] or 'https://' not in s['src']:

									if url[-1::] == '/':
										os.system('wget %s%s' % (url, s['src']))
									else:
										os.system('wget %s/%s' % (url, s['src']))
							else:
								os.system('wget %s' % (s['src']))
				for i in img:
					if '/' in i['src']:
						fav = i['src'].split('/')[-1]
						if '/' not in i['src'][:1:]:
							os.system('mkdir -p %s' % i['src'].split(i['src'].split('/')[-1::][0])[0])
						else:
							os.system('mkdir -p %s' % i['src'].split(i['src'].split('/')[-1::][0])[0][1::])
						if 'http://' not in i['src'] or 'https://' not in i['src']:
							if url[-1::] == '/' and i['src'][:1:] != '/':
								os.system('cd %s && wget %s%s' % (i['src'].split(i['src'].split('/')[-1::][0])[0], url, i['src']))
							else:
								if '/' == i['src'][:1:]:
									os.system('cd %s && wget %s/%s' % (i['src'].split(i['src'].split('/')[-1::][0])[0][1::], url, i['src']))
								else:
									os.system('cd %s && wget %s/%s' % (i['src'].split(i['src'].split('/')[-1::][0])[0], url, i['src']))
						else:
							os.system('cd %s && wget %s' % (i['src'].split(i['src'].split('/')[-1::][0])[0], i['src']))
					else:
						if 'http://' not in i['src'] or 'https://' not in i['src']:

								if url[-1::] == '/':
									os.system('wget %s%s' % (url, i['src']))
								else:
									os.system('wget %s/%s' % (url, i['src']))
						else:
							os.system('wget %s' % (i['src']))
				print('[%s*%s] Finished in %ss(%smins)' % (g, n, round(time.time() - t, 2), round((time.time() -t)/60, 4)))
			else:
				print('[%s*%s] Finished in %ss(%smins)' % (g, n,round(time.time() - t, 2), round((time.time() -t)/60, 4)))
				sys.exit(0)
			sys.exit(0)
		else:
			print('\t[%s!%s] ERROR!' % (r,n))
			sys.exit(1)
	else:
		help()
def help():
	print('usage: %s [url]' % sys.argv[0])
if __name__ == '__main__':
	if sys.platform == 'linux':
		if len(sys.argv) < 2:
			main(banner, False)
		else:
			main(banner, True)
			sys.exit(1)
	else:
		print('[ ERROR ] Sorry this tool can run only in Linux platform.')
		sys.exit(1)
