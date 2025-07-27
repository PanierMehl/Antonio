import nextcord
from nextcord import SlashOption, Embed, Interaction, Locale, File
from nextcord.ext import commands

import aiosqlite 
import asyncio
import yaml

from modules.setup_v2.view import (global_text_select_channels)

from modules.setup_v2.setup_view import (SetupAdminRoleSelect,
                                         SetupModerationRoleSelect,
                                         SetupSupporterRoleSelect,
                                         SetupLanguageSelect)

from modules.setup_v2.view_v2 import (universal_setup_remove,
                                      universal_role_select,
                                      universal_channel_select,
                                      language_add)

import perms_check
from mysql_class import BotDB
import config
from config import red


class Yes_OR_No(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        
    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = True
        button.disabled = True
        bn = self.children[1]
        bn.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
        
    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
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
        by.style = nextcord.ButtonStyle.grey
        bn.style = nextcord.ButtonStyle.grey

        await self.message.edit(view=self)
        




class Setup(commands.Cog, name="Setup"):
    """Contains all setup commands"""

    COG_EMOJI = config.dc_settings
    
    def __init__(self, bot):
        self.bot = bot

    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
            
                                
#################################################################################################################            
#################################################################################################################
#################################################################################################################

    async def get_status_embed(self, inter: Interaction):    
 
        data = BotDB().query_server_table(inter.guild.id)

        if data is None:
            admin_role = None
            mod_role = None
            sup_role = None
            global_channel = None
            language = None
            
        else:
            get_admin_role = inter.guild.get_role(data[1])
            admin_role = data[1]

            get_mod_role = inter.guild.get_role(data[2])
            mod_role = data[2]

            get_sup_role = inter.guild.get_role(data[3])
            sup_role = data[3]

            get_global_channel = inter.guild.get_channel(data[5])
            global_channel = data[4]

            language = data[5]                 
            
        nl = '\n'
            
        return nextcord.Embed(title="SETUP ➟ Status", description=
                    f"> Administrator Role {config.a_cross if admin_role is None else f'{config.a_tic} {nl} > {get_admin_role}'}\n\n"
                    
                    f"> Moderator Role {config.a_cross if mod_role is  None else f'{config.a_tic} {nl} > {get_mod_role}'}\n\n"
                    
                    f"> Supporter Role {config.a_cross if sup_role is None else f'{config.a_tic} {nl} > {get_sup_role}'}\n\n"
                    
                    f"> Global Channel {config.a_cross if global_channel is None else f'{config.a_tic} {nl} > {get_global_channel}'}\n\n"
                    
                    f"> Language {config.a_cross if language is None else f'{config.a_tic} {nl} > {language}'}",
                    
                    colour=config.gold)

#################################################################################################################            

    @nextcord.slash_command(name="setup", name_localizations={Locale.en_US: "setup", Locale.de: "einrichtung"})
    async def setup(self, inter: Interaction):
        pass

    @setup.subcommand(name="start", description="Setup the Bot! (Only Server Owner)", description_localizations={Locale.en_US: "Setup the Bot! (Only Server Owner)", Locale.de: "Richte den Bot ein. (Nur Serverbesitzer)"})
    async def setup_start(self, inter: Interaction):

        if inter.user.guild.owner:
            await inter.response.defer(ephemeral=True)
            org = await inter.original_message()

            data = BotDB().query_server_table(inter.guild.id)

            if data is None:
                admin_role = None
                mod_role = None
                sup_role = None
                global_channel = None
                language = None
            else:
                admin_role = data[1]

                mod_role = data[2]

                sup_role = data[3]

                global_channel = data[4]

                language = data[5]                  
        

            embed_start = nextcord.Embed(title=self.trans["commands"]["setup_start"]["embed_start"]["title"][inter.locale],
                                        description=self.trans["commands"]["setup_start"]["embed_start"]["description"][inter.locale], colour=config.blurple)
            
            embed_wait = nextcord.Embed(title=self.trans["commands"]["setup_start"]["embed_wait"]["title"][inter.locale],
                                        description=self.trans["commands"]["setup_start"]["embed_wait"]["description"][inter.locale], colour=config.blurple)
            
            status_embed_a = await self.get_status_embed(inter)
            await org.edit(embeds=[status_embed_a, embed_start])
            await asyncio.sleep(3)
            
            if admin_role is None:
                
                SetupAdminView = SetupAdminRoleSelect(inter)
                reply = nextcord.Embed(title=self.trans["commands"]["setup_start"]["reply_a_role"]["title"][inter.locale],
                                    description=self.trans["commands"]["setup_start"]["reply_a_role"]["description"][inter.locale].format(emoji=config.dc_settings), colour=config.blurple)
                
                status_embed_b = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_b, reply], view=SetupAdminView, attachments=[])
                
                SetupAdminView.message = org                                        
                await SetupAdminView.wait()
                
                status_embed_c = await self.get_status_embed(inter)
                await org.edit(embed=status_embed_c, attachments=[])
                await asyncio.sleep(2)
                    
            else:
                status_embed_d = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_d, embed_wait], attachments=[])
                await asyncio.sleep(2)
                

            if mod_role is None:               
                
                SetupModerationView = SetupModerationRoleSelect()
                reply = nextcord.Embed(title=self.trans["commands"]["setup_start"]["reply_m_role"]["title"][inter.locale],
                                    description=self.trans["commands"]["setup_start"]["reply_m_role"]["description"][inter.locale].format(emoji=config.dc_settings), colour=config.blurple)
                
                status_embed_e = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_e, reply], view=SetupModerationView, attachments=[])
                
                SetupModerationView.message = org
                await SetupModerationView.wait()
                
                status_embed_f = await self.get_status_embed(inter)
                await org.edit(embed=status_embed_f, attachments=[])
                await asyncio.sleep(2)                    


            else:
                status_embed_g = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_g, embed_wait], attachments=[])
                await asyncio.sleep(2)              
            

            if sup_role is None:

                SetupSupporterView = SetupSupporterRoleSelect()
                
                reply = nextcord.Embed(title=self.trans["commands"]["setup_start"]["reply_s_role"]["title"][inter.locale],
                                    description=self.trans["commands"]["setup_start"]["reply_s_role"]["description"][inter.locale].format(emoji=config.dc_settings), colour=config.blurple)
                status_embed_h = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_h, reply], view=SetupSupporterView, attachments=[])
                
                SetupSupporterView.message = org
                await SetupSupporterView.wait()
                
                status_embed_i = await self.get_status_embed(inter)
                await org.edit(embed=status_embed_i, attachments=[])
                await asyncio.sleep(2)
            
            else:
                status_embed_j = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_j, embed_wait], attachments=[])
                await asyncio.sleep(2)     


            if language is None:

                setup__language__view_select = SetupLanguageSelect()
                
                reply = nextcord.Embed(title=self.trans["commands"]["setup_start"]["reply_l"]["title"][inter.locale],
                                    description=self.trans["commands"]["setup_start"]["reply_l"]["description"][inter.locale].format(emoji=config.dc_settings), colour=config.blurple)
                status_embed_k = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_k, reply], view=setup__language__view_select, attachments=[])
                
                setup__language__view_select.message = org
                await setup__language__view_select.wait()
                
                status_embed_l = await self.get_status_embed(inter)
                await org.edit(embed=status_embed_l, attachments=[])
                await asyncio.sleep(2)
            
            else:
                status_embed_m = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_m, embed_wait], attachments=[])
                await asyncio.sleep(2)     

                
            if global_channel is None:
                
                view_yn = Yes_OR_No()
                yn_embed = nextcord.Embed(title=self.trans["commands"]["setup_start"]["yn_embed"]["title"][inter.locale],
                                        description=self.trans["commands"]["setup_start"]["yn_embed"]["description"][inter.locale], colour=config.blurple)  
                
                status_embed_r = await self.get_status_embed(inter)                
                await org.edit(embeds=[status_embed_r, yn_embed], view=view_yn)
                
                view_yn.message = org
                await view_yn.wait()

                if view_yn.value is None:
                    pass
                
                elif view_yn.value:                    
                    SetupGlobalChannelSelect = global_text_select_channels(inter)
                    reply = nextcord.Embed(title=self.trans["commands"]["setup_start"]["reply_g"]["title"][inter.locale],
                                        description=self.trans["commands"]["setup_start"]["reply_g"]["description"][inter.locale].format(emoji=config.dc_settings), colour=config.blurple)
                    status_embed_s = await self.get_status_embed(inter)
                    await org.edit(embeds=[status_embed_s, reply], view=SetupGlobalChannelSelect, attachments=[])
                    
                    SetupGlobalChannelSelect.message = org
                    await SetupGlobalChannelSelect.wait()
                    
                    status_embed_t = await self.get_status_embed(inter)
                    await org.edit(embed=status_embed_t, attachments=[])
                    await asyncio.sleep(2)                    

            else:
                status_embed_u = await self.get_status_embed(inter)
                await org.edit(embeds=[status_embed_u, embed_wait], attachments=[])
                await asyncio.sleep(2)          
            
            done = nextcord.Embed(title=self.trans["commands"]["setup_start"]["done"]["title"][inter.locale],
                                description=self.trans["commands"]["setup_start"]["done"]["description"][inter.locale], colour=config.blurple)
            status_embed_v = await self.get_status_embed(inter)
            await org.edit(embeds=[status_embed_v, done], view=None)    

        else:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            not_owner = Embed(title="No authorization", description="You are not the owner of this server. Only the owner can execute this command!", colour=red)
            not_owner.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.send_message(embed=not_owner, ephemeral=True, file=cancel_error_png_a)
                 
