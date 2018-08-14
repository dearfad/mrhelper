#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: mrhimp.py
# Usage: Medical Review Helper DataFile Import Module

import os

import mrhpkg.filters.cnki as cnki
import mrhpkg.filters.pubmed as pubmed
import mrhpkg.filters.wanfang as wanfang
import mrhpkg.filters.wos as wos


def getdb(filepath, parser):
    for dbname in parser:
        if parser[dbname].isdb(filepath):
            return dbname
    return ''


def getdata(filepath):
    parser = {'wos': wos, 'pubmed': pubmed, 'wanfang': wanfang, 'cnki': cnki}
    data = {'wos': [], 'pubmed': [], 'wanfang': [], 'cnki': []}
    if os.path.isdir(filepath):
        with os.scandir(filepath) as datafiles:
            for file in datafiles:
                if os.path.isfile(file.path):
                    dbname = getdb(file.path, parser)
                    if dbname in data.keys():
                        data[dbname] += parser[dbname].getdata(file.path)
                    else:
                        print('Unknown Database', file.path)
    elif os.path.isfile(filepath):
        dbname = getdb(filepath, parser)
        if dbname in data.keys():
            data[dbname] += parser[dbname].getdata(filepath)
        else:
            print('Unknown Database', filepath)
    else:
        print('Filepath is not a valid path.')
    return data


def main():
    datafile_path = '../data/'
    data = getdata(datafile_path)
    print(data)


if __name__ == '__main__':
    main()
