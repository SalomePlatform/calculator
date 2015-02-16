# Copyright (C) 2007-2015  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import string

import salome

import SALOME_MED

#CCRTfrom libSALOME_Swig import *
#CCRTsg = SALOMEGUI_Swig()

#CCRT :
import SALOMEDS

import os
host = os.getenv( 'HOST' )
orb, lcc, naming_service, contmgr = salome.salome_kernel.salome_kernel_init()
obj = naming_service.Resolve('myStudyManager')
myStudyManager = obj._narrow(SALOMEDS.StudyManager)
print "studyManager found"
myStudy = myStudyManager.NewStudy('medClient_withoutIHM_test')
studynameId = myStudy._get_StudyId()
studyname = myStudy._get_Name()
print "We are working in the study ",studyname," with the ID ",studynameId
#endCCRT

def print_ord(i):
    if i == 0:
        return 'first'
    elif i == 1:
        return 'second'
    elif i == 2:
        return 'third'
    else:
        return `(i+1)`+'th'

def changeBlankToUnderScore(stringWithBlank):
    blank = ' '
    underscore = '_'
    decompString = string.split(stringWithBlank,blank)
    length = len(decompString)
    stringWithUnderScore = decompString[0]
    for i in range(1,length):
        stringWithUnderScore += underscore
        stringWithUnderScore += decompString[i]
    return stringWithUnderScore

def getMedObjectFromStudy(file):
    objNameInStudy = "MED_OBJECT_FROM_FILE_"+file
    compNameInStudy= "MED"
    #CCRTlistOfSO = salome.myStudy.FindObjectByName(objNameInStudy,compNameInStudy)
    listOfSO = myStudy.FindObjectByName(objNameInStudy,compNameInStudy)
    listLength = len(listOfSO)
    if (listLength == 0) :
        print "getMedObjectFromStudy",objNameInStudy," cannot be found in the Study under the component ",compNameInStudy
        return None
    elif (listLength > 1) :
        print "there are more than one instance of ",objNameInStudy," in the Study under the component ",compNameInStudy
        return None
    mySO = listOfSO[0]
    if (mySO == None) :
        print "getMedObjectFromStudy",objNameInStudy," cannot be found in the Study"
        return mySO
    else:
        anAttr = mySO.FindAttribute("AttributeIOR")[1]
        #CCRTobj = salome.orb.string_to_object(anAttr.Value())
        obj = orb.string_to_object(anAttr.Value())
        myObj = obj._narrow(SALOME_MED.MED)
        if (myObj == None) :
            print objNameInStudy," has been found in the Study but with the wrong type"
        return myObj

def getMeshObjectFromStudy(meshName):
    objNameInStudy = "/Med/MEDMESH/"+meshName
    #CCRTmySO = salome.myStudy.FindObjectByPath(objNameInStudy)
    mySO = myStudy.FindObjectByPath(objNameInStudy)
    if (mySO == None) :
        print "getMeshObjectFromStudy",objNameInStudy," cannot be found in the Study"
        return mySO
    else:
        anAttr = mySO.FindAttribute("AttributeIOR")[1]
        #CCRTobj = salome.orb.string_to_object(anAttr.Value())
        obj = orb.string_to_object(anAttr.Value())
        myObj = obj._narrow(SALOME_MED.MESH)
        if (myObj == None) :
            print objNameInStudy," has been found in the Study but with the wrong type"
        return myObj

def getSupportObjectFromStudy(meshName,supportName):
    meshNameStudy = changeBlankToUnderScore(meshName)
    objNameInStudy = "/Med/MEDMESH/MEDSUPPORTS_OF_"+meshNameStudy+"/"+supportName
    #CCRTmySO = salome.myStudy.FindObjectByPath(objNameInStudy)
    mySO = myStudy.FindObjectByPath(objNameInStudy)
    if (mySO == None) :
        print "getSupportObjectFromStudy",objNameInStudy," cannot be found in the Study"
        print "/Med/MEDMESH/MEDSUPPORTS_OF_"+meshNameStudy,":",myStudy.GetObjectNames("/Med/MEDMESH/MEDSUPPORTS_OF_"+meshNameStudy)
        return mySO
    else:
        anAttr = mySO.FindAttribute("AttributeIOR")[1]
        #CCRTobj = salome.orb.string_to_object(anAttr.Value())
        obj = orb.string_to_object(anAttr.Value())
        myObj = obj._narrow(SALOME_MED.SUPPORT)
        if (myObj == None) :
            print objNameInStudy," has been found in the Study but with the wrong type"
        return myObj

