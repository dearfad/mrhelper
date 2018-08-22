# 参考文献格式

## MrhData字段转换表

**最后更新**: 2018.05.30

|MrhData|Endnote|Web Of Science|Pubmed|万方|CNKI|
|-|-|-|-|-|-|
|author|%A|AU|AU|Author|Author|
|title|%T|TI|TI|Title|Title|
|type|%0|DT|PT|ReferenceType|DataType|
|journal|%J|SO|JT|Journal|Source|
|year|%D|PY|DP|Year|Year|
|volumn|%V|VL|VI||Roll|
|issue|%N|IS|IP|Issue|Period|
|page|%P|BP-EP|PG|Pages|Page|
|link|%U|||URL|Link|
|doi|%R|DI|AID|DOI||
|pmid|%M|PM|PMID|||
|pmcid|||PMC|||
|abstract|%X|AB|AB|Abstract|Summary|
|cs||TC||||
|cr||NR||||
|lcr||LCR||||
|lcs||LCS||||
|keywords|%K|DE|OT|Keywords|Keyword|

## GB/T 7714-2015 参考文献著录规则

* GB/T 7714-2015 信息与文献 参考文献著录规则
* Information and documentation - Rules for bibliographic references and citations to information resources
* 百度文库：[在线阅读](https://wenku.baidu.com/view/bd63e138f121dd36a32d82cb.html)

## ENDNOTE-PUBMED 字段对照表

* Filters From EndNote X8.2
* Pubmed Import Filter
* Reference Type: **Journal Article**
* Last modified: 2017.04.14 0:08:34

|Tag|Field(s)|
|-|-|
|PT|'JOURNAL ARTICLE'|
|PT|'Journal Article'|
|PT|'Journal'|
|PT|'JOURNAL'|
|AB|Abstract|
|AD|Author Address|
|AID|{IGNORE} '[pii]'|
|AID|DOI '[doi]'|
|AU|Author|
|AUID|Notes|
|CDAT|{IGNORE}|
|CI|{IGNORE}|
|CN|Notes|
|CRDT|{IGNORE}|
|CY|{IGNORE}|
|DA|{IGNORE}|
|DCOM|{IGNORE}|
|DEP|{IGNORE}|
|DP|Year Date|
|DP|Year|
|EDAT|Epub Date 0{IGNORE}|
|EDAT|Epub Date 1{IGNORE}|
|EDAT|Epub Date|
|FAU|Notes|
|GR|Notes|
|IP|Issue|
|IS|Notes (Electronic)|
|IS|ISSN (Linking)|
|IS|ISSN|
|JC|{IGNORE}|
|JID|{IGNORE}|
|JT|Alternate Journal|
|LA|Language|
|LID|{IGNORE}'[pii]'|
|LID|DOI '[doi]'|
|LR|{IGNORE}|
|MH|Keywords|
|MHDA|{IGNORE}|
|MID|NIHMSID|
|OT|Keywords|
|OTO|{IGNORE}|
|OWN|Database Provider|
|PG|Pages|
|PHST|{IGNORE}|
|PL|Notes|
|PMC|PMCID|
|PMID|Accession Number|
|PST|{IGNORE}|
|PT|Notes|
|PUBM|{IGNORE}|
|RN|{IGNORE}|
|SB|{IGNORE}|
|SO|Notes|
|STAT|{IGNORE}|
|TA|Journal|
|TI|Title|
|TT|Original Publication|
|VI|Volume|
|UI|{IGNORE}|
|URL|URL|
|URLF|URL|
|URLS|URL|
|4099|URL|
|4100|URL|
|OAB|Abstract|
|OABL|Abstract|

## Endnote-Endnote 字段对照表

* EndNote X8.2
* Reference Type: **Journal Article**
* Last modified: 2017.04.14 0:08:38

!!! warning
    * **Comments and limitations**
        * This filter is designed to import text files that have been downloaded from online databases or exported from EndNote (version 8 and above) using the EndNote format.
    * **LIMITATIONS**
        * Since only "plain text" files can be imported into EndNote, this filter cannot be used to import images, graphics, &c.
        * Before importing, corporate authors must end in a comma or EndNote will not be able to distinguish them from personal authors and will therefore parse them incorrectly.

|Tag|Field(s)|
|-|-|
|%0|'Journal Article'|
|%A|Author|
|%B|Journal|
|%C|{IGNORE}|
|%D|Year|
|%E|{IGNORE}|
|%F|Label|
|%f|Figure|
|%G|Language|
|%H|Translated Author|
|%I|{IGNORE}|
|%J|Journal|
|%K|Keywords|
|%L|Call Number|
|%M|Accession Number|
|%N|Issue|
|%O|Alternate Journal|
|%P|Pages|
|%Q|Translated Title|
|%R|DOI|
|%S|{IGNORE}|
|%T|Title|
|%U|URL|
|%V|Volume|
|%W|Database Provider|
|%X|Abstract|
|%Y|{IGNORE}|
|%Z|Notes|
|%1|Legal Note|
|%2|PMCID|
|%3|{IGNORE}|
|%4|{IGNORE}|
|%6|{IGNORE}|
|%7|Epub Date|
|%8|Date|
|%9|Type of Article|
|%?|{IGNORE}|
|%@|ISSN|
|%!|Short Title|
|%#|{IGNORE}|
|%$|NIHMSID|
|%]|Article Number|
|%&|Start Page|
|%(|Original Publication|
|%)|Reprint Edition|
|%*|Reviewed Item|
|%+|Author Address|
|%f|Notes|
|%^|Caption|
|%>|File Attachments|
|%<|Research Notes|
|%[|Access Date|
|%=|{IGNORE}|
|%~|Name of Database|

## Web of Science Core Collection Import Filter

* Reference Type: **Journal Article**
* Last modified: 2017.04.14 0:08:32

!!! warning
    * **DOWNLOADING INSTRUCTIONS**
        1. Perform a WoS or DCI search as normal.
        2. Select the desired articles by clicking the button to the left of each article and add them to the Marked List.
        3. Go to the "Marked List" page by selecting the "Marked List" button under “Thomson Reuters.”
        4. On the "Marked List" page, near the bottom where all the exportable fields are shown, select "Select All."
        5. On the "Marked List" page confirm your selection and select the option to "Save to Other File Formats."
        6. Import the resulting "savedrecs.txt" file using this filter.
    * **LIMITATIONS**
        1. The author address may be presented twice, once with the street address and once without.  Users may manually delete the duplicated information manually after importing.
        2. The publisher's city may be presented without the state, which must be typed in manually after importing if desired.  Sometimes, even the city must be gleaned from the Notes field.
        3. Certain author names must be edited after importing.  The name "OBryen" for example will import as "Obryen" (note lower-case second letter).  Since the apostrophe wasn't supplied in the first place, one must provide it manually, thus "O'Bryen".
        4. Patent application and publication dates are presented with extraneous information, which must be deleted after importing.  In addtion, the year must be moved from the Patent Date field to the Year field manually.
        5. If you are using EndNote 8, the language code for patents is imported into the Language field.  In earlier versions, it is imported into the Patent Date field along with the pages; both pages and language code must be manually moved to their appropriate fields after importing.  (If you have EndNote 7 or earlier, you may edit this filter, changing the 'Language' to 'Notes' in the PD tag of the Patent template.)
        6. If you are using direct export and depending on which database you downloaded patents from, the issue date may in fact be the issue number of the journal in which the patent was published.

|Tag|Field(s)|
|-|-|
|PT|'J'|
|AB|Abstract|
|AR|Notes|
|AU|Author|
|BD|Keywords|
|BN|Notes|
|BP|Pages|
|BS|Notes|
|CC|Keywords|
|CH|Keywords|
|CN|Keywords|
|CO|{IGNORE}|
|CP|Notes|
|CR|{IGNORE}|
|C1|Author Address|
|CL|Notes|
|CP|{IGNORE}|
|CR|{IGNORE}|
|CT|Notes|
|CY|Notes|
|DE|Keywords|
|DI|DOI|
|DF|{IGNORE}|
|DT|Type of Article|
|DV|{IGNORE}|
|EM|Author Address|
|EP|Pages|
|FN|{IGNORE}|
|FO|Keywords|
|FT|Notes|
|FU|Notes|
|GA|{IGNORE}|
|GE|Keywords|
|ID|Keywords|
|IS|Issue|
|J9|{IGNORE}|
|JI|Alternate Journal (Notes)|
|JI|Alternate Journal|
|KC|Keywords|
|LA|Language|
|LS|Notes|
|MC|Keywords|
|ME|{IGNORE}|
|MQ|Keywords|
|NR|{IGNORE}|
|OR|Keywords|
|PA|{IGNORE}|
|PD|Date|, Year|
|PD|Date| Year|
|PD|Date|
|PG|{IGNORE}|
|PI|{IGNORE}|
|PN|Notes|
|PO|Keywords|
|PR|Keywords|
|PS|Pages|
|PT|{IGNORE}|
|PU|{IGNORE}|
|PV|{IGNORE}|
|PY|Year|
|RD|{IGNORE}|
|RP|Author Address|
|SC|{IGNORE}|
|SI|Notes|
|SN|ISSN|
|SO|Journal|
|SP|Notes|
|SS|Keywords|
|SU|Notes|
|TA|Keywords|
|TC|{IGNORE}|
|TI|Title|
|TM|Keywords|
|UT|Accession Number|
|VL|vol.Volume, no.Issue|
|VL|no.Issue|
|VL|vol.Volume|
|VL|Volume|
|VR|{IGNORE}|
|WP|URL|
|Z9|Notes|
|PM|Notes|
