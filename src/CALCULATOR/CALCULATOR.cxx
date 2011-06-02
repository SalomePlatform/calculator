// Copyright (C) 2007-2011  CEA/DEN, EDF R&D, OPEN CASCADE
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

#include "FIELDClient.hxx"
#include "MESHClient.hxx"

#include "MEDMEM_Mesh_i.hxx"
#include "MEDMEM_Support_i.hxx"
#include "MEDMEM_FieldTemplate_i.hxx"

#include <string>
#include <sstream>

#include <iomanip>
#include <cmath>
#include <float.h>

#include <memory>

using namespace std;
using namespace MEDMEM;

typedef FIELD<double,MEDMEM::FullInterlace> TFieldDouble;
typedef FIELDClient<double,MEDMEM::FullInterlace> TFieldDouble_c;
typedef FIELDTEMPLATE_I<double,MEDMEM::FullInterlace> TFieldDouble_i;

CALCULATOR::CALCULATOR (CORBA::ORB_ptr orb,
                        PortableServer::POA_ptr poa,
                        PortableServer::ObjectId * contId, 
                        const char *instanceName, 
                        const char *interfaceName)
  : Engines_Component_i(orb, poa, contId, instanceName, interfaceName, true),
    _errorCode(CALCULATOR_ORB::NO_ERROR)
{
  MESSAGE("activate object");
  _thisObj = this;
  _id = _poa->activate_object(_thisObj);
}

CALCULATOR::~CALCULATOR()
{
}

CORBA::Double CALCULATOR::norm2(SALOME_MED::FIELDDOUBLE_ptr field1)
{
    beginService( "CALCULATOR::norm2");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::Norm2(SALOME_MED::FIELDDOUBLE_ptr field1)";
  BEGIN_OF(LOC);
        
        if(CORBA::is_nil(field1)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return 0.0;
        }

        CORBA::Double norme = 0.0;
        // Create a local field from corba field, apply method normMax on it.
        // When exiting the function, f1 is deleted, and with it the remote corba field.
        TFieldDouble_c f1(field1);
        
        try {
                norme = f1.norm2();
        }
        catch(...) {
          _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
        }

  END_OF(LOC);
    endService( "CALCULATOR::norm2");
    return norme;
}

CORBA::Double CALCULATOR::normL2(SALOME_MED::FIELDDOUBLE_ptr field1)
{
    beginService( "CALCULATOR::normL2");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::NormL2(SALOME_MED::FIELDDOUBLE_ptr field1)";
  BEGIN_OF(LOC);

        if(CORBA::is_nil(field1)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return 0.0;
        }

    //Check that the Field is not on the Nodes (a limitation of normL2)
        SALOME_MED::SUPPORT_var aSupport = field1->getSupport();
        if(CORBA::is_nil(aSupport) || aSupport->getEntity() == SALOME_MED::MED_NODE) {
           _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
           return 0.0;
        }

    // Create a local field (on the stack) from corba field, apply method normMax on it.
    // When exiting the function, FIELDClient f1 is deleted, and with it the remote corba field.
    TFieldDouble_c  f1(field1);
        
    CORBA::Double norme = 0.0;
        try {
                norme = f1.normL2();
        }       
        catch(...) {
          _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
        }
    
        // Send a notification message to supervision
    ostringstream message("CALCULATOR::normL2 : ");
    message << norme;
    sendMessage("warning",message.str().c_str());
  END_OF(LOC);
    endService( "CALCULATOR::normL2");
    return norme;
}

CORBA::Double CALCULATOR::normMax(SALOME_MED::FIELDDOUBLE_ptr field1)
{
    beginService( "CALCULATOR::normMax");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::NormMax(SALOME_MED::FIELDDOUBLE_ptr field1)";
  BEGIN_OF(LOC);
        
        if(CORBA::is_nil(field1)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return 0.0;
        }

        CORBA::Double norme = 0.0;
        // An other way to do it : create an local field on the heap, inside an auto_ptr.
        // When exiting the function, auto_ptr is deleted, and with it the local field and 
        // the remote field if ownership was transferred.
        auto_ptr<TFieldDouble> f1 (new TFieldDouble_c(field1) );

        try {
                norme = f1->normMax();
        }
        catch(...) {
          _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
        }
    
  END_OF(LOC);
    endService( "CALCULATOR::normMax");
    return norme;
}

