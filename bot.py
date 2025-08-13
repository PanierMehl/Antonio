import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import random

import cooldowns
import nextcord
import pytz
import time
from cooldowns import CallableOnCooldown
from dotenv import load_dotenv
from nextcord import (ApplicationCheckFailure, ApplicationError,
                      ApplicationInvokeError, NotFound, Embed, Interaction, )
from nextcord.ext import commands, tasks

import asyncio 
import config
from rich.markdown import Markdown
from rich.console import Console
from rich.table import Table
#from discord.ext.ipc import Server, ClientPayload
from modules.ticket_system.view import TicketMain_One_V2, TicketMain_Two_V2, TicketMain_Three_V2
from modules.admin.view import join_giveawy_en, join_giveawy_de, TranscriptButton_de, TranscriptButton_en
from mysql_asyncmy import A_DB


'''
import asyncio
asyncio.get_event_loop().set_debug(True)


import logging
logging.basicConfig(level=logging.DEBUG)
'''

cwd = Path(__file__).parents[0]
cwd = str(cwd)
    

    
def main():
    bot = commands.Bot(intents=nextcord.Intents.all(), help_command=None, case_insensitive=True)
    ##

    load_dotenv()
    
    bot.config_token = os.getenv("BOT_TOKEN")

    bot.cwd = cwd
    #ipc = Server(bot=bot, secret_key="lol")
    
##################################################################################################################################################################  
    
    # load all cogs
    for folder in os.listdir(os.getcwd() + "/modules"):
        if os.path.exists(os.path.join(os.getcwd() + "/modules", folder, "cog.py")):
            bot.load_extension(f"modules.{folder}.cog")
            
    # load detections
    for folder in os.listdir(os.getcwd() + "/cogs"):
        if os.path.exists(os.path.join(os.getcwd() + "/cogs", folder, "ghost_ping.py")):
            bot.load_extension(f"cogs.{folder}.ghost_ping")
    

    
