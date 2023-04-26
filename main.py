"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from dataclasses import dataclass
import json
import pathlib 
from aiogram import Bot, Dispatcher, executor, types

@dataclass
class Settings:
    token:str
BASE_PATH = pathlib.Path(__file__).parent

with open(BASE_PATH.joinpath(".env"),'rb') as file:
    data = json.load(file)
    settings = Settings(**data)    

API_TOKEN = settings.token


class Register:
    _data = {}
    
    @classmethod
    def get(cls, pk):
        """Возврящяет значения из класса
        >>> Register.get(1)
        None
        >>> Register.set(1, "test")
        >>> Register.get(1)
        "test"
        """
        return cls._data.get(pk, None)
    
    @classmethod
    def set(cls, pk, val):
        """устанавливает значения из класса
        >>> Register.set(1,"test")
        >>> Register._data
        {1:"test"}
        """
        cls._data[pk] = val


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class PathDispather(object):
    __register = {}
    
    
    @classmethod
    def init(cls, dp: Dispatcher):
        for val in cls.__register.values():
            val.register(dp)
        dp.register_message_handler(cls.dispather)
    
    @classmethod
    def register(cls, obj) -> None:
        cls.__register[obj.prefix] = obj
    
    @staticmethod
    def get_state_key(message: types.Message):
        return f"state_{message.from_user.id}"

    @staticmethod
    def get_state_val(message: types.Message):
        return f"state_start_{cls.prefix}"

    @classmethod
    async def dispather(cls, message: types.Message):
        key = cls.get_state_key(message)
        data = Register.get(key)
        if data:
           prefix = data.split("_")[-1]
           return await cls.__register[prefix].process(message)
        else:
            message.reply("Состояние не установленно")   
        return None


class Base(object):
    prefix = ""

    @classmethod
    async def create(cls, message: types.Message):
        Register.set(f"state_{message.from_user.id}", f"state_start_{cls.prefix}")
    
    @classmethod
    async def process(cls, message: types.Message):
        pass

    @classmethod
    async def list(cls, message: types.Message):
        pass
    
    @classmethod
    async def get(cls, message: types.Message):
        pass
    
    @classmethod
    async def kill(cls, message: types.Message):
        pass
    
    @classmethod
    def register(cls, dispatcher: Dispatcher):
        dispatcher.register_message_handler(cls.create, commands=[f'create_{cls.prefix}'])
        dispatcher.register_message_handler(cls.list, commands=[f'list_{cls.prefix}'])
        dispatcher.register_message_handler(cls.get, commands=[f'get_{cls.prefix}'])
        dispatcher.register_message_handler(cls.kill, commands=[f'kill_{cls.prefix}'])

class Notes(Base):
    prefix = 'note'
    @classmethod
    async def list(cls, message: types.Message):
        await message.reply("Hi is good day")

class Task(Base):
    prefix = 'task'

    @classmethod
    async def create(cls, message: types.Message):
        await super().create(message)
        await message.reply("Можно создать задачи")
    @classmethod
    async def process(cls, message: types.Message):
        await message.reply("Успешно записана")
        


@dp.message_handler(commands = ['start', 'end'])
async def echo(message: types.Message):
    await message.answer("hellow")


if __name__ == '__main__':
    PathDispather.register(Notes)
    PathDispather.register(Task)
    PathDispather.init(dp)
    executor.start_polling(dp, skip_updates=True)
    