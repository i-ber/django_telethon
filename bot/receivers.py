import asyncio

from functools import partial

from django.dispatch import receiver
from telethon import events

from django_telethon.signals import telegram_client_registered

from .botpress import Botpress
from bot.models import NewDialogs

async def botpress_responce(event, client_session):
    session_name = client_session.name

    sender = await event.get_sender()
    msg_text = event.raw_text
    user_id = event.chat_id
    bot_id = "test1"  # в будущем сессия будет связана с именем отеля - так будем определять с кем общаться

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


async def start_new_dialogs(telegram_client, client_session):
    for new_dialog in NewDialogs.objects.filter(have_to_start=True, client_session=client_session):
        bot_id = "test1"
        # получаем пользователя dialog.phone_number
        user = await telegram_client.get_entity(new_dialog.phone_number)
        response = await Botpress.send_message(bot_id, user.id, "\start")
        for message in response:
            await telegram_client.send_message(user.id, message)

        new_dialog.have_to_start = False
        new_dialog.save()


@receiver(telegram_client_registered)
def receiver_telegram_client_registered(telegram_client, client_session, *args, **kwargs):
    handler = partial(botpress_responce, client_session=client_session)
    telegram_client.add_event_handler(
        handler,
        events.NewMessage,
    )

    # Запускаем асинхронную задачу из синхронного контекста
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Если loop уже запущен (например, в асинхронной вьюхе или другом асинхронном контексте),
        # лучше использовать create_task или run_coroutine_threadsafe
        asyncio.run_coroutine_threadsafe(start_new_dialogs(telegram_client, client_session), loop)
    else:
        # Если loop не запущен, мы можем запустить его здесь, но это редкая ситуация для Django
        loop.run_until_complete(start_new_dialogs(telegram_client, client_session))
