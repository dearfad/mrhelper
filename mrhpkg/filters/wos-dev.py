#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: wos.py
Usage: DataFile Parse Module For ALL Format of Web of Science
"""

from dataclasses import dataclass, field


@dataclass
class WOS:
    """WOS Data Format.
    Web of Science Core Collection Fields List
    http://images.webofknowledge.com/WOKRS5272R3/help/zh_CN/WOK/hs_wos_fieldtags.html
    """
    # Custom Fields
    datatype: str = 'CORE'
    database: str = 'WOS'
    RID: int = -1  # References ID
    CCR: list = field(default_factory=list)  # Remove DOI from Field CR
    CTX: str = ''  # Cited Text
    LCS: list = field(default_factory=list)  # Local Cited References List
    LCR: list = field(default_factory=list)  # Local Citing References List


def getdata(filepath):
    """Return Data From File By CORE Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = parsefile(filepath) if checktype(filepath) else -1
    # if data:
    #     data = optdata(data)
    return data


def checktype(filepath):
    """Check WOS Exported File Format."""
    validlines = ['FN Thomson Reuters Web of Science™\n', 'VR 1.0\n']
    with open(filepath, encoding='utf-8-sig') as datafile:
        return datafile.readline() == validlines[0] and datafile.readline() == validlines[1]


def parsefile(datafile_path):
    """Parse Exported File From Web of Science in CORE format."""
    data = []
    lastfield = ''
    uselesslines = ['\n', 'ER\n', 'EF\n',
                    'FN Thomson Reuters Web of Science™\n', 'VR 1.0\n']
    with open(datafile_path, encoding='utf-8-sig') as datafile:
        for line in datafile:
            if line not in uselesslines:
                field = line[:2].strip()
                text = line[3:].strip()
                if field:
                    if field == 'PT':
                        wositem = WOS()
                        data.append(wositem)
                    setattr(wositem, field, text)
                    lastfield = field
                else:
                    content = getattr(wositem, lastfield)
                    if isinstance(content, str):
                        content = [content]
                    content.append(text)
                    setattr(wositem, lastfield, content)
    return data


def addlcrlcs(data):
    for rid, item in enumerate(data):
        item.RID = rid  # 添加索引号
        item.CCR = set(remove_doiincr(item))  # 参考文献删除DOI
        item.CTX = add_ctx(item)  # 添加引用文本
    data = add_lcsr(data)
    return data


def remove_doiincr(item):
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
    citetext = ', '.join(item for item in (
        author, year, journal, volume, page) if item)
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


if __name__ == '__main__':
    path = './mrhpkg/filters/500.txt'
    srcdata = getdata(path)
    print(len(srcdata), srcdata[1].TI)
