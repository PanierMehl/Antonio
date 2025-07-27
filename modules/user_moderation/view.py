import nextcord as nc
from nextcord import File, Embed
import config
import aiosqlite
import random
import string
import time
import asyncio
from datetime import timedelta
from mysql_class import BotDB


#############################################################################################################
#############################################################################################################
    
  
            
            
def generate_random_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


#####  N E W   W A R N  #####
class NewWarnModal(nc.ui.Modal):
    def __init__(self, target):
        self.target = target
        super().__init__(f"Warning for {self.target.name}")
        
        
        
        self.reason = nc.ui.TextInput(label="Reason", style=nc.TextInputStyle.paragraph, placeholder="Type here your reason", required=True, max_length=50)

        self.add_item(self.reason)


    async def callback(self, inter: nc.Interaction):
                
        sucess = Embed(title=f"Created warn for {self.target.name}!", description=f"You have Sucessfully warned {self.target}.", colour=config.green)
        
        random_id = generate_random_id(10)
        
        formated_reason = ''.join(self.reason.value)

        warn_png = nc.File("pictures/warning.png", filename="warning.png")
        user_dm = Embed(title=f"You are beeing warned on {inter.guild.name}",
                        description=f"__**Reason:**__\n{formated_reason}", colour=config.red)
        user_dm.set_footer(text=f"Warned by: {inter.user} ➟ {inter.user.id}", icon_url=inter.user.avatar.url)
        user_dm.set_thumbnail(url="attachment://warning.png")

        current_time = config.aktuelldatum
        
        all_cases = BotDB().query_all_case_ids_with_type(self.target.id, inter.guild.id, "Warning")
        
        c = 1
        for case in all_cases:
            c += 1
        
        BotDB().insert_case(inter.guild.id, self.target.id, inter.user.id, current_time, self.reason.value, None, random_id, "Warning", "Open")
        
        try:
            await self.target.send(embed=user_dm, file=warn_png)
        except:
            pass
        
        sucess.add_field(name="Current Warnings", value=c)
        check_mark_maja_png = nc.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
        sucess.set_thumbnail(url="attachment://check_mark_maja.png")
        await inter.response.send_message(embed=sucess, file=check_mark_maja_png, ephemeral=True)
                
                
#####  E D I T   C A S E  #####     


class EditCaseDropdown(nc.ui.View):

    def __init__(self, target, options):

        super().__init__()
        self.target = target
        self.options = options
        self.button_back = self.children[0]
        self.button_next = self.children[1]
        self.select_edit_warn = SelectEditWarn(self.target, self.options, self.button_back, self.button_next)
        self.add_item(self.select_edit_warn)
        
    def update_select_edit_warn_options(self, options):
        self.select_edit_warn.options = options
        
    @nc.ui.button(label="Page Back", style=nc.ButtonStyle.blurple, row=1, disabled=True)
    async def page_back(self, button: nc.ui.Button, inter: nc.Interaction):

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        button_count = int(button_back.label.split()[1]) if button.label else 1
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count -= 1
            options = []
            offset_count = button_count - 1
            button_back.label = f"Page {button_count}"
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            button_next.disabled = False
            if offset_count == 0:
                button_back.disabled = True
                button_back.label = "Page Back"
            else:
                button_back.disabled = False
            for case in cases:
                button_next.label = f"Page {button_count + 1}"
                query = BotDB().query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_edit_warn_options(options) # update SelectEditWarn options
            await inter.response.edit_message(view=self)
        
                
    @nc.ui.button(label="Page 2", style=nc.ButtonStyle.blurple, row=1)
    async def next_page(self, button: nc.ui.Button, inter: nc.Interaction):
        button_count = int(button.label.split()[1]) if button.label else 1

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count += 1
            button_next.label = f"Page {button_count}"
            options = []
            offset_count = button_count - 2
            back_label = button_count - 1
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            next_cases_check = BotDB().query_all_cases_via_case_id_with_offset(back_label, self.target, inter.guild.id)
            button_back.disabled = False
            
            button_back.label = f"Page {back_label}"
            if next_cases_check:
                button_next.disabled = False
            else:
                button_next.disabled = True
                await inter.response.edit_message(view=self)
                return
            for case in cases:
                query = BotDB().query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_edit_warn_options(options) # update SelectEditWarn options
            await inter.response.edit_message(view=self)

                            
        else:
            button_next.disabled = True
            await inter.response.edit_message(view=self)


