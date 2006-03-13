#  Check availability of CALCULATOR binary distribution
#
#  Author : Marc Tajchman (CEA, 2002)
#------------------------------------------------------------

AC_DEFUN([CHECK_CALCULATOR],[

AC_CHECKING(for Calculator)

Calculator_ok=no

AC_ARG_WITH(calc,
	    --with-calculator=DIR  root directory path of CALCULATOR build or installation,
	    CALCULATOR_DIR="$withval",CALCULATOR_DIR="")

if test "x$CALCULATOR_DIR" = "x" ; then

# no --with-gui-dir option used

  if test "x$CALCULATOR_ROOT_DIR" != "x" ; then

    # SALOME_ROOT_DIR environment variable defined
    CALCULATOR_DIR=$CALCULATOR_ROOT_DIR

  else

    # search Salome binaries in PATH variable
    AC_PATH_PROG(TEMP, libCALCULATOREngine.so)
    if test "x$TEMP" != "x" ; then
      CALCULATOR_DIR=`dirname $TEMP`
    fi

  fi

fi

if test -f ${CALCULATOR_DIR}/lib/salome/libCALCULATOREngine.so  ; then
  Calculator_ok=yes
  AC_MSG_RESULT(Using CALCULATOR module distribution in ${CALCULATOR_DIR})

  if test "x$CALCULATOR_ROOT_DIR" == "x" ; then
    CALCULATOR_ROOT_DIR=${CALCULATOR_DIR}
  fi
  AC_SUBST(CALCULATOR_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled CALCULATOR module distribution")
fi
  
AC_MSG_RESULT(for CALCULATOR: $Calculator_ok)
 
])dnl
 
