#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tools
import pandas as pd
from tkinter import Scrollbar
from tools import AppSettings

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        ADLFrame(self, patName, hospID, invTime).pack()


class ADLFrame(tk.Frame):
    def __init__(self, master,patName,hospID,invTime):
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
        # 获得父级窗口的尺寸，但是如果是打开本文件，那么父级窗口的长宽会为1，所以做个判断
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
        bigBox.pack_propagate(False)
        bigBox.update()
        # 进一步将三者绑定
        CANVAS.create_window((10, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 标题 ----------------------------------
        # 创建存放标题的frame
        title_frame = tk.Frame(bigBox, bg=commonBG)
        title_frame.pack()

        # 标题
        tk.Label(title_frame,font=('', 7),bg=commonBG).pack()
        tk.Label(title_frame,bg=commonBG,font=('黑体', 18),text='ADL评分量表').pack()
        tk.Label(title_frame,font=('', 5),bg=commonBG).pack()

        # /////////////////////////////////////////////////////////////////////////////
        # 创建存放按钮表格的frame
        ADL_frame = tk.Frame(bigBox, bg=commonBG)

        # ----------------------第一行----------------------------------
        row1_name = ['日常活动项目','独立','部分独立或需要部分帮助',"需极大帮助","完全依赖"]
        for i in range(len(row1_name)):
            # 定义文字样式
            commonStyle = {'font': ('宋体', 12), 'fg': "black", 'justify': tk.CENTER, 'height': 1, 'padx': 1, 'pady': 10,
                           'wraplength': 100, 'bg': commonBG}
            if i == 0:
                tk.Label(ADL_frame, text=row1_name[i], width=35, **commonStyle).grid(column=i, row=0)
            else:
                tk.Label(ADL_frame, text=row1_name[i], width=18, **commonStyle).grid(column=i, row=0)

        # ----------------------第一列----------------------------------
        col1_name = ['洗澡',
                     '进餐',
                     '修饰 (洗脸/刷牙/刮脸/梳头)',
                     "穿衣 (包括系鞋带等)",
                     "可控制大便",
                     "可控制小便",
                     "用厕 (擦净/整理衣裤/冲水)",
                     "床椅转移",
                     "平地行走45米",
                     "上下楼梯"
                     ]
        for i in range(len(col1_name)):
            tk.Label(ADL_frame, text=col1_name[i],
                     font=('宋体', 12), fg="black",anchor='w',
                     justify=tk.LEFT, height=3,
                     padx=1, pady=1,
                     bg=commonBG).grid(column=0, row=i + 1)

        # ----------------------按钮列表----------------------------------
        btnNameL = [['10', '5', '0', '0'],
                    ['5', '0', '0', '0'],
                    ['5', '0', '0', '0'],
                    ['10', '5', '0', '0'],
                    ['10', '5(每周＜1次失控)', '0(已失控)', '0'],
                    ['10', '5(每24h＜1次失控)', '0(已失控)', '0'],
                    ['10', '5', '0', '0'],
                    ['15', '10', '0', '0'],
                    ['15', '10', '0', '0'],
                    ['10', '5', '0', '0'],
                    ]  # 按钮文字名称
        btnValueL = [[10, 5, 0, 0],
                     [5, 0, 0, 0],
                     [5, 0, 0, 0],
                     [10, 5, 0, 0],
                     [10, 5, 0, 0],
                     [10, 5, 0, 0],
                     [10, 5, 0, 0],
                     [15, 10, 0, 0],
                     [15, 10, 0, 0],
                     [10, 5, 0, 0],
                     ]  # 按钮文字名称
        FlagL = [[False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 [False, False, False, False],
                 ]  # 不重复标记
        evaluation_ADL = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0]

        #######################################################
        # 实时的将修改的ADL评分传入excel
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName,hospID,invTime])

        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')        # 打开excel并把 INDEX 列设置为行索引
        ADL_record = str(csvDf.loc[patientAnchor, 'ADL_record'])     # 通过行索引定位，然后输出列标签为 ADL_record 的值

        # 将获取到的 ADL_record 输入回此处，相当于是读取既往的数据

        try:
            FlagL = eval(ADL_record)
            # print(FlagL)
            for i in range(len(FlagL)):
                for j in range(4):
                    if FlagL[i][j]:
                        evaluation_ADL[i] = btnValueL[i][j]
        except:pass

        # //////////////////////////////
        # print(FlagL)
        # //////////////////////////////

        #######################################################

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, rID, cID, btn):
            """事件处理函数"""

            def turnGreen():
                """按钮变绿"""
                btn['bg'] = "green"
                btn['fg'] = highlightBG

            def turnWhite():
                """按钮变白"""
                btn['bg'] = highlightBG
                btn['fg'] = "black"

            # 记录上一步的状态，用于取消选择
            TT_FlagL = FlagL[rID][cID]

            # STEP1：点击时第一时间清空状态
            for i in range(4):  # 清空状态，满足单选
                btnNameL[rID][i]['bg'] = highlightBG
                btnNameL[rID][i]['fg'] = "black"
                FlagL[rID] = [False, False, False, False]
                turnWhite()
                FlagL[rID][cID] = TT_FlagL  # 记录上一步状态的变量，用于取消选择

            # STEP2: 如果点击时该按钮是False状态，更改按钮样式，同时把标签改变成True，同时改变下标签记录值evaluation_ADL列表里的对应位置
            if not FlagL[rID][cID]:
                turnGreen()
                FlagL[rID][cID] = True
                evaluation_ADL[rID] = btnValueL[rID][cID]
            # 如果已经是True状态了，再次点击，则更变为False
            else:
                FlagL[rID][cID] = False
                turnWhite()
                evaluation_ADL[rID] = 0

            # print(FlagL[rID][cID])

            # 计算结果
            score_count = sum(evaluation_ADL)
            ADLsum.set('总分：' + str(score_count))  # 为label设置值

            # print(evaluation_ADL)

            #######################################################
            # 实时的将修改的ADL评分传入excel
            tools.writeDataframeData(dataFilePath, patientAnchor, 'ADL_record', str(FlagL))  # 传入记录的过程
            tools.writeDataframeData(dataFilePath, patientAnchor, 'ADL评分', str(score_count))  # 传入记录的总分
            # 判断进度
            progress=0
            for i in FlagL:
                for j in i:
                    if j:
                        progress+=1
            tools.writeDataframeData(dataFilePath, patientAnchor, 'ADL进度', progress)  # 传入记录的总分

            # 将总分修改并传入
            tools.progressCount(dataFilePath, patName, hospID, invTime)

            #######################################################

        # -----------------按钮的10行--------------------------------------------------------------------
        for rID in range(len(btnNameL)):
            for cID in range(len(btnNameL[rID])):
                btnNameL[rID][cID] = tk.Label(ADL_frame,
                                              text=btnNameL[rID][cID],
                                              font=('宋体', 12), fg="black",
                                              justify=tk.LEFT, width=18, height=3,
                                              padx=0, pady=0,
                                              bg=highlightBG)
                btnNameL[rID][cID].bind("<Button-1>", handlerAdaptor(handler,
                                                                     rID=rID,
                                                                     cID=cID,
                                                                     btn=btnNameL[rID][cID]))
                btnNameL[rID][cID].grid(column=cID + 1, row=rID + 1)

                # 读取存储在csv中的状态，反应在按钮中
                if FlagL[rID][cID]:
                    btnNameL[rID][cID]['bg'] = "green"
                    btnNameL[rID][cID]['fg'] = highlightBG

        # # -----------------按钮最后一行的设计--------------------------------------------------------------------
        ADLsum = tk.StringVar()
        ADLsum.set('总分：' + str(sum(evaluation_ADL)))  # 为label设置值

        sumBtn = tk.Label(ADL_frame, textvariable=ADLsum,
                          font=('宋体', 12),
                          fg="black",
                          justify=tk.LEFT, width=18, height=3,
                          padx=0, pady=0,
                          bg=commonBG)
        sumBtn.grid(column=4, row=11, columnspan=10)

        ADL_frame.pack()

        # /////////////////////////////////////////////////////////////////////////////
        # ----------------------------- 最终设置相关 -----------------------------




if __name__ == "__main__":
    app = App()
    app.mainloop()
