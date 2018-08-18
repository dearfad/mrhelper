#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: pmd.py
# Usage: pmd DataFile Process Module For Medline Format

import os


class PubMed:
    def __init__(self):
        # Predefine Field
        # MEDLINE®/PubMed® Data Element (Field) Descriptions
        # https://www.nlm.nih.gov/bsd/mms/medlineelements.html
        self.AB = ''  # Abstract
        self.CI = ''  # Copyright Information
        self.AD = []  # Affiliation
        self.IRAD = ''  # Investigator Affiliation
        self.AID = []  # Article Identifier doi&pii
        self.AU = []  # Author
        self.AUID = []  # Author Identifier
        self.FAU = []  # Full Author
        self.BTI = ''  # Book Title
        self.CTI = ''  # Collection Title
        self.CIN = []  # Comment in
        self.CON = ''  # Comment on
        self.EIN = ''  # Erratum in
        self.EFR = ''  # Erratum for
        self.CRI = ''  # Corrected and Republished in
        self.CRF = ''  # Corrected and Republished from
        self.DDIN = ''  # Dataset described in
        self.DRIN = ''  # Dataset use reported in
        self.ECI = ''  # Expression Of ConcernIn
        self.ECF = ''  # Expression Of Concern For
        self.RPI = ''  # Republished in
        self.RPF = ''  # Republished from
        self.RIN = ''  # Retraction in
        self.ROF = ''  # Retraction of
        self.UIN = ''  # Update in
        self.UOF = ''  # Update of
        self.SPIN = ''  # Summary for patients in
        self.ORI = ''  # Original report in
        self.COI = ''  # Conflict of Interest
        self.CN = ''  # Corporate Author
        self.CRDT = ''  # Create Date
        self.DCOM = ''  # Date Completed
        self.DA = ''  # Date Created
        self.LR = ''  # Date Last Revised
        self.DEP = ''  # Date of Electronic Publication
        self.DP = ''  # Date of Publication
        self.EN = ''  # Edition
        self.ED = ''  # Editor Name
        self.FED = ''  # Full Editor Name
        self.EDAT = ''  # Entrez Date
        self.GS = ''  # Gene Symbol
        self.GN = ''  # General Note
        self.GR = []  # Grant Number
        self.IR = ''  # Investigator Name
        self.FIR = ''  # Full Investigator Name
        self.ISBN = ''  # ISBN
        self.IS = []  # ISSN
        self.IP = ''  # Issue
        self.TA = ''  # Journal Title Abbreviation
        self.JT = ''  # Journal Title
        self.LA = ''  # Language
        self.LID = []  # Location Identifier
        self.MID = ''  # Manuscript Identifier
        self.MHDA = ''  # MeSH Date
        self.MH = []  # MeSH Terms
        self.JID = ''  # NLM Unique ID
        self.RF = ''  # Number of References
        self.OAB = ''  # Other Abstract
        self.OCI = ''  # Other Copyright Information
        self.OID = []  # Other ID
        self.OT = []  # Other Term
        self.OTO = ''  # Other Term Owner
        self.OWN = ''  # Owner
        self.PG = ''  # Pagination
        self.PS = ''  # Personal Name as Subject
        self.FPS = ''  # Full Personal Name as Subject
        self.PL = ''  # Place of Publication
        self.PHST = []  # Publication History Status
        self.PST = ''  # Publication Status
        self.PT = []  # Publication Type
        self.PUBM = ''  # Publishing Model
        self.PMC = ''  # PubMed Central Identifier
        self.PMCR = ''  # PubMed Central Release
        self.PMID = ''  # PubMed Unique Identifier
        self.RN = []  # Registry Number/EC Number
        self.NM = ''  # Substance Name
        self.SI = ''  # Secondary Source ID
        self.SO = ''  # Source
        self.SFM = ''  # Space Flight Mission
        self.STAT = ''  # Status
        self.SB = []  # Subset
        self.TI = ''  # Title
        self.TT = ''  # Transliterated Title
        self.VI = ''  # Volume
        self.VTI = ''  # Volume Title
        # Custom Field
        self.cls = 'medline'
        self.reftype = 'medline'
        self.database = 'pubmed'
        self.srcfile = ''


def isdb(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as datafile:
        try:
            line = datafile.readline()
            line = datafile.readline()
            test_str_pmid = line[:4]
            if test_str_pmid != 'PMID':
                return False
        except UnicodeDecodeError:
            return False
    return True


def parsedata(datafile_path):
    data = []
    fields = ['FAU', 'AUID', 'RN', 'OT', 'OID', 'LID', 'AD',
            'PHST', 'AID', 'MH', 'SB', 'GS', 'CIN', 'IS',
            'AU', 'PT', 'GR']
    if isdb(datafile_path):
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
            data.append(dataitem) # Append last item
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
    datafile_path = './mrhpkg/filters/pubmed.txt'
    # Read Data
    data = getdata(datafile_path)
    print(len(data))
# endregion
