#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: wanfang.py
Usage: Wanfang DataFile Process Module For NoteExpress Format
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
    if data != -1:
        data = _fixdata(data)
    return data


def checktype(filepath):
    """Check WanFang NoteExpress Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline()[:16] == '{Reference Type}'


def _parsefile(filepath):
    """Parse Exported File From WanFang in NoteExpress format."""
    data = []
    lastfield = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            if line != '\n':
                field = line.split(': ')[0].strip('{}')
                field = field.replace('/', '')
                field = field.replace(' ', '')

                # Fix WanFang Exported File Abstract Format Error
                if lastfield == 'Abstract' and line[0] != '{':
                    field = 'Abstract'
                    text = line
                else:
                    text = line.split(': ')[1].strip()

                if field == 'ReferenceType':
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
    return data
