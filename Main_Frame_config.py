#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('1366x768+100+100')
        # self.attributes("-topmost", 1)
        self.configure(bg="black")

        ConfigFrame(self).pack(fill=tk.BOTH, expand=True)


class ConfigFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def __init__(self, master):
        super().__init__(master)

        global img_ico_close_48

        # ////////////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------顶条--------------------------------------
        def askToQuit():
            # self.quit()
            self.destroy()
            self.master.destroy()

        titleBG = '#2b2b2b'
        # ////////////////////////////////////////////////////////
        # 创建框架和画布
        FRAME_TOP = tk.Frame(self,bg=titleBG,bd=3)

        FRAME_111 = tk.Frame(FRAME_TOP,bg=titleBG)
        FRAME_111.place(relx=.50, rely=.5, anchor="center")
        tk.Label(FRAME_111,fg = 'white',bg =titleBG,font=('黑体', 28),text='设 置 页 面').pack()

        # 设置按钮
        img_ico_close_48 = ImageTk.PhotoImage(Image.open('img/ico_返回_i_64.png'))
        tk.Button(FRAME_TOP, image=img_ico_close_48, command=askToQuit,relief='flat',bd=1).pack(side='right')

        # 放置
        FRAME_TOP.pack(fill=tk.X)  # 放置第二级
        # ////////////////////////////////////////////////////////

        mianFrame = tk.Frame(self)
        mianFrame.pack()
        entry_usr_name = tk.Entry(mianFrame, font=('Arial', 14))
        entry_usr_name.pack()   # 放置的命令必须分开，因为上一步是创建变量

if __name__ == "__main__":
    app = App()
    app.mainloop()