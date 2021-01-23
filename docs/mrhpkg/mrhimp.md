# **MRHIMP.PY**

* 导入数据文件，并将其转换为mrhitem格式，返回mrhdata和rawdata.

---

## **MrhData字段转换表**

|MrhData|Endnote|Web Of Science|Pubmed|万方|CNKI|
|-|-|-|-|-|-|
|author|%A|AU|AU|Author|Author-作者|
|title|%T|TI|TI|Title|Title-题名|
|type|%0|DT|PT|ReferenceType|DataType|
|journal|%J|SO|JT|Journal|Source-刊名|
|year|%D|PY|DP|Year|Year-年|
|volumn|%V|VL|VI||Roll-卷|
|issue|%N|IS|IP|Issue|Period-期|
|page|%P|BP-EP|PG|Pages|Page-页码|
|link|%U|||URL|Link-链接|
|doi|%R|DI|AID|DOI||
|pmid|%M|PM|PMID|||
|pmcid|||PMC|||
|abstract|%X|AB|AB|Abstract|Summary-摘要|
|cs||TC||||
|cr||NR||||
|lcr||LCR||||
|lcs||LCS||||
|keywords|%K|DE|OT|Keywords|Keyword-关键词|

## **转换字段修正说明**

### **WOS**

* 页码 `[BP, EP] -> "BP-EP"`

### **PUBMED**

* 出版年：取前四位数字`mrhitem.year = mrhitem.year[:4]`
* DOI：提取包含`[doi]`字符串为DOI，舍弃`[pii]`
* 期刊名：转换为全部大写以便于对照SCI目录

### **CNKI**

* 类型：
    1. `rawitem.type == '1': mrhitem.type = 'Journal Article'`

### **万方**
