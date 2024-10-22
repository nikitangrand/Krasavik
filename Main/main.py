
import os
import sys
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)


        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Назад", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Наперад", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "Перазагрузіць", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Дадому", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        home_btn.triggered.connect(self.navigate_home)

        navtb.addSeparator()

        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-stop.png')), "Прыпынак", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        file_menu = self.menuBar().addMenu("&Меню")
        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "Новая ўкладка", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        help_menu = self.menuBar().addMenu("&Дапамога")
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),"Хатняя старонка", self)
        navigate_home_action.setStatusTip("Go to April Homepage")
        help_menu.addAction(navigate_home_action)
        navigate_home_action.triggered.connect(self.navigate_home)
        navigate_home_help = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')), "Інструкцыя", self)
        navigate_home_help.setStatusTip("Go to April Help")
        help_menu.addAction(navigate_home_help)
        navigate_home_help.triggered.connect(self.navigate_help)
        self.setWindowTitle("Красавік")
        self.setWindowIcon(QIcon(os.path.join('icons', 'original.png')))
        self.setStyleSheet("""QWidget{
           background-color: rgb(191, 51, 51);
           color: rgb(66, 25, 17);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(246, 143, 70);
            position: absolute;
            top: -0.5em;
            color: rgb(66, 25, 17);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(38, 166, 8);
            border: 2px solid rgb(152, 70, 53);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(66, 25, 17);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(64, 168, 40);
            border: 2px solid rgb(146, 69, 53);
            background-color: rgb(30, 125, 7);
        }

        QLineEdit {
            border: 2px solid rgb(231, 151, 134);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(204, 140, 127);
            color: rgb(66, 25, 17);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(255, 113, 0);
            color: rgb(94, 51, 51);
        }
        QPushButton{
            background: rgb(234, 111, 85);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")

        #url = http://www.google.com,
        #webbrowser.open('D:\bidowBrower\Site\main.html')
        self.add_new_tab(QUrl('https://iridescent-fairy-ecf671.netlify.app/'), 'Homepage')
        self.show()
 
    def add_new_tab(self, qurl=None, label="Новы ліст"):
        if qurl is None:
            qurl = QUrl('https://iridescent-fairy-ecf671.netlify.app/')#pass empty string to url

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
    
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  
            self.add_new_tab()
 
    def close_current_tab(self, i):
        if self.tabs.count() < 2: 
            return

        self.tabs.removeTab(i)

    
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            return
        # URL Schema
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)



    def current_tab_changed(self, i):
        # i = tab index
        # GET CURRENT TAB URL
        qurl = self.tabs.currentWidget().url()
        # UPDATE URL TEXT
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # UPDATE WINDOWS TITTLE
        self.update_title(self.tabs.currentWidget())


    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)


    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)


    def navigate_home(self):
        #self.tabs.currentWidget().setUrl('https://iridescent-fairy-ecf671.netlify.app/')
        self.add_new_tab(QUrl('https://iridescent-fairy-ecf671.netlify.app/'), 'Хатняя старонка')
        self.show()

    def navigate_help(self):
        #self.tabs.currentWidget().setUrl('https://iridescent-fairy-ecf671.netlify.app/')
        self.add_new_tab(QUrl('https://delightful-rolypoly-2e2e08.netlify.app/'), 'Дапамога')
        self.show()



app = QApplication(sys.argv)
app.setApplicationName("Красавік")
app.setOrganizationName("Bidow")
app.setOrganizationDomain("AprilBi.org")


window = MainWindow()
app.exec_()
