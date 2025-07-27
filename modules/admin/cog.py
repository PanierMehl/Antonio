import yaml
import asyncio

import nextcord
from nextcord import Embed, Interaction, SlashOption, Locale
from nextcord.ext import commands

from modules.admin.view import giveaway_selected_roles_de, giveaway_selected_roles_en, giveaway_create_de, giveaway_create_en, giveaway_selected_user_de, giveaway_selected_user_en
import config
import perms_check
from mysql_class import BotDB
import json
import random




class Admin(commands.Cog, name="Administrator"):
    """Contains all administrator commandse an"""

    COG_EMOJI = config.dc_owner_badge
    
    def __init__(self, bot):
        self.bot = bot
        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)


########################################################################################################################################
########################################################################################################################################               
########################################################################################################################################

    #DeleteAllInvites-Slash
        #v1 / No Issues
        
    @nextcord.slash_command(name="delete", name_localizations={Locale.de: "entferne", Locale.en_US: "deletw"})
    @perms_check.has_admin_perm_role()
    async def delete(self, inter: Interaction):
        pass
    
    @delete.subcommand(name="perma-invites", description="Removes all invites from your server without an expiry time",
                            name_localizations={Locale.de: "permanente-einladungen", Locale.en_US: "perma-invites"}, 
                            description_localizations={Locale.de: "Entfernt alle permanenten Einladungen", Locale.en_US: "Removes all permanent invites"})
    async def delete_all_invites(self, inter: Interaction):
        
        if inter.user == inter.guild.owner:
            progress = Embed(title=self.trans["commands"]["delete_all_invites"]["progress"]["title"][inter.locale].format(emoji=config.e_loading),
                             description=self.trans["commands"]["delete_all_invites"]["progress"]["title"][inter.locale], colour=config.gold)
            await inter.response.send_message(embed=progress, ephemeral=True)
            deleted_invites = []
        
            for d in await inter.guild.invites():
                if not d.max_age:
                    await d.delete()
                    await asyncio.sleep(1)
                deleted_invites.append(d)
            await inter.edit_original_message(embed=Embed(title=self.trans["commands"]["delete_all_invites"]["d_loop"]["title"][inter.locale].format(invites=len(deleted_invites)), 
                                                                            description='\n'.join([f'{config.a_tic} `{di.code}` by {di.inviter} ({di.uses})' for di in deleted_invites])))

  
    @nextcord.slash_command(name="giveaway", name_localizations={Locale.de: "gewinnspiel", Locale.en_US: "giveaway"})
    async def giveaway(self, inter: Interaction):
        pass
 

    @giveaway.subcommand(name="create", description="Create a giveaway",
                         name_localizations={Locale.de: "erstellen", Locale.en_US: "create"},
                         description_localizations={Locale.de: "Erstelle eine Gewinnspiel", Locale.en_US: "Create a giveaway"})  
    async def giveaway_create(self, inter: Interaction,
                              channel: nextcord.abc.GuildChannel = SlashOption(channel_types=[nextcord.ChannelType.text], description="What channel should the giveaway be in?", required=True,
                                                                               name_localizations={Locale.de: "kanal", Locale.en_US: "channel"},
                                                                               description_localizations={Locale.de:"In welchen Kanal soll die Gewinnspiel statt finden?", Locale.en_US: "What channel should the giveaway be in?"}),
                              entiled: str = SlashOption(name_localizations={Locale.de: "teilnahmevorraussetzung", Locale.en_US: "entiled"},
                                                         description_localizations={Locale.de: "Wer darf an diesem Gewinnspiel teilnehmen?",
                                                                                    Locale.en_US: "Who is allowed to participate in this GiveAWay?"},
                                                         choices=["roles", "user"], choice_localizations={"roles":{Locale.de: "rolle", Locale.en_US: "role"},
                                                                                                          "user": {Locale.de: "mitglied", Locale.en_US: "member"}}, required=False)):
        print("HELLO")
        
        if entiled is None:
            if inter.locale == "de":
                await inter.response.send_modal(modal=giveaway_create_de(channel, None, None))
            elif inter.locale == "en_US":
                await inter.response.send_modal(modal=giveaway_create_en(channel, None, None))
            else:
                await inter.response.send_modal(modal=giveaway_create_en(channel, None, None))
        
        
        elif entiled == "roles":
            await inter.response.defer(ephemeral=True)
            if inter.locale == "de":
                await inter.edit_original_message(view=giveaway_selected_roles_de(channel))
            elif inter.locale == "en_US":
                await inter.edit_original_message(view=giveaway_selected_roles_en(channel))
            else:
                await inter.edit_original_message(view=giveaway_selected_roles_en(channel))
        
        elif entiled == "user":
            await inter.response.defer(ephemeral=True)
            if inter.locale == "de":
                await inter.edit_original_message(view=giveaway_selected_user_de(channel))
        
            elif inter.locale == "en_US":
                await inter.edit_original_message(view=giveaway_selected_user_en(channel))
            
            else:
                await inter.edit_original_message(view=giveaway_selected_user_en(channel))
    

        
    @giveaway.subcommand(name="reroll", description="Reroll a Giveaway with the giveaway id",
                         name_localizations={Locale.de: "neuauslosung", Locale.en_US: "reroll"},
                         description_localizations={Locale.de: "Lose ein Gewinnspiel neu aus!", Locale.en_US: "Reroll a Giveaway with the giveaway id"})
    async def giveaway_reroll(self, inter: Interaction,
                              giveaway_id: str = SlashOption(name="giveaway_id", description="Please enter the giveaway ID here for the giveaway that should be redrawn.",
                                                             description_localizations={Locale.de: "Gebe die Gewinnspiel ID hier an, vom Giveaway, welches neu ausgelost werden soll.",
                                                                                 Locale.en_US: "Please enter the giveaway ID here for the giveaway that should be redrawn."})):
        query = BotDB().query_giveaway_data(giveaway_id)
        if query is None:
            return
        else:
            channel = inter.guild.get_channel(query[2])
            message = await channel.fetch_message(query[0])
            
            server_query = BotDB().query_server_table(inter.guild.id)
            
            participants_data = query[1]
            winners_tuple = BotDB().determine_winners(giveaway_id)
            winners_str = winners_tuple[0]
            num_winners = winners_tuple[1]

            participants_str = participants_data

            if participants_str is None:
                    participants = []
            else:
                try:
                    participants = json.loads(participants_str)
                except json.JSONDecodeError:
                    participants = []
                        
                        
            winners_list = winners_str.strip("[]").split(", ")
            selected_winners = random.sample(winners_list, min(num_winners, len(winners_list)))


            winner_mentions = ', '.join(f"<@{winner_id.strip()}>" for winner_id in selected_winners)
            
                                
            if server_query[5] == "Engish":
                embed = nextcord.Embed(title="🎉 Giveaway ended 🎉", description="The giveaway has ended, no further participation is possible!", colour=config.red)
                embed.add_field(name="Winners", value=f"{winner_mentions}\n\uFEFF")
                embed.add_field(name="Prize", value=f"{query[3]}\n\uFEFF")
                embed.add_field(name="Entries", value=f"{len(participants)}\n\uFEFF")
                embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
                await message.edit(embed=embed, view=None)
                
                await inter.response.send_message(content=f"{winner_mentions} was drawn as the new winner for the prize `{query[3]}` from giveaway `{giveaway_id}`. Congratulations.")
                
            elif server_query[5] == "German":
                embed = nextcord.Embed(title="🎉 Gewinnspiel beendet 🎉", description="Das Gewinnspiel ist beendet, eine weitere Teilnahme ist nicht möglich!", colour=config.red)
                embed.add_field(name="Gewinner", value=f"{winner_mentions}\n\uFEFF")
                embed.add_field(name="Preis", value=f"{query[3]}\n\uFEFF")
                embed.add_field(name="Teilnehmer", value=f"{len(participants)}\n\uFEFF")
                embed.set_footer(text=f"Gewinnspiel ID: {giveaway_id}")
                await message.edit(embed=embed, view=None)
                
                await inter.response.send_message(content=f"{winner_mentions} wurde zum neuen Gewinner ausgelost für den Gewinn von `{query[3]}` aus dem Gewinnspiel `{giveaway_id}`. Glückwunsch.")
                
            else:
                embed = nextcord.Embed(title="🎉 Giveaway ended 🎉", description="The giveaway has ended, no further participation is possible!", colour=config.red)
                embed.add_field(name="Winners", value=f"{winner_mentions}\n\uFEFF")
                embed.add_field(name="Prize", value=f"{query[3]}\n\uFEFF")
                embed.add_field(name="Entries", value=f"{len(participants)}\n\uFEFF")
                embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
                await message.edit(embed=embed, view=None)
                await inter.response.send_message(content=f"{winner_mentions} was drawn as the new winnerway. Congratulations.")
            


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))