#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Filename: cnki.py
# Usage: CNKI DataFile Process Module For E-Study Format
# DataType: 1=学术期刊；2=学位论文；3=会议；4=报纸...
# 限定首行 DataType: 1 为校验标准

CNKI E-Study格式范例
DataType: 1
Title-题名: 1例卡培他滨与苯妥英钠相互作用致乳腺癌合并癫痫患者小脑功能障碍的病例分析
Author-作者: 柯洪琴;陈璿英;王启斌;
Source-刊名: 中南药学
Year-年: 2021
PubTime-出版时间: 2021-01-18
Keyword-关键词: 苯妥英钠;卡培他滨;相互作用;小脑功能障碍;不良反应
Summary-摘要: <正>苯妥英钠作为一种传统抗癫痫药物(AEDs),因价格低、疗效佳、易获取,目前仍在基层医院广泛用于癫痫治疗。因其具有饱和性药代动力学特点,治疗窗窄,患者用药过程中容易发生血药浓度过高引起毒性反应。当合并癫痫的恶性肿瘤患者使用卡培他滨化疗时,卡培他滨与苯妥英钠的相互作用可能导致后者血药浓度升高甚至出现重度中毒的情况~([1-3])。
Period-期: 01
Roll-卷: 19
PageCount-页数: 3
Page-页码: 168-170
SrcDatabase-来源库: 期刊
Organ-机构: 十堰市太和医院药学部(湖北医药学院附属医院);南昌大学第一附属医院药剂科;
Link-链接: https://kns.cnki.net/kcms/detail/detail.aspx?FileName=ZNYX202101034&DbName=CJFQTEMP
"""


class CnkiItem:
    """CNKI ESTUDY Data Format."""

    def __init__(self):
        self.database = 'CNKI'


def getdata(filepath):
    """Return Data From File By E-Study Format Parser.
    Normal: Return Data List
    Error:  Return -1
    """
    data = _parsefile(filepath) if checktype(filepath) else -1
    data = _fixdata(data) if data != -1 else data
    return data


def checktype(filepath):
    """Check CNKI Exported File Format.
    Rule: First Line "DataType: 1\n"
    """
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline() == 'DataType: 1\n'


def _parsefile(filepath):
    """Parse Exported File From CNKI in ESTUDY format."""
    data = []
    lastfield = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            field, text = line.strip().split(': ')
            if field == 'DataType':
                cnkiitem = CnkiItem()
                data.append(cnkiitem)
            setattr(cnkiitem, field, text)
    return data


def _fixdata(data):
    """Data Preparation."""
    for cnkiitem in data:

        # Change Authors to list by split with ";"
        author = getattr(cnkiitem, 'Author-作者', '')
        if author:
            setattr(cnkiitem, 'Author-作者', author.strip(';').split(';'))

        # Change Keywords to list by split with ";"
        keyword = getattr(cnkiitem, 'Keyword-关键词', '')
        if keyword:
            setattr(cnkiitem, 'Keyword-关键词', keyword.split(';'))

        # Change Organs to list by split with ";"
        organ = getattr(cnkiitem, 'Organ-机构', '')
        if organ:
            setattr(cnkiitem, 'Organ-机构', organ.strip(';').split(';'))

        # Apply Pubtime year to Year if no Year
        year = getattr(cnkiitem, 'Year-年', '')
        if not year:
            pubtime = getattr(cnkiitem, 'PubTime-出版时间', '')
            if pubtime:
                pubdate = pubtime.split(' ')[0]
                pubyear = pubdate.split('-')[0]
                setattr(cnkiitem, 'Year-年', pubyear)

    return data


if __name__ == '__main__':
    filepath = './mrhpkg/filters/demo_cnki_202101.txt'
    data = getdata(filepath)
    for cnkiitem in data:
        print(getattr(cnkiitem, 'Author-作者', ''))
