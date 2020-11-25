# set this to true to log :allthethings: 
debug = False

TELEGRAM_TOKEN = 'your-telegram-bot-token'

# Telegram chat IDs to interact with. note these should be integers
allowed_chat_ids = [12345678,-98765432]

# the ansible playbooks depend on this being set as an environment variable so we can do that here
import os
os.environ['DO_API_TOKEN'] = 'your-digitalocaen-api-token'

# Factorio-specific configs
# the directory is used in `factorio_downloader.py` as the location for the server files
factorio_headless_directory = 'factorio_headless'
factorio_server_version = '1.1.0'

