import time
from src.bot_init import bot, banned_until, last_message_time, message_count_when_limit_reached, MESSAGE_COOLDOWN, \
    BAN_TIME


def handle_spamming(user_id) -> bool:
    # if the user is banned, ignore their messages
    if user_id in banned_until and banned_until[user_id] > time.time():
        send_message(user_id,
                     f"До окончания блокировки осталось {int(banned_until[user_id] - time.time())} секунд.")
        return False

    # rate limiting
    if user_id in last_message_time and time.time() - last_message_time[
        user_id] < MESSAGE_COOLDOWN:
        send_message(user_id,
                     f"Подождите, пока не прошло {MESSAGE_COOLDOWN} секунд с момента последнего сообщения.")
        message_count_when_limit_reached[user_id] = message_count_when_limit_reached.get(user_id,
                                                                                         0) + 1

        # If the user has sent too many messages in the cooldown period, ban them for a certain time
        if message_count_when_limit_reached[user_id] > 5:  # Adjust this value as needed
            banned_until[user_id] = time.time() + BAN_TIME
            send_message(user_id,
                         f"Вы были заблокированы на {BAN_TIME} секунд из-за слишком большого количества сообщений.")

        return False
    return True


def send_message(user_id, message_text) -> None:
    bot.send_message(user_id, message_text)
