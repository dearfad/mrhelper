#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: wos.py
# Usage: Web of Science DataFile Process Module


import os


class WosData:
    def __init__(self):
        # Predefine Field
        # Web of Science DataFile Class
        # http://images.webofknowledge.com/WOKRS5272R3/help/zh_CN/WOK/hs_wos_fieldtags.html
        self.FN = ''  # 文件名
        self.VR = ''  # 版本号
        self.PT = ''  # 出版物类型（J=期刊；B=书籍；S=丛书；P=专利）
        self.AU = []  # 作者
        self.AF = []  # 作者全名
        self.BA = ''  # 书籍作者
        self.BF = ''  # 书籍作者全名
        self.CA = ''  # 团体作者
        self.GP = ''  # 书籍团体作者
        self.BE = ''  # 编者
        self.TI = ''  # 文献标题
        self.SO = ''  # 出版物名称
        self.SE = ''  # 丛书标题
        self.BS = ''  # 丛书副标题
        self.LA = ''  # 语种
        self.DT = ''  # 文献类型
        self.CT = ''  # 会议标题
        self.CY = ''  # 会议日期
        self.CL = ''  # 会议地点
        self.SP = ''  # 会议赞助方
        self.HO = ''  # 会议主办方
        self.DE = []  # 作者关键词
        self.ID = []  # Keywords Plus®
        self.AB = ''  # 摘要
        self.C1 = []  # 作者地址
        self.RP = ''  # 通讯作者地址
        self.EM = []  # 电子邮件地址
        self.RI = []  # ResearcherID 号
        self.OI = []  # ORCID 标识符(Open Researcher and Contributor ID)
        self.FU = ''  # 基金资助机构和授权号
        self.FX = ''  # 基金资助正文
        self.CR = []  # 引用的参考文献
        self.NR = ''  # 引用的参考文献数
        self.TC = ''  # Web of Science 核心合集的被引频次计数
        self.Z9 = ''  # 被引频次合计
        self.U1 = ''  # 使用次数（最近 180 天）
        self.U2 = ''  # 使用次数（2013 年至今）
        self.PU = ''  # 出版商
        self.PI = ''  # 出版商所在城市
        self.PA = ''  # 出版商地址
        self.SN = ''  # 国际标准期刊号 (ISSN)
        self.EI = ''  # 电子国际标准期刊号(eISSN)
        self.BN = ''  # 国际标准书号(ISBN)
        self.J9 = ''  # 长度为 29 个字符的来源文献名称缩写
        self.JI = ''  # ISO 来源文献名称缩写
        self.PD = ''  # 出版日期
        self.PY = ''  # 出版年
        self.VL = ''  # 卷
        self.IS = ''  # 期
        self.PN = ''  # 子辑
        self.SU = ''  # 增刊
        self.MA = ''  # 会议摘要
        self.BP = ''  # 开始页
        self.EP = ''  # 结束页
        self.AR = ''  # 文献编号
        self.DI = ''  # 数字对象标识符 (DOI)
        self.D2 = ''  # 书籍的数字对象标识符(DOI)
        self.EA = ''  # 提前访问日期
        self.EY = ''  # 提前访问年份
        self.PG = ''  # 页数
        self.P2 = ''  # 章节数(Book Citation Index)
        self.WC = []  # Web of Science 类别
        self.SC = []  # 研究方向 OPTDATA
        self.GA = ''  # 文献传递号
        self.PM = ''  # PubMed ID
        self.UT = ''  # 入藏号
        self.OA = ''  # 公开访问指示符
        self.HP = ''  # ESI 热门论文。请注意，此字段值仅适用于 ESI 订阅者。
        self.HC = ''  # ESI 常被引用的论文请注意，此字段值仅适用于 ESI 订阅者。
        self.DA = ''  # 生成此报告的日期。
        self.ER = ''  # 记录结束
        self.EF = ''  # 文件结束
        # Custom Field
        self.cls = 'wos'
        self.reftype = 'wos'
        self.database = 'wos'
        self.srcfile = ''
        # Parse LCR/LCS
        self.RID = -1  # 文献编号
        self.CCR = []  # 参考文献删除DOI
        self.CTX = ''  # 引用文本
        self.LCS = []  # 本地被引文献编号
        self.LCR = []  # 本地引用文献编号


