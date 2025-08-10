import nextcord as nc
from nextcord import Interaction, Embed
import config
import humanfriendly
import time as pyTime
import random
import string
import json
from io import BytesIO
from datetime import datetime
        
def generate_random_id(length):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))

# Version 6 | Giveaway Create EN View
class giveaway_create_en(nc.ui.Modal):
    def __init__(self, channel, requirement, value):
        self.channel = channel
        self.value = value
        self.requirement = requirement
        
        super().__init__(f"Create a Giveaway in {self.channel}")
        self.prize = nc.ui.TextInput(label="Prize",
                                     style=nc.TextInputStyle.paragraph,
                                     placeholder="The prize for the giveaway",
                                     required=True,
                                     max_length=50)
        self.time = nc.ui.TextInput(label="Time",
                                    style=nc.TextInputStyle.short,
                                    max_length=3,
                                    placeholder="Max 14 Days",
                                    default_value="1h")
        self.winners = nc.ui.TextInput(label="Winners",
                                       style=nc.TextInputStyle.short,
                                       max_length=2,
                                       placeholder="The amount of giveaway winners (max 99).",
                                       default_value="0")
        self.add_item(self.prize)
        self.add_item(self.time)
        self.add_item(self.winners)
                            
    async def callback(self, inter: nc.Interaction):
        time = humanfriendly.parse_timespan(self.time.value)
        epochEnd = int(pyTime.time() + time)
        giveaway_id = generate_random_id(8)
        value_str = ",".join(map(str, self.value)) if isinstance(self.value, list) else str(self.value)
        
        await inter.client.db.insert_giveaway(giveaway_id,
                                              epochEnd,
                                              self.prize.value,
                                              self.channel.id,
                                              inter.guild.id,
                                              None,
                                              self.winners.value,
                                              self.requirement,
                                              value_str)
        
        if str(self.requirement).lower() == "role":
            mention_text = f"<@&{self.value}>"
            
        elif str(self.requirement).lower() == "user":
            
            if isinstance(self.value, list):
                mention_text = ", ".join([f"<@{u}>" for u in self.value])
            else:
                mention_text = f"<@{self.value}>"
                
        else:
            mention_text = "All"
            
        e_ga_en = Embed(title=f"🎉 {self.prize.value} 🎉",
                               description=f"Ends at <t:{int(epochEnd)}:f> or <t:{int(epochEnd)}:R>",
                               colour=config.green)
        e_ga_en.add_field(name=f"Winner(s): {self.winners.value}",
                                 value="Click the Button to join!\n\uFEFF")
        e_ga_en.add_field(name="Eligible to participate:",
                                 value=f"{mention_text}\n\uFEFF",
                                 inline=False)
        e_ga_en.add_field(name="Entries:",
                                 value="0\n\uFEFF",
                                 inline=False)
        e_ga_en.set_footer(text=f"Giveaway ID: {giveaway_id}")
        e_ga_en.set_author(name=f"{inter.user.name} started a Giveaway")
        
        e_ga_started_en = Embed(title=f"🎉 Giveaway started! 🎉",
                                 description=f"Giveaway started in {self.channel.mention}")
        
        await inter.response.send_message(embed=e_ga_started_en, ephemeral=True)
        
        view = join_giveawy_en(inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=e_ga_en, view=view)
        view.message = msg 

        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        await inter.client.db.update_giveaway(msg.id, inter.guild.id, giveaway_id)
        await inter.client.db.insert_button("en", inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
    

# Version 6 | Giveaway Create DE View
class giveaway_create_de(nc.ui.Modal):
    def __init__(self, channel, requirement, value):
        self.channel = channel
        self.requirement = requirement
        self.value = value
        
        super().__init__(f"Erstelle ein Gewinnspiel in {self.channel}")
        self.prize = nc.ui.TextInput(label="Gewinn",
                                     style=nc.TextInputStyle.paragraph,
                                     placeholder="Der Preis der Verlosung",
                                     required=True,
                                     max_length=50)
        self.time = nc.ui.TextInput(label="Zeit",
                                    style=nc.TextInputStyle.short,
                                    max_length=3,
                                    placeholder="Maximal 14 Tage",
                                    default_value="10s")
        self.winners = nc.ui.TextInput(label="Anzahl der Gewinner",
                                       style=nc.TextInputStyle.short,
                                       max_length=2,
                                       placeholder="Die Anzahl der Gewinner dieser Verlosung (Maximal 99).",
                                       default_value="1")
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
            
        e_ga_de = Embed(title=f"{config.giveaway} {self.prize.value} {config.giveaway}",
                        description=f"Endet am <t:{int(epochEnd)}:f> oder <t:{int(epochEnd)}:R>",
                        colour=config.green)
        e_ga_de.add_field(name=f"Gewinner: {self.winners.value}",
                          value="Drücke den Button um teilzunehmen!\n\uFEFF")
        e_ga_de.add_field(name="Teilnahmebrechtigt:",
                          value=f"{mention_text}\n\uFEFF", inline=False)        
        e_ga_de.add_field(name="Anzahl der Teilnhemer:",
                          value="0\n\uFEFF", inline=False)
        e_ga_de.set_footer(text=f"Verlosungs-ID: {giveaway_id}")
        e_ga_de.set_author(name=f"{inter.user.name} hat eine Verlosung gestartet")
        
        e_ga_started_de = Embed(title=f"{config.giveaway} Verlosung gestartet! {config.giveaway}",
                                 description=f"Verlosung wurde in {self.channel.mention} gestartet")
        
        await inter.response.send_message(embed=e_ga_started_de, ephemeral=True)
        
        view = join_giveawy_de(inter.guild.id, giveaway_id)
        msg = await self.channel.send(embed=e_ga_de, view=view)
        view.message = msg  
        
        embed_data = msg.embeds[0].to_dict()  # Convert the Embed object to a dictionary
        embed_json_string = json.dumps(embed_data) # Convert the dictionary to a JSON string

        await inter.client.db.update_giveaway(msg.id, inter.guild.id, giveaway_id)
        await inter.client.db.insert_button("de", inter.guild.id, giveaway_id, embed_json_string, None, inter.guild.id)
       

# Version 6 | Join Giveaway EN    
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

    @nc.ui.button(label="Join Giveaway",style=nc.ButtonStyle.blurple,emoji="🎁")
    async def giveaway_join(self,button: nc.ui.Button, inter: Interaction):
        
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

            if req[4] is None:
                await self.handle_participation(inter, participants, current_embed)

            elif req[4] == "role":
                required_role_id = int(req[5])
                role = inter.guild.get_role(required_role_id)
                if role and role in inter.user.roles:
                    await self.handle_participation(inter, participants, current_embed)
                    
                else:
                    e_no_access = Embed(
                        title=f"{config.access_denied} Not eligible {config.access_denied}",
                        description=f"You need the role {role.mention if role else 'Unknown Role'} to join this giveaway.",
                        colour=config.red)
                    await inter.response.send_message(embed=e_no_access, ephemeral=True)


            elif req[4] == "user":
                allowed_users = [int(u) for u in req[5].split(",")] if req[5] else []
                if inter.user.id in allowed_users:
                    await self.handle_participation(inter, participants, current_embed)
                else:
                    e_no_access = Embed(
                        title=f"{config.access_denied} Not eligible {config.access_denied}",
                        description="You are not allowed to join this giveaway.",
                        colour=config.red)
                    await inter.response.send_message(embed=e_no_access, ephemeral=True)


        else:
            e_giveaway_ended = Embed(
                title=f"{config.access_denied} You're too late! {config.access_denied}",
                description="Unfortunately, the giveaway is already over. Good luck next time.",
                colour=config.red)
            await inter.response.send_message(embed=e_giveaway_ended, ephemeral=True)


    async def handle_participation(self, inter, participants, current_embed):
        if inter.user.id in participants:
            e_already_joined = Embed(
                title=f"{config.access_denied} Only one chance per person! {config.access_denied}",
                description="You are already taking part in this giveaway.",
                colour=config.red)
            await inter.response.send_message(embed=e_already_joined, ephemeral=True)
            
            
        else:
            e_giveaway_joined = Embed(
                title=f"Giveaway joined {config.join}",
                description="You are now successfully participating in the giveaway. If you have won, you will be notified here and by private message.",
                colour=config.green)
            await inter.response.send_message(embed=e_giveaway_joined, ephemeral=True)

            participants.append(inter.user.id)
            await inter.client.db.update_giveaway_participants(
                json.dumps(participants),
                inter.guild.id,
                self.giveaway_id)
            
            new_entries_count = len(participants)
            current_embed.set_field_at(2, name="Entries:", value=str(new_entries_count), inline=False)
            await self.message.edit(embed=current_embed)
            

# Version 6 | Join Giveaway DE View 
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

            if req[4] is None:
                await self.handle_participation(inter, participants, current_embed)

            elif req[4] == "role":
                required_role_id = int(req[5])
                role = inter.guild.get_role(required_role_id)
                
                if role and role in inter.user.roles:
                    await self.handle_participation(inter, participants, current_embed)
                    
                else:
                    e_no_access = Embed(
                        title=f"{config.access_denied} Nicht teilnahmeberechtigt {config.access_denied}",
                        description=f"Du brauchst die Rolle {role.mention if role else 'Unbekannt'} um teilzunehmen.",
                        colour=config.red)
                    await inter.response.send_message(embed=e_no_access, ephemeral=True)


            elif req[4] == "user":
                allowed_users = [int(u) for u in req[5].split(",")] if req[5] else []
                
                if inter.user.id in allowed_users:
                    await self.handle_participation(inter, participants, current_embed)
                    
                else:
                    e_no_access = Embed(
                        title=f"{config.access_denied} Nicht teilnahmeberechtigt {config.access_denied}",
                        description="Du bist nicht berechtigt an dieser Verlosung teilzunehmen.",
                        colour=config.red)
                    await inter.response.send_message(embed=e_no_access, ephemeral=True)


        else:
            e_giveaway_ended = Embed(
                title=f"{config.access_denied} Du bist zu spät dran! {config.access_denied}",
                description="Leider ist die Verlosung schon vorbei. Viel Glück beim nächsten Mal :)",
                colour=config.red)
            await inter.response.send_message(embed=e_giveaway_ended, ephemeral=True)


    async def handle_participation(self, inter, participants, current_embed):
        if inter.user.id in participants:
            e_already_joined = Embed(
                title=f"{config.access_denied} Sei fair! {config.access_denied}",
                description="Du nimmst bereits an dieser Verlosung teil.",
                colour=config.red)
            await inter.response.send_message(embed=e_already_joined, ephemeral=True)
            
        else:
            e_giveaway_joined = Embed(
                title=f"Verlosung beigetreten {config.join}",
                description="Du bist dabei! Du nimmst nun an dieser Verlosung teil. Du wirst hier benachrichtigt, wenn du gewonnen hast.",
                colour=config.green)
            await inter.response.send_message(embed=e_giveaway_joined, ephemeral=True)

            participants.append(inter.user.id)
            await inter.client.db.update_giveaway_participants(
                json.dumps(participants),
                inter.guild.id,
                self.giveaway_id)

            new_entries_count = len(participants)
            current_embed.set_field_at(2, name="Teilnehmer:", value=str(new_entries_count), inline=False)
            await self.message.edit(embed=current_embed)


# Version 6 | Giveaway Select Role EN View
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
          
          
# Version 6 | Giveaway Select Role DE View        
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
    
    
# Version 6 | Giveaway Select User DE View
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
            
            
# Version 6 | Giveaway Select User EN View 
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
            


# Version 6 | Giveaway Transcript Button DE View
class TranscriptButton_de(nc.ui.View):
    def __init__(self, participants_data, winners, giveaway_id, prize, ended, winner_count):
        super().__init__(timeout=None)
        self.participants_data = participants_data
        self.winners = winners
        self.giveaway_id = giveaway_id
        self.prize = prize
        self.ended = ended
        self.winner_count = winner_count


    @nc.ui.button(style=nc.ButtonStyle.success, label="Teilnehmerliste")
    async def tr_button(self, button: nc.ui.Button, interaction: nc.Interaction):

        try:
            participants = json.loads(self.participants_data)
            if not isinstance(participants, list):
                raise ValueError("Teilnehmerdaten sind kein Array.")
        except Exception as e:
            await interaction.response.send_message(
                content=f"❌ Fehler beim Laden der Teilnehmerdaten:\n```{e}```",
                ephemeral=True
            )
            return

        winners = self.winners
        guild = interaction.guild
        client = interaction.client

        def user_block(user, is_winner=False):
            tag = f"{getattr(user, 'name', 'Unbekannt')}#{getattr(user, 'discriminator', '0000')}"
            avatar = getattr(user, "display_avatar", getattr(user, "avatar", None))
            avatar_url = avatar.url if avatar is not None else ""
            uid = getattr(user, "id", "Unbekannt")
            winner_class = " winner" if is_winner else ""
            return f"""
            <div class="user{winner_class}">
                <img src="{avatar_url}" alt="{tag}">
                <div class="text">
                    <strong>{tag}</strong><br>
                    <span>ID: {uid}</span>
                </div>
            </div>
            """

        entrant_html = ""
        winner_html = ""

        for uid in participants:
            try:
                uid_int = int(uid)
                user = guild.get_member(uid_int)
                if user is None:
                    user = await client.fetch_user(uid_int)

                if user:
                    is_win = str(uid) in winners
                    entrant_block = user_block(user, is_winner=False)
                    entrant_html += entrant_block

                    if is_win:
                        winner_block = user_block(user, is_winner=True)
                        winner_html += winner_block
                else:
                    entrant_html += f"<div class='user'><div class='text'>Unbekannter Nutzer (ID: {uid})</div></div>"
            except Exception as e:
                entrant_html += f"<div class='user'><div class='text'>Fehler bei ID {uid}: {e}</div></div>"

        try:
            ended_time = datetime.fromtimestamp(float(self.ended))
            ended_str = ended_time.strftime("%d.%m.%Y %H:%M:%S")
        except Exception:
            ended_str = "Unbekannt"

        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <title>Giveaway Transkript {self.giveaway_id}</title>
            <style>
                body {{
                    background-color: #f0f3ff;
                    font-family: Arial, sans-serif;
                    padding: 30px;
                }}
                h1 {{ text-align: center; color: #2c2c2c; }}
                .info {{ background: #dce3ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                .user-grid {{
                    display: grid;
                    /* responsive: so viele Spalten wie reinpassen; auf großen Bildschirmen typ. 3 */
                    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                /* wenn du wirklich immer 3 Spalten willst, ersetze die obere Zeile mit:
                   grid-template-columns: repeat(3, 1fr);
                */
                .user {{
                    display: flex;
                    align-items: center;
                    background: #cce4ff; /* hellblau für Teilnehmer */
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
                }}
                .user img {{
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    margin-right: 12px;
                }}
                .user .text strong {{ display: block; margin-bottom: 4px; }}
                .winner {{
                    border: 2px solid gold;
                    background-color: #fff9d6 !important; /* Gewinner gelb */
                }}
                .section-title {{
                    margin-top: 30px;
                    font-size: 20px;
                    border-bottom: 2px solid #999;
                    padding-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>🎉 Giveaway Transkript</h1>
            <div class="info">
                <p><strong>🎁 Preis:</strong> {self.prize}</p>
                <p><strong>🆔 Giveaway-ID:</strong> {self.giveaway_id}</p>
                <p><strong>⏰ Beendet:</strong> {ended_str}</p>
                <p><strong>👥 Teilnehmer:</strong> {len(participants)}</p>
                <p><strong>🏆 Gewinner:</strong> {self.winner_count}</p>
            </div>

            <div class="section-title">🏆 Gewinner</div>
            <div class="user-grid">
                {winner_html or "<p>Keine Gewinner</p>"}
            </div>

            <div class="section-title">👥 Teilnehmer</div>
            <div class="user-grid">
                {entrant_html or "<p>Keine Teilnehmer</p>"}
            </div>
        </body>
        </html>
        """

        buffer = BytesIO(html.encode("utf-8"))
        file = nc.File(buffer, filename=f"giveaway_transcript{self.giveaway_id}.html")

        await interaction.response.send_message(
            file=file,
            ephemeral=True
        )


# Version 6 | Giveaway Transcript Button EN View
class TranscriptButton_en(nc.ui.View):
    def __init__(self, participants_data, winners, giveaway_id, prize, ended, winner_count):
        super().__init__(timeout=None)
        self.participants_data = participants_data
        self.winners = winners
        self.giveaway_id = giveaway_id
        self.prize = prize
        self.ended = ended
        self.winner_count = winner_count


    @nc.ui.button(style=nc.ButtonStyle.success, label="Participants list")
    async def tr_button(self, button: nc.ui.Button, interaction: nc.Interaction):
        try:
            participants = json.loads(self.participants_data)
            if not isinstance(participants, list):
                raise ValueError("Error at Participants load")
        except Exception as e:
            await interaction.response.send_message(
                content=f"{config.a_cross} Error loading participant data:\n```{e}```",
                ephemeral=True
            )
            return

        winners = self.winners
        guild = interaction.guild
        client = interaction.client

        def user_block(user, is_winner=False):
            tag = f"{getattr(user, 'name', 'Unknown')}#{getattr(user, 'discriminator', '0000')}"
            avatar = getattr(user, "display_avatar", getattr(user, "avatar", None))
            avatar_url = avatar.url if avatar is not None else ""
            uid = getattr(user, "id", "Unknown")
            winner_class = " winner" if is_winner else ""
            return f"""
            <div class="user{winner_class}">
                <img src="{avatar_url}" alt="{tag}">
                <div class="text">
                    <strong>{tag}</strong><br>
                    <span>ID: {uid}</span>
                </div>
            </div>
            """

        entrant_html = ""
        winner_html = ""

        for uid in participants:
            try:
                uid_int = int(uid)
                user = guild.get_member(uid_int)
                if user is None:
                    user = await client.fetch_user(uid_int)

                if user:
                    is_win = str(uid) in winners
                    entrant_block = user_block(user, is_winner=False)
                    entrant_html += entrant_block

                    if is_win:
                        winner_block = user_block(user, is_winner=True)
                        winner_html += winner_block
                else:
                    entrant_html += f"<div class='user'><div class='text'>Unknown User (ID: {uid})</div></div>"
            except Exception as e:
                entrant_html += f"<div class='user'><div class='text'>Error on ID {uid}: {e}</div></div>"

        try:
            ended_time = datetime.fromtimestamp(float(self.ended))
            ended_str = ended_time.strftime("%d.%m.%Y %H:%M:%S")
        except Exception:
            ended_str = "Unknown"

        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <title>Giveaway Transcript {self.giveaway_id}</title>
            <style>
                body {{
                    background-color: #f0f3ff;
                    font-family: Arial, sans-serif;
                    padding: 30px;
                }}
                h1 {{ text-align: center; color: #2c2c2c; }}
                .info {{ background: #dce3ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                .user-grid {{
                    display: grid;
                    /* responsive: so viele Spalten wie reinpassen; auf großen Bildschirmen typ. 3 */
                    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                /* wenn du wirklich immer 3 Spalten willst, ersetze die obere Zeile mit:
                   grid-template-columns: repeat(3, 1fr);
                */
                .user {{
                    display: flex;
                    align-items: center;
                    background: #cce4ff; /* hellblau für Teilnehmer */
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
                }}
                .user img {{
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    margin-right: 12px;
                }}
                .user .text strong {{ display: block; margin-bottom: 4px; }}
                .winner {{
                    border: 2px solid gold;
                    background-color: #fff9d6 !important; /* Gewinner gelb */
                }}
                .section-title {{
                    margin-top: 30px;
                    font-size: 20px;
                    border-bottom: 2px solid #999;
                    padding-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>🎉 Giveaway Transcript</h1>
            <div class="info">
                <p><strong>🎁 Prize:</strong> {self.prize}</p>
                <p><strong>🆔 Giveaway-ID:</strong> {self.giveaway_id}</p>
                <p><strong>⏰ Ended:</strong> {ended_str}</p>
                <p><strong>👥 Participants:</strong> {len(participants)}</p>
                <p><strong>🏆 Winner(s):</strong> {self.winner_count}</p>
            </div>

            <div class="section-title">🏆 Winner(s)</div>
            <div class="user-grid">
                {winner_html or "<p>No Winner(s)</p>"}
            </div>

            <div class="section-title">👥 Participants</div>
            <div class="user-grid">
                {entrant_html or "<p>No Participants</p>"}
            </div>
        </body>
        </html>
        """

        buffer = BytesIO(html.encode("utf-8"))
        file = nc.File(buffer, filename=f"giveaway_transcript{self.giveaway_id}.html")

        await interaction.response.send_message(
            file=file,
            ephemeral=True
        )