class SelectEditWarn(nc.ui.Select):
    def __init__(self, target, options, button_back, button_next):
        super().__init__(placeholder="Choose a case", min_values=1, max_values=1, options=options)
        self.target = target
        self.options = options
        self.button_back = button_back
        self.button_next = button_next
    
    async def callback(self, inter: nc.Interaction):
        select_value = self.values[0].split()[1]
        query = BotDB().query_case_with_user(self.target, inter.guild.id, select_value)

        formated_reason = ''.join(query[2])

        if query[6].split()[0] == "Open":
            c_status = "Open"
            col = config.green
            view = ShowCaseInfo_Open(query[0], query[1], formated_reason, query[3], query[4], query[5], query[6], self.target, select_value)

        if query[6].split()[0] == "Closed":
            c_status = query[6]
            col = config.red
            view = ShowCaseInfo_Closed(query[0], query[1], formated_reason, query[3], query[4], query[5], query[6], self.target, select_value)

        opened_by = inter.guild.get_member(query[0])

        info_e = nc.Embed(title=f"{query[5]}: {select_value}", description=f"Case opened by **{opened_by.name}** at {query[1]}", colour=col)
        info_e.add_field(name="Informations", value=query[3])
        info_e.add_field(name="Case History", value=query[4])
        info_e.add_field(name="Case Status", value=c_status)

        await inter.response.edit_message(embed=info_e, view=view)


class ShowCaseInfo_Open(nc.ui.View):
    def __init__(self, case_creator, date, reason, info, changes, entry_type, case_status, target, case_id):
        super().__init__()  # Add this line to call the parent constructor
        self.case_creator = case_creator
        self.date = date
        self.reason = reason
        self.info = info
        self.changes = changes
        self.target = target
        self.case_id = case_id
        self.entry_type = entry_type
        self.case_status = case_status

    @nc.ui.button(label="Edit Case", style=nc.ButtonStyle.green, row=1, disabled=False)
    async def edit_case(self, button: nc.ui.Button, inter: nc.Interaction):
        query = BotDB().query_case_with_user(self.target, inter.guild.id, self.case_id)
        formated_reason = ''.join(query[2])
        view = EditCaseModal(query[0], query[1], formated_reason, query[3], query[4], query[5], self.target, self.case_id, query[6])
        button.disabled = True
        await inter.response.send_modal(modal=view)

    @nc.ui.button(label="Close Case", style=nc.ButtonStyle.red, row=1, disabled=False)
    async def close_case(self, button: nc.ui.Button, inter: nc.Interaction):
        query = BotDB().query_case_with_user(self.target, inter.guild.id, self.case_id)
        formated_reason = ''.join(query[2])

        info_e = nc.Embed(title=f"{query[5]}: {self.case_id} (CLOSED)", description=f"Case opened by: {query[0]} at {query[1]}", colour=config.red)
        info_e.add_field(name="Informations", value=query[3])
        info_e.add_field(name="Case History", value=query[4])
        info_e.add_field(name="Case Status", value=f"Closed by {inter.user} at {config.aktuelldatum}")

        BotDB().update_case_status(f"Closed by {inter.user} at {config.aktuelldatum}", inter.guild.id, self.case_id)
        view = ShowCaseInfo_Closed(query[0], query[1], formated_reason, query[3], query[4], query[5], query[6], self.target, self.case_id)
        await inter.response.edit_message(embed=info_e, view=view)


    @nc.ui.button(label="Menu", style=nc.ButtonStyle.blurple, row=2, disabled=False)
    async def menu_case(self, button: nc.ui.Button, inter: nc.Interaction):
        data = BotDB().query_server_table(inter.guild.id)
        target = inter.guild.get_member(self.target)            
        if data is None:
            fail_m = Embed(title="No role found", description="Please add Perm Roles with the setup commands to use this command!", colour=config.red)
            await inter.response.send_message(embed=fail_m)
            return False

        else:            
            if inter.user.get_role(data[1]):

                cases = BotDB().query_all_case_ids(target.id, inter.guild.id)
                if cases:
                    options = []
                    for case in cases:
                        query = BotDB().query_case_all(case[0], inter.guild.id)
                        
                        if query[6].split()[0] == "Closed":
                        
                            c_mod = inter.guild.get_member(query[0])
                            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])} (CLOSED)", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")

                            options.append(new_option)
                        
                        else:
                            c_mod = inter.guild.get_member(query[0])
                            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")

                            options.append(new_option)

                    options = options[:25]  

                    view = EditCaseDropdown(target.id, options)
                    i_embed = Embed(title=f"Cases from {target.name}", description="Please select a case to edit it", colour=config.blurple)  

                    await inter.response.edit_message(embed=i_embed, view=view)

                else:
                    notfound_embed = Embed(title=f"No Cases found", description=f"I couldn't find any strikes for {target.name}", colour=config.blurple)  
                    await inter.response.edit_message(embed=notfound_embed)

            else:
                no_perm_m = Embed(title="Missing Permissions", description="You don't have the required role!", color=config.red)
                await inter.response.edit_message(embed=no_perm_m)
                return False



