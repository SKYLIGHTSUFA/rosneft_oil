import customtkinter as ctk
import os
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk


class Predict(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.storage_name: str
        self.grid_columnconfigure(0, weight=1)
       # self.grid_rowconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Predict", fg_color="blue", text_color="white")
        self.label.grid(row=0, column=0, sticky="ew")
        self.button_get_dir = ctk.CTkButton(self, text="Choose folder", command=self.__open_file_dialog)
        self.button_get_dir.grid(row=1, column=0, pady=10, sticky="ew")
        self.button_start_predict = ctk.CTkButton(self, text="Start predict", command=self.__start_predict)
        self.button_start_predict.grid(row=2, column=0, pady=10, sticky="ew")


    def __open_file_dialog(self):
        root = ctk.CTk()
        root.withdraw()
        file_path = ctk.filedialog.askdirectory(title='Choose image dataset')
        if file_path != '':
            root.destroy()
            self.storage_name = file_path
            self.iterator = iter(os.listdir(self.storage_name))
            return file_path
    def __start_predict(self):
        model = YOLO("models/best3_all_data_v8s.pt")
        filename = next(self.iterator)
        if filename.endswith("png"):
            print(filename)
            results = model.predict(source=os.path.join(self.storage_name, filename), verbose=False)
            conf = results[0].probs.data.tolist()
            idx = conf.index(max(conf))
            print(f'idx = {idx}, filename = {filename}')
            image = cv2.imread(os.path.join(self.storage_name, filename))
            image = cv2.putText(image, ["BAD", "GOOD"][bool(idx != 0)],
                                (100, 100),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1,
                                color=(0, 255, 0),
                                thickness=2, )
            self.image = Image.fromarray(image)
            self.image_tk = ctk.CTkImage(self.image, size=(self.image.width, self.image.height))
            self.label = ctk.CTkLabel(self, image=self.image_tk)
            self.label.grid(row=3, column=0, pady=10, sticky="ew")