def getFieldObjectFromStudy(dt,it,fieldName,supportName,meshName):
    type = -1
    meshNameStudy = changeBlankToUnderScore(meshName)
    objNameInStudy = "/Med/MEDFIELD/"+fieldName+"/("+str(dt)+","+str(it)+")_ON_"+supportName+"_OF_"+meshNameStudy
    #CCRTmySO = salome.myStudy.FindObjectByPath(objNameInStudy)
    mySO = myStudy.FindObjectByPath(objNameInStudy)
    if (mySO == None) :
        print "getFieldObjectFromStudy",objNameInStudy," cannot be found in the Study"
        print "/Med/MEDFIELD/"+fieldName,":",myStudy.GetObjectNames("/Med/MEDFIELD/"+fieldName)
        return -1,-1
    else:
        anAttr = mySO.FindAttribute("AttributeIOR")[1]
        #CCRTobj = salome.orb.string_to_object(anAttr.Value())
        obj = orb.string_to_object(anAttr.Value())
        myObj = obj._narrow(SALOME_MED.FIELDINT)
        type = 0
        if (myObj == None):
            myObj = obj._narrow(SALOME_MED.FIELDDOUBLE)
            type = 1
            if (myObj == None) :
                print objNameInStudy," has been found in the Study but with the wrong type"
        return myObj,type


fileName = "pointe.med"

from MEDCoupling import *
from MEDLoader import *
from MEDCouplingCorba import *
from MEDCouplingClient import *
import MEDCouplingCorbaServant_idl

#CCRTmedComp=salome.lcc.FindOrLoadComponent("FactoryServer", "MED")
medComp=lcc.FindOrLoadComponent("FactoryServer", "MED")

import os

filePath=os.environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/med/"

filePathName = filePath + fileName

print "Reading the .med file ",filePathName," and pushing corba objects in the SALOME study"
#CCRTmedComp.readStructFileWithFieldType(filePathName,salome.myStudyName)
##medComp.readStructFileWithFieldType(filePathName,studyname)
#CCRTsg.updateObjBrowser(1)

##print "getting the MED object from the study"
##medObj = getMedObjectFromStudy(fileName)

meshNames = MEDLoader.GetMeshNames(filePathName)
nbOfMeshes = len(meshNames)#medObj.getNumberOfMeshes()

print "in this med file there is(are) ",nbOfMeshes," mesh(es):"

meshName = meshNames[0]

#meshObj = medObj.getMeshByName(meshName)
meshObj3D = MEDLoader.ReadUMeshFromFile(filePathName,meshName,0)

fieldName = "fieldcelldoublevector"
fieldTypedObj = MEDLoader.ReadFieldCell(filePathName,meshName,0,fieldName,-1,-1)
fieldTypedObjCORBA=MEDCouplingFieldDoubleServant._this(fieldTypedObj)

##############  Load Calculator Component ###################
# Calculator Component must be in the Container of MED
#
print "Load Calculator Component "
# we need to import CALCULATOR_ORB to get a typed object (to perform narrowing)
import CALCULATOR_ORB
#CCRTcalculator = salome.lcc.FindOrLoadComponent("FactoryServer", "CALCULATOR")
calculator = lcc.FindOrLoadComponent("FactoryServer", "CALCULATOR")
#

#calculator.printField(fieldTypedObj)

#
#
##############  Test Calculator Component ###################
#
#
print "Appel cloneField : fieldTypedObj -> f1,f2,f3,f4"
#fieldTypedObj.Register()
(f1,f2,f3,f4)=calculator.cloneField(fieldTypedObjCORBA)  # fieldTypedObj is consumed
#
##f1.Register()
##calculator.printField(f1)
print "Add fields f2+f3"
f_add=calculator.add(f2, f3)
##f_add.Register()
##calculator.printField( f_add ) # f_add is consumed

#
print "Apply linear function"
f_lin=calculator.applyLin(f4,2.0,1.0)
##f_lin.Register()
##calculator.printField( f_lin ) # f_lin is consumed
#
print "Appel Norme Max "
#f_lin.Register()
norme=calculator.normMax(f_lin) # f_lin is consumed
print " -> norme = ",norme
#

#
#
############  Creation of a MED file with fields created by Caculator  #################
#                   via Client classes
#
f_addLocal=MEDCouplingFieldDoubleClient.New(f_add)
f_add.UnRegister()
f_addLocal.setName(fieldName+"add")
f_linLocal=MEDCouplingFieldDoubleClient.New(f_lin)
f_lin.UnRegister()
f_linLocal.setName(fieldName+"lin")

meshLocal = f_addLocal.getMesh()

print "      getting information from the local copy of the distant mesh"
name = meshLocal.getName()
spaceDimension = meshLocal.getSpaceDimension()
meshDimension = meshLocal.getMeshDimension()
numberOfNodes = meshLocal.getNumberOfNodes()
print "          Name = ", name, " space Dim = ", spaceDimension, " mesh Dim = ", meshDimension, " Nb of Nodes = ", numberOfNodes


#Warning : OutputMedFiles are removed here after =================================
#Outmed21File="OutCalculatorpointe21_V3.2.0b1.med"
#os.system( 'rm -fr ' + Outmed21File )
Outmed22File="OutCalculatorpointe22_V3.2.0b1.med"
os.system( 'rm -fr ' + Outmed22File )

MEDLoader.WriteUMesh(Outmed22File,meshLocal,True)
MEDLoader.WriteFieldUsingAlreadyWrittenMesh(Outmed22File,f_addLocal)
MEDLoader.WriteFieldUsingAlreadyWrittenMesh(Outmed22File,f_linLocal)

print ""
print "END of the Pyhton script ..... Ctrl D to exit"
