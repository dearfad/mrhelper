#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: cnki.py
# Usage: CNKI DataFile Process Module For E-Study Format

import os
import tempfile

import defusedxml.ElementTree as et


class XmlData:
    def __init__(self):
        # Predefine Field
        self.DataType = ''
        self.Title = ''
        self.Author = []
        self.Source = ''
        self.Year = ''
        self.PubTime = ''
        self.Keyword = []
        self.Summary = ''
        self.Period = ''
        self.PageCount = ''
        self.Page = ''
        self.SrcDatabase = ''
        self.Organ = ''
        self.Link = ''
        self.City = ''
        self.Meeting = ''
        self.Roll = ''
        self.Degree = ''
        self.Teacher = ''
        # Custom Field
        self.cls = 'xml'
        self.reftype = 'noteexpress'
        self.database = 'cnki'
        self.srcfile = ''


def isdb(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        try:
            line = datafile.readline().lower()
            if line != '<?xml version="1.0" encoding="utf-8"?>\n':
                return False
        except UnicodeDecodeError:
            return False
    return True


def fixtreeparse(datafile_path):
    ##################################################
    # Add Func Here if Xml File is not good for parse.
    ##################################################
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        eslines = datafile.readlines()
        ############################################################################
        # For CNKI E-Study .eln Format
        fixstr = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >\n'
        if eslines[-2] == fixstr:
            eslines.pop(-2)
        ############################################################################
        tmpfile = tempfile.TemporaryFile(mode='w+t', encoding='utf-8', dir='.')
        tmpfile.writelines(eslines)
        tmpfile.seek(0)
        try:
            tree = et.parse(tmpfile)
        finally:
            tmpfile.close()  # make sure tempfile deleted
    return tree


def parsedata(datafile_path):
    data = []
    strlist = ['Title', 'DataType', 'Source', 'Year', 'PubTime',
               'Summary', 'Period', 'PageCount', 'Page', 'SrcDatabase',
               'Organ', 'Link', 'City', 'Meeting', 'Roll', 'Degree',
               'Teacher']
    if isdb(datafile_path):
        try:
            tree = et.parse(datafile_path)
        except et.ParseError:
            tree = fixtreeparse(datafile_path)
        root = tree.getroot()
        for sub in root:
            if sub.tag == 'DATA':
                dataitem = XmlData()
                for item in sub:
                    if item.tag in strlist:
                        setattr(dataitem, item.tag, item.text)
                    if item.tag == 'Author':
                        if ';' in item.text:
                            dataitem.Author = item.text.strip(';').split(';')
                        elif ',' in item.text:
                            dataitem.Author = item.text.split(',')
                        else:
                            dataitem.Author = [item.text]
                    if item.tag == 'Keyword':
                        dataitem.Keyword = item.text.split(';')
                dataitem.srcfile = datafile_path
                data.append(dataitem)
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


def main():
    datafile_path = '../../data/'
    data = getdata(datafile_path)
    print(data)


if __name__ == '__main__':
    main()
