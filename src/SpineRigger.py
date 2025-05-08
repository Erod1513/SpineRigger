from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget  
from PySide2.QtCore import Qt, Signal 
from maya.OpenMaya import MVector
import maya.OpenMayaUI as omui
import maya.mel as mel
import shiboken2 


def GetMayaMainWindow() -> QMainWindow:
     mainWindow = omui.MQtUtil.mainWindow()
     return shiboken2.wrapInstance(int(mainWindow), QMainWindow)

def DeleteWidgetWithName(name):
     for widget in GetMayaMainWindow().findChildren(QWidget, name):
          widget.deleteLater()

class MayaWindow(QWidget):
     def __init__(self):
          super().__init__(parent = GetMayaMainWindow())
          DeleteWidgetWithName(self.GetWidgetUniqueName())
          self.setWindowFlags(Qt.WindowType.Window)
          self.setObjectName(self.GetWidgetUniqueName())

     def GetWidgetUniqueName(self):
          return "jfhgiergbejnfgouefghrgkg"
     
import maya.cmds as mc

class SpineRigger:
     def __init__(self):
        self.root = ""
        self.sec = ""
        self.mid = ""
        self.fourth = ""
        self.end = ""
        self.controllerSize = 5
        self.controllerColor = [0,0,0]
        
     def SetColorOverride(self, objName, color: list[float]):
          mc.setAttr(objName + ".overrideEnabled", 1)
          mc.setAttr(objName + ".overrideRGBColors", 1)
          mc.setAttr(objName + ".overrideColorRGB", color[0], color[1], color[2], type="float3")


     def FindJointBasedOnSelection(self):
          try:
               self.root = mc.ls(sl = True, type = "joint") [0]
               self.sec = mc.listRelatives(self.root, c = True, type = "joint")[0]
               self.mid = mc.listRelatives(self.sec, c= True, type = "joint")[0]
               self.fourth = mc.listRelatives(self.mid, c= True, type = "joint")[0]
               self.end = mc.listRelatives(self.fourth, c = True, type = "joint")[0]
          except Exception as e:
               raise Exception ("wrong selection was made, please select the joint of the spine")
    
     def CreateFKControllerForJoint(self, jntName):
          ctrlName = "ac_l_fk_" + jntName
          ctrlGrpName = ctrlName + "_grp"
          mc.circle(name = ctrlName, radius = self.controllerSize, normal = (1,0,0))
          mc.group(ctrlName, n=ctrlGrpName)
          mc.matchTransform(ctrlGrpName, jntName)
          mc.orientConstraint(ctrlName, jntName)
          return ctrlName, ctrlGrpName
     


     def CreateCircleController(self, name):
          mc.circle(n=name, nr=(0,1,0), r=self.controllerSize)
          mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
          mc.makeIdentity(name, apply = True)
          grpName = name + "_grp"
          mc.group(name, n = grpName)
          return name, grpName
     
     def CreatePlusController(self, name):
          mel.eval(f"curve -n {name}-d 1 -p -0.94418 8.995776 0 -p 1.025536 8.977017 0 -p 1.025536 7.926502 0 -p 1.963496 7.945261 0 -p 1.963496 6.013063 0 -p 0.988018 6.013063 0 -p 0.988018 4.962547 0 -p -1.019217 5.000066 0 -p -1.000458 6.031822 0 -p -1.975936 6.031822 0 -p -1.957177 7.945261 0 -p -0.962939 7.926502 0 -p -0.94418 8.977017 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;")
          grpName = name + "_grp"
          mc.group(name, n = grpName)
          return name, grpName
     
     def GetObjectLocation(self, objectName):
          x,y,z = mc.xform(objectName, q = True, ws= True, t = True)
          return MVector(x,y,z)
     
     def PrintVector(self, vector):
          print(f"<{vector.x}, {vector.y}, {vector.z}>")

     def SpineRig(self):
          rootCtrl, rootCtrlGrp = self.CreateFKControllerForJoint(self.root)
          secCtrl, secCtrlGrp = self.CreateFKControllerForJoint(self.sec)
          midCtrl, midCtrlGrp = self.CreateFKControllerForJoint(self.mid)
          fourthCtrl, fourthCtrlGrp = self.CreateFKControllerForJoint(self.fourth)
          endCtrl, endCtrlGrp = self.CreateFKControllerForJoint(self.end)

          mc.parent(secCtrlGrp, rootCtrl)
          mc.parent(midCtrlGrp, secCtrl)
          mc.parent(fourthCtrlGrp, midCtrl)
          mc.parent(endCtrlGrp, fourthCtrl)

     

          #ikEndCtrl = "ac_ik_" + self.end
          #ikEndCtrl, ikEndCtrlGrp = self.CreateCircleController(ikEndCtrl)
          #mc.matchTransform(ikEndCtrlGrp, self.end)
          #endOrientContraint = mc.orientConstraint(ikEndCtrl, self.end)[0]

          #rootJntLoc = self.GetObjectLocation(self.root)
          #self.PrintVector(rootJntLoc)

          #ikHandleName = "ikHandle_" + self.end
          #mc.ikHandle(n=ikHandleName, sol = "ikRPsolver", sj = self.root, ee = self.end)
          
          #poleVectorLocationVals = mc.getAttr(ikHandleName + ".poleVector")[0]
          #poleVector = MVector(poleVectorLocationVals[0], poleVectorLocationVals[1], poleVectorLocationVals[2])
          #poleVector.normalize()

          #endJntLoc = self.GetObjectLocation(self.end)
          #rootToEndVector = endJntLoc - rootJntLoc

          #poleVectorCtrlLoc = rootJntLoc + rootToEndVector / 2 + poleVector * rootToEndVector.length()
          #poleVectorCtrl = "ac_ik_" + self.mid
          #mc.spaceLocator(n=poleVectorCtrl)
          #poleVectorCtrlGrp = poleVectorCtrl + "_grp"
          #mc.group(poleVectorCtrl, n=poleVectorCtrlGrp)
          #mc.setAttr(poleVectorCtrlGrp + ".t", poleVectorCtrlLoc.x, poleVectorCtrlLoc.y, poleVectorCtrlLoc.z, typ= "double3")

          #mc.poleVectorConstraint(poleVectorCtrlLoc, ikHandleName)
          
          #ikfkBlendCtrl = "ac_ikfk_blend_" + self.root
          #ikfkBlendCtrl, ikfkBlendCtrlGrp = self.CreatePlusController(ikfkBlendCtrl)
          #mc.setAttr(ikfkBlendCtrlGrp + ".t", rootJntLoc.x*2, rootJntLoc.y, rootJntLoc.z*2, typ="double3")

          #ikfkBlendAttrName = "sc_ikfkBlend"
          #mc.addAttr(ikfkBlendCtrl, ln=ikfkBlendAttrName, min = 0, max= 1, k=True)
          #ikfkBlendAttr = ikfkBlendCtrl + "." + ikfkBlendAttrName

          #mc.expression(s=f"{ikHandleName}.ikBlend={ikfkBlendAttr}")
          #mc.expression(s=f"{ikEndCtrlGrp}. v={poleVectorCtrlGrp}.v={ikfkBlendAttr}")
          #mc.expression(s=f"{rootCtrlGrp}.v=1-{ikfkBlendAttr}")
          #mc.expression(s=f"{endOrientContraint}.{endCtrl}W0 = 1-{ikfkBlendAttr}")
          #mc.expression(s=f"{endOrientContraint}.{ikEndCtrl}W1 = {ikfkBlendAttr}")

          #topGrpName = f"{self.root}_rig_grp"
          #mc.group({rootCtrlGrp,ikEndCtrlGrp,poleVectorCtrlGrp,ikfkBlendCtrlGrp}, n= topGrpName)
          #mc.parent(ikHandleName,ikEndCtrl)
 
          #mc.setAttr(topGrpName+".overrideEnabled", 1)
          #mc.setAttr(topGrpName+".overrideGBColors",1)
          #mc.setAttr(topGrpName+"overrideColorRGB", self.controllerColor[0], self.controllerColor[1],self.controllerColor[2], type = "double3")

          self.SetColorOverride(rootCtrlGrp, self.controllerColor)

