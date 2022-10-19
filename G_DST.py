#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tools
import pandas as pd
from tools import AppSettings
from tkinter import Scrollbar


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        DSTFrame(self, patName, hospID,invTime).pack()


global ico_music_64,MMSE_64


class DSTFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID,invTime):
        global ico_music_64,MMSE_64
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
        container_height = 750
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, bg=CANVAS_bg, width=container_width, height=container_height)
        # 创建滚动条
        scro = Scrollbar(master=self, width=70)
        scro.pack(side='right', fill='y')
        scro.config(command=CANVAS.yview)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS, bg=div0_bg, width=container_width, height=container_height)
        bigBox.pack(anchor=tk.N, side='right')
        bigBox.pack_propagate(0)
        bigBox.update()
        # 进一步将三者绑定
        CANVAS.create_window((10, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()
        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 标题 ----------------------------------
        # 标题frame
        title_frame = tk.Frame(bigBox, bg=commonBG)
        title_frame.pack()

        # 空行
        tk.Label(title_frame,font=('', 7), bg=commonBG).pack()

        tk.Label(title_frame, fg="black", bg=commonBG, font=('黑体', 18), width=60, height=2,
                 text='数字广度测试（DST）').pack()

        # /////////////////////////////////////////////////////////////////////////////
        fMiddle = tk.Frame(bigBox,width = 1000,height=900, bg=commonBG)
        fMiddle.pack_propagate(0)
        fMiddle.pack()

        fA = tk.Frame(fMiddle, width=800, height=250)
        fA.pack(pady = 1)
        fA1 = DST_create(fA, patName, hospID,invTime)
        fA1.pack()




class DST_create(tk.Frame):
    def __init__(self, master, patName, hospID,invTime):
        super().__init__(master)
        global DST_800px

        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        canvasFrame = tk.Frame(self)
        canvasFrame.pack()

        # 新建画布界面
        canvas = tk.Canvas(canvasFrame, width=825, height=580, highlightthickness=0, bg='white')
        canvas.grid()

        DST_800px = tk.PhotoImage(file=r"img\DST\DST_800px.png")
        canvas.create_image(0, 0, anchor='nw', image=DST_800px)

        content = {'判断': [False, False, False, False, False, False, False, False, False,        # 左边
                          False, False, False, False, False, False, False, False, False, False, False, False],  # 右边
                   '值':[2,3,4,5,6,7,7,8,8,                                                                                      # 左边
                          2,2,3,3,4,4,5,5,6,6,7,7],                                                                             # 右边
                   '坐标':[(9, 55),(9, 123),(9, 190),(9, 257),(9, 324),(9, 391),(9, 424),(9, 458),(9, 492),                       # 左边
                           (432, 123),(432, 156),(432, 190),(432, 223),(432, 257),(432, 290),(432, 324),(432, 358),(432, 391),(432, 424),(432, 458), (432, 492)]}   # 右边

        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName, hospID,invTime])
        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')  # 打开excel并把 INDEX 列设置为行索引

        try:
            content = eval(str(csvDf.loc[patientAnchor, 'DST_record']))  # 通过行索引定位，然后输出列标签为 ADL_record 的值
            # print('成功读取')
            # print(content)
        except:
            pass
            # print('没有检测到数据')


        label2Green = {'bg': 'green', 'fg': 'white'}
        label2White = {'bg': '#f2f2f2', 'fg': 'black'}

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event,myVar,cnt):
            """事件处理函数"""
            # print(content['值'][cnt])

            def turnGreen():
                """按钮变绿"""
                myVar.config(**label2Green)
                content['判断'][cnt] = True

            def turnWhite():
                """按钮变白"""
                myVar.config(**label2White)
                content['判断'][cnt] = False

            # 如果点击时该按钮是False状态，更改按钮状态，再次点击，再更改
            if not content['判断'][cnt]:
                turnGreen()
            else:
                turnWhite()

            # print(content)

            scoreL_list = []
            scoreR_list = []

            for i in range(len(content['判断'])):
                if i<9:
                    if content['判断'][i]:
                        scoreL_list.append(content['值'][i])
                else:
                    if content['判断'][i]:
                        scoreR_list.append(content['值'][i])

            # 计算记录的总分
            if len(scoreL_list)!=0:
                scoreL=max(scoreL_list)
            else:
                scoreL=0

            if len(scoreR_list)!=0:
                scoreR=max(scoreR_list)
            else:
                scoreR=0

            evaluation_DST= [scoreL,scoreR]

            # print(evaluation_DST)

            # 计算进度
            progress = 0
            if scoreL!=0:
                progress+=5
            if scoreR != 0:
                progress += 5

            # 实时的将修改的ADL评分传入excel
            tools.writeDataframeData(dataFilePath, patientAnchor, 'DST评分', str(evaluation_DST))  # 传入记录的总分
            tools.writeDataframeData(dataFilePath, patientAnchor, 'DST_record', str(content))  # 传入记录的过程
            tools.writeDataframeData(dataFilePath, patientAnchor, 'DST进度', progress)  # 传入记录的总分

            # 将总分修改并传入
            tools.progressCount(dataFilePath, patName, hospID, invTime)


        createVar = locals()
        myVarList = []

        btn_style = {"width": 10,'relief':tk.GROOVE}
        # 写左边
        for i in range(len(content['判断'])):
            bvn = 'btnVar' + str(i)         # bvn : btnVarName : label按钮变量的名称
            text2btn = str(content['值'][i])
            x = content['坐标'][i][0]
            y = content['坐标'][i][1]
            btnHeight=1
            if i < 5:
                btnHeight = 3
            createVar[bvn] = tk.Button(canvas, text=text2btn, height=btnHeight,**btn_style)
            # 判断是否要变绿
            if content['判断'][i]:
                createVar[bvn].config(**label2Green)
            else:
                createVar[bvn].config(**label2White)
            myVarList.append(createVar[bvn])
            canvas.create_window((x, y), window=createVar[bvn], anchor='nw')
            createVar[bvn].bind("<Button-1>", handlerAdaptor(handler,myVar = createVar[bvn],cnt=i))



if __name__ == "__main__":
    app = App()
    app.mainloop()
