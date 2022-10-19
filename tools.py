#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import time
import tkinter as tk
import pandas as pd
import numpy as np


class AppSettings(object):
    dataPath = r'data/CoreData.csv'
    frameBTitle = '欢迎来到病人选择界面！'

    def __init__(self, frameBTitle):
        self.frameBTitle = frameBTitle

    @staticmethod
    def dataFilePath():
        return AppSettings.dataPath


class FullScreenApp(object):
    """用于使用快捷键进行 窗口的全屏 相关处理"""

    def __init__(self, master, **kwargs):
        self.root = master
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"


def enumerate_lookup(list, lookup):
    """
    list: 要被查找的列表
    lookup：要被查找的元素
    enumerate函数：获取每个元素的索引和值
    :return:打印每个元素的索引和值

    例： list = ['Mike', 'male', 'male', '24']
        lookup = 'male'
        print(enumerate_lookup(list,'male'))
    输出：[1, 2]

    """
    ret = []
    for index, value in enumerate(list):
        if value == lookup:
            ret.append(index)
    return ret


def crateNewPatientLine(dataFilePath, patName, hospID, invTime):
    """
    :param dataFilePath: csv文件位置
    :param patName: 要传输的患者姓名
    :param hospID: 要传输的患者住院号
    :param invTime: 要传输的患者术前术后状态
    :return: 功能
        将患者姓名、住院号信息写入，并创建patientAnchor
        返回在第几行
    """
    if not os.path.exists(dataFilePath):
        print('目标路径 data 文件夹下没有数据文件，新建')
        new_df = pd.DataFrame(columns=['INDEX',
                                       '姓名', '住院号', '病区', '床号',
                                       '评估时间', '文化水平', '左利手右利手', '单次手术多次手术',
                                       '最初创建时间', '末次修改时间', '完成时间', '评估是否完成', '完成进度',
                                       'KPS_record', 'KPS评分', 'KPS进度',
                                       'ADL_record', 'ADL评分', 'ADL进度',
                                       'RAVLT_record', 'RAVLT评分', 'RAVLT进度',
                                       'MMSE_record', 'MMSE评分', 'MMSE进度',
                                       'DST_record', 'DST评分', 'DST进度',
                                       'MOCA_record', 'MOCA评分', 'MOCA进度',
                                       'STT_record', 'STT评分', 'STT进度',
                                       'VFT_record', 'VFT评分', 'VFT进度'])
        new_df.to_csv(dataFilePath, index=False, encoding='utf_8_sig')  # index参数指要不要行索引

    df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引
    patientAnchor = '★'.join([patName, hospID, invTime])

    # 使用新输入的个人信息作为索引，查询旧表内是否已经存在，返回一个列表
    judgeExist = enumerate_lookup(list(df.index), patientAnchor)

    # 如果找不到，那就说明输入的是新的，新建一行即可，返回新建行的行索引
    if len(judgeExist) == 0:
        df.loc[patientAnchor, '姓名'] = patName  # 列表内第一个参数 找到行索引，第二个参数 列标签
        df.loc[patientAnchor, '住院号'] = hospID  # 列表内第一个参数 找到行索引，第二个参数 列标签
        df.loc[patientAnchor, '评估时间'] = invTime  # 列表内第一个参数 找到行索引，第二个参数 列标签

        df.to_csv(dataFilePath, index=True, encoding='utf_8_sig')  # index参数指要不要行索引
        newPatIndex = len(list(df.index)) - 1
        print('已新建一患者')
        return newPatIndex
    else:
        return '已经存在此患者'

    # print('\n', df, '\n')


def writeDataframeData(dataFilePath, patientAnchor, key, value):
    """
    :param dataFilePath: csv文件位置
    :param patientAnchor: 是一个字符串，用于搜索行索引，如果找不到，就新建一个
    :param key: 数据新增在哪一个标签上
    :param value: 要新增的数据
    :return: 功能
        如传入参数
        dataFilePath = r'data/rettttttttttttttttt.csv'
        patientAnchorList = ['刘芸芸','000000']
        patientAnchor = '★'.join(patientAnchorList)
        key = 'KPS评分'
        value = 70
    """
    if not os.path.exists(dataFilePath):
        print('目标路径 data 文件夹下没有数据文件，新建')
        new_df = pd.DataFrame(
            columns=['INDEX', '姓名', '住院号', '病区', '床号', '文化水平', '左利手右利手', '术前术后', '单次手术多次手术', 'KPS_record', 'KPS评分',
                     'ADL评分'])
        new_df.to_csv(dataFilePath, index=False, encoding='utf_8_sig')  # index参数指要不要行索引

    df = pd.read_csv(dataFilePath).set_index('INDEX')  # 把【INDEX】列标签作为行的索引
    # print(df,'\n')
    df.loc[patientAnchor, key] = value  # 列表内第一个参数 找到行索引，第二个参数 列标签
    # print(df, '\n')

    df.to_csv(dataFilePath, index=True, encoding='utf_8_sig')  # index参数指要不要行索引
    # print('\n', df, '\n')


