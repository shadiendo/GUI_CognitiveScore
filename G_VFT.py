#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
import time
import tkinter as tk
from tkinter import Scrollbar
from tkinter import ttk
from tools import AppSettings
import numpy as np
import pandas as pd
import tools


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        VFTFrame(self, patName, hospID, invTime).pack()


class VFTFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID, invTime):
        super().__init__(master)
        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 基础设置 ----------------------------------
        CANVAS_bg = 'white'
        div0_bg = 'white'
        commonBG = 'white'
        highlightBG = '#f2f2f2'
        # 设置窗口长宽
        container_width = 1015
        container_height = 1400
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, bg=CANVAS_bg, width=container_width, height=container_height)
        # 创建滚动条
        scro = Scrollbar(master=self, width=70)
        scro.pack(side='right', fill='y')
        scro.config(command=CANVAS.yview)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS, bg=div0_bg, width=container_width, height=container_height)
        bigBox.pack(anchor=tk.N, side='right')
        bigBox.pack_propagate(False)
        bigBox.update()
        # 进一步将三者绑定
        CANVAS.create_window((10, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()
        # /////////////////////////////////////////////////////////////////////////////
        outcome_frame = tk.Frame(bigBox, bg=commonBG)
        outcome_frame.pack(anchor='w')

        # 实时的将修改的ADL评分传入excel
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName, hospID, invTime])

        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')  # 打开excel并把 INDEX 列设置为行索引
        STTscore = csvDf.loc[patientAnchor, 'VFT评分']  # 通过行索引定位，然后输出列标签为 ADL_record 的值

        titleFrame = tk.Frame(outcome_frame, bg='#94558d')
        titleFrame.pack(anchor='w')
        tk.Label(outcome_frame, fg='white', bg='#94558d', font=('黑体', 18),
                 text=patName[:-1] + '★' + hospID[:-1] + '★' + invTime).pack(anchor='w')

        ffffff = True
        try:
            if np.isnan(STTscore):
                ffffff = False
        except:
            pass
        if ffffff:
            tk.Label(outcome_frame, fg='white', bg='#94558d', font=('黑体', 18),
                     text='该患者已进行评分！分数为：' + str(STTscore)).pack(
                anchor='w')

        # ---------------------------- 标题 ----------------------------------
        # 标题frame
        title_frame = tk.Frame(bigBox, bg=commonBG)
        title_frame.pack()

        # 空行
        tk.Label(title_frame, font=('', 7), bg=commonBG).pack()
        tk.Label(title_frame, fg="black", bg=commonBG, font=('黑体', 18),
                 text='言语流畅性测试').pack()

        # /////////////////////////////////////////////////////////////////////////////
        global countTime, runFlag, restartflag

        restartflag = False
        countTime = 0
        runFlag = False

        def cyclethread():
            global countTime, runFlag, restartflag

            restartflag = False

            while 1:
                if restartflag:  # 用于重置
                    countTime = 0
                    restartflag = False

                countTime = countTime + 1
                progressbar1['value'] = countTime
                if 15 <= countTime < 30:
                    progressbar2['value'] = countTime - 14
                if 30 <= countTime < 45:
                    progressbar3['value'] = countTime - 29
                if 45 <= countTime < 60:
                    progressbar4['value'] = countTime - 44

                restartflag = False
                middleFrame.update()
                if countTime <= 0:  # 当时间到的时候运行结束
                    runFlag = False
                    # 这里有个bug,就是在外部引用时,一旦销毁本窗口,那么如果还在运行子进程,就会报错
                    return
                time.sleep(1)

        def startCount():  # 开始计时，把开始计时标签变成True
            global restartflag
            global runFlag
            restartflag = True
            progressbar1['value'] = 0
            progressbar2['value'] = 0
            progressbar3['value'] = 0
            progressbar4['value'] = 0

            if not runFlag:
                th = threading.Thread(target=cyclethread)
                th.setDaemon(True)
                th.start()
                runFlag = True

        def warning():
            main_toplevel = tk.Toplevel(self)
            winWidth = 500
            winHeight = 400
            screenWidth = self.winfo_screenwidth()  # 1920
            screenHeight = self.winfo_screenheight()  # 1080
            x = int((screenWidth - winWidth) / 2)
            y = int((screenHeight - winHeight) / 2)
            main_toplevel.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
            main_toplevel.overrideredirect(True)  # 取消窗口边框
            main_toplevel.attributes('-topmost', True)  # 为了让注册页面置顶

            def QuitCancel():
                main_toplevel.destroy()
                BC_toplevel.destroy()

            tk.Label(main_toplevel, text="某一个15秒还是默认值，请选择患\n者的结果，即使是0也要选一下！", font=('黑体', 18)).place(relx=.5, rely=.4, anchor="center")
            tk.Button(main_toplevel,text ="了解了",font=('Arial', 28), command=QuitCancel, relief='flat',bg='#825471',fg='white').place(relx=.5, rely=.65,anchor="center")

            # ---------------------------- 先放黑色背景 ------------------------------------
            BC_toplevel = tk.Toplevel(self)
            BC_toplevel.attributes('-alpha', 0.5)  # 设置透明度
            BC_toplevel.overrideredirect(True)  # 取消窗口边框
            BC_toplevel.state("zoomed")  # 最大化
            BC_toplevel.attributes('-topmost', True)  # 是否置顶
            Curtain = tk.Frame(BC_toplevel, bg='black')  # 设置幕布背景为纯黑
            Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充

        def saveCanvas():  # 开始计时，把开始计时标签变成True
            score = [scale1.get(), scale2.get(), scale3.get(), scale4.get()]
            print(score)

            flagg = False
            for i in score:
                if i == -1:
                    flagg = True
                    continue
            if flagg:
                warning()
            else:
                time_now = str(time.strftime('%Y-%m-%d %H.%M.%S'))  # 当前时间
                patPath1 = 'data\\VectorGraphic\\' + patName + '★' + hospID + '★' + invTime
                patPath2 = patPath1 + '\\' + time_now + 'VFT'

                if not os.path.exists(patPath1):
                    os.mkdir(patPath1)
                if not os.path.exists(patPath2):
                    os.mkdir(patPath2)

                fA1.canvas.postscript(file=os.path.join(patPath2, '1st 15s.ps'), colormode='color')  # 扩展名可为ps或esp
                fA2.canvas.postscript(file=os.path.join(patPath2, '2nd 15s.ps'), colormode='color')  # 扩展名可为ps或esp
                fA3.canvas.postscript(file=os.path.join(patPath2, '3rd 15s.ps'), colormode='color')  # 扩展名可为ps或esp
                fA4.canvas.postscript(file=os.path.join(patPath2, '4th 15s.ps'), colormode='color')  # 扩展名可为ps或esp

                print('成功保存图片至%s' % str(patPath2))

                dataFilePath = AppSettings.dataFilePath()
                patientAnchor = '★'.join([patName, hospID, invTime])
                tools.writeDataframeData(dataFilePath, patientAnchor, 'VFT评分', str(score))  # 传入记录的过程
                tools.writeDataframeData(dataFilePath, patientAnchor, 'VFT进度', 10)  # 传入记录的总分
                # 将总分修改并传入
                tools.progressCount(dataFilePath, patName, hospID, invTime)

        # ---------------------------- 标题 ----------------------------------
        top_frame = tk.Frame(bigBox, bg=commonBG)
        top_frame.pack()

        tk.Label(top_frame, fg="black", bg=commonBG, font=('黑体', 12), width=60, height=2,
                 text='一分钟内说出你所知道的动物的名称，记录说出的个数（每15秒记录）').grid(row=0, column=0)
        tk.Button(top_frame, fg="white", bg='#6a8759', font=('黑体', 12), height=2, width=10,
                  text='开始计时', command=startCount).grid(row=0, column=1, padx=15)

        tk.Button(top_frame, fg="white", bg='#2b2b2b', font=('黑体', 12), height=2, width=10,
                  text='保存', command=saveCanvas).grid(row=0, column=2, padx=0)

        middleFrame = tk.Frame(bigBox, bg=commonBG)
        middleFrame.pack()

        # --------------------------------------------------- 进度条1
        fA1 = PaintingCanvas(middleFrame)
        fA1.pack(pady=0)

        scale1 = tk.Scale(middleFrame, from_=-1, to=20, orient=tk.HORIZONTAL, font=('宋体', 20), width=40, borderwidth=1,
                          activebackground='#974827', troughcolor='#cdcdcd')
        scale1.set(-1)  # 设置初始值
        scale1.pack(fill=tk.X, expand=1)

        BarStyle = ttk.Style()
        BarStyle.theme_use('classic')
        # win10环境下主题：('winnative','clam','alt','default','classic','vista','xpnative')
        # 进度条漕的宽度改变测试成功的是：'winnative','alt','default','classic'
        BarStyle.configure("my3.Horizontal.TProgressbar", troughcolor='white', background='#5ada79',
                           thickness=30)  # troughcolor 水槽色

        progressbar1 = ttk.Progressbar(middleFrame, style="my3.Horizontal.TProgressbar")
        progressbar1['maximum'] = 15  # 设置进度条最大值为100
        progressbar1['length'] = 700  # 设置进度条长度
        # progressbar['value'] = countTime

        progressbar1.pack()
        middleFrame.update()

        # --------------------------------------------------- 进度条2
        fA2 = PaintingCanvas(middleFrame)
        fA2.pack(pady=0)

        scale2 = tk.Scale(middleFrame, from_=-1, to=20, orient=tk.HORIZONTAL, font=('宋体', 20), width=40, borderwidth=1,
                          activebackground='#974827', troughcolor='#cdcdcd')
        scale2.set(-1)  # 设置初始值
        scale2.pack(fill=tk.X, expand=1)

        progressbar2 = ttk.Progressbar(middleFrame, style="my3.Horizontal.TProgressbar")
        progressbar2['maximum'] = 15  # 设置进度条最大值为100
        progressbar2['length'] = 700  # 设置进度条长度
        # progressbar['value'] = countTime

        progressbar2.pack()
        middleFrame.update()

        # --------------------------------------------------- 进度条3
        fA3 = PaintingCanvas(middleFrame)
        fA3.pack(pady=0)

        scale3 = tk.Scale(middleFrame, from_=-1, to=20, orient=tk.HORIZONTAL, font=('宋体', 20), width=40, borderwidth=1,
                          activebackground='#974827', troughcolor='#cdcdcd')
        scale3.set(-1)  # 设置初始值
        scale3.pack(fill=tk.X, expand=1)

        progressbar3 = ttk.Progressbar(middleFrame, style="my3.Horizontal.TProgressbar")
        progressbar3['maximum'] = 15  # 设置进度条最大值为100
        progressbar3['length'] = 700  # 设置进度条长度
        # progressbar['value'] = countTime

        progressbar3.pack()
        middleFrame.update()

        # --------------------------------------------------- 进度条4
        fA4 = PaintingCanvas(middleFrame)
        fA4.pack(pady=0)

        scale4 = tk.Scale(middleFrame, from_=-1, to=20, orient=tk.HORIZONTAL, font=('宋体', 20), width=40, borderwidth=1,
                          activebackground='#974827', troughcolor='#cdcdcd')
        scale4.set(-1)  # 设置初始值
        scale4.pack(fill=tk.X, expand=1)

        progressbar4 = ttk.Progressbar(middleFrame, style="my3.Horizontal.TProgressbar")
        progressbar4['maximum'] = 15  # 设置进度条最大值为100
        progressbar4['length'] = 700  # 设置进度条长度
        # progressbar['value'] = countTime

        progressbar4.pack()
        middleFrame.update()

        # ---------------------------------------------------


