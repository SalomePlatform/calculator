####################################################################################################
# CALCULATOR_TEST_STUDY_WITHOUTIHM.py
#
# Test the calculator component: using Med Client classes with writing in a med file
# results from the calculator component
#
####################################################################################################
from libMEDClient import *

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

#CCRTmedComp=salome.lcc.FindOrLoadComponent("FactoryServer", "MED")
medComp=lcc.FindOrLoadComponent("FactoryServer", "MED")

import os

filePath=os.environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/med/"

filePathName = filePath + fileName

print "Reading the .med file ",filePathName," and pushing corba objects in the SALOME study"
#CCRTmedComp.readStructFileWithFieldType(filePathName,salome.myStudyName)
medComp.readStructFileWithFieldType(filePathName,studyname)
#CCRTsg.updateObjBrowser(1)

print "getting the MED object from the study"
medObj = getMedObjectFromStudy(fileName)

nbOfMeshes = medObj.getNumberOfMeshes()
meshNames = medObj.getMeshNames()

print "in this med file there is(are) ",nbOfMeshes," mesh(es):"

meshName = meshNames[0]

meshObj = medObj.getMeshByName(meshName)

fieldName = "fieldcelldouble"
dt = -1
it = -1
entitySupport = "MED_MAILLE"
supportName = "SupportOnAll_"+entitySupport

fieldTypedObj,typeField = getFieldObjectFromStudy(dt,it,fieldName,supportName,meshName)

if(typeField == 1):
    fieldTypedLocalCopy = FIELDDOUBLEClient(fieldTypedObj)
elif (typeField == 0):
    fieldTypedLocalCopy = FIELDINTClient(fieldTypedObj)
else:
    print "Problem with the type of the field"

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
fieldTypedObj.Register()
(f1,f2,f3,f4)=calculator.cloneField(fieldTypedObj)  # fieldTypedObj is consumed
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
f_lin.Register()
norme=calculator.normMax(f_lin) # f_lin is consumed
print " -> norme = ",norme
#

#
#
############  Creation of a MED file with fields created by Caculator  #################
#                   via Client classes
#

meshDistant = f_add.getSupport().getMesh()

meshLocalCopy = MESHClient(meshDistant)


print "      getting information from the local copy of the distant mesh"
name = meshLocalCopy.getName()
spaceDimension = meshLocalCopy.getSpaceDimension()
meshDimension = meshLocalCopy.getMeshDimension()
numberOfNodes = meshLocalCopy.getNumberOfNodes()
print "          Name = ", name, " space Dim = ", spaceDimension, " mesh Dim = ", meshDimension, " Nb of Nodes = ", numberOfNodes
coordSyst = meshLocalCopy.getCoordinatesSystem()
print "          The coordinates system is",coordSyst
print "          The Coordinates :"
coordNames = []
coordUnits = []
for isd in range(spaceDimension):
    coordNames.append(meshLocalCopy.getCoordinateName(isd))
    coordUnits.append(meshLocalCopy.getCoordinateUnit(isd))

print "          names:", coordNames
print "          units", coordUnits
print "          values:"
coordinates = meshLocalCopy.getCoordinates(MED_FULL_INTERLACE)
for k in range(numberOfNodes):
    kp1 = k+1
    print "         ---- ", coordinates[k*spaceDimension:(kp1*spaceDimension)]
print ""
print "          The Cell Nodal Connectivity of the Cells:"
nbTypesCell = meshLocalCopy.getNumberOfTypes(MED_CELL)
print ""
if (nbTypesCell>0):
    print "      The Mesh has",nbTypesCell,"Type(s) of Cell"
    types = meshLocalCopy.getTypes(MED_CELL)
    for k in range(nbTypesCell):
        type = types[k]
        nbElemType = meshLocalCopy.getNumberOfElements(MED_CELL,type)
        print "     For the type:",type,"there is(are)",nbElemType,"elemnt(s)"
        connectivity = meshLocalCopy.getConnectivity(MED_FULL_INTERLACE,MED_NODAL,MED_CELL,type)
        nbNodesPerCell = type%100
        for j in range(nbElemType):
            print "       Element",(j+1)," ",connectivity[j*nbNodesPerCell:(j+1)*nbNodesPerCell]
            pass
        pass
    pass

