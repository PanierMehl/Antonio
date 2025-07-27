import aiosqlite
import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Context

import config
from mysql_class import BotDB


#ADMIN-ROLE 
class SetupAdminRoleSelect(nextcord.ui.View):
    def __init__(self, ctx_or_interaction, *, timeout=45):
        super().__init__(timeout=timeout)
        
        self.ctx_or_interaction = ctx_or_interaction
        if isinstance(ctx_or_interaction, Context):
            self.user = ctx_or_interaction.author
        if isinstance(ctx_or_interaction, Interaction):
            self.user = ctx_or_interaction.user
        
        
    async def interaction_check(self, interaction):
            
        if self.user == interaction.user:
            return True
        else:
            await interaction.response.send_message(content="You are not allow to select the channel!")
    
    
    @nextcord.ui.role_select(placeholder="Please choose a role", max_values=1)
    async def on_select(self, select: nextcord.ui.RoleSelect, inter: nextcord.Interaction):
        roles = select.values.roles
        for role in roles:
            pass
                
        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_administrator_role(inter.guild.id, role.id)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_administrator_role(role.id, inter.guild.id)
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected @{role.name}"
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title="Admin role has been set", description=f"The Admin Role is now \n"f"{role.mention}\n `{role.id}`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
    
    async def on_timeout(self):
        try:
            eb = self.children[0]
            eb.disabled = True
            await self.message.edit(view=self)
            await self.message.delete(delay=5)   
        except:
            return
        
#################################################################################################################                  
#################################################################################################################
#################################################################################################################             

#MODERATION-ROLE       
class SetupModerationRoleSelect(nextcord.ui.View):
    def __init__(self, *, timeout=45):
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, inter: nextcord.Interaction):

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            if self.user == inter.user:
                return True
            else:
                await inter.response.send_message(content="You are not allowed to select the channel!")
                return False
        
        admin_role = inter.guild.get_role(int(data[1])) if data[1] is not None else None
        if admin_role and inter.user.get_role(admin_role.id):
            return True
        
        elif self.user == inter.user:
            return True
        
        else:
            await inter.response.send_message(content="You are not allowed to select the channel!")
            return False
                            
                        
    
    @nextcord.ui.role_select(placeholder="Please choose a role", max_values=1)
    async def on_select(self, select: nextcord.ui.RoleSelect, inter: nextcord.Interaction):
        roles = select.values.roles
        for role in roles:
            pass

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_moderator_role(inter.guild.id, role.id)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_moderator_role(role.id, inter.guild.id)
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected @{role.name}"
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title="Moderator role has been set", description=f"The Moderator Role is now \n"f"{role.mention}\n `{role.id}`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
    
    async def on_timeout(self):
        try:
            eb = self.children[0]
            eb.disabled = True
            await self.message.edit(view=self)
            await self.message.delete(delay=5)   
        except:
            return   
                

#################################################################################################################                  
#################################################################################################################
#################################################################################################################             

#SUPPORTER-ROLE       
class SetupSupporterRoleSelect(nextcord.ui.View):
    
    def __init__(self, *, timeout=45):
        super().__init__(timeout=timeout)
        
        
    async def interaction_check(self, inter: nextcord.Interaction):

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            if self.user == inter.user:
                return True
            else:
                await inter.response.send_message(content="You are not allowed to select the channel!")
                return False
        

        admin_role_id, moderator_role_id = data[1], data[2]
        if admin_role_id:
            admin_role = inter.guild.get_role(admin_role_id)
        if moderator_role_id:
            moderator_role = inter.guild.get_role(moderator_role_id)

        if admin_role and inter.user.get_role(admin_role.id):
            return True
        elif moderator_role and inter.user.get_role(moderator_role.id):
            return True

        elif self.user == inter.user:
            return True
        else:
            await inter.response.send_message(content="You are not allowed to select the channel!")
            return False
                        
                        

    
    @nextcord.ui.role_select(placeholder="Please choose a role", max_values=1)
    async def on_select(self, select: nextcord.ui.RoleSelect, inter: nextcord.Interaction):
        roles = select.values.roles
        for role in roles:
            pass
        
        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_supporter_role(inter.guild.id, role.id)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_supporter_role(role.id, inter.guild.id)
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected @{role.name}"
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title="Supporter role has been set", description=f"The Supporter Role is now \n"f"{role.mention}\n `{role.id}`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
    
    async def on_timeout(self):
        try:
            eb = self.children[0]
            eb.disabled = True
            await self.message.edit(view=self)
            await self.message.delete(delay=5)   
        except:
            return  
        
        
#################################################################################################################                  
#################################################################################################################
#################################################################################################################           
        
#LANGUAGE   
class SetupLanguageSelect(nextcord.ui.View):
    
    def __init__(self):
        super().__init__()


    options = [
    nextcord.SelectOption(label="German", description="This bot will reply in German", emoji=config.flag_de, value="German"),
    nextcord.SelectOption(label="English", description="This bot will reply in English", emoji=config.flag_us, value="English"),
    ]
                
    @nextcord.ui.string_select(placeholder="Please select an language", max_values=1, options=options)
    async def on_select(self, select: nextcord.ui.StringSelect, inter: nextcord.Interaction):
        
        selected_option = select.values[0]

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_language(inter.guild.id, selected_option)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_language(selected_option, inter.guild.id)
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title="Language has been set", description=f"Your language is now \n"f"{selected_option}", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected {selected_option}"
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
    



