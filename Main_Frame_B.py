#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
import tkinter as tk
from Main_Frame_B_newPat import CraetNewPat
from Main_Frame_B_newPatNotFinished import newPatNotFinished
from Main_Frame_B_oldPat import showOldPat
import pandas as pd
import tools
from tools import AppSettings

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('1366x768+100+100')
        self.configure(bg="black")
        # self.attributes("-topmost", 1)

        mianFrameB(self).pack(fill=tk.BOTH, expand=True)


class mianFrameB(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        global img_ico_close_48,ico_reset_32,img_ico_home_48,firstContainer_,secondContainer_,thirdContainer_

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------顶条--------------------------------------
        def back2home():
            # self.quit()
            self.destroy()
            self.master.destroy()

        def refreshFrameB():
            global firstContainer_, secondContainer_, thirdContainer_

            firstContainer_.destroy()
            firstContainer_ = firstContainer(FRAME_1)  # 第一个容器，新病人容器
            firstContainer_.pack(side='top')

            secondContainer_.destroy()
            secondContainer_ = secondContainer(FRAME_2)  # 第二个容器，老病人容器
            secondContainer_.pack(side='top')

            thirdContainer_.destroy()
            thirdContainer_ = thirdContainer(FRAME_3,B_finishedPat_canvas_width,B_finishedPat_canvas_height)
            thirdContainer_.pack()

        def rootQuitFrame():
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


            def QuitFrame():
                self.quit()
                # self.destroy()
                # self.master.destroy()
            def QuitCancel():
                # self.quit()
                main_toplevel.destroy()
                BC_toplevel.destroy()
                # self.master.destroy()

            tk.Label(main_toplevel, text="是否要退出软件", font=('黑体', 20)).place(relx=.5, rely=.4, anchor="center")
            tk.Button(main_toplevel,text ="退出",font=('Arial', 28), command=QuitFrame, relief='flat',bg='#825471',fg='white').place(relx=.3, rely=.65,anchor="center")
            tk.Button(main_toplevel,text ="取消",font=('Arial', 28), command=QuitCancel, relief='flat',bg='#825471',fg='white').place(relx=.7, rely=.65,anchor="center")

            # ---------------------------- 先放黑色背景 ------------------------------------
            BC_toplevel = tk.Toplevel(self)
            BC_toplevel.attributes('-alpha', 0.5)  # 设置透明度
            BC_toplevel.overrideredirect(True)  # 取消窗口边框
            BC_toplevel.state("zoomed")  # 最大化
            BC_toplevel.attributes('-topmost', True)  # 是否置顶
            Curtain = tk.Frame(BC_toplevel, bg='black')  # 设置幕布背景为纯黑
            Curtain.pack(fill=tk.BOTH, expand=True)  # 完全填充

        titleBG = '#2b2b2b'
        frameBTitle = AppSettings.frameBTitle
        # ////////////////////////////////////////////////////////
        # 创建框架和画布
        FRAME_TOP = tk.Frame(self,bg=titleBG,bd=3)

        FRAME_111 = tk.Frame(FRAME_TOP,bg=titleBG)
        FRAME_111.place(relx=.50, rely=.5, anchor="center")
        tk.Label(FRAME_111,fg = 'white',text = frameBTitle,bg =titleBG,font=('黑体', 28)).pack()

        # 设置按钮
        top = tk.Frame(FRAME_TOP)
        top.pack(side='right')
        ico_reset_32 = ImageTk.PhotoImage(Image.open('img/ico_refresh_i_64.png'))
        img_ico_close_48 = ImageTk.PhotoImage(Image.open('img/ico_close_i_64.png'))
        img_ico_home_48 = ImageTk.PhotoImage(Image.open('img/ico_home_i_64.png'))
        tk.Button(top, image=img_ico_home_48, command=back2home,relief='flat',bd=1).grid(row=0, column=0, sticky='nw') # 刷新
        tk.Button(top, image=ico_reset_32, command=refreshFrameB,relief='flat',bd=1).grid(row=0, column=1, sticky='nw') # 刷新
        tk.Button(top, image=img_ico_close_48, command=rootQuitFrame,relief='flat',bd=1).grid(row=0, column=2, sticky='nw') # 关闭

        # 放置
        FRAME_TOP.pack(fill=tk.X)  # 放置第二级

        # 假阴影
        FRAME_222 = tk.Frame(self,bg='grey',height=3)
        FRAME_222.pack(fill=tk.X)  # 放置第二级
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        FRAME_Reast = tk.Frame(self)
        FRAME_Reast.pack(side='left', anchor=tk.NW,fill=tk.BOTH, expand=True)

        # ///////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------左左半部分--------------------------------------
        Frame_LLeft = tk.Frame(FRAME_Reast)
        tk.LabelFrame(Frame_LLeft,padx=20).grid(row=0, column=0, sticky='nw', padx=10, pady=5, ipadx=0, ipady=0)
        Frame_LLeft.pack(side='left')

        # --------------------------------------左半部分--------------------------------------
        Frame_Left = tk.Frame(FRAME_Reast)
        Frame_Left.pack(side='left')

        # 左半部分 上
        FRAME_1 = tk.LabelFrame(Frame_Left,padx=10, pady=5,text=' 术前待采集病人列表',font=('仿宋', 15, 'bold'), labelanchor='nw')
        FRAME_1.grid(row=0, column=0, sticky='nw', padx=0, pady=5, ipadx=0, ipady=0)
        firstContainer_ = firstContainer(FRAME_1)       # 第一个容器，新病人容器
        firstContainer_.pack(side='top')

        # 左半部分 下
        FRAME_2 = tk.LabelFrame(Frame_Left,padx=10, pady=5,text=' 术后待二次采集',font=('仿宋', 15, 'bold'),labelanchor='nw')
        FRAME_2.grid(row=1, column=0, sticky='nw', padx=0, pady=5, ipadx=0, ipady=0)
        secondContainer_ = secondContainer(FRAME_2)        # 第二个容器，老病人容器
        secondContainer_.pack(side='top')

        # ///////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------右半部分--------------------------------------
        Frame_right = tk.Frame(FRAME_Reast)
        Frame_right.pack(side='left')

        FRAME_3 = tk.LabelFrame(Frame_right,padx=0, pady=20,text=' 已采集完毕病人列表',font=('仿宋', 15, 'bold'),labelanchor='nw')
        B_finishedPat_canvas_width = 380
        B_finishedPat_canvas_height = 590
        thirdContainer_ = thirdContainer(FRAME_3,B_finishedPat_canvas_width,B_finishedPat_canvas_height)
        thirdContainer_.pack()

        FRAME_3.grid(row=0, column=1, sticky='ne',rowspan = 10, padx=20, ipadx=0, ipady=0)


class firstContainer(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # ---------------------- 基础设置 ----------------------------------
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, width=840, height=160)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS)

        # ###########################################################
        CraetNewPat(bigBox).grid(row=0, column=0, sticky='nw',pady=10,padx=10)

        # 先读取文件，查看有多少要创建的
        dataFilePath = AppSettings.dataFilePath()
        df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引

        # 先获取所有属于术前评估的索引，然后看这个人是不是已经完成
        shuqianpinggu = tools.enumerate_lookup(list(df['评估时间']), '术前')  # 获取索引
        wanchengzhuangtai = tools.enumerate_lookup(list(df['评估是否完成']),'否')     # 获取索引
        print(shuqianpinggu)

        IdTo1stContainer=[]
        for i in shuqianpinggu:
            if i in wanchengzhuangtai:
                IdTo1stContainer.append(i)

        for i in IdTo1stContainer:
            newPatNotFinished(bigBox,i).grid(row=0, column=i+1, sticky='nw',pady=10,padx=10)


        ########################## 最终设置相关 #############################
        bigBox.pack()
        bigBox.update()

        scro = tk.Scrollbar(master=self, width=40,orient="horizontal")
        scro.pack(side='bottom', fill='x')
        scro.config(command=CANVAS.xview)

        CANVAS.create_window((0, 0), window=bigBox, anchor="nw")
        CANVAS.configure(xscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()


class secondContainer(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        # ---------------------- 基础设置 ----------------------------------
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, bg='#f0f0f0', width=840, height=330)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS)

        # ###########################################################
        # 先读取文件，查看有多少要创建的
        dataFilePath = r'data/CoreData.csv'
        df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引
        # 先获取所有属于术前评估的索引，然后看这个人是不是已经完成
        shuqianpinggu = tools.enumerate_lookup(list(df['评估时间']), '术后')  # 获取索引
        wanchengzhuangtai = tools.enumerate_lookup(list(df['评估是否完成']),'否')     # 获取索引
        IdTo2ndContainer=[]
        for i in shuqianpinggu:
            if i in wanchengzhuangtai:
                IdTo2ndContainer.append(i)

        for i in range(len(IdTo2ndContainer)):
            r = i % 2     # 取余数，比如 5 % 2 = 1
            c = i // 2    # 地板除，比如 5//2 = 2
            showOldPat(bigBox,IdTo2ndContainer[i]).grid(row=r, column=c, sticky='nw',pady=10,padx=10)

        ########################## 最终设置相关 #############################
        bigBox.pack()
        bigBox.update()

        scro = tk.Scrollbar(master=self, width=40,orient="horizontal")
        scro.pack(side='bottom', fill='x')
        scro.config(command=CANVAS.xview)

        CANVAS.create_window((0, 0), window=bigBox, anchor="nw")
        CANVAS.configure(xscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()


class thirdContainer(tk.Frame):

    def __init__(self, master,canvas_width,canvas_height):
        super().__init__(master)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # ---------------------- 基础设置 ----------------------------------
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self,width=canvas_width,height=canvas_height)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS)

        # ###########################################################
        # 中间设置
        label_options = {'fg': "black", 'bg': '#f0f0f0', 'font': ("黑体", 14),'height':1,'anchor':"w"}

        # 先读取文件，查看有多少要创建的
        dataFilePath = r'data/CoreData.csv'
        df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引
        # 先获取所有属于术前评估的索引，然后看这个人是不是已经完成
        IdTo3rdContainer = tools.enumerate_lookup(list(df['评估是否完成']),'是')     # 获取索引

        for rowIndex in IdTo3rdContainer:
            patName_ = df.iloc[rowIndex, list(df.columns).index('姓名')]
            hospID_ = df.iloc[rowIndex, list(df.columns).index('住院号')]
            invTime_ = df.iloc[rowIndex, list(df.columns).index('评估时间')]
            finishedTime_ = df.iloc[rowIndex, list(df.columns).index('完成时间')]
            text = str(finishedTime_)+"  "+str(invTime_)+'：'+str(patName_)+str(hospID_)+str(rowIndex)+"  "
            tk.Label(bigBox,text=text,**label_options).pack(anchor=tk.NW,side='top',padx=10, pady=5)

        ########################## 最终设置相关 #############################
        bigBox.pack()
        bigBox.update()

        scro = tk.Scrollbar(master=self, width=50)
        scro.pack(side='right', fill='y')
        scro.config(command=CANVAS.yview)

        CANVAS.create_window((0, 0), window=bigBox, anchor="nw")
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()
if __name__ == "__main__":
    app = App()
    app.mainloop()