class ShowCaseInfo_Closed(nc.ui.View):
    def __init__(self, case_creator, date, reason, info, changes, entry_type, case_status, target, case_id):
        super().__init__()  # Add this line to call the parent constructor
        self.case_creator = case_creator
        self.date = date
        self.reason = reason
        self.info = info
        self.changes = changes
        self.target = target
        self.case_id = case_id
        self.entry_type = entry_type
        self.case_status = case_status

    @nc.ui.button(label="Delete Case", style=nc.ButtonStyle.red, row=1, disabled=False)
    async def del_case(self, button: nc.ui.Button, inter: nc.Interaction):
        guild_exists = BotDB().query_server_table(inter.guild.id)
                    
        if guild_exists is None:
            fail_m = Embed(title="No role found", description="Please add Perm Roles with the setup commands to use this command!", colour=config.red)
            await inter.response.send_message(embed=fail_m)
            return False

        else:
            admin_role = BotDB().query_server_table(inter.guild.id)
            
            if inter.user.get_role(admin_role[1]):

                res = nc.Embed(title=f"Case {self.case_id} sucessfully deleted!", description="You will return to the Command before in 5 secounds!", colour=config.blurple)
                await inter.response.edit_message(embed=res, view=None)
                BotDB().delete_case(self.target, inter.guild.id, self.case_id)
                await asyncio.sleep(5)

                cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
                if cases:
                    options = []
                    for case in cases:
                        query = BotDB().query_case_all(case[0], inter.guild.id)
                        
                        if query[6].split()[0] == "Closed":
                        
                            c_mod = inter.guild.get_member(query[0])
                            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])} (CLOSED)", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")

                            options.append(new_option)
                        
                        else:
                            c_mod = inter.guild.get_member(query[0])
                            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")

                            options.append(new_option)

                    options = options[:25]  

                    view = EditCaseDropdown(self.target.id, options)
                    i_embed = Embed(title=f"Cases from {self.target}", description="Please select a case to edit it", colour=config.blurple)  

                    await inter.edit_original_message(embed=i_embed, view=view)
                else:
                    notfound_embed = Embed(title=f"No Cases found", description=f"I couldn't find any strikes for {self.target.name}", colour=config.blurple)  
                    await inter.edit_original_message(embed=notfound_embed)

            else:
                no_perm_m = Embed(title="Missing Permissions", description="You don't have the required role!", color=config.red)
                await inter.response.edit_message(embed=no_perm_m)
                return False

        


