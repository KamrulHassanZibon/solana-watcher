import requests
import json
import time
import os

# Set up Telegram bot information
telegram_bot_token = "<6167079188:AAHqQLFPtnlS3gqv8DQ0xApf8iaqfa0jD_I>"
telegram_channel_id = "+Xr-q8kfBWpNkYzJl"

# Set up Hello Moon API information
api_key = "4cc76a3f-5514-4818-9fd1-7387d51196b6"
solana_chain_id = "solana"
min_transaction_value = 100000  # Transactions over $100k USD

# Function to send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_id,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Error sending message to Telegram")

# Function to get the latest Solana transaction from the Hello Moon API
def get_latest_solana_transaction():
    url = f"https://api.hellomoon.io/v1/chains/{solana_chain_id}/transactions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "limit": 1,
        "offset": 0
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error getting latest transaction from Hello Moon API")
        return None
    transactions = json.loads(response.text)
    if len(transactions) == 0:
        return None
    transaction = transactions[0]
    return transaction

# Main loop
while True:
    transaction = get_latest_solana_transaction()
    if transaction and transaction["value"] >= min_transaction_value:
        value_in_usd = transaction["value"] / 10**6
        transaction_id = transaction["signature"]
        message = f"New Solana transaction detected!\nValue: ${value_in_usd:.2f} million\nTransaction ID: {transaction_id}"
        send_telegram_message(message)
    time.sleep(60)  # Check for new transactions every minute
