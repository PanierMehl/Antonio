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
        self.radio_stations = {
            "I Love Radio": "https://play.ilovemusic.de/ilm_iloveradio/",
            "I Love 2 Dance": "https://play.ilovemusic.de/ilm_ilove2dance/",
            "2000er + Throwbacks": "https://play.ilovemusic.de/ilm_ilove2000throwbacks/",
            "2010er + Throwbacks": "https://play.ilovemusic.de/ilm_ilove2010throwbacks/",
            "Bass by HBZ": "https://play.ilovemusic.de/ilm_ilovebass/",
            "I Love Biggest Pop Hits": "https://play.ilovemusic.de/ilm_ilovenewpop/",
            "I Love Chillpop": "https://play.ilovemusic.de/ilm_ilovechillhop/",
            "I Love Chillout Beats": "https://play.ilovemusic.de/ilm-ichillout_beats/",
            "I Love Dance 2025": "https://play.ilovemusic.de/ilm_dance-2023-jahrescharts/",
            "I Love Dance First!": "https://play.ilovemusic.de/ilm-dance_first/",
            "I Love Dance History": "https://play.ilovemusic.de/ilm_ilovedancehistory/",
            "I Love Deutschrap Beste": "https://play.ilovemusic.de/ilm_ilovedeutschrapbeste/",
            "I Love Deutschrap First!": "https://play.ilovemusic.de/ilm_ilovedeutschrapfirst/",
            "I Love From Mars": "https://play.ilovemusic.de/ilm_iloveradiofrommars/",
            "I Love Greatest Hits": "https://play.ilovemusic.de/ilm_ilovegreatesthits/",
            "I Love Hardstyle": "https://play.ilovemusic.de/ilm_ilovehardstyle/",
            "I Love Hip Hop": "https://play.ilovemusic.de/ilm_ilovehiphop/",
            "I Love Hip Hop 2025": "https://play.ilovemusic.de/ilm_hiphop-2023-jahrescharts/",
            "I Love Hip Hop History": "https://play.ilovemusic.de/ilm_ilovehiphophistory/",
            "I Love Hit Quiz": "https://play.ilovemusic.de/ilm-ihit-quiz/",
            "I Love Hits 2025": "https://play.ilovemusic.de/ilm_hits-2023-jahrescharts/",
            "I Love Hits History": "https://play.ilovemusic.de/ilm_ilovehitshistory/",
            "I Love Mainstage": "https://play.ilovemusic.de/ilm_ilovemainstagemadness/",
            "I Love Malle": "https://play.ilovemusic.de/ilm_ilovemalle/",
            "I Love Mashup": "https://play.ilovemusic.de/ilm_ilovemashup/",
            "I Love Music & Chill": "https://play.ilovemusic.de/ilm_ilovemusicandchill/",
            "I Love Party Hard": "https://play.ilovemusic.de/ilm_ilovepartyhard/",
            "I Love Rock Radio": "https://play.ilovemusic.de/ilm_iloveradiorock/",
            "I Love Sugar Radio": "https://play.ilovemusic.de/ilm_ilovesugarradio/",
            "I Love The 90s": "https://play.ilovemusic.de/ilm_ilovethe90s/",
            "I Love The Beach": "https://play.ilovemusic.de/ilm_ilovethebeach/",
            "I Love The Sun": "https://play.ilovemusic.de/ilm_ilovethesun/",
            "I Love Tomorrowland": "https://play.ilovemusic.de/ilm-itomorrowland_one_world_radio_germany/",
            "I Love Top 100 Charts": "https://play.ilovemusic.de/ilm_ilovetop100charts/",
            "I Love Trash Pop": "https://play.ilovemusic.de/ilm_ilovetrashpop/",
            "I Love US Rap Radio": "https://play.ilovemusic.de/ilm_iloveusonlyrapradio/",
            "I Love Workout": "https://play.ilovemusic.de/ilm_iloveworkout/",
            "I Love XMAS": "https://play.ilovemusic.de/ilm_ilovexmas/",
            "Radio Bob": "https://streams.radiobob.de/bob-live/mp3-192/streams.radiobob.de/",
            "1Live": "https://wdr-edge-1043-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3",
            "Antenne Bayern": "https://stream.antenne.de/antenne",
            "Radio NRW": "https://stream.lokalradio.nrw/stream.mp3",
            "Deutschlandfunk": "https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3"
        }

    async def radio_autocomplete(self, inter: Interaction, current: str):
        """Autocomplete für Radiosender"""
        return [
                        name
                        for name in self.radio_stations.keys()
                        if current.lower() in name.lower()
                    ][:25]

    @nextcord.slash_command(name="voice", description="Voice-Befehle")
    async def voice(self, inter: Interaction):
        pass

    @voice.subcommand(name="radio", description="Spielt ein Radio im Voice-Channel")
    async def voice_radio(
        self,
        inter: Interaction,
        sender: str = SlashOption(
            name="sender",
            description="Wähle den Radiosender",
            autocomplete=True,
        ),
    ):
        if inter.user.voice is None:
            await inter.response.send_message("❌ Du bist in keinem Voice-Channel.", ephemeral=True)
            return

        voice_channel = inter.user.voice.channel
        voice_client = inter.guild.voice_client

        if voice_client and voice_client.is_connected() and voice_client.channel != voice_channel:
            await inter.response.send_message("❌ Ich bin bereits in einem anderen Channel.", ephemeral=True)
            return

        if not voice_client:
            voice_client = await voice_channel.connect()

        # Stream URL ermitteln
        stream_url = self.radio_stations.get(sender)
        if not stream_url:
            await inter.response.send_message("❌ Ungültiger Radiosender.", ephemeral=True)
            return

        voice_client.stop()
        voice_client.play(nextcord.FFmpegPCMAudio(stream_url))
        await inter.response.send_message(f"▶ **Spiele jetzt:** `{sender}`")

    @voice_radio.on_autocomplete("sender")
    async def radio_autocomplete_handler(self, inter: Interaction, current: str):
        choices = await self.radio_autocomplete(inter, current)
        await inter.response.send_autocomplete(choices)

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
            

