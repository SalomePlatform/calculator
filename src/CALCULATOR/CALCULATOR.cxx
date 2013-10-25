// Copyright (C) 2007-2013  CEA/DEN, EDF R&D, OPEN CASCADE
//
// Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
// CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License.
//
// This library is distributed in the hope that it will be useful,
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

#include "CALCULATOR.hxx"
#include "CALCULATOR_version.h"

#include "MEDCouplingFieldDoubleClient.hxx"
#include "MEDCouplingMeshClient.hxx"

#include "MEDCouplingMeshServant.hxx"
#include "MEDCouplingFieldDoubleServant.hxx"

#include "MEDCouplingAutoRefCountObjectPtr.hxx"
#include "MEDCouplingMemArray.hxx"

#include <string>
#include <sstream>

#include <iomanip>
#include <cmath>
#include <float.h>

#include <memory>

using namespace std;

CALCULATOR::CALCULATOR (CORBA::ORB_ptr orb,
                        PortableServer::POA_ptr poa,
                        PortableServer::ObjectId * contId, 
                        const char *instanceName, 
                        const char *interfaceName)
  : Engines_Component_i(orb, poa, contId, instanceName, interfaceName, true),
    _errorCode(CALCULATOR_ORB::RES_OK)
{
  _thisObj = this;
  _id = _poa->activate_object(_thisObj);
}

CALCULATOR::~CALCULATOR()
{
}

CORBA::Double CALCULATOR::norm2(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)
{
  beginService( "CALCULATOR::norm2");
  _errorCode = CALCULATOR_ORB::RES_OK;
  //const char* LOC = "CALCULATOR::Norm2(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)";
        
  if(CORBA::is_nil(field1))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return 0.0;
    }

  CORBA::Double norme = 0.0;
  // Create a local field from corba field, apply method normMax on it.
  // When exiting the function, f1 is deleted, and with it the remote corba field.
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  /*ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::DataArrayDouble> d=ParaMEDMEM::DataArrayDouble::Multiply(f1->getArray(),f1->getArray());
  d->rearrange(1);
  try {
    norme = d->accumulate(0);
  }
  catch(...) {
    _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
  }*/
  try
    {
      norme = f1->norm2();
    }    
  catch(...)
    {
      _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
    }

  endService( "CALCULATOR::norm2");
  return norme;
}

CORBA::Double CALCULATOR::normL2(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)
{
  beginService( "CALCULATOR::normL2");
  _errorCode = CALCULATOR_ORB::RES_OK;
  //const char* LOC = "CALCULATOR::NormL2(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)";
  //BEGIN_OF(LOC);

  if(CORBA::is_nil(field1))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return 0.0;
    }

  //Check that the Field is not on the Nodes (a limitation of normL2)
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  
  if(f1->getTypeOfField()==ParaMEDMEM::ON_NODES)
    {
      _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
      return 0.0;
    }
        
  CORBA::Double norme = 0.0;
  try
    {
      norme = f1->normL2(0);
    }    
  catch(...)
    {
      _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
    }
    
  // Send a notification message to supervision
  ostringstream message("CALCULATOR::normL2 : ");
  message << norme;
  sendMessage("warning",message.str().c_str());
  //END_OF(LOC);
  endService( "CALCULATOR::normL2");
  return norme;
}

CORBA::Double CALCULATOR::normMax(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)
{
  beginService( "CALCULATOR::normMax");
  _errorCode = CALCULATOR_ORB::RES_OK;
         
  if(CORBA::is_nil(field1))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return 0.0;
    }

  CORBA::Double norme = 0.0;
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  try
    {
      norme = f1->normMax();
    }
  catch(...)
    {
      _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
    }
    
 
  endService( "CALCULATOR::normMax");
  return norme;
}

