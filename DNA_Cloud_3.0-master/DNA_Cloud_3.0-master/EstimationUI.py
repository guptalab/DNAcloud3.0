"""
###################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file shows UI related to Cost estimation and Memory Estimation
###################################################################
"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import SizeEstimation

class CostEstimation(QDialog) :
	def __init__(self, parent=None):
		super(CostEstimation, self).__init__(parent)
		self.initUI()
	def initUI(self):
		self.costPerDNATitle = QLabel("Cost Per DNA ($) : ")
		self.costPerDNA = QDoubleSpinBox()
		self.costPerDNA.setRange(0, 100.00)
		self.costPerDNA.setValue(1.00)

		self.costTitle = QLabel("Cost ($) : ")
		self.costValue = QLabel("0 $")

		self.encodingType = QLabel("Encoding Type : ")
		self.encodingValue = QComboBox()
		encodings = ['Goldman','Golay']
		self.encodingValue.addItems(encodings)

		self.fileTarget = QLabel("Browse File")
		self.browseButton = QPushButton("Browse")

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.layout.addWidget(self.fileTarget,0,0)
		self.layout.addWidget(self.browseButton,0,1)
		self.layout.addWidget(self.costPerDNATitle,1,0)
		self.layout.addWidget(self.costPerDNA,1,1)
		self.layout.addWidget(self.encodingType,2,0)
		self.layout.addWidget(self.encodingValue,2,1)
		self.layout.addWidget(self.costTitle,3,0)
		self.layout.addWidget(self.costValue,3,1)

		self.connect(self.costPerDNA,SIGNAL("valueChanged(double)"), self.updateUi)
		self.browseButton.clicked.connect(self.doBrowsing)
		self.connect(self.encodingValue,SIGNAL("currentIndexChanged(int)"), self.updateUi)
		
		self.fileName = ''

	def doBrowsing(self):
		openfile = QFileDialog.getOpenFileName(self) 
		if openfile == '' or (not openfile) :
			return
		self.fileName = openfile
		self.fileTarget.setText(openfile)
		self.updateUi()

	def updateUi(self):
		if self.fileName == '' or (not self.fileName) :
			return
		totDNABases = self.calculateDNABases(os.path.getsize(self.fileName),self.encodingValue.currentText())
		costVal = self.costPerDNA.value() * self.totDNABases
		self.costValue.setText("%0.2f" % costVal)
   
	def calculateDNABases(self,fileSize,encodingType) :
		return SizeEstimation.estimateNoOfDNABasesUsedForEncoding(encodingType,self.fileName,fileSize)

class MemoryEstimation(QDialog) :
	def __init__(self,parent=None):
		super(MemoryEstimation, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.fileSizeTitle = QLabel("Storage of above file on Disk(Bytes) : ")
		self.fileSize = QLabel("0")

		self.memoryTitle = QLabel("Storage of Encoded file on Disk(Bytes) : ")
		self.memoryValue = QLabel("0")
     
		self.fileTarget = QLabel("Browse File")
		self.browseButton = QPushButton("Browse")

		self.encodingType = QLabel("Encoding Type : ")
		self.encodingValue = QComboBox()
		encodings = ['Goldman','Golay']
		self.encodingValue.addItems(encodings)
     
		self.layout = QGridLayout()
		self.setLayout(self.layout)
     
		self.layout.addWidget(self.fileTarget,0,0)
		self.layout.addWidget(self.browseButton,0,1)
		self.layout.addWidget(self.fileSizeTitle,1,0)
		self.layout.addWidget(self.fileSize,1,1)
		self.layout.addWidget(self.encodingType,2,0)
		self.layout.addWidget(self.encodingValue,2,1)
		self.layout.addWidget(self.memoryTitle,3,0)
		self.layout.addWidget(self.memoryValue,3,1)

		self.browseButton.clicked.connect(self.doBrowsing)
		self.connect(self.encodingValue,SIGNAL("currentIndexChanged(int)"), self.updateUi)

		self.fileName = ''

	def doBrowsing(self):
		openfile = QFileDialog.getOpenFileName(self) 
		if openfile == '' or (not openfile) :
			return
		self.fileName = openfile
		self.fileTarget.setText(openfile)
		fileSize = os.path.getsize(openfile)
		self.fileSize.setText(str(fileSize))
		self.updateUi()

	def updateUi(self):
		if self.fileName == '' or (not self.fileName) :
			return
		totDNABases = self.calculateDNABases(os.path.getsize(self.fileName),self.encodingValue.currentText())
		self.memoryValue.setText(str(totDNABases))

	def calculateDNABases(self,fileSize,encodingType) :
		return  SizeEstimation.estimateNoOfDNABasesUsedForEncoding(encodingType,self.fileName,fileSize)
