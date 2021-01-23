#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: wanfang.py
Usage: Wanfang DataFile Process Module For NoteExpress Format
# 限定首行前16个字符为 {Reference Type}

{Reference Type}: Journal Article
{Title}: 超声引导下前锯肌平面阻滞对乳腺癌改良根治术术后肿瘤转移、复发的影响
{Translated Title}: Influence of ultrasound-guided serratus plane block on metastasis and recurrence of breast cancer after modified radical mastectomy
{Author}: 江文杰
{Author}: 韩超
{Author}: 顾达民
{Translated Author}: Wenjie JIANG
{Translated Author}:  Chao HAN
{Translated Author}:  Damin GU
{Author Address}: 宜兴市人民医院
{Author Address}: 宜兴市人民医院
{Author Address}: 宜兴市人民医院
{Journal}: 临床检验杂志（电子版）
{Translated Journal}: Clinical Laboratory Journal (Electronic Edition)
{Year}: 2020
{Volume}: 9
{Issue}: 1
{Pages}: 117-118
{Keywords}: 前锯肌平面阻滞
{Keywords}:  乳腺癌改良根治术
{Keywords}:  基质金属蛋白酶
{Abstract}: 目的 探讨超声引导下前锯肌平面(SP)阻滞对乳腺癌改良根治术术后免疫因子及基质金属蛋白酶(MMPs)的影响.方法 选择2015年6月-2017年6月于本院择期行乳腺癌改良根治术的患者60例,随机平均分为两组:SP阻滞组(S组)和对照组(C组).两组在麻醉诱导后均接受超声引导下SP穿刺,S组注射0.5％罗哌卡因15 mL,C组注射等容量生理盐水.观测两组患者术前30 min(T0)、术后3 h(T1)、术后24 h(T2)的血清IL-10和MMP-2、MMP-9的变化情况.结果 两组患者IL-10浓度在T0、T1、T2呈明显升高趋势(P<0.05).S组IL-10浓度在T1、T2均显著高于C组(P<0.05).两组患者MMP-2、MMP-9浓度在T0、T1、T2均呈明显升高趋势(P<0.05).S组MMP-2、MMP-9浓度在T1、T2均显著低于C组(P<0.05).结论 超声引导下SP阻滞可有效减少全麻下行乳腺癌改良根治术术后肿瘤转移、复发的可能性.
{URL}: http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=lcjyzz-d202001100
{Database Provider}: 北京万方数据股份有限公司
{Language}: chi
"""


class WanfangItem:
    """Wanfang NoteExpress Format."""

    def __init__(self):
        self.database = 'WANFANG'


def getdata(filepath):
    """Return Data From File By NoteExpress Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = _parsefile(filepath) if checktype(filepath) else -1
    data = _fixdata(data) if data != -1 else data
    return data


def checktype(filepath):
    """Check WanFang NoteExpress Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline()[:16] == '{Reference Type}'


def _parsefile(filepath):
    """Parse Exported File From WanFang in NoteExpress format."""
    data = []
    lastfield = ''
    wanfangitem = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            if line != '\n':

                # Fix WanFang Exported File Abstract Format Error
                if lastfield == 'Abstract' and line[0] != '{':
                    field = 'Abstract'
                    text = line
                else:
                    field, text = line.strip().split(': ')
                    field = field.strip('{}')
                    text = text.strip()

                if field == 'Reference Type':
                    wanfangitem = WanfangItem()
                    data.append(wanfangitem)

                if field == lastfield:
                    content = getattr(wanfangitem, field)
                    if isinstance(content, str):
                        content = [content]
                    content.append(text)
                    setattr(wanfangitem, field, content)
                else:
                    setattr(wanfangitem, field, text)

                lastfield = field
    return data


def _fixdata(data):
    """Data Preparation."""

    for wanfangitem in data:

        # Change str to list format
        listfield = set(['Author', 'Translated Author',
                         'Author Address', 'Keywords'])

        for wanfangitem in data:

            # Change field to list
            for key in wanfangitem.__dict__.keys():
                if key in listfield:
                    item = getattr(wanfangitem, key, '')
                    if isinstance(item, str):
                        setattr(wanfangitem, key, [item])

            # Change Abstract list to str Fix
            abstract = getattr(wanfangitem, 'Abstract', '')
            if abstract:
                if isinstance(abstract, list):
                    setattr(wanfangitem, 'Abstract', ' '.join(abstract))

    return data


if __name__ == '__main__':
    filepath = './mrhpkg/filters/demo_wanfang_202101.net'
    data = getdata(filepath)
    for wanfangitem in data[:1]:
        print(getattr(wanfangitem, 'Abstract', ''))
