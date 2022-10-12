import discord
from discord.ext import commands , menus , tasks
import random
from datetime import timezone, datetime
from typing import List
import asyncio
from itertools import cycle
import os 



TOKEN = ''




bot = commands.Bot(command_prefix='!!', intents=discord.Intents.all() , help_command=None)


########################################################################################################

status = cycle(['!!help', 'Youtube', 'Pornhub'])        

@tasks.loop(seconds=6)
async def changeStatus():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))


########################################################################################################

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print("we have logged in")
    print("-------------------------------------")
    changeStatus.start()


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}') 


async def on_message(self, message):
    await bot.process_commands(message)
    if message.author.id == self.user.id: #Ko cho bot tự trả lời chính mình
        return

    if message[0] == '!!':
        return

########################################################################################################

def it_is_me(ctx):
    return ctx.author.id == 874321270437728257 , 862692874348003338


@bot.command(name='test', help='test bot')
async def test(ctx):
    await ctx.send(f"done! {ctx.author.name}")



#@bot.command(name='ping', help='Xem độ phản hồi của bot')
#async def ping(ctx):
#    ping = discord.Embed(title = f"Pong! Your latency is {round(bot.latency*1000)}ms", color = discord.Colour.purple(), timestamp = datetime.now(timezone.utc))
#    ping.set_author(name = f'{ctx.author.name}')
#    ping.set_footer(text = 'Thank you so much')
#    msg = await ctx.send(embed = ping )



@bot.command(name='add', help='Cộng 2 số lại vs nhau')
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def joined(ctx, member: discord.Member):
        joined_at = member.joined_at.strftime("%b %d, %Y, %T")
        jnd = discord.Embed(title = f'{member} đã tham gia vào {joined_at}'.format(member), color = discord.Colour.purple())
        await ctx.send(embed = jnd)



@bot.command(aliases=['lot'], name='lottery', help='Đoán số')
async def lottery(ctx):
    await ctx.send(f'Hi {ctx.author.mention}, choose your number 1-20!')
    x = random.randint(1,20)
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    msg = await bot.wait_for("message", check=check)
    if int(msg.content) == x:
        await ctx.send(f'Congratulations {ctx.author.mention}, you won!!')
    else:
        await ctx.send(f'Nope {ctx.author.mention} :( , is was {x}')

@bot.command(name='serverinfo', help='Show thông tin của server discord này')
async def serverinfo(ctx): 
    if ctx.guild.owner is not None:
        name = ctx.guild.name
        description = ctx.guild.description
        owner = ctx.guild.owner
        id = ctx.guild.id
        Secure = str(ctx.guild.verification_level)
        high_role = ctx.guild.roles[-2]
        memberCount = ctx.guild.member_count
        icon = ctx.guild.icon
        create = ctx.guild.created_at
        embed = discord.Embed(
            title = '🔎 Server infomations! 🔎 ' + name,
            description=description,
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="👑 Owner by", value=owner.name, inline=True)
        embed.add_field(name='💬 Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline=True)
        embed.add_field(name="👥 Members", value=memberCount, inline=True)
        embed.add_field(name="🛡️ Verification level", value=Secure, inline=True)
        embed.add_field(name="📊 Highest role", value=high_role, inline=True)
        embed.add_field(name="📅 Created on", value=create, inline=False)
        embed.add_field(name="🆔 Server ID", value=id, inline=False)
        embed.set_footer(text="⭐ • Created by Cá")
        await ctx.send(embed=embed)

@commands.check(it_is_me)
@bot.command(name='clear', help='Xóa tin nhắn vs x lần')
async def clear(ctx, amount = 1000):
    await ctx.channel.purge(limit = amount)

@commands.check(it_is_me)
@bot.command(name='delallchannel', help='xóa tất cả các kênh văn bản')
async def delallchannels(ctx):
    for c in ctx.guild.channels: 
        await c.delete()

@commands.check(it_is_me)
@bot.command(aliases=['delc'], name='delchannel', help='Xóa kênh')
@commands.guild_only()
async def deletechannel(ctx, channels: commands.Greedy[discord.TextChannel] = None):
    if not channels:
        return await ctx.reply("//delc + tên kênh muốn xóa hoặc id kênh")
    
    for channel in channels:
        await channel.delete()

@commands.check(it_is_me)
@bot.command(aliases=['delvc'], name='delchannelvoice', help='Xóa voice')
async def delchannelvoice(ctx, channel: discord.VoiceChannel):
    await channel.delete()

@commands.check(it_is_me)
@bot.command(name='spam', help='Spam tin nhắn vs x lần')
async def spam(ctx, amount:int, *, message):
    for i in range(amount): 
        await ctx.send(message) 


@bot.command(name='createchannel', help='tạo kênh văn bản với x lần')
async def createchannel(ctx, amount:int ,*,  channel_name):
    guild = ctx.guild
    for i in range(amount):
         await guild.create_text_channel(channel_name)
    
@commands.check(it_is_me)
@bot.command(name='kick', help='kick 1 người')
async def kick(ctx, member : commands.MemberConverter, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f"{member} cút mịa m đi, lý do nè e: {reason}")

@commands.check(it_is_me)
@bot.command(name='createvoicechannel', help='tạo voice')
async def createvoicechannel(ctx, channel_name):
	guild = ctx.guild
	await guild.create_voice_channel(channel_name)

@commands.check(it_is_me)
@bot.command(name='delrole', help='xóa role vĩnh viễn')
async def delrole(ctx, *, role_name):
  role = discord.utils.get(ctx.message.guild.roles, name=role_name)
  if role:
    try:
      await role.delete()
      await ctx.send("Role {} đã đc xóa!".format(role.name))
    except discord.Forbidden:
      await ctx.send("Ko có quyền để xóa role")
  else:
    await ctx.send("Ko tồn tại role này!")

@commands.check(it_is_me)
@bot.command(name='makerole', help='tạo role')
async def makerole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` đã đc tạo')    

@commands.check(it_is_me)
@bot.command(pass_context=True, name='addrole', help='gắn role cho 1 người')
async def addrole(ctx, user: discord.Member, role: discord.Role):
    if not role :
         await ctx.send("Không có role này!")
    else:
        await user.add_roles(role)
        await ctx.send(f"{user.name} đã được gắn role : {role.name}")

@commands.check(it_is_me)
@bot.command(pass_context=True, name='removerole', help='gỡ role cho 1 người')
async def removerole(ctx, user: discord.Member, role: discord.Role):
    role = discord.Role
    if not role :
        return await ctx.send("Không có role này!")
    else:
        await user.remove_roles(role)
        await ctx.send(f"{user.name} đã được gỡ role : {role.name}")



#################################################################################

class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f'Hello {ctx.author.name}, bạn thấy bot như thế nào')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author.name}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"Hãy giúp tôi hoàn thiện hơn {self.ctx.author.name}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()

@bot.command()
async def vote(ctx):
    m = MyMenu()
    await m.start(ctx)

#################################################################################

class Confirm(menus.Menu):
    def __init__(self, msg):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.msg = msg
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.msg)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, payload):
        self.result = True
        self.stop()

    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result

@bot.command()
async def delete_things(ctx):
    confirm = await Confirm('Xóa hết ?').prompt(ctx)
    if confirm:
        await ctx.send('Đã xóa...')

####################################################################################




async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
