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

        self.title('KPS_frame')
        self.geometry('1366x768+100+100')
        self.configure(bg="blue")

        patName = '1┇'
        hospID = '1┇'
        invTime = '术后'
        KPSFrame(self,patName,hospID,invTime).pack()


class KPSFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def __init__(self, master,patName,hospID,invTime):
        global evaluation_KPS
        super().__init__(master)
        self.patName = str(patName)
        self.hospID = str(hospID)
        self.invTime = str(invTime)

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
        # ----------------------主内容----------------------------------
        btnNameL = ['正常，无症状及体征，无疾病证据',
                    '能正常活动，但有轻微症状及体征',
                    '勉强可进行正常活动，有某些症状或体征',
                    '生活可自理，但不能维持正常生活或工作',
                    '有时需人扶助，但大多数时间可自理，不能从事正常工作',
                    '需要一定的帮助和护理，以及给子药物治疗',
                    '生活不能自理，需特别照顾及治疗',
                    '生活严重不能自理，有住院指征，尚不到病重',
                    '病重，完全失去自理能力，需住院给予积极支持治疗',
                    '病危，临近死亡',
                    '死亡'
                    ]  # 按钮文字名称
        btnValueL = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
        FlagL = [False, False, False, False,False, False, False,False, False, False, False]  # 不重复标记
        evaluation_KPS = ''
        progress = '0'

        # 实时的将修改的ADL评分传入excel
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName,hospID,invTime])

        # 将获取到的 ADL_record 输入回此处，相当于是读取既往的数据
        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')        # 打开excel并把 INDEX 列设置为行索引
        try:
            FlagL = eval(str(csvDf.loc[patientAnchor, 'KPS_record']))     # 通过行索引定位，然后输出列标签为 ADL_record 的值
        except:pass
        # print(FlagL)


        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, btnID, btn):
            global evaluation_KPS

            """事件处理函数"""
            # print('原始FlagL: '+str(FlagL))

            def turnGreen():
                """按钮变绿"""
                btn['bg'] = "green"
                btn['fg'] = highlightBG

            def turnWhite():
                """按钮变白"""
                btn['bg'] = highlightBG
                btn['fg'] = "black"

            # 记录上一步的状态，用于取消选择
            TT_FlagL = FlagL[btnID]

            # STEP1：点击时第一时间清空状态
            for i in range(len(FlagL)):  # 清空状态，满足单选
                btnNameL[i]['bg'] = highlightBG
                btnNameL[i]['fg'] = "black"
                FlagL[i] = False
            FlagL[btnID] = TT_FlagL  # 记录上一步状态的变量，用于取消选择

            # STEP2: 如果点击时该按钮是False状态，更改按钮样式，同时把标签改变成True，同时改变下标签记录值evaluation_ADL列表里的对应位置
            if not FlagL[btnID]:
                turnGreen()
                FlagL[btnID] = True
            # 如果已经是True状态了，再次点击，则更变为False
            else:
                FlagL[btnID] = False
                turnWhite()
            for i in range(len(FlagL)):
                if FlagL[i]:
                    evaluation_KPS = str(btnValueL[i])

            # 取消选择时把标记总分记0
            if TT_FlagL:
                evaluation_KPS = '0'

            # 判断进度
            if evaluation_KPS == '0':
                progress='0'
            else:
                progress = '10'


            tools.writeDataframeData(dataFilePath, patientAnchor, 'KPS_record', str(FlagL))  # 传入记录的过程
            tools.writeDataframeData(dataFilePath, patientAnchor, 'KPS评分', evaluation_KPS)  # 传入记录的总分
            tools.writeDataframeData(dataFilePath, patientAnchor, 'KPS进度', progress)  # 传入记录的总分

            # 将总分修改并传入
            tools.progressCount(dataFilePath, patName, hospID, invTime)
            # print(FlagL[btnID])
            # print(evaluation_KPS)


        # /////////////////////////////////////////////////////////////////////////////
        # ----------------------标题----------------------------------
        # 创建存放标题的frame
        title_frame = tk.Frame(bigBox, bg=commonBG)
        title_frame.pack()

        # 空行
        tk.Label(title_frame,font=('', 7), bg=commonBG).pack()
        # 内容
        tk.Label(title_frame, text='KPS评分量表',
                 fg="black", bg=commonBG,
                 font=('黑体', 18),
                 height=1).pack()
        tk.Label(title_frame,font=('', 5), bg=commonBG).pack()


        # ----------------------主内容----------------------------------

        ADL_frame = tk.Frame(bigBox, bg=commonBG)
        ADL_frame.pack()

        commonStyle_title = {'font': ('宋体', 12), 'fg': "black", 'width':56, 'bg': commonBG}
        commonStyle_content = {'font': ('宋体', 12), 'fg': "black", 'width':11}

        # 先写第一行


        for i in range(len(btnNameL)):
            # 写第一列
            btnNameL[i] = tk.Label(ADL_frame,text=btnNameL[i],**commonStyle_title, anchor='w', justify='left')
            btnNameL[i].grid(column=0, row=i + 1,pady = 5,ipadx = 2,ipady = 10)
            # 写第二列
            btnNameL[i] = tk.Label(ADL_frame,text=btnValueL[i],**commonStyle_content,bg=highlightBG)
            btnNameL[i].bind("<Button-1>", handlerAdaptor(handler,btnID=i,btn=btnNameL[i]))
            btnNameL[i].grid(column=1, row=i + 1,pady = 2,ipadx = 5,ipady = 10)

            # 读取存储在csv中的状态，反应在按钮中
            if FlagL[i]:
                btnNameL[i]['bg'] = "green"
                btnNameL[i]['fg'] = highlightBG

        tk.Label(ADL_frame,text='临 床 症 状',font= ('黑体', 15),bg=commonBG).grid(column=0, row=50,sticky='w')
        tk.Label(ADL_frame,text='得 分',font= ('黑体', 15),bg=commonBG).grid(column=1, row=50,sticky='n')

if __name__ == "__main__":
    app = App()
    app.mainloop()
