from functools import partial

from django.dispatch import receiver
from telethon import events

from django_telethon.signals import telegram_client_registered

from .botpress import Botpress

async def botpress_responce(event, client_session):
    session_name = client_session.name

    sender = await event.get_sender()
    msg_text = event.raw_text
    user_id = event.chat_id
    bot_id = "test1" # в будущем сессия будет связана с именем отеля - так будем определять с кем общаться

    #username = sender.username
    #phone = sender.phone
    #first_name = sender.first_name
    #last_name = sender.last_name

    print(session_name, user_id, msg_text, sep =' | ')
    if sender.username and sender.username == "i_berdnikov":
        response = await Botpress.send_message(bot_id, user_id, msg_text)
        for message in response:
            await event.client.send_message(user_id, message)

        #async with event.client.conversation(user_id) as conv:
        #    await conv.send_message(f'Привет, я бот "{session_name}"')

@receiver(telegram_client_registered)
def receiver_telegram_client_registered(telegram_client, client_session, *args, **kwargs):
    handler = partial(botpress_responce, client_session=client_session)
    telegram_client.add_event_handler(
        handler,
        events.NewMessage,
    )
