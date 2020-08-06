from PySide2.QtWidgets import QApplication, QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QLabel, QPushButton, QRadioButton, QFileDialog, QTextEdit
import sys
from PySide2.QtGui import QIcon, QFont, QPixmap
import re
import numpy as np
from pyqtgraph.GraphicsScene import exportDialog
import pyqtgraph as pg
import pyqtgraph.exporters


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # ----------style-------------
        self.font_type = "Arial"
        self.font_size = 10
        self.font_color = "#676767"
        self.font_size2 = 12
        self.font_color_black = "#f0f0f0"
        #---------------------------------
        self.text8 = QTextEdit()
        self.text8.setReadOnly(True)
        self.check_text= False
        self.gbox6 = QGroupBox()

        try:
            f = open("plotter.txt", "x+")
        except:
            f = open("plotter.txt", "r")

        self.s = f.readline()
        f.close
        if self.s == "":
            f = open("plotter.txt", "w")
            f.write("dark")
            f.close()
            self.s="dark"
            self.information_dialog()

        else:
            self.gbox6.setStyleSheet("border:None;background-color:rgba(255,255,255,0)")
            self.text8.setStyleSheet("border:None;background-color:rgba(255,255,255,0)")
            self.gbox6.setTitle("")
            self.text8.setText("")

        np.seterr(invalid='raise')
        self.setWindowTitle("XGrapher")
        self.setGeometry(500, 400, 900, 600)
        self.setMinimumSize(900, 600)
        pg.setConfigOption('background', (255, 255, 255, 0))
        self.pw = pg.PlotWidget()
        self.pw.setXRange(0, 1)
        self.pw.setYRange(0, 1)
        self.pw.hideButtons()
        #---------------------------
        self.list_errors=[]
        # --------------------------
        self.a = False
        self.b = False
        self.c = False
        # -------------------------
        self.d = False
        self.e = False
        self.f = False
        self.g = False
        self.after = False
        # -------------------------
        self.check1 = False
        self.check2 = False
        self.check3 = False
        self.check_dot = False
        self.check_neg = False
        self.check_xrange = False
        self.check_yrange = False
        # ------------Labels-----------------------------------------
        self.label1 = QLabel()
        self.label1.setText("F(x):")
        self.label2 = QLabel()
        self.label2.setText("Min(x):")
        self.label3 = QLabel()
        self.label3.setText("Max(x):")
        self.label4 = QLabel()
        self.label5 = QLabel()
        self.label5.setText("< x <")
        self.label6 = QLabel()
        self.label6.setText("< y <")
        # --------------------------texteditors------------------
        self.text1 = QLineEdit(self)
        self.text1.textChanged.connect(self.text1_response)
        self.text1.returnPressed.connect(self.focus_text1)
        self.text2 = QLineEdit(self)
        self.text2.textChanged.connect(self.text2_response)
        self.text2.returnPressed.connect(self.focus_text2)
        self.text3 = QLineEdit(self)
        self.text3.textChanged.connect(self.text3_response)
        self.text3.returnPressed.connect(self.focus_text3)
        self.text4 = QLineEdit()
        self.text4.textChanged.connect(self.text4_response)
        self.text4.returnPressed.connect(self.focus_text4)
        self.text5 = QLineEdit()
        self.text5.textChanged.connect(self.text5_response)
        self.text5.returnPressed.connect(self.focus_text5)
        self.text6 = QLineEdit()
        self.text6.textChanged.connect(self.text6_response)
        self.text6.returnPressed.connect(self.focus_text6)
        self.text7 = QLineEdit()
        self.text7.textChanged.connect(self.text7_response)
        self.text7.returnPressed.connect(self.focus_text7)
        # --------------------------------------------------------
        self.button_2 = QPushButton()
        self.button_2.clicked.connect(self.auto_mode)
        self.button_save = QPushButton("Export Graph")
        self.button_help = QPushButton()
        self.button_help.clicked.connect(self.information_dialog)
        # ----------------------RadioButtons----------------------
        self.rbutton1 = QRadioButton("Light")
        self.rbutton1.toggled.connect(self.light_mode)
        self.rbutton2 = QRadioButton("Dark")
        self.rbutton2.toggled.connect(self.dark_mode)
        # --------------------------------------------------------

        self.setIcon()
        self.center()
        self.input_box()
        self.plot_box()
        self.vbox = QHBoxLayout()
        self.vbox.addWidget(self.gbox5)
        self.vbox.addSpacing(5)
        self.vbox.addWidget(self.plot)
        # self.setStyleSheet("background-color:rgb(32,32,32);")
        # self.setStyleSheet("background-color:rgb(240,240,240);")
        self.setLayout(self.vbox)
        if self.s == "dark":
            self.rbutton2.setChecked(True)
        else:
            self.rbutton1.setChecked(True)

        if self.s == "dark":
            self.dark_mode()
        else:
            self.light_mode()
        self.show()


        # --------------------------------------evalute-------------------------------------------------------------------
        self.replacements = {'sin': 'np.sin', 'cos': 'np.cos', 'tan': 'np.tan', 'arccos': 'np.arccos',
                             'arcsin': 'np.arcsin', 'arctan': 'np.arctan', 'exp': 'np.exp', 'sqrt': 'np.sqrt',
                             'cbrt': 'np.cbrt','ln':'np.log', "cosh":"np.cosh", "sinh":"np.cosh", "tanh":"np.cosh"}

        self.allowed_words = ["x", "sin", "cos", "tan", "arccos", "arcsin", "arctan", "cosh", "sinh", "tanh", "exp",
                              "sqrt", "cbrt", "log10", "ln"]

        # ----------------------------------------------------------------------------------------------------------------
        self.after = True

    def setIcon(self):
        appIcon = QIcon("close.ico")
        self.setWindowIcon(appIcon)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def input_box(self):
        self.input = QGroupBox("Function")
        self.gbox = QGroupBox("Range")
        vbox_parent = QVBoxLayout()
        self.hbox_parent = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addSpacing(17)
        hbox1.addWidget(self.text1)
        hbox2.addWidget(self.label2)
        hbox2.addSpacing(4)
        hbox2.addWidget(self.text2)
        hbox3.addWidget(self.label3)
        hbox3.addSpacing(0)
        hbox3.addWidget(self.text3)

        hbox_button = QHBoxLayout()

        hbox_button.addStretch(1)
        self.button = QPushButton("Reset")
        self.button.setFixedSize(70, 25)
        self.button.clicked.connect(self.reset)
        hbox_button.addWidget(self.button)

        vbox_parent.addLayout(hbox1)
        vbox_parent.addLayout(hbox2)
        vbox_parent.addLayout(hbox3)
        vbox_parent.addLayout(hbox_button)
        self.input.setLayout(vbox_parent)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.text4)
        hbox4.addWidget(self.label5)
        hbox4.addWidget(self.text5)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.text6)
        hbox5.addWidget(self.label6)
        hbox5.addWidget(self.text7)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.button_2)
        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox4)
        vbox2.addLayout(hbox5)
        hbox6 = QHBoxLayout()
        hbox6.addLayout(vbox2)
        hbox6.addLayout(vbox3)
        self.gbox.setLayout(hbox6)
        #self.button_save.setFixedSize(200, 25)
        self.button_save.setFixedHeight(25)
        self.button_save.setFixedWidth(220)
        self.button_save.clicked.connect(self.export)
        hbox7 = QHBoxLayout()
        hbox7.addWidget(self.button_save)
        hbox7.addWidget(self.button_help)
        self.gbox3 = QGroupBox()
        self.gbox3.setFlat(True)
        self.gbox3.setStyleSheet("border: None")
        #self.gbox3.setLayout(hbox7)




        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.gbox)
        self.gbox4 = QGroupBox("Status")
        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.label4)
        self.gbox4.setLayout(hbox8)

        self.gbox_mode = QGroupBox("Style")
        vbox4 = QHBoxLayout()
        vbox4.addWidget(self.rbutton1)
        vbox4.addWidget(self.rbutton2)
        self.gbox_mode.setLayout(vbox4)


        hbox9 = QHBoxLayout()
        hbox9.addWidget(self.text8)
        self.gbox6.setLayout(hbox9)


        self.hbox_parent.addWidget(self.input)
        self.hbox_parent.addLayout(vbox3)
        self.hbox_parent.addLayout(hbox7)
        self.hbox_parent.addWidget(self.gbox6)


        self.hbox_parent.addWidget(self.gbox_mode)
        self.hbox_parent.addWidget(self.gbox4)
        self.gbox5 = QGroupBox()
        self.gbox5.setLayout(self.hbox_parent)

    def plot_box(self):
        self.plot = QGroupBox()
        layout = QVBoxLayout()
        self.pw.showGrid(True, True, 0.5)
        layout.addWidget(self.pw)
        self.plot.setLayout(layout)

    def text_restricted(self, str):
        if str != "":
            word = str[len(str) - 1]
            if re.match('[0-9-.]', word) is None:
                k = str.translate({ord(word): None})
                str = k
            if word == "-" and len(str) > 1:
                k = str[1:].translate({ord(word): None})
                str = str.replace(str[1:], k)
            if word == ".":
                i = 0
                for v in str:
                    if v == ".":
                        i += 1
                if i > 1:
                    str = str[0:len(str) - 1] + ""
            if word == ".":
                self.check_dot = True
        else:
            str=""
        return str

    def text1_response(self):
        if self.check1 == False:
            self.a = True
            self.plotx()
        else:
            self.check1 = False


    def text2_response(self):
        self.text2.setText(self.text_restricted(self.text2.text()))
        if self.check2 == False:
            self.b = True
            self.plotx()
        else:
            self.check2 = False

    def text3_response(self):
        self.text3.setText(self.text_restricted(self.text3.text()))
        if self.check3 == False:
            self.c = True
            self.plotx()
        else:
            self.check3 = False

    def text4_response(self):
        self.text4.setText(self.text_restricted(self.text4.text()))
        self.xrange()

    def text5_response(self):
        self.text5.setText(self.text_restricted(self.text5.text()))
        self.xrange()

    def text6_response(self):
        self.text6.setText(self.text_restricted(self.text6.text()))
        self.yrange()

    def text7_response(self):
        self.text7.setText(self.text_restricted(self.text7.text()))
        self.yrange()

    def xrange(self):
        if self.text4.text() == "" and self.text5.text() == "":
            self.error("No X Min Range")
            self.error("No X Max Range")
            self.error("Invalid X Range")
            self.f = False
            self.check_xrange = False
            if self.text1.text() == "" or self.text2.text() == "" or self.text3.text() == "":
                self.pw.setXRange(0, 1)
            else:
                self.pw.enableAutoRange(axis='x')

        elif self.text4.text() != "" and self.text5.text() != "":
            self.check_xrange = True
            if float(self.text4.text()) >= float(self.text5.text()):
                self.error_add("Invalid X Range")
                self.f = True
            else:
                self.pw.setXRange(float(self.text4.text()), float(self.text5.text()))
                self.error("No X Min Range")
                self.error("No X Max Range")
                self.error("Invalid X Range")

                self.f = False
                self.plotx()
            if self.text6.text() == "" or self.text7.text() == "":
                self.pw.enableAutoRange(axis='y')
                self.pw.setAutoVisible(y=True)
        else:
            if self.text4.text()=="" and self.check_xrange == True:
                self.error_add("No X Min Range")
                self.f = True
                self.pw.setXRange(0, 1)
            if self.text5.text()=="" and self.check_xrange == True:
                self.error_add("No X Max Range")
                self.f = True
                self.pw.setXRange(0, 1)
            if self.text6.text() != "" and self.text7.text() != "":
                self.pw.enableAutoRange(axis='x')
                self.pw.setAutoVisible(x=True)
            else:
                if self.d == True or self.e == True:
                    self.pw.setYRange(0, 1)
                    self.pw.setXRange(0, 1)
                else:
                    self.pw.enableAutoRange()

    def yrange(self):
        if self.text6.text() == "" and self.text7.text() == "":
            self.error("No Y Min Range")
            self.error("No Y Max Range")
            self.error("Invalid Y Range")
            self.g = False
            self.check_yrange = False
            if self.text1.text() == "" or self.text2.text() == "" or self.text3.text() == "":
                self.pw.setYRange(0, 1)
            else:
                self.pw.enableAutoRange(axis='y')

        elif self.text6.text() != "" and self.text7.text() != "":
            self.check_yrange = True
            if float(self.text6.text()) >= float(self.text7.text()):
                self.error_add("Invalid Y Range")
                self.g = True
            else:
                self.pw.setYRange(float(self.text6.text()), float(self.text7.text()))
                self.error("No Y Min Range")
                self.error("No Y Max Range")
                self.error("Invalid Y Range")
                self.g = False
                self.plotx()
            if self.text4.text() == "" or self.text5.text() == "":
                self.pw.enableAutoRange(axis='x')
                self.pw.setAutoVisible(x=True)
        else:
             if self.text6.text()=="" and self.check_yrange == True:
                self.error_add("No Y Min Range")
                self.g = True
                self.pw.setYRange(0, 1)
             if self.text7.text()=="" and self.check_yrange == True:
                self.error_add("No Y Max Range")
                self.g = True
                self.pw.setYRange(0, 1)
             if self.text4.text() != "" and self.text5.text() != "":
                self.pw.enableAutoRange(axis='y')
                self.pw.setAutoVisible(y=True)
             else:
                 if self.d == True or self.e == True:
                    self.pw.setYRange(0, 1)
                    self.pw.setXRange(0, 1)
                 else:
                    self.pw.enableAutoRange()

    def string2func(self, str):
        if str != "" and self.a == True and self.b == True and self.c == True:
            self.error("No Function to draw")
            self.d = False
            for word in re.findall('[a-zA-Z_]+', str):
                if word not in self.allowed_words:
                    self.error_add("F(x) is not a Function of x")
                    self.d = True
                else:
                    self.d = False
                    self.error('F(x) is not a Function of x')
                if word in self.replacements:
                    str = str.replace(word, self.replacements[word])
            if "^" in str:
                    str = str.replace("^", "**")
        elif str=="" and self.b == True and self.c == True:
                self.error_add("No Function to draw")
                self.d = True
                self.pw.clear()




        def func(x):
            if str != "" and self.text2.text()!="" and self.text3.text()!="" and self.d == False:
                if self.d == False:
                    try:
                        if np.inf in eval(str):
                            raise ZeroDivisionError
                        if -np.inf in eval(str):
                            raise ValueError
                    except ZeroDivisionError:
                        self.error_add("Cannot divide by Zero")
                        self.d = True
                    except FloatingPointError:
                        self.error_addd("Undefined")
                        self.d = True
                    except ValueError:
                        self.error_add("Math Error")
                        self.d = True
                    except:
                        self.error_add("Syntax Error")
                        self.d = True
                    else:
                        self.error("Cannot divide by Zero")
                        self.error("Undefined")
                        self.error("Math Error")
                        self.error("Syntax Error")
                        self.d = False



            return eval(str)

        return func

    def plotx(self):
        if self.text2.text() == "" and self.text3.text() == "" and self.text1.text() == "" and self.a == True and self.b == True and self.c == True:
            self.reset()
        func = self.string2func(self.text1.text())
        if self.a == True and self.b == True and self.c == True and self.text2.text() != "" and self.text3.text() != "" and self.text1.text() != ""and self.d == False:
            if (self.text4.text() == "" and self.text5.text() == "") and (
                    self.text6.text() == "" and self.text7.text() == ""):
                self.pw.enableAutoRange()
            self.pw.clear()


            if (self.text2.text() == "-" or self.text3.text() == "-" or self.text3.text() == "." or self.text2.text() == "."):
                self.list_errors.append("Invalid Range")
                self.e = True
            else:
                min_num = float(self.text2.text())
                max_num = float(self.text3.text())
                if min_num >= max_num:
                    self.error_add("Invalid Range")
                    self.e = True
                else:
                    range = np.linspace(min_num, max_num, 2000)
                    if "x" not in self.text1.text()  and self.text1.text()!="":
                            try:
                                if self.s == "light":
                                    self.pw.plot(range, np.ones(len(range)) * eval(self.text1.text()), pen=pg.mkPen(color=(140, 140, 140), width=2))
                                else:
                                    self.pw.plot(range, np.ones(len(range)) * eval(self.text1.text()), pen=pg.mkPen(color="w", width=2))
                            except ZeroDivisionError:
                                self.error_add("Cannot divide by Zero")
                                self.d = True
                            except FloatingPointError:
                                self.error_add("Undefined")

                                self.d = True
                            except ValueError:
                                self.error_add("Math Error")

                                self.d = True
                            except:
                                self.error_add("Syntax Error")

                                self.d = True
                            else:
                                self.error("Cannot divide by Zero")
                                self.error("Undefined")
                                self.error("Math Error")
                                self.error("Syntax Error")
                                self.d = False
                    else:
                        y = func(range)
                        if self.s == "light":
                            self.pw.plot(range, y, pen=pg.mkPen(color=(140, 140, 140), width=2))
                            self.error("Invalid Range")
                            self.error("No Min Value")
                            self.error("No Max Value")
                        else:
                            self.pw.plot(range, y, pen=pg.mkPen(color="w", width=2))
                            self.error("Invalid Range")
                            self.error("No Min Value")
                            self.error("No Max Value")
                        self.e = False
        else:
            if ( self.text3.text() == "" and self.c == True) :
                self.pw.clear()
                self.e = True
                self.error_add("No Max Value")
            elif ( self.text3.text() != "" and self.c == True):
                self.error("No Max Value")
            if (self.text2.text() == "" and self.b == True):
                self.pw.clear()
                self.e = True
                self.error_add("No Min Value")
            elif (self.text2.text() != "" and self.b == True):
                self.error("No Min Value")

    def error(self,type):
        if type in self.list_errors:
            self.list_errors.remove(type)
        if len(self.list_errors)==0:
            self.label4.setText("")
        else:
            self.label4.setText(self.list_errors[len(self.list_errors)-1])
    def error_add(self,error):
        if error in self.list_errors:
            pass
        else:
            self.list_errors.append(error)
            self.label4.setText(self.list_errors[len(self.list_errors)-1])

    def reset(self):
        self.pw.clear()
        if self.text4.text() == "" and self.text5.text() == "" and self.text6.text() == "" and self.text7.text() == "":
            self.pw.setXRange(0, 1)
            self.pw.setYRange(0, 1)
        self.check1 = True
        self.check2 = True
        self.check3 = True
        self.text1.setText("")
        self.text2.setText("")
        self.text3.setText("")
        self.a = False
        self.b = False
        self.c = False
        self.text1.setFocus()
        self.d = False
        self.e = False
        self.error("Invalid Range")
        self.error("No Min Value")
        self.error("No Max Value")
        self.error("Cannot divide by Zero")
        self.error("Undefined")
        self.error("Math Error")
        self.error("Syntax Error")
        self.error('F(x) is not a Function of x')
        self.error("No Function to draw")

    def focus_text1(self):
        self.text2.setFocus()

    def focus_text2(self):
        self.text3.setFocus()

    def focus_text3(self):
        self.text1.setFocus()

    def focus_text4(self):
        self.text5.setFocus()

    def focus_text5(self):
        self.text6.setFocus()

    def focus_text6(self):
        self.text7.setFocus()

    def focus_text7(self):
        self.text4.setFocus()

    def save(self):
        pass

    def information_dialog(self):
        if self.check_text==False:
            if self.s=="dark":
                self.gbox6.setTitle("Help")
                self.gbox6.setStyleSheet("QGroupBox {border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
                self.text8.setStyleSheet("border:None;background-color:#383838;border:None;color: " + self.font_color_black)
                self.text8.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
                self.text8.setText("--> The following operators must be used when writting the function:\n( - + / ^ ( ) ).\n\n--> The program supports the following functions and must be written as:"
                                   "\nsin(x),cos(x),tan(x),arccos(x),\narcsin(x),arctan(x),cosh(x),sinh(x),\ntanh(x),exp(x),sqrt(X),cbrt(x),\n"
                                   "log10(x),ln(x) and polynomial and rational functions."
                                   "\n\n--> The 'A' button in the Range box sets the x-axis and y-axis ranges to the appropriate values according to the values of the function.\n\n" \
                                    "--> To close the Help box just click the help button beside the Export Graph.")
            else:
                self.gbox6.setTitle("Help")
                self.gbox6.setStyleSheet("QGroupBox {border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
                self.text8.setStyleSheet("border:None;background-color:#f5f6f7;color: " + self.font_color)
                self.text8.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
                self.text8.setText("--> The following operators must be used when writting the function:\n( - + / ^ ( ) ).\n\n--> The program supports the following functions and must be written as:"
                                   "\nsin(x),cos(x),tan(x),arccos(x),\narcsin(x),arctan(x),cosh(x),sinh(x),\ntanh(x),exp(x),sqrt(X),cbrt(x),\n"
                                   "log10(x),ln(x) and polynomial and rational functions."
                                   "\n\n--> The 'A' button in the Range box sets the x-axis and y-axis ranges to the appropriate values according to the values of the function.\n\n" \
                                    "--> To close the Help box just click the help button beside the Export Graph.")
            self.check_text=True
        else:
            self.gbox6.setStyleSheet("border:None;background-color:rgba(255,255,255,0)")
            self.text8.setStyleSheet("border:None;background-color:rgba(255,255,255,0)")
            self.text8.setText("")
            self.gbox6.setTitle("")
            self.check_text=False





    def auto_mode(self):
        self.text4.setText("")
        self.text5.setText("")
        self.text6.setText("")
        self.text7.setText("")
        self.f = False
        self.g = False
        self.check_yrange == False
        self.check_xrange == False
        self.xrange()
        self.yrange()


    def dark_mode(self):
        self.input.setMaximumWidth(250)
        self.input.setFixedSize(250, 150)
        self.gbox.setMaximumWidth(250)
        self.gbox.setFixedSize(250, 90)
        self.gbox3.setMaximumWidth(250)
        self.gbox3.setFixedSize(250, 90)
        self.gbox4.setMaximumWidth(250)
        self.gbox4.setFixedSize(250, 45)
        self.gbox_mode.setMaximumWidth(250)
        self.gbox_mode.setFixedSize(250, 50)
        self.gbox5.setMaximumWidth(270)
        self.input.setObjectName("input")
        self.input.setStyleSheet("QGroupBox#input{border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox#input::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox.setStyleSheet("QGroupBox {border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox4.setStyleSheet("QGroupBox {border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox_mode.setStyleSheet("QGroupBox {border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.plot.setStyleSheet("color: " + self.font_color)
        self.setStyleSheet("background-color:#202020")
        self.label1.setStyleSheet("background-color:#383838;border:None;color: " + self.font_color_black)
        self.label2.setStyleSheet("background-color:#383838;border:None;color:" + self.font_color_black)
        self.label3.setStyleSheet("background-color:#383838;border:None;color:" + self.font_color_black)
        self.label4.setStyleSheet("background-color:#383838;border:None;color:"+ self.font_color_black)
        self.label5.setStyleSheet("background-color:#383838;border:None;color:" + self.font_color_black)
        self.label6.setStyleSheet("background-color:#383838;border:None;color:" + self.font_color_black)
        self.rbutton1.setStyleSheet("background-color:#383838;color:" + self.font_color_black)
        self.rbutton2.setStyleSheet("background-color:#383838;color:" + self.font_color_black)
        self.rbutton1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.rbutton2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label3.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label4.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label5.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label6.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text1.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text2.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text3.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text4.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text5.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text6.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.text7.setStyleSheet("border:1px solid #5b5b5b;background-color:#383838;color:" + self.font_color_black)
        self.button_save.setStyleSheet(
            " QPushButton{border: 1px solid #f0f0f0;Text-align:center;background:#333333; color:#f0f0f0}"
            "QPushButton::hover{border: 1px solid #f0f0f0;Text-align:center;background:#2c2c2c}"
            "QPushButton::Pressed{border: 1px solid #f0f0f0;Text-align:center;background:#3d3c3c}")
        self.button.setStyleSheet(
            " QPushButton{border: 1px solid #f0f0f0;Text-align:center;background:#333333; color:#f0f0f0}"
            "QPushButton::hover{border: 1px solid #f0f0f0;Text-align:center;background:#2c2c2c}"
            "QPushButton::Pressed{border: 1px solid #f0f0f0;Text-align:center;background:#3d3c3c}")
        self.text1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text3.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text4.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text5.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text6.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text7.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.gbox5.setObjectName("GroupBox")
        self.gbox5.setStyleSheet("QGroupBox#GroupBox{border: None;background-color:#383838}")
        f = open("plotter.txt", "w")
        f.write("dark")
        f.close()
        self.s = "dark"
        self.pw.setBackground(background=None)
        if self.after == True:
            self.plotx()
        pixmap1 = QPixmap("auto-button_dark.png")
        button_icon1 = QIcon(pixmap1)
        self.button_2.setStyleSheet("border:none;background-color:#383838")
        self.button_2.setIcon(button_icon1)
        pixmap2 = QPixmap("help_dark.png")
        button_icon2 = QIcon(pixmap2)
        self.button_help.setIcon(button_icon2)
        self.button_help.setStyleSheet("border:none;background-color:#383838")
        if self.check_text==True:
            self.gbox6.setStyleSheet("QGroupBox {border: 2px solid #3d3d3d;background-color:#383838;color: " + self.font_color_black+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
            self.text8.setStyleSheet("border:None;background-color:#383838;border:None;color: " + self.font_color_black)
            self.text8.setFont(QFont(self.font_type, self.font_size, QFont.Normal))


    def light_mode(self):
        self.input.setMaximumWidth(250)
        self.input.setFixedSize(250, 150)
        self.gbox.setMaximumWidth(250)
        self.gbox.setFixedSize(250, 90)
        self.gbox3.setMaximumWidth(250)
        self.gbox3.setFixedSize(250, 90)
        self.gbox4.setMaximumWidth(250)
        self.gbox4.setFixedSize(250, 45)
        self.gbox_mode.setMaximumWidth(250)
        self.gbox_mode.setFixedSize(250, 50)
        self.gbox5.setMaximumWidth(270)
        self.input.setObjectName("input")
        self.input.setStyleSheet("QGroupBox#input{border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox#input::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox.setStyleSheet("QGroupBox {border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox4.setStyleSheet("QGroupBox {border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.gbox_mode.setStyleSheet("QGroupBox {border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
        self.plot.setStyleSheet("color: " + self.font_color)
        self.setStyleSheet("background-color:white;")
        self.label1.setStyleSheet("background-color:#f5f6f7;color: " + self.font_color)
        self.label2.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.label3.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.label4.setStyleSheet("background-color:#f5f6f7;color:"+ self.font_color)
        self.label5.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.label6.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.rbutton1.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.rbutton2.setStyleSheet("background-color:#f5f6f7;color:" + self.font_color)
        self.rbutton1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.rbutton2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label3.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label4.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label5.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.label6.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text1.setStyleSheet("background-color:white")
        self.text2.setStyleSheet("background-color:white")
        self.text3.setStyleSheet("background-color:white")
        self.text4.setStyleSheet("background-color:white")
        self.text5.setStyleSheet("background-color:white")
        self.text6.setStyleSheet("background-color:white")
        self.text7.setStyleSheet("background-color:white")
        self.button_save.setStyleSheet(
            " QPushButton{border: 1px solid #adadad;Text-align:center;background:#e1e1e1; color:black}"
            "QPushButton::hover{border: 1px solid #adadad;Text-align:center;background:#d8d7d7}"
            "QPushButton::Pressed{border: 1px solid #adadad;Text-align:center;background:#f5f6f7}")
        self.button.setStyleSheet(
            " QPushButton{border: 1px solid #adadad;Text-align:center;background:#e1e1e1; color:black}"
            "QPushButton::hover{border: 1px solid #adadad;Text-align:center;background:#d8d7d7}"
            "QPushButton::Pressed{border: 1px solid #adadad;Text-align:center;background:#f5f6f7}")
        self.text1.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text2.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text3.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text4.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text5.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text6.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.text7.setFont(QFont(self.font_type, self.font_size, QFont.Normal))
        self.gbox5.setObjectName("GroupBox")
        self.gbox5.setStyleSheet("QGroupBox#GroupBox{border: None;background-color:#f5f6f7}")
        f = open("plotter.txt", "w")
        f.write("light")
        f.close()
        self.s = "light"
        self.pw.setBackground(background=None)
        if self.after == True:
            self.plotx()
        pixmap2 = QPixmap("auto-button.png")
        button_icon2 = QIcon(pixmap2)
        self.button_2.setStyleSheet("border:none;background-color:#f5f6f7")
        self.button_2.setIcon(button_icon2)
        pixmap2 = QPixmap("help_light.png")
        button_icon2 = QIcon(pixmap2)
        self.button_help.setIcon(button_icon2)
        self.button_help.setStyleSheet("border:none;background-color:#f5f6f7")
        if self.check_text==True:
            self.gbox6.setStyleSheet("QGroupBox {border: 2px solid #e6e6e6;background-color:#f5f6f7;color: " + self.font_color+";margin-top: 6px;}"+"QGroupBox::title {subcontrol-origin:margin;left:8px;padding: 0px 0px 0px 0px;}")
            self.text8.setStyleSheet("border:None;background-color:#f5f6f7;color: " + self.font_color)
            self.text8.setFont(QFont(self.font_type, self.font_size, QFont.Normal))




    def export(self):
        self.exportdialog = exportDialog.ExportDialog(self.pw.plotItem.scene())
        name = QFileDialog.getSaveFileName(self, 'Save File',"","PNG (*.PNG;*.PNG);;CSV (*.CSV);;SVG(*.SVG)","",QFileDialog.Options())
        if name[0]!="":
            if "PNG" in name[1]:
                if self.s=="dark":
                    self.pw.setBackground(background=(0,0,0))
                else:
                    self.pw.setBackground(background=(255,255,255))
                exporter = pg.exporters.ImageExporter(self.pw.plotItem)
                exporter.export(name[0])
                self.pw.setBackground(background=None)
            elif "CSV" in name[1]:
                exporter= pg.exporters.CSVExporter(self.pw.plotItem)
                exporter.export(name[0])
            elif "SVG" in name[1]:
                if self.s=="dark":
                    self.pw.setBackground(background=(0,0,0))
                else:
                    self.pw.setBackground(background=(255,255,255))
                exporter= pg.exporters.SVGExporter(self.pw.plotItem)
                exporter.export(name[0])
                self.pw.setBackground(background=None)


myapp = QApplication(sys.argv)
window = Window()
window.show()
myapp.exec_()
sys.exit()

