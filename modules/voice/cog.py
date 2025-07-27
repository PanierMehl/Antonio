import nextcord
from nextcord import Embed, Interaction, File, FFmpegPCMAudio, SlashOption, Locale
from nextcord.ext import commands
import tempfile
import config
from mysql_class import BotDB
import io
import asyncio
from gtts import gTTS
import yaml
from modules.voice.view import RadioDropdown


        
class Voice(commands.Cog, name="Voice Commands"):
    """Contains all voice commands"""

    COG_EMOJI = config.dc_vc
    
    def __init__(self, bot):
        self.bot = bot
        
    with open("trans.yaml", encoding="utf-8") as file:
        trans = yaml.safe_load(file)      


    @nextcord.slash_command(name="voice",
                            name_localizations={
                                Locale.de: "sprachkanal",
                                Locale.en_US: "voice"
                            })
    
    async def voice(self, inter: Interaction):
        pass


    @voice.subcommand(name="join", description="The bot joins your voice channel",
                      name_localizations={
                          Locale.de: "beitreten",
                          Locale.en_US: "join"},
                      description_localizations={
                          Locale.de: "Der Bot schließt sich deinem Sprachkanal an",
                          Locale.en_US: "The bot joins your voice channel"
                      })
    async def voice_join(self, inter: Interaction):
        data = BotDB().query_server_table(inter.guild.id)

        re_cannot_join = Embed(title=self.trans["commands"]["voice_join"]["re_cannot_join"]["title"][f"{inter.locale}"],
                               description=self.trans["commands"]["voice_join"]["re_cannot_join"]["description"][f"{inter.locale}"], colour=config.red)
        
        re_already_in_voice = Embed(title=self.trans["commands"]["voice_join"]["re_already_in_voice"]["title"][f"{inter.locale}"],
                                    description=self.trans["commands"]["voice_join"]["re_already_in_voice"]["description"][f"{inter.locale}"], colour=config.red)
        
        re_in_your_voice = Embed(title=self.trans["commands"]["voice_join"]["re_in_your_voice"]["title"][f"{inter.locale}"],
                                 description=self.trans["commands"]["voice_join"]["re_in_your_voice"]["description"][f"{inter.locale}"], colour=config.red)

        if inter.user.voice is None:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            re_cannot_join.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.send_message(file=cancel_error_png_a, embed=re_cannot_join, ephemeral=True)
            return False

        if inter.guild.voice_client:
            if inter.user.voice.channel.id != inter.guild.me.voice.channel.id:
                if data:
                    admin_role_id, moderator_role_id, supporter_role_id = data[1], data[2], data[3]
                    if admin_role_id:
                        admin_role = inter.guild.get_role(admin_role_id)
                    if moderator_role_id:
                        moderator_role = inter.guild.get_role(moderator_role_id)
                    if supporter_role_id:
                        supporter_role = inter.guild.get_role(supporter_role_id)

                    if admin_role and inter.user.get_role(admin_role.id) or moderator_role and inter.user.get_role(moderator_role.id) or supporter_role and inter.user.get_role(supporter_role.id):
                        await inter.response.defer(ephemeral=True)
                        vc = inter.guild.voice_client
                        
                        if inter.locale == "de":
                            try:
                                audio_source = nextcord.FFmpegPCMAudio("audios/antonio_modcall_de.mp3")
                                vc.play(audio_source)
                            except:
                                pass
                            
                        elif inter.locale == "en_US":
                            try:
                                audio_source = nextcord.FFmpegPCMAudio("audios/antonio_modcall_eng.mp3")
                                vc.play(audio_source)
                            except:
                                pass
                            
                        else:
                            try:
                                audio_source = nextcord.FFmpegPCMAudio("audios/antonio_modcall_eng.mp3")
                                vc.play(audio_source)
                            except:
                                pass
                            
                        while vc.is_playing():
                            await asyncio.sleep(1)
                            
                        await inter.guild.me.move_to(channel=inter.user.voice.channel, reason="A moderator called me")
                        
                        re_connected = Embed(title=self.trans["commands"]["voice_join"]["re_connected"]["title"][inter.locale].format(channel=inter.user.voice.channel.name, emoji=config.a_join),
                                             description=self.trans["commands"]["voice_join"]["re_connected"]["description"][inter.locale].format(jump_url=inter.user.voice.channel.jump_url), colour=config.dark_green)
                   
                        check_mark_maja_png = File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
                        re_connected.set_thumbnail(url="attachment://check_mark_maja.png")
                        await inter.edit_original_message(embed=re_connected, file=check_mark_maja_png)
                        return
                    
                    else:
                        cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                        re_already_in_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                        await inter.response.send_message(embed=re_already_in_voice, file=cancel_error_png_a)
                        return False
                
                else:
                    cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                    re_already_in_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                    await inter.response.send_message(embed=re_already_in_voice, ephemeral=True, file=cancel_error_png_a)
                    return False   
            else:
                cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                re_in_your_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                await inter.response.send_message(embed=re_in_your_voice, ephemeral=True, file=cancel_error_png_a)
                return False    

        elif inter.user.voice:
            await inter.response.defer(ephemeral=True)
            vc = await inter.user.voice.channel.connect()

            await inter.guild.change_voice_state(channel=inter.user.voice.channel, self_deaf=True)
            check_mark_maja_png = File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
            
            re_connected = Embed(title=self.trans["commands"]["voice_join"]["re_connected"]["title"][inter.locale].format(channel=inter.user.voice.channel.name, emoji=config.a_join),
                                 description=self.trans["commands"]["voice_join"]["re_connected"]["description"][inter.locale].format(jump_url=inter.user.voice.channel.jump_url), colour=config.dark_green)
                   
            re_connected.set_thumbnail(url="attachment://check_mark_maja.png")
            await inter.edit_original_message(embed=re_connected, file=check_mark_maja_png)
            if inter.locale == "de":
                audio_source = FFmpegPCMAudio("audios/antonio_hallo_de.mp3")
                vc.play(audio_source)
            elif inter.locale == "en_US":
                audio_source = FFmpegPCMAudio("audios/antonio_hello_eng.mp3")
                vc.play(audio_source)
            else:
                audio_source = FFmpegPCMAudio("audios/antonio_hello_eng.mp3")
                vc.play(audio_source)



    @voice.subcommand(name="reconnect", description="Reconnects to the voice channel",
                      name_localizations={
                          Locale.de: "wiederherstellen",
                          Locale.en_US: "reconnect"
                          },
                      description_localizations={
                        Locale.de: "Stellt die Verbindung zum Sprachkanal wieder her",
                        Locale.en_US: "Reconnects to the voice channel"
                      })
    async def voice_reconnect(self, inter: Interaction):

        re_sucess = Embed(title=self.trans["commands"]["voice_reconnect"]["re_sucess"]["title"][f"{inter.locale}"].format(emoji=config.a_join),
                          description=self.trans["commands"]["voice_reconnect"]["re_sucess"]["description"][f"{inter.locale}"], colour=config.dark_green)
        
        re_not_in_voice = Embed(title=self.trans["commands"]["voice_reconnect"]["re_not_in_voice"]["title"][f"{inter.locale}"],
                                description=self.trans["commands"]["voice_reconnect"]["re_not_in_voice"]["description"][f"{inter.locale}"], colour=config.red)
        
        re_wrong_voice = Embed(title=self.trans["commands"]["voice_reconnect"]["re_wrong_voice"]["title"][f"{inter.locale}"],
                               description=self.trans["commands"]["voice_reconnect"]["re_wrong_voice"]["description"][f"{inter.locale}"], colour=config.red)
        
        if inter.user.voice:
            if inter.user.voice.channel.id == inter.guild.me.voice.channel.id:
                data = BotDB().query_server_table(inter.guild.id)

                await inter.response.defer(ephemeral=True)
                await inter.guild.voice_client.disconnect()
                await asyncio.sleep(1)

                await inter.user.voice.channel.connect()
                vc = inter.guild.voice_client
                if inter.locale == "de":
                    audio_source = nextcord.FFmpegPCMAudio("audios/antonio_reconnect_de.mp3")
                    vc.play(audio_source)
                elif inter.locale == "en_US":
                    audio_source = nextcord.FFmpegPCMAudio("audios/antonio_reconnect_eng.mp3")
                    vc.play(audio_source)
                else:
                    audio_source = nextcord.FFmpegPCMAudio("audios/antonio_reconnect_eng.mp3")
                    vc.play(audio_source)
                while vc.is_playing():
                    await asyncio.sleep(1)
                check_mark_maja_png = File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
                re_sucess.set_thumbnail(url="attachment://check_mark_maja.png")
                await inter.edit_original_message(embed=re_sucess, file=check_mark_maja_png)


            else:
                cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                re_wrong_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                await inter.response.send_message(embed=re_wrong_voice, ephemeral=True, file=cancel_error_png_a)

        else:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            re_not_in_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.send_message(embed=re_not_in_voice, ephemeral=True, file=cancel_error_png_a)



    @voice.subcommand(name="leave", description="Leaves the current voice channel",
                      name_localizations={
                          Locale.de: "verlassen",
                          Locale.en_US: "leave"
                      },
                      description_localizations={
                          Locale.de: "Verlässt den aktuellen Sprachkanal",
                          Locale.en_US: "Leaves the current voice channel"
                      })
    async def voice_disconnect(self, inter: Interaction):

        re_sucess = Embed(title=self.trans["commands"]["voice_disconnect"]["re_sucess"]["title"][f"{inter.locale}"].format(emoji=config.a_leave), 
                          description=self.trans["commands"]["voice_disconnect"]["re_sucess"]["description"][f"{inter.locale}"], colour=config.dark_green)
        
        re_not_in_voice = Embed(title=self.trans["commands"]["voice_disconnect"]["re_not_in_voice"]["title"][f"{inter.locale}"],
                                description=self.trans["commands"]["voice_disconnect"]["re_not_in_voice"]["description"][f"{inter.locale}"], colour=config.red)
        
        re_wrong_voice = Embed(title=self.trans["commands"]["voice_disconnect"]["re_wrong_voice"]["title"][f"{inter.locale}"],
                               description=self.trans["commands"]["voice_disconnect"]["re_wrong_voice"]["description"][f"{inter.locale}"], colour=config.red)
        
        if inter.guild.voice_client:
            if inter.user.voice.channel.id == inter.guild.me.voice.channel.id:

                await inter.response.defer(ephemeral=True)
                vc = inter.guild.voice_client
                
                if inter.locale == "de":
                    try:
                        audio_source = nextcord.FFmpegPCMAudio("audios/antonio_aufwiedersehen_de.mp3")
                        vc.play(audio_source)
                    except:
                        pass
                    
                elif inter.locale == "en_US":
                    try:
                        audio_source = nextcord.FFmpegPCMAudio("audios/antonio_goodbye_eng.mp3")
                        vc.play(audio_source)
                    except:
                        pass
                    
                else:
                    try:
                        audio_source = nextcord.FFmpegPCMAudio("audios/antonio_goodbye_eng.mp3")
                        vc.play(audio_source)
                    except:
                        pass
                    
                while vc.is_playing():
                    await asyncio.sleep(3.5)
                    await vc.disconnect()
                    
                check_mark_maja_png = File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
                re_sucess.set_thumbnail(url="attachment://check_mark_maja.png")
                await inter.edit_original_message(embed=re_sucess, file=check_mark_maja_png)


            else:
                cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                re_wrong_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                await inter.response.send_message(embed=re_wrong_voice, ephemeral=True, file=cancel_error_png_a)

        else:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            re_not_in_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.send_message(embed=re_not_in_voice, ephemeral=True, file=cancel_error_png_a)



    @voice.subcommand(name="tts",description="Let the bot say something in a voice channel",
                      description_localizations={
                          Locale.de: "Lasse den Bot etwas in einem Sprachkanal sagen",
                          Locale.en_US: "Let the bot say something in a voice channel"
                      })
    async def voice_tts(self, inter: nextcord.Interaction,
                        channel: nextcord.VoiceChannel = SlashOption(name="channel", description="Playback voice channel", required=True, 
                                                                     name_localizations={Locale.de: "sprachkanal", Locale.en_US: "channel"},
                                                                     description_localizations={Locale.de: "Wiedergabe des Sprachkanals", Locale.en_US: "Playback voice channel"}),
                        voice_message: str = SlashOption(name="text", description="This text is played back by the bot in the voice channel", required=True, max_length=150,
                                                         description_localizations={Locale.de: "Dieser Text wird vom Bot im Sprachkanal wiedergegeben", Locale.en_US: "This text is played back by the bot in the voice channel"}),
                        language: str = SlashOption(name="language", description="The language in which the bot should play the text", required=False,
                                                    name_localizations={Locale.de: "sprache", Locale.en_US: "language"},
                                                    description_localizations={Locale.de: "Die Sprache, in der der Bot den Text wiedergeben soll", Locale.en_US: "The language in which the bot should play the text"},
                                                    choices={"English UK": "en-co.uk", "English US": "en-us", "German": "de-de", "French": "fr-fr", "Spanish": "es-es", "Mandarin": "zh-CN"},
                                                    choice_localizations={"English UK": {Locale.de:"Englisch UK", Locale.en_US: "English UK"},
                                                                          "English US": {Locale.de: "Englisch US", Locale.en_US: "English US"},
                                                                          "German": {Locale.de: "Deutsch", Locale.en_US: "German"},
                                                                          "French": {Locale.de: "Franzözisch", Locale.en_US: "French"},
                                                                          "Spanish": {Locale.de: "Spanisch", Locale.en_US: "Spanish"},
                                                                          "Mandarin": {Locale.de: "Mandarin", Locale.en_US: "Mandarin"}})):

        vc = inter.guild.voice_client
        if not vc:
            voice_client = await channel.connect()

        if not voice_client.is_playing():
            
            e_process = Embed(title=self.trans["commands"]["voice_tts"]["e_process"]["title"][f"{inter.locale}"].format(emoji=config.e_loading),
                              description=self.trans["commands"]["voice_tts"]["e_process"]["description"][f"{inter.locale}"].format(voice_message=voice_message, language=language), colour=config.yellow)
            
            e_done = Embed(title=self.trans["commands"]["voice_tts"]["e_done"]["title"][f"{inter.locale}"],
                           description=self.trans["commands"]["voice_tts"]["e_done"]["description"][f"{inter.locale}"].format(voice_message=voice_message, language=language), colour=config.green)
            
            await inter.response.send_message(embed=e_process, ephemeral=True)
            if language == None:
                lang = "en"
                tld = "co.uk"
            else:
                lang = str(language).split("-")[0]
                tld = str(language).split("-")[1]
        myobj = gTTS(text=voice_message, lang=lang, tld=tld, slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            myobj.write_to_fp(temp_file)
        try:
            audio_source = nextcord.FFmpegPCMAudio(temp_file.name)
            voice_client.play(audio_source)
            await asyncio.sleep(1)
            await voice_client.disconnect()
            await inter.edit_original_message(embed=e_done)
        except:
            e_fail = Embed(title=self.trans["commands"]["voice_tts"]["e_fail"]["title"][f"{inter.locale}"],
                           description=self.trans["commands"]["voice_tts"]["e_fail"]["description"][f"{inter.locale}"], colour=config.red)
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            e_fail.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await voice_client.disconnect()
            await inter.edit_original_message(embed=e_fail, file=cancel_error_png_a)
            

        
    @voice.subcommand(name="radio")
    async def voice_radio(self, inter: Interaction):
        
        if inter.user.voice is None:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            not_in_voice = Embed(title="Failed to play", description=f"You are not in a voice channel.", colour=config.red)
            not_in_voice.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.send_message(embed=not_in_voice, ephemeral=True, file=cancel_error_png_a)
            return
        
        # Überprüfe, ob der Bot im selben Sprachkanal wie der Nutzer ist
        voice_channel = inter.user.voice.channel
        voice_client = inter.guild.voice_client

        if voice_client and voice_client.is_connected():
            bot_in_channel = voice_client.channel
            if bot_in_channel == voice_channel:
                options = [
                    nextcord.SelectOption(label="2000er + Trowbacks", value="https://streams.ilovemusic.de/iloveradio37.mp3"),
                    nextcord.SelectOption(label="2010er + Trowbacks", value="https://streams.ilovemusic.de/iloveradio38.mp3"),
                    nextcord.SelectOption(label="Bass", value="https://streams.ilovemusic.de/iloveradio29.mp3"),
                    nextcord.SelectOption(label="Chillout Beats", value="https://streams.ilovemusic.de/iloveradio17.mp3"),
                    nextcord.SelectOption(label="DJs from Mars", value="https://play.ilovemusic.de/ilovedjsfrommars"),
                    nextcord.SelectOption(label="Dance", value="https://streams.ilovemusic.de/iloveradio2.mp3"),
                    nextcord.SelectOption(label="Dance  History", value="https://streams.ilovemusic.de/iloveradio26.mp3"),
                    nextcord.SelectOption(label="Dance 2024", value="https://streams.ilovemusic.de/iloveradio36.mp3"),
                    nextcord.SelectOption(label="Dace First!", value="https://streams.ilovemusic.de/iloveradio103.mp3"),
                    nextcord.SelectOption(label="Deutschrap Beste", value="https://streams.ilovemusic.de/iloveradio6.mp3"),
                    nextcord.SelectOption(label="Deutschrap First", value="https://streams.ilovemusic.de/iloveradio104.mp3"),
                    nextcord.SelectOption(label="Greatest Hits", value="https://streams.ilovemusic.de/iloveradio16.mp3"),
                    nextcord.SelectOption(label="Hardstyle", value="https://streams.ilovemusic.de/iloveradio21.mp3"),
                    nextcord.SelectOption(label="Hip Hop", value="https://streams.ilovemusic.de/iloveradio3.mp3"),
                    nextcord.SelectOption(label="Hip Hop 2024", value="https://streams.ilovemusic.de/iloveradio35.mp3"),
                    nextcord.SelectOption(label="Hip Hop History", value="https://streams.ilovemusic.de/iloveradio27.mp3"),
                    nextcord.SelectOption(label="Hits 2024", value="https://streams.ilovemusic.de/iloveradio109.mp3"),
                    nextcord.SelectOption(label="Hits History", value="https://streams.ilovemusic.de/iloveradio12.mp3"),
                    nextcord.SelectOption(label="Mainstage", value="https://streams.ilovemusic.de/iloveradio22.mp3"),
                    nextcord.SelectOption(label="Malle", value="https://streams.ilovemusic.de/iloveradio25.mp3"),
                    nextcord.SelectOption(label="Mashup", value="https://streams.ilovemusic.de/iloveradio5.mp3"),
                    nextcord.SelectOption(label="Mix Radio", value="https://play.ilovemusic.de/ilm_iloveradio/"),
                    nextcord.SelectOption(label="Music & Chill", value="https://streams.ilovemusic.de/iloveradio10.mp3"),
                    nextcord.SelectOption(label="Party Hard", value="https://streams.ilovemusic.de/iloveradio14.mp3"),
                    nextcord.SelectOption(label="Pop Hits", value="https://play.ilovemusic.de/ilovebiggestpophits"),
                    nextcord.SelectOption(label="Rock Radio", value="https://play.ilovemusic.de/iloverockradio"),
                    nextcord.SelectOption(label="Sugar Radio", value="https://streams.ilovemusic.de/iloveradio18.mp3"),
                    nextcord.SelectOption(label="The 90s", value="https://streams.ilovemusic.de/iloveradio24.mp3"),
                    nextcord.SelectOption(label="The Beach", value="https://streams.ilovemusic.de/iloveradio7.mp3"),
                    nextcord.SelectOption(label="The Sun", value="https://streams.ilovemusic.de/iloveradio15.mp3"),
                    nextcord.SelectOption(label="Top 100 Charts", value="https://streams.ilovemusic.de/iloveradio9.mp3"),
                    nextcord.SelectOption(label="Trashpop", value="https://streams.ilovemusic.de/iloveradio19.mp3"),
                    nextcord.SelectOption(label="Tylor & Harry", value="https://play.ilovemusic.de/ilovetaylorandharry"),
                    nextcord.SelectOption(label="Tommorowland", value="https://play.ilovemusic.de/ilm-itomorrowland_one_world_radio_germany/"),
                    nextcord.SelectOption(label="US only Rap Radio", value="https://streams.ilovemusic.de/iloveradio13.mp3"),
                    nextcord.SelectOption(label="Workout", value="https://streams.ilovemusic.de/iloveradio23.mp3"),
                    nextcord.SelectOption(label="XMAs", value="https://streams.ilovemusic.de/iloveradio8.mp3")]
            
                await inter.response.send_message(view=RadioDropdown(options, voice_client), ephemeral=True)
                
            else:
                cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                not_same = Embed(title="Failed to play", description="You are currently in a different voice channel to me.\n"
                                 "I am currently entertaining other users in A. You can use me if I am not in another language channel.", colour=config.red)
                not_same.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                await inter.response.send_message(embed=not_same, ephemeral=True, file=cancel_error_png_a)
        else:
            options = [
                nextcord.SelectOption(label="2000er + Trowbacks", value="https://streams.ilovemusic.de/iloveradio37.mp3"),
                nextcord.SelectOption(label="2010er + Trowbacks", value="https://streams.ilovemusic.de/iloveradio38.mp3"),
                nextcord.SelectOption(label="Bass", value="https://streams.ilovemusic.de/iloveradio29.mp3"),
                nextcord.SelectOption(label="Chillout Beats", value="https://streams.ilovemusic.de/iloveradio17.mp3"),
                nextcord.SelectOption(label="DJs from Mars", value="https://play.ilovemusic.de/ilovedjsfrommars"),
                nextcord.SelectOption(label="Dance", value="https://streams.ilovemusic.de/iloveradio2.mp3"),
                nextcord.SelectOption(label="Dance  History", value="https://streams.ilovemusic.de/iloveradio26.mp3"),
                nextcord.SelectOption(label="Dance 2024", value="https://streams.ilovemusic.de/iloveradio36.mp3"),
                nextcord.SelectOption(label="Dace First!", value="https://streams.ilovemusic.de/iloveradio103.mp3"),
                nextcord.SelectOption(label="Deutschrap Beste", value="https://streams.ilovemusic.de/iloveradio6.mp3"),
                nextcord.SelectOption(label="Deutschrap First", value="https://streams.ilovemusic.de/iloveradio104.mp3"),
                nextcord.SelectOption(label="Greatest Hits", value="https://streams.ilovemusic.de/iloveradio16.mp3"),
                nextcord.SelectOption(label="Hardstyle", value="https://streams.ilovemusic.de/iloveradio21.mp3"),
                nextcord.SelectOption(label="Hip Hop", value="https://streams.ilovemusic.de/iloveradio3.mp3"),
                nextcord.SelectOption(label="Hip Hop 2024", value="https://streams.ilovemusic.de/iloveradio35.mp3"),
                nextcord.SelectOption(label="Hip Hop History", value="https://streams.ilovemusic.de/iloveradio27.mp3"),
                nextcord.SelectOption(label="Hits 2024", value="https://streams.ilovemusic.de/iloveradio109.mp3"),
                nextcord.SelectOption(label="Hits History", value="https://streams.ilovemusic.de/iloveradio12.mp3"),
                nextcord.SelectOption(label="Mainstage", value="https://streams.ilovemusic.de/iloveradio22.mp3"),
                nextcord.SelectOption(label="Malle", value="https://streams.ilovemusic.de/iloveradio25.mp3"),
                nextcord.SelectOption(label="Mashup", value="https://streams.ilovemusic.de/iloveradio5.mp3"),
                nextcord.SelectOption(label="Mix Radio", value="https://play.ilovemusic.de/ilm_iloveradio/"),
                nextcord.SelectOption(label="Music & Chill", value="https://streams.ilovemusic.de/iloveradio10.mp3"),
                nextcord.SelectOption(label="Party Hard", value="https://streams.ilovemusic.de/iloveradio14.mp3"),
                nextcord.SelectOption(label="Pop Hits", value="https://play.ilovemusic.de/ilovebiggestpophits"),
                nextcord.SelectOption(label="Rock Radio", value="https://play.ilovemusic.de/iloverockradio"),
                nextcord.SelectOption(label="Sugar Radio", value="https://streams.ilovemusic.de/iloveradio18.mp3"),
                nextcord.SelectOption(label="The 90s", value="https://streams.ilovemusic.de/iloveradio24.mp3"),
                nextcord.SelectOption(label="The Beach", value="https://streams.ilovemusic.de/iloveradio7.mp3"),
                nextcord.SelectOption(label="The Sun", value="https://streams.ilovemusic.de/iloveradio15.mp3"),
                nextcord.SelectOption(label="Top 100 Charts", value="https://streams.ilovemusic.de/iloveradio9.mp3"),
                nextcord.SelectOption(label="Trashpop", value="https://streams.ilovemusic.de/iloveradio19.mp3"),
                nextcord.SelectOption(label="Tylor & Harry", value="https://play.ilovemusic.de/ilovetaylorandharry"),
                nextcord.SelectOption(label="Tommorowland", value="https://play.ilovemusic.de/ilm-itomorrowland_one_world_radio_germany/"),
                nextcord.SelectOption(label="US only Rap Radio", value="https://streams.ilovemusic.de/iloveradio13.mp3"),
                nextcord.SelectOption(label="Workout", value="https://streams.ilovemusic.de/iloveradio23.mp3"),
                nextcord.SelectOption(label="XMAs", value="https://streams.ilovemusic.de/iloveradio8.mp3")]
            
            voice_client = await inter.user.voice.channel.connect()
            await inter.response.send_message(view=RadioDropdown(options, voice_client), ephemeral=True)
            
      
def setup(bot: commands.Bot):

    bot.add_cog(Voice(bot))