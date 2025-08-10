
from datetime import datetime

import cooldowns
import nextcord as nc
import pytz as pytz
from nextcord import SlashOption, Embed, Interaction, Locale
from nextcord.ext import commands

import config
from modules.member_information.views import mi_home

import yaml


class Member_Information(commands.Cog, name="Member Informations"):
    """Displays all Member Informations commands"""

    COG_EMOJI = config.e_information

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)       



    # Version 6 | Member Information Command
    @nc.slash_command(name="memberinfo",
                      description="Shows all about a user",
                      name_localizations={Locale.de: "mitgliederinformation", Locale.en_US: "memberinfo"},
                      description_localizations={Locale.de: "Zeigt alles über einen Benutzer an", Locale.en_US: "Shows all about a user"})        
    @cooldowns.cooldown(1, 25, bucket=cooldowns.SlashBucket.guild)
    async def memberinfo(self, inter: Interaction,
                       _member: nc.Member = SlashOption(name="member", description="Please select a member", required=False,
                                                        name_localizations={Locale.en_US: "member", Locale.de: "mitglied"},
                                                        description_localizations={Locale.en_US: "Please select a member",
                                                                                   Locale.de: "Bitte wähle ein Mitglied"}),
                       show_message: bool = SlashOption(name="message_visibility",
                                                        description="Would you like to make the message only visible to you?",
                                                        required=False,
                                                        name_localizations={Locale.en_US: "message_visibility",
                                                                            Locale.de: "nachrichtensichtbarkeit"},
                                                        description_localizations={
                                                            Locale.en_US: "Would you like to make the message only visible to you?",
                                                            Locale.de: "Möchtest du, dass die Nachricht nur für dich sichtbar ist?"})):
        
        member = _member or inter.user

        de = pytz.timezone('Europe/Berlin')
        
        e_memberinfo = Embed(title=self.trans["commands"]["memberinfo"]["memberinfo"]["title"][inter.locale].format(emoji_a=config.e_information, emoji_b=config.dc_members, member=member.display_name),
                            description='', colour=nc.Colour.random(), timestamp=datetime.now().astimezone(tz=de))

        await inter.response.defer(ephemeral=show_message if show_message else True)
        if inter.guild.get_member(member.id) != None: 

            def activity_s():
                
                try:
                    if member.activity.type == nc.ActivityType.playing:
                        return self.trans["commands"]["memberinfo"]["activity_s"]["playing"][inter.locale].format(status=member.activity.name)
                    
                    elif member.activity.type == nc.ActivityType.streaming:
                        return self.trans["commands"]["memberinfo"]["activity_s"]["streaming"][inter.locale].format(status=member.activity.name, button=member.activity.buttons)
                    
                    elif member.activity.type == nc.ActivityType.custom:
                        return self.trans["commands"]["memberinfo"]["activity_s"]["custom"][inter.locale].format(status=member.activity.name)
                    
                    elif member.activity is None:
                        return self.trans["commands"]["memberinfo"]["activity_s"]["no_activity"][inter.locale]
                    
                    else:
                        return self.trans["commands"]["memberinfo"]["activity_s"]["no_activity"][inter.locale]
                    
                except:
                    return self.trans["commands"]["memberinfo"]["activity_s"]["no_activity"][inter.locale]
                
                
            e_memberinfo.add_field(name=self.trans["commands"]["memberinfo"]["memberinfo"]["field_a"]["name"][inter.locale], 
                                value=self.trans["commands"]["memberinfo"]["memberinfo"]["field_a"]["value"][inter.locale].format(member=member, member_id=member.id, created={str(member.created_at)[:19]}, activity=activity_s(), emoji=config.a_tic if member.bot else config.a_cross))
            
            e_memberinfo.add_field(name=self.trans["commands"]["memberinfo"]["memberinfo"]["field_b"]["name"][inter.locale],
                                 value=self.trans["commands"]["memberinfo"]["memberinfo"]["field_b"]["value"][inter.locale].format(nick=member.nick if member.nick else '-----', joined_at=str(member.joined_at)[:19], premium_since=config.a_tic if member.premium_since else config.a_cross))
            
            input_member = member
            view_r = mi_home(inter, input_member)
            await inter.edit_original_message(embed=e_memberinfo, view=view_r)
            view_r.message = await inter.original_message()
            
            
        elif inter.guild.get_member(member.id) == None: 
            await inter.response.defer(ephemeral=bool(show_message) if show_message is not None else True)

            e_memberinfo.add_field(name=self.trans["commands"]["memberinfo"]["memberinfo"]["field_c"]["name"][inter.locale], 
                                value=self.trans["commands"]["memberinfo"]["memberinfo"]["field_c"]["value"][inter.locale].format(member=member, member_id=member.id, created_at=str(member.created_at)[:19], bot=config.a_tic if member.bot else config.a_cross))
        
            
            await inter.edit_original_message(embed=e_memberinfo)   
            
            
        
                 
def setup(bot: commands.Bot):
    bot.add_cog(Member_Information(bot))