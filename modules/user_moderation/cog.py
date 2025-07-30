import random
import re
import string
import yaml

import nextcord as nc
from nextcord import Embed, Interaction, SlashOption, Locale
from nextcord.ext import commands

import config
import perms_check
from modules.user_moderation.view import (MT, CaseInfoDropdown,
                                          DeleteCaseDropdown, EditCaseDropdown,
                                          NewWarnModal)
from mysql_asyncmy import A_DB

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)


def generate_random_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

########################################################################################################################################
########################################################################################################################################
        
        
class Member_Moderation(commands.Cog, name="Member Moderation"):
    """Contains all Member Moderation commands"""

    COG_EMOJI = config.dc_moderators
    
    def __init__(self, bot):
        self.bot = bot
        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
#############################################################################################################
#############################################################################################################

    @nc.slash_command(name="member")
    async def member(self, inter: Interaction):
        pass

    #Kick_Command (V 4.0)
    @member.subcommand(name="kick", description="Remove a member from your server",
                       description_localizations={Locale.de:"Entferne einen Member von deinem Server", Locale.en_US: "Remove a member from your server"}) 
    @perms_check.has_min_moderator_perm_role()
    async def member_kick(self, interaction: Interaction,
                    member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                    description_localizations={Locale.de: "Bitte wähle ein Mitglied", Locale.en_US: "Please select a member"}),
                    reason: str = SlashOption(name="reason", description="Please enter a reason", required=True,
                                              name_localizations={Locale.de: "grund", Locale.en_US: "reason"},
                                              description_localizations={Locale.en_US: "Please enter a reason", Locale.de: "Bitte gib einen Grund an"})):
        
        
        if member.id == interaction.user.id:
            notyourself = Embed(description=self.trans["commands"]["member_kick"]["notyourself"]["description"][interaction.locale].format(emoji=config.a_cross), colour=config.dark_red)
            await interaction.response.send_message(embed=notyourself, ephemeral=True)
            return
                
        wait = Embed(description=self.trans["commands"]["member_kick"]["wait"]["description"][interaction.locale], colour=config.red)
        

        
        invitecreate = await interaction.channel.create_invite(reason="Kick-Invite", max_age=432000, max_uses=1, unique=True)

        kickdm = Embed(title=self.trans["commands"]["member_kick"]["kickdm"]["title"][interaction.locale].format(emoji=config.DiscordBan, guild=interaction.guild.name),
                        description=self.trans["commands"]["member_kick"]["kickdm"]["description"][interaction.locale], colour=config.red)
        kickdm.set_author(name=interaction.guild.name)
        kickdm.add_field(name=self.trans["commands"]["member_kick"]["kickdm"]["field_a"]["name"][interaction.locale], value=config.aktuelldatum, inline=True)
        kickdm.add_field(name=self.trans["commands"]["member_kick"]["kickdm"]["field_b"]["name"][interaction.locale], value=f"`{reason}`")
        kickdm.add_field(name=self.trans["commands"]["member_kick"]["kickdm"]["field_c"]["name"][interaction.locale], value=invitecreate, inline=False)
        kickdm.add_field(name=self.trans["commands"]["member_kick"]["kickdm"]["field_d"]["name"][interaction.locale],
                         value=self.trans["commands"]["member_kick"]["kickdm"]["field_d"]["value"][interaction.locale])
        kickdm.set_footer(text=f"Moderator {interaction.user.name} ➟ {interaction.user.id}", icon_url=interaction.user.avatar.url)
        
        kickctx = Embed(title=self.trans["commands"]["member_kick"]["kickctx"]["title"][interaction.locale],
                        description=self.trans["commands"]["member_kick"]["kickctx"]["description"][interaction.locale].format(emoji_a=config.a_tic, emoji_b=config.dc_members, member=member.mention), colour=config.blurple)
        
        await interaction.response.send_message(embed=wait, ephemeral=True)

        try:
            await member.send(embed=kickdm)
            await member.kick(reason=f"{reason} - Member was notified about his ban!")
            await interaction.edit_original_message(embed=kickctx)
            
        except nc.Forbidden:
            await member.kick(reason=f"{reason} - Member was not notified about his ban!")
            await interaction.edit_original_message(embed=kickctx)
            

 