#################################################################################################################            
#################################################################################################################
#################################################################################################################


    @setup.subcommand(name="global-chat", description="Settings for the GlobalChat",
                      name_localizations={Locale.en_US: "global-chat", Locale.de: "globaler-chat"},
                      description_localizations={Locale.en_US: "Settings for the GlobalChat", Locale.de: "Einstellungen für den Globalen Chat"})
    @perms_check.has_admin_perm_role()
    async def global_chat(self, inter: Interaction):

        s_input = "global_channel"
        s_object = "Global Chat"
        
        await inter.response.defer(ephemeral=True)

        #Check if Guild ID already used
        data_check = BotDB().query_server_table(inter.guild.id)

        #If the guild id is in use
        if data_check[0]:
            data_channel = BotDB().query_custom_one_slot(s_input, "server", inter.guild.id)
            
            #If global_channel already set test
            if data_channel[0]:
                channel = inter.guild.get_channel(data_channel[0])
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["global_chat"]["if_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["global_chat"]["if_r"]["description"][inter.locale].format(s_object=s_object, channel=channel.mention), colour=config.random_colour)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_setup_remove(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)
            

            #If global_channel is not set
            else:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["global_chat"]["else_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["global_chat"]["else_r"]["description"][inter.locale].format(s_object=s_object), colour=config.blurple)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_channel_select(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)


#################################################################################################################            
#################################################################################################################
#################################################################################################################

    @setup.subcommand(name="administrator-role", description="Settings for the highest permission role",
                      name_localizations={Locale.en_US: "administrator-role", Locale.de: "administrator-rolle"}, 
                      description_localizations={Locale.en_US: "Settings for the highest permission role", Locale.de: "Einstellungen für die Rolle mit der höchsten Berechtigung"})
    async def administrator_role(self, inter: Interaction):

        s_input = "admin_role"
        s_object = "Administrator Role"

        await inter.response.defer(ephemeral=True)

        #Check if Guild ID already used
        data_check = BotDB().query_server_table(inter.guild.id)
        #If the guild id is in use
        if data_check is not None:
            data_role = BotDB().query_custom_one_slot(s_input, "setup", inter.guild.id)
            
            #If admin_role already set test
            if data_role is not None:
                role = inter.guild.get_role(data_role[0])
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["administrator_role"]["if_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["administrator_role"]["if_r"]["description"][inter.locale].format(s_object=s_object, role=role.mention), colour=role.colour)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_setup_remove(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)
            

            #If admin_role is not set
            else:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["administrator_role"]["else_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["administrator_role"]["else_r"]["description"][inter.locale].format(s_object=s_object), colour=config.blurple)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_role_select(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)


#################################################################################################################            
#################################################################################################################
#################################################################################################################


    @setup.subcommand(name="moderator-role", description="Settings for the middlemost permission role",
                      name_localizations={Locale.en_US: "moderator-role", Locale.de: "moderations-rolle"}, 
                      description_localizations={Locale.en_US: "Settings for the middlemost permission role", Locale.de: "Einstellungen für die mittlere Berechtigungsrolle"})
    @perms_check.has_admin_perm_role()
    async def moderator_role(self, inter: Interaction):

        s_input = "moderator_role"
        s_object = "Moderation Role"
        
        await inter.response.defer(ephemeral=True)

        #Check if Guild ID already used
        data_check = BotDB().query_server_table(inter.guild.id)

        #If the guild id is in use
        if data_check is not None:
            data_role = BotDB().query_custom_one_slot(s_input, "setup", inter.guild.id)
            
            #If moderator_role already set test
            if data_role is not None:
                role = inter.guild.get_role(data_role[0])
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["moderator_role"]["if_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["moderator_role"]["if_r"]["description"][inter.locale].format(s_object=s_object, role=role.mention), colour=role.colour)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_setup_remove(s_input)
                await inter.edit_original_message(embed=r, iew=view, file=settings_png)
            

            #If moderator_role is not set
            else:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["moderator_role"]["else_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["moderator_role"]["else_r"]["description"][inter.locale].format(s_object=s_object), colour=config.blurple)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_role_select(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)

                                    
#################################################################################################################            
#################################################################################################################
#################################################################################################################


    @setup.subcommand(name="supporter-role", description="Settings for the lowest permission role",
                      name_localizations={Locale.en_US: "supporter-role", Locale.de: "supporter-rolle"}, 
                      description_localizations={Locale.en_US: "Settings for the lowest permission role", Locale.de: "Einstellungen für die niedrigste Berechtigungsrolle"})
    @perms_check.has_admin_perm_role()
    async def supporter_role(self, inter: Interaction):

        s_input = "supporter_role"
        s_object = "Supporter Role"
       
        await inter.response.defer(ephemeral=True)

        #Check if Guild ID already used
        data_check = BotDB().query_server_table(inter.guild.id)

        #If the guild id is in use
        if data_check is not None:
            data_role = BotDB().query_custom_one_slot(s_input, "setup", inter.guild.id)
            
            #If supporter_role already set test
            if data_role is not None:
                role = inter.guild.get_role(data_role[0])
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["supporter_role"]["if_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["supporter_role"]["if_r"]["description"][inter.locale].format(s_object=s_object, role=role.mention), colour=role.colour)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_setup_remove(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)
            

            #If supporter_role is not set
            else:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["supporter_role"]["else_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["supporter_role"]["else_r"]["description"][inter.locale].format(s_object=s_object), colour=config.blurple)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_role_select(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)


#################################################################################################################            
#################################################################################################################
#################################################################################################################




    @setup.subcommand(name="language", description="Settings for the bot language",
                      name_localizations={Locale.en_US: "language", Locale.de: "spraches"}, 
                      description_localizations={Locale.en_US: "Settings for the bot language", Locale.de: "Einstellungen für die Bot-Sprache"})
    @perms_check.has_admin_perm_role()
    async def language(self, inter: Interaction):

        s_input = "language"
        s_object = "Language"

        await inter.response.defer()

        #Check if Guild ID already used
        data_check = BotDB().query_server_table(inter.guild.id)

        #If the guild id is in use
        if data_check is not None:
            data_language = BotDB().query_custom_one_slot(s_input, "setup", inter.guild.id)
            
            #If language already set test
            if data_language is not None:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["language"]["if_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["language"]["if_r"]["title"][inter.locale].format(s_object=s_object, data_language=data_language[0]), colour=config.random_colour)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = universal_setup_remove(s_input)
                await inter.edit_original_message(embed=r, view=view, file=settings_png)
            

            #If language is not set
            else:
                settings_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
                
                r = Embed(title=self.trans["commands"]["language"]["else_r"]["title"][inter.locale].format(s_object=s_object),
                          description=self.trans["commands"]["language"]["else_r"]["description"][inter.locale].format(s_object=s_object), colour=config.blurple)
                
                r.set_thumbnail(url="attachment://changed-settings.png")
                view = language_add()
                await inter.edit_original_message(embed=r, view=view, file=settings_png)
                                     
#################################################################################################################            
#################################################################################################################
#################################################################################################################

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))