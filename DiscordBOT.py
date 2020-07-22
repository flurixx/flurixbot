import discord
from discord.ext import commands
import json
import requests
import os
from Cybernator import Paginator as pag
from discord.utils import get
import random
import time
import asyncio
from discord.ext.commands import has_permissions

settings = {
    'bot': 'flurixX',
    'prefix': '!'
}

bot = commands.Bot(command_prefix = settings['prefix'])
bot.remove_command('help')

@bot.command()
@has_permissions(manage_roles=True)
async def start(ctx,name="muted"):
		guild = ctx.guild
		for role in guild.roles:
			if name.lower() in role.name.lower():
				await ctx.send(embed = discord.Embed(description = 'Бот уже настроен!', color = 0x49FF33))
				return role
			else:
				perms = discord.Permissions(send_messages=False)
				await guild.create_role(name="muted", permissions=perms)
				await ctx.send(embed = discord.Embed(description = '''Первоначальная настройка бота завершена!
Удачного пользования :)''', color = 0x49FF33))
				return None

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" !info"))
    print('DiscordBOT stable v1 by flurix запущен')
    print('Ссылка-приглашение для бота: https://discord.com/api/oauth2/authorize?client_id=734071346312773723&permissions=8&scope=bot')
	
@bot.command()
async def game(ctx):
	game_random = random.randint(1, 101)
	await ctx.send(embed = discord.Embed(description = 'Бросаю монетку...', color = 0x49FF33))
	time.sleep(1)
	if game_random <= 50:
		await ctx.send(embed = discord.Embed(description = ':full_moon: Выпала решка!', color = 0x49FF33))
	elif game_random >= 51 and game_random <= 100:
		await ctx.send(embed = discord.Embed(description = ':new_moon: Выпал орёл!', color = 0x49FF33))
	else:
		await ctx.send(embed = discord.Embed(description = ':first_quarter_moon: Монета встала ребром! Шанс этого всего 1%!', color = 0x49FF33))
				
@bot.command(aliases = ['помощь','помоги','команды'])
async def info(ctx):
	embed1 = discord.Embed(title = 'Обо мне', description = '''Привет!
Я - бот FlurixX.
На данный момент я нахожусь в активной разработке
Чтобы бот работал правильно - введите команду !start''', color = 0xFF8C00)
	embed2 = discord.Embed(title = 'Команды', description = '''Список доступных комманд:
!start - первоначальная настройка бота на сервере(вводить единожды)
!info - информация, которую вы сейчас видите
!game - игра "Орёл или Решка". Только рандом!
!clear - очистка чата(требуется разрешение "Упрвлять сообщениями")
!kick - кик пользователя с сервера(требуется разрешение "Исключение пользователей")
!ban и !unban - бан и соответственно разбан пользователя на сервере(требуется разрешение "Банить пользователей")
!tempban - временный бан пользователя на сервере(требуется разрешение "Банить пользователей")
!tempmute - временная блокировка чата пользователю(требуется разрешение "Управление ролями")
!mute - блокировка чата пользователю(требуется разрешение "Управление ролями")''', color = 0xFF8C00)
	embed3 = discord.Embed(title = 'План разработки', description = '''В скором времени будут доступны и другие комманды.
Например, скоро разработчик планирует добавить систему валюты, уровней и другие плюшки...''', color = 0xFF8C00)
	embeds = [embed1, embed2, embed3]
	message = await ctx.send(embed = embed1)
	page = pag(bot, message, only=ctx.author, use_more=False, embeds=embeds)
	await page.start()

#Очистка чата
@bot.command( pass_context = True )
@has_permissions(manage_messages=True)
async def clear( ctx, amount = 10000):
	await ctx.channel.purge( limit = amount )
	await ctx.send(embed = discord.Embed(description = f"""Привет! Если ты видишь это сообщение то чат был очищен.
Список команд - !info""",color=0x008080))

