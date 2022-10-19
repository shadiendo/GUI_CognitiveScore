#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Scrollbar
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from G_KPS import KPSFrame
from G_ADL import ADLFrame
from G_RAVLT import RAVLTFrame
from G_MMSE import MMSEFrame
from G_MOCA import MoCAFrame
from G_DST import DSTFrame
from G_STT import STTFrame
from G_VFT import VFTFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('KPS_frame')
        self.geometry('1366x768+100+100')
        # self.overrideredirect(True)  # 取消窗口边框
        # self.attributes("-fullscreen", True)

        # self.attributes("-topmost", 1)
        self.configure(bg="black")

        dataFilePath = r'data/CoreData.csv'
        PatIndex = 0
        mianFrameC(self,dataFilePath,PatIndex).pack(fill=tk.BOTH, expand=True)


class mianFrameC(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 KPSFrame(self).pack() 这么来显示"""


    def __init__(self, master,dataFilePath,PatIndex):
        super().__init__(master)

        global img_ico_close_48, FRAME_3_kpsFrame, FRAME_3_adlFrame, FRAME_3_ravltFrame, FRAME_3_mmseFrame, MMSE_64, FRAME_3_mocaFrame, FRAME_3_dstFrame, FRAME_3_sttFrame, FRAME_3_vftFrame

        df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引

        self.dataFilePath = dataFilePath
        self.newPatIndex = PatIndex
        # self.master.wm_attributes("-topmost", 1)

        patName = df.iloc[PatIndex,list(df.columns).index('姓名')]
        hospID = df.iloc[PatIndex, list(df.columns).index('住院号')]
        invTime = df.iloc[PatIndex, list(df.columns).index('评估时间')]

        # 改变标题颜色的小玩意
        titleBG = '#2b2b2b'
        if invTime=='术后':
            titleBG = '#c75450'

        # ////////////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------顶条--------------------------------------
        def rootQuitFrame_C():
            # self.quit()
            self.destroy()
            self.master.destroy()

        # ////////////////////////////////////////////////////////
        # 创建框架和画布
        FRAME_1 = tk.Frame(self,bg=titleBG,height=64,bd=3)


        # 病人信息
        FRAME_Pat = tk.Frame(FRAME_1,bg=titleBG)
        FRAME_Pat.place(relx=.01, rely=.5, anchor="w")

        tk.Label(FRAME_Pat,fg = 'white',bg =titleBG,font=('黑体', 28),text=str(invTime)).grid(column=0, row=0, sticky='w',padx=10)

        FRAME_Pat_R = tk.Frame(FRAME_Pat,bg=titleBG)
        FRAME_Pat_R.grid(column=1, row=0, sticky='w')
        tk.Label(FRAME_Pat_R,fg = 'white',bg =titleBG,font=('黑体', 18),text='姓  名：'+patName[:-1]).pack(anchor= 'w')
        tk.Label(FRAME_Pat_R,fg = 'white',bg =titleBG,font=('黑体', 13),text='住 院 号： '+hospID[:-1]).pack(anchor= 'w')

        # 标题
        FRAME_111 = tk.Frame(FRAME_1,bg=titleBG)
        FRAME_111.place(relx=.53, rely=.5, anchor="center")
        tk.Label(FRAME_111,fg = 'white',bg =titleBG,font=('黑体', 18),text='江  苏  省  人  民  医  院').pack()
        tk.Label(FRAME_111,fg = 'white',bg =titleBG,font=('黑体', 13),text='南 京 医 科 大 学 第 一 附 属 医 院').pack()

        # 设置按钮
        img_ico_close_48 = ImageTk.PhotoImage(Image.open('img/ico_返回_i_64.png'))
        tk.Button(FRAME_1, image=img_ico_close_48, command=rootQuitFrame_C,relief='flat',bd=1).pack(side='right')

        FRAME_1.pack(fill=tk.X)  # 放置第二级

        # 假阴影
        FRAME_222 = tk.Frame(self,bg='grey',height=3)
        FRAME_222.pack(fill=tk.X)  # 放置第二级
        # ////////////////////////////////////////////////////////////////////////////////////////
        # --------------------------------------左侧选单--------------------------------------
        # 创建框架和画布
        FRAME_2 = tk.Frame(self, bg='#3c3f41', padx=15, pady=5)
        FRAME_2.pack(side=tk.LEFT, fill=tk.Y)

        # 设置参数 创建按钮
        btn_style = {'fg': "white", 'bg': '#499c54', 'font': ('黑体', 13), "width": 20, "height": 2,'relief':tk.GROOVE}
        grid_options = {'column': 0, 'padx': 10, 'pady': 10, 'ipadx': 20, 'ipady': 5}

        Button_KPS = tk.Button(FRAME_2, text='KPS\nKarnofsky功能状态评分', **btn_style)
        Button_KPS.grid(row=0, **grid_options)
        Button_KPS.bind('<Button-1>',lambda e:switch('KPS',Button_KPS))        #左键切换为橙色界面

        Button_ADL = tk.Button(FRAME_2, text='ADL\n日常生活活动评分', **btn_style)
        Button_ADL.grid(row=1, **grid_options)
        Button_ADL.bind('<Button-1>',lambda e:switch('ADL',Button_ADL))       #右键切换为蓝色界面

        Button_RAVLT = tk.Button(FRAME_2, text='RAVLT\n听觉语言学习测验', **btn_style)
        Button_RAVLT.grid(row=2, **grid_options)
        Button_RAVLT.bind('<Button-1>',lambda e:switch('RAVLT',Button_RAVLT))       #右键切换为蓝色界面

        Button_MMSE = tk.Button(FRAME_2, text='MMSE\n简易精神状态评价量表', **btn_style)
        Button_MMSE.grid(row=3, **grid_options)
        Button_MMSE.bind('<Button-1>',lambda e:switch('MMSE',Button_MMSE))       #右键切换为蓝色界面

        Button_MoCA = tk.Button(FRAME_2, text='MoCA\n蒙特利尔认知评估量表', **btn_style)
        Button_MoCA.grid(row=4, **grid_options)
        Button_MoCA.bind('<Button-1>',lambda e:switch('MoCA',Button_MoCA))       #右键切换为蓝色界面

        Button_DST = tk.Button(FRAME_2, text='DST\n数字广度测验', **btn_style)
        Button_DST.grid(row=5, **grid_options)
        Button_DST.bind('<Button-1>',lambda e:switch('DST',Button_DST))       #右键切换为蓝色界面

        Button_VFT = tk.Button(FRAME_2, text='VFT\n语言流畅性测试', **btn_style)
        Button_VFT.grid(row=6, **grid_options)
        Button_VFT.bind('<Button-1>',lambda e:switch('VFT',Button_VFT))       #右键切换为蓝色界面

        Button_STT = tk.Button(FRAME_2, text='STT\n形状连线测验', **btn_style)
        Button_STT.grid(row=7, **grid_options)
        Button_STT.bind('<Button-1>',lambda e:switch('STT',Button_STT),)       #右键切换为蓝色界面

        # 放置


        # ////////////////////////////////////////////////////////////////////////////////////////
        # # --------------------------------------中间组件--------------------------------------
        FRAME_3 = tk.Frame(self,bg='white')
        FRAME_3.pack(side=tk.RIGHT)

        ttttttFrame = TTTTTTFrame(FRAME_3, patName, hospID)
        ttttttFrame.pack(side = tk.LEFT)


        FRAME_3_kpsFrame = KPSFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_adlFrame = ADLFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_ravltFrame = RAVLTFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_mmseFrame = MMSEFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_mocaFrame = MMSEFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_dstFrame = DSTFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_vftFrame = VFTFrame(FRAME_3, patName, hospID,invTime)
        FRAME_3_sttFrame = STTFrame(FRAME_3, patName, hospID,invTime)




        def switch(selection,btn):
            btn.config(state=tk.ACTIVE)
            global img_ico_close_48, FRAME_3_kpsFrame, FRAME_3_adlFrame, FRAME_3_ravltFrame, FRAME_3_mmseFrame, MMSE_64, FRAME_3_mocaFrame, FRAME_3_dstFrame,FRAME_3_sttFrame,FRAME_3_vftFrame
            FRAME_3_kpsFrame.destroy()
            FRAME_3_adlFrame.destroy()
            FRAME_3_ravltFrame.destroy()
            FRAME_3_mmseFrame.destroy()
            FRAME_3_mocaFrame.destroy()
            FRAME_3_dstFrame.destroy()
            FRAME_3_sttFrame.destroy()
            FRAME_3_vftFrame.destroy()
            ttttttFrame.destroy()
            if selection=='KPS':
                FRAME_3_kpsFrame = KPSFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_kpsFrame.pack()
            if selection=='ADL':
                FRAME_3_adlFrame = ADLFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_adlFrame.pack()
            if selection=='RAVLT':
                FRAME_3_ravltFrame = RAVLTFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_ravltFrame.pack()
            if selection=='MMSE':
                FRAME_3_mmseFrame = MMSEFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_mmseFrame.pack()
            if selection=='MoCA':
                FRAME_3_mocaFrame = MoCAFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_mocaFrame.pack()
            if selection=='DST':
                FRAME_3_dstFrame = DSTFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_dstFrame.pack()
            if selection == 'VFT':
                FRAME_3_vftFrame = VFTFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_vftFrame.pack()
            if selection=='STT':
                FRAME_3_sttFrame = STTFrame(FRAME_3, patName, hospID,invTime)
                FRAME_3_sttFrame.pack()


class TTTTTTFrame(tk.Frame):
    """这是一个 tk.Frame 对象，可以比如 ADLFrame(self).pack() 这么来显示"""

    def __init__(self, master, patName, hospID):
        global ico_music_64,MMSE_64
        super().__init__(master)
        self.patName = patName
        self.hospID = hospID

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 基础设置 ----------------------------------
        # 定义整个框架的大小
        container_width = 1000
        container_height = 2500
        # 创建画布，此处一定一定要加长宽，因为默认大小是380*270左右
        CANVAS = tk.Canvas(master=self, bg='#678d85', width=container_width, height=container_height)
        # 创建滚动条
        scro = Scrollbar(master=self, width=50)
        scro.pack(side='right', fill='y')
        scro.config(command=CANVAS.yview)
        # 创建画布上存放东西的框架，后续将该frame与画布绑定
        bigBox = tk.Frame(CANVAS, bg='#f0f0f0', width=container_width, height=container_height)
        bigBox.pack(anchor=tk.N)
        bigBox.pack_propagate(0)
        bigBox.update()
        # 进一步将三者绑定
        CANVAS.create_window((10, 0), window=bigBox, anchor=tk.N)  # anchor=tk.N 决定了把东西放上面，可以换成W看看
        CANVAS.configure(yscrollcommand=scro.set, scrollregion=CANVAS.bbox("all"))
        CANVAS.pack()

        # /////////////////////////////////////////////////////////////////////////////
        # ---------------------------- 标题 ----------------------------------
        # 标题frame
        title_frame = tk.Frame(bigBox, bg='#f0f0f0')
        title_frame.pack()

        # 空行
        tk.Label(title_frame, text='', font=('', 1)).pack()
        tk.Label(title_frame, fg="black", bg='#f0f0f0', font=('黑体', 70), width=60, height=1,
                 text='歓迎いたします！').pack()

        # 内容行
        middle_frame = tk.Frame(bigBox, bg='#f0f0f0')
        middle_frame.pack(anchor=tk.NW)

        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 13), width=60, height=1,anchor= 'w', justify='left',
                 text='←左をクリックして開始').grid(column=0, row=0, sticky='w')
        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 15), width=200, height=3,anchor= 'w', justify='left',
                 text='① 该系统用于采集患者认知功能，共使用了8种评分量表，以全面评估脑肿瘤，尤其是脑胶质瘤患者术前术后\n'+
                      '   的认知功能改变。').grid(column=0, row=1, sticky='w')
        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 15), width=200, height=3,anchor= 'w', justify='left',
                 text='② 使用时如果页面上有 保存 按钮，记得按一下，如果没有保存按钮，那么填写数据时会自动保存至本地数\n'+
                      '   据库中，路径为 data→CoreData.csv。'
                      ).grid(column=0, row=2, sticky='w')
        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 15), width=200, height=3,anchor= 'w', justify='left',
                 text='③ 评分量表中有涉及图像保存的，存储路径为 data→VectorGraphic 由于tkinter的canvas模块只能保存格\n'+
                      '   式为ps或eps的矢量图，建议有事没事就去检查一下数据，删除不需要的。'
                      ).grid(column=0, row=3, sticky='w')
        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 15), width=200, height=2,anchor= 'w', justify='left',
                 text='④ 开发单位为江苏省人民医院神经外科，本软件不设账号，可拷贝至本地使用。').grid(column=0, row=4, sticky='w')
        tk.Label(middle_frame, fg="black", bg='#f0f0f0', font=('黑体', 15), width=200, height=2,anchor= 'w', justify='left',
                 text='⑤ bug反馈，请联系作者vanshaw@126.com').grid(column=0, row=5, sticky='w')

if __name__ == "__main__":
    app = App()
    app.mainloop()