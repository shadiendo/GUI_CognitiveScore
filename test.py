import tkinter as tk

class App(tk.Tk):
    """Creat mian window"""
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('480x240')
        self.resizable(False, False)


if __name__ == "__main__":
    # 自此可以多次创建窗口，比如app1为窗口1，app2为窗口2
    app1 = App()
    app1.mainloop()

    # app2 = App()
    # app2.mainloop()