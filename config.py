from dotenv.main import load_dotenv
import nextcord
import datetime

load_dotenv()


# Bot setup
BOT_NAME = "ANTONIO"
VERSION = "V5.0"
#Emojis


eventnews_emoji = "<:bot_events:952893298303987813>"
giveawaynews_emoji = "<:bot_giveaways:952893298475937812>"
servernews_emoji = "<:enews:952893523923972097>"



#All Emojis
DiscordMention = "<:DiscordMention:965409831571845231>"
DiscordSecurity = "<:DiscordSecurity:965410282321100880>"
DiscordMuted = "<:DiscordMuted:967699987637075968>"
DiscordUnmuted = "<:DiscordUnmuted:970996884707627019>"
DiscordBan = "<:DiscordBan:971102898756927529>"

BotBeta = "<:Bot_beta:1053051716276342804>"

flag_us = "\U0001f1fa\U0001f1f8"
flag_de = "\U0001f1e9\U0001f1ea"

#V2 Emojilist
dc_owner_badge = "<:dc_owners:1107645824080551936>"
dc_voice = "<:dc_voice:1107645829336027216>"
dc_settings = "<:dc_settings:1107645826316120074>"
dc_bots = "<:dc_bots:1107645811032076329>"
dc_members = "<:dc_members:1107645819026423848>"
dc_moderators = "<:dc_moderators:1107645821949853696>"
dc_owners = "<:dc_owners:1107645824080551936>"
dc_voice = "<:dc_voice:1107645829336027216>"
dc_dot = "<:dc_dot:1107704836625014855>"
dc_filter = "<:dc_filter:1107704838218850376>"
dc_guide = "<:dc_guide:1107704841045811331>"
dc_vc = "<:dc_vc:1107704921471582328>"
dc_language = "<:dc_language:1107705344941101178>"
dc_mail = "<:dc_mail:1107705377463730287>"
dc_channel = "<:dc_channel:1107715420577865808>"

#V2.1 Emojis
a_lock = "<:a_lock:1170704064598782032> "
a_unlock = "<:a_unlock:1170704024471883817>"
a_trash = "<:a_trash:1170712376262262886>"
a_tic = "<:a_tic:1174389672064065546>"
a_notes = "<:a_notes:1222321392553562222>"
a_support = "<:a_support:1222323146343055470>"

#V 4.0 Emojis
e_information = "<:a_information:1222687984244097074>"
e_loading = "<a:f_loadinf:1222689491060392056>"
a_cross = "<:a_cross:1174409200701550663>"
a_join = "<:a_added:1177667904850886787>"
a_leave = "<:a_removed:1177667891122942010>"

#Bot Emojis (TestBot)
#confirm = "<:Confirmed:1385636712213905498>"
#giveaway = "<a:Giveaway:1385653154624045179>"
#join = "<:Join:1385655299872129054>"


#Bot Emojis (Main)
confirm = "<:Confirm:1385636098243432591>"
giveaway = "<a:Giveaway:1387513889721417849>"
join = "<:Join:1387513893965795399>"


#Farb IDs
red = nextcord.Colour.red()
dark_red = nextcord.Colour.dark_red()
yellow = nextcord.Colour.yellow()
blue = nextcord.Colour.blue()
dark_blue = nextcord.Colour.dark_blue()
blurple = nextcord.Colour.blurple()
old_blurple = nextcord.Colour.og_blurple()
green = nextcord.Colour.green()
dark_green = nextcord.Colour.dark_green()
light_grey = nextcord.Colour.light_grey()
dark_grey = nextcord.Colour.dark_grey()
gold = nextcord.Colour.gold()
dark_gold = nextcord.Colour.dark_gold()
magenta = nextcord.Colour.magenta()
dark_magenta = nextcord.Colour.dark_magenta()
orange = nextcord.Colour.orange()
dark_orange = nextcord.Colour.dark_orange()
purple = nextcord.Colour.purple()
dark_purple = nextcord.Colour.dark_purple()
random_colour = nextcord.Colour.random()
fuchsia = nextcord.Colour.fuchsia()
greyple = nextcord.Colour.greyple()
brand_red = nextcord.Colour.brand_red()


#Zeitstempel
aktuelldatum = (nextcord.utils.format_dt(nextcord.utils.utcnow(), style="F"))
##########################
aktuelldatum_and_time_add = datetime.datetime.now().timestamp()

TESTGUILD = 900100165397008465
universal_invite = "https://discord.com/invite/3QJ6BDMgc"


#PNG
cancel_error_png = nextcord.File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
cancel_error_url = "attachment://cancel_and_error_maja.png"

check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
check_mark_maja_url = "attachment://check_mark_maja.png"



