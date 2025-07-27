import nextcord
from nextcord.ui import View
from nextcord import Embed, Interaction

import asyncio


#####################################################################################################
class RadioDropdown(nextcord.ui.View):

    def __init__(self, options, voice_client):

        super().__init__()
        self.options = options
        self.voice_client = voice_client
        self.page_number = 1
        self.options_per_page = 25
        self.button_back = self.children[0]
        self.button_next = self.children[1]
        self.SelectRadio = SelectRadio([], self.button_back, self.button_next, voice_client)
        self.add_item(self.SelectRadio)
        self.update_select()

    def update_select(self):
        start_index = (self.page_number - 1) * self.options_per_page
        end_index = start_index + self.options_per_page
        options_page = self.options[start_index:end_index]
        self.SelectRadio.options = options_page

    def update_select_radio_options(self, options):
        self.options = options
        self.update_select()

    @nextcord.ui.button(label="<< Prev", style=nextcord.ButtonStyle.blurple, disabled=True, row=2)
    async def r_previous_page(self, button: nextcord.Button, inter: nextcord.Interaction):
        if self.page_number > 1:
            self.page_number -= 1
            self.update_select()
            self.button_back.disabled = True
            self.button_next.disabled = False
            await inter.response.edit_message(view=self)

    @nextcord.ui.button(label="Next >>", style=nextcord.ButtonStyle.blurple, row=2)
    async def r_next_page(self, button: nextcord.ui.Button, inter: nextcord.Interaction):
        total_pages = (len(self.options) - 1) // self.options_per_page + 1

        if self.page_number < total_pages:
            self.page_number += 1
            self.update_select()
            self.button_back.disabled = False
            self.button_next.disabled = True
            await inter.response.edit_message(view=self)


class SelectRadio(nextcord.ui.Select):
    def __init__(self, options, button_back, button_next, voice_client):
        super().__init__(placeholder="Choose a radio", min_values=1, max_values=1, options=options, row=1)
        self.options = options
        self.button_back = button_back
        self.button_next = button_next
        self.voice_client = voice_client

    async def callback(self, inter: nextcord.Interaction):
        selected_option = self.values[0] 
        selected_option_value = None
        
        for option in self.options:
            if option.label == selected_option:
                selected_option_value = option.value
                break
            
        self.voice_client.stop()
        await asyncio.sleep(1)
        self.voice_client.play(nextcord.FFmpegPCMAudio(f"{selected_option}"))
        

        
    