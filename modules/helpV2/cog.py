
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption

import config
from typing import Optional
        
######################################################################################################################      
        

class HelpDropdown_Slash(nextcord.ui.Select):
    def __init__(self, ctx, help_command: "MyHelpCommand_Slash", options: list[nextcord.SelectOption]):
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self._help_command = help_command
        self.ctx = ctx
        
        
    #Selected Cog
    async def callback(self, interaction: nextcord.Interaction):

            selected_cog = self.values[0]
            cog_info = interaction.client.get_cog(selected_cog)
            
            if cog_info is not None:
                emoji = getattr(cog_info, "COG_EMOJI", None)
                embed = nextcord.Embed(title=f"__{cog_info.qualified_name} {emoji}__" if emoji else cog_info.qualified_name,
                                        description=cog_info.description,
                                        colour=config.blurple)
                
                for cog_name in self.values:
                    
                    cog = interaction.client.get_cog(cog_name)
                                   
                    for cmd in cog.application_commands:

                        if cmd.children:
                            for _, sub in cmd.children.items():
                                embed.add_field(name=sub.get_mention(),
                                        value=f'{sub.description or "..."}\n\uFEFF')
                        else:
                            embed.add_field(name=cmd.get_mention(),
                                        value=f'{cmd.description or "..."}\n\uFEFF')

                                
                    
                await interaction.response.edit_message(embed=embed)
                
            if cog_info is None:

                embed = nextcord.Embed(description="Command categories", colour=config.blurple)
                
                cog_filter = [cog for cog in interaction.client.cogs.values() if len(cog.get_application_commands) > 0]

                for cog in cog_filter:
                    emoji = getattr(cog, "COG_EMOJI", None)
                    embed.add_field(name=f"{emoji}{cog.qualified_name}" if emoji else cog.qualified_name, value=f"{cog.description}\n\uFEFF")
                
                await interaction.response.edit_message(embed=embed)

class HelpView_Slash(nextcord.ui.View):
    def __init__(self, ctx, help_command: "MyHelpCommand_Slash", options: list[nextcord.SelectOption], message: nextcord.InteractionMessage, *, timeout: Optional[float] = 45):
        super().__init__(timeout=timeout)
        self._help_command = help_command
        self.ctx = ctx
        self.message = message
        self.add_item(HelpDropdown_Slash(self.ctx, help_command, options))
        
    async def on_timeout(self):
        # remove dropdown from message on timeout
        self.clear_items()
        await self.message.edit(view=self)