CORBA::Double CALCULATOR::normL1(SALOME_MED::FIELDDOUBLE_ptr field1)
{
    beginService( "CALCULATOR::normL1");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::NormL1(SALOME_MED::FIELDDOUBLE_ptr field1)";
  BEGIN_OF(LOC);

        if(CORBA::is_nil(field1)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return 0.0;
        }

        //Check that the Field is not on the Nodes (a limitation of normL1)
        SALOME_MED::SUPPORT_var aSupport = field1->getSupport();

        if(CORBA::is_nil(aSupport) || aSupport->getEntity() == SALOME_MED::MED_NODE) {
           _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
           return 0.0;
        }       
        
        CORBA::Double norme = 0.0;
        auto_ptr<TFieldDouble> f1 (new TFieldDouble_c(field1) );

        try {
                norme = f1->normL1();
        }
        catch(...) {
          _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
        }

  END_OF(LOC);
    endService( "CALCULATOR::normL1");
    return norme;
}


SALOME_MED::FIELDDOUBLE_ptr CALCULATOR::applyLin(SALOME_MED::FIELDDOUBLE_ptr field1,CORBA::Double a,CORBA::Double b)
{
    beginService( "CALCULATOR::applyLin");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "applyLin(SALOME_MED::FIELDDOUBLE_ptr field1,CORBA::Double a,CORBA::Double b)";
  BEGIN_OF(LOC);
    
        if(CORBA::is_nil(field1)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return NULL;
        }

        SALOME_MED::FIELDDOUBLE_ptr myFieldIOR = NULL;
        // create a local field on the heap, because it has to remain after exiting the function
        TFieldDouble * f1 = new TFieldDouble_c(field1);
        TFieldDouble_i * NewField = NULL;

        try {
                f1->applyLin(a,b);
                // create servant from f1, give it the property of c++ field (parameter true).
                // This imply that when the client will release it's field, it will delete NewField,
                // and f1.
                NewField = new TFieldDouble_i(f1,true) ;
                // activate object
                myFieldIOR = NewField->_this() ;
        }
        catch(...) {
          _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
        }

  END_OF(LOC);
    endService( "CALCULATOR::applyLin");
    return myFieldIOR;
}

SALOME_MED::FIELDDOUBLE_ptr CALCULATOR::add(SALOME_MED::FIELDDOUBLE_ptr field1, SALOME_MED::FIELDDOUBLE_ptr field2) 
{
    beginService( "CALCULATOR::add");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::add(SALOME_MED::FIELDDOUBLE_ptr field1, SALOME_MED::FIELDDOUBLE_ptr field2)";
  BEGIN_OF(LOC);

        if(CORBA::is_nil(field1) || CORBA::is_nil(field2)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return NULL;
        }

    // Create local fields from corba field
    TFieldDouble_c f1(field1);
    TFieldDouble_c f2(field2);

    // Create new c++ field on the heap by copying f1, add f2 to it.
    TFieldDouble* fres = new TFieldDouble(f1);
    
        // catch exception for non compatible fields
    try
    {
        *fres+=f2;
    }
    catch(MEDEXCEPTION)
    {
                 _errorCode = CALCULATOR_ORB::NOT_COMPATIBLE;
                 return NULL;
    }

    // create CORBA field from c++ toField. give property to servant (true)
    TFieldDouble_i * myFieldDoubleI = new TFieldDouble_i(fres,true);
    SALOME_MED::FIELDDOUBLE_ptr myFieldIOR = myFieldDoubleI->_this() ;

  END_OF(LOC);
    endService( "CALCULATOR::add");
    return myFieldIOR;
}

