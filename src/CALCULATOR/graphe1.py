#  Copyright (C) 2007-2011  CEA/DEN, EDF R&D, OPEN CASCADE
#
#  Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
#  CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
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
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

# Generated python file of Graph aNewDataFlow
#
from SuperV import *

# Graph creation of aNewDataFlow
def DefaNewDataFlow() :
    aNewDataFlow = Graph( 'aNewDataFlow' )
    aNewDataFlow.SetName( 'aNewDataFlow' )
    aNewDataFlow.SetAuthor( '' )
    aNewDataFlow.SetComment( '' )
    aNewDataFlow.Coords( 0 , 0 )
    
    # Creation of Factory Nodes
    
    normL2 = aNewDataFlow.FNode( 'CALCULATOR' , 'CALCULATOR_Gen' , 'normL2' )
    normL2.SetName( 'normL2' )
    normL2.SetAuthor( '' )
    normL2.SetContainer( 'localhost/FactoryServer' )
    normL2.SetComment( 'normL2 from CALCULATOR' )
    normL2.Coords( 496 , 144 )
    InormL2field = normL2.GetInPort( 'field' )
    InormL2Gate = normL2.GetInPort( 'Gate' )
    OnormL2return = normL2.GetOutPort( 'return' )
    OnormL2Gate = normL2.GetOutPort( 'Gate' )
    
    readFieldInFile = aNewDataFlow.FNode( 'MED' , 'MED' , 'readFieldInFile' )
    readFieldInFile.SetName( 'readFieldInFile' )
    readFieldInFile.SetAuthor( '' )
    readFieldInFile.SetContainer( 'localhost/FactoryServer' )
    readFieldInFile.SetComment( 'readFieldInFile from MED' )
    readFieldInFile.Coords( 271 , 144 )
    IreadFieldInFilefileName = readFieldInFile.GetInPort( 'fileName' )
    IreadFieldInFilestudyName = readFieldInFile.GetInPort( 'studyName' )
    IreadFieldInFilefieldName = readFieldInFile.GetInPort( 'fieldName' )
    IreadFieldInFileordre = readFieldInFile.GetInPort( 'ordre' )
    IreadFieldInFileiter = readFieldInFile.GetInPort( 'iter' )
    IreadFieldInFileGate = readFieldInFile.GetInPort( 'Gate' )
    OreadFieldInFilereturn = readFieldInFile.GetOutPort( 'return' )
    OreadFieldInFileGate = readFieldInFile.GetOutPort( 'Gate' )
    
    # Creation of InLine Nodes
    Pyinit_parameter = []
    Pyinit_parameter.append( '#                 ' )
    Pyinit_parameter.append( '# init_parameter()                 ' )
    Pyinit_parameter.append( '#                 ' )
    Pyinit_parameter.append( '#   this function initialize med files paths, field names                 ' )
    Pyinit_parameter.append( '#                 ' )
    Pyinit_parameter.append( '#   returned arguments :                 ' )
    Pyinit_parameter.append( '#                 ' )
    Pyinit_parameter.append( '#    - fromMedFile (string)   : path of file containing fromfieldname                 ' )
    Pyinit_parameter.append( '#    - fromfieldname (string) : name of field                 ' )
    Pyinit_parameter.append( '#    - myStudyId (string)     : name of study                 ' )
    Pyinit_parameter.append( '#                 ' )
    Pyinit_parameter.append( 'def init_parameter(): ' )
    Pyinit_parameter.append( '    import batchmode_salome                 ' )
    Pyinit_parameter.append( '    StudyName = batchmode_salome.myStudyName               ' )
    Pyinit_parameter.append( '    print "init_parameter : myStudyName = ", StudyName              ' )
    Pyinit_parameter.append( '    from os import environ                 ' )
    Pyinit_parameter.append( '    filePath=environ["MED_ROOT_DIR"]                 ' )
    Pyinit_parameter.append( '    filePath=filePath+"/share/salome/resources/med/"                 ' )
    Pyinit_parameter.append( '    fromMedFile=filePath+"pointe.med"                            ' )
    Pyinit_parameter.append( '    print "init_parameter : fromMedFile = ", fromMedFile                             ' )
    Pyinit_parameter.append( '    fromfieldname="fieldcelldouble"                     ' )
    Pyinit_parameter.append( '    return fromMedFile,fromfieldname,StudyName             ' )
    init_parameter = aNewDataFlow.INode( 'init_parameter' , Pyinit_parameter )
    init_parameter.SetName( 'init_parameter' )
    init_parameter.SetAuthor( '' )
    init_parameter.SetComment( 'Compute Node' )
    init_parameter.Coords( 6 , 147 )
    Iinit_parameterGate = init_parameter.GetInPort( 'Gate' )
    Oinit_parameterfromMedFile = init_parameter.OutPort( 'fromMedFile' , 'string' )
    Oinit_parameterfromfieldname = init_parameter.OutPort( 'fromfieldname' , 'string' )
    Oinit_parameterstudyId = init_parameter.OutPort( 'studyId' , 'string' )
    Oinit_parameterGate = init_parameter.GetOutPort( 'Gate' )
    
    # Creation of Links
    Linit_parameterfromMedFilereadFieldInFilefileName = aNewDataFlow.Link( Oinit_parameterfromMedFile , IreadFieldInFilefileName )
    
    Linit_parameterfromfieldnamereadFieldInFilefieldName = aNewDataFlow.Link( Oinit_parameterfromfieldname , IreadFieldInFilefieldName )
    
    Linit_parameterstudyIdreadFieldInFilestudyName = aNewDataFlow.Link( Oinit_parameterstudyId , IreadFieldInFilestudyName )
    
    LreadFieldInFilereturnnormL2field = aNewDataFlow.Link( OreadFieldInFilereturn , InormL2field )
    
    # Input datas
    IreadFieldInFileordre.Input( -1 )
    IreadFieldInFileiter.Input( -1 )
    
    # Output Ports of the graph
    #OnormL2return = normL2.GetOutPort( 'return' )
    return aNewDataFlow


aNewDataFlow = DefaNewDataFlow()
