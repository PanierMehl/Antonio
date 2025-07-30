import nextcord as nc
from nextcord import Interaction, Embed
from nextcord.ext.commands import Context
import config
import pytz
from datetime import datetime
import humanfriendly
import time as pyTime
from mysql_asyncmy import A_DB
import random
import string
import json
from io import BytesIO

def generate_random_id(length):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))


class giveaway_create_en(nc.ui.Modal):
    def __init__(self, channel, requirement, value):
        self.channel = channel
        self.value = value
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
        epochEnd = int(pyTime.time() + time)
        giveaway_id = generate_random_id(8)
        value_str = ",".join(map(str, self.value)) if isinstance(self.value, list) else str(self.value)
        await inter.client.db.insert_giveaway(giveaway_id, epochEnd, self.prize.value, self.channel.id, inter.guild.id, None, self.winners.value, self.requirement, value_str)
        
        if str(self.requirement).lower() == "role":
            mention_text = f"<@&{self.value}>"
        elif str(self.requirement).lower() == "user":
            if isinstance(self.value, list):
                mention_text = ", ".join([f"<@{u}>" for u in self.value])
            else:
                mention_text = f"<@{self.value}>"
        else:
            mention_text = "All"
            
        giveaway_embed = Embed(title=f"🎉 {self.prize.value} 🎉", description=f"Ends at <t:{int(epochEnd)}:f> or <t:{int(epochEnd)}:R>", colour=config.green)
        giveaway_embed.add_field(name=f"Winner(s): {self.winners.value}", value="Click the Button to join!\n\uFEFF")
        giveaway_embed.add_field(name="Eligible to participate:", value=f"{mention_text}\n\uFEFF", inline=False)
        giveaway_embed.add_field(name="Entries:", value="0\n\uFEFF", inline=False)
        giveaway_embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
        giveaway_embed.set_author(name=f"{inter.user.name} started a Giveaway")
        giveaway_started = Embed(title=f"🎉 Giveaway started! 🎉", description=f"Giveaway started in {self.channel.mention}")
        
        await inter.response.send_message(embed=giveaway_started, ephemeral=True)
        view = join_giveawy_en(inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=giveaway_embed, view=view)
        view.message = msg 

        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        await inter.client.db.update_giveaway(msg.id, inter.guild.id, giveaway_id)
        await inter.client.db.insert_button("en", inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
    
    
class giveaway_create_de(nc.ui.Modal):
    def __init__(self, channel, requirement, value):
        self.channel = channel
        self.requirement = requirement
        self.value = value
        
        super().__init__(f"Erstelle ein Gewinnspiel in {self.channel}")
        self.prize = nc.ui.TextInput(label="Gewinn", style=nc.TextInputStyle.paragraph, placeholder="Der Preis der Verlosung", required=True, max_length=50)
        self.time = nc.ui.TextInput(label="Zeit", style=nc.TextInputStyle.short, max_length=3, placeholder="Maximal 14 Tage", default_value="1h")
        self.winners = nc.ui.TextInput(label="Anzahl der Gewinner", style=nc.TextInputStyle.short, max_length=2, placeholder="Die Anzahl der Gewinner dieser Verlosung (Maximal 99).", default_value="0")
        self.add_item(self.prize)
        self.add_item(self.time)
        self.add_item(self.winners)
                            
    async def callback(self, inter: nc.Interaction):
        time = humanfriendly.parse_timespan(self.time.value)
        epochEnd = int(pyTime.time() + time)
        giveaway_id = generate_random_id(8)
        value_str = ",".join(map(str, self.value)) if isinstance(self.value, list) else str(self.value)
        await inter.client.db.insert_giveaway(giveaway_id, epochEnd, self.prize.value, self.channel.id, inter.guild.id, None, self.winners.value, self.requirement, value_str)
        
        if str(self.requirement).lower() == "role":
            mention_text = f"<@&{self.value}>"
        elif str(self.requirement).lower() == "user":
            if isinstance(self.value, list):
                mention_text = ", ".join([f"<@{u}>" for u in self.value])
            else:
                mention_text = f"<@{self.value}>"
        else:
            mention_text = "Alle"
            
        giveaway_embed = Embed(title=f"{config.giveaway} {self.prize.value} {config.giveaway}", description=f"Endet am <t:{int(epochEnd)}:f> oder <t:{int(epochEnd)}:R>", colour=config.green)
        giveaway_embed.add_field(name=f"Gewinner: {self.winners.value}", value="Drücke den Button um teilzunehmen!\n\uFEFF")
        giveaway_embed.add_field(name="Teilnahmebrechtigt:", value=f"{mention_text}\n\uFEFF", inline=False)        
        giveaway_embed.add_field(name="Anzahl der Teilnhemer:", value="0\n\uFEFF", inline=False)
        giveaway_embed.set_footer(text=f"Verlosungs-ID: {giveaway_id}")
        giveaway_embed.set_author(name=f"{inter.user.name} hat eine Verlosung gestartet")
        giveaway_started = Embed(title=f"{config.giveaway} Verlosung gestartet! {config.giveaway}", description=f"Verlosung wurde in {self.channel.mention} gestartet")
        
        await inter.response.send_message(embed=giveaway_started, ephemeral=True)
        view = join_giveawy_de(inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=giveaway_embed, view=view)
        view.message = msg  
        
        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        await inter.client.db.update_giveaway(msg.id, inter.guild.id, giveaway_id)
        await inter.client.db.insert_button("de", inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
       
        
class join_giveawy_en(nc.ui.View):
    def __init__(self, guild, giveaway_id):
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
        await inter.response.defer(ephemeral=True)
        data = await inter.client.db.fetch_giveaway_participants(inter.guild.id, self.giveaway_id)
        req = await inter.client.db.query_giveaway_data(self.giveaway_id)
        
        try:
            current_embed = self.message.embeds[0]
        except:
            abc = await inter.client.db.ga_embed_data(self.giveaway_id)
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

            # --- Regeln prüfen ---
            if req[4] is None:
                await self.handle_participation(inter, participants, current_embed)

            elif req[4] == "role":
                required_role_id = int(req[5])
                role = inter.guild.get_role(required_role_id)
                if role and role in inter.user.roles:
                    await self.handle_participation(inter, participants, current_embed)
                else:
                    no_access = Embed(
                        title=f"{config.access_denied} Not eligible {config.access_denied}",
                        description=f"You need the role {role.mention if role else 'Unknown Role'} to join this giveaway.",
                        colour=config.red
                    )
                    await inter.response.send_message(embed=no_access, ephemeral=True)

            elif req[4] == "user":
                allowed_users = [int(u) for u in req[5].split(",")] if req[5] else []
                if inter.user.id in allowed_users:
                    await self.handle_participation(inter, participants, current_embed)
                else:
                    no_access = Embed(
                        title=f"{config.access_denied} Not eligible {config.access_denied}",
                        description="You are not allowed to join this giveaway.",
                        colour=config.red
                    )
                    await inter.response.send_message(embed=no_access, ephemeral=True)

        else:
            giveaway_ended = Embed(
                title=f"{config.access_denied} You're too late! {config.access_denied}",
                description="Unfortunately, the giveaway is already over. Good luck next time.",
                colour=config.red
            )
            await inter.response.send_message(embed=giveaway_ended, ephemeral=True)

    # --- Hilfsfunktion ---
    async def handle_participation(self, inter, participants, current_embed):
        if inter.user.id in participants:
            already_joined = Embed(
                title=f"{config.access_denied} Only one chance per person! {config.access_denied}",
                description="You are already taking part in this giveaway.",
                colour=config.red
            )
            await inter.response.send_message(embed=already_joined, ephemeral=True)
        else:
            giveaway_joined = Embed(
                title=f"Giveaway joined {config.join}",
                description="You are now successfully participating in the giveaway. If you have won, you will be notified here and by private message.",
                colour=config.green
            )
            await inter.response.send_message(embed=giveaway_joined, ephemeral=True)

            participants.append(inter.user.id)
            await inter.client.db.update_giveaway_participants(
                json.dumps(participants),
                inter.guild.id,
                self.giveaway_id
            )

            new_entries_count = len(participants)
            current_embed.set_field_at(2, name="Entries:", value=str(new_entries_count), inline=False)
            await self.message.edit(embed=current_embed)
            
            
class join_giveawy_de(nc.ui.View):
    def __init__(self, guild, giveaway_id):
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
        data = await inter.client.db.fetch_giveaway_participants(inter.guild.id, self.giveaway_id)
        req = await inter.client.db.query_giveaway_data(self.giveaway_id)  # Hier prüfen wir die Bedingungen
        
        try:
            current_embed = self.message.embeds[0]
        except:
            abc = await inter.client.db.ga_embed_data(self.giveaway_id)
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

            # --- Teilnahmebedingungen ---
            if req[4] is None:
                await self.handle_participation(inter, participants, current_embed)

            elif req[4] == "role":
                required_role_id = int(req[5])
                role = inter.guild.get_role(required_role_id)
                if role and role in inter.user.roles:
                    await self.handle_participation(inter, participants, current_embed)
                else:
                    no_access = Embed(
                        title=f"{config.access_denied} Nicht teilnahmeberechtigt {config.access_denied}",
                        description=f"Du brauchst die Rolle {role.mention if role else 'Unbekannt'} um teilzunehmen.",
                        colour=config.red
                    )
                    await inter.response.send_message(embed=no_access, ephemeral=True)

            elif req[4] == "user":
                allowed_users = [int(u) for u in req[5].split(",")] if req[5] else []
                if inter.user.id in allowed_users:
                    await self.handle_participation(inter, participants, current_embed)
                else:
                    no_access = Embed(
                        title=f"{config.access_denied} Nicht teilnahmeberechtigt {config.access_denied}",
                        description="Du bist nicht berechtigt an dieser Verlosung teilzunehmen.",
                        colour=config.red
                    )
                    await inter.response.send_message(embed=no_access, ephemeral=True)

        else:
            giveaway_ended = Embed(
                title=f"{config.access_denied} Du bist zu spät dran! {config.access_denied}",
                description="Leider ist die Verlosung schon vorbei. Viel Glück beim nächsten Mal :)",
                colour=config.red
            )
            await inter.response.send_message(embed=giveaway_ended, ephemeral=True)

    # --- Hilfsfunktion für Teilnahme ---
    async def handle_participation(self, inter, participants, current_embed):
        if inter.user.id in participants:
            already_joined = Embed(
                title=f"{config.access_denied} Sei fair! {config.access_denied}",
                description="Du nimmst bereits an dieser Verlosung teil.",
                colour=config.red
            )
            await inter.response.send_message(embed=already_joined, ephemeral=True)
        else:
            giveaway_joined = Embed(
                title=f"Verlosung beigetreten {config.join}",
                description="Du bist dabei! Du nimmst nun an dieser Verlosung teil. Du wirst hier benachrichtigt, wenn du gewonnen hast.",
                colour=config.green
            )
            await inter.response.send_message(embed=giveaway_joined, ephemeral=True)

            participants.append(inter.user.id)
            await inter.client.db.update_giveaway_participants(
                json.dumps(participants),
                inter.guild.id,
                self.giveaway_id
            )

            new_entries_count = len(participants)
            current_embed.set_field_at(2, name="Teilnehmer:", value=str(new_entries_count), inline=False)
            await self.message.edit(embed=current_embed)

class giveaway_selected_roles_en(nc.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        
    
    @nc.ui.role_select(placeholder="Please choose a role", max_values=1)
    async def on_select(self, select: nc.ui.RoleSelect, inter: nc.Interaction):
        roles = select.values
        for role in roles:
            pass
        
        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, "role", role.id))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "role", role.id))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "role", role.id))
          
          
            
