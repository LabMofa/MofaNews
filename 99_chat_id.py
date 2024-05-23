import requests

# Replace with your bot's token
bot_token = 'INPUT YOUR TOKEN'
# Get updates
response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates')

if response.status_code == 200:
    updates = response.json()
    chat_ids = set()
    
    for update in updates['result']:
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            chat_ids.add(chat_id)
        elif 'edited_message' in update:
            chat_id = update['edited_message']['chat']['id']
            chat_ids.add(chat_id)
        elif 'channel_post' in update:
            chat_id = update['channel_post']['chat']['id']
            chat_ids.add(chat_id)
        elif 'edited_channel_post' in update:
            chat_id = update['edited_channel_post']['chat']['id']
            chat_ids.add(chat_id)
        elif 'callback_query' in update:
            chat_id = update['callback_query']['message']['chat']['id']
            chat_ids.add(chat_id)
        elif 'inline_query' in update:
            chat_id = update['inline_query']['from']['id']
            chat_ids.add(chat_id)
        elif 'chosen_inline_result' in update:
            chat_id = update['chosen_inline_result']['from']['id']
            chat_ids.add(chat_id)
    
    print(f'Chat IDs: {chat_ids}')
else:
    print('Failed to get updates.')