class EditCaseModal(nc.ui.Modal):
    def __init__(self, warned_by, date, reason, info, changes, entry_type, target, case_id, case_status):
        self.warned_by = warned_by
        self.date = date
        self.reason = reason
        self.info = info
        self.changes = changes
        self.target = target
        self.case_id = case_id
        self.entry_type = entry_type
        self.case_status = case_status


        super().__init__(f"Edit {self.entry_type}: {self.case_id}")
        self.new_reason = nc.ui.TextInput(label="Reason", style=nc.TextInputStyle.paragraph, placeholder="Type here your new reason", default_value=self.reason, required=True, max_length=50)

        self.add_item(self.new_reason)

                           
    async def callback(self, inter: nc.Interaction):

  
        current_time = config.aktuelldatum
        if self.changes is None:
            new_changes = f"Moderator: {inter.user.id} | {inter.user.name}\nOld Reason: {self.reason}\nNew Reason: {self.new_reason.value}\nDate: {current_time}\n---------------"
        else:
            old_changes = ''.join(self.changes)
            new_changes = f"{old_changes}\n\nModerator: {inter.user.id} | {inter.user.name}\n\n __Reason__\nOld: {self.reason}\nNew: {self.new_reason.value}\nDate: {current_time}"
        BotDB().update_case(self.new_reason.value, new_changes, self.case_id, inter.guild.id)

        
        e_updated = Embed(description="Case Overview", colour=config.blurple)
        e_updated.add_field(name="__Case ID__", value=f"{self.case_id}\n\uFEFF")
        e_updated.add_field(name="__Warned by__", value=f"<@{self.warned_by}>\n\uFEFF")
        e_updated.add_field(name="__Reason__", value=f"Old: `{self.reason}`\nNew: `{self.new_reason.value}`\n\uFEFF")
        e_updated.add_field(name="__Date__", value=f"<t:{self.date}:F>\n\uFEFF")
        e_updated.add_field(name="__Changes__", value=f"{new_changes}\n\uFEFF")


        await inter.response.edit_message(view=None)
        next_label = self.button_next.label.split()[1]
        site = int(next_label) - 1
        if site == 1:
            cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        else:
            cases = BotDB().query_all_cases_via_case_id_with_offset(site, self.target, inter.guild.id)
        options = []
        for case in cases:
            query = BotDB().query_case_reason_and_type(case[0], inter.guild.id)
            c_mod = inter.guild.get_member(query[0])
            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
            options.append(new_option)
        self.options = options
        
        await inter.edit_original_message(view=EditCaseDropdown(self.target, self.options))


#####  C A S E   I N F O  #####     


