import discord
from discord.ext import commands
import json
import requests
import os

settings = {
    'bot': 'flurix[BOT]',
    'prefix': '!'
}

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" !info"))

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

#Информация
@bot.command()
async def info(ctx):
    channel = bot.get_channel( 734072439620763733 )
    author = ctx.message.author
    await channel.send ( embed = discord.Embed(description = f"""Привет, {author.mention}! 
Я - discordBOT by flurix v0.4.
На данный момент я нахожусь в разработке, поэтому доступен только некоторый перечень команд:
!info - информация, которую вы сейчас видите
!hello - поздороваться с ботом
!clear - очистка чата(Доступно только роли Кодер)
!kick - кик пользователя с сервера(Доступно только роли Админ)
!ban и !unban - бан и соответственно разбан пользователя на сервере(Доступно только роли Админ)
!mute - блокировка чата пользователю(Доступно только роли Админ)
В дальнейшем бот будет улучшаться, и будут новые команды"""
, color = 0xFFD700))

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


print('DiscordBOT v0.4 by flurix запущен')

token = os.environ.get('BOT_TOKEN')
bot.run(token)
