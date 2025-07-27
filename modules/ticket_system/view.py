import random
import string
import asyncio 

import nextcord as nc
from nextcord import Embed, Interaction, File

import config
from mysql_class import BotDB

import chat_exporter
import io
import datetime
import yaml
import config

def generate_random_id(length):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))

class SetupTicket_en(nc.ui.Modal):
    def __init__(self):
        super().__init__(f"Create new Ticketsystem")
        self.header = nc.ui.TextInput(label="Header", style=nc.TextInputStyle.short, max_length=50, required=True, placeholder="Exp: Support Ticket")
        self.textbox = nc.ui.TextInput(label="Textbox", style=nc.TextInputStyle.paragraph, max_length=2500, required=True, placeholder="Exp: If you would like to contact a staff please open a Ticket.")
        self.button_one_label = nc.ui.TextInput(label="Button 1 (Blue)", style=nc.TextInputStyle.short, max_length=50, required=True, placeholder="Contact Staff")
        self.button_two_label = nc.ui.TextInput(label="Button 2 (Red)", style=nc.TextInputStyle.short, max_length=50, required=False, placeholder="Report Member")
        self.button_three_label = nc.ui.TextInput(label="Button 3 (Green)", style=nc.TextInputStyle.short, max_length=50, required=False, placeholder="Other")
 
        self.add_item(self.header)
        self.add_item(self.textbox)
        self.add_item(self.button_one_label)
        self.add_item(self.button_two_label)
        self.add_item(self.button_three_label)

 
    async def callback(self, inter: Interaction):
 
        embed_create = Embed(title=self.header.value, description=self.textbox.value, colour=config.blurple)
        re = await inter.response.send_message(embed=embed_create)
        c_re = await re.fetch()
        f_re = c_re.id
        channel = inter.channel.id
        category = inter.channel.category.id
 
        if self.button_one_label.value:
            if not self.button_two_label.value and not self.button_three_label.value:
                b_one_id = generate_random_id(8)
                view = TicketMain_One_V2(self.button_one_label.value, f_re, b_one_id)
                await inter.edit_original_message(view=view) 
                BotDB().insert_ticket_system(f_re, "1", inter.guild_id, channel, category, self.button_one_label.value, None, None, b_one_id, None, None)

            elif self.button_two_label.value:
                if not self.button_three_label.value:
                    b_one_id = generate_random_id(8)
                    b_two_id = generate_random_id(8)
                    view = TicketMain_Two_V2(self.button_one_label.value, self.button_two_label.value, f_re, b_one_id, b_two_id)
                    await inter.edit_original_message(view=view)
                    BotDB().insert_ticket_system(f_re, "2", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, None, b_one_id, b_two_id, None)

                else:
                    b_one_id = generate_random_id(8)
                    b_two_id = generate_random_id(8)
                    b_three_id = generate_random_id(8)
                    view = TicketMain_Three_V2(self.button_one_label.value, self.button_two_label.value, self.button_three_label.value, f_re, b_one_id, b_two_id, b_three_id)
                    await inter.edit_original_message(view=view) 
                    BotDB().insert_ticket_system(f_re, "3", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, self.button_three_label.value, b_one_id, b_two_id, b_three_id)

            
            elif self.button_three_label.value:
                b_one_id = generate_random_id(8)
                b_two_id = generate_random_id(8)
                view = TicketMain_Two_V2(self.button_one_label.value, self.button_two_label.value, f_re, b_one_id, b_two_id)
                await inter.edit_original_message(view=view)
                BotDB().insert_ticket_system(f_re, "2", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, None, b_one_id, b_two_id, None)

