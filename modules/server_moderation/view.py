import nextcord
import config

class ChannelRename(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Rename your Channel")
        
        self.new_name = nextcord.ui.TextInput(label="New Channel Name", style=nextcord.TextInputStyle.short, placeholder="Type here your new name", required=True, max_length=24)

        self.add_item(self.new_name)


    async def callback(self, inter: nextcord.Interaction):
        
        co = nextcord.Embed(description="The name of the Channel has changed", colour=config.blurple)
        co.add_field(name="Changes:", value=f"Before: {inter.channel.name}\nNow: {self.new_name.value}")
        
        channel = inter.client.get_channel(inter.channel.id)
        cr = "rename command used"
        
        if isinstance(channel, nextcord.TextChannel):
            await channel.edit(name=self.new_name.value, reason=cr)
            await inter.response.send_message(embed=co, ephemeral=True)
            
        if isinstance(channel, nextcord.StageChannel):
            await channel.edit(name=self.new_name.value, reason=cr)
            await inter.response.send_message(embed=co, ephemeral=True)
            
        if isinstance(channel, nextcord.VoiceChannel):
            await channel.edit(name=self.new_name.value, reason=cr)
            await inter.response.send_message(embed=co, ephemeral=True)
            
        if isinstance(channel, nextcord.Thread):
            await channel.edit(name=self.new_name.value)
            await inter.response.send_message(embed=co, ephemeral=True)
            
        if isinstance(channel, nextcord.ForumChannel):
            await inter.channel.edit(name=self.new_name.value, reason=cr)
            await inter.response.send_message(embed=co, ephemeral=True)
            
            
class ChannelSlowmode(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        
    options = [nextcord.SelectOption(label="Disable", value=0),
               nextcord.SelectOption(label="30 Secouds", value=30),
               nextcord.SelectOption(label="1 Minute", value=60),
               nextcord.SelectOption(label="5 Minutes", value=300),
               nextcord.SelectOption(label="10 Minutes", value=600),
               nextcord.SelectOption(label="15 Minutes", value=900),
               nextcord.SelectOption(label="30 Minutes", value=1800),
               nextcord.SelectOption(label="1 Hour", value=3600),
               nextcord.SelectOption(label="2 Hours", value=7200),
               nextcord.SelectOption(label="4 Hours", value=14400),
               nextcord.SelectOption(label="6 Hours", value=21600),
               nextcord.SelectOption(label="8 Hours", value=28800),
               nextcord.SelectOption(label="16 Hours", value=57600),
               nextcord.SelectOption(label="24 Hours", value=86400)]   
    
    @nextcord.ui.string_select(placeholder="Please select a slowmode delay", max_values=1, options=options)
    async def on_select(self, select: nextcord.ui.StringSelect, inter: nextcord.Interaction):
        
        selected_option = select.values[0]
        channel = inter.guild.get_channel(inter.channel.id) 
        changed_setting_png = nextcord.File("pictures/changed-settings.png", filename="changed-settings.png")
        reply = nextcord.Embed(title=f"Slowmode Delay changed for {inter.channel.jump_url}\n\uFEFF", description=f"__Old Slowmode-Delay:__ `{channel.slowmode_delay} Secounds`\n\n__New Slowmode-Delay:__ `{selected_option} Secounds`", colour=config.blurple)
        reply.set_thumbnail(url="attachment://changed-settings.png")
        await channel.edit(slowmode_delay=selected_option)
        await inter.response.edit_message(embed=reply, file=changed_setting_png, view=None)
        

#####  P E R M I S S I O N   O V E R W R I T E  #####  
        
class PermissionOverwriteView(nextcord.ui.View):
    def __init__(self, managed_role, selected_channel):
        super().__init__(timeout=30)
        self.value = None
        self.managed_role = managed_role
        self.selected_channel = selected_channel

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        button.disabled = True
        bca = self.children[1]
        bca.disabled = True
        await interaction.response.edit_message(view=self)
        await self.selected_channel.set_permissions(self.managed_role, send_messages=True)
        embed = nextcord.Embed(title=f"Permission Changed for {self.selected_channel.name} {config.a_tic}", description=f"I have successfully adjusted the `send messages` permission for my role in this channel.", colour=config.green)
        
        
        lockdownclose = nextcord.Embed(description=f"{config.a_lock} This channel has been closed by a moderator",
                            color=config.red)
        lockdownopen = nextcord.Embed(description=f"{config.a_unlock} This channel was opened by a moderator",
                                      colour=config.green)        


        if interaction.guild.default_role not in self.selected_channel.overwrites:
            overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
            }
            await self.selected_channel.edit(overwrites=overwrites)

            await interaction.edit_original_message(embed=embed, view=None)
            await self.selected_channel.send(embed=lockdownclose)
            

            
        elif self.selected_channel.overwrites[interaction.guild.default_role].send_messages == True or self.selected_channel.overwrites[interaction.guild.default_role].send_messages == None:

            await interaction.edit_original_message(embed=embed, view=None)
            await self.selected_channel.send(embed=lockdownclose)

            
        else:
            overwrites = self.selected_channel.overwrites[interaction.guild.default_role]
            overwrites._values["send_messages"] = None
            await self.selected_channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

            await interaction.edit_original_message(embed=embed, view=None)
            await self.selected_channel.send(embed=lockdownopen)
                

                
                
                
                       
    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        button.disabled = True
        bco = self.children[0]
        bco.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()