void CALCULATOR::cloneField(SALOME_MED::FIELDDOUBLE_ptr field,
                SALOME_MED::FIELDDOUBLE_out clone1, SALOME_MED::FIELDDOUBLE_out clone2,
                SALOME_MED::FIELDDOUBLE_out clone3, SALOME_MED::FIELDDOUBLE_out clone4)
{
    beginService( "CALCULATOR::cloneField");
        _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::cloneField";
  BEGIN_OF(LOC);

        if(CORBA::is_nil(field)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return;
        }

    // load local field, using MED ressource file pointe.med
    TFieldDouble_c f(field);

    // create three c++ field on the heap by copying myField_
    // All this fields share with f the same SUPPORT and MESH client.
    // Both SUPPORT and MESH client are connected to a reference count, and will 
    // be deleted after release of all the fields.
    TFieldDouble* fc1 = new TFieldDouble(f);
    TFieldDouble* fc2 = new TFieldDouble(f);
    TFieldDouble* fc3 = new TFieldDouble(f);
    TFieldDouble* fc4 = new TFieldDouble(f);
    
    // Initialize out references : 
    // Create three CORBA clones with cloned c++ fields - give property of c++ fields to servant (true)
    TFieldDouble_i * myClone1 = new TFieldDouble_i(fc1, true);
    TFieldDouble_i * myClone2 = new TFieldDouble_i(fc2, true);
    TFieldDouble_i * myClone3 = new TFieldDouble_i(fc3, true);
    TFieldDouble_i * myClone4 = new TFieldDouble_i(fc4, true);
    clone1 = myClone1->_this();
    clone2 = myClone2->_this();
    clone3 = myClone3->_this();
    clone4 = myClone4->_this();
  END_OF(LOC);
    endService( "CALCULATOR::cloneField");
    return;
}

void CALCULATOR::printField(SALOME_MED::FIELDDOUBLE_ptr field)
{
    beginService( "CALCULATOR::printField");
    _errorCode = CALCULATOR_ORB::NO_ERROR;

        if(CORBA::is_nil(field)) {
                _errorCode = CALCULATOR_ORB::INVALID_FIELD;
                return;
        }

    // Create a local field from corba field.
    // Use auto_ptr to perform automatic deletion after usage.
    // The deletion of the FIELDClient will delete the remote Corba object.
    auto_ptr<TFieldDouble> myField (new TFieldDouble_c(field) );

    const SUPPORT * mySupport = myField->getSupport();
    cout << "\n------------------ Field "<< myField->getName() << " : " <<myField->getDescription() << "------------------" <<  endl ;
    int NumberOfComponents = myField->getNumberOfComponents() ;
    cout << "- Type : " << mySupport->getEntity() << endl;
    cout << "- Nombre de composantes : "<< NumberOfComponents << endl ;
    cout << "- Nombre de valeurs     : "<< myField->getNumberOfValues() << endl ;
    for (int i=1; i<NumberOfComponents+1; i++) {
        cout << "  - composante "<<i<<" :"<<endl ;
        cout << "      - nom         : "<<myField->getComponentName(i)<< endl;
        cout << "      - description : "<<myField->getComponentDescription(i) << endl;
        cout << "      - units       : "<<myField->getMEDComponentUnit(i) << endl;
    }
    cout << "- iteration :" << endl ;
    cout << "    - numero : " << myField->getIterationNumber()<< endl  ;
    cout << "    - ordre  : " << myField->getOrderNumber()<< endl  ;
    cout << "    - temps  : " << myField->getTime()<< endl  ;
    cout << "- Type : " << myField->getValueType()<< endl;
    
    cout << "- Valeurs :"<<endl;
    int NumberOf = mySupport->getNumberOfElements(MED_ALL_ELEMENTS);

    bool displayNode = mySupport->isOnAllElements() && mySupport->getEntity()==MED_NODE;
    bool displayBary = mySupport->isOnAllElements() && mySupport->getEntity()==MED_CELL;
    int dim_space = mySupport->getMesh()->getSpaceDimension();
    const double * coord = mySupport->getMesh()->convertInMESH()->getCoordinates(MED_FULL_INTERLACE);

    auto_ptr<TFieldDouble> barycenter(0);
    if(displayBary)
        barycenter=auto_ptr<TFieldDouble>(mySupport->getMesh()->getBarycenter(mySupport)) ;

    const int width=10;
    for (int i=1; i<NumberOf+1; i++) {
        const double * value = myField->getRow(i) ;
        if(displayNode)
        {
            int N=(i-1)*dim_space;
            cout << setw(width) << i << setw(width) << coord[N] << " " << setw(width) << coord[N+1]<<  " " << setw(width) << coord[N+2] << "  : " ;
        }
        if(displayBary) {
          cout << setw(width) << i;
          for (int j=1; j<=dim_space; j++ ) 
            cout<< setw(width) << barycenter->getValueIJ(i,j) << " " ;
          cout<< "  : " ;
        }
        for (int j=0; j<NumberOfComponents; j++)
          cout << value[j]<< " ";
        cout<<endl;
    }
    cout << endl;
    cout << "Norme euclidienne : " << myField->norm2() << endl;
    cout << "Norme max         : " << myField->normMax() << endl;
    cout << "------------------------------------------------------------------------" << endl << endl;
    endService( "CALCULATOR::printField");
    return;

}

