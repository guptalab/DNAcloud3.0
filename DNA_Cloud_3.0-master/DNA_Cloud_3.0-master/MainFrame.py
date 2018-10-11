"""
########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file is the Main GUI file that is to be launched via command - python MainFrame.py.
########################################################################################
"""
import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from collections import deque
import GoldmanEncoding
import GoldmanDecoding
import golayEncoding
import GolayDecode
import time
import EstimationUI


# This object carries out encoding action of certain type
class EncodeThread(QThread):
	signalStatus = pyqtSignal(str)  # Used for indication how much percentage of action completed
	
	def __init__(self,fileName,typeOfAction,parent=None):
		super(EncodeThread,self).__init__(parent)
		self.fileName = fileName
		self.typeOfAction = typeOfAction # 0 for encodeGoldman , 1 for encodeGolay , 2 for decodeGoldman , 3 for decodeGolay

	def run(self):
		if self.typeOfAction == 0 :      #Goldman Encoding
			GoldmanEncoding.encodeFile(self.fileName,self.signalStatus)
		elif self.typeOfAction == 1 :   # Golay Encoding
			golayEncoding.encodeFile(self.fileName,self.signalStatus)
		self.signalStatus.emit('Idle.') #Indicating action is finished

# This object carries out decoding action of certain type
class DecodeThread(QThread):
	signalStatus = pyqtSignal(str)  # Used for indication how much percentage of action completed
	
	def __init__(self,fileName,typeOfAction,parent=None):
		super(DecodeThread,self).__init__(parent)
		self.fileName = fileName
		self.typeOfAction = typeOfAction # 0 for encodeGoldman , 1 for encodeGolay , 2 for decodeGoldman , 3 for decodeGolay

	def run(self):
		if self.typeOfAction == 2 :    # Goldman Decoding
			GoldmanDecoding.decodeFile(self.fileName,self.signalStatus)
		elif self.typeOfAction == 3 :   # Golay Decoding
			GolayDecode.decodeFile(self.fileName,self.signalStatus)
		self.signalStatus.emit('Idle.') #Indicating action is finished

# This object shows dialouge box for selecting encoding type
class EncodeSelection(QDialog):
	def __init__(self, parent=None):
		super(EncodeSelection, self).__init__(parent)
		self.initUI()
	def initUI(self):
		self.selectionComboBox = QComboBox()
		encodings = ['Goldman','Golay']
		self.selectionComboBox.addItems(encodings)

		# OK and Cancel buttons
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
     
		layout = QVBoxLayout(self)
		layout.addWidget(self.selectionComboBox)
		layout.addWidget(self.buttons)
		self.setLayout(layout)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

# This object shows dialouge box for selecting decoding type
class DecodeSelection(QDialog):
	def __init__(self, parent=None):
		super(DecodeSelection, self).__init__(parent)
		self.initUI()
	def initUI(self):
		self.selectionComboBox = QComboBox()
		encodings = ['Goldman','Golay']
		self.selectionComboBox.addItems(encodings)

		# OK and Cancel buttons
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
     
		layout = QVBoxLayout(self)
		layout.addWidget(self.selectionComboBox)
		layout.addWidget(self.buttons)
		self.setLayout(layout)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)


# Selects one of the type of encoding/decoding (Golay or Goldman)
def getActionType(typeOfAction,parent = None):
	if typeOfAction == 'E':   # Encoding Action
		dialog = EncodeSelection(parent)
		result = dialog.exec_()
		encodingType = unicode(dialog.selectionComboBox.currentText())
		if encodingType == 'Goldman' :
			return 0
		elif encodingType == 'Golay' :
			return 1
		return -1
	else :
		dialog = DecodeSelection(parent)
		result = dialog.exec_()
		decodingType = unicode(dialog.selectionComboBox.currentText())
		if decodingType == 'Goldman' :
			return 2
		elif decodingType == 'Golay' :
			return 3
		return -1

# Used for identifying any action
class ActionIdentifierTuple():
	def __init__(self,progressBar,fileName,encodingType):
		self.progressBar = progressBar
		self.fileName = fileName
		self.encodingType = encodingType

