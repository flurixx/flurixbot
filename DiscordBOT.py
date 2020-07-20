import discord
from discord.ext import commands
import json
import requests
import os
from Cybernator import Paginator as pag
from discord.utils import get
import youtube_dl

settings = {
    'bot': 'flurix[BOT]',
    'prefix': '!'
}

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" !info"))

@bot.command()
async def play(ctx, url: str):
	global voice
	voice = get(client.voice_clients, guild = ctx.guild)
	channel = ctx.message.author.voice.channel
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect
	song_there=os.path.isfile('song.mp3')
	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Старый файл удалён.')
	except PermissionError:
		print('[log] Не удалось удалить файл')
	await ctx.send('Идёт загрузка аудиофайла, ожидайте...')

	voice = get(client.voice_clients, guild = ctx.guild)
	ydl_opts = {
		'format' : 'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('[log] Загружаю музыку...')
		ydl.download([url])

	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print(f'[log] Переименовываю файл {file}')
			os.rename(file, 'song.mp3')

	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила проигрывание...'))
	voice.source = discord.PCMVolumeTransformer('voice.source')
	voice.source.volume = 0.07

	songname = name.rsplit('-', 2)
	await ctx.send(f'Сейчас играет: {song_name[0]}')

@bot.command()
async def leave(ctx):
	voice = get(client.voice_clients, guild = ctx.guild)
	channel = ctx.message.author.voice.channel
	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')
	
@bot.command(aliases = ['помощь','помоги','команды'])
async def info(ctx):
	embed1 = discord.Embed(title = 'Обо мне', description = '''Привет!
Я - discordBOT by flurix v0.5.
На данный момент я нахожусь в активной разработке''', color = 0xFF8C00)
	embed2 = discord.Embed(title = 'Команды', description = '''Список доступных комманд:
!info - информация, которую вы сейчас видите
!hello - поздороваться с ботом
!clear - очистка чата(Доступно только роли Админ)
!kick - кик пользователя с сервера(Доступно только роли Админ)
!ban и !unban - бан и соответственно разбан пользователя на сервере(Доступно только роли Админ)
!mute - блокировка чата пользователю(Доступно только роли Админ)''', color = 0xFF8C00)
	embed3 = discord.Embed(title = 'План разработки', description = '''В скором времени будут доступны и другие комманды.
Например, скоро разработчик планирует добавить функцию воспроизведения музыки,
Систему валюты на сервере...''', color = 0xFF8C00)
	embeds = [embed1, embed2, embed3]
	message = await ctx.send(embed = embed1)
	page = pag(bot, message, only=ctx.author, use_more=False, embeds=embeds)
	await page.start()

#Очистка чата
@bot.command( pass_context = True )
@commands.has_role('Админ')
async def clear( ctx, amount = 10000):
	channel = bot.get_channel( 734072439620763733 )
	await ctx.channel.purge( limit = amount )
	await channel.send(embed = discord.Embed(description = f"""Привет! Если ты видишь это сообщение то чат был очищен.
Список команд - !info""",color=0x008080))

@clear.error
async def clear_error(ctx,error):
	channel = bot.get_channel( 734072439620763733 )
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		await channel.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		await channel.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Кик пользователя
@bot.command( pass_context = True )
@commands.has_role('Админ')
async def kick( ctx, member: discord.Member, *, reason = 'Вы были кикнуты с сервера' ):
	channel = bot.get_channel( 734072439620763733 )
	await ctx.channel.purge( limit = 1)
	await member.kick(reason = reason)
	await channel.send(embed = discord.Embed(description = f'{member.name}, был исключён с сервера.',color=0xFF0000))

@kick.error
async def kick_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingRole):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Бан пользователя
@bot.command( pass_context = True )
@commands.has_role('Админ')
async def ban( ctx, member: discord.Member, *, reason = 'Вы были забанены на сервере' ):
	await ctx.channel.purge( limit = 1)
	await member.ban(reason = reason)
	await ctx.send(f'Пользователь {member.name} был забанен на сервере.')
	
@ban.error
async def ban_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingRole):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

#Разбан пользователя
@bot.command( pass_context = True )
@commands.has_role('Админ')
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
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент без @',color=0xFF0000))
	if isinstance(error, commands.MissingRole):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))


#Авто-выдача роли Участник при заходе на сервер
@bot.event
async def on_member_join( member ):
	channel = bot.get_channel( 734072439620763733 )
	role = discord.utils.get( member.guild.roles, id = 734137828652482570 )
	await member.add_roles( role )
	await channel.send ( embed = discord.Embed(description = f'Привет, ``{member.name}``, добро пожаловать на сервер! Информация - !info', color = 0x49FF33))

#Мут пользователя
@bot.command( pass_context = True )
@commands.has_role( 'Админ' )
async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTED' )
	await member.add_roles( mute_role )
	await ctx.send(f'Пользователь {member.name}, был замьючен на сервере.' )

@mute.error
async def mute_error(ctx,error):
	author = ctx.message.author
	if isinstance (error, commands.MissingRequiredArgument):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, укажите аргумент!',color=0xFF0000))
	if isinstance(error, commands.MissingPermissions):
		channel = bot.get_channel( 734072439620763733 )
		await channel.send(embed = discord.Embed(description = f'{author.mention}, вы не обладаете такими правами!',color=0xFF0000))

bad_words = ['сука','блять','пидорас','еблан','хуесос','хуй','пизда','ебал','хуйня','чмо']
@bot.event
async def on_message(message):
	channel = bot.get_channel( 734072439620763733 )
	await bot.process_commands( message )
	msg = message.content.lower()
	if msg in bad_words:
		await message.delete()
		await channel.send(embed = discord.Embed(description = f'{message.author}, прошу не материться на сервере.',color=0xFF0000)) 

cool_words = ['бот крутой', 'бот лучший','бот топ','бот классный','бот прикольный']		
@bot.event
async def on_message(message):
	channel = bot.get_channel( 734072439620763733 )
	await bot.process_commands( message )
	msg = message.content.lower()
	if msg in cool_words:
		await channel.send(embed = discord.Embed(description = f'{message.author}, cпасибо :) Ты тоже крут!',color=0xFF1493)) 


print('DiscordBOT v0.4 by flurix запущен')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
