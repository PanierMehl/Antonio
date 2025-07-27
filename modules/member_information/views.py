import nextcord as nc
from nextcord import Interaction, Embed
from nextcord.ext.commands import Context
import config
import pytz
from datetime import datetime

class mi_home(nc.ui.View):
    def __init__(self, ctx_or_interaction, input_member):
        super().__init__(timeout=30)
        
        self.input_member = input_member

        self.ctx_or_interaction = ctx_or_interaction
        if isinstance(ctx_or_interaction, Context):
            self.user = ctx_or_interaction.author
        if isinstance(ctx_or_interaction, Interaction):
            self.user = ctx_or_interaction.user        

    async def interaction_check(self, inter):

        if self.user == inter.user:
            return True
        else:
            embed = Embed(description=f"{config.a_cross} You are not authorized to press this button", colour=config.red)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return False
        

    @nc.ui.button(label="Server Avatar", style=nc.ButtonStyle.blurple, disabled=False)
    async def s_av(self, button: nc.ui.Button, inter: Interaction):
        re = Embed(title=f"Avatar from {self.input_member}", description=f"Here is the avatar of {config.dc_members} {self.input_member.display_name}", colour=config.blurple)
        re.set_image(url=self.input_member.avatar.url)
        await inter.response.edit_message(embed=re, view=mi_backtohome(inter, self.input_member))

    @nc.ui.button(label="Member Avatar", style=nc.ButtonStyle.blurple, disabled=False)
    async def m_av(self, button: nc.ui.Button, inter: Interaction):
        re = Embed(title=f"Avatar from {self.input_member}", description=f"Here is the avatar of {config.dc_members} {self.input_member.display_name}", colour=config.blurple)
        re.set_image(url=self.input_member.avatar.url)
        await inter.response.edit_message(embed=re, view=mi_backtohome(inter, self.input_member))      
        
    @nc.ui.button(label="Show all Roles", style=nc.ButtonStyle.blurple)
    async def show_all_roles(self, button: nc.ui.Button, inter: Interaction):
        
        rlist = []
        for role in self.input_member.roles:
            if role.name == "@everyone":
                continue
            rlist.append(str(role.mention))
            
        embed = nc.Embed(title="Roles from {}".format(self.input_member.display_name), colour=config.random_colour)
        if len(rlist) == 0:
            embed.add_field(name="Rollen",value="Dieser User hat keine Rollen")
            return await inter.response.edit_message(embed=embed)
        embed.add_field(name=f"Roles: {len(self.input_member.roles) - 1}", value='\n'.join(rlist), inline=False)

        await inter.response.edit_message(embed=embed, view=mi_backtohome(inter, self.input_member))
    

class mi_backtohome(nc.ui.View):
    def __init__(self, ctx_or_interaction, input_member):
        super().__init__(timeout=30)

        self.input_member = input_member

        self.ctx_or_interaction = ctx_or_interaction
        if isinstance(ctx_or_interaction, Context):
            self.user = ctx_or_interaction.author
        if isinstance(ctx_or_interaction, Interaction):
            self.user = ctx_or_interaction.user        

    async def interaction_check(self, inter):

        if self.user == inter.user:
            return True
        else:
            embed = Embed(description=f"{config.a_cross} You are not authorized to press this button", colour=config.red)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return False
        

    @nc.ui.button(label="Home", style=nc.ButtonStyle.green, disabled=False)
    async def s_av(self, button: nc.ui.Button, inter: Interaction):
        member = self.input_member

        de = pytz.timezone('Europe/Berlin')
        
        memberinfo = Embed(title=f'{config.e_information} User-Info for {config.dc_members} {member.display_name}',
                            description='', colour=nc.Colour.random(), timestamp=datetime.now().astimezone(tz=de))

        
        if inter.guild.get_member(member.id) != None: 

            def activity_s():
                try:
                    if member.activity.type == nc.ActivityType.playing:
                        return f"Playing: {member.activity.name}"
                    elif member.activity.type == nc.ActivityType.streaming:
                        return f"`Streaming` **{member.activity.name}** {member.activity.buttons}"
                    elif member.activity.type == nc.ActivityType.custom:
                        return f"{member.activity.name}"
                    elif member.activity is None:
                        return "No activity"
                    else:
                        return "No activity"
                except:
                    return "No activity"
                
                
            memberinfo.add_field(name='__**General**__', 
                                value=f"> **Member:** {member}\n"
                                f"> **ID:** `{member.id}`\n"
                                f"> **Created:** `{str(member.created_at)[:19]}`\n"
                                f"> **Current activity:** {activity_s()}\n"
                                f"> **Is Bot:** {config.a_tic if member.bot else config.a_cross}")
            
            memberinfo.add_field(name="__**Server**__",
                            value=f"> **Nickname:** {member.nick if member.nick else '-----'}\n"
                            f"> **Server joined:** `{str(member.joined_at)[:19]}`\n"
                            f"> **Booster:** {config.a_tic if member.premium_since else config.a_cross}")
            
            input_member = member
            view_r = mi_home(inter, input_member)
            await inter.response.edit_message(embed=memberinfo, view=view_r)
            
            
        elif inter.guild.get_member(member.id) == None: 

            memberinfo.add_field(name='General', 
                                value=f"> Member: `{member}`\n"
                                f"> ID: `{member.id}`\n"
                                f"> Created: `{str(member.created_at)[:19]}`\n"
                            f"> Is Bot: {config.a_tic if member.bot else config.a_cross}")
        
            
            await inter.response.edit_message(embed=memberinfo, view=mi_home(inter, self.input_member))   

        
        