class SetupTicket_de(nc.ui.Modal):
    def __init__(self):
        super().__init__(f"Erstelle ein neues Ticketsystem")
        self.header = nc.ui.TextInput(label="Kopfzeile", style=nc.TextInputStyle.short, max_length=50, required=True, placeholder="Beispiel: Support Ticket")
        self.textbox = nc.ui.TextInput(label="Textbox", style=nc.TextInputStyle.paragraph, max_length=2500, required=True, placeholder="Beispiel: Wenn du ein Teammitglied erreichen möchtest, dann öffne bitte ein Ticket.")
        self.button_one_label = nc.ui.TextInput(label="Option 1 (Blau)", style=nc.TextInputStyle.short, max_length=50, required=True, placeholder="Teammitglieder kontaktiere")
        self.button_two_label = nc.ui.TextInput(label="Option 2 (Rot)", style=nc.TextInputStyle.short, max_length=50, required=False, placeholder="Mitglied melden")
        self.button_three_label = nc.ui.TextInput(label="Option 3 (Grün)", style=nc.TextInputStyle.short, max_length=50, required=False, placeholder="Sonstiges")
 
        self.add_item(self.header)
        self.add_item(self.textbox)
        self.add_item(self.button_one_label)
        self.add_item(self.button_two_label)
        self.add_item(self.button_three_label)

 
    async def callback(self, inter: Interaction):
 
        embed_create = Embed(title=self.header.value, description=self.textbox.value, colour=config.blurple)
        re = await inter.response.send_message(embed=embed_create)
        c_re = await re.fetch()
        f_re = c_re.id
        channel = inter.channel.id
        category = inter.channel.category.id
 
        if self.button_one_label.value:
            if not self.button_two_label.value and not self.button_three_label.value:
                b_one_id = generate_random_id(8)
                view = TicketMain_One_V2(self.button_one_label.value, f_re, b_one_id)
                await inter.edit_original_message(view=view) 
                BotDB().insert_ticket_system(f_re, "1", inter.guild_id, channel, category, self.button_one_label.value, None, None, b_one_id, None, None)

            elif self.button_two_label.value:
                if not self.button_three_label.value:
                    b_one_id = generate_random_id(8)
                    b_two_id = generate_random_id(8)
                    view = TicketMain_Two_V2(self.button_one_label.value, self.button_two_label.value, f_re, b_one_id, b_two_id)
                    await inter.edit_original_message(view=view)
                    BotDB().insert_ticket_system(f_re, "2", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, None, b_one_id, b_two_id, None)

                else:
                    b_one_id = generate_random_id(8)
                    b_two_id = generate_random_id(8)
                    b_three_id = generate_random_id(8)
                    view = TicketMain_Three_V2(self.button_one_label.value, self.button_two_label.value, self.button_three_label.value, f_re, b_one_id, b_two_id, b_three_id)
                    await inter.edit_original_message(view=view) 
                    BotDB().insert_ticket_system(f_re, "3", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, self.button_three_label.value, b_one_id, b_two_id, b_three_id)

            
            elif self.button_three_label.value:
                b_one_id = generate_random_id(8)
                b_two_id = generate_random_id(8)
                view = TicketMain_Two_V2(self.button_one_label.value, self.button_two_label.value, f_re, b_one_id, b_two_id)
                await inter.edit_original_message(view=view)
                BotDB().insert_ticket_system(f_re, "2", inter.guild_id, channel, category, self.button_one_label.value, self.button_two_label.value, None, b_one_id, b_two_id, None)


def generate_random_id(length):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))

