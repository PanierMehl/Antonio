import nextcord as nc
from nextcord import Interaction, Embed
from nextcord.ext.commands import Context
import config
import pytz
from datetime import datetime
import humanfriendly
import time as pyTime
from mysql_class import BotDB
import random
import string
import json
import yaml

def generate_random_id(length):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))


class giveaway_create_en(nc.ui.Modal):
    def __init__(self, channel, requirement):
        self.channel = channel
        self.requirement = requirement
        
        super().__init__(f"Create a Giveaway in {self.channel}")
        self.prize = nc.ui.TextInput(label="Prize", style=nc.TextInputStyle.paragraph, placeholder="The prize for the giveaway", required=True, max_length=50)
        self.time = nc.ui.TextInput(label="Time", style=nc.TextInputStyle.short, max_length=3, placeholder="Max 14 Days", default_value="1h")
        self.winners = nc.ui.TextInput(label="Winners", style=nc.TextInputStyle.short, max_length=2, placeholder="The amount of giveaway winners (max 99).", default_value="0")
        self.add_item(self.prize)
        self.add_item(self.time)
        self.add_item(self.winners)
                            
    async def callback(self, inter: nc.Interaction):
        time = humanfriendly.parse_timespan(self.time.value)
        epochEnd = pyTime.time() + time
        giveaway_id = generate_random_id(8)
        
        BotDB().insert_giveaway(giveaway_id, int(epochEnd), self.prize.value, self.channel.id, inter.guild.id, None, self.winners.value, self.requirement)
        
        giveaway_embed = Embed(title=f"🎉 {self.prize.value} 🎉", description=f"Ends at <t:{int(epochEnd)}:f> or <t:{int(epochEnd)}:R>", colour=config.green)
        giveaway_embed.add_field(name=f"Winner(s): {self.winners.value}", value="Click the Button to join!\n\uFEFF")
        giveaway_embed.add_field(name="Entries:", value="0\n\uFEFF", inline=False)
        giveaway_embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
        giveaway_embed.set_author(name=f"{inter.user.name} started a Giveaway")
        giveaway_started = Embed(title=f"🎉 Giveaway started! 🎉", description=f"Giveaway started in {self.channel.mention}")
        
        await inter.response.send_message(embed=giveaway_started, ephemeral=True)
        view = join_giveawy_en(epochEnd, inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=giveaway_embed, view=view)
        view.message = msg 

        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        BotDB().update_giveaway(msg.id, inter.guild.id, giveaway_id)
        BotDB().insert_button(epochEnd, inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
    
    
class giveaway_create_de(nc.ui.Modal):
    def __init__(self, channel, requirement):
        self.channel = channel
        self.requirement = requirement
        
        super().__init__(f"Erstelle ein Gewinnspiel im Kanal {self.channel}")
        self.prize = nc.ui.TextInput(label="Gewinn", style=nc.TextInputStyle.paragraph, placeholder="Der Preis der Verlosung", required=True, max_length=50)
        self.time = nc.ui.TextInput(label="Zeit", style=nc.TextInputStyle.short, max_length=3, placeholder="Maximal 14 Tage", default_value="1h")
        self.winners = nc.ui.TextInput(label="Anzahl der Gewinner", style=nc.TextInputStyle.short, max_length=2, placeholder="Die Anzahl der Gewinner dieser Verlosung (Maximal 99).", default_value="0")
        self.add_item(self.prize)
        self.add_item(self.time)
        self.add_item(self.winners)
                            
    async def callback(self, inter: nc.Interaction):
        time = humanfriendly.parse_timespan(self.time.value)
        epochEnd = int(pyTime.time() + time)
        print(f"epoch_end {epochEnd}")
        giveaway_id = generate_random_id(8)
        
        BotDB().insert_giveaway(giveaway_id, epochEnd, self.prize.value, self.channel.id, inter.guild.id, None, self.winners.value, self.requirement)
        
        giveaway_embed = Embed(title=f"{config.giveaway} {self.prize.value} {config.giveaway}", description=f"Endet am <t:{int(epochEnd)}:f> oder <t:{int(epochEnd)}:R>", colour=config.green)
        giveaway_embed.add_field(name=f"Gewinner: {self.winners.value}", value="Drücke den Button um teilzunehmen!\n\uFEFF")
        giveaway_embed.add_field(name="Anzahl der Teilnhemer:", value="0\n\uFEFF", inline=False)
        giveaway_embed.set_footer(text=f"Verlosungs-ID: {giveaway_id}")
        giveaway_embed.set_author(name=f"{inter.user.name} hat eine Verlosung gestartet")
        giveaway_started = Embed(title=f"{config.giveaway} Verlosung gestartet! {config.giveaway}", description=f"Verlosung wurde in {self.channel.mention} gestartet")
        
        await inter.response.send_message(embed=giveaway_started, ephemeral=True)
        view = join_giveawy_de(epochEnd, inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=giveaway_embed, view=view)
        view.message = msg  
        
        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        BotDB().update_giveaway(msg.id, inter.guild.id, giveaway_id)
        BotDB().insert_button(epochEnd, inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
       
        
class join_giveawy_en(nc.ui.View):
    def __init__(self, time, guild, giveaway_id):
        super().__init__(timeout=None)
        self.guild = guild
        self.giveaway_id = giveaway_id
        self.giveaway_join.custom_id = str(self.giveaway_id)
        
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=self)
    
    @nc.ui.button(label="Join Giveaway", style=nc.ButtonStyle.blurple, emoji="🎁")
    async def giveaway_join(self, button: nc.ui.Button, inter: Interaction):
        data = BotDB().fetch_giveaway_participants(inter.guild.id, self.giveaway_id)
        
        try:
            current_embed = self.message.embeds[0]
        except:
            abc = BotDB().ga_embed_data(self.giveaway_id)
            current_embed = abc[0]

        if data:
            participants_str = data[0]

            if participants_str is None:
                participants = []
            else:
                try:
                    participants = json.loads(participants_str)
                except json.JSONDecodeError:
                    participants = []

            if inter.user.id in participants:
                already_joined = Embed(
                    title="Only one chance per person!",
                    description="You are already taking part in this giveaway.",
                    colour=config.red
                )
                await inter.response.send_message(embed=already_joined, ephemeral=True)
                
            else:
                
                giveaway_joined = Embed(
                    title="Giveaway joined",
                    description="You are now successfully participating in the giveaway. If you have won, you will be notified here and by private message.",
                    colour=config.green
                )
                await inter.response.send_message(embed=giveaway_joined, ephemeral=True)
                
                participants.append(inter.user.id)
                BotDB().update_giveaway_participants(
                    json.dumps(participants), 
                    inter.guild.id, 
                    self.giveaway_id
                )

                               
                new_entries_count = len(participants)
                current_embed.set_field_at(1, name="Entries:", value=str(new_entries_count), inline=False)
                await self.message.edit(embed=current_embed)

        else:
            giveaway_ended = Embed(
                title="You're too late!",
                description="Unfortunately, the giveaway is already over. Good luck next time.",
                colour=config.red
            )
            await inter.response.send_message(embed=giveaway_ended, ephemeral=True)
            
            
            
class join_giveawy_de(nc.ui.View):
    def __init__(self, time, guild, giveaway_id):
        super().__init__(timeout=None)
        self.guild = guild
        self.giveaway_id = giveaway_id
        self.giveaway_join.custom_id = str(self.giveaway_id)
        
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=self)
    
    @nc.ui.button(label="Mitmachen", style=nc.ButtonStyle.blurple, emoji="🎁")
    async def giveaway_join(self, button: nc.ui.Button, inter: Interaction):
        data = BotDB().fetch_giveaway_participants(inter.guild.id, self.giveaway_id)
        
        try:
            current_embed = self.message.embeds[0]
        except:
            abc = BotDB().ga_embed_data(self.giveaway_id)
            current_embed = abc[0]

        if data:
            participants_str = data[0]

            if participants_str is None:
                participants = []
            else:
                try:
                    participants = json.loads(participants_str)
                except json.JSONDecodeError:
                    participants = []

            if inter.user.id in participants:
                already_joined = Embed(
                    title="Sei fair!",
                    description="Du nimmst bereits an dieser Verlosung teil.",
                    colour=config.red
                )
                await inter.response.send_message(embed=already_joined, ephemeral=True)
                
            else:
                
                giveaway_joined = Embed(
                    title="Verlosung beigetreten",
                    description="Du bist dabei! Du nimmst nun an dieser Verlosung teil. Du wirst hier benachrichtigt wenn du gewonnen hast.",
                    colour=config.green
                )
                await inter.response.send_message(embed=giveaway_joined, ephemeral=True)
                
                participants.append(inter.user.id)
                BotDB().update_giveaway_participants(
                    json.dumps(participants), 
                    inter.guild.id, 
                    self.giveaway_id
                )

                               
                new_entries_count = len(participants)
                current_embed.set_field_at(1, name="Teilnehmer:", value=str(new_entries_count), inline=False)
                await self.message.edit(embed=current_embed)

        else:
            giveaway_ended = Embed(
                title="Du bist zu spät dran!",
                description="Leider ist die Verlosung schon vorbei. Viel Glück beim nächsten mal :)",
                colour=config.red
            )
            await inter.response.send_message(embed=giveaway_ended, ephemeral=True)
            
            

