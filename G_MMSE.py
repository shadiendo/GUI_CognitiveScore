#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
from tools import AppSettings
import tools
import pandas as pd
from tkinter import Scrollbar
import os
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1366x768+100+100')

        patName = '1┇'
        hospID = '1┇'
        invTime = '术前'
        MMSEFrame(self, patName, hospID, invTime).pack()


global ico_music_64, MMSE_64


class MMSEFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID, invTime):
        global ico_music_64, MMSE_64
        super().__init__(master)
        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        # /////////////////////////////////////////////////////////////////////////////
        content = [['（1）', '现在是哪一年？', False, False,
                    '（2）', '现在是什么季节？', False, False,
                    '（3）', '现在是几月份？', False, False,
                    '（4）', '今天是几号？', False, False,
                    '（5）', '今天是星期几？', False, False,
                    '（6）', '这是什么城市', False, False,
                    '（7）', '这是什么区或县', False, False,
                    '（8）', '这是什么街道或乡', False, False,
                    '（9）', '这是第几层楼？', False, False,
                    '（10）', '这是什么地方？', False, False],
                   ['（1）', '回答出“皮球”', False, False,
                    '（1）', '回答出“国旗”', False, False,
                    '（1）', '回答出“树木”', False, False],
                   ['（1）', '100-7 = 93', False, False,
                    '（1）', ' 93-7 = 86', False, False,
                    '（1）', ' 86-7 = 79', False, False,
                    '（1）', ' 79-7 = 72', False, False,
                    '（1）', ' 72-7 = 65s', False, False],
                   ['（1）', '回答出“皮球”', False, False,
                    '（1）', '回答出“国旗”', False, False,
                    '（1）', '回答出“树木”', False, False],
                   ['（1）', '回答出“手表” （回答出“表”就算对）', False, False,
                    '（1）', '回答出“铅笔” （回答出“笔”就算对）', False, False],
                   ['（1）', '说出“大家齐心协力把绳子拉紧”', False, False],
                   ['（1）', '请闭上您的眼睛', False, False],
                   ['（1）', '患者右手拿起纸', False, False,
                    '（1）', '患者将纸对折', False, False,
                    '（1）', '患者将纸放在左腿上', False, False],
                   ['（1）', '表达正确', False, False],
                   ['（1）', '绘图正确', False, False],
                   ]
        # ---------------------------- part0 函数部分 ----------------------------------
        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName, hospID, invTime])
        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')  # 打开excel并把 INDEX 列设置为行索引

        try:
            content = eval(str(csvDf.loc[patientAnchor, 'MMSE_record']))  # 通过行索引定位，然后输出列标签为 ADL_record 的值
            # print('成功读取')
        except:
            pass
            # print('没有检测到数据')

        def handlerAdaptor(fun, **kwds):
            """事件处理函数的适配器，相当于中介，进行事件绑定，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def handler(event, myVarList, item, cnt):
            """事件处理函数"""
            # print(content[item])

            # 更改按钮状态
            def turnGreen():
                """按钮变绿"""
                myVarList[cnt].config(**label2Green)
                content[item][cnt] = True

            def turnWhite():
                """按钮变白"""
                myVarList[cnt].config(**label2White)
                content[item][cnt] = False

            # 第一步:先将自己和隔壁按钮变白
            myVarList[cnt].config(**label2White)
            c = cnt % 4  # 计算应该排布在哪一列
            if c == 3:
                myVarList[cnt - 1].config(**label2White)
                content[item][cnt - 1] = False
            else:
                myVarList[cnt + 1].config(**label2White)
                content[item][cnt + 1] = False

            # 如果点击时该按钮是False状态，更改按钮状态，再次点击，再更改
            if not content[item][cnt]:
                turnGreen()
            else:
                turnWhite()

            # 计算评分
            evaluation_MMSE = 0
            for i in range(len(content)):
                for j in range(len(content[i])):
                    if str(content[i][j]) == 'True':
                        evaluation_MMSE += 1
            # print(evaluation_MMSE)

            progress = evaluation_MMSE / 3
            # 实时的将修改的ADL评分传入excel
            tools.writeDataframeData(dataFilePath, patientAnchor, 'MMSE_record', str(content))  # 传入记录的过程
            tools.writeDataframeData(dataFilePath, patientAnchor, 'MMSE评分', evaluation_MMSE)  # 传入记录的总分
            tools.writeDataframeData(dataFilePath, patientAnchor, 'MMSE进度', progress)  # 传入记录的总分

            # 将总分修改并传入
            tools.progressCount(dataFilePath, patName, hospID, invTime)

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 基础设置 ----------------------------------
        CANVAS_bg = 'white'
        div0_bg = 'white'
        commonBG = 'white'
        highlightBG = '#f2f2f2'
        # 设置窗口长宽
        container_width = 1015
        container_height = 2500
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
        # ---------------------------- 文字和变量的基础设置 ----------------------------------
        commonFontStyle = {'font': ('宋体', 12), 'fg': "black", 'bg': commonBG}
        label2LEFT = {'anchor': 'w', 'justify': 'left'}
        label2Green = {'bg': 'green', 'fg': highlightBG}
        label2White = {'bg': highlightBG, 'fg': 'black'}

        createVar = locals()
        myVarList = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 标题 ----------------------------------
        # 标题frame
        title_frame = tk.Frame(bigBox, bg=commonBG)
        title_frame.pack()

        # 空行
        tk.Label(title_frame, font=('', 7), bg=commonBG).pack()
        tk.Label(title_frame, fg="black", bg=commonBG, font=('黑体', 18), width=60, height=2,
                 text='简易精神状态评价量表（MMSE）').pack()

        Qstem = ['1. 定向力：现在我要问您一些问题，多数都很简单，请您认真回答',
                 '2. 即刻记忆：现在我告诉您三种东西的名称，我说完后请您重复一遍\n  （回答出的词语正确即可，顺序不要求）',
                 '3. 注意力和计算力：现在请您算一算，从100中减去7，然后从所得的\n   数算下去，请您将每减一个7后的答案告诉我，直到我说“停”为止\n  【依次减5次，减对几次给几分，如果前面减错，不影响后面评分】',
                 '4. 回忆：现在请您说出刚才我让您记住的是哪三种东西？\n  （回答出的词语正确即可，顺序不要求）',
                 '5. 命名：请问这是什么？',
                 '6. 重复：请您跟我说',
                 '7. 阅读：请您念一念这句话，并按这句话的意思去做（如患者为文盲，该项评为0分）',
                 '8. 三步指令：我给您一张纸，请您按我说的去做。\n   ①用右手拿着这张纸\n   ②用两只手把它对折起来\n   ③放在您的左腿上',
                 '9. 表达：请您写一个完整的句子\n  （句子要有主语、谓语，能表达一定的意思, 如患者为文育，该项评为0分）',
                 '10.请您照着这个样子把它画下来'
                 ]

        # # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- part2 ----------------------------------

        def AAA(Qid):
            frame_Qid = tk.Frame(bigBox, bg=commonBG)
            frame_Qid.pack(anchor=tk.N)

            tk.Label(frame_Qid, font=('', 5), bg=commonBG).pack()  # 空行
            tk.Label(frame_Qid, **commonFontStyle, **label2LEFT, width=80,
                     text=Qstem[Qid]).pack(anchor=tk.N)

            frame_Qid_A = tk.Frame(frame_Qid, bg=commonBG)
            frame_Qid_A.pack()

            for cnt in range(len(content[Qid])):
                part = Qid
                r = cnt // 4  # 计算应该排布在哪一行
                c = cnt % 4  # 计算应该排布在哪一列
                # 创建所有的label
                bvn = 'btnVar' + str(part) + str(r) + str(c)  # bvn : btnVarName : label按钮变量的名称
                text2Label = str(content[part][cnt])
                if c == 2:
                    text2Label = '错'
                if c == 3:
                    text2Label = '对'
                createVar[bvn] = tk.Label(frame_Qid_A, text=text2Label, **commonFontStyle, )
                myVarPart = myVarList[str(part)]
                myVarPart.append(createVar[bvn])

                # 设置第一行的样式
                if c == 0:
                    myVarPart[cnt].config(padx=1, pady=1, width=5, **label2LEFT)
                    myVarPart[cnt].grid(row=r, column=c, padx=1, pady=1)
                elif c == 1:
                    myVarPart[cnt].config(padx=1, pady=1, width=40, **label2LEFT)
                    myVarPart[cnt].grid(row=r, column=c, padx=1, pady=1)
                else:
                    if content[part][cnt]:
                        myVarPart[cnt].config(**label2Green, width=10)
                    else:
                        myVarPart[cnt].config(**label2White, padx=1, pady=1, width=10)
                    myVarPart[cnt].grid(row=r, column=c, padx=1)
                    myVarPart[cnt].bind("<Button-1>", handlerAdaptor(handler, myVarList=myVarPart, item=part, cnt=cnt))

        for i in range(10):
            AAA(i)

        # /////////////////////////////////////////////////////////////////////////////
        frame_part_10_B = tk.Frame(bigBox, bg=commonBG)
        frame_part_10_B.pack()

        canvas_part_10_B = tk.Canvas(frame_part_10_B, height=300, width=300, bg=commonBG)
        # 自带的PhotoImage只能使用gif图片
        MMSE_64 = tk.PhotoImage(file=r"img\MMSE_64.png")
        # 0,0 -> 锚定的点, anchor='nw' -> 左上角锚定
        canvas_part_10_B.create_image(0, 0, anchor='nw', image=MMSE_64)
        canvas_part_10_B.pack()

        frame_part_10_C = tk.Frame(bigBox, bg=commonBG)
        frame_part_10_C.pack()
        HandPaintedCanvas(frame_part_10_C, patName, hospID, invTime).pack()


class HandPaintedCanvas(tk.Frame):
    def __init__(self, master, patName, hospID, invTime):
        super().__init__(master)

        self.patName = patName
        self.hospID = hospID
        self.invTime = invTime

        dataFilePath = AppSettings.dataFilePath()
        patientAnchor = '★'.join([patName, hospID, invTime])
        csvDf = pd.read_csv(dataFilePath).set_index('INDEX')  # 打开excel并把 INDEX 列设置为行索引

        ffflag = csvDf.loc[patientAnchor, 'MMSE进度']  # 通过行索引定位，然后输出列标签为 ADL_record 的值

        tk.Label(self, font=('黑体', 18), text='该患者似乎没有图').pack(anchor='w')
        if ffflag==10:
            try:
                picPath = 'data\\VectorGraphic\\' + patName + '★' + hospID+ '★'+ invTime
                # os.listdir()方法获取文件夹名字，返回数组
                file_name_list = os.listdir(picPath)

                for fName in file_name_list:
                    if fName[-7:] =='MMSE.ps':
                        tk.Label(self, fg='white', bg='#a04127', font=('黑体', 18), text='该患者已画过图').pack(
                            anchor='w')
                        continue
            except:pass

        canvasFrame = tk.Frame(self)
        canvasFrame.pack()

        # 新建画布界面
        canvas = tk.Canvas(canvasFrame, width=500, height=500, highlightthickness=0, bg='#f2f2f2')
        canvas.grid()

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

        # 清空功能
        def _canvas_clear():
            canvas.delete("line")  # 清除 tags = "line"的图像
            revoke[:] = []
            clear.append(1)

        def _canvas_save():
            time_now = str(time.strftime('%Y-%m-%d %H.%M.%S'))  # 当前时间
            patPath = 'data\\VectorGraphic\\' + patName + '★' + hospID+ '★'+invTime
            filename = time_now+'MMSE.ps'
            finalFile = os.path.join(patPath, filename)
            if not os.path.exists(patPath):
                os.mkdir(patPath)
            canvas.postscript(file=finalFile, colormode='color')  # 扩展名可为ps或esp
            print('成功保存图片至%s' % str(finalFile))


        # 添加右键菜单
        menu = tk.Menu(self, tearoff=0)  # 不加 tearoff=0 的会出现可弹出选项
        menu.add_command(label="撤销", command=lambda: _canvas_re(rev=1))
        menu.add_command(label="恢复", command=lambda: _canvas_re(rec=1))
        menu.add_command(label="清空", command=_canvas_clear)
        canvas.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))  # 右键激活菜单



        # 创建一个Button对象，默认设置为居中对齐
        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        btn_type = {'relief': tk.GROOVE, 'width': 10, 'height': 2, 'font': ('宋体', 12)}
        btn_grid = {'padx': 10, 'pady': 5, 'sticky': 'nw'}
        tk.Button(buttonFrame, text='撤销', **btn_type, command=lambda: _canvas_re(rev=1)).grid(column=0, row=0,**btn_grid)
        tk.Button(buttonFrame, text='恢复', **btn_type, command=lambda: _canvas_re(rec=1)).grid(column=1, row=0,**btn_grid)
        tk.Button(buttonFrame, text="清空", **btn_type, command=_canvas_clear).grid(column=2, row=0, **btn_grid)
        tk.Button(buttonFrame, text="保存", **btn_type, command=_canvas_save).grid(column=3, row=0, **btn_grid)


if __name__ == "__main__":
    app = App()
    app.mainloop()
