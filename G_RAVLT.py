#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tools
import pandas as pd
from tkinter import Scrollbar
from PIL import Image, ImageTk
import winsound
from tools import AppSettings

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        RAVLTFrame(self, patName, hospID,invTime).pack()


global ico_music_48,ico_musicStop_32,cnt,ico_reset_32,myVarList

class RAVLTFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID,invTime):
        global ico_music_48,ico_musicStop_32,ico_reset_32,myVarList
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
        # ---------------------------- 标题 ---------------------------------
        title_frame = tk.Frame(bigBox, bg=commonBG,height = 60)
        title_frame.pack(fill=tk.X)

        button_L_frame = tk.Frame(title_frame, bg='red')
        button_L_frame.place(relx=.04, rely=.5, anchor="w")

        ico_music_48 = ImageTk.PhotoImage(Image.open('img/ico_music_48.png'))
        ico_musicStop_32 = ImageTk.PhotoImage(Image.open('img/ico_musicStop_32.png'))
        ico_reset_32 = ImageTk.PhotoImage(Image.open('img/ico_reset_32.png'))

        def playAudio1():
            winsound.PlaySound(r".\audio\REVAL_词语A.wav", winsound.SND_ASYNC)
        tk.Button(button_L_frame,
                  text='词语A',
                  image=ico_music_48,
                  compound=tk.LEFT,
                  padx=8, pady=0,
                  relief=tk.GROOVE,
                  command = playAudio1).pack(side = 'left')

        def playAudio2():
            winsound.PlaySound(r".\audio\REVAL_词语B.wav", winsound.SND_ASYNC)
        tk.Button(button_L_frame,
                  text='词语B',
                  image=ico_music_48,
                  compound=tk.LEFT,
                  padx=8, pady=0,
                  relief=tk.GROOVE,
                  command = playAudio2).pack(side = 'left')

        def stopAudio():
            winsound.PlaySound(None, winsound.SND_NODEFAULT)
        tk.Button(button_L_frame,
                  text=' 停止',
                  image=ico_musicStop_32,
                  compound=tk.LEFT,
                  padx = 8,pady = 8,
                  relief=tk.GROOVE,
                  command = stopAudio).pack(side = 'left')

        button_M_frame = tk.Frame(title_frame)
        button_M_frame.place(relx = .5, rely = .5,anchor='center')
        tk.Label(button_M_frame, fg="black", bg=commonBG, font=('黑体', 18), height=2,
                 text='RAVLT评分量表').pack()

        def resetAllSelection():
            pass
            # for i in range(len(content)):
            #     r = i // 11  # 计算应该排布在哪一行
            #     c = i % 11  # 计算应该排布在哪一列
            #     if r !=0 and c!= 0 and c!=6:
            #         myVarList[i].config(bg="white")
            #         content[i] = False
            #         tools.writeDataframeData(dataFilePath, patientAnchor, 'RAVLT_record', str(content))

        button_R_frame = tk.Frame(title_frame)
        button_R_frame.place(relx = .96, rely = .5,anchor='e')
        tk.Button(button_R_frame,
                  text=' 重置一切',
                  image=ico_reset_32,
                  compound=tk.LEFT,
                  padx = 8,pady = 8,
                  relief=tk.GROOVE,
                  command = resetAllSelection).pack(side = 'left')


        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 主内容 ----------------------------------

        content = ['词语A', 'A1', 'A2', 'A3', 'A4', 'A5', '词语B', 'B1', 'A6', 'A7', '回忆词A',
                   '锣鼓', False, False, False, False, False, '桌子', False, False, False, False,
                   '窗帘', False, False, False, False, False, '骑警', False, False, False, False,
                   '时钟', False, False, False, False, False, '小鸟', False, False, False, False,
                   '咖啡', False, False, False, False, False, '鞋子', False, False, False, False,
                   '学校', False, False, False, False, False, '火炉', False, False, False, False,
                   '父亲', False, False, False, False, False, '高山', False, False, False, False,
                   '月亮', False, False, False, False, False, '眼镜', False, False, False, False,
                   '公园', False, False, False, False, False, '毛巾', False, False, False, False,
                   '帽子', False, False, False, False, False, '白云', False, False, False, False,
                   '农夫', False, False, False, False, False, '轮船', False, False, False, False,
                   '鼻子', False, False, False, False, False, '羔羊', False, False, False, False,
                   '火鸡', False, False, False, False, False, '手枪', False, False, False, False,
                   '颜色', False, False, False, False, False, '铅笔', False, False, False, False,
                   '房子', False, False, False, False, False, '教堂', False, False, False, False,
                   '河流', False, False, False, False, False, '第一', False, False, False, False,
                   ]

        # 实时的将修改的ADL评分传入excel
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName,hospID,invTime])

        # 将获取到的 ADL_record 输入回此处，相当于是读取既往的数据
        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')        # 打开excel并把 INDEX 列设置为行索引

        try:
            content = eval(str(csvDf.loc[patientAnchor, 'RAVLT_record']))     # 通过行索引定位，然后输出列标签为 ADL_record 的值
        except:
            pass
            # print('没有检测到数据')
        # print(content)

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event,cnt):
            """事件处理函数"""
            # print(content)
            # print(content[cnt])

            # 更改按钮状态
            def turnGreen():
                """按钮变绿"""
                myVarList[cnt].config(bg="green")
                content[cnt] = True
            def turnWhite():
                """按钮变白"""
                myVarList[cnt].config(bg="#f2f2f2")
                content[cnt] = False

            # 如果点击时该按钮是False状态，更改按钮状态，再次点击，再更改
            if not content[cnt]:
                turnGreen()
            else:
                turnWhite()


            # 计算评分
            evaluation_RAVLT = [0 for i in range(9)]
            Srecord = [1,2,3,4,5,7,8,9,10]      # 记录哪几列
            for i in range(len(content)):
                c = i % 11
                for j in range(len(Srecord)):
                    if c==Srecord[j] and str(content[i])=='True':
                        evaluation_RAVLT[j]+=1
            # print(evaluation_RAVLT)

            # 计算进度
            pAll = 0
            for i in evaluation_RAVLT:
                if i != 0:
                    pAll +=1
            progress=(pAll/len(evaluation_RAVLT))*10

            # 将内容写入
            tools.writeDataframeData(dataFilePath, patientAnchor, 'RAVLT_record', str(content))  # 传入记录的过程
            tools.writeDataframeData(dataFilePath, patientAnchor, 'RAVLT评分', str(evaluation_RAVLT))  # 传入记录的总分
            tools.writeDataframeData(dataFilePath, patientAnchor, 'RAVLT进度', str(progress))  # 传入记录的总分
            # 将总分修改并传入
            tools.progressCount(dataFilePath, patName, hospID, invTime)

            # print(content)

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 主内容 ----------------------------------
        middle_frame = tk.Frame(bigBox, bg=commonBG)
        middle_frame.pack()
        commonStyle = {'font': ('宋体', 12), 'fg': "black", 'justify': tk.CENTER,'width': 10, 'height': 2}

        createVar = locals()
        myVarList = []  # 存放自己创建的变量
        for cnt in range(len(content)):

            r = cnt // 11       # 计算应该排布在哪一行
            c = cnt % 11        # 计算应该排布在哪一列

            # 创建所有的label
            bvn = 'btnVar' + str(r) + str(c)  # bvn : btnVarName : label按钮变量的名称
            text2Label = str(content[cnt])
            if text2Label == 'False' or text2Label == 'True':
                text2Label = ''
            createVar[bvn] = tk.Label(middle_frame, text=text2Label,**commonStyle)
            myVarList.append(createVar[bvn])

            # 设置第一行的样式
            if r ==0:
                myVarList[cnt].config(bg=commonBG)
                myVarList[cnt].grid(row=r, column=c,padx= 1, pady= 1)
            elif c==0:
                myVarList[cnt].config(bg=commonBG,padx= 1, pady= 1)
                myVarList[cnt].grid(row=r, column=c,padx= 1, pady= 1)
            elif c==6:
                myVarList[cnt].config(bg=commonBG)
                myVarList[cnt].grid(row=r, column=c,padx= 1, pady= 1)
            else:
                if content[cnt]:
                    myVarList[cnt].config(bg="green")
                else:
                    myVarList[cnt].config(bg=highlightBG)
                myVarList[cnt].grid(row=r, column=c)
                myVarList[cnt].bind("<Button-1>", handlerAdaptor(handler, cnt=cnt))



if __name__ == "__main__":
    app = App()
    app.mainloop()