'''        
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
                    nextcord.SelectOption(label="I Love Radio", value="https://play.ilovemusic.de/ilm_iloveradio/"),
                    nextcord.SelectOption(label="I Love 2 Dance", value="https://play.ilovemusic.de/ilm_ilove2dance/"),
                    nextcord.SelectOption(label="2000er + Trowbacks", value="https://play.ilovemusic.de/ilm_ilove2000throwbacks/"),
                    nextcord.SelectOption(label="2010er + Trowbacks", value="https://play.ilovemusic.de/ilm_ilove2010throwbacks/"),
                    nextcord.SelectOption(label="Bass by HBZ", value="https://play.ilovemusic.de/ilm_ilovebass/"),
                    nextcord.SelectOption(label="I Love Biggest Pop Hits", value="https://play.ilovemusic.de/ilm_ilovenewpop/"),
                    nextcord.SelectOption(label="I Love Chillpop", value="https://play.ilovemusic.de/ilm_ilovechillhop/"),
                    nextcord.SelectOption(label="I Love Chillout Beats", value="https://play.ilovemusic.de/ilm-ichillout_beats/"),
                    nextcord.SelectOption(label="I Love Dance 2025", value="https://play.ilovemusic.de/ilm_dance-2023-jahrescharts/"),
                    nextcord.SelectOption(label="I Love Dance First!", value="https://play.ilovemusic.de/ilm-dance_first/"),
                    nextcord.SelectOption(label="I Love Dance History", value="https://play.ilovemusic.de/ilm_ilovedancehistory/"),
                    nextcord.SelectOption(label="I Love Deutschrap Beste", value="https://play.ilovemusic.de/ilm_ilovedeutschrapbeste/"),
                    nextcord.SelectOption(label="I Love Deutschrap First!", value="https://play.ilovemusic.de/ilm_ilovedeutschrapfirst/"),
                    nextcord.SelectOption(label="I Love From Mars", value="https://play.ilovemusic.de/ilm_iloveradiofrommars/"),
                    nextcord.SelectOption(label="I Love Greatest Hits", value="https://play.ilovemusic.de/ilm_ilovegreatesthits/"),
                    nextcord.SelectOption(label="I Love Hardstyle", value="https://play.ilovemusic.de/ilm_ilovehardstyle/"),
                    nextcord.SelectOption(label="I Love Hip Hop", value="https://play.ilovemusic.de/ilm_ilovehiphop/"),
                    nextcord.SelectOption(label="I Love Hip Hop 2025", value="https://play.ilovemusic.de/ilm_hiphop-2023-jahrescharts/"),
                    nextcord.SelectOption(label="I Love Hip Hop History", value="https://play.ilovemusic.de/ilm_ilovehiphophistory/"),
                    nextcord.SelectOption(label="I Love Hit Quiz", value="https://play.ilovemusic.de/ilm-ihit-quiz/"),
                    nextcord.SelectOption(label="I Love Hits 2025", value="https://play.ilovemusic.de/ilm_hits-2023-jahrescharts/"),
                    nextcord.SelectOption(label="I Love Hits Histroy", value="https://play.ilovemusic.de/ilm_ilovehitshistory/"),
                    nextcord.SelectOption(label="I Love Mainstage", value="https://play.ilovemusic.de/ilm_ilovemainstagemadness/"),
                    nextcord.SelectOption(label="I love Malle", value="https://play.ilovemusic.de/ilm_ilovemalle/"),
                    nextcord.SelectOption(label="I Love Mashup", value="https://play.ilovemusic.de/ilm_ilovemashup/"),
                    nextcord.SelectOption(label="I Love Music&Chill", value="https://play.ilovemusic.de/ilm_ilovemusicandchill/"),
                    nextcord.SelectOption(label="I Love Party Hard", value="https://play.ilovemusic.de/ilm_ilovepartyhard/"),
                    nextcord.SelectOption(label="I Love Rock Radio", value="https://play.ilovemusic.de/ilm_iloveradiorock/"),
                    nextcord.SelectOption(label="I Love Sugar Radio", value="https://play.ilovemusic.de/ilm_ilovesugarradio/"),
                    nextcord.SelectOption(label="I Love The 90S", value="https://play.ilovemusic.de/ilm_ilovethe90s/"),
                    nextcord.SelectOption(label="I Love The Beach", value="https://play.ilovemusic.de/ilm_ilovethebeach/"),
                    nextcord.SelectOption(label="I Love The Sun", value="https://play.ilovemusic.de/ilm_ilovethesun/"),
                    nextcord.SelectOption(label="I Love Tomoorowland", value="https://play.ilovemusic.de/ilm-itomorrowland_one_world_radio_germany/"),
                    nextcord.SelectOption(label="I Love Top 100 Charts", value="https://play.ilovemusic.de/ilm_ilovetop100charts/"),
                    nextcord.SelectOption(label="I Love Trash Pop", value="https://play.ilovemusic.de/ilm_ilovetrashpop/"),
                    nextcord.SelectOption(label="I Love US Rap Radio", value="https://play.ilovemusic.de/ilm_iloveusonlyrapradio/"),
                    nextcord.SelectOption(label="I Love Workout", value="https://play.ilovemusic.de/ilm_iloveworkout/"),
                    nextcord.SelectOption(label="I Love XMAS", value="https://play.ilovemusic.de/ilm_ilovexmas/")]

                    
                    
                await inter.response.send_message(view=RadioDropdown(options, voice_client), ephemeral=True)
                
            else:
                cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
                not_same = Embed(title="Failed to play", description="You are currently in a different voice channel to me.\n"
                                 "I am currently entertaining other users in A. You can use me if I am not in another language channel.", colour=config.red)
                not_same.set_thumbnail(url="attachment://cancel_and_error_maja.png")
                await inter.response.send_message(embed=not_same, ephemeral=True, file=cancel_error_png_a)
        else:
            options = [
                nextcord.SelectOption(label="I Love Radio", value="https://play.ilovemusic.de/ilm_iloveradio/"),
                nextcord.SelectOption(label="I Love 2 Dance", value="https://play.ilovemusic.de/ilm_ilove2dance/"),
                nextcord.SelectOption(label="2000er + Trowbacks", value="https://play.ilovemusic.de/ilm_ilove2000throwbacks/"),
                nextcord.SelectOption(label="2010er + Trowbacks", value="https://play.ilovemusic.de/ilm_ilove2010throwbacks/"),
                nextcord.SelectOption(label="Bass by HBZ", value="https://play.ilovemusic.de/ilm_ilovebass/"),
                nextcord.SelectOption(label="I Love Biggest Pop Hits", value="https://play.ilovemusic.de/ilm_ilovenewpop/"),
                nextcord.SelectOption(label="I Love Chillpop", value="https://play.ilovemusic.de/ilm_ilovechillhop/"),
                nextcord.SelectOption(label="I Love Chillout Beats", value="https://play.ilovemusic.de/ilm-ichillout_beats/"),
                nextcord.SelectOption(label="I Love Dance 2025", value="https://play.ilovemusic.de/ilm_dance-2023-jahrescharts/"),
                nextcord.SelectOption(label="I Love Dance First!", value="https://play.ilovemusic.de/ilm-dance_first/"),
                nextcord.SelectOption(label="I Love Dance History", value="https://play.ilovemusic.de/ilm_ilovedancehistory/"),
                nextcord.SelectOption(label="I Love Deutschrap Beste", value="https://play.ilovemusic.de/ilm_ilovedeutschrapbeste/"),
                nextcord.SelectOption(label="I Love Deutschrap First!", value="https://play.ilovemusic.de/ilm_ilovedeutschrapfirst/"),
                nextcord.SelectOption(label="I Love From Mars", value="https://play.ilovemusic.de/ilm_iloveradiofrommars/"),
                nextcord.SelectOption(label="I Love Greatest Hits", value="https://play.ilovemusic.de/ilm_ilovegreatesthits/"),
                nextcord.SelectOption(label="I Love Hardstyle", value="https://play.ilovemusic.de/ilm_ilovehardstyle/"),
                nextcord.SelectOption(label="I Love Hip Hop", value="https://play.ilovemusic.de/ilm_ilovehiphop/"),
                nextcord.SelectOption(label="I Love Hip Hop 2025", value="https://play.ilovemusic.de/ilm_hiphop-2023-jahrescharts/"),
                nextcord.SelectOption(label="I Love Hip Hop History", value="https://play.ilovemusic.de/ilm_ilovehiphophistory/"),
                nextcord.SelectOption(label="I Love Hit Quiz", value="https://play.ilovemusic.de/ilm-ihit-quiz/"),
                nextcord.SelectOption(label="I Love Hits 2025", value="https://play.ilovemusic.de/ilm_hits-2023-jahrescharts/"),
                nextcord.SelectOption(label="I Love Hits Histroy", value="https://play.ilovemusic.de/ilm_ilovehitshistory/"),
                nextcord.SelectOption(label="I Love Mainstage", value="https://play.ilovemusic.de/ilm_ilovemainstagemadness/"),
                nextcord.SelectOption(label="I love Malle", value="https://play.ilovemusic.de/ilm_ilovemalle/"),
                nextcord.SelectOption(label="I Love Mashup", value="https://play.ilovemusic.de/ilm_ilovemashup/"),
                nextcord.SelectOption(label="I Love Music&Chill", value="https://play.ilovemusic.de/ilm_ilovemusicandchill/"),
                nextcord.SelectOption(label="I Love Party Hard", value="https://play.ilovemusic.de/ilm_ilovepartyhard/"),
                nextcord.SelectOption(label="I Love Rock Radio", value="https://play.ilovemusic.de/ilm_iloveradiorock/"),
                nextcord.SelectOption(label="I Love Sugar Radio", value="https://play.ilovemusic.de/ilm_ilovesugarradio/"),
                nextcord.SelectOption(label="I Love The 90S", value="https://play.ilovemusic.de/ilm_ilovethe90s/"),
                nextcord.SelectOption(label="I Love The Beach", value="https://play.ilovemusic.de/ilm_ilovethebeach/"),
                nextcord.SelectOption(label="I Love The Sun", value="https://play.ilovemusic.de/ilm_ilovethesun/"),
                nextcord.SelectOption(label="I Love Tomoorowland", value="https://play.ilovemusic.de/ilm-itomorrowland_one_world_radio_germany/"),
                nextcord.SelectOption(label="I Love Top 100 Charts", value="https://play.ilovemusic.de/ilm_ilovetop100charts/"),
                nextcord.SelectOption(label="I Love Trash Pop", value="https://play.ilovemusic.de/ilm_ilovetrashpop/"),
                nextcord.SelectOption(label="I Love US Rap Radio", value="https://play.ilovemusic.de/ilm_iloveusonlyrapradio/"),
                nextcord.SelectOption(label="I Love Workout", value="https://play.ilovemusic.de/ilm_iloveworkout/"),
                nextcord.SelectOption(label="I Love XMAS", value="https://play.ilovemusic.de/ilm_ilovexmas/")]  
            voice_client = await inter.user.voice.channel.connect()
            await inter.response.send_message(view=RadioDropdown(options, voice_client), ephemeral=True)
            
      '''
def setup(bot: commands.Bot):

    bot.add_cog(Voice(bot))