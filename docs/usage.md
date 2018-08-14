# 使用方法

## 快速入门

  - Step 1  
    将以下（全部或单独）数据文件置于在程序所在 **data目录**

  - Web of Science  
    Core Database -\> Search -\> Save to other format -\> All Records
    and References -\> Download

  - Pubmed  
    Search -\> Sent to -\> File -\> Format(MEDLINE) -\> Create File -\>
    Download

  - Wanfang  
    检索 -\> 全选 -\> 全选 -\> 全选 -\> 全选 -\> ... -\> 导出 -\> NoteExpress -\> 下载

  - CNKI  
    检索 -\> 全选 -\> 全选 -\> 全选 -\> 全选 -\> ... -\> 导出 -\> CNKI E-Study -\>
    下载

  - Step 2  
    运行 **mrhelper.exe**

  - Step 3  
    在 **阅读** 界面阅读并标记文献

  - Step 4  
    在 **整理** 界面调整分组及文献顺序

  - Step 5  
    在 **导出** 界面设置导出综述文档及数据文件

  - Step 6  
    使用 **Endnote** 新建数据库并以 **Endnote Import-Import All-Unicode (UTF-8)**
    导入save目录下数据文件 **endnote.txt**

  - Step 7  
    设置ENDNOTE -\> Edit -\> Preferences -\> Temporary Citation -\> Use
    Field (勾选) -\> Label

  - Step 8  
    使用 **Word** 打开save目录下综述文档 **reference.docx**，在Endnote栏下将Instant
    Formatting is **Off** 更改为 **On**

  - Step 9  
    **保存** 综述文档

## 启动

  -   - 启动mrhelper.exe后，程序将自动创建一下目录：
        
          - ./data/ 用于放置从Web of Science Core Collection, Pubmed, CNKI,
            万方下载得到的文件
          - ./save/
            存放项目存档mrhelper.save和程序界面执行导出后得到的.docx文档及用于导入ENDNOTE的数据文件
          - ./log/ 记录项目运行异常

## 抓取数据

  - Web of Science: 无需抓取

  -   - Pubmed: 通过PMID得到文献在PMC中的相关信息
        
          - 说明文档：https://www.ncbi.nlm.nih.gov/books/NBK25497/
          - 网址遵循：https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
          - api\_key: 注册Pubmed-NCBI可得到api\_key 10 r/s

  -   - CNKI: 通过link得到文献页面及相关文献
        
          - RefType 1: 参考文献
          - RefType 3: 引证文献

  - 万方: 通过link得到文献页面及相关文献

## 模板说明

  - mrhelper.docx
  - 标题 1 - 16：中文 微软雅黑；西文 Cambria；加粗；居中；间距 段前18磅 段后18磅 单倍行距；
  - 标题 2 - 14；中文 微软雅黑；西文 Cambria；加粗；左对齐；间距 段前18磅 段后18磅 单倍行距；
  - 标题 3 - 12；中文 微软雅黑；西文 Cambria；加粗；左对齐；间距 段前18磅 段后18磅 单倍行距；
  - 标题 4 - 10.5；中文 微软雅黑；西文 Cambria；加粗；左对齐；间距 段前18磅 段后18磅 单倍行距；
  - 正文 - 10.5；中文 微软雅黑；西文 Cambria；间距 段前18磅 段后18磅 单倍行距；
  - 纸张大小：A4
  - 页边距：中等
  - 软件：Office 2016 - Word
