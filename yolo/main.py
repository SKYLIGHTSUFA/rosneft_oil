from tkinter import messagebox
from Class_start import Start


def on_closing():
    if messagebox.askokcancel("Подтверждение закрытия", "Вы уверены, что хотите закрыть приложение?"):
        app.destroy()

app = Start()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