##########################################################################################################################################################

    #Ban_Command (V 4.0)
    @member.subcommand(name="ban", description="Ban a member from your guild", description_localizations={Locale.en_US: "Ban a member from your guild", Locale.de: "Verbanne ein Mitglied aus deinem Server"})    
    @perms_check.has_admin_perm_role()
    async def member_ban(self,
                  interaction: Interaction,
                    member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                    description_localizations={Locale.de: "Bitte wähle ein Mitglied", Locale.en_US: "Please select a member"}),
                    reason: str = SlashOption(name="reason", description="Please enter a reason", required=True,
                                              name_localizations={Locale.de: "grund", Locale.en_US: "reason"},
                                              description_localizations={Locale.en_US: "Please enter a reason", Locale.de: "Bitte gib einen Grund an"})):
         
        if member.id == interaction.user.id:
            notyourself = Embed(description=f"{config.a_cross} You can't ban yourself!", colour=config.dark_red)
            await interaction.response.send_message(embed=notyourself, ephemeral=True)
            return
            
        wait = Embed(description=f"Please wait a moment. I prepare everything!", colour=config.red)
        
        
        bandm = Embed(title=self.trans["commands"]["member_ban"]["bandm"]["title"][interaction.locale].format(emoji=config.DiscordBan, guild=interaction.guild.name),
                                description=self.trans["commands"]["member_ban"]["bandm"]["description"][interaction.locale], colour=config.yellow)
        bandm.set_author(name=interaction.guild.name)
        bandm.add_field(name=self.trans["commands"]["member_ban"]["bandm"]["field_a"]["name"][interaction.locale], value=config.aktuelldatum, inline=True)
        bandm.add_field(name=self.trans["commands"]["member_ban"]["bandm"]["field_b"]["name"][interaction.locale], value=reason)
        bandm.set_footer(text=f"Moderator {interaction.user.name} ➟ {interaction.user.id}", icon_url=interaction.user.avatar.url)

        banctx_nt = Embed(description=self.trans["commands"]["member_ban"]["banctx_nt"]["description"][interaction.locale].format(emoji_a=config.DiscordBan, emoji_b=config.dc_members, member=member.mention, emoji_c=config.a_tic), colour=config.blurple)
        banctx_nf = Embed(description=self.trans["commands"]["member_ban"]["banctx_nf"]["description"][interaction.locale].format(emoji_a=config.DiscordBan, emoji_b=config.dc_members, member=member.mention, emoji_c=config.a_cross), colour=config.blurple)


        await interaction.response.send_message(embed=wait, ephemeral=True)   

        try:
            await member.send(embed=bandm)
            await member.ban(reason=f"{reason} - Member was notified about his ban!", delete_message_seconds=604800)
            await interaction.edit_original_message(embed=banctx_nt)
            
        except nc.Forbidden:
            await member.ban(reason=f"{reason} - Member was not notified about his ban!", delete_message_seconds=604800)
            await interaction.edit_original_message(embed=banctx_nf)
                
##########################################################################################################################################################
  
    #Unban Command (V 4.0)
    @member.subcommand(name="unban", description="Unban a banned member", description_localizations={Locale.en_US: "Unban a banned member", Locale.de: "Ein verbanntes Mitglied wieder freigeben"})   
    @perms_check.has_min_moderator_perm_role() 
    async def member_unban(self, interaction: Interaction,
                    member: nc.Member = SlashOption(name="member", description="Please enter ID of the target member", required=True, 
                                                    description_localizations={Locale.en_US: "Please enter ID of the target member", Locale.de: "Bitte gib die ID des Mitglieds ein"}),
                    reason: str = SlashOption(name="reason", description="Please enter a reason", required=True,
                                              name_localizations={Locale.de: "grund", Locale.en_US: "reason"},
                                              description_localizations={Locale.en_US: "Please enter a reason", Locale.de: "Bitte gib einen Grund an"})):
                
        if member.id == interaction.user.id:
            notyourself = Embed(description=self.trans["commands"]["member_unban"]["notyourself"]["description"][interaction.locale].format(emoji=config.a_cross), colour=config.dark_red)
            await interaction.response.send_message(embed=notyourself, ephemeral=True)
            return
        
        unbanctx = Embed(description=self.trans["commands"]["member_unban"]["notyourself"]["description"][interaction.locale].format(emoji_a=config.DiscordBan, emoji_b=config.dc_members, member=member.mention), colour=config.green)
        
        await interaction.guild.unban(member, reason=reason)
        await interaction.response.send_message(embed=unbanctx, ephemeral=True)

