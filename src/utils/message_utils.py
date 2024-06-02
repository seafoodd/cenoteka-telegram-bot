import time
from bot_init import bot, banned_until, last_message_time, message_count_when_limit_reached, MESSAGE_COOLDOWN, \
    BAN_TIME


def handle_spamming(user_id) -> bool:
    # if the user is banned, ignore their messages
    if user_id in banned_until and banned_until[user_id] > time.time():
        return False

    # rate limiting
    if user_id in last_message_time and time.time() - last_message_time[
        user_id] < MESSAGE_COOLDOWN:
        send_message(user_id,
                     f"Please wait until {MESSAGE_COOLDOWN} seconds have passed since the last message.")
        message_count_when_limit_reached[user_id] = message_count_when_limit_reached.get(user_id,
                                                                                         0) + 1

        # If the user has sent too many messages in the cooldown period, ban them for a certain time
        if message_count_when_limit_reached[user_id] > 5:  # Adjust this value as needed
            banned_until[user_id] = time.time() + BAN_TIME
            send_message(user_id,
                         f"You were banned for {BAN_TIME} seconds due to too many messages.")

        return False
    return True


def send_message(user_id, message_text) -> None:
    bot.send_message(user_id, message_text)
