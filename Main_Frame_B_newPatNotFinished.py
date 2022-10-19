#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import time
import pandas as pd
from Main_Frame_C import mianFrameC
from tools import AppSettings

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('700x400+600+300')
        self.attributes("-topmost", 1)

        newPatNotFinished(self,1).pack(pady=50)


class newPatNotFinished(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def on_main_click(self, event):
        print("sub-canvas binding")

    def __init__(self, master,rowIndex):
        super().__init__(master)
        self.rowIndex = rowIndex

        dataFilePath = AppSettings.dataFilePath()
        df = pd.read_csv(dataFilePath)  # 把【INDEX】列标签作为行的索引

        patName_ = df.iloc[rowIndex, list(df.columns).index('姓名')]
        hospID_ = df.iloc[rowIndex, list(df.columns).index('住院号')]
        wardID_ = df.iloc[rowIndex, list(df.columns).index('病区')]
        bedID_ = df.iloc[rowIndex, list(df.columns).index('床号')]
        createTime = df.iloc[rowIndex, list(df.columns).index('最初创建时间')]
        barValue = df.iloc[rowIndex, list(df.columns).index('完成进度')]

        def callback(event):
            newFrameeee = tk.Toplevel(self)
            newFrameeee.title('子窗口')
            newFrameeee.geometry('1366x768+100+100')
            # 全屏
            # newFrameeee.attributes("-fullscreen", True)

            demoFrame_ = mianFrameC(newFrameeee, dataFilePath, rowIndex)
            demoFrame_.pack(fill=tk.BOTH, expand=True)
            # print("clicked at:", event.x, event.y)  # 打印出该事件（按下鼠标）的x，y轴


        lastChangeTime = ' 末次修改：'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+' '
        FRAME_1 = tk.LabelFrame(self,
                           width=260,
                           height=150,
                           padx=10, pady=5,
                           text=lastChangeTime,
                           font=('仿宋',12),
                           labelanchor='nw',)

        FRAME_1.propagate(False)
        FRAME_1_canvas = tk.Canvas(FRAME_1)
        FRAME_1_canvas.pack()
        FRAME_1_canvas.bind('<1>', callback)
        FRAME_1.pack()

        info_Frame = tk.Frame(FRAME_1_canvas)
        info_Frame.pack()

        label_options = {'fg': "black", 'bg': '#f0f0f0', 'font': ("黑体", 14)}
        grid_options = {'sticky': "NW", 'pady': 0, 'padx':1}
        # ---------------------------------------------------------
        # 左侧信息栏
        frame1 = tk.Frame(info_Frame, bg='#f0f0f0')
        frame1.pack(side='left', anchor=tk.NW)


        tk.Label(frame1, text=patName_[:-1], **label_options).grid(row=1, column=0, **grid_options)
        tk.Label(frame1, text=hospID_[:-1], **label_options).grid(row=2, column=0, **grid_options)

        # ---------------------------------------------------------
        # 中间分隔
        sep = ttk.Separator(info_Frame, orient=tk.VERTICAL, style='red.TSeparator')
        sep.pack(side='left', fill=tk.Y, padx=5)

        # ---------------------------------------------------------
        # 右侧信息栏
        frame2 = tk.Frame(info_Frame, bg='#f0f0f0')
        frame2.pack(side='left', anchor=tk.NW)

        frame2_1 = tk.Frame(frame2, bg='#f0f0f0')
        frame2_1.grid(row=0, column=0, **grid_options)

        tk.Label(frame2_1, text=wardID_[:-1]+bedID_[:-1]+'床', **label_options).grid(row=0, column=0, **grid_options)
        tk.Label(frame2_1, text='术前',fg='#ffffff',font=("黑体", 14,'bold'), bg='#008000').grid(row=0, column=1,**grid_options)
        tk.Label(frame2, text='🅽'+str(createTime)[:10], **label_options).grid(row=1, column=0, **grid_options)

        # ---------------------------------------------------------
        frame3 = tk.Frame(FRAME_1_canvas)

        def Pro_Bar_npnf(root, value):
            # 进度条
            BarStyle_npnf = ttk.Style()
            BarStyle_npnf.theme_use('classic')
            # win10环境下主题：('winnative','clam','alt','default','classic','vista','xpnative')
            # 进度条漕的宽度改变测试成功的是：'winnative','alt','default','classic'
            BarStyle_npnf.configure("my0.Horizontal.TProgressbar", troughcolor='white', background='#499c54',
                               thickness=80)  # troughcolor 水槽色

            progressbar = ttk.Progressbar(root, style="my0.Horizontal.TProgressbar", length=200)
            progressbar['maximum'] = 80  # 设置进度条最大值为100
            progressbar['length'] = 280  # 设置进度条长度
            progressbar['value'] = value

            progressbar.pack()
            progressbar.bind('<1>', callback)
            root.update()

        Pro_Bar_npnf(frame3,barValue)

        frame3.pack(side='left',fill=tk.X,pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