class giveaway_selected_roles_de(nc.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        
    
    @nc.ui.role_select(placeholder="Bitte wähle eine Rolle aus", max_values=1)
    async def on_select(self, select: nc.ui.RoleSelect, inter: nc.Interaction):
        roles = select.values
        for role in roles:
            pass
        print(role)
        print(role.id)
        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, "role", role.id))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "role", role.id))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "role", role.id))
    
    
            
class giveaway_selected_user_de(nc.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        
    
    @nc.ui.user_select(placeholder="Bitte wähle Mitglieder aus", max_values=10)
    async def on_select(self, select: nc.ui.UserSelect, inter: nc.Interaction):
        users = [user.id for user in select.values]
        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, "user", users))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "user", users))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "user", users))
            
            
            
class giveaway_selected_user_en(nc.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        
    
    @nc.ui.user_select(placeholder="Please select members", max_values=10)
    async def on_select(self, select: nc.ui.UserSelect, inter: nc.Interaction):
        users = [user.id for user in select.values]

        if inter.locale == "de":
            await inter.response.send_modal(modal=giveaway_create_de(self.channel, "user", users))
        
        elif inter.locale == "en_US":
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "user", users))
            
        else:
            await inter.response.send_modal(modal=giveaway_create_en(self.channel, "user", users))
            
            
