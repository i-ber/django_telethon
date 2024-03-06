from functools import partial

from django.dispatch import receiver
from telethon import events

from django_telethon.signals import telegram_client_registered

async def botpress_responce(event, client_session):
    session_name = client_session.name
    msg_text = event.raw_text
    username = event.sender.username
    user_id = event.chat_id
    #phone = event.sender.phone
    #first_name = event.sender.first_name
    #last_name = event.sender.last_name

    print(session_name, user_id, msg_text, sep =' | ')
    if username == "i_berdnikov":
        async with event.client.conversation(user_id) as conv:
            await conv.send_message(f'Привет, я бот "{session_name}"')

@receiver(telegram_client_registered)
def receiver_telegram_client_registered(telegram_client, client_session, *args, **kwargs):
    handler = partial(botpress_responce, client_session=client_session)
    telegram_client.add_event_handler(
        handler,
        events.NewMessage,
    )