class CaseInfoDropdown(nc.ui.View):

    def __init__(self, target, options):

        super().__init__()
        self.target = target
        self.options = options
        self.button_back = self.children[0]
        self.button_next = self.children[1]
        self.select_edit_warn = SelctCaseInfo(self.target, self.options, self.button_back, self.button_next)
        self.add_item(self.select_edit_warn)
        
    def update_select_edit_warn_options(self, options):
        self.select_edit_warn.options = options
        
    @nc.ui.button(label="Page Back", style=nc.ButtonStyle.blurple, row=1, disabled=True)
    async def page_back(self, button: nc.ui.Button, inter: nc.Interaction):

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        button_count = int(button_back.label.split()[1]) if button.label else 1
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count -= 1
            options = []
            offset_count = button_count - 1
            button_back.label = f"Page {button_count}"
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            button_next.disabled = False
            if offset_count == 0:
                button_back.disabled = True
                button_back.label = "Page Back"
            else:
                button_back.disabled = False
            for case in cases:
                button_next.label = f"Page {button_count + 1}"
                query = BotDB().query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_edit_warn_options(options) # update SelectEditWarn options
            await inter.response.edit_message(view=self)
        
                
    @nc.ui.button(label="Page 2", style=nc.ButtonStyle.blurple, row=1)
    async def next_page(self, button: nc.ui.Button, inter: nc.Interaction):
        button_count = int(button.label.split()[1]) if button.label else 1

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count += 1
            button_next.label = f"Page {button_count}"
            options = []
            offset_count = button_count - 2
            back_label = button_count - 1
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            next_cases_check = BotDB().query_all_cases_via_case_id_with_offset(back_label, self.target, inter.guild.id)
            button_back.disabled = False
            
            button_back.label = f"Page {back_label}"
            if next_cases_check:
                button_next.disabled = False
            else:
                button_next.disabled = True
                await inter.response.edit_message(view=self)
                return
            for case in cases:
                query = BotDB().query_case_all(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_edit_warn_options(options) # update SelectEditWarn options
            await inter.response.edit_message(view=self)

                            
        else:
            button_next.disabled = True
            await inter.response.edit_message(view=self)


class SelctCaseInfo(nc.ui.Select):
    def __init__(self, target, options, button_back, button_next):
        super().__init__(placeholder="Choose a case", min_values=1, max_values=1, options=options)
        self.target = target
        self.options = options
        self.button_back = button_back
        self.button_next = button_next
    
    async def callback(self, inter: nc.Interaction):
        select_value = self.values[0].split()[1]

        query = BotDB().query_case_with_user(self.target, inter.guild.id, select_value)
        formated_reason = ''.join(query[2])
        if query[3] is None:
            formated_info = None
        else:
            formated_info = ''.join(query[3])
        member = inter.guild.get_member(query[0])
        if query[6].split()[0] == "CLOSED":
            i_embed = Embed(title=f"{query[5]}: {select_value}", description=f"Case opened by: {member.mention}\nCase Status: {query[6].split[0]}", colour=config.red)
        else:
            i_embed = Embed(title=f"{query[5]}: {select_value}", description=f"Case opened by: {member.mention}", colour=config.blurple)
        i_embed.add_field(name="Informations", value=f"Reason: {formated_reason}\n{formated_info if formated_info is not None else 'No Info'}\n\uFEFF")
        i_embed.add_field(name="Case History", value=f"{query[4] if query[4] is not None else 'No entrys'}\n\uFEFF")
        i_embed.add_field(name="Case opened at:", value=f"{query[1]}\n\uFEFF")

        await inter.response.send_message(embed=i_embed, ephemeral=True)


        
    




#####  D E L E T E   C A S E  #####     
                
class DeleteCaseDropdown(nc.ui.View):

    def __init__(self, target, options):

        super().__init__()
        self.target = target
        self.options = options
        self.button_back = self.children[0]
        self.button_next = self.children[1]
        self.select_del_warn = SelectDelWarn(self.target, self.options, self.button_back, self.button_next)
        self.add_item(self.select_del_warn)
        
    def update_select_del_warn_options(self, options):
        self.select_del_warn.options = options
        
    @nc.ui.button(label="Page Back", style=nc.ButtonStyle.blurple, row=1, disabled=True)
    async def page_back(self, button: nc.ui.Button, inter: nc.Interaction):

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        button_count = int(button_back.label.split()[1]) if button.label else 1
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count -= 1
            options = []
            offset_count = button_count - 1
            button_back.label = f"Page {button_count}"
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            button_next.disabled = False
            if offset_count == 0:
                button_back.disabled = True
                button_back.label = "Page Back"
            else:
                button_back.disabled = False
            for case in cases:
                button_next.label = f"Page {button_count + 1}"
                query = BotDB().query_case_reason_and_type(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_del_warn_options(options) # update SelectDelWarn options
            await inter.response.edit_message(view=self)
        
                
    @nc.ui.button(label="Page 2", style=nc.ButtonStyle.blurple, row=1)
    async def next_page(self, button: nc.ui.Button, inter: nc.Interaction):
        button_count = int(button.label.split()[1]) if button.label else 1

        count_cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        count = 0
        button_back = self.children[0]
        button_next = self.children[1]
        for amount in count_cases:
            count += 1
        if count > 25:
            button_count += 1
            button_next.label = f"Page {button_count}"
            options = []
            offset_count = button_count - 2
            back_label = button_count - 1
            cases = BotDB().query_all_cases_via_case_id_with_offset(offset_count, self.target, inter.guild.id)
            next_cases_check = BotDB().query_all_cases_via_case_id_with_offset(back_label, self.target, inter.guild.id)
            button_back.disabled = False
            
            button_back.label = f"Page {back_label}"
            if next_cases_check:
                button_next.disabled = False
            else:
                button_next.disabled = True
                await inter.response.edit_message(view=self)
                return
            for case in cases:
                query = BotDB().query_case_reason_and_type(case[0], inter.guild.id)
                c_mod = inter.guild.get_member(query[0])
                new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
                options.append(new_option)
            self.options = options
            self.update_select_del_warn_options(options) # update SelectDelWarn options
            await inter.response.edit_message(view=self)

                            
        else:
            button_next.disabled = True
            await inter.response.edit_message(view=self)


class SelectDelWarn(nc.ui.Select):
    def __init__(self, target, options, button_back, button_next):
        super().__init__(placeholder="Choose a case", max_values=len(options) if len(options) < 25 else 25, options=options)
        self.target = target
        self.options = options
        self.button_back = button_back
        self.button_next = button_next
    
    async def callback(self, inter: nc.Interaction):
        m = inter.guild.get_member(self.target)
        out = Embed(title=f"Deleted Cases from {m.name}", description=f"Here you will find all the cases you just removed from {m.mention}", colour=config.green)

        for value in self.values:
            v = value.split()[1]
            query = BotDB().query_case_all(v, inter.guild.id)
            formated_reason = ''.join(query[2])
            out.add_field(name=f"{query[5]}: {v}", value=f"Reason: {formated_reason}\n\uFEFF")
            if query[3] is not None:
                formated_info = ''.join(query[3])
                out.add_field(name=f"Case Informations", value=f"{formated_info}\n\uFEFF")
            if query[4] is not None:
                formated_history = ''.join(query[4])
                out.add_field(name=f"Case History", value=f"{formated_history}\n\uFEFF")
            out.add_field(name=f"Case Opened at:", value=f"{query[1]}\n\uFEFF")
            BotDB().delete_case(self.target, inter.guild.id, v)
        
        
        next_label = self.button_next.label.split()[1]
        site = int(next_label) - 1
        if site == 1:
            cases = BotDB().query_all_case_ids(self.target, inter.guild.id)
        else:
            cases = BotDB().query_all_cases_via_case_id_with_offset(site, self.target, inter.guild.id)
                    
        options = []
        for case in cases:
            query = BotDB().query_case_all(case[0], inter.guild.id)
            c_mod = inter.guild.get_member(query[0])
            new_option = nc.SelectOption(label=f"{query[5]}: {str(case[0])}", description=f"Case Opened by: {c_mod.name}\nReason: {query[2]}\n{query[3] if query[3] is not None else 'No Info'}")
            options.append(new_option)
        self.options = options

        if len(self.options) == 0:
            cancel_error_png_a = File("pictures/cancel_and_error_maja.png", filename="cancel_and_error_maja.png")
            no_more = Embed(title=f"No more Warnings found for {m.name}", description=f"I could not find any warnings for {m.mention} in the system for this server", colour=config.red)
            no_more.set_thumbnail(url="attachment://cancel_and_error_maja.png")
            await inter.response.edit_message(view=None, embed=no_more, file=cancel_error_png_a)
            
            check_mark_maja_png = nc.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
            out.set_thumbnail(url="attachment://check_mark_maja.png")
            await inter.followup.send(embed=out, file=check_mark_maja_png, ephemeral=True)
        else:
            check_mark_maja_png = nc.File("pictures/check_mark_maja.png", filename="check_mark_maja.png")
            out.set_thumbnail(url="attachment://check_mark_maja.png")
            await inter.response.edit_message(view=DeleteCaseDropdown(self.target, self.options))
            await inter.followup.send(embed=out, file=check_mark_maja_png, ephemeral=True)
            
    
 
            

#### M E M B E R   T I M E O U T ####

class MT(nc.ui.Modal):
    def __init__(self, target):
        self.target = target

        super().__init__(f"Create Timeout for {self.target}")
        self.reason = nc.ui.TextInput(label="Reason", style=nc.TextInputStyle.paragraph, placeholder="Type here your reason", required=True, max_length=50, default_value="No Reason")
        self.days = nc.ui.TextInput(label="Days", style=nc.TextInputStyle.short, max_length=2, placeholder="Max 28 Days", default_value="0")
        self.hours = nc.ui.TextInput(label="Hours", style=nc.TextInputStyle.short, max_length=3, placeholder="Max 672 Hours", default_value="0")
        self.minutes = nc.ui.TextInput(label="Minutes", style=nc.TextInputStyle.short, max_length=5, placeholder="Max 40320 Minutes", default_value=5)
        self.seconds = nc.ui.TextInput(label="Seconds", style=nc.TextInputStyle.short, max_length=7, placeholder="Max 2419200 Seconds", default_value="0")
        self.add_item(self.reason)
        self.add_item(self.days)
        self.add_item(self.hours)
        self.add_item(self.minutes)
        self.add_item(self.seconds)

                           
    async def callback(self, inter: nc.Interaction):
        if isinstance(int(self.days.value), int) and isinstance(int(self.hours.value), int) and isinstance(int(self.minutes.value), int) and isinstance(int(self.seconds.value), int):
            now = nc.utils.utcnow()
            delta = timedelta(days=int(self.days.value), hours=int(self.hours.value), minutes=int(self.minutes.value), seconds=int(self.seconds.value))
            if delta <= timedelta(days=28):
                
                deadline = now + delta
                
                random_id = generate_random_id(10)

                wait = nc.Embed(description=f"Please wait a moment. I prepare everything!", colour=config.red)
                
                await inter.response.send_message(embed=wait, ephemeral=True)
                
                now_timestamp = nc.utils.format_dt(now, style='F')
                future_timestamp = nc.utils.format_dt(deadline, style='F')

                formated_reason = ''.join(self.reason.value)
                
                timeoutdm = nc.Embed(title=f"You got a timeout on {inter.guild.name}",
                                        description="Information about your timeout", colour=config.yellow)
                timeoutdm.set_author(name=inter.guild.name)
                timeoutdm.add_field(name="You received your timeout at:", value=now_timestamp, inline=True)
                timeoutdm.add_field(name=f"Your timeout ends at:", value=future_timestamp)
                timeoutdm.add_field(name="Reason:", value=f"`{formated_reason}`")
                timeoutdm.set_footer(text=f"Moderator {inter.user.name} ➟ {inter.user.id}", icon_url=inter.user.avatar.url)
                
                timeoutctx = nc.Embed(description=f"{config.DiscordMuted} {self.target.mention} has successfully received his timeout", colour=config.blurple)
                
                try:
                    await self.target.send(embed=timeoutdm)
                    timeoutctx.add_field(name="DM Status", value="This member has been notified of their private message timeout.")
                except:
                    timeoutctx.add_field(name="DM Status", value="The member could not be notified of its timeout.")
                    pass
                
                await self.target.edit(timeout=deadline)
                await inter.edit_original_message(embed=timeoutctx)
                BotDB().insert_case(inter.guild.id, self.target.id, inter.user.id, config.aktuelldatum, formated_reason, f"Duration: {delta}\nExecution: Added", random_id, "Timeout", "Open")
            
            else:
                embed = nc.Embed(description=f"{config.a_cross} The member **{self.target}** could not be put into the timeout because the specified time was more than **28 days**.")
                await inter.response.send_message(embed=embed, ephemeral=True)   

        else:
            r = nc.Embed(title="Input incorrect", description="The Days, Hours, Minutes, and Seconds fields can only contain numbers", colour=config.red)
            await inter.response.send_message(embed=r, ephemeral=True)
        

                
            
                
