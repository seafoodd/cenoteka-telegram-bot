# Cenoteka Telegram Bot

This is a Python-based telegram bot that helps users find best prices for the products on Cenoteka.

## Features

- Search for products by name
- Get product details including name, discount, and prices from different shops

## Commands

- `/start`: Start the bot
- `/help`: Get help on how to use the bot
- `[text]`: Enter the name of the product you want to find

## Installation

1. Clone this repository
```bash
git clone https://github.com/seafoodd/cenoteka-telegram-bot
cd cenoteka-telegram-bot
```
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project and add the following environment variables:

```dotenv
TOKEN='$YOUR-BOT-TOKEN'
MESSAGE_COOLDOWN=5
BAN_TIME=60
```

## Usage

To start the bot, run the following command:

```bash
cd src
python main.py
```

Then, you can interact with the bot using the supported commands.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
