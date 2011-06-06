# Copyright (C) 2007-2011  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
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

#CALCULATOR_TEST_WITHOUTIHM.py
#
from omniORB import CORBA

import salome
import SALOME
import SALOME_MED
import SALOMEDS

import os
host = os.getenv( 'HOST' )
orb, lcc, naming_service, contmgr = salome.salome_kernel.salome_kernel_init()

################   GET A MED FIELD FROM FILE pointe.med   ###################
#
# This test program is based on the field named fieldcelldoublevector in 
# med file $MED_ROOT_DIR/share/salome/resources/med/pointe.med
filePath=os.environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/med/"
medFile=filePath+"pointe.med"
fieldname = "fieldcelldoublevector"

# Launch the Med Component and use it to load into memory the test field 
print "Launch the Med Component: "
med_comp = lcc.FindOrLoadComponent("FactoryServer", "MED")

# Get a Corba field proxy on the distant field (located in the med_comp server).
try:
    obj = naming_service.Resolve('myStudyManager')
    myStudyManager = obj._narrow(SALOMEDS.StudyManager)
    print "studyManager found"
    myStudy = myStudyManager.NewStudy('CALCULATOR_TEST_WITHOUTIHM')
    studynameId = myStudy._get_StudyId()
    studyname = myStudy._get_Name()
    print "We are working in the study ",studyname," with the ID ",studynameId
    print "Read field ",fieldname
    fieldcell  = med_comp.readFieldInFile(medFile,studyname,fieldname,-1,-1)
    fieldcelldouble = fieldcell._narrow(SALOME_MED.FIELDDOUBLE)
except SALOME.SALOME_Exception, ex:
    print ex.details
    print ex.details.type
    print ex.details.text
    print ex.details.sourceFile
    print ex.details.lineNumber
    raise

print "Description of Field : "
print fieldcelldouble
print fieldcelldouble.getName()
print fieldcelldouble.getDescription()
print fieldcelldouble.getNumberOfComponents()

#
#
##############  Load Calculator Component ###################
# Calculator Component must be in the Container of MED
#
print "Load Calculator Component "
# we need to import CALCULATOR_ORB to get a typed object (to perform narrowing)
import CALCULATOR_ORB
calculator = lcc.FindOrLoadComponent("FactoryServer", "CALCULATOR")

#
#
##############  Test Calculator Component ###################
#
#
print "Appel cloneField : fieldcelldoublevector -> f1,f2,f3,f4"
(f1,f2,f3,f4)=calculator.cloneField(fieldcelldouble)  # fieldcelldouble is consumed
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
from libMEDClient import *

gmeshDistant = f_add.getSupport().getMesh()
gmeshLocal = GMESHClient(gmeshDistant)

meshLocal = gmeshLocal.convertInMESH()

f_addLocal = FIELDDOUBLEClient(f_add)

f_addLocal.setName(f_addLocal.getName()+"add")

f_linLocal = FIELDDOUBLEClient(f_lin)

f_linLocal.setName(f_linLocal.getName()+"lin")

# med file with 2.1 format
# OutmedFile21="Calculatorpointe_V21.med"
# os.system( 'rm -fr ' + OutmedFile21 )

# medFileVersion = getMedFileVersionForWriting()
# if (medFileVersion == V22):
#     print "setMedFileVersionForWriting(V21)"
#     setMedFileVersionForWriting(V21)

# # writting the mesh
# print "meshLocal.write :"
# idMed = meshLocal.addDriver(MED_DRIVER, OutmedFile21, meshLocal.getName(), MED_REMP)
# meshLocal.write(idMed)

# # writting the 2 fields
# print "f_addLocal.write :"
# idMed = f_addLocal.addDriver(MED_DRIVER, OutmedFile21, f_addLocal.getName())
# f_addLocal.write(idMed)

# print "f_linLocal.write :"
# idMed = f_linLocal.addDriver(MED_DRIVER, OutmedFile21, f_linLocal.getName())
# f_linLocal.write(idMed)

# med file with 2.2 format
OutmedFile22="Calculatorpointe_V22.med"
os.system( 'rm -fr ' + OutmedFile22 )

# medFileVersion = getMedFileVersionForWriting()
# if (medFileVersion == V21):
#     print "setMedFileVersionForWriting(V22)"
#     setMedFileVersionForWriting(V22)

# writting the mesh
print "meshLocal.write :"
idMed = meshLocal.addDriver(MED_DRIVER, OutmedFile22, meshLocal.getName(), MED_REMP)
meshLocal.write(idMed)

# writting the 2 fields
print "f_addLocal.write :"
idMed = f_addLocal.addDriver(MED_DRIVER, OutmedFile22, f_addLocal.getName())
f_addLocal.write(idMed)

print "f_linLocal.write :"
idMed = f_linLocal.addDriver(MED_DRIVER, OutmedFile22, f_linLocal.getName())
f_linLocal.write(idMed)

print "End of Calculator Test!"
