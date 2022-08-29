# PyQt5 Media player
#code by kevin
__author__ = "Kevin Chan"
__copyright__ = "Copyright (C) 2022 Kevin Chan"
__license__ = "GPL-3.0"
__version__ = "0.1.0"

import os, sys, random, csv
import datetime
from multiprocessing import shared_memory
key = "SQMediaPlayer"
instance = 1
try:
    single = shared_memory.SharedMemory(key, create=False)
    single.buf[0] = 0
except:
    instance = 0
if instance == 0:
    single = shared_memory.SharedMemory(key, create=True,size=1)
    single.buf[0] = 1
else:
    sys.exit("App is runing")

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget

ui_path = os.path.dirname(os.path.abspath(__file__))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"SQMedia.ui"))

class Star(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.loadMain)
        self.flash = QtCore.QTimer(self)
        self.flash.start(30)
        self.flash.timeout.connect(self.update)

        self.sec = 0
        self.line = 0
        self.star = 1000
        self.pointSize = 1
        self.sizeControl = -1

    def loadMain(self):
        if self.sec == 3 :
            self.main = Main()
            self.main.show()
            self.close()
            self.timer.stop()
            self.flash.stop()
        self.sec = self.sec+1
                
    def initUI(self):
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle('SQMedia Player')

        # change position to center of main display
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def paintEvent(self, event) -> None:
        qp = QtGui.QPainter()

        qp.begin(self)
        self.draw_points(event, qp)
        qp.end()

    def draw_points(self, event, qp):

        pen = QtGui.QPen(QtGui.QColor(255,random.randrange(255),80))
        pen.setWidth(self.pointSize)
        qp.setPen(pen)

        size = self.size()
        self.star = self.star - 10
        self.sizeControl = self.sizeControl * -1 
        self.pointSize = self.pointSize + 1 + self.sizeControl*3


        for i in range(self.star):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)
        self.line = self.line + 1 

        qp.setPen(QtGui.QPen(QtGui.QColor(255,127,80), self.line, QtCore.Qt.DashLine))

        gradient = QtGui.QLinearGradient(QtCore.QPoint(150, 50),QtCore.QPoint(200, 100))
        gradient.setColorAt(0,QtGui.QColor(184,134,11,110))
        gradient.setColorAt(1,QtGui.QColor(255,127,80,911))

        qp.setBrush(QtGui.QBrush(gradient))

        qp.drawEllipse(int(size.width()/4), int(size.height()/4), int(size.width()/2), int(size.height()/2))
        qp.setFont(QtGui.QFont("Arial", 16))
        qp.drawText(event.rect(),QtCore.Qt.AlignCenter,"SQMedia Player")