##################################################################################################################################################################
    """        
    @Server.route()
    async def guild_count(self, _):
        return str(len(self.guilds))
    

    @Server.route()
    async def bot_guilds(self, _):
        guild_ids = [str(guild.id) for guild in self.guilds]
        return {"data": guild_ids}


    @Server.route()
    async def guild_stats(self, data: ClientPayload):
        guild = self.get_guild(data.guild_id)
        if not guild:
            return {
                "member_count": "Unbekannt",
                "name": "Unbekannt"
            }
        
        return {
            "member_count": guild.member_count,
            "name": guild.name,
        }


    async def on_ipc_error(self, endpoint: str, exc: Exception) -> None:
        raise exc  """
    #########################################################################
    persistent_view_added = False

    @bot.listen('on_ready')
    async def on_ready():
        
        bot.db = A_DB()
        await bot.db.connect()
        await bot.db.create_tables()
        print(await bot.db.query_server_table("900100165397008465"))
        
        nonlocal persistent_view_added
        if not persistent_view_added:
            for guild in bot.guilds:
                
                ts_query = await bot.db.query_ticket_system(guild.id)
                if ts_query is not None:
                    if ts_query[1] == "1":
                        bot.add_view(TicketMain_One_V2(ts_query[5], ts_query[0], ts_query[8]))
                    if ts_query[1] == "2":
                        bot.add_view(TicketMain_Two_V2(ts_query[5], ts_query[6], ts_query[0], ts_query[8], ts_query[9]))
                    if ts_query[1] == "3":
                        bot.add_view(TicketMain_Three_V2(ts_query[5], ts_query[6], ts_query[7], ts_query[0], ts_query[8], ts_query[9], ts_query[10]))

                buttons_query = await bot.db.query_buttons(guild.id)
                if buttons_query is not None:
                    for buttons in buttons_query:
                        if buttons[0] == "en":
                            bot.add_view(join_giveawy_en(buttons[5], buttons[2]))
                        if buttons[0] == "de":
                            bot.add_view(join_giveawy_de(buttons[5], buttons[2]))
                

            persistent_view_added = True

        console = Console()
        #await ipc.start()
        #Markdown
        startup = f"""# {bot.user.name}#{bot.user.discriminator} is starting up"""
        w_b = Markdown(startup)
        console.print(w_b)

        #Table
        command_table = Table(leading=1 , header_style="cyan2", border_style="white")
        command_table.add_column("Time", style="magenta",  width=30)
        command_table.add_column("Command", style="dark_green",  width=30, justify="center")
        command_table.add_column("Status", style="blue3", justify="right")
        command_table.add_column("IS Global?", style="blue3", justify="right", width=15)
        
        for cmd in bot.get_all_application_commands():
            command_table.add_row(f"{str(datetime.now())[:16]}", f"{cmd.name}", "Loaded", f"[green]YES[/]" if cmd.is_global else "[red]NO[/]")
            if cmd.children:                
                
                for sub in cmd.children:
                    command_table.add_row(f"{str(datetime.now())[:16]}", f"{sub}", "Loaded", f"Subcommand of {cmd.name}")
            else:
                pass
        console.print(command_table)

        #Loop Start
        check_giveaway_ending.start()
        change_presence.start()
         
    #########################################################################
    
    @bot.listen('on_guild_join')
    async def on_guild_join(guild):
        
        file = nextcord.File("GIFS/AddingBot.gif", filename="AddingBot.gif")
        
        information_embed = nextcord.Embed(title=f"Thanks for adding {config.BOT_NAME} {config.dc_bots} to your Server",
                                           description="I Hope you enjoy the Bot")
        information_embed.add_field(name="BOT Infos",
                                    value=f"The Bot is currently at V2.0\n"
                                    f"{config.VERSION}\n"
                                    f"Made by: PanierMehl")
        information_embed.add_field(name="Current Features:", value=
                                    "Information Commands\n"
                                    "Moderation Command\n"
                                    "Level 1 and Level 2 command acees roles\n"
                                    "Ticket System\n")
        
        information_embed.add_field(name="Planed Features:",
                                    value=f"Custom Voice (only one per server)\n"
                                    "Audith Log\n"
                                    "Warn Commands")
        information_embed.set_image(url="attachment://AddingBot.gif")
        
        channel = guild.system_channel or guild.text_channels[0]
        await channel.send(file=file, embed=information_embed)
        
    #########################################################################
    
    @bot.listen('on_application_command_error')
    async def on_application_command_error(interaction: nextcord.Interaction, error):
        error = getattr(error, "original", error)

        # Ignore Check Failure
        if isinstance(error, ApplicationCheckFailure):
            return

        # Handle Cooldown Errors
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = nextcord.Embed(
                description=f"⏳ This command is on cooldown! Try again in `{error.retry_after:.1f}` seconds.",
                colour=0xE74C3C
            )
            try:
                await interaction.response.send_message(embed=cooldown_embed, ephemeral=True)
            except nextcord.InteractionResponded:
                await interaction.followup.send(embed=cooldown_embed, ephemeral=True)
            return

        # Ignore NotFound (e.g. user deleted message)
        if isinstance(error, NotFound):
            return

        # Debugging-Ausgabe in der Konsole:
        print("=== Application Command Error Debug ===")
        print(f"Guild: {interaction.guild.name if interaction.guild else 'DM'} (ID: {interaction.guild.id if interaction.guild else 'N/A'})")
        print(f"User: {interaction.user} (ID: {interaction.user.id})")
        print(f"Command: {interaction.application_command.qualified_name if interaction.application_command else 'Unknown'}")
        print(f"Error Type: {type(error).__name__}")
        import traceback
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        print(tb)
        print("=== End of Debug ===")

        # Send error to log channel
        error_channel = interaction.client.get_channel(1084273834305265737)
        error_name = str(error)[:90]

        error_embed = nextcord.Embed(
            title=f"Error in {interaction.guild.name if interaction.guild else 'DM'}",
            description=f"```py\n{tb[:1020]}```",
            colour=0xE74C3C
        )

        # Add context details
        error_embed.add_field(name="Command", value=interaction.application_command.qualified_name if interaction.application_command else "Unknown", inline=False)
        error_embed.add_field(name="User", value=f"{interaction.user} ({interaction.user.id})", inline=False)
        error_embed.add_field(name="Error", value=str(error), inline=False)

        thread = await error_channel.create_thread(name=f"Error: {error_name}", embed=error_embed)
        await thread.send(content="<@&903363204200140831>")  # Notify staff

        # Notify the user
        user_msg = "⚠️ An unexpected error occurred. Our team has been notified and will look into it. Thank you for your understanding!"
        try:
            await interaction.response.send_message(content=user_msg, ephemeral=True)
        except nextcord.InteractionResponded:
            await interaction.followup.send(content=user_msg, ephemeral=True)



