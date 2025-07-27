from distutils.command.config import config
import nextcord
import config

from nextcord.ext import commands


class GhostPing(commands.Cog, name="Ghost-Ping-Detection"):
    """Zeigt Setup Funktionen an"""

    COG_EMOJI = config.DiscordSecurity
    
    def __init__(self, bot):
        self.bot = bot


        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.mention in message.content:
            pass
        if message.author.bot: 
            return
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return
        if message.mentions:  
            output = nextcord.Embed(title=f"{config.DiscordSecurity} Ghost Ping Detection", description=f"{config.DiscordMention} A ghost ping was found in the following message:",
                                    colour=config.brand_red)
            output.add_field(name="Message", value=f"> {message.content}")
            output.set_footer(text=f"Ghost Ping send by {message.author}")
            await message.channel.send(embed=output)
            
def setup(bot: commands.Bot):
    bot.add_cog(GhostPing(bot))