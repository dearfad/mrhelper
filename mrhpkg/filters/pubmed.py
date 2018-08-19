#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: pubmed.py
Usage: DataFile Parse Module For MEDLINE Format of PubMed
"""

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
    """Return Data From File By MEDLINE Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    return parsedata(filepath) if checktype(filepath) else -1


def checktype(filepath):
    """Check PubMed MEDLINE Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline() == '\n' and datafile.readline()[:4] == 'PMID'


def parsedata(filepath):
    """Parse Exported File From Pubmed in MEDLINE format."""
    data = []
    lastfield = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            if line == '\n':
                pmditem = PubMed()
                data.append(pmditem)
            else:
                field = line[:4].strip()
                text = line[6:].strip()
                if field:
                    content = getattr(pmditem, field, '')
                    if content:
                        if isinstance(content, str):
                            content = [content]
                        content.append(text)
                        setattr(pmditem, field, content)
                    else:
                        setattr(pmditem, field, text)
                    lastfield = field
                else:
                    content = getattr(pmditem, lastfield)
                    if isinstance(content, str):
                        content = ' '.join([content, text])
                    else:
                        content[-1] = ' '.join([content[-1], text])
                    setattr(pmditem, lastfield, content)
    return data
