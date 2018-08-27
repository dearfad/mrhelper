#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Filename: cnki.py
# Usage: CNKI DataFile Process Module For E-Study Format
"""

import tempfile

import defusedxml.ElementTree as ElementTree


class CnkiItem:
    """CNKI ESTUDY Data Format."""

    def __init__(self):
        self.database = 'CNKI'


def getdata(filepath):
    """Return Data From File By XML Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = _parsefile(filepath) if checktype(filepath) else -1
    if data != -1:
        data = _fixdata(data)
    return data


def checktype(filepath):
    """Check CNKI Exported File Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline().lower() == '<?xml version="1.0" encoding="utf-8"?>\n'


def _fix_treeparse(datafile_path):
    """Remove Lines For XML Parse."""
    with open(datafile_path, encoding='utf-8') as datafile:
        eslines = datafile.readlines()
        fixstr = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >\n'
        if eslines[-2] == fixstr:
            eslines.pop(-2)
        tmpfile = tempfile.TemporaryFile(mode='w+t', encoding='utf-8', dir='.')
        tmpfile.writelines(eslines)
        tmpfile.seek(0)
        tree = ElementTree.parse(tmpfile)
        tmpfile.close()
    return tree


def _parsefile(filepath):
    """Parse Exported File From CNKI in ESTUDY format."""
    data = []
    tree = _fix_treeparse(filepath)
    root = tree.getroot()
    for sub in root:
        if sub.tag == 'DATA':
            cnkiitem = CnkiItem()
            data.append(cnkiitem)
            for item in sub:
                setattr(cnkiitem, item.tag, item.text)
    return data


def _fixdata(data):
    """Data Preparation."""
    for cnkiitem in data:
        if getattr(cnkiitem, 'Author', ''):
            if ';' in cnkiitem.Author:
                cnkiitem.Author = cnkiitem.Author.strip(';').split(';')
            elif ',' in cnkiitem.Author:
                cnkiitem.Author = cnkiitem.Author.split(',')
            else:
                cnkiitem.Author = [cnkiitem.Author]
        if getattr(cnkiitem, 'Keyword', ''):
            cnkiitem.Keyword = cnkiitem.Keyword.split(';;')
    return data
