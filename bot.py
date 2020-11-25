import config
import telebot 
import re
import server_handler

def listener(messages):
	'''
	logs if we receive a message from a chat not on our allowlist
	prints all server-related commands to stdout for debugging
	if debug is set to true, prints *all* chats to stdout 
	TODO: update this to use python logging
	'''
	for m in messages:
		if m.chat.id not in config.allowed_chat_ids:
			print('received message from non-allowed chat ID: {}'.format(m.chat.id))
			print(m)
			bot.send_message(m.chat.id, "Sorry, you're not allowed to interact with me")
			return
		if config.debug:
			print(m) # if debug=True print everything
		else:
			if m.text:
				if 'server' in m.text: # else only print server-related things for cleaner logging
					print('incoming message: {}'.format(m.text))


bot = telebot.TeleBot(config.TELEGRAM_TOKEN, parse_mode="MARKDOWN", threaded=False)
bot.set_update_listener(listener)

@bot.message_handler(regexp="@factorio_server_bot start_server")
def handle_start(message):
	chat_id = message.chat.id
	if chat_id not in config.allowed_chat_ids: return	#TODO: refactor this :/ 

	bot.send_message(chat_id, '🔧 OK! Starting server – this will take a few minutes. I\'ll let you know when it\'s ready')

	server_result = server_handler.start_server()
	if server_result['dark'] or server_result['failures']:
		bot.send_message(chat_id, '❓ Something went wrong, check the logs for more info')
	else:
		ip_address = list(server_result['ok'].keys())[1] # TODO: fix this is it's really brittle
		bot.send_chat_action(chat_id, 'typing')
		bot.send_message(chat_id, '🚀 Server launched! IP address is: `{}` – have fun!'.format(ip_address))

@bot.message_handler(regexp='@factorio_server_bot stop_server')
def handle_stop(message):
	chat_id = message.chat.id
	if chat_id not in config.allowed_chat_ids: return

	bot.send_message(chat_id, '🛑 Got it – stopping the server')

	# fetch the savefile from the cloud server
	# if this fails we want to stop since otherwise we could potentially lose the save
	server_result = server_handler.fetch_savefile()
	if server_result['dark'] or server_result['failures']:
		bot.send_message(chat_id, '❓ Something went wrong, check the logs for more info')
		return

	# do some local file manipulation to update `latest_save.zip` so we're ready for next time
	latest_savefile = server_handler.update_latest_save()

	# stop the server
	server_result = server_handler.stop_server()
	if server_result['dark'] or server_result['failures']:
		bot.send_message(chat_id, '❓ Something went wrong, check the logs for more info')
	else:
		bot.send_message(chat_id, '⬇️ Server shutdown successfully')
		bot.send_message(chat_id, '🗂 I\'ll remember this for next time, but just in case, here\'s the latest save file:')
		# TODO: this works to send a file (!), move it to the "shutdown" and "fetch save" functions
		bot.send_chat_action(chat_id, 'upload_document')
		bot.send_document(chat_id, open('factorio_saves/{}'.format(latest_savefile), 'rb'))

# TODO: implement way to change server version
@bot.message_handler(regexp='@factorio_server_bot check_version')
def set_factorio_version(message):
	chat_id = message.chat.id
	if chat_id not in config.allowed_chat_ids: return

	bot.send_message(chat_id, '📍 The currently set Factorio version is {}'.format(config.factorio_server_version))

@bot.message_handler(commands=['ping'])
def handle_ping(message):
	chat_id = message.chat.id
	if chat_id not in config.allowed_chat_ids: return

	bot.reply_to(message, "pong")


bot.polling()


