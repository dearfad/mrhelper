#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: wos.py
Usage: DataFile Parse Module For ALL Format of Web of Science
"""


class WosItem:
    """WOS Data Format.
    Web of Science Core Collection Fields List
    http://images.webofknowledge.com/WOKRS5272R3/help/zh_CN/WOK/hs_wos_fieldtags.html
    """

    def __init__(self):
        self.database = 'WOS'
    # Custom Fields
    # RID: int = -1  # References ID
    # CCR: set()  # Remove DOI from Field CR
    # CTX: str = ''  # Cited Text
    # LCS: list = field(default_factory=list)  # Local Cited References List
    # LCR: list = field(default_factory=list)  # Local Citing References List


def getdata(filepath):
    """Return Data From File By CORE Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = _parsefile(filepath) if _checktype(filepath) else -1
    if data != -1:
        data = fixdata(data)
        data = localinfo(data)
    return data


def _checktype(filepath):
    """Check WOS Exported File Format."""
    validlines = ['FN Thomson Reuters Web of Science™\n', 'VR 1.0\n']
    with open(filepath, encoding='utf-8-sig') as datafile:
        return datafile.readline() == validlines[0] and datafile.readline() == validlines[1]


def _parsefile(datafile_path):
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
                        wositem = WosItem()
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


def localinfo(data):
    """Parse WosItem LCR LCS Data."""
    for rid, wositem in enumerate(data):
        wositem.RID = rid
        wositem.CCR = set(_remove_doi(wositem))
        wositem.CTX = _add_ctx(wositem)
    data = add_info(data)
    return data


def _remove_doi(wositem):
    """Remove DOI In WosItem.CR."""
    ccr = []
    for item in wositem.CR:
        if ', DOI ' in item:
            item = item.split(', DOI')[0]
        ccr.append(item)
    return ccr


def _add_ctx(wositem):
    """Add Cited Text."""
    # todo
    author = wositem.AU[0].replace(', ', ' ') if getattr(wositem, 'AU', '') else ''
    year = wositem.PY if getattr(wositem, 'PY', '') else ''
    journal = wositem.J9 if wositem.J9 else wositem.BS if wositem.BS else wositem.SO if wositem.SO else ''
    volume = 'V' + wositem.VL if wositem.VL else ''
    page = 'P' + wositem.BP if wositem.BP else ''
    citetext = ', '.join(item for item in (
        author, year, journal, volume, page) if item)
    return citetext


def add_info(data):
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


def fixdata(data):
    for wositem in data:
        if isinstance(wositem.AU, str):
            wositem.AU = [wositem.AU]
    return data


if __name__ == '__main__':
    path = './mrhpkg/filters/500.txt'
    srcdata = getdata(path)
    for item in srcdata:
        bs = getattr(item, 'SO', '')
        print(type(bs))