##
## TEST METHODS ABOUT POLY ELEMENTS ##
##
nbTypesCellWithPoly = meshLocalCopy.getNumberOfTypesWithPoly(MED_CELL)
if (nbTypesCell == nbTypesCellWithPoly):
    print ""
    print "          No Poly Cells in the mesh"
    print ""
    pass
else:
    print ""
    print "          The Cell Nodal Connectivity of the Poly Cells:"
    print ""
    print "      The Mesh has",nbTypesCellWithPoly-nbTypesCell,"Type(s) of Poly Cell"
    types = meshLocalCopy.getTypesWithPoly(MED_CELL)
    for k in range(nbTypesCellWithPoly):
        type = types[k]
        if type == MED_POLYGON:
            nbElemType = meshLocalCopy.getNumberOfPolygons()
        elif type == MED_POLYHEDRA:
            nbElemType = meshLocalCopy.getNumberOfPolyhedron()
        else:
            continue
        print ""
        print "     For the type:",type,"there is(are)",nbElemType,"elemnt(s)"
        if type == MED_POLYGON:
            connectivity = meshLocalCopy.getPolygonsConnectivity(MED_NODAL,MED_CELL)
            index = meshLocalCopy.getPolygonsConnectivityIndex(MED_NODAL,MED_CELL)
            for j in range(nbElemType):
                print "       Polygon",(j+1)," ",connectivity[ index[j]-1 : index[j+1]-1 ]
                pass
            pass
        else:
            connectivity = meshLocalCopy.getPolyhedronConnectivity(MED_NODAL)
            fIndex = meshLocalCopy.getPolyhedronFacesIndex()
            index = meshLocalCopy.getPolyhedronIndex(MED_NODAL)
            for j in range(nbElemType):
                print     "       Polyhedra",(j+1)
                iF1, iF2 = index[ j ]-1, index[ j+1 ]-1
                for f in range( iF2 - iF1 ):
                    iN1, iN2 = fIndex[ iF1+f ]-1, fIndex[ iF1+f+1 ]-1
                    print "         Face",f+1," ",connectivity[ iN1 : iN2 ]
                    pass
                pass
            pass
        pass
    pass
pass

f_addLocal = FIELDDOUBLEClient(f_add)

f_addLocal.setName(f_addLocal.getName()+"add")

f_linLocal = FIELDDOUBLEClient(f_lin)

f_linLocal.setName(f_linLocal.getName()+"lin")

#Warning : OutputMedFiles are removed here after =================================
Outmed21File="OutCalculatorpointe21_V3.2.0b1.med"
os.system( 'rm -fr ' + Outmed21File )
Outmed22File="OutCalculatorpointe22_V3.2.0b1.med"
os.system( 'rm -fr ' + Outmed22File )

# writting the mesh and the fields
medFileVersion = getMedFileVersionForWriting()

if (medFileVersion == V22):
    setMedFileVersionForWriting(V21)

idMed = meshLocalCopy.addDriver(MED_DRIVER, Outmed21File, meshLocalCopy.getName(), MED_REMP)
meshLocalCopy.write(idMed)

idMed = f_addLocal.addDriver(MED_DRIVER, Outmed21File, f_addLocal.getName())
f_addLocal.write(idMed)

idMed = f_linLocal.addDriver(MED_DRIVER, Outmed21File, f_linLocal.getName())
f_linLocal.write(idMed)

medFileVersion = getMedFileVersionForWriting()

if (medFileVersion == V21):
    setMedFileVersionForWriting(V22)