CORBA::Double CALCULATOR::normL1(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1)
{
  beginService( "CALCULATOR::normL1");
  _errorCode = CALCULATOR_ORB::RES_OK;

  if(CORBA::is_nil(field1)) {
    _errorCode = CALCULATOR_ORB::INVALID_FIELD;
    return 0.0;
  }

  //Check that the Field is not on the Nodes (a limitation of normL1)
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  if (f1->getTypeOfField()==ParaMEDMEM::ON_NODES) {
    _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
    return 0.0;
  }       
        
  CORBA::Double norme = 0.0;
  try {
    norme = f1->normL1(0);
  }
  catch(...) {
    _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
  }

  endService( "CALCULATOR::normL1");
  return norme;
}

SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr CALCULATOR::applyLin(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1,CORBA::Double a,CORBA::Double b)
{
  beginService( "CALCULATOR::applyLin");
  _errorCode = CALCULATOR_ORB::RES_OK;
    
  if(CORBA::is_nil(field1))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return NULL;
    }

  // create a local field on the heap, because it has to remain after exiting the function
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  int nbOfCompo=f1->getArray()->getNumberOfComponents();
  f1->getArray()->rearrange(1);
  ParaMEDMEM::MEDCouplingFieldDoubleServant *NewField=NULL;
  SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr myFieldIOR = NULL;

  try
    {
      f1->applyLin(a,b,0);
      f1->getArray()->rearrange(nbOfCompo);
      // create servant from f1, give it the property of c++ field (parameter true).
      // This imply that when the client will release it's field, it will delete NewField,
      // and f1.
      NewField = new ParaMEDMEM::MEDCouplingFieldDoubleServant(f1);
      // activate object
      myFieldIOR = NewField->_this() ;
    }
  catch(...)
    {
      _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
    }
  
  endService( "CALCULATOR::applyLin");
  return myFieldIOR;
}

SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr CALCULATOR::add(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1, SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field2) 
{
  beginService( "CALCULATOR::add");
  _errorCode = CALCULATOR_ORB::RES_OK;
  //const char* LOC = "CALCULATOR::add(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field1, SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field2)";

  if(CORBA::is_nil(field1) || CORBA::is_nil(field2))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return NULL;
    }

  // Create local fields from corba field
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field1);
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f2=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field2);
    
  // catch exception for non compatible fields
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble>  fres;
  try
    {
      f2->changeUnderlyingMesh(f1->getMesh(),0,1e-12);
      fres = (*f1)+(*f2);
    }
  catch(INTERP_KERNEL::Exception)
    {
      _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
      return NULL;
    }

  // create CORBA field from c++ toField. give property to servant (true)
  ParaMEDMEM::MEDCouplingFieldDoubleServant *myFieldDoubleI=new ParaMEDMEM::MEDCouplingFieldDoubleServant(fres);
  SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr myFieldIOR = myFieldDoubleI->_this();
  endService( "CALCULATOR::add");
  return myFieldIOR;
}

void CALCULATOR::cloneField(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field,
			    SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_out clone1, SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_out clone2,
			    SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_out clone3, SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_out clone4)
{
  beginService( "CALCULATOR::cloneField");
  _errorCode = CALCULATOR_ORB::RES_OK;

  if(CORBA::is_nil(field))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return;
    }
  
  // load local field, using MED ressource file pointe.med
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> f=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);

  // create three c++ field on the heap by copying myField_
  // All this fields share with f the same SUPPORT and MESH client.
  // Both SUPPORT and MESH client are connected to a reference count, and will 
  // be deleted after release of all the fields.
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fc1=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fc2=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fc3=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fc4=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);
    
  // Initialize out references : 
  // Create three CORBA clones with cloned c++ fields - give property of c++ fields to servant (true)
  ParaMEDMEM::MEDCouplingFieldDoubleServant * myClone1 = new ParaMEDMEM::MEDCouplingFieldDoubleServant(fc1);
  ParaMEDMEM::MEDCouplingFieldDoubleServant * myClone2 = new ParaMEDMEM::MEDCouplingFieldDoubleServant(fc2);
  ParaMEDMEM::MEDCouplingFieldDoubleServant * myClone3 = new ParaMEDMEM::MEDCouplingFieldDoubleServant(fc3);
  ParaMEDMEM::MEDCouplingFieldDoubleServant * myClone4 = new ParaMEDMEM::MEDCouplingFieldDoubleServant(fc4);
  clone1 = myClone1->_this();
  clone2 = myClone2->_this();
  clone3 = myClone3->_this();
  clone4 = myClone4->_this();
  endService( "CALCULATOR::cloneField");
  return;
}

