from PyQt5 import QtCore, QtGui, QtWidgets
import pqBodyForecast as bf
import pqWeeklyForecast as wf

class Ui_MainWindow(object):
    """
    Sets up a user interface to access the computational PyQuaza modules and output celestial body forecasting information. 
    
    GUI User Inputs: Latitude, longitude, celestial body (depending on forecasting selection)
    GUI Outputs: Celestial body forecast image and text details
    
    """
    def setupUi(self, MainWindow):
        #Configure main window size and style
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1248, 891)
        MainWindow.setStyleSheet("background-color: rgb(223,223,223);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #Define entry fields for user latitude and longitude
        self.latEntry = QtWidgets.QSpinBox(self.centralwidget)
        self.latEntry.setGeometry(QtCore.QRect(130, 210, 81, 31))
        self.latEntry.setMinimum(-90) #Limit latitude entries to be within [-90,90]
        self.latEntry.setMaximum(90)
        self.latEntry.setObjectName("latEntry")
        self.latEntry.setStyleSheet("background-color: White;")
        
        self.lonEntry = QtWidgets.QSpinBox(self.centralwidget)
        self.lonEntry.setGeometry(QtCore.QRect(130, 250, 81, 31))
        self.lonEntry.setMinimum(-180) #Limit longitude entries to be within [-180,180]
        self.lonEntry.setMaximum(180)
        self.lonEntry.setObjectName("lonEntry")
        self.lonEntry.setStyleSheet("background-color: White;")
        
        #Define labels for the latitude and longitude entry fields
        self.label_latEntry = QtWidgets.QLabel(self.centralwidget)
        self.label_latEntry.setGeometry(QtCore.QRect(30, 210, 91, 31))
        self.label_latEntry.setObjectName("label_latEntry")
        
        self.label_lonEntry = QtWidgets.QLabel(self.centralwidget)
        self.label_lonEntry.setGeometry(QtCore.QRect(30, 250, 91, 31))
        self.label_lonEntry.setObjectName("label_lonEntry")
        
        #Setup widget where celestial body forecasts will be displayed
        self.forecastImage = QtWidgets.QLabel(self.centralwidget)
        self.forecastImage.setGeometry(QtCore.QRect(450, 190, 780, 650))
        self.forecastImage.setText("")
        self.forecastImage.setPixmap(QtGui.QPixmap("forecastImage.png")) #Setup initial image to be displayed when GUI is first opened
        self.forecastImage.setScaledContents(True)
        self.forecastImage.setObjectName("forecastImage")
        self.forecastImage.setStyleSheet("border: 1px solid black;")
        
        #Display PyQuaza logo on GUI main window:
        self.pyquazaLogo = QtWidgets.QLabel(self.centralwidget)
        self.pyquazaLogo.setGeometry(QtCore.QRect(20, 10, 471, 171))
        self.pyquazaLogo.setText("")
        self.pyquazaLogo.setPixmap(QtGui.QPixmap("pyquazaLogo.png"))
        self.pyquazaLogo.setObjectName("pyquazaLogo")
        
        #Setup location for PyQuaza/GUI functionality overview 
        self.pyquazaOverview = QtWidgets.QTextBrowser(self.centralwidget)
        self.pyquazaOverview.setGeometry(QtCore.QRect(480, 20, 751, 155))
        self.pyquazaOverview.setObjectName("pyquazaOverview")
        self.pyquazaOverview.setStyleSheet("background-color: White;")
        
        #Setup location for forecasting output text to be displayed
        self.forecastOutputText = QtWidgets.QTextBrowser(self.centralwidget)
        self.forecastOutputText.setGeometry(QtCore.QRect(230, 190, 211, 651))
        self.forecastOutputText.setObjectName("forecastOutputText")
        self.forecastOutputText.setStyleSheet("background-color: White; font: bold 14px;")
        
        #Define button to provide specific body forecast:
        self.specificBodyButton = QtWidgets.QPushButton(self.centralwidget)
        self.specificBodyButton.setGeometry(QtCore.QRect(30, 390, 181, 51))
        self.specificBodyButton.setObjectName("specificBodyButton")
        self.specificBodyButton.setStyleSheet("background-color: White;")
        
        #Setup combobox with fields for celestial body options:
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 350, 111, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setStyleSheet("background-color: White;")
        
        #Setup label for combobox:
        self.label_bodySelect = QtWidgets.QLabel(self.centralwidget)
        self.label_bodySelect.setGeometry(QtCore.QRect(30, 310, 181, 41))
        self.label_bodySelect.setObjectName("label_bodySelect")
        
        #Define button to review all body options & forecast optimal body to view:
        self.generalForecastButton = QtWidgets.QPushButton(self.centralwidget)
        self.generalForecastButton.setGeometry(QtCore.QRect(30, 700, 181, 51))
        self.generalForecastButton.setObjectName("generalForecastButton")
        self.generalForecastButton.setStyleSheet("background-color: White;")
        
        #Setup label to differentiate between forecasting options
        self.label_bodySelect_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_bodySelect_2.setGeometry(QtCore.QRect(30, 650, 181, 41))
        self.label_bodySelect_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bodySelect_2.setObjectName("label_bodySelect_2")
       
        #Define widget to display planet image depending on user-selected body
        self.specificBodyLogo = QtWidgets.QLabel(self.centralwidget)
        self.specificBodyLogo.setGeometry(QtCore.QRect(30, 450, 181, 181))
        self.specificBodyLogo.setText("")
        self.specificBodyLogo.setPixmap(QtGui.QPixmap("moon.png"))
        self.specificBodyLogo.setScaledContents(True)
        self.specificBodyLogo.setObjectName("specificBodyLogo")
        
        #Define menu and status bars for GUI
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1248, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Tie GUI buttons to target functions below:
        self.specificBodyButton.clicked.connect(self.showSpecificBody)
        self.comboBox.currentTextChanged.connect(self.showSpecificBodyImage)
        self.generalForecastButton.clicked.connect(self.showGeneralForecast)

    def showSpecificBodyImage(self):
        #Function to show a sample image of the user-selected planet, linked to combobox selection
        body = self.comboBox.currentText() #Pull user-selected body choice
        bodyLogoFile = f"{body}.png" #Establish file name (predetermined)
        self.specificBodyLogo.setPixmap(QtGui.QPixmap(bodyLogoFile))
    
    def showSpecificBody(self):
        #Function to feed user inputs (latitude, longitude, body) into pqBodyForecast module
        #Outputs image and text corresponding to optimal viewing time from pqBodyForecast into GUI widgets
        _translate = QtCore.QCoreApplication.translate
        lat = self.latEntry.value() #Pull user-entered latitude entry
        lon = self.lonEntry.value() #Pull user-entered longitude entry
        body = self.comboBox.currentText() #Pull user-selected body choice           
              
        if body == 'Earth': 
            self.forecastOutputText.setText(_translate("MainWindow", "Maybe just look down?"))
            self.forecastImage.setPixmap(QtGui.QPixmap("outputIfEarth.png"))
        else:     
            bodyForecast = bf.BodyForecast(lat, lon, body)
            bodyForecast.run_all()
            self.forecastOutputText.setText(_translate("MainWindow", bodyForecast.figText))
            self.forecastImage.setPixmap(QtGui.QPixmap("body.png"))
        
    def showGeneralForecast(self):
        #Function to feed user inputs (latitude, longitude) into pqWeeklyForecast module
        #Outputs image and text corresponding to optimal body choice and viewing time from pqWeeklyForecast into GUI widgets
        _translate = QtCore.QCoreApplication.translate
        lat = self.latEntry.value() #Pull user-entered latitude entry
        lon = self.lonEntry.value() #Pull user-entered longitude entry
        genForecast = wf.WeeklyForecast(lat,lon)
        genForecast.get_plot()
        self.forecastOutputText.setText(_translate("MainWindow", genForecast.figText))
        self.forecastImage.setPixmap(QtGui.QPixmap("body.png"))

##################################################

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #Set text for previously defined labels, text boxes, and combobox fields
        self.label_latEntry.setText(_translate("MainWindow", "Enter Latitude:"))
        self.label_lonEntry.setText(_translate("MainWindow", "Enter Longitude:"))
        self.pyquazaOverview.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">About PyQuaza</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">PyQuaza is a forecasting resource for amateur astronomers to optimize their stargazing experiences! Use the widgets below to forecast optimal viewing times for a specific astrological body, or for the best option from the list of available bodies. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">How To Use</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">First, enter the latitude (-90, 90) and longitude (-180, 180) of the viewing location. To find the best viewing time for a specific astrological body, select a planet from the drop-down menu and hit &quot;Display Planet Forecast&quot;. To evaluate the general list of celestial bodies to display an optimal body choice & viewing time, simply hit &quot;Display General Forecast&quot;. Note that both forecast options are evaluated over a 7-day time frame, starting from today's date.</span></p></body></html>"))
        self.specificBodyButton.setText(_translate("MainWindow", "Display Planet Forecast"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Moon"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Mercury"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Venus"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Earth"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Mars"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Jupiter"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Saturn"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Uranus"))
        self.comboBox.setItemText(8, _translate("MainWindow", "Neptune"))
        self.label_bodySelect.setText(_translate("MainWindow", "Select Celestial Body of Interest:"))
        self.generalForecastButton.setText(_translate("MainWindow", "Display General Forecast"))
        self.label_bodySelect_2.setText(_translate("MainWindow", "-- OR --"))

if __name__ == "__main__":
    import sys  
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()