# The Main GUI of any action
class ActionUI(QFrame):
  
	def __init__(self,parent,actionType):
		QFrame.__init__(self, parent)
		self.actionType = actionType   # 'E' for encoding , 'D' for decoding
		self.noOfFiles = 0
		self.processQueue = deque()
		self.running = False
		self.initUI()
        
	def initUI(self):
		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignTop)
		self.setLayout(self.layout)

		self.setAcceptDrops(True)
		self.setAutoFillBackground(False)
		self.setStyleSheet("background-color: rgb(255,250,250); margin:5px; border:1px solid rgb(0, 0, 0);")

	# This is called when any drag and drop event begins
	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore() 

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
			for url in event.mimeData().urls():
				linkToFile = str(url.toLocalFile())
				if os.path.isdir(linkToFile):
					print 'Folder Not Supported Yet'
					continue
				self.addLink(linkToFile)
		else:
            		event.ignore()

	def addLink(self,linkToFile):
		if not os.path.isfile(linkToFile):
			return

		textView = QLabel(linkToFile)
                textView.setStyleSheet("background-color: rgb(255,255,255); margin:5px; border:0px solid rgb(0, 0, 0);")
                scroll = QScrollArea()
                scroll.setWidget(textView)
                scroll.setWidgetResizable(True)
                scroll.setFixedWidth(250)
                scroll.setFixedHeight(40)
                scroll.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
                scroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff ) 

                self.progress = QProgressBar(self)
                self.progress.setValue(0)
                self.progress.setAlignment(Qt.AlignCenter)

                self.layout.addWidget(scroll,self.noOfFiles,0)
                self.layout.addWidget(self.progress,self.noOfFiles,1)

                self.noOfFiles = self.noOfFiles + 1
                self.addAction(self.progress,linkToFile,getActionType(self.actionType))

	def addAction(self,progressBar,fileName,encodingType):
		if len(self.processQueue)==0 :
			self.processQueue.append(ActionIdentifierTuple(progressBar,fileName,encodingType))
			self.startAction()
		else:
			self.processQueue.append(ActionIdentifierTuple(progressBar,fileName,encodingType))

	def startAction(self):
 		fileName = self.processQueue[0].fileName
		encodingType = self.processQueue[0].encodingType
		if(encodingType<=1):
			self.thread = EncodeThread(fileName,encodingType)
		else:
			self.thread = DecodeThread(fileName,encodingType)
		self.thread.signalStatus.connect(self.updateStatus)
		self.thread.start()

	def updateStatus(self,status):
		if status != 'Idle.':
			self.processQueue[0].progressBar.setValue(int(status))
		else:
			self.thread.wait()
			self.processQueue.popleft()
			if len(self.processQueue):
				self.startAction()

# This object represents main UI which is collection of all actions (Here encoding window + decoding window)
class MainUI(QWidget):
   
  def __init__(self,parent=None):
        super(MainUI, self).__init__(parent)
        self.initUI()

  def initUI(self):
        self.encodeUI = ActionUI(self,'E')
        self.decodeUI = ActionUI(self,'D')
      
	layout = QHBoxLayout()
	layout.addWidget(self.encodeUI,1)
        layout.addWidget(self.decodeUI,1)
        self.setLayout(layout)

# This object represents main GUI of application will all menus like FILE,ABOUT etc...
class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
                self.setWindowTitle('DNA 3.0')
		self.initUI()

	def initUI(self):               
		self.main_widget = MainUI() 
                self.setCentralWidget(self.main_widget)

		self.statusBar()   # for showing status bar in application
        	menubar = self.menuBar() # for showing menu items like FILE,ABOUT etc..

		#Actions for File menu	
		self.encodeAction = QAction('&Encode',self)
		self.encodeAction.setShortcut('Ctrl+E')
		self.encodeAction.setStatusTip('Encode file to DNA')
                self.connect(self.encodeAction,SIGNAL("triggered()"), self.encodeFile)
		
		self.decodeAction = QAction('&Decode',self)
		self.decodeAction.setShortcut('Ctrl+D')
		self.decodeAction.setStatusTip('Decode file from DNA')
                self.connect(self.decodeAction,SIGNAL("triggered()"), self.decodeFile)
		
		exitAction = QAction( '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		
		#File menu creation
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(self.encodeAction)
		fileMenu.addAction(self.decodeAction)
		fileMenu.addAction(exitAction)

		#Actions for Tools menu
		self.storageEstimatorAction = QAction('&Storage Estimator',self)
		self.storageEstimatorAction.setStatusTip('Estimates approximate encoded file size required on disk ')
                self.connect(self.storageEstimatorAction,SIGNAL("triggered()"), self.showMemoryEstimator)

		
		self.costEstimatorAction = QAction('&Cost Estimator',self)
		self.costEstimatorAction.setStatusTip('Predicts approximate cost to encode in DNA')
                self.connect(self.costEstimatorAction,SIGNAL("triggered()"), self.showCostEstimator)
		
		self.barcodeGeneratorAction = QAction('&Generate Barcode',self)
		self.barcodeGeneratorAction.setStatusTip('Generate Barcode')
		self.connect(self.barcodeGeneratorAction,SIGNAL("triggered()"), self.showBarcode)
		
                #Tools menu creation
		toolsMenu=menubar.addMenu('&Tools')
		toolsMenu.addAction(self.storageEstimatorAction)
		toolsMenu.addAction(self.costEstimatorAction)
		toolsMenu.addAction(self.barcodeGeneratorAction)

		#Actions for About menu
		versionAction = QAction('&Version',self)
		versionAction.setStatusTip('Version info.')
		
		#About menu creation
		AboutMenu=menubar.addMenu('&About')
		AboutMenu.addAction(versionAction)

                self.statusBar().showMessage("Drag and drop on left to encode file or on right to decode file");
                self.setStyleSheet("background-color: rgb(238,203,173)")

	def getEncodeActionUI(self):
		return self.main_widget.encodeUI

	def getDecodeActionUI(self):
		return self.main_widget.decodeUI

	def encodeFile(self) :
		openfile = QFileDialog.getOpenFileName(self) 
		encodeAction = self.getEncodeActionUI()
		encodeAction.addLink(str(openfile))

	def decodeFile(self) :
		openfile = QFileDialog.getOpenFileName(self) 
		decodeAction = self.getDecodeActionUI()
		decodeAction.addLink(str(openfile))

	def showBarcode(self) :  # Not supported Yet
		return

	def showMemoryEstimator(self) :
		est = EstimationUI.MemoryEstimation(self)
		est.exec_()

	def showCostEstimator(self) :
		est = EstimationUI.CostEstimation(self)
		est.exec_()

app = QApplication(sys.argv)
dna3Win = MainWindow()
dna3Win.showMaximized()
app.exec_() 
