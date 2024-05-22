import requests

bot_token = '7109066009:AAF5dilbMQrgxd6fdHvRvOGPas-yBBLfvYQ'
CID = "1453432519"
msg = "Booking Succesfully Made!"

url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
print(requests.get(url).json())