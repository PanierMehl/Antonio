import nextcord
from nextcord import Embed, Interaction
from nextcord.ext.commands import Context

import aiosqlite

import config
from mysql_class import BotDB


class universal_setup_remove(nextcord.ui.View):

    def __init__(self, s_input):
        self.s_input = s_input
        super().__init__(timeout=15)

    @nextcord.ui.button(label="Update", style=nextcord.ButtonStyle.green)
    async def update_button(self, button: nextcord.ui.Button, inter: Interaction):

        if self.s_input == "language":
            view = language_add()

        elif self.s_input == "admin_role":
            f_input = "admin_role"
            view = universal_role_select(f_input)

        elif self.s_input == "moderator_role":
            f_input = "moderator_role"
            view = universal_role_select(f_input)

        elif self.s_input == "supporter_role":
            f_input = "supporter_role"
            view = universal_role_select(f_input)    

        elif self.s_input == "global_channel":
            f_input = "global_channel"
            view = universal_channel_select(f_input)    

        await inter.response.edit_message(view=view)


    @nextcord.ui.button(label="Remove", style=nextcord.ButtonStyle.red)
    async def remove_button(self, button: nextcord.ui.Button, inter: Interaction):
        
        if self.s_input == "language":
            s_object = "Language"
        elif self.s_input == "admin_role":
            s_object = "Admin Role"
        elif self.s_input == "moderator_role":
            s_object = "Moderation Role"
        elif self.s_input == "supporter_role":
            s_object = "Supporter Role"
        elif self.s_input == "global_channel":
            s_object = "Global Chat"

        BotDB().update_custom_one_slot("server", self.s_input, None, inter.guild.id)

        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")

        r = Embed(title=f"Setup ➟ {s_object} removed ",description=f"The {s_object} has been successfully removed!", colour=config.green)
        r.set_thumbnail(url="attachment://check_mark_maja.png")

        button = self.children[0]
        button.disabled = True
        button.style = nextcord.ButtonStyle.grey

        await inter.response.edit_message(embed=r, file=check_mark_maja_png, view=None)

    async def on_timeout(self, inter: Interaction):
        b_u = self.children[0]
        b_r = self.children[1]
        b_u.disabled = True
        b_r.disabled = True
        await inter.response.edit_message(view=self)




class language_add(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=15)

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
        reply = nextcord.Embed(title="Language has been set", description=f"Your language is now \n"f"{selected_option}", colour=config.dark_green)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected {selected_option}"
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=None)
        self.stop()


    @nextcord.ui.button(label="Cancel action", style=nextcord.ButtonStyle.secondary)
    async def cancel_action(self, button: nextcord.ui.Button, inter: Interaction):
        await inter.delete_original_message()

    async def on_timeout(self, inter: Interaction):
        await inter.response.edit_message(view=self)



class universal_role_select(nextcord.ui.View):

    def __init__(self, s_input):
        self.s_input = s_input
        super().__init__(timeout=15)        
            
    @nextcord.ui.role_select(placeholder="Please choose a role", max_values=1, )
    async def on_select(self, select: nextcord.ui.RoleSelect, inter: Interaction):

        if self.s_input == "admin_role":
            s_object = "admin_role"
            name = "Admin Role"
        elif self.s_input == "moderator_role":
            s_object = "moderator_role"
            name = " Moderation Role"
        elif self.s_input == "supporter_role":
            s_object = "supporter_role"
            name = " Supporter Role"

        roles = select.values.roles
        for role in roles:
            pass

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_custom_one_slot("setup", s_object, inter.guild.id, role.id)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_custom_one_slot("setup", s_object, role.id, inter.guild.id)
        

        sel = self.children[0]
        but = self.children[1]
        sel.disabled = True
        but.disabled = True
        sel.placeholder = f"You selected @{role.name}"
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title=f"{name} has been set", description=f"The {name} is now \n"f"{role.mention}\n `{role.id}`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
        return
    

    @nextcord.ui.button(label="Cancel action", style=nextcord.ButtonStyle.secondary)
    async def cancel_action(self, button: nextcord.ui.Button, inter: Interaction):
        await inter.delete_original_message()


    async def on_timeout(self, inter: Interaction):
        await inter.response.edit_message(view=self)




class universal_channel_select(nextcord.ui.View):

    def __init__(self, s_input):
        self.s_input = s_input
        super().__init__(timeout=15)           
    
    @nextcord.ui.channel_select(channel_types=[nextcord.ChannelType.text], max_values=1, placeholder="Please choose one channel")  
    async def on_select(self, select: nextcord.ui.ChannelSelect, inter: nextcord.Interaction):
        channels = select.values.channels
        for channel in channels:
            pass
        
        if self.s_input == "global_channel":
            s_object = "global_channel"
            name = "Global Chat"

        data = BotDB().query_server_table(inter.guild.id)
        
        if data is None:
            BotDB().insert_custom_one_slot("server", s_object, inter.guild.id, channel.id)
            
        if data is not None:
            if inter.guild.id in data:
                BotDB().update_custom_one_slot("server", s_object, channel.id, inter.guild.id)
    
        sel = self.children[0]
        but = self.children[1]
        sel.disabled = True
        but.disabled = True
        sel.placeholder = f"You selected @{channel.name}"
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title=f"{name} has been set", description=f"The {name} is now \n"f"{channel.mention}\n `{channel.id}`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
        return
    

    @nextcord.ui.button(label="Cancel action", style=nextcord.ButtonStyle.secondary)
    async def cancel_action(self, button: nextcord.ui.Button, inter: Interaction):
        await inter.delete_original_message()


    async def on_timeout(self, inter: Interaction):
        await inter.response.edit_message(view=self)

        