##########################################################################################################################################################

    #Timeout_Command (V 4.0)
    @member.subcommand(name="timeout", description="Add or stop a timeout",
                       description_localizations={Locale.en_US: "Add or stop a timeout", Locale.de: "Hinzufügen oder Beenden einer Auszeit"})
    @perms_check.has_min_moderator_perm_role()
    async def member_timeout(self, interaction: Interaction,
                    member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                    description_localizations={Locale.en_US: "Please select a member", Locale.de: "Bitte wähle ein Mitglied"}),
                    option: str = SlashOption(name="execution", description="Choose whether you want to add or remove a timeout", choices=["Add", "Remove"], required=True,
                                              name_localizations={Locale.en_US: "execution", Locale.de: "ausführung"},
                                              description_localizations={Locale.en_US: "Choose whether you want to add or remove a timeout", Locale.de: "Wähle, ob du eine Auszeit hinzufügen oder entfernen willst"},
                                              choice_localizations={"Add": {Locale.en_US: "Add", Locale.de: "Hintufügen"},
                                                                    "Remove": {Locale.en_US: "Remove", Locale.de: "Entfernen"}})):
        if member.id == interaction.user.id:
            notyourself = Embed(description=self.trans["commands"]["member_timeout"]["notyourself"]["description"][interaction.locale].format(emoji=config.a_cross), colour=config.dark_red)
            await interaction.response.send_message(embed=notyourself, ephemeral=True)
            return
        
        
        elif member.communication_disabled_until:
            r = Embed(title=self.trans["commands"]["member_timeout"]["r"]["title"][interaction.locale],
                      description=self.trans["commands"]["member_timeout"]["r"]["description"][interaction.locale], colour=config.red)
            await interaction.response.send_message(embed=r, ephemeral=True)
        
        else:
            match option:
                case "Add":
                    await interaction.response.send_modal(modal=MT(member))

                case "Remove":
                    untimeoutdm = Embed(title=self.trans["commands"]["member_timeout"]["untimeoutdm"]["title"][interaction.locale].format(emoji=config.DiscordUnmuted, guild=interaction.guild.name),
                                            description=self.trans["commands"]["member_timeout"]["untimeoutdm"]["description"][interaction.locale], colour=config.green)
                    untimeoutdm.set_author(name=interaction.guild.name)
                    untimeoutdm.add_field(name=self.trans["commands"]["member_timeout"]["untimeoutdm"]["field_a"]["name"][interaction.locale], value=config.aktuelldatum, inline=True)
                    untimeoutdm.set_footer(text=f"Moderator {interaction.user.name} ➟ {interaction.user.id}", icon_url=interaction.user.avatar.url)
                    
                    untimeoutctx = Embed(description=self.trans["commands"]["member_timeout"]["untimeoutctx"]["description"][interaction.locale].format(emoji_a=config.DiscordUnmuted, emoji_b=config.dc_members, member=member.mention), colour=config.blurple)

                    try:
                        await member.send(embed=untimeoutdm)
                        untimeoutctx.add_field(name=self.trans["commands"]["member_timeout"]["untimeoutctx"]["field_a"]["name"][interaction.locale],
                                               value=self.trans["commands"]["member_timeout"]["untimeoutctx"]["field_a"]["value"][interaction.locale])
                    
                    except:
                        untimeoutctx.add_field(name=self.trans["commands"]["member_timeout"]["untimeoutctx"]["field_b"]["name"][interaction.locale],
                                               value=self.trans["commands"]["member_timeout"]["untimeoutctx"]["field_b"]["value"][interaction.locale])
                        pass
                    
                    await member.edit(timeout=None)
                    await interaction.edit_original_message(embed=untimeoutctx)

