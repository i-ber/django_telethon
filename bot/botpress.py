import os
import datetime

from django.conf import settings

import aiohttp

class Botpress:
    _root_url = settings.BOTPRESS['ROOT_URL']
    _login_route = settings.BOTPRESS['LOGIN_ROUTE']
    _msg_route = settings.BOTPRESS['MSG_ROUTE'] # bot_id, user_id
    _email = os.environ["BOTPRESS_EMAIL"]
    _pass = os.environ["BOTPRESS_PASS"]
    _headers = {"Content-Type": "application/json"}
    # Принудительно устаревший токен
    _last_jwt_update = datetime.datetime.now() - datetime.timedelta(minutes=5)

    @classmethod
    async def auth(cls):
        url = cls._root_url + cls._login_route
        data = {'email': cls._email, 'password': cls._pass}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=cls._headers) as response:
                res = await response.json()
                print(res)
                jwt_token = res['payload']['jwt']
                cls._headers['Authorization'] = f"Bearer {jwt_token}"

    @classmethod
    async def token_update(cls):
        if datetime.datetime.now() - cls._last_jwt_update > datetime.timedelta(minutes=30):
            await cls.auth()

    @classmethod
    async def send_message(cls, bot_id, user_id, message):
        await cls.token_update()  # Проверяем и обновляем токен перед отправкой сообщения
        url = cls._root_url + cls._msg_route(bot_id, user_id)
        data = {
            "type": "text",
            "text": message,
            "includedContexts": ["global"],  # optional, for NLU context
            "metadata": {}  # optional, useful to send additional data for custom hooks
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=cls._headers) as response:
                res = await response.json()
                return res['responses']
