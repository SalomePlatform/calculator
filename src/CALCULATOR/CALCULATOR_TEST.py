#  Copyright (C) 2005  CEA/DEN, EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
from omniORB import CORBA

import salome
import SALOME
import SALOME_MED

#CCRT :
import os
import Engines
import LifeCycleCORBA

host = os.getenv( 'HOST' )

orb = CORBA.ORB_init([''], CORBA.ORB_ID)

lcc = LifeCycleCORBA.LifeCycleCORBA(orb)
#endCCRT

################   GET A MED FIELD FROM FILE pointe.med   ###################
#
# This test program is based on the field named fieldcelldoublevector in 
# med file $MED_ROOT_DIR/share/salome/resources/pointe.med
from os import environ
filePath=environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/"
medFile=filePath+"pointe.med"
fieldname = "fieldcelldoublescalar"

# Launch the Med Component and use it to load into memory the test field 
print "Launch the Med Component: "
#CCRTmed_comp = salome.lcc.FindOrLoadComponent("FactoryServer", "MED")
med_comp = lcc.FindOrLoadComponent("FactoryServer", "MED")

# Get a Corba field proxy on the distant field (located in the med_comp server).
try:
    studyname = salome.myStudyName
    studynameId = salome.myStudyId
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
##############  Load Calculator Component and test it   ###################
#
#
print "Load Calculator Component "
# we need to import CALCULATOR_ORB to get a typed object (to perform narrowing)
import CALCULATOR_ORB
calculator = salome.lcc.FindOrLoadComponent("FactoryServer", "CALCULATOR")
#
print "Appel cloneField : fieldcelldouble -> f1,f2,f3,f4"
(f1,f2,f3,f4)=calculator.cloneField(fieldcelldouble)  # fieldcelldouble is consumed
#
calculator.printField(f1)
print "Add fields f2+f3"
f_add=calculator.add(f2, f3)
calculator.printField(f_add)

#
print "Apply linear function"
f_lin=calculator.applyLin(f4,2.0,1.0)
#
print "Appel Norme Max "
norme=calculator.normMax(f_lin)
print " -> norme = ",norme
#
print "End of Calculator Test!"