##########################################################################################################################################################    
    
    #Mute Command (V 4.0)
    @member.subcommand(name="mute", description="Mute a member in the voice channel",
                       name_localizations={Locale.en_US: "mute", Locale.de: "stummschalten"}, 
                       description_localizations={Locale.en_US: "Mute a member in the voice channel", Locale.de: "Schalte einen Member im Sprachkanal stumm"})
    @perms_check.has_min_moderator_perm_role()
    async def member_mute(self, inter: Interaction, member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                                                    description_localizations={Locale.en_US: "Please select a member", Locale.de: "Bitte wähle ein Mitglied"}),
                          target: str = SlashOption(name="mode", choices=["microphone", "microphone and headset"], required=True,
                                                    name_localizations={Locale.en_US: "mode", Locale.de: "modus"},
                                                    choice_localizations={"microphone": {Locale.en_US: "microphone", Locale.de: "mikrofon"},
                                                                          "microphone and headset": {Locale.en_US: "microphone and headset", Locale.de: "nikrofon und headset"}}),
                          reason: str = SlashOption(name="reason", required=False, max_length=45, default="No reason", description="Please enter a reason",
                                                    name_localizations={Locale.de: "grund", Locale.en_US: "reason"},
                                                    description_localizations={Locale.en_US: "Please enter a reason", Locale.de: "Bitte gib einen Grund an"})):
        
       
        case_a = Embed(title=self.trans["commands"]["member_timeout"]["case_a"]["title"][inter.locale].format(emoji=config.a_tic),
                       description=self.trans["commands"]["member_timeout"]["case_a"]["description"][inter.locale].format(member=member), colour=config.green)
        
        case_b = Embed(title=self.trans["commands"]["member_timeout"]["case_b"]["title"][inter.locale].format(emoji=config.a_tic),
                       description=self.trans["commands"]["member_timeout"]["case_b"]["description"][inter.locale].format(member=member), colour=config.green)
        
        err = Embed(title=self.trans["commands"]["member_timeout"]["err"]["title"][inter.locale].format(emoji=config.a_tic),
                    description=self.trans["commands"]["member_timeout"]["err"]["description"][inter.locale].format(member=member), colour=config.red)
        
        await inter.response.defer(ephemeral=True)
        random_id = generate_random_id(10)
        current_time = config.aktuelldatum


        match target:
            case "microphone":
                try:
                    await member.edit(mute=True)
                    await self.bot.db.insert_case(inter.guild.id, member.id, inter.user.id, current_time, reason, None, random_id, "Mute", "Open")
                    await inter.edit_original_message(embed=case_a)
                except:
                    await inter.edit_original_message(embed=err)

            case "microphone and headset":
                try:
                    await self.bot.db.insert_case(inter.guild.id, member.id, inter.user.id, current_time, reason, None, random_id, "Fullmute", "Open")
                    await inter.edit_original_message(embed=case_b)
                except:
                    await inter.edit_original_message(embed=err)
                          
##########################################################################################################################################################

    #Warn-Member_Command
    @nc.slash_command(name="warn", description="Warn a member")
    @perms_check.has_min_moderator_perm_role()
    async def warn_member(self, inter: Interaction, member: nc.Member = SlashOption(name="member", description="Please select a member", required=True)):
                    
        modal = NewWarnModal(member)
        await inter.response.send_modal(modal)
    
