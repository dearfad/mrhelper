#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: wanfang.py
# Usage: Wanfang DataFile Process Module For NoteExpress Format

import os


class NoteExpress:
    def __init__(self):
        # Predefine Field
        self.ReferenceType = ''
        self.Title = ''
        self.TranslatedTitle = ''
        self.Author = []
        self.TranslatedAuthor = []
        self.AuthorAddress = []
        self.Journal = ''
        self.TranslatedJournal = ''
        self.ISBNISSN = ''
        self.Year = ''
        self.Issue = ''
        self.Pages = ''
        self.Keywords = []
        self.Abstract = ''
        self.URL = ''
        self.DOI = ''
        self.DatabaseProvider = []
        self.Language = ''
        # Custom Field
        self.cls = 'noteexpress'
        self.reftype = 'noteexpress'
        self.database = 'wanfang'
        self.srcfile = ''
        self.reftxt = ''


def isdb(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        try:
            line = datafile.readline()
            if line[:16] != '{Reference Type}':
                return False
        except UnicodeDecodeError:
            return False
    return True


def parsedata(datafile_path):
    data = []
    fields = ['Title', 'TranslatedTitle', 'Journal', 'TranslatedJournal',
              'ISBNISSN', 'Year', 'Issue', 'Pages', 'URL', 'DOI',
              'DatabaseProvider']
    field_list = ['Author', 'TranslatedAuthor', 'AuthorAddress', 'Keywords']
    if isdb(datafile_path):
        with open(datafile_path, 'r', encoding='utf-8') as datafile:
            lastfield = ''
            for line in datafile:
                if line != '\n':
                    if line[0] == '{':
                        field = line.split(': ')[0].strip('{}')
                        field = field.replace('/', '')
                        field = field.replace(' ', '')
                        text = line.split(': ')[1].strip()
                        if field == 'ReferenceType':
                            dataitem = NoteExpress()
                            dataitem.ReferenceType = text
                        if field in fields:
                            setattr(dataitem, field, text)
                        if field in field_list:
                            txt = getattr(dataitem, field)
                            if txt:
                                txt.append(text)
                            else:
                                txt = [text]
                            setattr(dataitem, field, txt)
                        if field == 'Abstract':
                            if dataitem.Abstract:
                                dataitem.Abstract = ' '.join([dataitem.Abstract, text])
                            else:
                                dataitem.Abstract = text
                        if field == 'Language':
                            dataitem.Language = text
                            dataitem.srcfile = datafile_path
                            data.append(dataitem)
                        lastfield = field
                    else:
                        text = line.strip()
                        lasttext = getattr(dataitem, lastfield)
                        newtext = ' '.join([lasttext, text])
                        setattr(dataitem, lastfield, newtext)
    else:
        data = []
    return data


def optdata(data):
    return data


# region Same in Filters
def getdata(datafile_path):
    # Auto Detect File or Dir
    if os.path.isfile(datafile_path):
        data = openfile(datafile_path)
    elif os.path.isdir(datafile_path):
        data = opendir(datafile_path)
    else:
        data = []
    # Change Field Type for Use
    if data:
        data = optdata(data)
    return data


def openfile(datafile_path):
    data = parsedata(datafile_path)
    return data


def opendir(datafile_path):
    data = []
    with os.scandir(datafile_path) as datafiles:
        for file in datafiles:
            if os.path.isfile(file.path):
                data += parsedata(file.path)
    return data


if __name__ == '__main__':
    # Datafile Path
    datafile_path = '../../data/'
    # Read Data
    data = getdata(datafile_path)
# endregion
