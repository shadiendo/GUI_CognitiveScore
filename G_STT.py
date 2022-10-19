#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import tkinter as tk
from tkinter import Scrollbar
import os
import numpy as np
import pandas as pd
import tools
from tools import AppSettings

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        STTFrame(self, patName, hospID,invTime).pack()


global ico_music_64


class STTFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID,invTime):
        global ico_music_64
        super().__init__(master)
        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 基础设置 ----------------------------------
        content = {'视空间/执行功能': [False, False, False, False, False],
                   "命名": [False, False, False],
                   "记忆": [False, False, False, False, False, False, False, False, False, False],
                   "注意力": [False, False, False, False, False, False],
                   "语言": [False, False, False],
                   "抽象能力": [False, False, False, False, False, False, False],
                   "定向力": [False, False, False, False, False, False],
                   }
        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 基础设置 ----------------------------------
        # 定义整个框架的大小
        container_width = 1000
        container_height = 4000
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, bg='white', width=container_width, height=container_height)
        # 创建滚动条
        scro = Scrollbar(master=self, width=50)
        scro.pack(side='right', fill='y')
        scro.config(command=CANVAS.yview)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS, bg='#94558d', width=container_width, height=container_height)
        bigBox.pack(anchor=tk.N, side='right')
        bigBox.pack_propagate(False)
        bigBox.update()
        # 进一步将三者绑定
        CANVAS.create_window((10, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 主内容 ----------------------------------
        # 实时的将修改的ADL评分传入excel
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName,hospID,invTime])

        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')        # 打开excel并把 INDEX 列设置为行索引
        STTscore = csvDf.loc[patientAnchor, 'STT评分']     # 通过行索引定位，然后输出列标签为 ADL_record 的值

        titleFrame = tk.Frame(bigBox,bg='#94558d')
        titleFrame.pack(anchor='w')
        tk.Label(titleFrame, fg='white', bg='#94558d', font=('黑体', 18), text=patName[:-1]+'★'+hospID[:-1]+'★'+invTime).pack(anchor='w')

        ffffff = True
        try:
            if np.isnan(STTscore):
                ffffff = False
        except:pass
        if ffffff:
            tk.Label(titleFrame, fg='white', bg='#94558d', font=('黑体', 18), text='该患者已进行评分！分数为：' + str(STTscore)).pack(
                anchor='w')


        MainFrame = tk.Frame(bigBox, bg='white', width=container_width, height=container_height,borderwidth =2)
        MainFrame.pack()
        MainFrame.pack_propagate(False)

        fA = tk.Frame(MainFrame, width=800, height=1000)
        fA.pack(pady = 1)

        MoCA_create(fA,patName, hospID,invTime).pack()