class PaintingCanvas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        canvasFrame = tk.Frame(self)
        canvasFrame.pack()

        # 新建画布界面
        self.canvas = tk.Canvas(canvasFrame, width=700, height=200, highlightthickness=0, bg='#f0f0f0')
        self.canvas.grid()

        # 创建一个可在 canvas 上手动绘图的效果,通过两点画线段的方式
        draw_point = ['', '']  # 用于储存拖拉鼠标时的点
        revoke = []  # 用于储存每次鼠标绘图操作的ID供撤销用[[...],[...],[...]]
        recover = []  # 用于储存每次鼠标绘图的点构成的列表供恢复
        clear = []  # 用于记录是否使用过清空，因为列表可变，支持全局修改，所以用列表记录

        def _canvas_draw(event):
            if not event:  # 松开鼠标左键时执行，清空记录点
                draw_point[:] = ['', '']  # [:]只改变draw_point指向的列表的内容，不是重新赋值一个新的列表所以修改值全局通用
                return
            point = [event.x, event.y]  # 此次传递的点坐标
            if draw_point == ['', '']:  # 按下鼠标左键开始拖动时执行
                draw_point[:] = point  # 保存拖动的第一个点
                if len(revoke) < len(recover):
                    recover[len(revoke):] = []  # 用于使用过撤销后再绘图，清除撤销点后的恢复数据
                clear[:] = []
                revoke.append([])  # 新建一个撤销记录列表
                recover.append([])  # 新建一个恢复记录列表
                recover[-1].extend(point)  # 在新建的恢复记录列表里记录第一个点
            else:
                revoke[-1].append(
                    self.canvas.create_line(draw_point[0], draw_point[1], event.x, event.y, fill="#2b2b2b", width=3,
                                            tags="line")
                )  # 绘制的线段并保存到撤销记录的末次列表
                draw_point[:] = point  # 保存拖动点，覆盖上一次
                recover[-1].extend(point)  # 保存此次传递的点坐标到恢复记录的末次列表

        self.canvas.bind("<B1-Motion>", _canvas_draw)  # 设定拖动鼠标左键画线段
        self.canvas.bind("<ButtonRelease-1>", lambda event: _canvas_draw(0))  # 设定松开鼠标左键清除保存的点

        # 清空功能
        def _canvas_clear():
            self.canvas.delete("line")  # 清除 tags = "line"的图像
            revoke[:] = []
            clear.append(1)

        # 创建一个Button对象，默认设置为居中对齐
        buttonFrame = tk.Frame(self, bg='#f0f0f0')
        self.canvas.create_window((700, 100), window=buttonFrame, anchor='e')

        btn_type = {'relief': tk.GROOVE, 'width': 2, 'height': 3, 'font': ('宋体', 12), 'bg': '#974827', 'fg': 'white'}
        btn_grid = {'padx': 5, 'pady': 2, 'sticky': 'nw'}
        tk.Button(buttonFrame, text="清\n\n空", **btn_type, command=_canvas_clear).grid(column=0, row=2, **btn_grid)


if __name__ == "__main__":
    app = App()
    app.mainloop()
