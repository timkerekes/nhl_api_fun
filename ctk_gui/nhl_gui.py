# import tkinter
import customtkinter
from PIL import Image
import sys
import os
from pynput import keyboard

# Add the parent folder to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nhl_api import *

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("NHL API")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=2)

        #### Create Sidebar Frame with App Settings Widgets (turn into navigation later?) ####
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=2)

        self.my_image = customtkinter.CTkImage(light_image=Image.open("./NHL_LOGO.png"),
                                               dark_image=Image.open(
            "./NHL_LOGO.png"),
            size=(199.2, 143.4))

        self.image_label = customtkinter.CTkLabel(
            self.sidebar_frame, image=self.my_image, text="")
        self.image_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("Dark")
        self.appearance_mode_optionemenu.grid(
            row=2, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 10))

        #### Create Searching Options Frame & Widgets ####
        self.center_frame = customtkinter.CTkFrame(
            self, corner_radius=0)
        self.center_frame.grid(row=0, column=1, columnspan=2, rowspan=3, sticky="NSEW")

        self.logo_label = customtkinter.CTkLabel(
            self.center_frame, text="Team Name:", font=customtkinter.CTkFont(size=20), anchor='w')
        self.logo_label.grid(row=0, column=1, padx=20, pady=(10, 0))

        # self.game_type_optionmenu = customtkinter.CTkOptionMenu(
        #     self, values=["Season", "Playoffs"])
        # self.game_type_optionmenu.grid(row=1, column=1)

        self.get_team_info_entry = customtkinter.CTkEntry(self.center_frame,
                                                          placeholder_text="Enter Team Name")
        self.get_team_info_entry.grid(row=0, column=2, padx=20, pady=(10, 10))

        self.get_team_info_button = customtkinter.CTkButton(self.center_frame,
                                                            text="Search", command=self.get_team_info)
        self.get_team_info_button.grid(row=0, column=3, padx=20, pady=(10, 10))

        #### Create Search Output Frame & Widgets ####
        self.output_frame = customtkinter.CTkFrame(
            self, corner_radius=0)
        self.output_frame.grid(row=2, column=1, columnspan=2, rowspan=3)

        self.output_textbox = customtkinter.CTkTextbox(
            self.output_frame, height=400, width=850, corner_radius=0, border_spacing=3, font=('Arial', 16))
        self.output_textbox.grid(row=2, column=1)

        self.get_team_info_entry.focus_set()

        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    ##########################FUNCTIONS##########################

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def get_team_info(self):
        self.output_textbox.configure(state='normal')
        self.output_textbox.delete("0.0", "end")
        team = self.get_team_info_entry.get().lower()

        if team:
            results = getNhlStandings(team)
            self.output_textbox.insert("0.0", results)
            self.output_textbox.configure(state='disabled')
        else:
            error = self.output_textbox.insert("0.0", "Please Enter A Team Name Above\n(Eg. Colorado Avalanche, Avalanche, avalanche)")
            self.output_textbox.configure(state='disabled')
            return error
        
    #### HANDLE KEY PRESS ####
        
    def on_key_press(self, key):
        if key == keyboard.Key.enter:
            print('Enter key pressed')
            self.get_team_info()


if __name__ == "__main__":
    app = App()
    app.mainloop()
