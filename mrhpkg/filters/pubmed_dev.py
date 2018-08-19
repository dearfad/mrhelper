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
    datatype: str = 'MEDLINE'
    database: str = 'pubmed'


def getdata(filepath):
    """Return Data From File By MEDLINE Format Parser."""
    return parsedata(filepath) if checktype(filepath) else -1


def checktype(filepath):
    """Check PubMed MEDLINE Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline() == '\n' and datafile.readline()[:4] == 'PMID'


def parsedata(filepath):
    """Parse Exported File in MEDLINE format."""
    data = []
    lastfield = ''
    with open(filepath, encoding='utf-8') as datafile:
        for index, line in enumerate(datafile):
            if line == '\n':
                item = PubMed()
                if not lastfield:
                    data.append(item)
            else:
                field = line[:4].strip()
                text = line[6:].strip()
                if field:
                    content = getattr(item, field, '')
                    if content:
                        content = ' '.join([content, text])
                        setattr(item, field, content)
                    else:
                        setattr(item, field, text)
                    lastfield = field
                else:
                    content = getattr(item, lastfield)
                    content = ' '.join([content, text])
                    setattr(item, lastfield, content)
        if item:
            data.append(item)
    return data


if __name__ == '__main__':
    path = './mrhpkg/filters/pubmed.txt'
    srcdata = getdata(path)
    if srcdata == -1:
        print('-1')
    else:
        print(len(srcdata))
