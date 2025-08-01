import requests
import urllib.request as urllib_request
import httpx
import aiohttp

TELEGRAM_BOT_TOKEN = '7784987344:AAEIY3r5FAMQ7FhgBlA5o_KAvZMm7xPMO9g'
TELEGRAM_CHAT_ID = '5887438800'

def notify_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        requests.post(url, data=data)
    except:
        pass

# patch requests
original_request = requests.request
def patched_request(method, url, *args, **kwargs):
    notify_telegram(f'📡 requests:\nMethod: {method}\nURL: {url}')
    return original_request(method, url, *args, **kwargs)
requests.request = patched_request

# patch urllib
original_urlopen = urllib_request.urlopen
def patched_urlopen(url, *args, **kwargs):
    notify_telegram(f'📡 urllib:\nURL: {url}')
    return original_urlopen(url, *args, **kwargs)
urllib_request.urlopen = patched_urlopen

# patch httpx
original_httpx_request = httpx.Client.request
def patched_httpx_request(self, method, url, *args, **kwargs):
    notify_telegram(f'📡 httpx:\nMethod: {method}\nURL: {url}')
    return original_httpx_request(self, method, url, *args, **kwargs)
httpx.Client.request = patched_httpx_request

# patch aiohttp
original_aiohttp_request = aiohttp.ClientSession._request
async def patched_aiohttp_request(self, method, url, *args, **kwargs):
    notify_telegram(f'📡 aiohttp:\nMethod: {method}\nURL: {url}')
    return await original_aiohttp_request(self, method, url, *args, **kwargs)
aiohttp.ClientSession._request = patched_aiohttp_request

# استدعاء السكربت المشفر
import bot