######################################################################################################
    @bot.listen('on_message')
    async def on_message(message: nextcord.Message):
        if message.author == bot.user:
            return
        
        if message.author.bot:
            return
        
        if message.webhook_id is not None:
            return

        #https://docs.nextcord.dev/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working
        #bot.process_commands(message)
         
                 
        word_count = len(message.content.split())
        message_length = len(message.content) 
        multiplier = 0.7
        if word_count < 4:
            if message_length != 0:
                total_message_xp = (word_count * multiplier) / message_length
            else:
                total_message_xp = 0
        elif 4 <= word_count <= 15:
            total_message_xp = (message_length * multiplier) / word_count
        elif 15 <= word_count <= 25:
            total_message_xp = (message_length * multiplier) / 3.75
        elif word_count > 26:
            total_message_xp = (message_length * multiplier) / (word_count / 2)
            

        guild = message.guild.id
        user = message.author.id
        
        level_thresholds = [20, 50, 75, 100, 150, 250, 400, 650, 800, 1000]
        
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        stats = await bot.db.level_user_query(user, guild)
        
        if stats is None:
            await bot.db.level_insert_new_user(user, guild)
            return
                    
        old_xp_count = float(stats[0] or 0)
        old_level = float(stats[1] or 0)
        
        if stats[2] is not None:
            last_entry = stats[2]
            time_difference = current_datetime - last_entry
                                        
            if time_difference >= timedelta(seconds=30):
                new_xp_count = total_message_xp + old_xp_count
                rounded_xp_count = round(new_xp_count, 2)
                new_lvl = sum(1 for threshold in level_thresholds if new_xp_count >= threshold) + 1
                
                if old_level != new_lvl:
                    await message.channel.send(content=f"Level UP {message.author.mention}. You are now Level {new_lvl}", delete_after=10)
                await bot.db.level_user_update(rounded_xp_count, new_lvl, formatted_datetime, user, guild)
                return
            else:
                pass
                
        else:
            new_xp_count = total_message_xp + old_xp_count
            rounded_xp_count = round(new_xp_count, 2)
            
            new_lvl = sum(1 for threshold in level_thresholds if new_xp_count >= threshold) + 1
            
            if old_level < new_lvl:
                await message.channel.send(content=f"Level UP {message.author.mention}. You are now Level {new_lvl}", delete_after=10)
            await bot.db.level_user_update(rounded_xp_count, new_lvl, formatted_datetime, user, guild)
            return
                        
                
    
            
        # G L O B A L - C H A T
    
        _check_global_exists = await bot.db.query_server_table(message.guild.id)
                                    
        channel = message.channel
        if _check_global_exists is None:
            return
        
        if _check_global_exists is not None:
            _get_all_global_ids = await bot.db.query_all_global_channels()
            
            
            if channel.id == _check_global_exists[4]:
                
                inv = await message.channel.create_invite(unique=False)
                link_bot_invite = '[Invite Bot](https://discord.com/api/oauth2/authorize?client_id=1026298999369650216&permissions=8&scope=bot%20applications.commands)'
                link_server = f'[Go to Server]({inv})'
                
                for channel_id in map(lambda data: data[0], _get_all_global_ids):
                    if channel_id == None:
                        continue
                    else:
                        try:
                            c = bot.get_channel(int(channel_id))
                            if c:
                                guild: nextcord.Guild = bot.get_guild(c.guild.id)
                                perms: nextcord.Permissions = c.permissions_for(guild.get_member(bot.user.id))
                                if perms.send_messages and perms.attach_files and perms.embed_links and perms.external_emojis:
                                    de = pytz.timezone('Europe/Berlin')
                                    ge = nextcord.Embed(description=f"{message.content}\n\n{link_bot_invite} ║ {link_server}", timestamp=datetime.now().astimezone(tz=de), color=message.author.color)
                                    ge.set_footer(text=message.guild.name, icon_url=message.guild.icon)
                                    ge.set_author(name=message.author, icon_url=message.author.display_avatar.url)

                                    await c.send(embed=ge)
                                else:
                                    continue
                                
                        except nextcord.Forbidden:
                            continue
                        except nextcord.HTTPException:
                            continue
                                            
                await message.delete()
                return
        
            else:
                return
                
                
            
            
    @bot.event
    async def on_guild_channel_delete(channel: nextcord.abc.GuildChannel):
        check = await bot.db.query_ticket_informations(channel.id)
        if check is not None:
            await bot.db.delete_ticket(channel.id, channel.guild.id)
            return True
        else:
            pass     
    
    
    @tasks.loop(seconds=10)
    async def change_presence():
        statuses = [
            nextcord.Activity(type=nextcord.ActivityType.competing, name="to beat other Bots"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="Antonio's Radio"),
            nextcord.Activity(type=nextcord.ActivityType.watching, name="your Server"),
            nextcord.Activity(type=nextcord.ActivityType.watching, name="on my best creater: @garniermehl"),
            nextcord.Activity(type=nextcord.ActivityType.playing, name=f"Version {config.VERSION}")
        ]

        # Wähle zufällig einen Status aus der Liste aus
        new_status = random.choice(statuses)
        await bot.change_presence(activity=new_status)



    @tasks.loop(seconds=0.5)
    async def check_giveaway_ending():
        current_time = datetime.now(timezone.utc)  # Zeit mit Zeitzoneninfo
        giveaways = await bot.db.get_giveaway_ending()
        for giveaway in giveaways:
            if giveaway is None:
                continue
            
            giveaway_end_time = datetime.fromtimestamp(giveaway[0], tz=timezone.utc)
            message_id = giveaway[1]
            guild_id = giveaway[2]
            channel_id = giveaway[3]
            giveaway_id = giveaway[4]
            prize = giveaway[5]
            participants_data = giveaway[6]
            winners = giveaway[7]
            finished = giveaway[8]
            
            time_since_end = current_time - giveaway_end_time
            if time_since_end >= timedelta(hours=12):
                await bot.db.remove_giveaway(giveaway_end_time, guild_id)
                
            elif timedelta(seconds=1) <= time_since_end <= timedelta(seconds=749):
                
                if finished == 1:
                    continue
                else:
                    winners_tuple = await bot.db.determine_winners(giveaway_id)
                    winners_str = winners_tuple[0]
                    num_winners = winners_tuple[1]
                    await bot.db.mark_giveaway_as_finished(giveaway_id, True)
                    
                    guild = bot.get_guild(guild_id)
                    if guild:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            try:
                                message = channel.get_partial_message(message_id)
                                
                                if winners_str is None:
                                    embed = nextcord.Embed(title="🎉 Giveaway ended 🎉", description="The giveaway has ended, no further participation is possible!", colour=config.red)
                                    embed.add_field(name="Winners", value="No Winners\n\uFEFF")
                                    embed.add_field(name="Prize:", value=f"{prize}\n\uFEFF")
                                    embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
                                    await message.edit(embed=embed, view=None)
                                    return
                            
                                
                                participants_str = participants_data

                                if participants_str is None:
                                        participants = []
                                else:
                                    try:
                                        participants = json.loads(participants_str)
                                    except json.JSONDecodeError:
                                        participants = []
                    
                                            
                                            
                                winners_list = winners_str.strip("[]").split(", ")
                                selected_winners = random.sample(winners_list, min(num_winners, len(winners_list)))


                                winner_mentions = ', '.join(f"<@{winner_id.strip()}>" for winner_id in selected_winners)
                                l = await bot.db.query_server_table(guild_id)
                                if l is not None:
                                    if l[5] == "English":
                                        view = TranscriptButton_en(participants_data, winner_mentions, giveaway_id, prize, time.time(), winners)
                                        embed = nextcord.Embed(title="🎉 Giveaway ended 🎉", description="The giveaway has ended, no further participation is possible!", colour=config.red)
                                        embed.add_field(name="Winners", value=f"{winner_mentions}\n\uFEFF")
                                        embed.add_field(name="Prize", value=f"{prize}\n\uFEFF")
                                        embed.add_field(name="Entries", value=f"{len(participants)}\n\uFEFF")
                                        embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
                                        await message.edit(embed=embed, view=view)
                                        
                                        await channel.send(content=f"{winner_mentions} has won the giveaway `{giveaway_id}`. Congratulations.")
                                        
                                    elif l[5] == "German":
                                        view = TranscriptButton_de(participants_data, winner_mentions, giveaway_id, prize, time.time(), winners)
                                        embed = nextcord.Embed(title="🎉 Gewinnspiel beendet 🎉", description="Das Gewinnspiel ist beendet, eine weitere Teilnahme ist nicht möglich!", colour=config.red)
                                        embed.add_field(name="Gewinner", value=f"{winner_mentions}\n\uFEFF")
                                        embed.add_field(name="Preis", value=f"{prize}\n\uFEFF")
                                        embed.add_field(name="Teilnehmer", value=f"{len(participants)}\n\uFEFF")
                                        embed.set_footer(text=f"Gewinnspiel ID: {giveaway_id}")
                                        await message.edit(embed=embed, view=view)
                                        
                                        await channel.send(content=f"{winner_mentions} hat das Gewinnspiel `{giveaway_id}` gewonnen. Glückwunsch.")
                                        
                                else:
                                    view = TranscriptButton_en(participants_data, winner_mentions, giveaway_id, prize, time.time(), winners)
                                    embed = nextcord.Embed(title="🎉 Giveaway ended 🎉", description="The giveaway has ended, no further participation is possible!", colour=config.red)
                                    embed.add_field(name="Winners", value=f"{winner_mentions}\n\uFEFF")
                                    embed.add_field(name="Prize", value=f"{prize}\n\uFEFF")
                                    embed.add_field(name="Entries", value=f"{len(participants)}\n\uFEFF")
                                    embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
                                    await message.edit(embed=embed, view=view)
                                    
                                    await channel.send(content=f"{winner_mentions} has won the giveaway `{giveaway_id}`. Congratulations.")
                                
                            except nextcord.NotFound:
                                return
                            except nextcord.Forbidden:
                                return
                            except nextcord.HTTPException as e:
                                return
                            
            elif time_since_end > timedelta(seconds=750):
                continue 
                
                


######################################################################################################


                
    bot.run(bot.config_token)

if __name__ == '__main__':
    main()
    



    