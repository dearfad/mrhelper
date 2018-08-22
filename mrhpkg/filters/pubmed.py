#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: pubmed.py
Usage: DataFile Parse Module For MEDLINE Format of PubMed
"""


class PubmedItem:
    """PubMed MEDLINE Data Format.
    MEDLINE®/PubMed® Data Element (Field) Descriptions
    https://www.nlm.nih.gov/bsd/mms/medlineelements.html
    """

    def __init__(self):
        self.database = 'PUBMED'


def getdata(filepath):
    """Return Data From File By MEDLINE Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = _parsefile(filepath) if checktype(filepath) else -1
    if data != -1:
        data = _fixdata(data)
    return data


def checktype(filepath):
    """Check PubMed MEDLINE Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline() == '\n' and datafile.readline()[:4] == 'PMID'


def _parsefile(filepath):
    """Parse Exported File From Pubmed in MEDLINE format."""
    data = []
    lastfield = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            if line == '\n':
                pubmeditem = PubmedItem()
                data.append(pubmeditem)
            else:
                field = line[:4].strip()
                text = line[6:].strip()
                if field:
                    content = getattr(pubmeditem, field, '')
                    if content:
                        if isinstance(content, str):
                            content = [content]
                        content.append(text)
                        setattr(pubmeditem, field, content)
                    else:
                        setattr(pubmeditem, field, text)
                    lastfield = field
                else:
                    content = getattr(pubmeditem, lastfield)
                    if isinstance(content, str):
                        content = ' '.join([content, text])
                    else:
                        content[-1] = ' '.join([content[-1], text])
                    setattr(pubmeditem, lastfield, content)
    return data


def _fixdata(data):
    """Data Preparation."""
    return data
