#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image, ImageTk
from Main_Frame_B import mianFrameB
from Main_Frame_config import ConfigFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('1366x768+100+100')
        # self.attributes("-fullscreen", True)

class mainFrameA(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""
    def __init__(self, master):
        super().__init__(master)

        global img1, img2 ,img3
        container = tk.Frame(self, width=1366, height=768)
        container.pack()

        # --------------------------------------文字--------------------------------------

        tk.Label(container, text='认知量表评分辅助系统', font=('黑体', 58)).place(relx=.5, rely=.3, anchor="center")
        tk.Label(container, text='尤组专用   版本号 v1.0.0   更新日期：2022/09/14', font=('黑体', 25)).place(relx=.5, rely=.4,
                                                                                               anchor="center")

        # --------------------------------------按钮--------------------------------------
        Button_box = tk.Frame(container)
        Button_box.place(relx=.5, rely=.65, anchor="center")

        img1 = ImageTk.PhotoImage(Image.open('img/ico_config_128.png'))
        img2 = ImageTk.PhotoImage(Image.open('img/ico_new_128.png'))
        img3 = ImageTk.PhotoImage(Image.open('img/ico_quit_128.png'))

        def switchToConfig():
            topLevel_config = tk.Toplevel(app)
            topLevel_config.geometry('1366x768+100+100')
            # topLevel_config.overrideredirect(True)      # 取消窗口边框
            topLevel_config.wm_attributes("-topmost", 1)  # 置顶，当前GUI为普通窗口
            # 全屏
            # topLevel_config.attributes("-fullscreen", True)
            # topLevel1.attributes('-topmost', True)
            demoFrame_ = ConfigFrame(topLevel_config)
            demoFrame_.pack(fill=tk.BOTH, expand=True)

        def switchToFrameB():
            topLevel_mainframeB = tk.Toplevel(app)
            topLevel_mainframeB.geometry('1366x768+100+100')
            # 全屏
            # topLevel_mainframeB.attributes("-fullscreen", True)
            # topLevel_mainframeB.overrideredirect(True)      # 取消窗口边框
            # topLevel_mainframeB.wm_attributes("-topmost", 1)  # 置顶，当前GUI为普通窗口
            # topLevel_mainframeB.attributes('-topmost', True)
            mianFrameB_ = mianFrameB(topLevel_mainframeB)
            mianFrameB_.pack(fill=tk.BOTH, expand=True)

        def QuitAll():
            self.quit()

        # 设置按钮1
        Button1 = tk.Label(Button_box, image=img1,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button1.grid(row=0, column=0, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button1.bind('<Button-1>', lambda e: switchToConfig())  # 左键切换为橙色界面
        tk.Label(Button_box, text='配置', font=('黑体', 25)).grid(row=1, column=0, sticky='n')

        # 设置按钮2
        Button2 = tk.Label(Button_box, image=img2,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button2.grid(row=0, column=1, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button2.bind('<Button-1>', lambda e: switchToFrameB())  # 左键切换为橙色界面
        tk.Label(Button_box, text='开始', font=('黑体', 25)).grid(row=1, column=1, sticky='n')

        # 设置按钮3
        Button3 = tk.Label(Button_box, image=img3,relief=tk.GROOVE,bd=2,width=200,height=160)
        Button3.grid(row=0, column=2, sticky='nw', padx=30, pady=0, ipadx=0, ipady=0)
        Button3.bind('<Button-1>', lambda e: QuitAll())  # 左键切换为橙色界面
        tk.Label(Button_box, text='关闭', font=('黑体', 25)).grid(row=1, column=2, sticky='n')


if __name__ == "__main__":
    app = App()

    mainFrame_ = mainFrameA(app)
    mainFrame_.pack(fill=tk.BOTH, expand=True)

    ConfigFrame_ = ConfigFrame(app)
    demoFrame_ = mianFrameB(app)

    app.mainloop()

