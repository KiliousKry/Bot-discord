from tkinter.tix import Tree
import discord
from discord.ext import commands 
from discord import app_commands
from datetime import datetime, timezone




class SlashCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded SlashCommands Cog!')


    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)

        await ctx.send(f'sync {len(fmt)} commands')


    @app_commands.command(name = 'test', description='test bot')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Successfully!')

    
    


async def setup(bot):
    await bot.add_cog(SlashCommands(bot), guilds = [discord.Object(id=995149354635628555)])
