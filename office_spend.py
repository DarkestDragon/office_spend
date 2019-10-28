#! python3.7

from dialog_bot_sdk.bot import DialogBot
import grpc
import re

def on_msg(*params):
	global help
	global leftover_arr
	global user_ids
	msg = params[0].message.textMessage.text
	current_user = (params[0].sender_uid, params[0].peer)
	if msg == "/start" or msg == "" or msg == "help":
		bot.messaging.send_message(params[0].peer, help)
		if msg == "/start" and current_user not in user_ids:
			user_ids.append(current_user)
			leftover_arr.append(0.00)
	else:
		token_list = msg.split()
		match = re.search(r'\d+[.]\d{2}|\d+', msg)
		user_index = user_ids.index(current_user)
		if ' '.join(token_list[:3]).lower() == "у меня есть":
			if match:
				leftover_arr[user_index] = float(match.group(0))
				bot.messaging.send_message(params[0].peer, "ОК. Остаток :" + str(leftover_arr[user_index]))
			else:
				bot.messaging.send_message(params[0].peer, "Извините, не понял.\n" + help)
		elif match:
			leftover_arr[user_index] -= float(match.group(0))
			bot.messaging.send_message(params[0].peer, "Остаток: " + str(leftover_arr[user_index]))
		else:
			bot.messaging.send_message(params[0].peer, "Извините, не понял.\n" + help)

if __name__ == "__main__":
	bot = DialogBot.get_secure_bot(
		"hackathon-mob.transmit.im",
		grpc.ssl_channel_credentials(),
		"TOKEN"
	)
	with open("./spend_help.txt", "r") as help_file:
		help = help_file.read()
	user_ids = []
	leftover_arr = []
	bot.messaging.on_message(on_msg)
