#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Filename: mrhimp.py
# Usage: Medical Review Helper DataFile Import Module
"""

import re

import mrhpkg.filters.cnki as cnki
import mrhpkg.filters.pubmed as pubmed
import mrhpkg.filters.wanfang as wanfang
import mrhpkg.filters.wos as wos


class MrhProject:
    """MrHelper Project Data Format."""

    def __init__(self):
        self.title = ''
        self.author = []
        self.abstract = ''
        self.keywords = []
        self.refseq = []
        self.data = []
        self.srcdata = {}


class MrhItem:
    """MrHelper Data Item Format."""

    def __init__(self):
        self.author = []
        self.title = ''
        self.type = ''
        self.journal = ''
        self.year = ''
        self.volumn = ''
        self.issue = ''
        self.page = ''
        self.link = ''
        self.doi = ''
        self.pmid = ''
        self.pmcid = ''
        self.abstract = ''
        self.database = ''
        self.cs = ''  # Cited By
        self.cr = ''  # Citing
        self.lcs = []  # Local Cited By
        self.lcr = []  # Local Citing
        self.keywords = []
        # Mrhelper Define Field
        self.rid = -1  # References ID
        self.use = 1  # 0-Useless, 1-Evaluate, 2-Use
        self.iv = ''  # Independent Variable
        self.dv = ''  # Dependent Variable
        self.relation = 1  # Relation: 0-decrease, 1-no relation, 2-increase
        self.reftext = ''  # Description
        self.group = ['', '']  # Group, Subgroup


def _get_field_value(item, dbname, field_dict):
    field = field_dict.setdefault(dbname, '')
    if isinstance(field, list):
        value = []
        for unit in field:
            data = getattr(item, unit)
            if data:
                value.append(getattr(item, unit))
    else:
        value = getattr(item, field) if field else ''
    return value


def _parse_data(srcdata):
    mrhdata = []
    databases = ['wos', 'pubmed', 'wanfang', 'cnki']
    field_dict = {
        'author': {'wos': 'AU', 'pubmed': 'AU', 'wanfang': 'Author', 'cnki': 'Author'},
        'title': {'wos': 'TI', 'pubmed': 'TI', 'wanfang': 'Title', 'cnki': 'Title'},
        'type': {'wos': 'DT', 'pubmed': 'PT', 'wanfang': 'ReferenceType', 'cnki': 'DataType'},
        'journal': {'wos': 'SO', 'pubmed': 'JT', 'wanfang': 'Journal', 'cnki': 'Source'},
        'year': {'wos': 'PY', 'pubmed': 'DP', 'wanfang': 'Year', 'cnki': 'Year'},
        'volumn': {'wos': 'VL', 'pubmed': 'VI', 'wanfang': '', 'cnki': 'Roll'},
        'issue': {'wos': 'IS', 'pubmed': 'IP', 'wanfang': 'Issue', 'cnki': 'Period'},
        'page': {'wos': ['BP', 'EP'], 'pubmed': 'PG', 'wanfang': 'Pages', 'cnki': 'Page'},
        'link': {'wos': '', 'pubmed': '', 'wanfang': 'URL', 'cnki': 'Link'},
        'doi': {'wos': 'DI', 'pubmed': 'AID', 'wanfang': 'DOI', 'cnki': ''},
        'pmid': {'wos': 'PM', 'pubmed': 'PMID', 'wanfang': '', 'cnki': ''},
        'pmcid': {'wos': '', 'pubmed': 'PMC', 'wanfang': '', 'cnki': ''},
        'abstract': {'wos': 'AB', 'pubmed': 'AB', 'wanfang': 'Abstract', 'cnki': 'Summary'},
        'cs': {'wos': 'TC', 'pubmed': '', 'wanfang': '', 'cnki': ''},
        'cr': {'wos': 'NR', 'pubmed': '', 'wanfang': '', 'cnki': ''},
        'lcr': {'wos': 'LCR', 'pubmed': '', 'wanfang': '', 'cnki': ''},
        'lcs': {'wos': 'LCS', 'pubmed': '', 'wanfang': '', 'cnki': ''},
        'keywords': {'wos': 'DE', 'pubmed': 'OT', 'wanfang': 'Keywords', 'cnki': 'Keyword'}
    }
    rid = -1
    for dbname in databases:
        for item in srcdata[dbname]:
            mrhitem = MrhItem()
            rid += 1
            mrhitem.rid = rid
            mrhitem.database = dbname
            for key in field_dict.keys():
                value = _get_field_value(item, dbname, field_dict[key])
                setattr(mrhitem, key, value)
            mrhdata.append(mrhitem)
    return mrhdata


def _fix_data(mrhdata, srcdata):
    for item in mrhdata:
        # fix cnki link
        if item.database == 'cnki':
            item.link = item.link.replace('/kns/', '/kcms/')
            item.link = item.link.replace('nvsm.cnki.net', 'kns.cnki.net')
            # fix type
            if item.type == '1':
                item.type = 'Journal Article'
        # fix wos page
        if item.database == 'wos':
            item.page = '-'.join(item.page) if item.page else ''
        # fix pubmed year
        if item.database == 'pubmed':
            item.year = re.findall('\d\d\d\d', item.year)[0]
            for doi in item.doi:
                if '[doi]' in doi:
                    item.doi = doi.split(' ')[0]
                    break
            else:
                item.doi = ''
            item.journal = item.journal.upper() if item.journal else ''
    return mrhdata


def getdata(filepath):
    mrhproject = MrhProject()
    srcdata = getsrcdata(filepath)
    mrhproject.srcdata = srcdata
    # mrhdata = _parse_data(srcdata)
    # mrhdata = _fix_data(mrhdata, srcdata)
    # mrhproject.data = mrhdata
    return mrhproject


def getsrcdata(filepath):
    databases = [wos, pubmed, wanfang, cnki]
    for database in databases:
        data = database.getdata(filepath)
        if data != -1:
            return data
    return -1


def main():
    path = './mrhpkg/pubmed.txt'
    mrhproject = getdata(path)
    pass

if __name__ == '__main__':
    main()
