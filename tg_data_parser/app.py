from threading import Thread
from time import sleep
import asyncio

import uvicorn
from fastapi import FastAPI
from loguru import logger
from telethon.sync import TelegramClient, events
from config import api_hash, api_id, phone

from config import my_host, get_info_delay
from crawler.data_crawler import crawl_channel
from views.articles import article_router
from views.channels import channels_router
from source.mongo import channels_list, add_example_channels, add_article


logger.add("data.log", rotation="100 MB", enqueue=True)
app = FastAPI()

app.include_router(article_router)
app.include_router(channels_router)


def daemon():
    while True:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as ex:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        client = TelegramClient('session1', api_id, api_hash)
        try:
            client.connect()
        except Exception as e:
            client.start(phone=phone)
        add_example_channels()
        channels = channels_list.find({})
        for i in channels:
            logger.info('get data from tg')
            # data = crawl_channel(client, i['link'])
            data = ["""\u200b«Восемь лет назад я уже писал статью о том, как делал простенький дампер (устройство для чтения картриджей) для Денди/Famicom. Думаю, пора рассказать о том, как этот проект преобразился спустя эти годы вместе с ростом моих скиллов»\n\nДампер картриджей для Денди/Famicom""", """\u200bНевероятные приключения Человека-Админа: в поисках хранилища паролей\n\nСильнейший из офисных супергероев\xa0— Человек‑Админ, защитник безопасности и хранитель паролей. Каждую рабочую неделю он сталкивается с новыми испытаниями: то нужно помочь коллегам выявить уязвимые пароли, то восстановить утерянный доступ к жизненно важным ресурсам.\n\nНа этой неделе ему предстоят сложнейшие испытания в его супергеройской карьере: подобрать самый сложный пароль, который защищает жизненно важную базу данных, вовремя сменить все пароли, которые мог скомпрометировать уволившийся сотрудник, и даже научиться работать в команде! Чтобы преодолеть все эти препятствия, Человек-Админ отправится на поиски решения для оптимального и удобного хранения паролей.""", """\u200bКем работать в IT в 2023: маркетолог\n\nРубрика «Кем работать в IT»\xa0— интервью с представителями IT-профессий, в которых специалисты рассказывают о тонкостях своей работы: плюсах, минусах, подводных камнях и заработной плате. Мы надеемся, что джунам и стажёрам она поможет больше узнать о том, что их ожидает на карьерном пути, а профессионалам\xa0— посмотреть на свою специальность через чужой опыт и, может быть, открыть для себя что-то новое.\n\nСегодня о своём опыте работы нам расскажет Ирина Черненко, маркетинг бизнес-партнёр в «Ростелеком-Солар»""", """Абракадабра текст для теста снова здесь"""]
            logger.info(data)
            # add_article(channel_id=i['_id'], article_text=data[0])
            break
        sleep(get_info_delay * 60)


@app.on_event("startup")
async def main():
    daemon_thread = Thread(target=daemon)
    daemon_thread.start()


if __name__ == "__main__":
    client = TelegramClient('session1', api_id, api_hash)
    # # try:
    # # client.connect()
    # # except Exception as e:
    # client.start(phone=phone)
    # data = crawl_channel(client, 'https://t.me/habr_com')
    # print(data)
    uvicorn.run(app, host=my_host, port=8000)
