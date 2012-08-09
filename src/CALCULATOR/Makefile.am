# Copyright (C) 2007-2012  CEA/DEN, EDF R&D, OPEN CASCADE
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

#  SuperVisionTest AddComponent : example of component that adds two numbers
#  File   : Makefile.in
#  Author : , CEA
#  Modified by : Alexander BORODIN (OCN) - autotools usage
#
include $(top_srcdir)/adm_local/unix/make_common_starter.am

# header files 
salomeinclude_HEADERS = CALCULATOR.hxx

# Libraries targets
lib_LTLIBRARIES = libCALCULATOREngine.la
dist_libCALCULATOREngine_la_SOURCES = \
	CALCULATOR.cxx

libCALCULATOREngine_la_CPPFLAGS = \
	$(CORBA_CXXFLAGS) \
	$(CORBA_INCLUDES) \
	$(MED_CXXFLAGS) \
	$(KERNEL_CXXFLAGS) \
	-I$(top_builddir)/idl

libCALCULATOREngine_la_LDFLAGS = \
	$(CORBA_LIBS) \
	$(HDF5_LIBS) \
	$(KERNEL_LDFLAGS) \
	-lSalomeContainer \
	-lOpUtil \
	-lSalomeIDLKernel \
	$(MED_LDFLAGS) \
	-lSalomeIDLMED \
	-lmedcouplingclient \
	-lmedcouplingcorba \
	$(top_builddir)/idl/libSalomeIDLCALCULATOR.la

# Scripts to be installed
dist_salomescript_DATA = \
	CALCULATOR_TEST.py \
	CALCULATOR_TEST_STUDY_WITHOUTIHM.py \
	CALCULATOR_TEST_WITHOUTIHM.py

dist_salomeres_DATA       = graphe1.xml 
dist_salomescript_SCRIPTS = graphe1.py