class TranscriptButton(nc.ui.View):
    def __init__(self, participants_data, winners, giveaway_id, prize, ended):
        super().__init__(timeout=180)
        self.participants_data = participants_data
        self.winners = winners
        self.giveaway_id = giveaway_id
        self.prize = prize
        self.ended = ended


@nc.ui.button(style=nc.ButtonStyle.primary, label="📄 Teilnehmerliste (HTML)")
async def tr_button(self, button: nc.ui.Button, interaction: nc.Interaction):
    try:
        participants = json.loads(self.participants_data)
    except Exception as e:
        await interaction.response.send_message(
            content=f"❌ Fehler beim Verarbeiten der Teilnehmerdaten:\n`{e}`",
            ephemeral=True
        )
        return

    winners = self.winners  # Liste von User-IDs als Strings
    guild = interaction.guild

    def user_block(user, is_winner=False):
        tag = f"{user.name}#{user.discriminator}"
        avatar = user.display_avatar.url
        uid = user.id
        winner_class = "winner" if is_winner else ""
        return f"""
        <div class="user {winner_class}">
            <img src="{avatar}" alt="{tag}">
            <div class="text">
                <strong>{tag}</strong><br>
                <span>({uid})</span>
            </div>
        </div>
        """

    winner_html = ""
    entrant_html = ""

    for uid in participants:
        member = guild.get_member(int(uid))
        if member:
            block = user_block(member, is_winner=(str(member.id) in winners))
            if str(member.id) in winners:
                winner_html += block
            else:
                entrant_html += block

    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Giveaway Transkript</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #b7c7f0; padding: 20px; color: #333; }}
        h1 {{ color: #3b3b3b; }}
        .user {{
            display: flex; align-items: center; margin: 10px 0;
            background: #dbe4ff; padding: 10px; border-radius: 10px;
        }}
        .user img {{
            width: 48px; height: 48px; border-radius: 50%; margin-right: 10px;
        }}
        .winner {{ border: 2px solid gold; background-color: #fff8dc; }}
        .text strong {{ font-size: 16px; }}
        .section-title {{ margin-top: 30px; font-size: 22px; color: #2c2c2c; }}
    </style>
</head>
<body>
    <h1>Giveaway Transkript</h1>
    <p><strong>Giveaway ID:</strong> {self.giveaway_id}</p>
    <p><strong>Prize:</strong> {self.prize}</p>
    <p><strong>Ended:</strong> {self.ended}</p>

    <div class="section-title">🎉 Winners</div>
    {winner_html or "<p>No winners</p>"}

    <div class="section-title">👥 Entrants</div>
    {entrant_html or "<p>No participants</p>"}
</body>
</html>
"""

    # Encode & senden
    buffer = BytesIO(html_template.encode("utf-8"))
    file = nc.File(buffer, filename="giveaway_transcript.html")

    await interaction.response.send_message(
        content="📄 HTML-Teilnehmerliste:",
        file=file,
        ephemeral=True
    )
