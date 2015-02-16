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

#CALCULATOR_TEST_WITHOUTIHM.py
#
from omniORB import CORBA

import salome
import SALOME
import SALOME_MED
import SALOMEDS

from MEDCouplingCorba import *
from MEDCoupling import *
from MEDLoader import *

import os
host = os.getenv( 'HOST' )
orb, lcc, naming_service, contmgr = salome.salome_kernel.salome_kernel_init()

################   GET A MED FIELD FROM FILE pointe.med   ###################
#
# This test program is based on the field named fieldcelldoublevector in 
# med file $MED_ROOT_DIR/share/salome/resources/pointe.med
filePath=os.environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/med/"
medFile=filePath+"pointe.med"
fieldname = "fieldcelldoublevector"
meshname = "maa1"

# Launch the Med Component and use it to load into memory the test field 
print "Launch the Med Component: "
med_comp = lcc.FindOrLoadComponent("FactoryServer", "MED")

# Get a Corba field proxy on the distant field (located in the med_comp server).
try:
    #TODO
    #Manager = obj._narrow(SALOMEDS.StudyManager)
    #print "studyManager found"
    #myStudy = myStudyManager.NewStudy('CALCULATOR_TEST')
    #studynameId = myStudy._get_StudyId()
    #studyname = myStudy._get_Name()
    #print "We are working in the study ",studyname," with the ID ",studynameId
    print "Read field ",fieldname
    
    f = MEDLoader.ReadFieldCell(medFile,meshname,0,fieldname,-1,-1)
    fieldcelldouble=MEDCouplingFieldDoubleServant._this(f)
except SALOME.SALOME_Exception, ex:
    print ex.details
    print ex.details.type
    print ex.details.text
    print ex.details.sourceFile
    print ex.details.lineNumber
    raise

print "Description of Field : "
print f
print f.getName()
print f.getDescription()
print f.getNumberOfComponents()

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
f1.Register()
calculator.printField(f1)
print "Add fields f2+f3"
f_add=calculator.add(f2, f3)
f_add.Register()
calculator.printField( f_add ) # f_add is consumed

#
print "Apply linear function"
f_lin=calculator.applyLin(f4,2.0,1.0)
f_lin.Register()
calculator.printField( f_lin ) # f_lin is consumed
#
print "Appel Norme Max "
f_lin.Register()
norme=calculator.normMax(f_lin) # f_lin is consumed
print " -> norme = ",norme
#

print "End of Calculator Test!"