class giveaway_selecetes_roles_en(nc.ui.View):
    def __init__(self, channel):
        self.channel = channel
        
    
    @nc.ui.role_select(placeholder="Please choose a role", max_values=1)
    async def on_select(self, select: nc.ui.RoleSelect, inter: nc.Interaction):
        roles = select.values.roles
        for role in roles:
            pass
        
        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, role))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, role))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, role))
          
          
            
class giveaway_selecetes_roles_de(nc.ui.View):
    def __init__(self, channel):
        self.channel = channel
        
    
    @nc.ui.role_select(placeholder="Bitte wähle eine Rolle aus", max_values=1)
    async def on_select(self, select: nc.ui.RoleSelect, inter: nc.Interaction):
        roles = select.values.roles
        for role in roles:
            pass
        
        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, role))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, role))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, role))
    
    
            
class giveaway_selecetes_user_de(nc.ui.View):
    def __init__(self, channel):
        self.channel = channel
        
    
    @nc.ui.user_select(placeholder="Bitte wähle Mitglieder aus", max_values=10)
    async def on_select(self, select: nc.ui.UserSelect, inter: nc.Interaction):
        users = select.values.users

        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, users))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, users))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, users))
            
            
            
class giveaway_selecetes_user_en(nc.ui.View):
    def __init__(self, channel):
        self.channel = channel
        
    
    @nc.ui.user_select(placeholder="Please select members", max_values=10)
    async def on_select(self, select: nc.ui.UserSelect, inter: nc.Interaction):
        users = select.values.users

        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, users))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, users))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, users))