CORBA::Double CALCULATOR::convergenceCriteria(SALOME_MED::FIELDDOUBLE_ptr field)
{
  beginService( "CALCULATOR::convergenceCriteria");
  _errorCode = CALCULATOR_ORB::NO_ERROR;
  const char* LOC = "CALCULATOR::convergenceCriteria(SALOME_MED::FIELDDOUBLE_ptr field)";
  BEGIN_OF(LOC);

  if(CORBA::is_nil(field)) {
    _errorCode = CALCULATOR_ORB::INVALID_FIELD;
    return 0.0;
  }

  double criteria=1;
  static auto_ptr<TFieldDouble> fold(0);
  auto_ptr<TFieldDouble> fnew (new TFieldDouble_c(field) );

  try {
    if (fold.get() == NULL) // if old field is not set, set it and return 1
      fold=fnew;
    else
    {
      // if size of fields are not equal, return 1
      const int size=fold->getNumberOfValues()*fold->getNumberOfComponents();
      if ( size == fnew->getNumberOfValues()*fnew->getNumberOfComponents() )
      {
        //MED_EN::medModeSwitch mode=fold->getInterlacingType(); // storage mode
        const double* oldVal= fold->getValue(); // retrieve values
        const double* newVal= fnew->getValue();
        criteria=0.0;
        double ecart_rel=0.0;
        for (unsigned i=0; i!=size; ++i) // compute criteria
        {
          //if ( oldVal[i] != 0.0) // PAL14028
          if ( std::abs( oldVal[i] ) > DBL_MIN )
          {
            ecart_rel = std::abs( (oldVal[i]-newVal[i])/oldVal[i] );
            if ( ecart_rel>criteria )
              criteria=ecart_rel;
          }
        }
      }
    }
  }
  catch(...) {
    _errorCode = CALCULATOR_ORB::EXCEPTION_RAISED;
  }

  endService( "CALCULATOR::convergenceCriteria");
  END_OF(LOC);
  return criteria;
}

CORBA::Boolean CALCULATOR::isDone()
{
        return (_errorCode == CALCULATOR_ORB::NO_ERROR);                
}

CALCULATOR_ORB::ErrorCode CALCULATOR::getErrorCode()
{
        return _errorCode;
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
    MESSAGE("PortableServer::ObjectId * CALCULATOREngine_factory()");
    SCRUTE(interfaceName);
    CALCULATOR * myCALCULATOR =
      new CALCULATOR (orb, poa, contId, instanceName, interfaceName);
    return myCALCULATOR->getId();
  }
}