class ColorPicker(QWidget):
     colorChanged = Signal(QColor)
     def __init__(self):
          super().__init__()
          self.masterLayout = QVBoxLayout()
          self.setLayout(self.masterLayout)
          self.pickColorBtn = QPushButton()
          self.pickColorBtn.setStyleSheet(f"background-color:black")
          self.masterLayout.addWidget(self.pickColorBtn)
          self.pickColorBtn.clicked.connect(self.PickColorBtnClicked)
     
     def PickColorBtnClicked(self):
          self.color = QColorDialog.getColor()
          self.pickColorBtn.setStyleSheet(f"background-color:{self.color.name()}")
          self.colorChanged.emit(self.color)
          self.color = QColor(0,0,0)


class SpineRiggerWidget(MayaWindow):
     def __init__(self):
          super().__init__()
          self.rigger = SpineRigger()
          self.setWindowTitle("Spine Rigger")

          self.masterLayout = QVBoxLayout()
          self.setLayout(self.masterLayout)

          toolTipLabel = QLabel("select the first joint of the spine, and press the auto find button")
          self.masterLayout.addWidget(toolTipLabel)

          self.jntsListLineEdit = QLineEdit()
          self.masterLayout.addWidget(self.jntsListLineEdit)
          self.jntsListLineEdit.setEnabled(False)

          autoFindJntBtn = QPushButton("Auto Find")
          autoFindJntBtn.clicked.connect(self.AutoFindJntBtnClicked)
          self.masterLayout.addWidget(autoFindJntBtn)

          ctrlSizeSlider = QSlider()
          ctrlSizeSlider.setOrientation(Qt.Horizontal)
          ctrlSizeSlider.setRange(1,30)
          ctrlSizeSlider.setValue(self.rigger.controllerSize)
          self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
          ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)

          colorPicker = ColorPicker()
          colorPicker.colorChanged.connect(self.ColorPickerChanged)
          self.masterLayout.addWidget(colorPicker)

          ctrlSizeLayout = QHBoxLayout()
          ctrlSizeLayout.addWidget(ctrlSizeSlider)
          ctrlSizeLayout.addWidget(self.ctrlSizeLabel)
          self.masterLayout.addLayout(ctrlSizeLayout)

          rigLimbBtn = QPushButton("rig spine")
          rigLimbBtn.clicked.connect(lambda:self.rigger.SpineRig())
          self.masterLayout.addWidget(rigLimbBtn)

     def ColorPickerChanged(self, newColor: QColor):
          self.rigger.controllerColor[0] = newColor.redF()
          self.rigger.controllerColor[1] = newColor.greenF()
          self.rigger.controllerColor[2] = newColor.blueF()

     def CtrlSizeSliderChanged(self, newValue):
        self.ctrlSizeLabel.setText(f"{newValue}")
        self.rigger.controllerSize = newValue

     def AutoFindJntBtnClicked(self):
        try:
            self.rigger.FindJointBasedOnSelection()
            self.jntsListLineEdit.setText(f"{self.rigger.root},{self.rigger.sec},{self.rigger.mid},{self.rigger.fourth},{self.rigger.end}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}") 


spineRigger = SpineRiggerWidget() 
spineRigger.show()   

GetMayaMainWindow() #Update Code for Spine 
