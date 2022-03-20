import sys
import os
import threading
from playsound import playsound
from PyQt5 import QtCore,QtWidgets,QtGui
from Ui_ring import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.timeEdit.setTime(QtCore.QTime.currentTime())
        self.timeEdit.setDisplayFormat("hh:mm:ss")
        self.btnappend.clicked.connect(self.appendname)
        self.btnchoose.clicked.connect(self.choosefile)
        self.rbtrepeat.toggled.connect(self.rbtstate)
        self.rbtonce.toggled.connect(self.rbtstate)
        self.rbtrepeat.setChecked(True)
        self.btndel.clicked.connect(self.delring)
        self.btnsort.clicked.connect(self.sortring)
        self.btnplay.clicked.connect(self.tplayring)
        self.cbox6.stateChanged.connect(self.cbstate)
        self.cbox7.stateChanged.connect(self.cbstate)
        self.cbox6.setChecked(False)
        #print(self.cbox6.isChecked())        
        if not os.path.exists("ring.txt"):
            with open("ring.txt","w") as f:
                f.write("")
        self.statusBar.showMessage("就绪")
        
    def cbstate(self,cb):
        sender=self.sender()
        #print(sender.text(),cb)
    def playring(self,s):   
        list0=[]
        list1=[]
        list2=[]
        list3=[]
        list4=[]       
        strlist=""

        with open("ring.txt","r") as f:
            for line in f.readlines():
                line=eval(line.strip("\n"))
                list0.append(line[0])
                list1.append(line[1])
                list2.append(line[2])
                list3.append(line[3])
                list4.append(line[4])             
        while True:
            QtWidgets.QApplication.processEvents()
            dtnow=QtCore.QTime.currentTime().toString("hh:mm:ss")   
            dtdate=QtCore.QDate.currentDate().toString("yyyy-MM-dd")
            dtweek=QtCore.QDateTime.currentDateTime().toString("dddd")
            #print(dtnow)        
            #print(dtweek            
            for dt in list2:
                isonce=list4[list2.index(dt)]              
                if isonce==1:         
                    if dtnow==dt:                            
                        s=list3[list2.index(dt)]
                        #print(s)
                        if (dtweek=="星期六" and not self.cbox6.isChecked())  or (dtweek=="星期日" and not self.cbox7.isChecked()):
                            pass
                        else:
                            playsound(s)
                else:
                    if dtnow==dt and dtdate==list1[list2.index(dt)]:                            
                        s=list3[list2.index(dt)]
                        #print(s)
                        if (dtweek=="星期六" and not self.cbox6.isChecked())  or (dtweek=="星期日" and not self.cbox7.isChecked()):
                            pass
                        else:
                            playsound(s)

    def tplayring(self,s):    
        self.statusBar.showMessage("正在播放...")    
        t=threading.Thread(target=self.playring(s))
        t.start()
        

    def sortring(self):
        list0=[]
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        listid=[]
        list0s=[]
        list1s=[]
        list2s=[]
        list3s=[]
        list4s=[]
        strlist=""
        with open("ring.txt","r") as f:
            for line in f.readlines():
                line=eval(line.strip("\n"))
                list0.append(line[0])
                list1.append(line[1])
                list2.append(line[2])
                list3.append(line[3])
                list4.append(line[4])
        #print(list2)
        list2s=list2[:]
        list2s.sort()
        #print(list2,list2s)
        for v in list2s:
            listid.append(list2.index(v)) 
        #print(listid)
        for id in listid:
            list0s.append(list0[id])
            list1s.append(list1[id])
            list3s.append(list3[id])
            list4s.append(list4[id])
        
        for i in range(len(listid)):
            line=[list0s[i],list1s[i],list2s[i],list3s[i],list4s[i]]
            strlist=strlist+str(line)+"\n"        
        with open("ring.txt","w") as f:
            f.write(strlist)

        self.opentxt("ring.txt")


        
    def delring(self):
        list0=[]
        strlist=""
        listid=self.listname.currentIndex().row()
        strname=self.listname.currentIndex().data()
        #print(listid,strname)

        with open("ring.txt","r") as f:
            for line in f.readlines():
                line=eval(line.strip("\n"))
                if strname!=line[0]:
                    list0.append(line)
        for line in list0:
            strlist=strlist+str(line)+"\n"        
        with open("ring.txt","w") as f:
            f.write(strlist)

        self.opentxt("ring.txt")



    def choosefile(self):
        file,ok=QtWidgets.QFileDialog.getOpenFileName(self,"选择铃声文件",os.getcwd(),"mp3文件(*.mp3);;wav文件(*.wav)")
        self.ringfile.setText(file) 

    bflag=1
    def rbtstate(self,rbtn):
        global bflag
        sender=self.sender()        
        #print(sender.objectName())
        if rbtn:
            if sender.text()=="每天":
                bflag=1
            if sender.text()=="单次":
                bflag=0
        else:
            if sender.text()=="每天":
                pass
            if sender.text()=="单次":
                pass
    
    def savetxt(self,filename,txtrec):
        with open(filename,"a") as f:
            f.write(txtrec+"\n")

    def opentxt(self,filename):  
        list1=[]
        list2=[]
        list3=[]      
        with open(filename,"r") as f:
            data=f.readlines()
            for line in data:
                line=eval(line.strip("\n"))                
                list1.append(line[0])
                list2.append(line[1]+" "+line[2])
                list3.append(line[3])
            
            slm1=QtCore.QStringListModel()
            slm1.setStringList(list1)
            slm2=QtCore.QStringListModel()
            slm2.setStringList(list2)
            slm3=QtCore.QStringListModel()
            slm3.setStringList(list3)
            self.listname.setModel(slm1)
            self.listdt.setModel(slm2)
            self.listfile.setModel(slm3)

    def appendname(self):
        global bflag
        rname=self.ringname.text()
        ddate=self.dateEdit.date().toString("yyyy-MM-dd")
        dtime=self.timeEdit.time().toString("hh:mm:ss")
        ddatetime=QtCore.QDateTime()
        ddatetime.setDate(self.dateEdit.date())
        ddatetime.setTime(self.timeEdit.time())
        #print(bflag)              
        #print(ddatetime.toString("yyyy-MM-dd dddd HH:mm:ss"))
        #print(ddatetime.toString("dddd"))
        rfile=self.ringfile.text()
        
        if rname=="":
            QtWidgets.QMessageBox.information(self,"错误","铃声名称不能为空")
        elif rfile=="":
            QtWidgets.QMessageBox.information(self,"错误","铃声文件不能为空")
        else:
            #print(rname,ddate,dtime,rfile)
            self.label.setText(ddate+" "+ dtime)
            self.label.adjustSize()                      
            rlist=str([rname,ddate,dtime,rfile,bflag])
            #print(rlist)
            self.savetxt("ring.txt",rlist)
        self.opentxt("ring.txt")
            
    
    
        
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    mywin=MainWindow()
    mywin.setWindowTitle("铃声播放系统")
    mywin.opentxt("ring.txt")
    mywin.setFixedSize(mywin.width(),mywin.height())
    mywin.show()
    sys.exit(app.exec())