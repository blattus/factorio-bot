# FactorioBot
FactorioBot is a Telegram Bot that uses Ansible to spin up / down a headless [Factorio](https://factorio.com/) server on demand.

![](media/start-stop.gif)

## Why?
Multliplayer Factorio is a great time, but there are a few drawbacks to locally hosting a game that friends connect to:
- The host needs a fast, low-latency, and reliable internet connection to prevent gameplay issues
	- Example: operating vehicles like cars in the game, which have noticeable control lag when connecting to a friend's instance
- In a traditional peer-to-peer hosting case, the server can't be "left on" for others to connect as they have time
	- If you're hosting a game as a player, your player stays logged in which means the server continues to advance the game state. This gets...problematic with aggressive biter game scenarios

Luckily, Factorio has a wonderful [headless](https://wiki.factorio.com/Multiplayer#Dedicated.2FHeadless_server) version of the server available. While it's easy enough to get this running on some at-home equipment, you still run into the network requirements listed above.

So -- to the cloud! There are some great community projects, including the wonderful [factorio.zone](factorio.zone) for quickly spinning up a cloud server. I thought it would be fun to try a version of that on my own, controlled by a bot. This way we can use a beefy virtual server for the game, but make sure we're only running it when we need to. 

For an example of cost savings with the current server config (4GB RAM, 2 vCPUs, 80GB storage)
- monthly cost: $20
- 12 hours per week for 4 weeks: $1.44

Plus, the actual server creation doesn't take too long. From my testing, the full process to start a DigitalOcean VPS, install Factorio, copy over a save file, register a service, and boot the server takes around **2 minutes** end-to-end.

# Installation
FactorioBot uses [Ansible](https://www.ansible.com/) to create, configure, and destroy server instances. The Telegram interaction is handled by [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). The ansible host and bot need to be run on a box wtih a persistent internet connection. I use a LXC container in my own infrastructure, but it would probably run just fine on a Raspberry Pi or a cheap VPS instance (Vultr has some that start at $2.50 / month).

## Getting started
- Clone this repo on the server that's going to run everything
	- make a copy of `config_example.py` and rename it to `config.py` for your own configs
- Create a virtual environment (optional) and install python dependencies (required): `pip install -r requirements.txt`
- Run `factorio_downloader.py` to grab the latest version of the factorio server. you might want to update the server version in `config.py` if you want a specific version

## Ansible
- Install ansible using the instructions [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). On Ubuntu: 

```bash
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible

```

- Update `/etc/ansible/config.cfg` and set `host_key_checking = False`. This is needed to keep the server setup playbook interaction-free since we run that in the background without any user input.

## DigitalOcean
- Create a DigitalOcean API key and add it to `config.py`
- Setup ssh keys: ansible uses key-based SSH to copy files and provision the VPS 
	- [create an ssh key](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) on the host running the files
	- Add the ssh key to the digitalocean dashboard (Settings > Security > SSH keys section)
	- Query the digitalocean API to get the numeric key ID, e.g.,:
		`curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer your-digitalocean-api-token" "https://api.digitalocean.com/v2/account/keys"`
	- Update `ansible_vars.yml` to include the appropriate numeric key ID(s) 
	- *note:* the ansible script doesn't pause for input, so make sure to source ssh keys using `ssh-add` / keychain / etc.

## Telegram
- Talk to [@botfather](https://t.me/botfather) to create a telegram bot; follow the prompts
	- Save your API key somewhere secret
	- Update `config.py` to include your bot API key 
- I recommend adding your bot to a group chat if needed, and then interacting with botfather to disable group adds if you want to keep your bot relatively private

## Running
- Run `bot.py`, or use the included `factorio-bot.service` to set up a system service. You probably shouldn't run this as root like I did




# alternatives considered / things for the future
- Initially I was thinking of using the DigitalOcean API directly and re-creating a new VPS based on a saved VM snapshot rather than from scratch each time. After some investigation of this approach I realized the thing we're doing here (copying some files and unzipipng a binary) are low-lift enough that they don't seem worth saving to a snapshot image
- Ideally we would support a range of possible VPS providers (made easier with Ansible due to a variety of provider-specific playbooks)
- This project doesn't support Factorio mods at all