class TicketMain_One_V2(nc.ui.View):
    def __init__(self, label_one, message_id, b_one_id):
        super().__init__(timeout=None)
        self.b_one.label = label_one
        self.b_one.custom_id = str(b_one_id)
        self.message_id = message_id
    
    async def check_if_ticket_is_already_open(self, inter: Interaction):
        ticket_check = BotDB().query_tickets_by_user(inter.guild.id, inter.user.id)
        if not ticket_check:
            return None
        else:
            return ticket_check[0]

    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)

    @nc.ui.button(style=nc.ButtonStyle.blurple)
    async def b_one(self, button: nc.ui.Button, inter: Interaction):
        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)
            
            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["description"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")
    

################################################################################

class TicketMain_Two_V2(nc.ui.View):
    def __init__(self, label_one, label_two, message_id, b_one_id, b_two_id):
        super().__init__(timeout=None)
        self.b_one.label = label_one
        self.b_one.custom_id = str(b_one_id)
        self.b_two.label = label_two
        self.b_two.custom_id = str(b_two_id)
        self.message_id = message_id
    
    async def check_if_ticket_is_already_open(self, inter: Interaction):
        ticket_check = BotDB().query_tickets_by_user(inter.guild.id, inter.user.id)
        if not ticket_check:
            return None
        else:
            return ticket_check[0]
    
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
    @nc.ui.button(style=nc.ButtonStyle.blurple)
    async def b_one(self, button: nc.ui.Button, inter: Interaction):

        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)
            
            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")

            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["description"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")

    ############################################################################################################################################

    @nc.ui.button(style=nc.ButtonStyle.red)
    async def b_two(self, button: nc.ui.Button, inter: Interaction):

        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)

            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")

            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["description"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")

################################################################################

class TicketMain_Three_V2(nc.ui.View):
    def __init__(self, label_one, label_two, label_three, message_id, b_one_id, b_two_id, b_three_id):
        super().__init__(timeout=None)
        self.b_one.label = label_one
        self.b_one.custom_id = str(b_one_id)
        self.b_two.label = label_two
        self.b_two.custom_id = str(b_two_id)
        self.b_three.label = label_three
        self.b_three.custom_id = str(b_three_id)
        self.message_id = message_id
    
    async def check_if_ticket_is_already_open(self, inter: Interaction):
        ticket_check = BotDB().query_tickets_by_user(inter.guild.id, inter.user.id)
        if not ticket_check:
            return None
        else:
            return ticket_check[0]
    
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
    ############################################################################################################################################

    @nc.ui.button(style=nc.ButtonStyle.blurple)
    async def b_one(self, button: nc.ui.Button, inter: Interaction):

        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)

            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
                
            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["description"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")

    ############################################################################################################################################

    @nc.ui.button(style=nc.ButtonStyle.red)
    async def b_two(self, button: nc.ui.Button, inter: Interaction):

        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)

            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")

            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")

    ############################################################################################################################################

    @nc.ui.button(style=nc.ButtonStyle.green)
    async def b_three(self, button: nc.ui.Button, inter: Interaction):
        
        msg = await inter.response.send_message(content=self.trans["view"]["ticket"]["wait_msg"][inter.locale].format(emoji=config.e_loading),
                                                ephemeral=True)
        
        if await self.check_if_ticket_is_already_open(inter) is None:
            roles = BotDB().query_server_table(inter.guild.id)
            if roles:
                admin_role_id, moderator_role_id, supporter_role_id = roles[1], roles[2], roles[3]
                if admin_role_id:
                    admin_role = inter.guild.get_role(admin_role_id)
                if moderator_role_id:
                    moderator_role = inter.guild.get_role(moderator_role_id)
                if supporter_role_id:
                    supporter_role = inter.guild.get_role(supporter_role_id)

            overwirtes = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                inter.user: nc.PermissionOverwrite(read_messages=True),
                admin_role: nc.PermissionOverwrite(read_messages=True),
                moderator_role: nc.PermissionOverwrite(read_messages=True),
                supporter_role: nc.PermissionOverwrite(read_messages=True)
            }

            create = await inter.guild.create_text_channel(name=f"{button.label}-{inter.user.name}", reason="Ticket opened", position=1,
                                                            topic=f"Please take care of pinned messages!",
                                                                category=inter.channel.category, overwrites=overwirtes)
            
            info = Embed(title=self.trans["view"]["ticket"]["info"]["title"][inter.locale].format(emoji=config.a_support, id=create.id, label=button.label),
                         description=self.trans["view"]["ticket"]["info"]["description"][inter.locale].format(user=inter.user.name), colour=config.blurple)

            if inter.locale == "de":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_de(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            elif inter.locale == "en_US":
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")
            else:
                pin = await create.send(content=inter.user.mention, embed=info, view=Ticket_Options_en(self.message_id))
                await pin.pin(reason="Ticket Info Message")

            BotDB().insert_ticket(create.id, inter.guild.id, inter.user.id, config.aktuelldatum, None)

            cc = Embed(title=self.trans["view"]["ticket"]["cc"]["title"][inter.locale].format(emoji=config.a_support, create=create.id, tic=config.a_tic, mention=create.mention), colour=config.green)
            await msg.edit(embed=cc, content="")

        else:
            er = Embed(title=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(emoji=config.a_cross),
                       description=self.trans["view"]["ticket"]["er"]["title"][inter.locale].format(guild=inter.guild.id, fkt={await self.check_if_ticket_is_already_open(inter)}),
                       colour=config.red)
            await msg.edit(embed=er, content="")



class TicketSystem_Del_en(nc.ui.View):
    def __init__(self, guild_id, message_id, channel_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.message_id = message_id
        self.channel_id = channel_id

        url = f'https://discord.com/channels/{self.guild_id}/{self.channel_id}/{self.message_id}'

        self.add_item(nc.ui.Button(style=nc.ButtonStyle.link, label="Jump to!", url=url))

    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
    @nc.ui.button(style=nc.ButtonStyle.red, label="Remove it!", emoji=config.a_trash)
    async def ts_delete(self, button: nc.ui.Button, inter: Interaction):
        
        load = Embed(title=self.trans["view"]["ts_delete"]["load"][inter.locale].format(emoji=config.e_loading), colour=config.blue)
        await inter.response.send_message(embed=load, ephemeral=True)
        
        BotDB().delete_ticket_system(self.guild_id, self.message_id)
        button.disabled = True
        
        org_c = inter.guild.get_channel(self.channel_id)
        try:
            org_m = await org_c.fetch_message(self.message_id)
            await org_m.delete()
        except:
            pass

        confirm = Embed(title=self.trans["view"]["ts_delete"]["confirm"]["title"][inter.locale].format(emoji=config.confirm),
                        description=self.trans["view"]["ts_delete"]["confirm"]["description"][inter.locale],
                        colour=config.green)
        
        await inter.edit_original_message(view=self, embed=confirm)


class TicketSystem_Del_de(nc.ui.View):
    def __init__(self, guild_id, message_id, channel_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.message_id = message_id
        self.channel_id = channel_id

        url = f'https://discord.com/channels/{self.guild_id}/{self.channel_id}/{self.message_id}'

        self.add_item(nc.ui.Button(style=nc.ButtonStyle.link, label="Bring mich hin!", url=url))

    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)
        
    @nc.ui.button(style=nc.ButtonStyle.red, label="Enteferne es", emoji=config.a_trash)
    async def ts_delete(self, button: nc.ui.Button, inter: Interaction):
        
        load = Embed(title=self.trans["view"]["ts_delete"]["load"][inter.locale].format(emoji=config.e_loading), colour=config.blue)
        await inter.response.send_message(embed=load, ephemeral=True)
        
        BotDB().delete_ticket_system(self.guild_id, self.message_id)
        button.disabled = True
        
        org_c = inter.guild.get_channel(self.channel_id)
        try:
            org_m = await org_c.fetch_message(self.message_id)
            await org_m.delete()
        except:
            pass

        confirm = Embed(title=self.trans["view"]["ts_delete"]["confirm"]["title"][inter.locale].format(emoji=config.confirm),
                        description=self.trans["view"]["ts_delete"]["confirm"]["description"][inter.locale],
                        colour=config.green)
        
        await inter.edit_original_message(view=self, embed=confirm)
        
        
class Ticket_Options_en(nc.ui.View):
    def __init__(self, message_id):
        super().__init__(timeout=None)
        self.message_id = message_id
        
        for item in self.children:
            if isinstance(item, nc.ui.Button) and item.label == "Close Ticket":
                item.custom_id = str(message_id)
                break

    async def check_staff_permissions(self, inter: Interaction):
        roles_data = BotDB().query_server_table(inter.guild.id)
        if roles_data:
            admin_role_id = roles_data[1]
            moderator_role_id = roles_data[2]
            supporter_role_id = roles_data[3]

            admin_role = inter.guild.get_role(admin_role_id)
            moderator_role = inter.guild.get_role(moderator_role_id)
            supporter_role = inter.guild.get_role(supporter_role_id)
            
            staff_roles = [role for role in (admin_role, moderator_role, supporter_role) if role is not None]
            
            if any(role in inter.user.roles for role in staff_roles):
                return True
        return False



    @nc.ui.button(label="Open Ticket", style=nc.ButtonStyle.green, row=1, emoji=config.a_unlock, disabled=True)
    async def open_ticket(self, button: nc.ui.Button, inter: Interaction):
        if await self.check_staff_permissions(inter):
            ticket_query = BotDB().query_ticket_informations(inter.channel.id)
            if not ticket_query:
                err = Embed(title=f"Ticket infotmation not found in database {config.a_cross}", colour=config.red)
                await inter.response.send_message(embed=err)
                return
            
            o = Embed(title=f"Ticket is opened {config.e_loading}", colour=config.blue)
            await inter.response.send_message(embed=o)
            
            user_id = ticket_query[0]
            get_user = inter.guild.get_member(user_id)

            if not get_user:
                err = Embed(title=f"Ticket owner not found in this guild {config.a_cross}", colour=config.red)
                await inter.response.send_message(embed=err, ephemeral=True)
                return

            overwrites = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                get_user: nc.PermissionOverwrite(read_messages=True),
            }
            
            self.open_ticket.disabled = True
            self.delete_ticket.disabled = True
            self.close_ticket.disabled = False
            
            await inter.channel.edit(overwrites=overwrites, reason="Opening Ticket")

            message = await inter.channel.fetch_message(inter.message.id)
            await message.edit(view=self)
            
            info = Embed(description=f"{config.a_unlock} {inter.user.mention} has opened this Ticket.", colour=config.green)
            await inter.edit_original_message(embed=info)
        else:
            perm = Embed(title=f"This Button is only for staff members {config.a_leave}", colour=config.red)
            await inter.edit_original_message(emebd=perm)



    @nc.ui.button(label="Close Ticket", style=nc.ButtonStyle.red, row=1, emoji=config.a_lock)
    async def close_ticket(self, button: nc.ui.Button, inter: Interaction):

        if await self.check_staff_permissions(inter):
            ticket_query = BotDB().query_ticket_informations(inter.channel.id)
            if not ticket_query:
                await inter.response.send_message(content="Ticket information not found in database.")
                return
            
            i = Embed(title=f"Ticket is closing {config.e_loading}", colour=config.blue)
            await inter.response.send_message(embed=i)

            user_id = ticket_query[0]
            get_user = inter.guild.get_member(user_id)

            overwrites = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                get_user: nc.PermissionOverwrite(read_messages=False),
            }
            
            self.open_ticket.disabled = False
            self.delete_ticket.disabled = False
            self.close_ticket.disabled = True
            
            await inter.channel.edit(overwrites=overwrites, reason="Closing Ticket")

            message = await inter.channel.fetch_message(inter.message.id)
            await message.edit(view=self)
            
            info = Embed(description=f"{config.a_lock} {inter.user.mention} has closed this Ticket. The ticket can now be deleted or reopened.", colour=config.red)
            await inter.edit_original_message(embed=info)
        
        else:
            await inter.edit_original_message(content="This Button is only for staff members!")



    @nc.ui.button(label="Delete Ticket", style=nc.ButtonStyle.red, row=1, disabled=True, emoji=config.a_trash)
    async def delete_ticket(self, button: nc.ui.Button, inter: Interaction):
        if not await self.check_staff_permissions(inter):
            await inter.response.send_message(content="This Button is only for staff members!", ephemeral=True)
            return

        info_initial = Embed(
            title="Ticket deletion requested!",
            description=f"Please wait a moment...\n\nTranscript sending {config.e_loading}\nTicket removed from database {config.e_loading}\nChannel deletion {config.e_loading}",
            colour=config.blurple
        )
        
        await inter.response.send_message(embed=info_initial, ephemeral=True)

        transcript_succeeded = True
        failed_dm_members = []

        try:
            message_count = await inter.channel.history(limit=None).flatten()
            messages_to_export = len(message_count) + 3
            transcript = await chat_exporter.export(
                inter.channel,
                limit=messages_to_export,
                bot=inter.client,
                tz_info="Europe/Berlin"
            )
            transcript_data = io.BytesIO(transcript.encode("utf-8"))
            
            text_members = inter.channel.members
            for member in text_members:
                if member.bot:
                    continue

                transcript_data.seek(0)
                file = File(transcript_data, filename=f"{inter.channel.name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.html")
                
                try:
                    await member.send(file=file)
                except nc.Forbidden:
                    failed_dm_members.append(member.mention)
                    transcript_succeeded = False
                except Exception as e:
                    print(f"Error sending transcript to {member.name} ({member.id}): {e}")
                    failed_dm_members.append(member.mention)
                    transcript_succeeded = False
            
            transcript_status_emoji = config.a_tic if transcript_succeeded else config.a_cross
            
            updated_info_transcript = Embed(
                title="Ticket deletion requested!",
                description=f"Please wait a moment...\n\nTranscript sent {transcript_status_emoji}\nTicket removed from database {config.e_loading}\nChannel deletion {config.e_loading}",
                colour=config.blurple
            )
            await inter.edit_original_response(embed=updated_info_transcript)

            if failed_dm_members:
                await inter.followup.send(
                    f"⚠️ Could not send transcript to the following members (DMs closed/Error): {', '.join(failed_dm_members)}",
                    ephemeral=True
                )

        except Exception as e:
            print(f"Error creating or sending transcript: {e}")
            transcript_succeeded = False
            error_embed = Embed(
                title="Ticket deletion failed!",
                description=f"An error occurred while creating or sending the transcript: {config.a_cross}\nPlease try again or contact the bot developer.",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)
            return

        await asyncio.sleep(2)

        db_succeeded = True
        try:
            BotDB().delete_ticket(inter.channel.id, inter.guild.id)
        except Exception as e:
            print(f"Error deleting ticket from database: {e}")
            db_succeeded = False
        
        db_status_emoji = config.a_tic if db_succeeded else config.a_cross
        updated_info_db = Embed(
            title="Ticket deletion requested!",
            description=f"Please wait a moment...\n\nTranscript sent {transcript_status_emoji}\nTicket removed from database {db_status_emoji}\nChannel deletion {config.e_loading}",
            colour=config.blurple
        )
        await inter.edit_original_response(embed=updated_info_db)
        await asyncio.sleep(2)

        self.open_ticket.disabled = True
        self.close_ticket.disabled = True
        button.disabled = True
        
        try:
            message_to_edit = await inter.channel.fetch_message(self.message_id)
            await message_to_edit.edit(view=self)
        except nc.NotFound:
            print("The message with the ticket button was not found.")
        except Exception as e:
            print(f"Error updating the ticket message view: {e}")

        channel_deleted_successfully = False
        try:
            await inter.edit_original_response(
                embed=Embed(
                    title="Ticket deletion requested!",
                    description=f"Please wait a moment...\n\nTranscript sent {transcript_status_emoji}\nTicket removed from database {db_status_emoji}\nChannel deletion {config.e_loading}",
                    colour=config.blurple
                )
            )
            await asyncio.sleep(1)
            await inter.channel.delete()
            channel_deleted_successfully = True
        except nc.Forbidden:
            error_embed = Embed(
                title="Ticket deletion failed!",
                description=f"Channel could not be deleted: Missing permissions. {config.a_cross}",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)
        except Exception as e:
            print(f"Error deleting channel {inter.channel.id}: {e}")
            error_embed = Embed(
                title="Ticket deletion failed!",
                description=f"An unexpected error occurred while deleting the channel: {config.a_cross}",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)


