import discord
import datetime
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='$')


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def dembel():
    td = datetime.date.today()
    dds = "2020-12-15"
    d = dds.split('-')
    dd = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    resd = dd - td
    return str(resd).split()[0]


def store_img(imgLink):
    link = imgLink.split(" ")
    with open("imgLink.txt", "r") as f:
        existLines = f.readlines()
    if link[1]+"\n" in existLines:
        return 1
    else:
        with open("imgLink.txt", "a") as f:
            f.write(f"""{link[1]}\n""")
            return 0


def get_img(imgNumber):
    with open("imgLink.txt", "r") as f:
        lines = f.readlines()
        return lines[imgNumber].strip()


def img_file_size():
    with open("imgLink.txt", "r") as f:
        lines = f.readlines()
        return len(lines)

game_gunlet = ""
def gun_gunlet(message):
    global game_gunlet
    game_name = str(message.content).split(" ")
    game_gunlet += game_name[1] + "+"
    return game_gunlet


token = read_token()

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("гольф промеж твоих булок"))


@client.event
async def on_message(message):

    global game_gunlet

    if message.content.startswith("!help"):
        embed = discord.Embed(title="Помощь по боту", description="Итак гаврики вот вам парочку команд")
        embed.add_field(name="!t", value="Оставшиеся дни до дембеля")
        embed.add_field(name="!s url", value="Сохраняет картинку по сылке")
        embed.add_field(name="!o", value="Показывает картинку по порядковуму номеру")
        embed.add_field(name="!r", value="Выпуливает рандомную картинку")
        embed.add_field(name="!ga", value="Добавляет игру в рулетку")
        embed.add_field(name="!gc", value="Чистит рулетку")
        embed.add_field(name="!gs", value="Показывает победителя рулетки")
        await message.channel.send(content=None, embed=embed)

    elif message.content.startswith("!t"):
        await message.channel.send(f"""{dembel()}""")

    elif message.content.startswith("пидр"):
        await message.channel.send(f"""скорее {message.author} пидр""")

    elif message.content.startswith("!s "):
        if "https" in message.content and len(message.content) > 10:
            if "twitch.tv" in message.content or "youtube" in message.content:
                await message.channel.send("не кидай сюда хню")
            else:
                if store_img(str(message.content)) == 0:
                    await message.channel.send("забрал")
                else:
                    await message.channel.send("изображение уже есть мудила")

    elif message.content.startswith("!o "):
        num = str(message.content).split(" ")
        await message.channel.send(get_img(int(num[1])))

    elif message.content.startswith("!r"):
        await message.channel.send(get_img(random.randint(0, img_file_size()-1)))

    elif message.content.startswith("!ga "):
        if str(message.content) == "!ga":
            await message.channel.send("Напиши название дурашка")
        else:
            await message.channel.send(f"""Игра {str(message.content).split(" ")[1]} добавлена в обойму""")
            await message.channel.send(f"""Текущие игры в обойме: {gun_gunlet(message)}""")

    elif message.content.startswith("!gc"):
        game_gunlet = ""
        await message.channel.send("Магазин разряжен")

    elif message.content.startswith("!gs"):
        if game_gunlet == "":
            await message.channel.send("Ты куда стреляешь обойма то пустая")
        else:
            winner = game_gunlet.split("+")
            await message.channel.send(f"""Победитель: {winner[random.randint(0,len(winner)-2)]}""")
            await message.channel.send("Если кончил стрелять то разряди магазин с помощью !gc")


client.run(token)
