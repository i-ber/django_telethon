import datetime

from django.conf import settings

import aiohttp

class Botpress:
    _root_url = settings.BOTPRESS['ROOT_URL']
    _login_route = settings.BOTPRESS['LOGIN_ROUTE']
    _msg_route = settings.BOTPRESS['MSG_ROUTE'] # bot_id, user_id
    _email = settings.BOTPRESS['BOTPRESS_EMAIL']
    _pass = settings.BOTPRESS['BOTPRESS_PASS']
    _headers = {"Content-Type": "application/json"}
    # Принудительно устаревший токен
    _last_jwt_update = datetime.datetime.now() - datetime.timedelta(minutes=120)

    @classmethod
    async def auth(cls):
        url = cls._root_url + cls._login_route
        data = {'email': cls._email, 'password': cls._pass}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=cls._headers) as response:
                if response.status == 200:
                    res = await response.json()
                    print(res)
                    jwt_token = res['payload']['jwt']
                    cls._headers['Authorization'] = f"Bearer {jwt_token}"
                else:
                    print(f"Botpress auth error. Response status: {response.status}")
                    print(f"Error text: {response.text}")

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
                if response.status == 200:
                    res = await response.json()
                    print(res)
                    return res['responses']
                else:
                    print(f"Botpress send message error. Response status: {response.status}")
                    print(f"Error text: {response.text}")
