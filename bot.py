import asyncio
import aioschedule
import os
from sqlalchemy import select, create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from telebot.async_telebot import AsyncTeleBot, types
import json

PLAYER_START_DATA = None 
TOKEN = '5922991439:AAFtURg7fdlC0G1xPe-ZyTGAWi0BYTjXJ-o'
bot = AsyncTeleBot(TOKEN)

engine = create_engine('sqlite+pysqlite:///chinook.db', echo=True)
session = None 

Session = sessionmaker(bind=engine, future=True, expire_on_commit=False)
Base = declarative_base() # предок для всех моделей (таблиц)


def InitConfigs():
    global PLAYER_START_DATA

    with open('player_init_data.json', 'r') as f:
        PLAYER_START_DATA = json.loads(f.read())


class Players(Base):
    __tablename__ = 'players' # имя таблицы

    PlayerId = Column(Integer, name='PlayerId', primary_key=True) 
    Nickname = Column(String) 
    Level = Column(Integer) 
    Hp = Column(Integer) 
    CurHp = Column(Integer) 
    Money = Column(Integer) 
    Attack = Column(Integer) 
    MagicAttack = Column(Integer) 
    Xp = Column(Integer) 
    Armour = Column(Integer) 
    MagicArmour = Column(Integer)
    LocationID = Column(Integer)


class Mobs(Base):
    __tablename__ = 'mobs' # имя таблицы

    MobID = Column(Integer, name='MobID', primary_key=True)
    Hp = Column(Integer) 
    Xp = Column(Integer) 
    ReqLevel = Column(Integer) 
    AttackType = Column(Integer)
    Attack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)


class Locations(Base):
    __tablename__ = 'locations' # имя таблицы

    LocationID = Column(Integer, name='LocationID', primary_key=True)
    XCoord = Column(Integer) 
    YCoord = Column(Integer) 
    LocationType = Column(String)


class Items(Base):
    __tablename__ = 'items'

    ItemId = Column(Integer, name='ItemID', primary_key=True)
    Cost = Column(Integer) 
    CostToSale = Column(Integer) 
    ItemType = Column(String) 
    Hp = Column(Integer) 
    Mana = Column(Integer) 
    Attack = Column(Integer) 
    MagicAttack = Column(Integer) 
    Armour = Column(Integer) 
    MagicArmour = Column(Integer) 
    ReqLevel = Column(Integer)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hi! It's time to start your adventure! \n \
                                 Please use /create_character <name> to rise your warrior!")


def get_city_actions_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton("Check inventory")
    item_2 = types.KeyboardButton("Visit shop")
    item_3 = types.KeyboardButton("Go fight")
    item_4 = types.KeyboardButton("Print character info")
    markup.add(item_1, item_2, item_3, item_4)
    return markup


def add_player(id, character_name):
    new_player = Players(PlayerId=id, \
                         Nickname=character_name, \
                         Level=PLAYER_START_DATA['Level'], \
                         Hp=PLAYER_START_DATA['Hp'], \
                         CurHp=PLAYER_START_DATA['CurHp'], \
                         Money=PLAYER_START_DATA['Money'], \
                         Attack=PLAYER_START_DATA['Attack'], \
                         MagicAttack=PLAYER_START_DATA['MagicAttack'], \
                         Xp=PLAYER_START_DATA['Xp'], \
                         Armour=PLAYER_START_DATA['Armour'], \
                         MagicArmour=PLAYER_START_DATA['MagicArmour'], \
                         LocationID=PLAYER_START_DATA['LocationID'])

    session.add(new_player)


@bot.message_handler(commands=['create_character'])
async def create_character(message):
    args = message.text.split()
    print(len(args))
    if len(args) != 2:
        return await bot.reply_to(message, "Please call this command with single parameter")

    character_name = args[1]
    query = select(Players).where(Players.Nickname == character_name)
    player = session.execute(query).scalar()
    print('player', player)

    if player != None:
        return await bot.reply_to(message, 'Sorry character with such a name already exists')

    add_player(message.from_user.id, character_name)

    return await bot.send_message(message.chat.id, "Uffff", reply_markup=get_city_actions_markup())



@bot.message_handler(content_types=['text'])
async def message_reply(message):
    if message.text == "Check inventory":
        pass
    elif message.text == "Visit shop":
        pass
    elif message.text == "Go fight":
        await bot.send_message(message.chat.id, "Sorry Skyrim for this platform is not available yet, please wait another year and we'll release it at E3 2023, respectfully Todd")
    elif message.text == "Print character info":
        # Get character information
        pass
        
    return await bot.send_message(message.chat.id, "Please choose your next action", reply_markup=get_city_actions_markup())


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


if __name__ == '__main__':
    InitConfigs()
    print(PLAYER_START_DATA)
    session = Session()
    asyncio.run(main())