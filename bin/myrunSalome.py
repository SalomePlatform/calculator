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
#  See http://www.salome-platform.org/
#
#!/usr/bin/env python

def test(clt):
   """
        Test function that creates an instance of CALCULATOR component
        usage : hello=test(clt)
   """
   # create an LifeCycleCORBA instance
   import LifeCycleCORBA
   lcc = LifeCycleCORBA.LifeCycleCORBA(clt.orb)
   import CALCULATOR_ORB
   hello = lcc.FindOrLoadComponent("FactoryServer", "CALCULATOR")
   return hello

#

if __name__ == "__main__":
   import user
   from runSalome import *
   clt,args = main()
   
   #
   #  Impression arborescence Naming Service
   #
   
   if clt != None:
     print
     print " --- registered objects tree in Naming Service ---"
     clt.showNS()
     session=clt.waitNS("/Kernel/Session")
     catalog=clt.waitNS("/Kernel/ModulCatalog")
     import socket
     container =  clt.waitNS("/Containers/" + socket.gethostname().split('.')[0] + "/FactoryServer")
