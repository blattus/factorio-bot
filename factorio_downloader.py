'''
checks for and downloads the latest version of the Factorio headless server.

server files are saved in `./factorio_headless`
'''

import re
import requests
import os
import time
from config import factorio_headless_directory, factorio_server_version


def main():
	# make the directory if it doesn't exist
	if factorio_headless_directory in os.listdir(os.getcwd()):
		pass
	else:
		os.mkdir(factorio_headless_directory)
	
	download_single_factorio_file(factorio_server_version)


def download_single_factorio_file(version):
	'''
	downloads the headless Factorio server files for a given `version`
	'''
	base_url = 'https://factorio.com/get-download/{}/headless/linux64'
	base_filename = 'factorio_headless_x64_{}.tar.xz'

	print('downloading factorio headless version {}'.format(version))
	server_file = requests.get(base_url.format(version), stream=True)
	with open('{}/factorio_headless_x64_{}.tar.xz'.format(factorio_headless_directory,version),'wb') as f: 
		for chunk in server_file.raw.stream(1024, decode_content=False):
			if chunk:
				f.write(chunk)
	print('download of version {} succeeded!'.format(version))

def download_factorio_files():
	'''
	unused for now, this downloads the latest 5 versions of the Factorio headless server
	based on the data on the Factorio download archives webpage.
	'''

	webpage = requests.get('https://factorio.com/download/archive')
	
	# use re to parse the factorio page and obtain just version numbers
	# we can generally trust the results are sorted from most recent --> least recent
	# but later could sort this if needed
	temp_results = re.findall('get-download\/(.*)\/headless',webpage.text)
	versions = temp_results
	print('found {} possible downloads'.format(len(versions)))

	base_url = 'https://factorio.com/get-download/{}/headless/linux64'
	base_filename = 'factorio_headless_x64_{}.tar.xz'

	# download the last 5 server versions
	for version in versions[0:5]:
		if base_filename.format(version) in os.listdir(factorio_headless_directory):
			print('version {} already downloaded. skipping...'.format(version))
		else:
			print('downloading factorio headless version {}'.format(version))
			server_file = requests.get(base_url.format(versions[0]), stream=True)
			with open('{}/factorio_headless_x64_{}.tar.xz'.format(factorio_headless_directory,version),'wb') as f: 
				for chunk in server_file.raw.stream(1024, decode_content=False):
					if chunk:
						f.write(chunk)
			print('download of version {} succeeded!'.format(version))
		time.sleep(5) # so we don't spam the factorio host



if __name__ == '__main__':
	main()