void CALCULATOR::printField(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field)
{
  beginService( "CALCULATOR::printField");
  _errorCode = CALCULATOR_ORB::RES_OK;

  if(CORBA::is_nil(field))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return;
    }

  // Create a local field from corba field.
  // Use auto_ptr to perform automatic deletion after usage.
  // The deletion of the FIELDClient will delete the remote Corba object.
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> myField=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);
  cout << myField->advancedRepr() ; 

  cout << endl;
  cout << "Norme euclidienne : " << myField->norm2() << endl;
  cout << "Norme max         : " << myField->normMax() << endl;
  cout << "------------------------------------------------------------------------" << endl << endl;
  endService( "CALCULATOR::printField");
  return;

}

CORBA::Double CALCULATOR::convergenceCriteria(SALOME_MED::MEDCouplingFieldDoubleCorbaInterface_ptr field)
{
  beginService( "CALCULATOR::convergenceCriteria");
  _errorCode = CALCULATOR_ORB::RES_OK;

  if(CORBA::is_nil(field))
    {
      _errorCode = CALCULATOR_ORB::INVALID_FIELD;
      return 0.0;
    }

  double criteria=1;
  static ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fold(0);
  ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble> fnew=ParaMEDMEM::MEDCouplingFieldDoubleClient::New(field);

  try
    {
      if ((ParaMEDMEM::MEDCouplingFieldDouble*)fold == NULL) // if old field is not set, set it and return 1
          fold=fnew;
      else
	   {
    	  // if size of fields are not equal, return 1
	      // catch exception for non compatible fields
	      ParaMEDMEM::MEDCouplingAutoRefCountObjectPtr<ParaMEDMEM::MEDCouplingFieldDouble>  fres;
	      try
	        {
	           fnew->changeUnderlyingMesh(fold->getMesh(),0,1e-12);
	           fres = (*fnew)-(*fold);
	           criteria = fres->normMax();
	        }
	      catch(INTERP_KERNEL::Exception)
	        {
	           _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
	        }
	   }
    }
  catch(...)
    {
      _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
    }
  
  endService( "CALCULATOR::convergenceCriteria");
  return criteria;
}

CORBA::Boolean CALCULATOR::isDone()
{
  return (_errorCode == CALCULATOR_ORB::RES_OK);                
}

CALCULATOR_ORB::ErrorCode CALCULATOR::getErrorCode()
{
  return _errorCode;
}

// Version information
char* CALCULATOR::getVersion()
{
#if defined(CALCULATOR_DEVELOPMENT)
  return CORBA::string_dup(CALCULATOR_VERSION_STR"dev");
#else
  return CORBA::string_dup(CALCULATOR_VERSION_STR);
#endif
}

//=============================================================================
/*!
 *  CALCULATOREngine_factory
 *
 *  C factory, accessible with dlsym, after dlopen
 */
//=============================================================================

extern "C"
{
  PortableServer::ObjectId * CALCULATOREngine_factory (CORBA::ORB_ptr orb,
                                                       PortableServer::POA_ptr poa,
                                                       PortableServer::ObjectId * contId,
                                                       const char *instanceName,
                                                       const char *interfaceName)
  {
    CALCULATOR * myCALCULATOR = new CALCULATOR (orb, poa, contId, instanceName, interfaceName);
    return myCALCULATOR->getId();
  }
}

