import customtkinter
import platform
import  customtkinter as ctk
from Class_Predict import Predict
from Class_dataset import Dataset
class Start(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        #self.title(" ($",")
        #self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.predict = Predict(self, title="K1@0BL")
        self.predict.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.dataset = Dataset(self)
        self.dataset.grid(row=0, column=1, sticky="nsew", pady=5)

        '''
        system = platform.system()
        if system == "Windows":
            self.after(0, lambda: self.state('zoomed'))
        elif system == "Linux":
            print("-B0 ?@>3@0<<0 @01>B05B =0 Linux")
            self.attributes("-fullscreen", True)
        self.bind("<F12>", lambda event: self.attributes("-fullscreen",
                                                         not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        '''