class Ticket_Options_de(nc.ui.View):
    def __init__(self, message_id):
        super().__init__(timeout=None)
        self.message_id = message_id
        
        for item in self.children:
            if isinstance(item, nc.ui.Button) and item.label == "Ticket schließen":
                item.custom_id = str(message_id)
                break

    async def check_staff_permissions(self, inter: Interaction):
        roles_data = BotDB().query_server_table(inter.guild.id)
        if roles_data:
            admin_role_id = roles_data[1]
            moderator_role_id = roles_data[2]
            supporter_role_id = roles_data[3]

            admin_role = inter.guild.get_role(admin_role_id)
            moderator_role = inter.guild.get_role(moderator_role_id)
            supporter_role = inter.guild.get_role(supporter_role_id)
            
            staff_roles = [role for role in (admin_role, moderator_role, supporter_role) if role is not None]
            
            if any(role in inter.user.roles for role in staff_roles):
                return True
        return False



    @nc.ui.button(label="Ticket öffnen", style=nc.ButtonStyle.green, row=1, emoji=config.a_unlock, disabled=True)
    async def open_ticket(self, button: nc.ui.Button, inter: Interaction):
        
        if await self.check_staff_permissions(inter):
            ticket_query = BotDB().query_ticket_informations(inter.channel.id)
            if not ticket_query:
                await inter.response.send_message("Ticket-Informationen nicht in der Datenbank gefunden.", ephemeral=True)
                return

            await inter.response.defer(with_message=f"Ticket wird geöffnet {config.e_loading}")
        
            user_id = ticket_query[0]
            get_user = inter.guild.get_member(user_id)

            if not get_user:
                await inter.response.send_message("Ticket-Besitzer nicht auf diesem Server gefunden.", ephemeral=True)
                return

            overwrites = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                get_user: nc.PermissionOverwrite(read_messages=True),
            }
            
            self.open_ticket.disabled = True
            self.delete_ticket.disabled = True
            self.close_ticket.disabled = False
            
            await inter.channel.edit(overwrites=overwrites, reason="Ticket wird geöffnet")

            message = await inter.channel.fetch_message(inter.message.id)
            await message.edit(view=self)
            
            info = Embed(description=f"{config.a_unlock} {inter.user.mention} hat dieses Ticket geöffnet.", colour=config.green)
            await inter.edit_original_message(embed=info, ephemeral=True)
        else:
            await inter.edit_original_message(content="Dieser Button ist nur für Teammitglieder!", ephemeral=True)



    @nc.ui.button(label="Ticket schließen", style=nc.ButtonStyle.red, row=1, emoji=config.a_lock)
    async def close_ticket(self, button: nc.ui.Button, inter: Interaction):

        if await self.check_staff_permissions(inter):
            ticket_query = BotDB().query_ticket_informations(inter.channel.id)
            if not ticket_query:
                await inter.edit_original_message(content="Ticket-Informationen nicht in der Datenbank gefunden.")
                return
            
            await inter.response.defer(with_message=f"Ticket wird geschlossen {config.e_loading}")
        
            user_id = ticket_query[0]
            get_user = inter.guild.get_member(user_id)

            overwrites = {
                inter.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                get_user: nc.PermissionOverwrite(read_messages=False),
            }
            
            self.open_ticket.disabled = False
            self.delete_ticket.disabled = False
            self.close_ticket.disabled = True
            
            await inter.channel.edit(overwrites=overwrites, reason="Ticket wird geschlossen")

            message = await inter.channel.fetch_message(inter.message.id)
            await message.edit(view=self)
            
            info = Embed(description=f"{config.a_lock} {inter.user.mention} hat dieses Ticket geschlossen. Das Ticket kann nun gelöscht oder wieder geöffnet werden.", colour=config.red)
            await inter.edit_original_message(embed=info)
        else:
            await inter.edit_original_message(content="Dieser Button ist nur für Teammitglieder!")



    @nc.ui.button(label="Ticket löschen", style=nc.ButtonStyle.red, row=1, disabled=True, emoji=config.a_trash)
    async def delete_ticket(self, button: nc.ui.Button, inter: Interaction):
        if not await self.check_staff_permissions(inter):
            await inter.response.send_message(content="Dieser Button ist nur für Teammitglieder!", ephemeral=True)
            return

        info_initial = Embed(
            title="Ticket-Löschung angefordert!",
            description=f"Bitte warten Sie einen Moment...\n\nTranskript wird gesendet {config.e_loading}\nTicket aus Datenbank entfernt {config.e_loading}\nKanal-Löschung {config.e_loading}",
            colour=config.blurple
        )
        
        await inter.response.send_message(embed=info_initial)

        transcript_succeeded = True
        failed_dm_members = []

        try:
            message_count = await inter.channel.history(limit=None).flatten()
            messages_to_export = len(message_count) + 3
            transcript = await chat_exporter.export(
                inter.channel,
                limit=messages_to_export,
                bot=inter.client,
                tz_info="Europe/Berlin"
            )
            transcript_data = io.BytesIO(transcript.encode("utf-8"))
            
            text_members = inter.channel.members
            for member in text_members:
                if member.bot:
                    continue

                transcript_data.seek(0)
                file = File(transcript_data, filename=f"{inter.channel.name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.html")
                
                try:
                    await member.send(file=file)
                except nc.Forbidden:
                    failed_dm_members.append(member.mention)
                    transcript_succeeded = False
                except Exception as e:
                    print(f"Fehler beim Senden des Transkripts an {member.name} ({member.id}): {e}")
                    failed_dm_members.append(member.mention)
                    transcript_succeeded = False
            
            transcript_status_emoji = config.a_tic if transcript_succeeded else config.a_cross
            
            updated_info_transcript = Embed(
                title="Ticket-Löschung angefordert!",
                description=f"Bitte warten Sie einen Moment...\n\nTranskript gesendet {transcript_status_emoji}\nTicket aus Datenbank entfernt {config.e_loading}\nKanal-Löschung {config.e_loading}",
                colour=config.blurple
            )
            await inter.edit_original_response(embed=updated_info_transcript)

            if failed_dm_members:
                await inter.followup.send(
                    f"⚠️ Konnte Transkript nicht an folgende Mitglieder senden (DMs geschlossen/Fehler): {', '.join(failed_dm_members)}",
                    ephemeral=True
                )

        except Exception as e:
            print(f"Fehler beim Erstellen oder Senden des Transkripts: {e}")
            transcript_succeeded = False
            error_embed = Embed(
                title="Ticket-Löschung fehlgeschlagen!",
                description=f"Ein Fehler ist beim Erstellen oder Senden des Transkripts aufgetreten: {config.a_cross}\nBitte versuchen Sie es erneut oder kontaktieren Sie den Bot-Entwickler.",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)
            return

        await asyncio.sleep(2)

        db_succeeded = True
        try:
            BotDB().delete_ticket(inter.channel.id, inter.guild.id)
        except Exception as e:
            print(f"Fehler beim Löschen des Tickets aus der Datenbank: {e}")
            db_succeeded = False
        
        db_status_emoji = config.a_tic if db_succeeded else config.a_cross
        updated_info_db = Embed(
            title="Ticket-Löschung angefordert!",
            description=f"Bitte warten Sie einen Moment...\n\nTranskript gesendet {transcript_status_emoji}\nTicket aus Datenbank entfernt {db_status_emoji}\nKanal-Löschung {config.e_loading}",
            colour=config.blurple
        )
        await inter.edit_original_response(embed=updated_info_db)
        await asyncio.sleep(2)

        self.open_ticket.disabled = True
        self.close_ticket.disabled = True
        button.disabled = True
        
        try:
            message_to_edit = await inter.channel.fetch_message(inter.message.id)
            await message_to_edit.edit(view=self)
        except nc.NotFound:
            print("Die Nachricht mit dem Ticket-Button wurde nicht gefunden.")
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Ticket-Nachricht-View: {e}")

        channel_deleted_successfully = False
        try:
            await inter.edit_original_response(
                embed=Embed(
                    title="Ticket-Löschung angefordert!",
                    description=f"Bitte warten Sie einen Moment...\n\nTranskript gesendet {transcript_status_emoji}\nTicket aus Datenbank entfernt {db_status_emoji}\nKanal-Löschung {config.e_loading}",
                    colour=config.blurple
                )
            )
            await asyncio.sleep(1)
            await inter.channel.delete()
            channel_deleted_successfully = True
        except nc.Forbidden:
            error_embed = Embed(
                title="Fehler bei der Ticket-Löschung!",
                description=f"Kanal konnte nicht gelöscht werden: Fehlende Berechtigungen. {config.a_cross}",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)
        except Exception as e:
            print(f"Fehler beim Löschen des Kanals {inter.channel.id}: {e}")
            error_embed = Embed(
                title="Fehler bei der Ticket-Löschung!",
                description=f"Ein unerwarteter Fehler ist beim Löschen des Kanals aufgetreten: {config.a_cross}",
                colour=config.red
            )
            await inter.edit_original_response(embed=error_embed)