@clear.error
async def clear_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Кик пользователя
@bot.command( pass_context = True )
@has_permissions(kick_members=True)
async def kick( ctx, member: discord.Member, *, reason = 'Вы были кикнуты с сервера' ):
	await ctx.channel.purge( limit = 1)
	await member.kick(reason = reason)
	await ctx.send(embed = discord.Embed(description = f'{member.name}, был исключён с сервера.',color=0xFF0000))

@kick.error
async def kick_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		channel = bot.get_channel( 734072439620763733 )
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Tempban(бан на время)
@bot.command()
@has_permissions(ban_members=True)
async def tempban(ctx, member:discord.User, duration: int):
	await ctx.guild.ban(member)
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был забанен на сервере на {duration} секунд.',color=0xFF0000))
	await asyncio.sleep(duration)
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был разбанен на сервере спустя {duration} секунд.',color=0xFF0000))
	await ctx.guild.unban(member)
	
#Ошибка tempban	
@tempban.error
async def tempban_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Tempmute(мут на время)
@bot.command()
@has_permissions(manage_roles=True)
async def tempmute(ctx, member:discord.Member, duration: int):
	role = discord.utils.get(ctx.guild.roles, name="muted")
	await member.add_roles(role)
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был замьючен на сервере на {duration} секунд.',color=0xFF0000))
	await asyncio.sleep(duration)
	await member.remove_roles(role)	
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был размьючен на сервере спустя {duration} секунд.',color=0xFF0000))

#Ошибка tempmute	
@tempmute.error
async def tempmute_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))
		
#Убираем мут у пользователя
@bot.command()
@has_permissions(manage_roles=True)
async def unmute(ctx, member:discord.Member):
	role = discord.utils.get(ctx.guild.roles, name="muted")
	await member.remove_roles(role)
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был размьючен!',color=0x49FF33))
	
@unmute.error
async def unmute_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Бан пользователя
@bot.command()
@has_permissions(ban_members=True)
async def ban( ctx, member: discord.Member, *, reason = 'Вы были забанены на сервере' ):
	await ctx.channel.purge( limit = 1)
	await member.ban(reason = reason)
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был забанен на сервере.',color=0xFF0000))
	
@ban.error
async def ban_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Разбан пользователя
@bot.command()
@has_permissions(ban_members=True)
async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1)
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		await ctx.guild.unban(user)
		await ctx.send(f'Пользователь {user.mention} был разблокирован на сервере.')
		return

@unban.error
async def unban_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент без @',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))
		
#Роль для авто-выдачи
@bot.command()
@has_permissions(manage_roles=True)
async def autorole(ctx,autoroles:int):
	global autoroles
	await ctx.send ( embed = discord.Embed(description = f'Роль успешно добавлена в авто-выдачу!', color = 0x49FF33))
	
@autorole.error
async def autorole_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите id роли!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))


#Авто-выдача роли при заходе на сервер
@bot.event
async def on_member_join( member ):
	await ctx.send ( embed = discord.Embed(description = f'Привет, ``{member.name}``, добро пожаловать на сервер! Информация - !info', color = 0x49FF33))
	role = discord.utils.get( member.guild.roles, id = autoroles )
	await member.add_roles( role )

#Мут пользователя
@bot.command()
@has_permissions(manage_roles=True)
async def mute( ctx, member: discord.Member ):
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTED' )
	await member.add_roles( mute_role )
	await ctx.send(embed = discord.Embed(description = f'Пользователь {member.name} был замьючен на сервере',color=0xFF0000))

@mute.error
async def mute_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

cool_words = ['бот крутой', 'бот лучший','бот топ','бот классный','бот прикольный', 'топ бот', 'крутой бот', 'классный бот','лучший бот','прикольный бот']		
@bot.event
async def on_message(message):
	await bot.process_commands( message )
	msg = message.content.lower()
	if msg in cool_words:
		await ctx.send(embed = discord.Embed(description = f'{message.author}, cпасибо :) Ты тоже крут!',color=0xFF1493)) 

token = os.environ.get('BOT_TOKEN')
bot.run(token)