##########################################################################################################################################################
    
    #History_Command    
    @nc.slash_command(name="history", name_localizations={Locale.de: "historie", Locale.en_US: "history"})
    async def history(self, inter: Interaction):
        pass

    #History-Info (V 4.0)
    @history.subcommand(name="information", description="Get Info about a Case from a member",
                        description_localizations={Locale.en_US: "Get Info about a Case from a member", Locale.de: "Informationen über einen Fall von einem Mitglied erhalten"})
    @perms_check.has_min_moderator_perm_role()
    async def history_info(self, inter: Interaction,
                            member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                            description_localizations={Locale.en_US: "Please select a member", Locale.de: "Bitte wähle ein Mitglied"})):
        cases = await self.bot.db.query_all_case_ids(member.id, inter.guild.id)
        if cases:
            options = []
            for case in cases:
                query = await self.bot.db.query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                
                if inter.locale == "de":
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Fall geöffnet von: {c_mod.name}\nGrund: {query[2]}\n{query[3] if query[3] is not None else 'Keine Information'}")
                
                elif inter.locale == "en_US":
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                
                else:
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                
                options.append(new_option)
            options = options[:25]  

            i_embed = Embed(title=self.trans["commands"]["history_info"]["i_embed"]["title"][inter.locale].format(member=member),
                            description=self.trans["commands"]["history_info"]["i_embed"]["description"][inter.locale], colour=config.blurple)  
            
            if inter.locale == "de":
                await inter.response.send_message(content="Bitte warten", ephemeral=True)
                
            elif inter.locale == "en_US":
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            else:
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            member_id = member.id
            dropdown = CaseInfoDropdown(member_id, options)
            await inter.edit_original_message(embed=i_embed, view=dropdown, content=None)
            
        else:
            notfound_embed = Embed(title=self.trans["commands"]["history_info"]["notfound_embed"]["title"][inter.locale],
                                   description=self.trans["commands"]["history_info"]["notfound_embed"]["description"][inter.locale].format(member=member), colour=config.blurple)  
            await inter.response.send_message(embed=notfound_embed, ephemeral=True)

##########################################################################################################################################################
        
    #history-Edit (V 4.0)
    @history.subcommand(name="edit", description="Edit some Cases from a member",
                        name_localizations={Locale.en_US: "edit", Locale.de: "bearbeiten"},
                        description_localizations={Locale.en_US: "Edit some Cases from a member", Locale.de: "Fälle eines Mitglieds bearbeiten"})
    @perms_check.has_min_moderator_perm_role()
    async def history_edit_by_user(self, inter: Interaction,
                            member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                            description_localizations={Locale.en_US: "Please select a member", Locale.de: "Bitte wähle ein Mitglied"})):
            
        cases = await self.bot.db.query_all_case_ids(member.id, inter.guild.id)
        if cases:
            options = []
            for case in cases:
                query = await self.bot.db.query_case_all(case[0], inter.guild.id)
                
                if query[6].split()[0] == "Closed":
                
                    c_mod = inter.guild.get_member(query[0])
                    
                    if inter.locale == "de":
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])} (GESCHLOSSEN)", description=f"Fall geöffnet von: {c_mod.name}\nGrund: {query[2]}\n{query[3] if query[3] is not None else 'Keine Informationen'}")
                        
                    elif inter.locale == "en_US":
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])} (CLOSED)", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")
                        
                    else:
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])} (CLOSED)", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")

                    options.append(new_option)
                
                else:
                    c_mod = inter.guild.get_member(query[0])
                    
                    if inter.locale == "de":
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Fall geöffnet von: {c_mod.name}\nGrund: {query[2]}\n{query[3] if query[3] is not None else 'Keine Informationen'}")
                        
                    elif inter.locale == "en_US":
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")
                        
                    else:
                        new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")

                    options.append(new_option)

            options = options[:25]  

            i_embed = Embed(title=self.trans["commands"]["history_edit_by_user"]["i_embed"]["title"][inter.locale].format(member=member),
                            description=self.trans["commands"]["history_edit_by_user"]["i_embed"]["description"][inter.locale], colour=config.blurple)  

            if inter.locale == "de":
                await inter.response.send_message(content="Bitte warten", ephemeral=True)
                
            elif inter.locale == "en_US":
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            else:
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            member_id = member.id
            dropdown = EditCaseDropdown(member_id, options)
            await inter.edit_original_message(embed=i_embed, view=dropdown, content=None)
            
        else:
            notfound_embed = Embed(title=self.trans["commands"]["history_edit_by_user"]["notfound_embed"]["title"][inter.locale],
                                   description=self.trans["commands"]["history_edit_by_user"]["notfound_embed"]["description"][inter.locale].format(member=member), colour=config.blurple)    
            await inter.response.send_message(embed=notfound_embed, ephemeral=True)
       
