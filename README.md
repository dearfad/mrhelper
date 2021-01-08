# MrHelper

![GitHub (pre-)release](https://img.shields.io/github/release/dearfad/mrhelper/all.svg?style=plastic)

* **MrHelper**：**M**edical **R**eriew **H**elper
* 是一个用于**整理标注参考文献**、**快速创建医学综述初稿**的WORD文档及ENDNOTE参考文献生成器。

## 特色

* 使用**Web Of Science**, **Pubmed**, **CNKI**, **万方**数据库文献导出文件
* 便捷查看文献网页、全文、是否核心/SCI文献
* **CS/LCS/CR/LCR** 相关文献显示
* 导出生成含有ENDNOTE临时引文的WORD综述初稿

## 使用方法

* 快速入门 - [链接](https://dearfad.github.io/mrhelper/quickstart)
* 帮助文档 - [链接](https://dearfad.github.io/mrhelper)
* 解压后执行 **mrhelper.exe**

## 源码执行：

* **mrhelper.py**
* 安装 python 3
* 安装依赖库
    ```python
    pip install -r requirements.txt
    ```

## 依赖库

* [Python](https://www.python.org) - 编程语言
* [python-docx](https://python-docx.readthedocs.io) - 生成综述WORD文稿
* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) - (GPL) 程序界面
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 解析抓取的文献页面
* [requests/requests[socks]](http://www.python-requests.org) - Pubmed, CNKI, 万方文献页面抓取
* [Pyinstaller](http://www.pyinstaller.org/) - 打包可执行程序文件（.exe）

* 可选装
    - [mkdocs](https://www.mkdocs.org/) 网站文档生成
    - [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) 网站material模板
    - [pymdown-extensions](https://squidfunk.github.io/mkdocs-material/extensions/pymdown/) material模板Markdown支持
    - [pylint](https://www.pylint.org/) Python代码分析
    - [autopep8](https://github.com/hhatto/autopep8) Python PEP8 格式化代码
    
## 贡献

* 请参阅 [CONTRIBUTING.md](https://github.com/dearfad/MrHelper/blob/master/docs/CONTRIBUTING.md)

## 版本

* 使用 [SemVer](http://semver.org/)

## 作者

* [**dearfad**](https://github.com/dearfad)

## 版权

* 本项目遵循 GPLv3 License - 参阅 [LICENSE](https://github.com/dearfad/MrHelper/blob/master/LICENSE)

## 行为规范

* 请参阅[行为规范](https://github.com/dearfad/MrHelper/blob/master/docs/CODE_OF_CONDUCT.md)

## 致谢

* 所有本软件的使用者