idMed = meshLocalCopy.addDriver(MED_DRIVER, Outmed22File, meshLocalCopy.getName(), MED_REMP)
meshLocalCopy.write(idMed)

idMed = f_addLocal.addDriver(MED_DRIVER, Outmed22File, f_addLocal.getName())
f_addLocal.write(idMed)

idMed = f_linLocal.addDriver(MED_DRIVER, Outmed22File, f_linLocal.getName())
f_linLocal.write(idMed)

myStudy.GetObjectNames('/Med')
myStudy.GetObjectNames('/Med/MED_OBJECT_FROM_FILE_pointe.med')
myStudy.GetObjectNames('/Med/MEDMESH')
myStudy.GetObjectNames('/Med/MEDMESH/maa1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_2')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_3')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_NOEUD_1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_NOEUD_2')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_NOEUD_3')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_NOEUD_4')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe2')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe3')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe4')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe5')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/SupportOnAll_MED_MAILLE')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/SupportOnAll_MED_NOEUD')

myStudy.GetObjectNames('/Med/MEDFIELD')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldouble')
#myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldouble/(-1,-1)_ON_SupportOnAll_MED_MAILLE_OF_maa1')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodedouble')
#myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodedouble/(-1,-1)_ON_SupportOnAll_MED_NOEUD_OF_maa1')
#myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodedouble/1,-1)_ON_SupportOnAll_MED_NOEUD_OF_maa1')
#myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodedouble/(2,-1)_ON_SupportOnAll_MED_NOEUD_OF_maa1')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodeint')
#myStudy.GetObjectNames('/Med/MEDFIELD/fieldnodeint/(-1,-1)_ON_SupportOnAll_MED_NOEUD_OF_maa1')

#myStudyManager.Close(myStudy)
#myStudy.Close()

#
#
############   Output MED file with fields created by Caculator  #################
#                   via Client classes
#

myStudy = myStudyManager.NewStudy('medClient_withoutIHM_add_lin')
studynameId = myStudy._get_StudyId()
studyname = myStudy._get_Name()
print "We are working in the study ",studyname," with the ID ",studynameId

print "Reading the .med file ",Outmed21File," and pushing corba objects in the SALOME study"

medComp.readStructFileWithFieldType(Outmed21File,studyname)

Outf_add  = medComp.readFieldInFile(Outmed21File,studyname,'fieldcelldoubleadd',-1,-1)
Outf_lin  = medComp.readFieldInFile(Outmed21File,studyname,'fieldcelldoublelin',-1,-1)

myStudy.GetObjectNames('/Med')

myStudy.GetObjectNames('/Med/MED_OBJECT_FROM_FILE_OutCalculatorpointe21_V3.2.0b1.med')

myStudy.GetObjectNames('/Med/MEDMESH')
myStudy.GetObjectNames('/Med/MEDMESH/maa1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_2')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/FAMILLE_ELEMENT_3')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe1')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe2')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe3')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe4')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/groupe5')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/SupportOnAll_MED_MAILLE')
myStudy.GetObjectNames('/Med/MEDMESH/MEDSUPPORTS_OF_maa1/SupportOnAll_MED_NOEUD')

myStudy.GetObjectNames('/Med/MEDFIELD')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldoubleadd')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldoubleadd/(-1,-1)_ON_SupportOnAll_MED_MAILLE_OF_maa1')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldoublelin')
myStudy.GetObjectNames('/Med/MEDFIELD/fieldcelldoublelin/(-1,-1)_ON_SupportOnAll_MED_MAILLE_OF_maa1')

#myStudyManager.Save(myStudy,1)
#myStudy.DumpStudy("/tmp","medClient_withoutIHM_add_lin",1)

myStudyManager.SaveAs(studyname+'.hdf',myStudy,0)

print ""
print "END of the Pyhton script ..... Ctrl D to exit"
