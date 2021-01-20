#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Medical Review Helper
~~~~~~~~~~~~~~~~~~~~~

:mrhgui: GUI Module
:copyright: (c) 2018 by Dearfad
:Email: dearfad@sina.com
:license: GPL-v3
"""

import sys

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QTreeWidget
from PyQt5.QtWidgets import QLineEdit, QLabel, QPlainTextEdit, QCheckBox, QPushButton
from PyQt5.QtWidgets import QTextEdit, QAbstractItemView, QGroupBox, QSplitter
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QCompleter


# noinspection PyArgumentList
class MrhMainWindow(QMainWindow):
    """Main Window."""

    def __init__(self):
        super().__init__()
        self.menuBar()
        self.maintabwidget = MrhTabWidget()
        self.maintabwidget.setObjectName('main_tab')
        self.setCentralWidget(self.maintabwidget)
        self.statusBar()


class MrhTabWidget(QTabWidget):
    """Main TabWidget."""

    def __init__(self):
        super().__init__()
        self.tab_read = MrhReadWidget()
        self.tab_classify = MrhClassifyWidget()
        self.tab_export = MrhExportWidget()
        self.tab_help = MrhHelpWidget()
        self.tab_about = MrhAboutWidget()
        self.tab_config = MrhConfigWidget()
        self.addTab(self.tab_read, '阅读')
        self.addTab(self.tab_classify, '整理')
        self.addTab(self.tab_export, '导出')
        self.addTab(self.tab_help, '帮助')
        self.addTab(self.tab_about, '关于')
        self.addTab(self.tab_config, '设置')


# noinspection PyArgumentList
class MrhReadWidget(QWidget):
    """Tab READ."""

    def __init__(self):
        super().__init__()
        self.datatable = MrhReadTable()
        self.datatable.setObjectName('read_datatable')
        self.viewoptiongroup = MrhReadViewGroupbox()
        self.viewoptiongroup.setObjectName('read_viewoption')
        self.info_textedit = QTextEdit()
        self.info_textedit.setObjectName('read_info_textedit')
        self.functiongroup = MrhReadFunctionGroupbox()
        self.functiongroup.setObjectName('read_functiongroup')
        self.memooptiongroup = MrhReferenceMemoGroupbox()
        self.memooptiongroup.setObjectName('read_memooption')
        self.vlayout = QVBoxLayout()
        self.splitter = QSplitter()
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.datatable)
        self.splitter.addWidget(self.info_textedit)
        self.splitter.addWidget(self.memooptiongroup)
        self.vlayout.addWidget(self.splitter)
        self.vlayout.addWidget(self.viewoptiongroup)
        self.vlayout.addWidget(self.functiongroup)
        self.setLayout(self.vlayout)


class MrhReadTable(QTableWidget):
    """Tab READ: DATATABLE."""

    def __init__(self):
        super().__init__()
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # Table NOT Editable
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Choose Entire Line
        self.horizontalHeader().setStretchLastSection(True)  # Stretch Last Section
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Allow Custom Context Menu
        self.verticalHeader().setObjectName('read_table_vheader')
        self.horizontalHeader().setObjectName('read_table_hheader')


# noinspection PyArgumentList
class MrhReadViewGroupbox(QGroupBox):
    """Tab READ: View Options."""

    def __init__(self):
        super().__init__()
        self.setTitle('View Options')
        self.use_checkbox = QCheckBox('USE')
        self.use_checkbox.setObjectName('read_view_option_use')
        self.use_checkbox.setTristate()
        self.use_checkbox.setCheckState(Qt.PartiallyChecked)
        self.abstract_checkbox = QCheckBox('Abstract')
        self.abstract_checkbox.setObjectName('read_view_option_abstract')
        self.abstract_checkbox.setTristate()
        self.abstract_checkbox.setCheckState(Qt.PartiallyChecked)
        self.fiveyears_checkbox = QCheckBox('Year')
        self.fiveyears_checkbox.setObjectName('read_view_option_year')
        self.fiveyears_checkbox.setTristate()
        self.fiveyears_checkbox.setCheckState(Qt.PartiallyChecked)
        self.type_checkbox = QCheckBox('Type')
        self.type_checkbox.setObjectName('read_view_option_type')
        self.type_checkbox.setTristate()
        self.type_checkbox.setCheckState(Qt.PartiallyChecked)
        self.search_label = QLabel('Search: ')
        self.search_label.setObjectName('read_view_option_search_label')
        self.search_lineedit = QLineEdit()
        self.search_lineedit.setObjectName('read_view_option_search_lineedit')
        self.relate_checkbox = QCheckBox('Relate')
        self.relate_checkbox.setObjectName('read_view_option_relate')
        self.relate_checkbox.setCheckState(Qt.Unchecked)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.use_checkbox)
        self.hlayout.addWidget(self.abstract_checkbox)
        self.hlayout.addWidget(self.fiveyears_checkbox)
        self.hlayout.addWidget(self.type_checkbox)
        self.hlayout.addWidget(self.search_label)
        self.hlayout.addWidget(self.search_lineedit)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.relate_checkbox)
        self.setLayout(self.hlayout)


# noinspection PyArgumentList
class MrhReadFunctionGroupbox(QGroupBox):
    """Tab READ: Function Group."""

    def __init__(self):
        super().__init__()
        self.setTitle('Function Group')
        self.info_button = QPushButton('Info')
        self.info_button.setObjectName('read_functiongroup_info')
        self.view_button = QPushButton('View')
        self.view_button.setObjectName('read_functiongroup_view')
        self.memo_button = QPushButton('Memo')
        self.memo_button.setObjectName('read_functiongroup_memo')
        self.openbrowser_button = QPushButton('WebPage')
        self.openbrowser_button.setObjectName('read_functiongroup_webpage')
        self.fulltext_button = QPushButton('FullText')
        self.fulltext_button.setObjectName('read_functiongroup_fulltext')
        self.citeref_button = QPushButton('References')
        self.citeref_button.setObjectName('read_functiongroup_references')
        self.new_button = QPushButton('New')
        self.new_button.setObjectName('read_functiongroup_new')
        self.open_button = QPushButton('Open')
        self.open_button.setObjectName('read_functiongroup_open')
        self.add_button = QPushButton('Add')
        self.add_button.setObjectName('read_functiongroup_add')
        self.save_button = QPushButton('Save')
        self.save_button.setObjectName('read_functiongroup_save')
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.info_button)
        self.hlayout.addWidget(self.view_button)
        self.hlayout.addWidget(self.memo_button)
        self.hlayout.addWidget(self.openbrowser_button)
        self.hlayout.addWidget(self.fulltext_button)
        self.hlayout.addWidget(self.citeref_button)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.new_button)
        self.hlayout.addWidget(self.open_button)
        self.hlayout.addWidget(self.add_button)
        self.hlayout.addWidget(self.save_button)
        self.setLayout(self.hlayout)


# noinspection PyArgumentList
class MrhReferenceMemoGroupbox(QGroupBox):
    """Tab READ: Memo Group."""

    def __init__(self):
        super().__init__()
        self.setTitle('Memo Options')
        self.keywords_label = QLabel('Keywords: ')
        self.keywords_label.setObjectName('read_memo_option_keywords')
        self.iv_label = QLabel('IV:')
        self.iv_label.setObjectName('read_memo_option_iv_label')
        self.iv_lineedit = QLineEdit()
        self.iv_lineedit.setObjectName('read_memo_option_iv_lineedit')
        self.iv_completer = QCompleter()
        self.iv_list_model = QStringListModel()
        self.iv_completer.setModel(self.iv_list_model)
        self.iv_lineedit.setCompleter(self.iv_completer)
        self.relation_checkbox = QCheckBox('relation')
        self.relation_checkbox.setObjectName('read_memo_option_relation')
        self.relation_checkbox.setTristate()
        self.dv_label = QLabel('DV:')
        self.dv_label.setObjectName('read_memo_option_dv_label')
        self.dv_lineedit = QLineEdit()
        self.dv_lineedit.setObjectName('read_memo_option_dv_lineedit')
        self.dv_completer = QCompleter()
        self.dv_list_model = QStringListModel()
        self.dv_completer.setModel(self.dv_list_model)
        self.dv_lineedit.setCompleter(self.dv_completer)
        self.group_label = QLabel('Group:')
        self.group_label.setObjectName('read_memo_option_group')
        self.group_lineedit = QLineEdit()
        self.group_lineedit.setObjectName('read_memo_option_group_lineedit')
        self.group_list_model = QStringListModel()
        self.group_completer = QCompleter()
        self.group_completer.setModel(self.group_list_model)
        self.group_lineedit.setCompleter(self.group_completer)
        self.subgroup_lineedit = QLineEdit()
        self.subgroup_lineedit.setObjectName('read_memo_option_subgroup')
        self.subgroup_list_model = QStringListModel()
        self.subgroup_lineedit.setDisabled(True)
        self.subgroup_completer = QCompleter()
        self.subgroup_completer.setModel(self.subgroup_list_model)
        self.subgroup_lineedit.setCompleter(self.subgroup_completer)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.iv_label)
        self.hlayout.addWidget(self.iv_lineedit)
        self.hlayout.addWidget(self.relation_checkbox)
        self.hlayout.addWidget(self.dv_label)
        self.hlayout.addWidget(self.dv_lineedit)
        self.hlayout.addWidget(self.group_label)
        self.hlayout.addWidget(self.group_lineedit)
        self.hlayout.addWidget(self.subgroup_lineedit)
        self.memo_label = QLabel('Description')
        self.memo_label.setObjectName('read_memo_option_description')
        self.reftext_textedit = QPlainTextEdit()
        self.reftext_textedit.setObjectName('read_memo_option_reftext')
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.keywords_label)
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(self.memo_label)
        self.vlayout.addWidget(self.reftext_textedit)
        self.setLayout(self.vlayout)


# noinspection PyArgumentList
class MrhClassifyWidget(QWidget):
    """Tab Classify."""

    def __init__(self):
        super().__init__()
        self.treelist = MrhClassifyTree()
        self.treelist.setObjectName('classify_treelist')
        self.info_textedit = QTextEdit()
        self.info_textedit.setObjectName('classify_info_textedit')
        self.memooptiongroup = MrhReferenceMemoGroupbox()
        self.memooptiongroup.setObjectName('classify_memooption')
        self.functiongroup = MrhClassifyFunctionGroupbox()
        self.functiongroup.setObjectName('classify_functiongroup')
        self.vlayout = QVBoxLayout()
        self.splitter = QSplitter()
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.treelist)
        self.splitter.addWidget(self.info_textedit)
        self.splitter.addWidget(self.memooptiongroup)
        self.vlayout.addWidget(self.splitter)
        self.vlayout.addWidget(self.functiongroup)
        self.setLayout(self.vlayout)


# noinspection PyArgumentList
class MrhClassifyTree(QTreeWidget):
    """Tab Classify: TreeWidget."""

    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.header().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setColumnCount(6)
        self.setHeaderLabels(['Tag', 'ID', 'RID', 'Group', 'SubGroup', 'Title'])
        columnwidth = [180, 50, 50, 90, 90]
        for index, width in enumerate(columnwidth):
            self.setColumnWidth(index, width)
            self.headerItem().setTextAlignment(index, Qt.AlignHCenter | Qt.AlignVCenter)
        self.headerItem().setTextAlignment(5, Qt.AlignHCenter | Qt.AlignVCenter)


# noinspection PyArgumentList
class MrhClassifyFunctionGroupbox(QGroupBox):
    """Tab Classify: Function Group."""

    def __init__(self):
        super().__init__()
        self.setTitle('Function Group')
        self.info_button = QPushButton('Info')
        self.info_button.setObjectName('classify_functiongroup_info')
        self.memo_button = QPushButton('Memo')
        self.memo_button.setObjectName('classify_functiongroup_memo')
        self.openbrowser_button = QPushButton('WebPage')
        self.openbrowser_button.setObjectName('classify_functiongroup_webpage')
        self.fulltext_button = QPushButton('FullText')
        self.fulltext_button.setObjectName('classify_functiongroup_fulltext')
        self.genseq_button = QPushButton('GenSeq')
        self.genseq_button.setObjectName('classify_genseq_button')
        self.save_button = QPushButton('Save')
        self.save_button.setObjectName('classify_save_button')
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.info_button)
        self.hlayout.addWidget(self.memo_button)
        self.hlayout.addWidget(self.openbrowser_button)
        self.hlayout.addWidget(self.fulltext_button)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.genseq_button)
        self.hlayout.addWidget(self.save_button)
        self.setLayout(self.hlayout)


# noinspection PyArgumentList
class MrhExportWidget(QWidget):
    """Tab EXPORT."""

    def __init__(self):
        super().__init__()
        self.formlayout = QFormLayout()
        self.export_button = QPushButton('Export')
        self.export_button.setObjectName('export_export_button')
        self.save_button = QPushButton('Save')
        self.save_button.setObjectName('export_save_button')
        self.opendata_button = QPushButton('Open Data Folder')
        self.opendata_button.setObjectName('export_open_data_button')
        self.title_lineedit = QLineEdit()
        self.title_lineedit.setObjectName('export_title_linedit')
        self.author_lineedit = QLineEdit()
        self.author_lineedit.setObjectName('export_author_linedit')
        self.abstract_lineedit = QLineEdit()
        self.abstract_lineedit.setObjectName('export_abstract_linedit')
        self.keywords_lineedit = QLineEdit()
        self.keywords_lineedit.setObjectName('export_keywords_linedit')
        self.formlayout.addRow(self.export_button)
        self.formlayout.addRow(self.save_button)
        self.formlayout.addRow(self.opendata_button)
        self.formlayout.addRow('Title: ', self.title_lineedit)
        self.formlayout.addRow('Author: ', self.author_lineedit)
        self.formlayout.addRow('Abstract: ', self.abstract_lineedit)
        self.formlayout.addRow('Keywords: ', self.keywords_lineedit)
        self.setLayout(self.formlayout)


# noinspection PyArgumentList
class MrhHelpWidget(QWidget):
    """Tab HELP."""

    def __init__(self):
        super().__init__()
        self.help_textedit = QTextEdit()
        self.help_textedit.setObjectName('help_help_textedit')
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.help_textedit)
        self.setLayout(self.hlayout)


# noinspection PyArgumentList
class MrhAboutWidget(QWidget):
    """Tab ABOUT."""

    def __init__(self):
        super().__init__()
        self.about_textedit = QTextEdit()
        self.about_textedit.setObjectName('about_about_textedit')
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.about_textedit)
        self.setLayout(self.hlayout)

class MrhConfigWidget(QWidget):
    """Tab Config."""

    def __init__(self):
        super().__init__()
        self.formlayout = QFormLayout()

        self.save_button = QPushButton('Save Config')
        self.save_button.setObjectName('config_save_button')

        self.scihub_label = QLabel('Scihub')
        self.scihub_label.setObjectName('config_scihub_label')

        self.scihuburl_lineedit = QLineEdit()
        self.scihuburl_lineedit.setObjectName('config_scihuburl_linedit')

        self.formlayout.addRow(self.save_button)
        self.formlayout.addRow(self.scihub_label)
        self.formlayout.addRow('url: ', self.scihuburl_lineedit)

        self.setLayout(self.formlayout)

def main():
    """Show GUI."""
    app = QApplication(sys.argv)
    mainwindow = MrhMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
