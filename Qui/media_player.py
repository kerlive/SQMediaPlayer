# PyQt5 Media player
#code by kevin
__author__ = "Kevin Chan"
__copyright__ = "Copyright (C) 2022 Kevin Chan"
__license__ = "GPL-3.0"
__version__ = "0.1.0"

import os, sys, random
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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(1000, 600, 500, 300)
        self.setWindowTitle('App Name')

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
        self.videoLayout.addWidget(self.videoWidget)
        self.player.setVideoOutput(self.videoWidget)

        self.videoWidget.installEventFilter(self)

        # Layout
        self.setLayout(self.allinLayout)
        self.groupBox.setMinimumSize(451, 90)
        self.groupBox.setFixedHeight(90)
        self.groupBox_2.setFixedWidth(241)

        self.videoWidget.setMinimumSize(451, 381)


        #set can not minisize for trayicon
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWhatsThis("Any you want to know in help.html")


        self.sizecontrol = 0
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
        self.horizontalSlider.sliderReleased.connect(self.slider_moved)
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

        # loop signal
        self.loop = 0
        self.listloop = 0

        self.list_Media()


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
    



        # Icon change signal
        self.pause = 0

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
        quit.triggered.connect(self.trayicon_quit)
        quit.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        menu.addAction(quit)

        self.trayIcon.setContextMenu(menu)

        self.anotherCall()

    def eventFilter(self, object, event):

        if object == self.videoWidget and event.type() == QtCore.QEvent.MouseButtonPress:
            self.media_pause()
        
        elif object == self.videoWidget and event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.full_screen()
            
        return True
        

    def full_screen(self):
        if self.videoWidget.isFullScreen() == True:
            self.videoWidget.setFullScreen(False)
        else:
            self.videoWidget.setFullScreen(True)
    def exc_fullScreen(self):
        if self.videoWidget.isFullScreen() == True:
            self.videoWidget.setFullScreen(False)
 

    def scroll_plane(self):
        if self.sizecontrol == 0 :
            self.sizecontrol = 1
            self.groupBox_2.hide()
            
            self.scrollButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        else:
            self.sizecontrol = 0
            self.groupBox_2.show()
            self.scrollButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        
    def anotherCall(self):
        cTimer = QtCore.QTimer(self)
        cTimer.start(1000)
        cTimer.timeout.connect(self.checkNew)
    def checkNew(self):
         if single.buf[0] == 0:
             self.show()
             single.buf[0] = 1
    
    def trayicon_quit(self):
        sys.exit(1)
    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.hide()
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def Media_add(self):
        name = self.listWidget.currentItem().text()
        sound_path =  os.path.dirname(os.path.abspath(__name__)) + "/Media/" + name
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
        name_list = os.listdir(os.getcwd()+"/Media/")
        for n,name in enumerate(name_list):
            url = QtCore.QUrl.fromLocalFile(os.getcwd()+"/Media/"+name)
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
        self.set_position(self.horizontalSlider.maximum())
    def skip_backward(self):
        self.set_position(0)
    def move_forward(self):
        self.set_position(self.horizontalSlider.sliderPosition()+15000)
    def move_backward(self):
        self.set_position(self.horizontalSlider.sliderPosition()-15000)
    
    def slider_moved(self):
        self.set_position(self.horizontalSlider.value())

    def set_position(self, position):
        self.player.setPosition(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)

    def show_mediaState(self):
        match self.player.state():
            case 1:
                self.setWindowTitle("Media Playing")
            case 2:
                self.setWindowTitle("Media Paused")
            case 0:
                self.setWindowTitle("Small Media Player")
                self.horizontalSlider.setValue(0)
                self.label_time.setText("00:00:00/00:00:00")
                self.PlayButton.setText("Play")
                self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def Media_del(self):
        if self.listWidget.currentRow() == -1:
            self.setWindowTitle("NO Media select in List")
        else:
            name = self.listWidget.currentItem().text()
            Dpath = os.path.dirname(os.path.abspath(__name__))+"\Media/"+name
            os.remove(Dpath)
            self.listWidget.clear()
            self.list_Media()

    def listAdd(self):
        ADD = QFileDialog()
        MFile = ADD.getOpenFileName(self,"Add New Media", "","Media Files(*.mp4 *.avi *.mkv *.mov *.wmv *.flv)")
        Mname = os.path.split(MFile[0])
        QtCore.QFile.copy(MFile[0],"./Media/"+Mname[1])
        self.listWidget.clear()
        self.list_Media()

    def list_Media(self):
        Media_path = os.path.dirname(os.path.abspath(__name__)) + "/Media"
        dir_list = os.listdir(Media_path)
        for m in dir_list:
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
        else:
            self.player.setMuted(True)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            
    def volumeUpdate(self):
        self.player.setVolume(self.Slider_player_volume.value())

    def media_pause(self):
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
            self.label_time.setText("00:00:00/00:00:00")

    def event(self, event):
        if event.type() == QtCore.QEvent.EnterWhatsThisMode:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.getcwd()+"/Help/help.html"))
        return super().event(event)