import asyncio
import time

import cooldowns
import nextcord
from nextcord import SlashOption, Embed, NotFound, File, Interaction, Locale
from nextcord.ext import commands

import config


import aiosqlite
import yaml


class BotInfo(commands.Cog, name="Bot Informations"):
    """Includes all commands about the Bot"""

    COG_EMOJI =config.dc_bots

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
    
    #############################################################################################################

    # Version 6 | Bot Statistics Command
    @nextcord.slash_command(name="bot-statistics",
                            description="Shows you various statistics!",
                            name_localizations={Locale.de: "bot-statistik", Locale.en_US: "bot-statistics"},
                            description_localizations={Locale.de: "Zeigt verschiedene Statistiken zum Bot an!",
                                                       Locale.en_US: "Displays various statistics about the bot!"})        
    @cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.guild)
    async def stats(self, inter: Interaction):

        await inter.response.defer(ephemeral=True)
        servercount = len(inter.client.guilds)
        membercount = len(set(inter.client.get_all_members()))
        channelcount = len(set(inter.client.get_all_channels()))
        
        information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
        information_icon_url = "attachment://information-icon.png"

        info_embed = Embed(title=self.trans["commands"]["stats"]["info_embed"]["title"][inter.locale], 
                           description=self.trans["commands"]["stats"]["info_embed"]["description"][inter.locale].format(servercount=servercount,
                                                                                                                         membercount=membercount,
                                                                                                                         channelcount=channelcount),
                           colour=config.old_blurple)
        
        info_embed.set_thumbnail(url=information_icon_url)

        await inter.edit_original_message(embed=info_embed, file=information_icon_png)
        
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #Version 6 | Ping Command 
    @nextcord.slash_command(name="ping",
                            description="Checks for a response from the bot",
                            description_localizations={Locale.de: "Prüft auf eine Antwort vom Bot", Locale.en_US: "Checks for a response from the bot"})
    
    async def ping(self, interaction: Interaction):
        latency = int(round(interaction.client.latency * 1000))
        p = ""
        c = ""
        
        if latency < 150:
            p = self.trans["commands"]["ping"]["p"]["e"][interaction.locale]
            c = config.green
            
        elif 150 <= latency <= 300:
            p = self.trans["commands"]["ping"]["p"]["g"][interaction.locale]
            c = config.yellow
            
        elif latency > 300:
            p = self.trans["commands"]["ping"]["p"]["u"][interaction.locale]
            c = config.red

        information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
        information_icon_url = "attachment://information-icon.png"

        r = Embed(title=self.trans["commands"]["ping"]["r"]["title"][interaction.locale], description=f"**{p}**:  {latency}ms", colour=c)
        r.set_thumbnail(url=information_icon_url)
        await interaction.response.send_message(embed=r, file=information_icon_png, ephemeral=True)
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------#                           

def setup(bot: commands.Bot):
    bot.add_cog(BotInfo(bot))
