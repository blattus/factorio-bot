import config
import ansible_runner
import os
from shutil import copyfile

working_directory = os.getcwd()

def start_server():
	r = ansible_runner.run(private_data_dir=working_directory, inventory='hosts.ini',
		playbook='ansible_playbooks/create-droplet.yml')
	print("Finished starting server")
	print("Final status:")
	print(r.stats)
	print(r.events)
	return r.stats

def stop_server():
	# stop the server using ansible
	r = ansible_runner.run(private_data_dir=working_directory, inventory='hosts.ini',
		playbook='ansible_playbooks/destroy-droplet.yml')
	print("Finished stopping server")
	print("Final status:")
	print(r.stats)
	return r.stats

	
def fetch_savefile():
	# fetch the save using ansible	
	r = ansible_runner.run(private_data_dir=working_directory, inventory='hosts.ini',
		playbook='ansible_playbooks/fetch-save.yml')
	print("Finished fetching savefile")
	print("Final status:")
	print(r.stats)
	return r.stats

def update_latest_save():
	'''
	update the `latest_save` file
	
	saves are of the format `save_YYYY-MM-DD_epoch.zip` so we can use
	the epoch timestamp to figure out which save is the most recent
	'''

	files = os.listdir('factorio_saves')
	latest_timestamp = 1 # placeholder for us to compare during iteration
	latest_savefile = ''

	for file in files:
		split_file = file.split('_')
		if len(split_file) < 3:	# ignore all filenames that don't have a date + timestamp
			pass
		else:
			this_files_epoch_timestamp = int(split_file[2].split('.')[0]) 
			if this_files_epoch_timestamp > latest_timestamp:
				latest_timestamp = this_files_epoch_timestamp
				latest_savefile = file

	# overwrite the old `latest_save` with the newly-calculated latest save
	# note: this is kinda dangerous as implemented; might be worth archiving the old saves somehow
	copyfile('factorio_saves/{}'.format(latest_savefile), 'factorio_saves/latest_save.zip')

	return(latest_savefile)
