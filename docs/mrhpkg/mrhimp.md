# **MRHIMP.PY**

* 导入数据文件，并将其转换为mrhitem格式，返回mrhdata和rawdata.

---

## **MrhData字段转换表**

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

## **转换字段修正说明**

### **WOS**

* 页码 `[BP, EP] -> "BP-EP"`

### **PUBMED**

* 出版年：取前四位数字`mrhitem.year = mrhitem.year[:4]`
* DOI：提取包含`[doi]`字符串为DOI，舍弃`[pii]`
* 期刊名：转换为全部大写以便于对照SCI目录

### **CNKI**

* 链接：
    1. 转换`'/kns/' -> '/kcms/'`
    2. 转换`'nvsm.cnki.net' -> 'kns.cnki.net'`
* 类型：
    1. `rawitem.type == '1': mrhitem.type = 'Journal Article'`

### **万方**
