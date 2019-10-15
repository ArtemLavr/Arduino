from pyfirmata import Arduino, util

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from prog import Ui_MainWindow  
import sys, time, json
 

class QThread1 (QtCore.QThread):
	sigtxt = pyqtSignal(str)
	sigbar = pyqtSignal(float)
	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		
	
		
	def run(self):
		
		self.running = True
		
		self.board = Arduino('COM3')
		SENSOR_PIN=0
		LED_PIN=13
		it = util.Iterator(self.board)
		it.start()
		self.board.analog[0].enable_reporting()
		while True:
			self.light_level = self.board.analog[SENSOR_PIN].read()
			if self.light_level != None:

				if self.light_level < 0.5:
					
					self.status = "Kto-to probil kabel"
					self.board.digital[13].write(1)
					
					self.sigtxt.emit(self.status)
					self.sigbar.emit(self.light_level)
				else:
					self.board.digital[13].write(0)
					self.status = "Vse v norme"
					
					self.sigtxt.emit(self.status)
					self.sigbar.emit(self.light_level)
					
					
			self.board.pass_time(1)    
	def stop(self):
		self.board.exit()
		self.terminate()
		self.running = False
		


count = 1 
class mywindow(QtWidgets.QMainWindow):
	
	
	
	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.label.setText('Datchik 1')
		self.progress = self.ui.progressBar
		self.progress.setMinimum(0)
		self.progress.setMaximum(100)

		self.ui.pushButton.clicked.connect(self.monitor)
		self.ui.actionAdd_Bar.triggered.connect(self.Add)
		self.setting()


	def monitor(self):
		if self.ui.pushButton.text() == 'Start':
			self.ui.pushButton.setText('Stop')
			self.thread1= QThread1()
			self.thread1.start()
			self.thread1.sigtxt.connect(self.status_info)
			self.thread1.sigbar.connect(self.bar_info)
			
		else:
			
			time.sleep(2)
			
			self.thread1.stop()
			self.ui.pushButton.setText('Start')

	def status_info(self, info):
		info = str(info)
		localtime = time.asctime( time.localtime(time.time()) )
		self.ui.textEdit.append(localtime + " :" + info)

	def bar_info(self, bar_val):
		self.progress.setValue(int(bar_val*100))
		if int(bar_val*100)<50:
			self.progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")                                                 

	def Add(self):
		global count
		
		self.bar =  QtWidgets.QProgressBar()
		self.bar.setProperty("value", 50)
		self.bar.setOrientation(QtCore.Qt.Vertical)
		self.bar.setFormat("%p%")
		self.lbl = QtWidgets.QLabel()
		self.lbl.setText("Datchik"+str(count +1))
		self.ui.gridLayout.addWidget(self.bar,0, count,1, 1)
		self.ui.gridLayout.addWidget(self.lbl,1, count,1, 1)   
		count +=1
		with open("setting.json", "r") as jsonFile:
			data = json.load(jsonFile)

		tmp = data["barcol"]
		data["barcol"] = count-1

		with open("setting.json", "w") as jsonFile:
			json.dump(data, jsonFile)


	def setting(self):
		with open('setting.json') as json_file:
			data = json.load(json_file)
			for i in range(data["barcol"]):
				self.Add()       
			

		
		
	
		

			
				


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())
