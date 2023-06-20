# import tkinter
import customtkinter
from PIL import Image


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
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create Sidebar Frame with App Settings Widgets (turn into navigation later?)
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=1)

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

        # Create Searching Options Frame & Widgets
        self.logo_label = customtkinter.CTkLabel(
            self, text="Record Types", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1)

        self.game_type_optionmenu = customtkinter.CTkOptionMenu(
            self, values=["Season", "Playoffs"])
        self.game_type_optionmenu.grid(row=1, column=1)

        # Create Search Output Frame & Widgets
        self.output_frame = customtkinter.CTkFrame(
            self, corner_radius=0)
        self.output_frame.grid(row=2, column=1, columnspan=3, sticky="NSEW")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
