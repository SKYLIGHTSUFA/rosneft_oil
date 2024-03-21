import customtkinter as ctk
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import random
import time
import statistics
from tkinter import messagebox


def show_error_message(message):
    messagebox.showerror("Ошибка", message)
    return

class Dataset(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.xlsx_file: str
        self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Create dataset", fg_color="blue", text_color="white")
        self.label.grid(row=0, column=0, sticky="ew")
        self.button_get_file = ctk.CTkButton(self, text="Choose file data", command=self.__open_file_dialog)
        self.button_get_file.grid(row=1, column=0, pady=10, sticky="ew")
        self.check_var = ctk.StringVar(value="on")
        self.checkbox = ctk.CTkCheckBox(self, text="Use axis", command=self.checkbox_event,
                                             variable=self.check_var, onvalue="on", offvalue="off")
        self.checkbox.grid(row=3, column=0, pady=5, sticky="ew")
        self.check_var_dot = ctk.StringVar(value="on")
        self.checkbox_dot = ctk.CTkCheckBox(self, text="Use dot and values", command=self.checkbox_event_dot,
                                        variable=self.check_var_dot, onvalue="on", offvalue="off")
        self.checkbox_dot.grid(row=4, column=0, pady=5, sticky="ew")
        self.button_generator_images = ctk.CTkButton(self, text="Start generate image",
                                                     command=self.__start_generator)
        self.button_generator_images.grid(row=5, column=0, pady=10, sticky="ew")
        self.bar = ctk.CTkProgressBar(master=self,
                                      orientation='horizontal',
                                      mode='determinate')

        self.bar.grid(row=6, column=0, pady=10, padx=20, sticky="n")
        self.bar.set(0)
    def __start_generator(self):
        df = pd.read_excel(self.xlsx_file, sheet_name="Обрывы_акт.мощность")
        df.drop(["Мест-е"], axis=1, inplace=True, errors="ignore")
        df.drop(["Площадь"], axis=1, inplace=True, errors="ignore")
        df.drop(["mst"], axis=1, inplace=True, errors="ignore")
        df["p"] = df.apply(lambda x: str(x.p).replace(",", "."), axis=1)

        def get_num(x):
            try:
                if isinstance(float(x), float):
                    return round(float(x), 2)
            except:
                return None

        df["p"] = df["p"].apply(lambda x: get_num(x))
        df.query("p >=-100 and p<=100", inplace=True)
        self.info__values = ctk.CTkLabel(self,
                                         text=f"min = {round(df['p'].min(),2)}, max = {round(df['p'].max(),2)}, mean = {round(df['p'].mean(),2)}")
        self.info__values.grid(row=7, column=0, pady=10, sticky="we")
        self.info__process = ctk.CTkLabel(self,
                                         text=f"grouping data of each scv")
        self.info__process.grid(row=8, column=0, pady=10, sticky="we")
        dicter = defaultdict(list)
        for index, row in df.iterrows():
            dicter[row["skv"]].append(round(row["p"], 2))
        self.info__process1 = ctk.CTkLabel(self,
                                          text=f"Creating dir and get images")
        self.info__process1.grid(row=9, column=0, pady=10, sticky="we")
        # plt.figure(figsize=(1.28, 1.28))
        for k, v in tqdm(dicter.items()):
            count = 0
            os.makedirs(f'images//Скв_{k}', exist_ok=True)
            # if k != 1101:continue
            while 12 * (count + 1) <= len(v):
                dots = v[count * 12:(count + 1) * 12]
                if len(dots) != 12: print(len(dots))
                if 0.65 < statistics.pstdev(dots) < 0.95: print(k, count + 1)
                if statistics.pstdev(dots) < 0.65:
                    normalized_data = list(map(lambda x: 0.3, dots))
                else:
                    normalized_data = [(value - min(dots)) / (max(dots) - min(dots)) for value in dots]
                # print(count, normalized_data, dots)
                count += 1
                # plt.axis([0, 12, 0, 1])
                plt.axis(self.checkbox.get())
                plt.plot(range(12), normalized_data, linewidth=1, color="black")

                if self.checkbox_dot.get() == "on":
                    plt.plot(range(12), normalized_data, "ro")
                    for index, y in enumerate(normalized_data):
                        plt.text(index,y,dots[index])
                plt.savefig(os.path.join(f'images/Скв_{k}', f'scv_{k}_{count}'), pad_inches=0)
                plt.clf()

    def __open_file_dialog(self):
        root = ctk.CTk()
        root.withdraw()
        file_path = ctk.filedialog.askopenfile(title='Choose data of xlsx')
        if file_path != '':
            root.destroy()
            self.xlsx_file = file_path.name
            print(self.xlsx_file)
            return file_path

    def checkbox_event(self):
        print("checkbox toggled, current value:", self.check_var.get())
    def checkbox_event_dot(self):
        print("checkbox toggled, current value:", self.check_var_dot.get())