##########################################################################################################################################################

    #history_Delete Command (V 4.0)
    @history.subcommand(name="delete", description="Remove a member's case",
                        name_localizations={Locale.de: "löschen", Locale.en_US: "delete"},
                        description_localizations={Locale.en_US: "Remove a member's case", Locale.de: "Fall eines Mitglieds entfernen"})
    @perms_check.has_min_moderator_perm_role()
    async def history_delete(self, inter: Interaction, member: nc.Member = SlashOption(name="member", description="Please select a member", required=True,
                                                                                       description_localizations={Locale.en_US: "Please select a member", Locale.de: "Bitte wähle ein Mitglied"})):

        cases = await self.bot.db.query_all_case_ids(member.id, inter.guild.id)
        
        if cases:
            options = []
            for case in cases:
                query = await self.bot.db.query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                
                if inter.locale == "de":
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Fall geöffnet von: {c_mod.name}\nGrund: {query[2]}\n{query[3] if query[3] is not None else 'Keine Informationen'}")
                
                elif inter.locale == "en_US":
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")
                
                else:
                    new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Informations'}")
                
                options.append(new_option)
            options = options[:25]  

            i_embed = Embed(title=self.trans["commands"]["history_delete"]["i_embed"]["title"][inter.locale].format(member=member),
                            description=self.trans["commands"]["history_delete"]["i_embed"]["description"][inter.locale], colour=config.blurple)  

            if inter.locale == "de":
                await inter.response.send_message(content="Bitte warten", ephemeral=True)
                                
            elif inter.locale == "en_US":
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            else:
                await inter.response.send_message(content="Please wait", ephemeral=True)
                
            member_id = member.id
            dropdown = DeleteCaseDropdown(member_id, options)
            await inter.edit_original_message(embed=i_embed, view=dropdown, content=None)
        
        else:
            notfound_embed = Embed(title=self.trans["commands"]["history_delete"]["notfound_embed"]["title"][inter.locale],
                                   description=self.trans["commands"]["history_delete"]["notfound_embed"]["description"][inter.locale].format(member=member), colour=config.blurple)  
            await inter.response.send_message(embed=notfound_embed, ephemeral=True)
                    
##########################################################################################################################################################

    #RoleInfo_Command
    @nc.slash_command(name="role-info", description="Get information about a role")    
    @perms_check.has_min_supporter_perm_role()
    async def role_info(self, interaction: Interaction,
                        role: nc.Role = SlashOption(name="role", description="Please select a role", required=True)):
                
        new_line = "\n"
        roleidctx = Embed(title=f"{config.e_information} Info about the role {role} on {interaction.guild.name}",
                                description=f"```Name: {role.name}\n"
                                f"ID: {role.id}\n"
                                f"Display Separately: {role.hoist}\n"
                                f"Position: {role.position}\n"
                                f"Member Count: {len(role.members)}\n"
                                f"Mentionable: {role.mentionable}\n"
                                f"Colour: {role.colour}\n"
                                f"\n"
                                f"Permsissions: \n{new_line.join([perm for perm, value in role.permissions if value is True])}\n"
                                f"\n"
                                f"Created at: {str(role.created_at)[0:16]}```", colour=role.colour)

        await interaction.response.send_message(embed=roleidctx, ephemeral=True)
    

##########################################################################################################################################################
  
def setup(bot: commands.Bot):
    bot.add_cog(Member_Moderation(bot))