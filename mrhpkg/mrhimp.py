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
        self.mrhdata = []
        self.rawdata = []


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
        self.keywords = []
        # Mrhelper Define Field
        self.rid = -1  # References ID
        self.database = ''  # WOS, PUBMED, CNKI, WANFANG
        self.cs = ''  # Cited By
        self.cr = ''  # Citing
        self.lcs = []  # Local Cited By
        self.lcr = []  # Local Citing
        self.use = 1  # 0-Useless, 1-Evaluate, 2-Use
        self.iv = ''  # Independent Variable
        self.dv = ''  # Dependent Variable
        self.relation = 1  # Relation: 0-decrease, 1-no relation, 2-increase
        self.reftext = ''  # Description
        self.group = ['', '']  # Group, Subgroup


def getdata(filepath):
    """GET mrhdata AND rawdata From File.
    return dict{'mrhdata':mrhdata, 'rawdata':rawdata}
    """
    rawdata = _get_rawdata(filepath)
    mrhdata = _get_mrhdata(rawdata)
    return {'mrhdata': mrhdata, 'rawdata': rawdata}


def _get_rawdata(filepath):
    """Get rawdata From One of WOS, PUBMED, CNKI, WANFANG DATABASES."""
    databases = [wos, pubmed, wanfang, cnki]
    for database in databases:
        data = database.getdata(filepath)
        if data != -1:
            return data
    return -1


def _get_mrhdata(rawdata):
    """Transform rawdata Into mrhdata."""
    mrhdata = []
    field_dict = {
        'author': {'WOS': 'AU', 'PUBMED': 'AU', 'WANFANG': 'Author', 'CNKI': 'Author'},
        'title': {'WOS': 'TI', 'PUBMED': 'TI', 'WANFANG': 'Title', 'CNKI': 'Title'},
        'type': {'WOS': 'DT', 'PUBMED': 'PT', 'WANFANG': 'ReferenceType', 'CNKI': 'DataType'},
        'journal': {'WOS': 'SO', 'PUBMED': 'JT', 'WANFANG': 'Journal', 'CNKI': 'Source'},
        'year': {'WOS': 'PY', 'PUBMED': 'DP', 'WANFANG': 'Year', 'CNKI': 'Year'},
        'volumn': {'WOS': 'VL', 'PUBMED': 'VI', 'WANFANG': '', 'CNKI': 'Roll'},
        'issue': {'WOS': 'IS', 'PUBMED': 'IP', 'WANFANG': 'Issue', 'CNKI': 'Period'},
        'page': {'WOS': ['BP', 'EP'], 'PUBMED': 'PG', 'WANFANG': 'Pages', 'CNKI': 'Page'},
        'link': {'WOS': '', 'PUBMED': '', 'WANFANG': 'URL', 'CNKI': 'Link'},
        'doi': {'WOS': 'DI', 'PUBMED': 'AID', 'WANFANG': 'DOI', 'CNKI': ''},
        'pmid': {'WOS': 'PM', 'PUBMED': 'PMID', 'WANFANG': '', 'CNKI': ''},
        'pmcid': {'WOS': '', 'PUBMED': 'PMC', 'WANFANG': '', 'CNKI': ''},
        'abstract': {'WOS': 'AB', 'PUBMED': 'AB', 'WANFANG': 'Abstract', 'CNKI': 'Summary'},
        'cs': {'WOS': 'TC', 'PUBMED': '', 'WANFANG': '', 'CNKI': ''},
        'cr': {'WOS': 'NR', 'PUBMED': '', 'WANFANG': '', 'CNKI': ''},
        'lcr': {'WOS': 'LCR', 'PUBMED': '', 'WANFANG': '', 'CNKI': ''},
        'lcs': {'WOS': 'LCS', 'PUBMED': '', 'WANFANG': '', 'CNKI': ''},
        'keywords': {'WOS': 'DE', 'PUBMED': 'OT', 'WANFANG': 'Keywords', 'CNKI': 'Keyword'}
    }
    for rid, rawitem in enumerate(rawdata):
        mrhitem = MrhItem()
        mrhitem.rid = rid
        mrhitem.database = rawitem.database
        for key in field_dict.keys():
            field = field_dict[key].setdefault(rawitem.database, '')
            if isinstance(field, list):
                value = [getattr(rawitem, unit, '') for unit in field]
            else:
                value = getattr(rawitem, field, '')
            setattr(mrhitem, key, value)
        mrhitem = _fix_mrhitem(mrhitem)
        mrhdata.append(mrhitem)
    return mrhdata


def _fix_mrhitem(mrhitem):
    """Fix mrhdata For General Use."""
    if mrhitem.database == 'CNKI':
        mrhitem.link = mrhitem.link.replace('/kns/', '/kcms/')
        mrhitem.link = mrhitem.link.replace('nvsm.cnki.net', 'kns.cnki.net')
        if mrhitem.type == '1':
            mrhitem.type = 'Journal Article'

    if mrhitem.database == 'WOS':
        mrhitem.page = '-'.join(mrhitem.page) if mrhitem.page else ''
        if mrhitem.cr:
            mrhitem.cr = int(mrhitem.cr)
        if mrhitem.cs:
            mrhitem.cs = int(mrhitem.cs)

    if mrhitem.database == 'PUBMED':
        mrhitem.year = re.findall(r'\d\d\d\d', mrhitem.year)[0]
        for doi in mrhitem.doi:
            if '[doi]' in doi:
                mrhitem.doi = doi.split(' ')[0]
                break
            else:
                mrhitem.doi = ''
        mrhitem.journal = mrhitem.journal.upper() if mrhitem.journal else ''

    return mrhitem