class Main(base_1, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        
        self.player = QMediaPlayer()
        
        self.videoWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoWidget)
        self.videoWidget.installEventFilter(self)
        

        # Layout
        self.setLayout(self.allinLayout)
        self.controlBox.setMinimumSize(451, 90)
        self.controlBox.setFixedHeight(5)
        self.groupBox_2.setFixedWidth(241)
        self.groupBox_2.setLayout(self.listbarLayout)

        self.videoWidget.setMinimumSize(451, 381)

    
        self.iconPage = QWidget()
        self.icon = QLabel()
        self.icon.setStyleSheet("background-image : url(:/Icon/Orange_SQMP.ico); background-repeat: no repeat; background-position: center;")
        self.iconlayout = QGridLayout()
        self.iconlayout.addWidget(self.icon)
        self.iconPage.setLayout(self.iconlayout)
        self.iconPage.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.795, y1:0.193182, x2:0.136182, y2:0.858, stop:0.125 rgba(58, 58, 58, 182), stop:1 rgba(108, 108, 108, 72));")
        self.videoLayout.addWidget(self.iconPage)

        self.videoWidget.hide()
        self.videoLayout.addWidget(self.videoWidget)

        self.listWidget.setWordWrap(True)


        self.scrollControl = False
        self.groupBox_2.hide()
        self.setWindowIcon(QtGui.QIcon(':/Icon/Orange_SQMP.ico'))

        # Player shortcut
        self.shortcutFull = QShortcut(self)
        self.shortcutFull.setKey(QtGui.QKeySequence('Ctrl+Shift+F'))
        self.shortcutFull.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.full_screen)

        self.shortcutExFu = QShortcut(self)
        self.shortcutExFu.setKey(QtGui.QKeySequence('Escape'))
        self.shortcutExFu.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutExFu.activated.connect(self.exc_fullScreen)

        self.shortcutPause = QShortcut(self)
        self.shortcutPause.setKey(QtGui.QKeySequence('Space'))
        self.shortcutPause.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutPause.activated.connect(self.media_pause)

        self.shortcutForward = QShortcut(self)
        self.shortcutForward.setKey(QtGui.QKeySequence('Right'))
        self.shortcutForward.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutForward.activated.connect(self.move_forward)

        self.shortcutBackward = QShortcut(self)
        self.shortcutBackward.setKey(QtGui.QKeySequence('Left'))
        self.shortcutBackward.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutBackward.activated.connect(self.move_backward)

        self.shortcutSkipNext = QShortcut(self)
        self.shortcutSkipNext.setKey(QtGui.QKeySequence('Shift+Right'))
        self.shortcutSkipNext.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutSkipNext.activated.connect(self.skip_forward)

        self.shortcutSkipReload = QShortcut(self)
        self.shortcutSkipReload.setKey(QtGui.QKeySequence('Shift+Left'))
        self.shortcutSkipReload.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutSkipReload.activated.connect(self.skip_backward)

        # Player control panel
        
        self.PlayButton.clicked.connect(self.media_play)
        self.pauseButton.clicked.connect(self.media_pause)
        self.muteButton.clicked.connect(self.volumeMute)
        self.Slider_player_volume.valueChanged.connect(self.volumeUpdate)
        self.Slider_player_volume.setValue(80)
        self.timeSlider.sliderReleased.connect(self.slider_moved)
        self.seekforwardButton.clicked.connect(self.move_forward)
        self.seekbackwardButton.clicked.connect(self.move_backward)
        self.addButton.clicked.connect(self.listAdd)
        self.delButton.clicked.connect(self.Media_del)
        self.listWidget.itemClicked.connect(self.Media_add)
        self.listWidget.itemDoubleClicked.connect(self.media_play)
        self.loopButton.clicked.connect(self.loop_control)
        self.looplistButton.clicked.connect(self.list_charge)
        self.skipbackwardButton.clicked.connect(self.skip_backward)
        self.skipforwardButton.clicked.connect(self.skip_forward)
        self.listcontrolButton.clicked.connect(self.list_control)
        self.scrollButton.clicked.connect(self.scroll_plane)
        self.fullscreenButton.clicked.connect(self.full_screen)
        self.topButton.clicked.connect(self.topWidget)

        # loop signal
        self.loop = 0
        self.listloop = 0




        # Media player signals
        self.player.stateChanged.connect(self.show_mediaState)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

        # Set Button Icon to QtStandardIcon

        self.scrollButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.looplistButton.setIcon(self.style().standardIcon(QStyle.SP_DriveCDIcon))
        self.addButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.delButton.setIcon(self.style().standardIcon(QStyle.SP_DialogDiscardButton))
        self.seekbackwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.seekforwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.skipbackwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.skipforwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))
        self.topButton.setIcon(QtGui.QIcon(':/image/Qui/image/normal.png'))

        # list media path and name
        self.mediaList = []
        self.mediaPath = []
        self.loadList()
        self.list_Media()

        # Icon change signal
        self.pause = 0
        self.ontop = 0

        # Block Button
        self.PlayButton.setEnabled(False)
        self.loopButton.setEnabled(False)
        self.listcontrolButton.setEnabled(False)

        #QTrayIcon
        QApplication.setQuitOnLastWindowClosed(False)

        icon = QtGui.QIcon(":/Icon/Orange_SQMP.ico")
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(icon)
        self.trayIcon.setVisible(True)

        self.trayIcon.activated.connect(self.onTrayIconActivated)

        menu = QMenu()

        self.mute = QAction("Mute", self)
        self.mute.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.mute.triggered.connect(self.volumeMute)
        menu.addAction(self.mute)
        
        pause = QAction("Pause",self)
        pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        pause.triggered.connect(self.media_pause)
        menu.addAction(pause)

        reload = QAction("Reload",self)
        reload.triggered.connect(self.skip_backward)
        reload.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        menu.addAction(reload)

        next = QAction("Next",self)
        next.triggered.connect(self.skip_forward)
        next.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        menu.addAction(next)
        
        quit = QAction("Quit",self)
        quit.triggered.connect(self.appQuit)
        quit.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        menu.addAction(quit)

        self.listMenu = QMenu()
        
        item1 = QAction("item1",self)
        item1.triggered.connect(lambda: print("menu item clicked"))



        self.trayIcon.setContextMenu(menu)

        self.anotherCall()

        self.controlBox.installEventFilter(self)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        pathText = event.mimeData().text()
        type = ['.avi','.mp4','.mkv','.mov','.wmv','.flv']        
        for n, filtration in enumerate( (event.mimeData().text()).split('\n') ):
            if filtration != '' and (os.path.splitext(filtration)[-1] in type):
                self.mediaPath.append(filtration.replace('file:///', ''))
                self.mediaList.append(os.path.basename(filtration.replace('file:///', '')))
        self.list_Media()

    def loadList(self):
        if os.path.exists('filelist.lmnop') == True:
            with open('filelist.lmnop', 'r') as file:
                reader = csv.reader(file)
                for  n, row in enumerate(reader):
                    if n == 0:
                        self.mediaList = row
                    if n == 2:
                        self.mediaPath = row

    def listMenu_onRightClicked(self):
        
        position = self.videoWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(position)
        self.listMenu.show()

    def anotherCall(self):
        cTimer = QtCore.QTimer(self)
        cTimer.start(1000)
        cTimer.timeout.connect(self.checkNew)

    def checkNew(self):
        if single.buf[0] == 0:
            self.show()
            single.buf[0] = 1
    
    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.hide()
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def appQuit(self):
        with open("filelist.lmnop", "w") as File:
            csv.writer(File, delimiter=',', quotechar='"', quoting= csv.QUOTE_MINIMAL).writerow(self.mediaList)
            csv.writer(File, delimiter=',', quotechar='"', quoting= csv.QUOTE_MINIMAL).writerow(self.mediaPath)

        sys.exit(1)

    def closeEvent(self,event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Exit ...")
        msg.setText("Are you sure want to Exit ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        hide = msg.button(QMessageBox.No)
        hide.setText('Hide')
        close = msg.button(QMessageBox.Yes)
        close.setText('Exit')
        msg.setInformativeText("Choose Close App or Hide ......")
        result = msg.exec_()

        event.ignore()
        if result == QMessageBox.Yes:
            self.appQuit()
        if result == QMessageBox.No:
            self.hide()


    def eventFilter(self, object, event):
        if object == self.controlBox and event.type() == QtCore.QEvent.Enter:
            self.controlBox.setFixedHeight(90)
        if object ==  self.controlBox and event.type() == QtCore.QEvent.Leave:
            self.controlBox.setFixedHeight(5)
        if object == self.videoWidget and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print("right clicked show tool menu")
                self.listMenu_onRightClicked()

            if event.button() == QtCore.Qt.LeftButton:
                self.media_pause()

        elif object == self.videoWidget and event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.full_screen()
            
        return True

    def topWidget(self):
        if self.ontop == 0 :
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.ontop = 1
            self.topButton.setIcon(QtGui.QIcon(':/image/Qui/image/ontop.png'))
            self.show()
            
        else:
            self.setWindowFlags(QtCore.Qt.WindowShadeButtonHint)
            self.ontop = 0
            self.topButton.setIcon(QtGui.QIcon(':/image/Qui/image/normal.png'))
            self.show()

    def full_screen(self):
        if self.player.state() != 0:
            if self.ontop == 0:
                if self.videoWidget.isFullScreen() == False:
                    self.videoWidget.setFullScreen(True)              
                else:
                    self.videoWidget.setFullScreen(False)
            else:
                self.ontop = -1
                if self.videoWidget.isFullScreen() == False:
                    self.videoWidget.setFullScreen(True)
                    self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
                    self.show()
                else:
                    self.videoWidget.setFullScreen(False)
                    self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.ontop = 1
                    self.show()
                
            
    def exc_fullScreen(self):
        if self.ontop == -1:
            if self.videoWidget.isFullScreen() == True:
                self.videoWidget.setFullScreen(False)
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.ontop = 1
                self.show()
        else:
            if self.videoWidget.isFullScreen() == True:
                self.videoWidget.setFullScreen(False)
 

    def scroll_plane(self):
        if self.scrollControl == True :
            self.scrollControl = False
            self.groupBox_2.hide()
            
            self.scrollButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        else:
            self.scrollControl = True
            self.groupBox_2.show()
            self.scrollButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        

    def Media_add(self):

        sound_path = self.mediaPath[self.listWidget.currentRow()]
        url = QtCore.QUrl.fromLocalFile(sound_path)
        content = QMediaContent(url)
        self.soundtrack = QMediaPlaylist()
        self.soundtrack.addMedia(content)
        self.soundtrack.setCurrentIndex(1)

        self.player.setPlaylist(self.soundtrack)
        self.PlayButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.listcontrolButton.setEnabled(False)
    
    def list_charge(self):
        self.soundtrack_list = QMediaPlaylist()

        for n,name in enumerate(self.mediaPath):
            url = QtCore.QUrl.fromLocalFile(name)
            content = QMediaContent(url)
            self.soundtrack_list.addMedia(content)

        self.soundtrack_list.setCurrentIndex(1)
        self.player.setPlaylist(self.soundtrack_list)
        self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.PlayButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.listcontrolButton.setEnabled(True)
        self.loopButton.setEnabled(False)

        self.media_play()
    def list_control(self):
        match self.listloop:
            case 0:
                self.listloop = 1
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarContextHelpButton))
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Sequential)
            case 1:
                self.listloop = 2
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Random)
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            case 2:
                self.listloop = 0
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Loop)
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))
    
    def loop_control(self):
        if self.loop == 0:
            self.loop = 1
            self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
            self.soundtrack.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif self.loop == 1:
            self.loop = 0
            self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            self.soundtrack.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

    def skip_forward(self):
        self.set_position(self.timeSlider.maximum())
    def skip_backward(self):
        self.set_position(0)
    def move_forward(self):
        self.set_position(self.timeSlider.sliderPosition()+15000)
    def move_backward(self):
        self.set_position(self.timeSlider.sliderPosition()-15000)
    
    def slider_moved(self):
        self.set_position(self.timeSlider.value())

    def set_position(self, position):
        self.player.setPosition(position)

    def duration_changed(self, duration):
        self.timeSlider.setRange(0, duration)

    def position_changed(self, position):
        self.timeSlider.setValue(position)

    def show_mediaState(self):
        match self.player.state():
            case 1:
                self.setWindowTitle("Media Playing")
                self.iconPage.hide()
                self.videoWidget.show()
            case 2:
                self.setWindowTitle("Media Paused")
            case 0:
                self.setWindowTitle("Small Media Player")
                self.timeSlider.setValue(0)
                self.videoWidget.hide()
                self.iconPage.show()


    def Media_del(self):
        if self.listWidget.currentRow() == -1:
            self.setWindowTitle("NO Media select in List")
        else:
            index = self.listWidget.currentRow()
            self.mediaPath.pop(index)
            self.mediaList.pop(index)
            self.list_Media()

    def listAdd(self):
        ADD = QFileDialog()
        MFile = ADD.getOpenFileNames(self,"Add New Media", "","Media Files(*.mp4 *.avi *.mkv *.mov *.wmv *.flv)")

        for n in range(len(MFile[0])):
            path = MFile[0][n]
            self.mediaPath.append(path)
            self.mediaList.append(os.path.split(path)[1])
        self.list_Media()

    def list_Media(self):
        self.listWidget.clear()
        for m in self.mediaList:
            self.listWidget.addItem(m)
    
    def media_position(self):
        self.time = QtCore.QTimer(self)
        self.time.start(1000)
        self.time.timeout.connect(self.media_viewtime)
    
    def media_viewtime(self):
        pos_sec = int(self.player.position()/1000)
        pos = str(datetime.timedelta(seconds=pos_sec))
        dat_sec = int(self.player.duration()/1000)
        dat = str(datetime.timedelta(seconds=dat_sec))
        text = pos + "/" + dat
        self.label_time.setText(text)

    def volumeMute(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            self.mute.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.player.setMuted(True)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            self.mute.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            
    def volumeUpdate(self):
        self.player.setVolume(self.Slider_player_volume.value())

    def media_pause(self):
        if self.PlayButton.text() == "Play":
            self.setWindowTitle("NO media is playing Now!")
        else:
            if self.pause == 0:
                self.pause = 1
                self.player.pause()
                self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            else:
                self.pause = 0
                self.player.play()
                self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))    
        
    def media_play(self):
        if self.PlayButton.text() == "Play":
            self.PlayButton.setText("Stop")
            self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

            self.player.play()

            self.media_position()
        else:
            self.PlayButton.setText("Play")
            self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.player.stop()

            self.pause = 0
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))   

            self.time.stop()
            self.label_time.setText("--:--:-- / --:--:--")

    def play_arg(self, argval):
        print(argval)
        print("add list: [-1]:")
        print("media_play()")
