#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from tools import AppSettings
from Main_Frame_C import mianFrameC
import tools


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('700x400+600+300')

        CraetNewPat(self).pack(padx=10,pady=10)


class CraetNewPat(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global img1

        '''注册功能，点击后跳出弹窗'''
        def registration(event):
            MainTopWin(self)

        mianFrame = tk.LabelFrame(self, width=260, height=150, padx=10, pady=5, text='创建一个新被试', font=('仿宋', 12),
                                  labelanchor='nw')
        mianFrame.propagate(False)  # 让窗口强制大小显示
        mianFrame.pack()

        mainCanvas = tk.Canvas(mianFrame)
        img1 = ImageTk.PhotoImage(Image.open('img/ico_newPet_128.png'))
        mainCanvas.create_image(110, 55, anchor=tk.CENTER, image=img1)
        mainCanvas.bind("<Button-1>", registration)  # 点击函数
        mainCanvas.pack()


class MainTopWin(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""

    def __init__(self, master):
        super().__init__(master)
        global infoDict, edu_level, var_titelLabel

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 子窗口界面设置 ------------------------------------
        main_toplevel = tk.Toplevel(self)
        winWidth = 500
        winHeight = 400
        screenWidth = self.winfo_screenwidth()  # 1920
        screenHeight = self.winfo_screenheight()    # 1080
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        main_toplevel.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        main_toplevel.overrideredirect(True)  # 取消窗口边框
        main_toplevel.attributes('-topmost', True)  # 为了让注册页面置顶

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 先放黑色背景 ------------------------------------
        BC_toplevel = tk.Toplevel(self)
        BC_toplevel.attributes('-alpha', 0.5)  # 设置透明度
        BC_toplevel.overrideredirect(True)  # 取消窗口边框
        BC_toplevel.state("zoomed")  # 最大化
        BC_toplevel.attributes('-topmost', True)  # 是否置顶
        Curtain = tk.Frame(BC_toplevel, bg='black')  # 设置幕布背景为纯黑
        Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 信息基础定义 ------------------------------------
        # 文件存储位置
        dataFilePath = AppSettings.dataFilePath()

        # 先创建基础，用来做一开始的匹配
        infoDict = {
            "姓名": '',
            "住院号": '',
            "病区": '',
            "床号": '',
            "文化水平": '',
            "左利手右利手": [False, False],
            "评估时间": [False, False],
            "单次手术多次手术": [False, False],
            "评估是否完成": False}

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 函数部分 ------------------------------------
        """控制开关按钮颜色,并且改变状态的函数"""
        def controlTheLight(btnName, state):
            if state == 'OPEN':
                btnName['bg'] = "green"
                btnName['fg'] = "white"
            elif state == 'CLOSE':
                btnName['bg'] = "#f0f0f0"
                btnName['fg'] = "black"

        """控制 左右利手 按钮组的值"""
        def JudgeAndSave_hand_L():
            if infoDict["左利手右利手"][0]:
                infoDict["左利手右利手"][0] = False
                controlTheLight(bt_hand_L, 'CLOSE')
                # print(infoDict)
            else:
                controlTheLight(bt_hand_L, 'OPEN')
                infoDict["左利手右利手"][0] = True
                # print(infoDict)

        def JudgeAndSave_hand_R():
            if infoDict["左利手右利手"][1]:
                infoDict["左利手右利手"][1] = False
                controlTheLight(bt_hand_R, 'CLOSE')
                # print(infoDict)
            else:
                controlTheLight(bt_hand_R, 'OPEN')
                infoDict["左利手右利手"][1] = True
                # print(infoDict)

        """控制 评估时间 按钮组的值"""
        def J_PreOp():
            if infoDict["评估时间"][0]:
                # 如果关联的另一盏灯是开的，先关了
                controlTheLight(bt_PreOpration, 'CLOSE')
                infoDict["评估时间"][0] = False
                # 再开灯
                controlTheLight(bt_PostOpration, 'OPEN')
                infoDict["评估时间"][1] = True
                # print(infoDict)
            else:
                # 如果另一盏灯是关的，先点亮
                controlTheLight(bt_PreOpration, 'OPEN')
                infoDict["评估时间"][0] = True
                # 再关自己
                controlTheLight(bt_PostOpration, 'CLOSE')
                infoDict["评估时间"][1] = False
                # print(infoDict)

        """控制 单/多次手术 按钮组的值"""
        def J_Single_Multiple_Op():
            if infoDict["单次手术多次手术"][0]:
                # 如果关联的另一盏灯是开的，先关了
                controlTheLight(bt_SingleOp, 'CLOSE')
                infoDict["单次手术多次手术"][0] = False
                # 再开灯
                controlTheLight(bt_MutiOp, 'OPEN')
                infoDict["单次手术多次手术"][1] = True
                # print(infoDict)
            else:
                # 如果另一盏灯是关的，先点亮
                controlTheLight(bt_SingleOp, 'OPEN')
                infoDict["单次手术多次手术"][0] = True
                # 再关自己
                controlTheLight(bt_MutiOp, 'CLOSE')
                infoDict["单次手术多次手术"][1] = False
                # print(infoDict)

        """最关键的函数，提交按钮，开启下一个页面，同时提交信息"""
        def submitAll():
            patName_ = infoDict["姓名"] = str(patName.get()) + '┇'
            hospID_ = infoDict["住院号"] = str(hospID.get()) + '┇'
            wardID_ = infoDict["病区"] = str(wardID.get()) + '┇'
            bedID_ = infoDict["床号"] = str(bedID.get()) + '┇'
            edu_combobox_ = infoDict["文化水平"] = edu_combobox.get()
            invTime_ = '术前' if (infoDict["评估时间"] == [True, False]) else '术后'
            SiMu_operation_ = '单次手术' if (infoDict["单次手术多次手术"] == [True, False]) else '多次手术'
            LR_hand_ = '左手' if (infoDict["左利手右利手"] == [True, False]) else '右手' if (infoDict["左利手右利手"] == [False, True]) else '左右手'

            # --------------------------------------------------------------------------------
            # 判断输入，否则不能继续
            # ①判断是否输入完整
            infoDict_K = ['姓名', '住院号', '病区', '床号', '文化水平', '左利手右利手', '评估时间', '单次手术多次手术']
            Insert_match = ['┇', '┇', '┇', '┇', '请选择文化水平', '[False, False]', '[False, False]', '[False, False]']
            for i in range(len(infoDict_K)):
                if str(infoDict[infoDict_K[i]]) == Insert_match[i]:
                    titleFrame['bg'] = '#dd001b'  # 变色警告
                    titelLabel['bg'] = '#dd001b'  # 变色警告m
                    var_titelLabel.set('您还没输入 ' + infoDict_K[i])
                    return "信息没输完"
            # ②逐一判断条件是否合适
            for cha in hospID_[:-1]:
                if cha not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    titleFrame['bg'] = '#8888c6'  # 变色警告
                    titelLabel['bg'] = '#8888c6'  # 变色警告
                    var_titelLabel.set('住院号输入不合法')
                    return "住院号输入不合法"
            # --------------------------------------------------------------------------------

            # 实时的将修改的KPS评分传入excel，并创建该人的基本条目
            patientAnchor = '★'.join([patName_, hospID_, invTime_])
            newPatIndex = tools.crateNewPatientLine(dataFilePath, patName_, hospID_, invTime_)
            if newPatIndex == '已经存在此患者':
                titleFrame['bg'] = '#1d55ae'  # 变色警告
                titelLabel['bg'] = '#1d55ae'  # 变色警告
                var_titelLabel.set('数据库中已有此患者')
                return "数据库中已有此患者"
            else:
                # 此时 newPatIndex 是一个返回值，表示新病人在第几行，是索引   并且，此时已经把 姓名、住院号、评估时间  三个参数写进去了
                # --------------------------------------------------------------------------------
                # 获取当前时间，用来添加
                createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 将其他信息写入
                tools.writeDataframeData(dataFilePath, patientAnchor, '病区', wardID_)
                tools.writeDataframeData(dataFilePath, patientAnchor, '床号', bedID_)
                tools.writeDataframeData(dataFilePath, patientAnchor, '文化水平', edu_combobox_)
                tools.writeDataframeData(dataFilePath, patientAnchor, '最初创建时间', createTime)
                tools.writeDataframeData(dataFilePath, patientAnchor, '末次修改时间', createTime)  # 初始值为最初创建时间
                tools.writeDataframeData(dataFilePath, patientAnchor, '评估是否完成', '否')
                tools.writeDataframeData(dataFilePath, patientAnchor, '完成进度', 0)
                tools.writeDataframeData(dataFilePath, patientAnchor, '左利手右利手', LR_hand_)
                tools.writeDataframeData(dataFilePath, patientAnchor, '单次手术多次手术', SiMu_operation_)

                # --------------------------------------------------------------------------------
                # 最后创建链接到新窗口
                newFrameeee = tk.Toplevel(self)
                newFrameeee.title('子窗口')
                newFrameeee.configure(bg="white")
                newFrameeee.geometry('1366x768+100+100')
                # 全屏
                newFrameeee.attributes("-fullscreen", True)
                # newWindow.wm_attributes("-topmost", 1)  # 置顶，当前GUI为普通窗口
                newFrameeee.attributes('-topmost', True)

                # 传入病人定位信息
                demoFrame_ = mianFrameC(newFrameeee, dataFilePath, newPatIndex)
                demoFrame_.pack(fill=tk.BOTH, expand=True)

                main_toplevel.destroy()
                BC_toplevel.destroy()

        # //////////////////////////////////////////////////////////////////////////
        # ---------------------------- 子主窗口内容 ------------------------------------
        def Quit_newPatFrame():
            master.destroy()

        defaultTitleBg = '#499c54'  # 默认的标题颜色
        titleFrame = tk.Frame(main_toplevel, bg=defaultTitleBg)
        titleFrame.pack(fill=tk.X)
        var_titelLabel = tk.StringVar()
        var_titelLabel.set('输入病人信息')
        titelLabel = tk.Label(titleFrame, text='输入病人信息', font=('黑体', 16), bg=defaultTitleBg, fg='#f0f0f0', width=30,
                              height=2, textvariable=var_titelLabel)
        titelLabel.pack()

        middleFrame = tk.Frame(main_toplevel)
        middleFrame.pack(padx=20, pady=10)

        # ----------------------------------------------------------------
        # 创建左侧小列框架
        leftFrame = tk.Frame(middleFrame)
        leftFrame.pack(side='left', fill=tk.Y, padx=5)

        # 通用设置
        leftFrame_label_style = {'fg': "black", 'bg': '#f0f0f0', 'font': ('黑体', 12), "width": 5, "height": 1}
        leftFrame_entry_style = {'font': ('黑体', 12), "width": 10}
        leftFrame_label_grid_style = {'sticky': 'NWWE', 'padx': 5, 'pady': 5, 'ipadx': 10, 'ipady': 7}
        leftFrame_entry_grid_style = {'sticky': 'NWWE', 'padx': 5, 'pady': 5, 'ipadx': 10, 'ipady': 7}
        # 姓名
        tk.Label(leftFrame, text='姓名', **leftFrame_label_style).grid(column=0, row=0, **leftFrame_label_grid_style)
        patName = tk.Entry(leftFrame, show='', **leftFrame_entry_style)
        patName.grid(column=1, row=0, **leftFrame_entry_grid_style)
        # 住院号
        tk.Label(leftFrame, text='住院号', **leftFrame_label_style).grid(column=0, row=1, **leftFrame_label_grid_style)
        hospID = tk.Entry(leftFrame, show='', **leftFrame_entry_style)
        hospID.grid(column=1, row=1, **leftFrame_entry_grid_style)
        # 病区
        tk.Label(leftFrame, text='病区', **leftFrame_label_style).grid(column=0, row=2, **leftFrame_label_grid_style)
        wardID = tk.Entry(leftFrame, show='', **leftFrame_entry_style)
        wardID.grid(column=1, row=2, **leftFrame_entry_grid_style)
        # 床号
        tk.Label(leftFrame, text='床号', **leftFrame_label_style).grid(column=0, row=3, **leftFrame_label_grid_style)
        bedID = tk.Entry(leftFrame, show='', **leftFrame_entry_style)
        bedID.grid(column=1, row=3, **leftFrame_entry_grid_style)

        # ----------------------------------------------------------------
        # 分割
        sep = ttk.Separator(middleFrame, orient=tk.VERTICAL, style='red.TSeparator')
        sep.pack(side='left', fill=tk.Y, padx=5)

        # ----------------------------------------------------------------
        # 创建右侧小列框架
        rightFrame = tk.Frame(middleFrame)
        rightFrame.pack(side='left', fill=tk.Y, padx=5)

        # 通用设置
        rightFrame_label_grid_style = {'sticky': 'nw', 'padx': 0, 'pady': 5, 'ipadx': 0, 'ipady': 5}
        # 选择文化
        edu_level = tk.StringVar()
        edu_level.set("请选择文化水平")

        edu_combobox = ttk.Combobox(rightFrame,
                                    textvariable=edu_level,
                                    values=["未接受教育", "小学", "初中", "高中", "大学", "更高层次"],
                                    height=10,  # 高度,下拉显示的条目数量
                                    width=20,  # 宽度
                                    font=('', 12),  # 字体
                                    state='readonly')  # 设置只读

        edu_combobox.grid(column=0, row=0, columnspan=2, **rightFrame_label_grid_style)

        # 选择利手
        bt_hand_L = tk.Button(rightFrame, text="左利手", font=('黑体', 12), relief=tk.GROOVE, width=10, height=1)
        bt_hand_L['command'] = JudgeAndSave_hand_L
        bt_hand_L.grid(column=0, row=1, **rightFrame_label_grid_style)
        bt_hand_R = tk.Button(rightFrame, text="右利手", font=('黑体', 12), relief=tk.GROOVE, width=10, height=1)
        bt_hand_R['command'] = JudgeAndSave_hand_R
        bt_hand_R.grid(column=1, row=1, **rightFrame_label_grid_style)

        # 选择术前术后
        bt_PreOpration = tk.Button(rightFrame, text="术前", font=('黑体', 12), relief=tk.GROOVE, command=J_PreOp, width=10,
                                   height=1)
        bt_PreOpration.grid(column=0, row=2, **rightFrame_label_grid_style)
        bt_PostOpration = tk.Button(rightFrame, text="术后", font=('黑体', 12), relief=tk.GROOVE, command=J_PreOp, width=10,
                                    height=1)
        bt_PostOpration.grid(column=1, row=2, **rightFrame_label_grid_style)

        # 首次入院？
        bt_SingleOp = tk.Button(rightFrame, text="初次手术", font=('黑体', 12), relief=tk.GROOVE,
                                command=J_Single_Multiple_Op, width=10, height=1)
        bt_SingleOp.grid(column=0, row=3, **rightFrame_label_grid_style)
        bt_MutiOp = tk.Button(rightFrame, text="多次手术", font=('黑体', 12), relief=tk.GROOVE, command=J_Single_Multiple_Op,
                              width=10, height=1)
        bt_MutiOp.grid(column=1, row=3, **rightFrame_label_grid_style)

        # ----------------------------------------------------------------
        # 保存、重置、取消按钮
        bottomFrame = tk.Frame(main_toplevel)
        bottomFrame.pack(padx=20, pady=10)

        leftFrame_label_style = {'fg': "black", 'bg': '#dcdad5', 'font': ('黑体', 12), "width": 15, "height": 2,
                                 'relief': tk.GROOVE}
        tk.Button(bottomFrame, text="提交", command=submitAll, **leftFrame_label_style).pack(side='left', padx=10, pady=5)
        tk.Button(bottomFrame, text="取消", command=Quit_newPatFrame, **leftFrame_label_style).pack(side='left', padx=10,
                                                                                                  pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
