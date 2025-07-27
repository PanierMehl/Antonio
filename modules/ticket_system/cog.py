import nextcord
from nextcord import Embed, File, Interaction, Locale
from nextcord.ext import commands

import config
from mysql_class import BotDB
from modules.ticket_system.view import SetupTicket_en, SetupTicket_de, TicketSystem_Del_de, TicketSystem_Del_en

import yaml


class Ticket_System(commands.Cog, name="Ticket System"):
    """Commands around and for the ticket system"""

    COG_EMOJI = config.a_support
    
    def __init__(self, bot):
        self.bot = bot
        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
        
    @nextcord.slash_command(name="ticket")
    async def ticket(self, inter: Interaction):
        pass

    #Ticket_Setup Command
    @ticket.subcommand(name="setup", description="Create your own personalized ticket system",
                       name_localizations={Locale.de: "konfiguration", Locale.en_US: "setup"},
                       description_localizations={Locale.de: "Erstelle dein eigenes personalisiertes Ticketsystem", Locale.en_US: "Create your own personalized ticket system"})
    async def ticket_setup(self, inter: Interaction):

        
        check = BotDB().query_ticket_system(inter.guild_id)
        
        if check is None:
            if inter.locale == "de":
                await inter.response.send_modal(modal=SetupTicket_de())
            elif inter.locale == "en_US":
                await inter.response.send_modal(modal=SetupTicket_en())
            else:
                await inter.response.send_modal(modal=SetupTicket_en())

        else:
            channel = inter.guild.get_channel(check[3])
            e = Embed(title=self.trans["commands"]["ticket_setup"]["e"]["title"][inter.locale],
                      description=self.trans["commands"]["ticket_setup"]["e"]["description"][inter.locale].format(channel=channel.mention), colour=config.red)
            
            if inter.locale == "de":
                await inter.response.send_message(embed=e, view=TicketSystem_Del_de(inter.guild.id, check[0], check[3]), ephemeral=True)
            elif inter.locale == "en_US":
                await inter.response.send_message(embed=e, view=TicketSystem_Del_en(inter.guild.id, check[0], check[3]), ephemeral=True)
            else:
                await inter.response.send_message(embed=e, view=TicketSystem_Del_en(inter.guild.id, check[0], check[3]), ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Ticket_System(bot))