def isdb(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        try:
            line = datafile.readline()
            fn = line[4:].strip()
            line = datafile.readline()
            vr = line[3:].strip()
            data_header = ('Clarivate Analytics Web of Science',
                           'Thomson Reuters Web of Science™',
                           'Thomson Reuters Web of Knowledge™',
                           'ISI Export Format')
            if fn not in data_header or vr != '1.0':
                return False
        except UnicodeDecodeError:
            return False
    return True


def parsedata(datafile_path):
    data = []
    fields = ['AF', 'CR', 'AU', 'C1']
    if isdb(datafile_path):
        with open(datafile_path, 'r', encoding='utf-8') as datafile:
            lastfield = ''
            line = datafile.readline()
            fn = line[4:].strip()
            line = datafile.readline()
            vr = line[3:].strip()
            for line in datafile:
                if line != '\n':
                    if line != 'ER\n':
                        field = line[:2]
                        text = line[3:].strip()
                        if field == 'PT':
                            dataitem = WosData()
                            dataitem.FN = fn
                            dataitem.VR = vr
                        if field in fields:
                            setattr(dataitem, field, [text])
                        elif field == '  ':
                            txt = getattr(dataitem, lastfield)
                            if lastfield in fields:
                                txt.append(text)
                            else:
                                txt = ' '.join([txt, text])
                            setattr(dataitem, lastfield, txt)
                        else:
                            setattr(dataitem, field, text)
                        if field != '  ':
                            lastfield = field
                    else:
                        dataitem.srcfile = datafile_path
                        data.append(dataitem)
    else:
        data = []
    return data


def addlcrlcs(data):
    for rid, item in enumerate(data):
        item.RID = rid  # 添加索引号
        item.CCR = set(add_ccr(item))  # 参考文献删除DOI
        item.CTX = add_ctx(item)  # 添加引用文本
    data = add_lcsr(data)
    return data


def add_ccr(item):
    # 去掉参考文献内DOI
    ccr = []
    for unit in item.CR:
        if ', DOI ' in unit:
            unit = unit.split(', DOI')[0]
        ccr.append(unit)
    return ccr


def add_ctx(data):
    # 添加文献引用文本
    author = data.AU[0].replace(', ', ' ') if data.AU else ''
    year = str(data.PY) if data.PY else ''
    journal = data.J9 if data.J9 else data.BS if data.BS else data.SO if data.SO else ''
    volume = 'V' + data.VL if data.VL else ''
    page = 'P' + data.BP if data.BP else ''
    citetext = ', '.join(item for item in (author, year, journal, volume, page) if item)
    return citetext


def add_lcsr(data):
    # 添加 LCS LCR
    cite_dict = {}  # 建立CTX与RID索引字典
    cite_set = set()  # 建立CTX SET总表
    for item in data:
        cite_dict[item.CTX] = item.RID
        cite_set.add(item.CTX)
    for rid, item in enumerate(data):
        if item.CCR:
            cite_list = cite_set & item.CCR  # 计算引用文本总表与当前文献CR的交集
            for unit in cite_list:
                data[cite_dict.get(unit)].LCS.append(rid)
                item.LCR.append(cite_dict.get(unit))
    return data


def optdata(data):
    keys = ('SC', 'ID', 'EM', 'DE', 'RI', 'WC', 'OI')
    for item in data:
        for key in keys:
            text = getattr(item, key)
            if text:
                txt = text.split(';')
                txt = [t.strip() for t in txt]
                setattr(item, key, txt)
    # Add LCR/LCS
    data = addlcrlcs(data)
    return data


# region Same in Filters
def getdata(datafile_path):
    # Auto Detect File or Dir
    if os.path.isfile(datafile_path):
        data = openfile(datafile_path)
    elif os.path.isdir(datafile_path):
        data = opendir(datafile_path)
    else:
        data = []
    # Change Field Type for Use
    if data:
        data = optdata(data)
    return data


def openfile(datafile_path):
    data = parsedata(datafile_path)
    return data


def opendir(datafile_path):
    data = []
    with os.scandir(datafile_path) as datafiles:
        for file in datafiles:
            if os.path.isfile(file.path):
                data += parsedata(file.path)
    return data


if __name__ == '__main__':
    # Datafile Path
    datafile_path = '../../data/'
    # Read Data
    data = getdata(datafile_path)
# endregion