class MyHelpCommand_Slash(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(verify_check=False)
        
###################################################################################################################### 


class HelpCommand(commands.Cog, name="Help"):
    """Shows all Informations about Commands or Modules"""
    
    COG_EMOJI = config.a_support
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot


    #############################################################################################  


                
    @nextcord.slash_command(name="help")
    async def help(self, interaction: nextcord.Interaction, module: str = SlashOption(name="module", description="Please give a command name", required=False)):
    
        #First response
        wait = nextcord.Embed(description=f"{config.e_loading} Please wait", colour=config.red)
        await interaction.response.send_message(embed=wait)
        
        #If module is empty
        if module is None:
            cog_filter = [cog for cog in interaction.client.cogs.values() if len(cog.application_commands) > 0]
            
            cog_select_options = []
            
            for cog in cog_filter:
                emoji = getattr(cog, "COG_EMOJI", None)
                select_options = nextcord.SelectOption(label=cog.qualified_name if cog else "No Category", emoji=emoji, description=cog.description[:120] if cog and cog.description else None)
                cog_select_options.append(select_options)
            
            view = HelpView_Slash(interaction, "help_command", cog_select_options, message=await interaction.original_message())
                 
            #MAINpage
            embed = nextcord.Embed(description="Command categories", colour=config.blurple)
                
            for cog in cog_filter:
                emoji = getattr(cog, "COG_EMOJI", None)
                embed.add_field(name=f"{emoji}  {cog.qualified_name}" if emoji else cog.qualified_name, value=f"{cog.description}\n\uFEFF")
                
            embed.set_author(name=interaction.client.user.name)
            embed.set_footer(text="NOTE: All commands here are only available in ENGLISH, as well as their descriptions and details.")
            await interaction.edit_original_message(embed=embed, view=view)
            

        #Page of a cog
        if module is not None:
            
            ccog = interaction.client.get_cog(module)
            if ccog is not None:
                #Page of a choosen cog
                emoji = getattr(ccog, "COG_EMOJI", None)
                
                embed = nextcord.Embed(title=f"{emoji} __{ccog.qualified_name}__" if emoji else f'_{ccog.qualified_name}_',
                                       description=f"{ccog.description or '...'}",
                                       colour=config.blurple)
                
                for cmd in ccog.application_commands:

                    if cmd.children:
                        for _, sub in cmd.children.items():
                            embed.add_field(name=sub.get_mention(),
                                        value=f'{sub.description or "..."}\n\uFEFF')
                    else:
                        embed.add_field(name=cmd.get_mention(),
                                    value=f'{cmd.description or "..."}\n\uFEFF')  
                        
                await interaction.edit_original_message(embed=embed)
                
                
            if ccog is None:
                #Page of a choosen command
                
                is_no_subcommand = nextcord.utils.get(interaction.client.get_all_application_commands(), name=module)
                
                if is_no_subcommand is None:
                    get_sub = nextcord.utils.get(interaction.client.get_all_application_commands(), name=module.split()[0])
                    try:
                        if get_sub.children:
                            cog_filter = [cog for cog in interaction.client.cogs.values() if len(cog.application_commands) > 0]
                            
                            for cog in cog_filter: 
                                if get_sub in cog.application_commands:
                                    cog_name = cog.qualified_name
                                    emoji = getattr(cog, "COG_EMOJI", None)  

                                    
                            embed = nextcord.Embed(description=f"{emoji if emoji else ''} __**{cog_name}**__\n\uFEFF", colour=config.blurple)  
                                
                            for _, cmd in get_sub.children.items():
                                if cmd.name == module.split()[1]:
                                    fcommand = cmd
                                    break
                                else:
                                    fcommand = None
    
                            if fcommand.children:
                                for _, sub in fcommand.children.items():
                                    embed.add_field(name=sub.get_mention(),
                                                value=f'{sub.description or "..."}\n\uFEFF')
                            else:
                                options = fcommand.options.values()
                                options_str = ''

                                if options:
                                    options_str += '_'
                                    for option in options:
                                        if option.required:
                                            options_str += f'<{option.name}> '
                                        else:
                                            options_str += f' [{option.name}] '
                                    options_str += '_'
                                    
                                    embed.add_field(name=f"{fcommand.get_mention()} {options_str or ''}",
                                                        value=fcommand.description if fcommand.description else "...")
                        
                                await interaction.edit_original_message(embed=embed)
                    
                    except: 
                        embed = nextcord.Embed(description=f"{config.a_cross} The command category or command `/{module}` was not found",
                                            colour=config.red)
                        await interaction.edit_original_message(embed=embed)
                    
                elif is_no_subcommand is not None:
                    
                    cog_filter = [cog for cog in interaction.client.cogs.values() if len(cog.application_commands) > 0]
                    for cog in cog_filter: 
                        
                        if is_no_subcommand in cog.application_commands:
                            cog_name = cog.qualified_name
                            emoji = getattr(cog, "COG_EMOJI", None) 
 
                    embed = nextcord.Embed(description=f"{emoji if emoji else ''} __**{cog_name}**__\n\uFEFF", colour=config.blurple)
                    
                    if is_no_subcommand.children:
                        for _, sub in is_no_subcommand.children.items():
                            embed.add_field(name=sub.get_mention(),
                                        value=f'{sub.description or "..."}\n\uFEFF')
                    else:
                        options = is_no_subcommand.options.values()
                        options_str = ''

                        if options:
                            options_str += '_'
                            for option in options:
                                if option.required:
                                    options_str += f'<{option.name}> '
                                else:
                                    options_str += f' [{option.name}] '
                            options_str += '_'
                            
                            embed.add_field(name=f"{is_no_subcommand.get_mention()} {options_str or ''}",
                                                value=is_no_subcommand.description if is_no_subcommand.description else "...")
 
                    await interaction.edit_original_message(embed=embed)
                                        
                else: 
                    embed = nextcord.Embed(description=f"{config.a_cross} The command category or command `/{module}` was not found",
                                           colour=config.red)
                    await interaction.edit_original_message(embed=embed)
            


                   
def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))