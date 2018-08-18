#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: pubmed.py
Usage: DataFile Parse Module For MEDLINE Format of PubMed
"""

import os
from dataclasses import dataclass


@dataclass
class PubMed:
    """PubMed MEDLINE Data Format.
    MEDLINE®/PubMed® Data Element (Field) Descriptions
    https://www.nlm.nih.gov/bsd/mms/medlineelements.html
    """
    # Custom Fields
    type: str = 'MEDLINE'
    database: str = 'pubmed'


def checktype(filepath):
    """Check PubMed MEDLINE Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline() == '\n' and datafile.readline()[:4] == 'PMID'


def parsedata(datafile_path):
    data = []
    fields = ['FAU', 'AUID', 'RN', 'OT', 'OID', 'LID', 'AD',
              'PHST', 'AID', 'MH', 'SB', 'GS', 'CIN', 'IS',
              'AU', 'PT', 'GR']
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        lastfield = ''
        datafile.readline()
        for line in datafile:
            if line != '\n':
                field = line[:4].strip()
                text = line[6:].strip()
                if field == 'PMID':
                    dataitem = PubMed()
                if field in fields:
                    txt = getattr(dataitem, field)
                    if txt:
                        txt.append(text)
                    else:
                        txt = [text]
                    setattr(dataitem, field, txt)
                elif not field:
                    lasttext = getattr(dataitem, lastfield)
                    if lastfield in fields:
                        lasttext[-1] = ' '.join([lasttext[-1], text])
                        setattr(dataitem, lastfield, lasttext)
                    else:
                        newtext = ' '.join([lasttext, text])
                        setattr(dataitem, lastfield, newtext)
                else:
                    setattr(dataitem, field, text)
                if field == 'AD' and lastfield == 'AD':
                    #######################
                    # 1 author 2 address
                    # parse necessary ?
                    #######################
                    pass
                if field:
                    lastfield = field
            else:
                dataitem.srcfile = datafile_path
                data.append(dataitem)
        data.append(dataitem)  # Append last item
    return data


def getdata(filepath):
    """Return Data From File By MEDLINE Format Parser."""
    return parsedata(filepath) if checktype(filepath) else -1


if __name__ == '__main__':
    path = 'pubmed.txt'
    srcdata = getdata(path)
    if srcdata == -1:
        print('-1')
    else:
        print(len(srcdata))
