import discord
from discord.ext import commands, tasks
import datetime
import random


client = commands.Bot(command_prefix='.', case_insensitive=True)

with open("imgLink.txt", "r") as f:
    lines = f.readlines()

game_list = ''


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


@client.event
async def on_ready():
    #my_background_task.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Escape from Tarkov"))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Такой команды нет дурашка",
                              description="Смотри .info что б не обосраться в следующий раз")
        await ctx.send(content=None, embed=embed)


@tasks.loop(hours=24)
async def my_background_task():
    channel = client.get_channel(683756925917462620) #поменять на 655490771222528020
    await channel.send(f"{str((datetime.date(int(2020), int(12), int(15)))-datetime.date.today()).split()[0]}")


@client.event
async def on_message(message):
    if message.content.startswith("пидр"):
        await message.channel.send(f"""скорее {message.author} пидр""")
    await client.process_commands(message)


@client.command(aliases = ['sas', 'sw'])
async def say(ctx, *, arg):
    await ctx.send(f"""{arg}""")


@client.command(aliases = ['i', 'inf'])
async def info(ctx):
    embed = discord.Embed(title="Помощь по боту", description="Итак гаврики вот вам парочку команд")
    embed.add_field(name=".d", value="Оставшиеся дни до дембеля")
    embed.add_field(name=".s url", value="Сохраняет картинку по сылке")
    embed.add_field(name=".l или .l номер", value="Показывает картинку по порядковуму номеру или рандом если без числа")
    embed.add_field(name=".g название игры", value="Добавляет игру в рулетку")
    embed.add_field(name=".g start или .g clear", value="Запуск рулетки или ее очистка")
    embed.add_field(name=".8 и свой вопрос", value="Получи ответ на свой вопросец от писаря")
    await ctx.send(content=None, embed=embed)


@client.command(aliases = ['d', 'dem'])
async def dembel(ctx):
    td = datetime.date.today()
    dds = "2020-12-15"
    d = dds.split('-')
    dd = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    resd = dd - td
    #await ctx.send(f"""{str(resd).split()[0]}""")

    embed = discord.Embed(title="Шо там по возращениею?", description=f"Вернусь домой через: {str(resd).split()[0]}")
    await ctx.send(content=None, embed=embed)


@client.command(aliases = ['s', 'si'])
async def img_save(ctx, link):
    if "https" in link and len(link) > 10:
        if "twitch.tv" in link or "youtube" in link:
            #await ctx.send("не кидай сюда хню")

            embed = discord.Embed(title="Не кидай сюда хню")
            await ctx.send(content=None, embed=embed)
        else:
            with open("imgLink.txt", "r") as f:
                existLines = f.readlines()
            if link+'\n' not in existLines:
                #await ctx.send("забрал")

                embed = discord.Embed(title="Забрал")
                await ctx.send(content=None, embed=embed)

                with open("imgLink.txt", "a") as f:
                    f.write(f"""{link}\n""")
            else:
                #await ctx.send("изображение уже есть мудила")

                embed = discord.Embed(title="Изображение уже есть мудила")
                await ctx.send(content=None, embed=embed)


@client.command(aliases = ['l', 'il'])
async def img_load(ctx, img_num = None):
    with open("imgLink.txt", "r") as f:
        global lines
        lines = f.readlines()
        if img_num == None:
            img_num = random.randint(0, len(lines) - 1)
            await ctx.send(f"""{lines[img_num].strip()}""")
        else:
            await ctx.send(f"""{lines[int(img_num)].strip()}""")


@client.command(aliases = ['g', 'gr'])
async def game_roulette(ctx, *, game_name):
    global game_list
    if str(game_name) == "clear":
        game_list = ""
        #await ctx.send("Магазин разряжен")

        embed = discord.Embed(title="Магазин разряжен")
        await ctx.send(content=None, embed=embed)

    elif str(game_name) == "start":
        if game_list == "":
            #await ctx.send("Ты куда стреляешь обойма то пустая")

            embed = discord.Embed(title="Ты куда стреляешь обойма то пустая")
            await ctx.send(content=None, embed=embed)
        else:
            winner = game_list.split("+")
            #await ctx.send(f"""Победитель: {winner[random.randint(0, len(winner) - 2)]}""")
            #await ctx.channel.send("Если кончил стрелять то разряди магазин с помощью .g clear")

            embed = discord.Embed(title=f"""Победитель: {winner[random.randint(0, len(winner) - 2)]}""")
            embed.add_field(name="----", value="Если кончил стрелять то разряди магазин с помощью .g clear")
            await ctx.send(content=None, embed=embed)
    else:
        game_list += game_name + '+'
        #await ctx.send(f"""Игра {game_name} добавлена в обойму""")
        #await ctx.send(f"""Текущие игры в обойме: {game_list}""")

        embed = discord.Embed(title=f"""Игра {game_name} добавлена в обойму""")
        embed.add_field(name="Текущие игры в обойме:", value=f"""{str(game_list)}""")
        await ctx.send(content=None, embed=embed)


@client.command()
async def clear(ctx, amount = 4):
    if amount < 5:
        await ctx.channel.purge(limit=amount)
        #await ctx.send("уничтоженно 4 сообщения")

        embed = discord.Embed(title="Уничтоженно 4 сообщения")
        await ctx.send(content=None, embed=embed)
    else:
        #await ctx.send("нахуйя ты пол планеты удалить хочешь?")

        embed = discord.Embed(title="Нахуйя ты пол планеты удалить хочешь?")
        await ctx.send(content=None, embed=embed)


@client.command(aliases = ['8', 'ball'])
async def _8ball(ctx, *, quest):
    responses = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да', 'Можешь быть уверен в этом',
                 'Мне кажется — да', 'Вероятнее всего', 'Хорошие перспективы', 'Знаки говорят — да', 'Да',
                 'Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять',
                 'Даже не думай', 'Мой ответ — нет', 'По моим данным — нет', 'Перспективы не очень хорошие', 'Весьма сомнительно']
    embed = discord.Embed(title=f"{quest}", description=f"{random.choice(responses)}")
    await ctx.send(content=None, embed=embed)


client.run(read_token())
