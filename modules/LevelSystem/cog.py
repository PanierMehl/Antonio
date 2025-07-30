import nextcord
from nextcord import Interaction, SlashOption, Member
from nextcord.ext import commands

import config
from mysql_asyncmy import A_DB
import perms_check


class LevelSystem(commands.Cog, name="Level Commands"):
    """Contains all level commands"""

    COG_EMOJI = config.a_trash
    
    def __init__(self, bot):
        self.bot = bot


    @nextcord.slash_command(name="level")
    async def level(self, inter: Interaction):
        pass
    
    @level.subcommand(name="show")
    @perms_check.has_min_moderator_perm_role()
    async def level_show(self, inter: Interaction, member: Member = SlashOption(name="member")):
        check = await self.bot.db.level_query(member.id, inter.guild.id)
        
        if check == None:
            await inter.response.send_message(content="None", ephemeral=True)
            return False
        else:
            await inter.response.send_message(content="YES", ephemeral=True)
            return True
        
        

def setup(bot: commands.Bot):

    bot.add_cog(LevelSystem(bot))
        