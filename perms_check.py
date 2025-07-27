import nextcord
from nextcord.ext import application_checks, commands
from nextcord import Interaction, Embed

import config
from mysql_class import BotDB

import aiosqlite


##################################################################################################################

async def get_admin_role(inter: Interaction):
    check = BotDB().query_server_table(inter.guild.id)
                    
    if check is None:
        admin_role = None
        return admin_role

    else:
        return check[1]
                
##################################################################################################################

async def get_moderator_role(inter: Interaction):
    check = BotDB().query_server_table(inter.guild.id)
                    
    if check is None:
        moderator_role = None
        return moderator_role

    else:
        return check[2]
            
##################################################################################################################

async def get_supporter_role(inter: Interaction):
    check = BotDB().query_server_table(inter.guild.id)
                    
    if check is None:
        supporter_role = None
        return supporter_role

    else:
        return check[3]
            
##################################################################################################################

def has_admin_perm_role():
    async def extended_check(inter: Interaction):

        fail_m = Embed(title="No role found", description="Please add a administrator role with the setup commands to use this command!", colour=config.red)

        no_perm_m = Embed(title="Missing Permissions", description="You don't have the required role!", color=config.red)
        admin_role = await get_admin_role(inter)
        if admin_role is None:
            await inter.response.send_message(embed=fail_m, ephemeral=True)
            return False
        
        else:
            if inter.user.get_role(admin_role):
                return True
            else:
                await inter.response.send_message(embed=no_perm_m, ephemeral=True)
                return False
    
    return application_checks.check(extended_check)


def has_min_moderator_perm_role():
    async def extended_check(inter: Interaction):

        fail_m = Embed(title="No role found", description="Please add Perm Roles with the setup commands to use this command!", colour=config.red)

        no_perm_m = Embed(title="Missing Permissions", description="You don't have the required role!", color=config.red)
        
        admin_role = await get_admin_role(inter)
        moderator_role = await get_moderator_role(inter)

        if admin_role and moderator_role is None:
            await inter.response.send_message(embed=fail_m, ephemeral=True)
            return False
        
        elif admin_role and moderator_role is not None:
            if inter.user.get_role(admin_role) or inter.user.get_role(moderator_role):
                return True
            else:
                await inter.response.send_message(embed=no_perm_m, ephemeral=True)
                return False
        else:
            await inter.response.send_message(embed=fail_m, ephemeral=True)
            return False
    
    return application_checks.check(extended_check)



def has_min_supporter_perm_role():
    async def extended_check(inter: Interaction):

        fail_m = Embed(title="No role found", description="Please add Perm Roles with the setup commands to use this command!", colour=config.red)

        no_perm_m = Embed(title="Missing Permissions", description="You don't have the required role!", color=config.red)
        
        admin_role = await get_admin_role(inter)
        moderator_role = await get_moderator_role(inter)
        supporter_role = await get_supporter_role(inter)

        if admin_role and moderator_role and supporter_role is None:
            await inter.response.send_message(embed=fail_m, ephemeral=True)
            return False
        
        elif admin_role and moderator_role and supporter_role is not None:
            if inter.user.get_role(admin_role) or inter.user.get_role(moderator_role) or inter.user.get_role(supporter_role):
                return True
            else:
                await inter.response.send_message(embed=no_perm_m, ephemeral=True)
                return False
            
        else:
            await inter.response.send_message(embed=fail_m, ephemeral=True)
            return False
    
    return application_checks.check(extended_check)


def check_vip_status():
    async def extended_check(inter: Interaction):

        fail = Embed(title=f"{config.a_cross} No active VIP status available.", description=f"There is currently no active VIP status for this server.  This means you cannot access VIP functions.  If you have VIP status but it is not registered, please contact us [here]({config.universal_invite}).", colour=config.red)


        check = BotDB().query_server_table(inter.guild.id)
        if check is None:
            await inter.response.send_message(embed=fail, ephemeral=True)
            return False

        else:
            if check[7] is None:
                await inter.response.send_message(embed=fail, ephemeral=True)
                return False
            
            else:
                return True
            
    return application_checks.check(extended_check)
