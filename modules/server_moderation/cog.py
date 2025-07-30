import cooldowns

import nextcord
from nextcord import ChannelType, SlashOption, Embed, File, ButtonStyle, Interaction, Locale
from nextcord.ext import commands

import config
from modules.server_moderation.view import ChannelRename, ChannelSlowmode
from modules.server_moderation.view import PermissionOverwriteView
import perms_check
import yaml



class Yes_OR_No(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        
    @nextcord.ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = True
        button.disabled = True
        bn = self.children[1]
        bn.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
        
    @nextcord.ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = False
        button.disabled = True
        by = self.children[0]
        by.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

        
    async def on_timeout(self):
        by = self.children[0]
        bn = self.children[1]
        by.disabled = True
        bn.disabled = True
        by.style = ButtonStyle.grey
        bn.style = ButtonStyle.grey

        await self.message.edit(view=self)

class Ja_Oder_Nein(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        
    @nextcord.ui.button(label="Ja", style=ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = True
        button.disabled = True
        bn = self.children[1]
        bn.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
        
    @nextcord.ui.button(label="Nein", style=ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = False
        button.disabled = True
        by = self.children[0]
        by.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

        
    async def on_timeout(self):
        by = self.children[0]
        bn = self.children[1]
        by.disabled = True
        bn.disabled = True
        by.style = ButtonStyle.grey
        bn.style = ButtonStyle.grey

        await self.message.edit(view=self)

class server_moderation(commands.Cog, name="Server Moderation"):
    """Contains all Server-Moderation commands"""

    COG_EMOJI = config.dc_guide
    
    def __init__(self, bot):
        self.bot = bot

    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
    
########################################################################################################       
    
    #Channel-Info_Command (V5.1)
    @nextcord.slash_command(name="channel-info", description="Displays all information about a channel",
                            name_localizations={Locale.en_US: "channel-info", Locale.de: "kanalinformation"},
                            description_localizations={Locale.en_US: "Displays all information about a channel", Locale.de: "Zeigt alle Informationen über einen Kanal an"})   
    @perms_check.has_min_supporter_perm_role() 
    async def channel_info(self, interaction: Interaction,
                           channel: nextcord.abc.GuildChannel = SlashOption(name="channel", description=f"Please select a channel", name_localizations={Locale.en_US: "channel", Locale.de: "kanal"},
                                                                            description_localizations={Locale.en_US: "Please select a channel!", Locale.de: "Bitte wähle einen Kanal!"},
                                                                             channel_types=[ChannelType.text, 
                                                                                            ChannelType.news_thread, 
                                                                                            ChannelType.public_thread,
                                                                                            ChannelType.private_thread, 
                                                                                            ChannelType.forum,
                                                                                            ChannelType.voice,
                                                                                            ChannelType.stage_voice], required=False)):
        
        s_channel = channel or interaction.channel
                
        cs = Embed(title=f"Statistics for:   {config.dc_channel} **{s_channel.name}**",
                            description=f"{'Category: {}'.format(s_channel.category.name) if s_channel.category else 'This channel is not in any category!'}",
                            colour=config.random_colour)

        cs_de = Embed(title=f"Statistiken für:   {config.dc_channel} **{s_channel.name}**",
                            description=f"{'Kategorie: {}'.format(s_channel.category.name) if s_channel.category else 'Dieser Kanal befindet sich in keiner Kategorie!'}",
                            colour=config.random_colour)
                
        await interaction.response.defer(ephemeral=True)
    
        if isinstance(s_channel, nextcord.TextChannel):

            information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
            information_icon_url = "attachment://information-icon.png"

            cs.add_field(name="__**General**__", value=
                        f"> **Channel-Name:** {s_channel.name}\n"
                        f"> **Channel-Mention:** {s_channel.jump_url}\n"
                        f"> **Channel-ID:** `{s_channel.id}`\n\n"
                        f"> **Category:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n"                          
                        f"> **Category-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Topic:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)
            cs.add_field(name="__**Channel Settings**__", value=
                        f"> **Slowmode-Delay:** {s_channel.slowmode_delay} secounds\n\n"
                        f"> **Default-Auto-Archive-Duration:** {s_channel.default_auto_archive_duration/60} hours\n", inline=True)
            cs.add_field(name="__**Channel Informations**__", value=
                        f"> **Created:**  {f'<t:{int(s_channel.created_at.timestamp())}:F>'}\n\n", inline=True)
            cs.set_thumbnail(url=information_icon_url)


            cs_de.add_field(name="__**Allgemein**__", value=
                        f"> **Kanal-Name:** {s_channel.name}\n"
                        f"> **Kanal-Erwähnung:** {s_channel.jump_url}\n"
                        f"> **Kanal-ID:** `{s_channel.id}`\n\n"
                        f"> **Kategorie:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n"                          
                        f"> **Kategorie-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Thema:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)
            cs_de.add_field(name="__**Kanaleinstellungen**__", value=
                        f"> **Slowmode:** {s_channel.slowmode_delay} Sekunden\n\n"
                        f"> **Standard-Auto-Archivierungsdauer:** {s_channel.default_auto_archive_duration/60} Stunden\n", inline=True)
            cs_de.add_field(name="__**Kanalinformationen**__", value=
                        f"> **Erstellt:**  {f'<t:{int(s_channel.created_at.timestamp())}:F>'}\n\n", inline=True)
            cs_de.set_thumbnail(url=information_icon_url)
            
            if interaction.locale == "de":
                await interaction.edit_original_message(embed=cs_de, file=information_icon_png)
                
            elif interaction.locale == "en_US":
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            else:
                await interaction.edit_original_message(embed=cs, file=information_icon_png)


        if isinstance(s_channel, nextcord.StageChannel):

            information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
            information_icon_url = "attachment://information-icon.png"
            
            cs.add_field(name="__**General**__", value=
                        f"> **Stage-Name:** {s_channel.name}\n"
                        f"> **Stage-Mention:** {s_channel.jump_url}\n"
                        f"> **Stage-ID:** `{s_channel.id}`\n\n"
                        f"> **Topic:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Category:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n" 
                        f"> **Category-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)  
            cs.add_field(name="__**Stage Voice Settings**__", value=
                        f"> **Bitrate:** {s_channel.bitrate}\n\n"
                        f"> **User-Limit:** {s_channel.user_limit}\n\n"
                        f"> **Region:** {s_channel.rtc_region if s_channel.rtc_region else '`-----`'}\n\n"
                        f"> **Video-Quality-Mode:** {s_channel.video_quality_mode}\n", inline=True)       
            cs.add_field(name="__**Thread Informations**__", value=
                        f"> **Created:** <t:{int(s_channel.created_at.timestamp())}:F>\n\n", inline=True)
            cs.set_thumbnail(url=information_icon_url)


            cs_de.add_field(name="__**Allgemein**__", value=
                        f"> **Stage-Name:** {s_channel.name}\n"
                        f"> **Stage-Erwähnung:** {s_channel.jump_url}\n"
                        f"> **Stage-ID:** `{s_channel.id}`\n\n"
                        f"> **Thema:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Kategorie:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n" 
                        f"> **Kategorie-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)  
            cs_de.add_field(name="__**Stage-Kanal-Einstellungen**__", value=
                        f"> **Bitrate:** {s_channel.bitrate}\n\n"
                        f"> **Benutzerlimit:** {s_channel.user_limit}\n\n"
                        f"> **Region:** {s_channel.rtc_region if s_channel.rtc_region else '`-----`'}\n\n"
                        f"> **Video-Qualität-Modus:** {s_channel.video_quality_mode}\n", inline=True)       
            cs_de.add_field(name="__**Stage-Kanal-Informationen**__", value=
                        f"> **Erstellt:** <t:{int(s_channel.created_at.timestamp())}:F>\n\n", inline=True)
            cs_de.set_thumbnail(url=information_icon_url)
                                   
            if interaction.locale == "de":
                await interaction.edit_original_message(embed=cs_de, file=information_icon_png)
                
            elif interaction.locale == "en_US":
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            else:
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
        

        if isinstance(s_channel, nextcord.VoiceChannel):

            information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
            information_icon_url = "attachment://information-icon.png"
                        
            cs.add_field(name="__**General**__", value=
                        f"> **Voice-Name:** {s_channel.name}\n"
                        f"> **Voice-Mention:** {s_channel.jump_url}\n"
                        f"> **Voice-ID:** `{s_channel.id}`\n\n"
                        f"> **Category:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n" 
                        f"> **Category-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)
            cs.add_field(name="__**Voice Settings**__", value=
                        f"> **Bitrate:** {s_channel.bitrate}\n\n"
                        f"> **User-Limit:** {s_channel.user_limit}\n\n"
                        f"> **Region:** {s_channel.rtc_region if s_channel.rtc_region else '`-----`'}\n\n"
                        f"> **Video-Quality-Mode:** {s_channel.video_quality_mode}\n", inline=True)       
            cs.add_field(name="__**Voice Informations**__", value=
                        f"> **Created:** <t:{int(s_channel.created_at.timestamp())}:F>\n\n", inline=True)
            cs.set_thumbnail(url=information_icon_url)

            cs_de.add_field(name="__**Allgemein**__", value=
                        f"> **Voice-Name:** {s_channel.name}\n"
                        f"> **Voice-Mention:** {s_channel.jump_url}\n"
                        f"> **Voice-ID:** `{s_channel.id}`\n\n"
                        f"> **Kategorie:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n" 
                        f"> **Kategorie-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position+1}`\n\uFEFF", inline=False)
            cs_de.add_field(name="__**Voice-EInstellungen**__", value=
                        f"> **Bitrate:** {s_channel.bitrate}\n\n"
                        f"> **Benutzerlimit:** {s_channel.user_limit}\n\n"
                        f"> **Region:** {s_channel.rtc_region if s_channel.rtc_region else '`-----`'}\n\n"
                        f"> **Video-Quality-Modus:** {s_channel.video_quality_mode}\n", inline=True)       
            cs_de.add_field(name="__**Voice-Informationen**__", value=
                        f"> **Erstellt:** <t:{int(s_channel.created_at.timestamp())}:F>\n\n", inline=True)
            cs_de.set_thumbnail(url=information_icon_url)
                                   
            if interaction.locale == "de":
                await interaction.edit_original_message(embed=cs_de, file=information_icon_png)
                
            elif interaction.locale == "en_US":
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            else:
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            return
            
            
        if isinstance(s_channel, nextcord.Thread):

            information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
            information_icon_url = "attachment://information-icon.png"
             
            cs.add_field(name="__**General**__", value=
                        f"> **Thread-Name:** {s_channel.name}\n"
                        f"> **Thread-Mention:** {s_channel.jump_url}\n"
                        f"> **Thread-ID:** `{s_channel.id}`\n\n"
                        f"> **Original-Channel:** <#{s_channel.parent_id}>\n"
                        f"> **Original-ID:** `{s_channel.parent_id}`\n\n"
                        f"> **Thread-Owner:** <@{s_channel.owner_id}>\n"
                        f"> **Thread-Owner-ID:** `{s_channel.owner_id}`\n\uFEFF", inline=False)
            cs.add_field(name="__**Thread Settings**__", value=
                        f"> **Slowmode-Delay:** {s_channel.slowmode_delay}\n\n"
                        f"> **Auto-Archive-Duration:** {s_channel.auto_archive_duration/60} hours\n\n"
                        f"> **Private:** {config.a_tic if s_channel.is_private() else config.a_cross}\n\n"
                        f"> **NSFW:** {config.a_tic if s_channel.is_nsfw() else config.a_cross}", inline=True)
            cs.add_field(name="__**Thread Informations**__", value=
                        f"> **Created:** <t:{int(s_channel.create_timestamp.timestamp())}:F>\n\n"
                        f"> **Archived:** {config.a_tic if s_channel.archived else config.a_cross}\n"
                        f"> **Last Archive:** {f'<t:{int(s_channel.archive_timestamp.timestamp())}:F>' if s_channel.archive_timestamp else 'Not archived'}\n\n"
                        f"> **Locked:** {config.a_tic if s_channel.locked else config.a_cross}\n\n"
                        f"> **Invitable:** {config.a_tic if s_channel.invitable else config.a_cross}\n\n", inline=True)
            cs.set_thumbnail(url=information_icon_url)
            
            
            cs_de.add_field(name="__**Allgemein**__", value=
                        f"> **Thread-Name:** {s_channel.name}\n"
                        f"> **Thread-Erwähnung:** {s_channel.jump_url}\n"
                        f"> **Thread-ID:** `{s_channel.id}`\n\n"
                        f"> **Originaler Kanal:** <#{s_channel.parent_id}>\n"
                        f"> **Original-ID:** `{s_channel.parent_id}`\n\n"
                        f"> **Thread-Besitzer:** <@{s_channel.owner_id}>\n"
                        f"> **Thread-Besitzer-ID:** `{s_channel.owner_id}`\n\uFEFF", inline=False)
            cs_de.add_field(name="__**Thread-Einstellungen**__", value=
                        f"> **Slowmode:** {s_channel.slowmode_delay}\n\n"
                        f"> **Auto-Archivierungsdauer:** {s_channel.auto_archive_duration/60} hours\n\n"
                        f"> **Privat:** {config.a_tic if s_channel.is_private() else config.a_cross}\n\n"
                        f"> **NSFW:** {config.a_tic if s_channel.is_nsfw() else config.a_cross}", inline=True)
            cs_de.add_field(name="__**Thread-Informationen**__", value=
                        f"> **Erstellt:** <t:{int(s_channel.create_timestamp.timestamp())}:F>\n\n"
                        f"> **Archived:** {config.a_tic if s_channel.archived else config.a_cross}\n"
                        f"> **letzte Archivierung:** {f'<t:{int(s_channel.archive_timestamp.timestamp())}:F>' if s_channel.archive_timestamp else 'Not archived'}\n\n"
                        f"> **Geschlossen:** {config.a_tic if s_channel.locked else config.a_cross}\n\n"
                        f"> **Einladbar:** {config.a_tic if s_channel.invitable else config.a_cross}\n\n", inline=True)
            cs_de.set_thumbnail(url=information_icon_url)

            if interaction.locale == "de":
                await interaction.edit_original_message(embed=cs_de, file=information_icon_png)
                
            elif interaction.locale == "en_US":
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            else:
                await interaction.edit_original_message(embed=cs, file=information_icon_png)



        if isinstance(s_channel, nextcord.ForumChannel):

            information_icon_png = File("pictures/information-icon.png", filename="information-icon.png")
            information_icon_url = "attachment://information-icon.png"
                        
            cs.add_field(name="__**General**__", value=
                        f"> **Forum-Name:** {s_channel.name}\n"
                        f"> **Forum-Mention:** {s_channel.jump_url}\n"
                        f"> **Forum-ID:** `{s_channel.id}`\n\n"
                        f"> **Topic:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Category:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n"
                        f"> **Category-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position}`\n\uFEFF", inline=False)
            cs.add_field(name="__**Forum Channel Settings**__", value=
                        f"> **Slowmode-Delay:** {s_channel.slowmode_delay}\n"
                        f"> **Default-Auto-Archive-Duration:** {s_channel.default_auto_archive_duration/60} hours\n"
                        f"> **NSFW:** {config.a_tic if s_channel.is_nsfw() else config.a_cross}\n", inline=True)
            cs.add_field(name="__**Forum Channel Informations**__", value=
                        f"> **Created:**  {f'<t:{int(s_channel.created_at.timestamp())}:F>'}\n\n", inline=True)
            cs.set_thumbnail(url=information_icon_url)


            cs_de.add_field(name="__**Allgemein**__", value=
                        f"> **Forum-Name:** {s_channel.name}\n"
                        f"> **Forum-Erwähnung:** {s_channel.jump_url}\n"
                        f"> **Forum-ID:** `{s_channel.id}`\n\n"
                        f"> **Thema:** {s_channel.topic if s_channel.topic else '`-----`'}\n\n"
                        f"> **Kategorie:** {f'<#{s_channel.category_id}>' if s_channel.category_id else '`-----`'}\n"
                        f"> **Kategorie-ID:** `{s_channel.category_id if s_channel.category else '-----'}`\n\n"
                        f"> **Position:** `{s_channel.position}`\n\uFEFF", inline=False)
            cs_de.add_field(name="__**Forum-Kanal-Einstellungen**__", value=
                        f"> **Slowmode:** {s_channel.slowmode_delay}\n"
                        f"> **Standard-Auto-Archivierungsdauer:** {s_channel.default_auto_archive_duration/60} hours\n"
                        f"> **NSFW:** {config.a_tic if s_channel.is_nsfw() else config.a_cross}\n", inline=True)
            cs_de.add_field(name="__**Forum-Kanal-Informationen**__", value=
                        f"> **Erstellt:**  {f'<t:{int(s_channel.created_at.timestamp())}:F>'}\n\n", inline=True)
            cs_de.set_thumbnail(url=information_icon_url)
                                   
            if interaction.locale == "de":
                await interaction.edit_original_message(embed=cs_de, file=information_icon_png)
                
            elif interaction.locale == "en_US":
                await interaction.edit_original_message(embed=cs, file=information_icon_png)
                
            else:
                await interaction.edit_original_message(embed=cs, file=information_icon_png)


        return    

##########################################################################################################################################################
    
    #Clear_Command (V5.1)
    @nextcord.slash_command(name="clear", description="Clean up the chat the way you want it",
                            description_localizations={Locale.de: "Räume den Chat so auf, wie du es möchtest.", Locale.en_US: "Clean up the chat the way you want it"},)    
    @perms_check.has_min_moderator_perm_role()
    async def clear(self, interaction: Interaction,
                    amount: int = SlashOption(name="amount", description="How many messages should be deleted? (1-100 messages)", min_value=1, max_value=100,
                                              name_localizations={Locale.de: "anzahl", Locale.en_US: "amount"},
                                              description_localizations={Locale.de: "Wie viele Nachrichten sollen gelöscht werden? (1-100 Nachrichten)", Locale.en_US: "How many messages should be deleted? (1-100 messages)"})):
        
        ays = nextcord.Embed(description=self.trans["commands"]["clear"]["ays"]["description"][interaction.locale].format(a_support=config.a_support, amount=amount), colour=config.blurple)

        if interaction.locale == "de":
            view = Ja_Oder_Nein()
        elif interaction.locale == "en_US":
            view = Yes_OR_No()
        else:
            view = Yes_OR_No()

        clearctx = nextcord.Embed(title=self.trans["commands"]["clear"]["clear_ctx"]["title"][interaction.locale],
                                  description=f"{self.trans['commands']['clear']['clear_ctx']['title'][interaction.locale].format(a_trash=config.a_trash, amount=amount)} messages!", colour=config.blurple)

        if amount >= 5:
            await interaction.response.send_message(embed=ays, ephemeral=True, view=view)
        
            view.message = await interaction.original_message()
        
            await view.wait()
        
            if view.value is None:
                return
            
            elif view.value:                
                await interaction.channel.purge(limit=amount)
                await interaction.edit_original_message(embed=clearctx)
                
            else:
                embed = nextcord.Embed(description=self.trans["commands"]["clear"]["embed"]["description"][interaction.locale], colour=config.red)
                await interaction.edit_original_message(embed=embed)

        else:                
            await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(embed=clearctx, ephemeral=True)
    
##########################################################################################################################################################                

    #Edit-Channel_Command           
    @nextcord.slash_command(name="edit-channel", description="Change the name of a choosen Channel")
    @perms_check.has_min_moderator_perm_role()
    @cooldowns.cooldown(1, 300, bucket=cooldowns.SlashBucket.channel)
    async def edit_channel(self, inter: Interaction, option: str = SlashOption(name="option", description="Please select a option", required=True, choices=["rename", "slowmode_delay"])):
        match option:
            case "rename":
                modal = ChannelRename()
                await inter.response.send_modal(modal)
            
            case "slowmode_delay":
                await inter.response.send_message(view=ChannelSlowmode(), ephemeral=True)

########################################################################################################################################

    #Lockdown_Command (V 3.10)

    @nextcord.slash_command(name="lockdown", description="Opens or closes a text channel!")    
    @perms_check.has_min_supporter_perm_role()
    async def lockdown(self, interaction: Interaction,
                        channel: nextcord.abc.GuildChannel = SlashOption(name="channel", channel_types=[ChannelType.text], required=False)):
                            
        selected_channel = channel or interaction.channel
        target_channel = interaction.guild.get_channel(selected_channel.id)

        lockdownclose = Embed(description=f"{config.a_lock} This channel has been closed by a moderator",
                            colour=config.red)
        lockdownopen = Embed(description=f"{config.a_unlock} This channel was opened by a moderator",
                                      colour=config.green)

        done = Embed(description=f"{config.a_tic} I have successfully locked/unlocked the channel", colour=config.green)

        bot = interaction.guild.get_member(self.bot.user.id)

        roles = bot.roles
        for role in roles:
            if role.is_bot_managed():
                managed_role = interaction.guild.get_role(role.id)
                break

        q_embed = Embed(title=f"{config.a_cross} Missing Permissions", description=f"To continue I need permission __**Send Messages**__.\n"
                                   f"I would like to overwrite the permission __**Send Messages**__ for my role {managed_role.id} in this channel <#{interaction.channel.id}>.\n" 
                                   "Please confirm this action or cancel it.", colour=config.red)  
        
        permissions = target_channel.permissions_for(interaction.guild.get_member(bot.id))
        permissions_managed_role = target_channel.permissions_for(managed_role)      
                     
        await interaction.response.defer(ephemeral=True)
        
        if interaction.guild.default_role not in selected_channel.overwrites:
            if permissions.send_messages:
                if permissions_managed_role.send_messages:
                    overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
                    }
                    await selected_channel.edit(overwrites=overwrites)

                    await interaction.edit_original_message(embed=done)
                    await target_channel.send(embed=lockdownclose)
                    
                else:   
                    view = PermissionOverwriteView(managed_role, selected_channel)
                    await interaction.edit_original_message(embed=q_embed, view=view)
                    await view.wait()
                    if view.value is True:
                        return True
                    else:
                        return False
                                     
            else:
                view = PermissionOverwriteView(managed_role, selected_channel)
                await interaction.edit_original_message(embed=q_embed, view=view)
                await view.wait()
                if view.value is True:
                    return True
                else:
                    return False           
            
            
        elif selected_channel.overwrites[interaction.guild.default_role].send_messages == True or selected_channel.overwrites[interaction.guild.default_role].send_messages == None:
            if permissions_managed_role.send_messages:
                await interaction.edit_original_message(embed=done, view=None)
                await target_channel.send(embed=lockdownclose)
                await selected_channel.set_permissions(interaction.guild.default_role, send_messages=False)
                
            else:              
                view = PermissionOverwriteView(managed_role, selected_channel)
                await interaction.edit_original_message(embed=q_embed, view=view)
                await view.wait()
                if view.value is True:
                    return True
                else:
                    return False             
            
        else:            
            if permissions.send_messages:
                if permissions_managed_role.send_messages:
                    overwrites = selected_channel.overwrites[interaction.guild.default_role]
                    overwrites._values["send_messages"] = None
                    await selected_channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

                    await interaction.edit_original_message(embed=done)
                    await target_channel.send(embed=lockdownopen)
                    
                else:               
                    view = PermissionOverwriteView(managed_role, selected_channel)
                    await interaction.edit_original_message(embed=q_embed, view=view)
                    await view.wait()
                    if view.value is True:
                        return True
                    else:
                        return False   
            else:                
                view = PermissionOverwriteView(managed_role, selected_channel)
                await interaction.edit_original_message(embed=q_embed, view=view)
                await view.wait()
                if view.value is True:
                    return True
                else:
                    return False             
                
########################################################################################################################################

            
def setup(bot: commands.Bot):
    bot.add_cog(server_moderation(bot))