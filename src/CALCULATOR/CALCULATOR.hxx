// Copyright (C) 2005  CEA/DEN, EDF R&D
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License.
//
// This library is distributed in the hope that it will be useful
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
//
// See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
//
#ifndef _CALCULATOR_HXX_
#define _CALCULATOR_HXX_

#include <SALOMEconfig.h>
#include CORBA_SERVER_HEADER(CALCULATOR_Gen)
#include CORBA_CLIENT_HEADER(MED)
#include "SALOME_Component_i.hxx"

class CALCULATOR:
  public POA_CALCULATOR_ORB::CALCULATOR_Gen,
  public Engines_Component_i 
{

public:
    CALCULATOR(CORBA::ORB_ptr orb,
	    PortableServer::POA_ptr poa,
	    PortableServer::ObjectId * contId, 
	    const char *instanceName, 
	    const char *interfaceName);
    virtual ~CALCULATOR();

    CORBA::Double convergenceCriteria(SALOME_MED::FIELDDOUBLE_ptr field);
    CORBA::Double normMax(SALOME_MED::FIELDDOUBLE_ptr field1);
    CORBA::Double normL2(SALOME_MED::FIELDDOUBLE_ptr field1);
    CORBA::Double norm2(SALOME_MED::FIELDDOUBLE_ptr field1);
    CORBA::Double normL1(SALOME_MED::FIELDDOUBLE_ptr field1);
    SALOME_MED::FIELDDOUBLE_ptr applyLin(SALOME_MED::FIELDDOUBLE_ptr field1,CORBA::Double a,CORBA::Double b);
    SALOME_MED::FIELDDOUBLE_ptr add(SALOME_MED::FIELDDOUBLE_ptr field1, SALOME_MED::FIELDDOUBLE_ptr field2)
	throw ( SALOME::SALOME_Exception );
    void printField(SALOME_MED::FIELDDOUBLE_ptr field);
    void cloneField(SALOME_MED::FIELDDOUBLE_ptr field, SALOME_MED::FIELDDOUBLE_out clone1, SALOME_MED::FIELDDOUBLE_out clone2,
	            SALOME_MED::FIELDDOUBLE_out clone3, SALOME_MED::FIELDDOUBLE_out clone4);
};


extern "C"
    PortableServer::ObjectId * CALCULATOREngine_factory(
	    CORBA::ORB_ptr orb,
	    PortableServer::POA_ptr poa,
	    PortableServer::ObjectId * contId,
	    const char *instanceName,
	    const char *interfaceName);


#endif
