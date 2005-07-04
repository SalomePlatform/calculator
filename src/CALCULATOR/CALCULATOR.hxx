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
