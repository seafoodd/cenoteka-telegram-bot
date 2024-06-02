import logging
import time


def configure_logging() -> None:
    logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def send_search_log(message, search_query) -> None:
    user_id = message.chat.id
    logging.info(f'User: @{message.chat.username}({user_id}) - Search Query: "{search_query}" - Time: {time.ctime()}')
    print(f'User: @{message.chat.username}({user_id}) - Search Query: "{search_query}" - Time: {time.ctime()}')


def send_ban_log(message, ban_time) -> None:
    user_id = message.chat.id
    print(
        f'User: @{message.chat.username}({user_id}) was banned for {ban_time} seconds due to too many messages. - {time.ctime()}')
    logging.info(
        f'User: @{message.chat.username}({user_id}) was banned for {ban_time} seconds due to too many messages. - {time.ctime()}')