def progressCount(dataFilePath, patName, hospID, invTime):
    patientAnchor = '★'.join([patName, hospID, invTime])
    print(patientAnchor)
    df = pd.read_csv(dataFilePath).set_index('INDEX')  # 打开excel并把 INDEX 列设置为行索引

    patName_ = df.loc[patientAnchor, '姓名']
    hospID_ = df.loc[patientAnchor, '住院号']
    wardID_ = df.loc[patientAnchor, '病区']
    bedID_ = df.loc[patientAnchor, '床号']
    culture_ = df.loc[patientAnchor, '文化水平']
    LRhand_ = df.loc[patientAnchor, '左利手右利手']

    invTime_ = df.loc[patientAnchor, '评估时间']

    barValue1 = df.loc[patientAnchor, 'ADL进度']
    barValue2 = df.loc[patientAnchor, 'DST进度']
    barValue3 = df.loc[patientAnchor, 'KPS进度']
    barValue4 = df.loc[patientAnchor, 'MMSE进度']
    barValue5 = df.loc[patientAnchor, 'MOCA进度']
    barValue6 = df.loc[patientAnchor, 'RAVLT进度']
    barValue7 = df.loc[patientAnchor, 'STT进度']
    barValue8 = df.loc[patientAnchor, 'VFT进度']

    if np.isnan(barValue1):
        barValue1 = 0
    if np.isnan(barValue2):
        barValue2 = 0
    if np.isnan(barValue3):
        barValue3 = 0
    if np.isnan(barValue4):
        barValue4 = 0
    if np.isnan(barValue5):
        barValue5 = 0
    if np.isnan(barValue6):
        barValue6 = 0
    if np.isnan(barValue7):
        barValue7 = 0
    if np.isnan(barValue8):
        barValue8 = 0

    titalScore = int(barValue1 + barValue2 + barValue3 + barValue4 + barValue5 + barValue6 + barValue7 + barValue8)
    df.loc[patientAnchor, '完成进度'] = titalScore  # 列表内第一个参数 找到行索引，第二个参数 列标签

    if titalScore != 80:
        df.loc[patientAnchor, '评估是否完成'] = '否'
        df.loc[patientAnchor, '完成时间'] = ''
        print('目前总分：%d分（满分80）' % titalScore)

    else:
        currentTime = str(time.strftime('%Y-%m-%d %H:%M:%S'))
        if invTime_ == '术前':
            # 将原来的行修改内容
            df.loc[patientAnchor, '评估是否完成'] = '是'
            df.loc[patientAnchor, '完成时间'] = currentTime

            NewAnchor = '★'.join([patName_, hospID_, '术后'])

            df.loc[NewAnchor, '姓名'] = patName_
            df.loc[NewAnchor, '住院号'] = hospID_
            df.loc[NewAnchor, '病区'] = wardID_
            df.loc[NewAnchor, '床号'] = bedID_
            df.loc[NewAnchor, '最初创建时间'] = currentTime
            df.loc[NewAnchor, '修改时间'] = currentTime
            df.loc[NewAnchor, '评估时间'] = '术后'
            df.loc[NewAnchor, '文化水平'] = culture_
            df.loc[NewAnchor, '左利手右利手'] = LRhand_
            df.loc[NewAnchor, '评估是否完成'] = '否'

            print('恭喜！已满分%d，完成全部评估，同时已创建该病人术后数据条目' % titalScore)

        # 如果已经是术后的了，那么只需要改一下完成状态即可
        if invTime_ == '术后':
            df.loc[patientAnchor, '评估是否完成'] = '是'
            df.loc[patientAnchor, '完成时间'] = currentTime


    df.to_csv(dataFilePath, index=True, encoding='utf_8_sig')


def ifContentChange():
    AppSettings('AA')
    print(AppSettings.frameBTitle)