# Copyright (C) 2012-2013  CEA/DEN, EDF R&D, OPEN CASCADE
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

# --- options ---
# additional include directories
INCLUDE_DIRECTORIES(
  ${OMNIORB_INCLUDE_DIR}
  ${KERNEL_INCLUDE_DIRS}
  ${MED_INCLUDE_DIRS}
  ${PROJECT_BINARY_DIR}
  ${PROJECT_BINARY_DIR}/idl
)

# additional preprocessor / compiler flags
ADD_DEFINITIONS(
  ${QT_DEFINITIONS}
  ${OMNIORB_DEFINITIONS}
)

IF(WIN32)
 ADD_DEFINITIONS(-DNOMINMAX)
ENDIF(WIN32)

# libraries to link to
SET(_link_LIBRARIES
  ${KERNEL_SalomeContainer}
  ${KERNEL_OpUtil}
  ${KERNEL_SalomeIDLKERNEL}
  ${MED_medcouplingclient}
  ${MED_medcouplingcorba}
  ${MED_SalomeIDLMED}
  SalomeIDLCALCULATOR
)
# --- headers ---

# header files / no moc processing
SET(CALCULATOR_HEADERS
  CALCULATOR.hxx
)

# --- sources ---

# sources / static
SET(CALCULATOR_SOURCES
  CALCULATOR.cxx
)

# --- scripts ---

# scripts / static
SET(_bin_SCRIPTS
  CALCULATOR_TEST.py
  CALCULATOR_TEST_WITHOUTIHM.py
  CALCULATOR_TEST_STUDY_WITHOUTIHM.py
  graphe1.py
)

# resource files / static
SET(CALCULATOR_RESOURCES
  graphe1.xml
)


# --- rules ---

ADD_LIBRARY(CALCULATOREngine ${CALCULATOR_SOURCES})
TARGET_LINK_LIBRARIES(CALCULATOREngine ${_link_LIBRARIES})
INSTALL(TARGETS CALCULATOREngine EXPORT ${PROJECT_NAME}TargetGroup DESTINATION ${SALOME_INSTALL_LIBS})

INSTALL(FILES ${CALCULATOR_HEADERS} DESTINATION ${SALOME_INSTALL_HEADERS})

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_SCRIPT_PYTHON})

INSTALL(FILES ${CALCULATOR_RESOURCES} DESTINATION ${SALOME_CALCULATOR_INSTALL_RES_DATA})