import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Context

import config
from mysql_asyncmy import A_DB

  
#################################################################################################################                  
#################################################################################################################
################################################################################################################# 


#GLOBAL-CHANNEL       
class global_text_select_channels(nextcord.ui.View):
    def __init__(self, ctx_or_interaction, *, timeout=45):
        super().__init__(timeout=timeout)
        
        self.ctx_or_interaction = ctx_or_interaction
        if isinstance(ctx_or_interaction, Context):
            self.user = ctx_or_interaction.author
        if isinstance(ctx_or_interaction, Interaction):
            self.user = ctx_or_interaction.user
        
        
    async def interaction_check(self, interaction):
            
        if self.user == interaction.user:
            return True
        else:
            await interaction.response.send_message(content="You are not allow to select the channel!")
    
    
    @nextcord.ui.channel_select(channel_types=[nextcord.ChannelType.text], max_values=1, placeholder="Please choose one channel")  
    async def on_select(self, select: nextcord.ui.ChannelSelect, inter: nextcord.Interaction):
        channels = select.values.channels
        for channel in channels:
            pass
                        
        await inter.client.db.update_global_channel(channel.id, inter.guild.id)
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected #{channel.name}"
        self.stop()
        reply = nextcord.Embed(title="Global Channel has been set", description=f"The Global Channel is now \n"f"{channel.jump_url}\n `{channel.id}`", colour=config.blurple)
        await inter.response.edit_message(embed=reply, view=self)
        await inter.delete_original_message(delay=7)
    
    async def on_timeout(self):
        eb = self.children[0]
        eb.disabled = True
        await self.message.edit(view=self)
        await self.message.delete(delay=5)
        


class global_del_view(nextcord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)  

    async def unset_global_channel(self, inter: nextcord.Interaction):
        await inter.client.db.update_global_channel(None, inter.guild.id)  


#################################################################################################################                  
#################################################################################################################
################################################################################################################# 

#LANGUAGE   
class language_select_view(nextcord.ui.View):
    
    def __init__(self, ctx_or_interaction):

        self.ctx_or_interaction = ctx_or_interaction
        if isinstance(ctx_or_interaction, Context):
            self.user = ctx_or_interaction.author
        if isinstance(ctx_or_interaction, Interaction):
            self.user = ctx_or_interaction.user
        super().__init__()


    options = [
    nextcord.SelectOption(label="German", description="This bot will reply in German", emoji=config.flag_de, value="German"),
    nextcord.SelectOption(label="English", description="This bot will reply in English", emoji=config.flag_us, value="English"),
    ]
                
    @nextcord.ui.string_select(placeholder="Please select an language", max_values=1, options=options)
    async def on_select(self, select: nextcord.ui.StringSelect, inter: nextcord.Interaction):
        
        selected_option = select.values[0]

        data = await inter.client.db.query_server_table(inter.guild.id)
        
        if data is None:
            await inter.client.db.insert_language(inter.guild.id, selected_option)
            
        if data is not None:
            if inter.guild.id in data:
                await inter.client.db.update_language(selected_option, inter.guild.id)
        
        check_mark_maja_png = nextcord.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        reply = nextcord.Embed(title="Language has been set", description=f"Your language is now \n"f"{selected_option}", colour=config.blurple)
        reply.set_thumbnail(url="attachment://check_mark_maja.png")
        
        eb = self.children[0]
        eb.disabled = True
        eb.placeholder = f"You selected {selected_option}"
        
        await inter.response.edit_message(attachments=[], file=check_mark_maja_png, embed=reply, view=self)
        self.stop()
    

class language_del_view(nextcord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)  

    async def unset_language(self, inter: nextcord.Interaction):
        await inter.client.db.update_language(None, inter.guild.id)