class MoCA_create(tk.Frame):
    def __init__(self, master,patName, hospID,invTime):
        super().__init__(master)
        global img

        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        canvasFrame = tk.Frame(self)
        canvasFrame.pack()

        # 新建画布界面
        canvas = tk.Canvas(canvasFrame, width=700, height=3650, highlightthickness=0, bg='white')
        canvas.grid()

        img = tk.PhotoImage(file=r"img\STT\STT.png")
        canvas.create_image(0, 0, anchor='nw', image=img)

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
                    canvas.create_line(draw_point[0], draw_point[1], event.x, event.y, fill="#2b2b2b", width=3,
                                       tags="line")
                )  # 绘制的线段并保存到撤销记录的末次列表
                draw_point[:] = point  # 保存拖动点，覆盖上一次
                recover[-1].extend(point)  # 保存此次传递的点坐标到恢复记录的末次列表

        canvas.bind("<B1-Motion>", _canvas_draw)  # 设定拖动鼠标左键画线段
        canvas.bind("<ButtonRelease-1>", lambda event: _canvas_draw(0))  # 设定松开鼠标左键清除保存的点

        # 添加撤销和恢复功能rev撤销，rec恢复
        def _canvas_re(rev=0, rec=0):
            if rev and revoke:  # 撤销执行
                for i in revoke.pop(-1): canvas.delete(i)  # pop弹出最后一个撤销列表，删除图像
            elif rec and recover and (len(revoke) != len(recover)):  # 恢复执行，恢复列表需要大于撤销列表
                if clear:
                    for i in recover: revoke.append([canvas.create_line(i, fill="#2b2b2b", width=3, tags="line")])
                    clear[:] = []
                else:
                    revoke.append([canvas.create_line(recover[len(revoke)], fill="#2b2b2b", width=3, tags="line")])

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

            tk.Label(main_toplevel, text="某一个窗口没填分数！", font=('黑体', 18)).place(relx=.5, rely=.4, anchor="center")
            tk.Button(main_toplevel,text ="了解了",font=('Arial', 28), command=QuitCancel, relief='flat',bg='#825471',fg='white').place(relx=.5, rely=.65,anchor="center")

            # ---------------------------- 先放黑色背景 ------------------------------------
            BC_toplevel = tk.Toplevel(self)
            BC_toplevel.attributes('-alpha', 0.5)  # 设置透明度
            BC_toplevel.overrideredirect(True)  # 取消窗口边框
            BC_toplevel.state("zoomed")  # 最大化
            BC_toplevel.attributes('-topmost', True)  # 是否置顶
            Curtain = tk.Frame(BC_toplevel, bg='black')  # 设置幕布背景为纯黑
            Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充

        # 清空功能
        def _canvas_clear():
            canvas.delete("line")  # 清除 tags = "line"的图像
            revoke[:] = []
            clear.append(1)

        # 保存功能
        def _canvas_save():
            score = [scoreEntry1.get(),scoreEntry2.get(),scoreEntry3.get(),scoreEntry4.get()]
            flagg = False
            for i in score:
                if i=='':
                    flagg = True
                    continue
            if flagg:
                warning()
            else:
                time_now = str(time.strftime('%Y-%m-%d %H.%M.%S'))  # 当前时间
                patPath = 'data\\VectorGraphic\\'+ patName+'★'+hospID+ '★'+invTime
                filename = time_now+'STT.ps'
                finalFile = os.path.join(patPath,filename)
                if not os.path.exists(patPath):
                    os.mkdir(patPath)
                canvas.postscript(file=finalFile, colormode='color')  # 扩展名可为ps或esp
                print('成功保存图片至%s' % str(finalFile))

                dataFilePath = r'data/CoreData.csv'
                patientAnchor = '★'.join([patName, hospID, invTime])
                tools.writeDataframeData(dataFilePath, patientAnchor, 'STT评分', str(score))  # 传入记录的过程
                tools.writeDataframeData(dataFilePath, patientAnchor, 'STT进度', 10)  # 传入记录的总分
                # 将总分修改并传入
                tools.progressCount(dataFilePath, patName, hospID, invTime)


        # 添加右键菜单
        menu = tk.Menu(self, tearoff=0)  # 不加 tearoff=0 的会出现可弹出选项
        menu.add_command(label="撤销", command=lambda: _canvas_re(rev=1))
        menu.add_command(label="恢复", command=lambda: _canvas_re(rec=1))
        menu.add_command(label="清空", command=_canvas_clear)
        canvas.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))  # 右键激活菜单

        # 创建一个Button对象，默认设置为居中对齐
        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        btn_type = {'relief': tk.GROOVE,'width':10, 'height':2,'font': ('宋体', 12)}
        btn_grid = {'padx': 10,'pady':5, 'sticky':'nw'}
        tk.Button(buttonFrame, text='撤销', **btn_type, command=lambda: _canvas_re(rev=1)).grid(column=0, row=0, **btn_grid)
        tk.Button(buttonFrame, text='恢复', **btn_type, command=lambda: _canvas_re(rec=1)).grid(column=1, row=0, **btn_grid)
        tk.Button(buttonFrame, text="清空", **btn_type, command=_canvas_clear).grid(column=2, row=0, **btn_grid)
        tk.Button(buttonFrame, text="保存", **btn_type, command=_canvas_save).grid(column=3, row=0, **btn_grid)

        scoreEntry1 = tk.Entry(canvas, font=('Arial', 28),bg='#c75450',fg='white',width=6)
        canvas.create_window((540, 720), window=scoreEntry1, anchor='nw')

        scoreEntry2 = tk.Entry(canvas, font=('Arial', 28),bg='#c75450',fg='white',width=6)
        canvas.create_window((540, 1690), window=scoreEntry2, anchor='nw')

        scoreEntry3 = tk.Entry(canvas, font=('Arial', 28),bg='#c75450',fg='white',width=6)
        canvas.create_window((540, 2540), window=scoreEntry3, anchor='nw')

        scoreEntry4 = tk.Entry(canvas, font=('Arial', 28),bg='#c75450',fg='white',width=6)
        canvas.create_window((540, 3590), window=scoreEntry4, anchor='nw')

if __name__ == "__main__":
    app = App()
    app.mainloop()
