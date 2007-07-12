
"""
 Copyright (C) 2007 Eric Ehlers

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <http://quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

"""Generate source code for C++ addin."""

from gensrc.Addins import addin
from gensrc.Addins import cppexceptions
from gensrc.Addins import serialization
from gensrc.Configuration import environment
from gensrc.Categories import category
from gensrc.Utilities import outputfile
from gensrc.Utilities import log

class CppAddin(addin.Addin):
    """Generate source code for C++ addin."""

    #############################################
    # class variables
    #############################################

    voSupported_ = True
    #convertPermanentFlag_ = '''
    #    bool permanentCpp =
    #        ObjectHandler::callOperToScalar<bool>(*permanent, "permanent", false);
    #    if (permanentCpp)
    #        objectPointer->setPermanent();'''
    convertPermanentFlag_ = ''
    BUFFER_ALL = '''\
#include <Addins/C++/addincppdefines.hpp>
#include <Addins/C++/init.hpp>\n'''

    #############################################
    # public interface
    #############################################

    def generate(self, categoryList, enumerationList):
        """Generate source code for C++ addin."""

        self.categoryList_ = categoryList
        self.enumerationList_ = enumerationList

        log.Log.instance().logMessage(' begin generating %s...' % self.name_)
        self.generateFunctions()
        if environment.config().usingSerialization():
            serialization.generateSerialization(self, self.relativePath_)
        log.Log.instance().logMessage(' done generating %s.' % self.name_)

    def generateFunctions(self):
        """Generate source code for all functions in all categories."""
        bufferAll = CppAddin.BUFFER_ALL
        for cat in self.categoryList_.categories(self.name_):
            categoryIncludes = cat.includeList()
            #categoryIncludes = cat.includeList(LOOP_INCLUDES)
            bufferAll += "#include <Addins/C++/%s.hpp>\n" % cat.name()
            bufferCpp = ''
            bufferHpp = ''
            for func in cat.functions(self.name_): 
                bufferCpp += self.generateFunction(func)
                bufferHpp += self.generateDeclaration(func)
            bufferBody = self.bufferBody_.text() % { 
                'bufferCpp' : bufferCpp,
                'categoryIncludes' : categoryIncludes }
            bufferHeader = self.bufferHeader_.text() % { 
                'categoryName' : cat.name(),
                'bufferHpp' : bufferHpp }
            fileNameCpp = '%s%s.cpp' % ( self.rootPath_, cat.name())
            outputfile.OutputFile(self, fileNameCpp, cat.copyright(), bufferBody)
            fileNameHpp = '%s%s.hpp' % ( self.rootPath_, cat.name())
            outputfile.OutputFile(self, fileNameHpp, cat.copyright(), bufferHeader)
        bufferAll += "\n"
        fileNameAll = '%saddincpp.hpp' % self.rootPath_
        outputfile.OutputFile(self, fileNameAll, self.copyright_, bufferAll)

    def generateFunction(self, func):
        """Generate source code for a given function."""
        return self.bufferFunction_.text() % {
            'cppConversions' : func.parameterList().generate(self.cppConversions_),
            'enumConversions' : func.parameterList().generate(self.enumConversions_),
            'functionBody' : func.generateBody(self),
            'functionDeclaration' : func.parameterList().generate(self.functionDeclaration_),
            'functionName' : func.name(),
            'functionReturnType' : self.functionReturnType_.apply(func.returnValue()),
            'libConversions' : func.parameterList().generate(self.libraryConversions_),
            'objectConversions' : func.parameterList().generate(self.objectConversions_),
            'refConversions' : func.parameterList().generate(self.referenceConversions_),
            'returnConversion' : self.returnConversion_.apply(func.returnValue()) }

    def generateDeclaration(self, func):
        """Generate source code for a given function."""
        return self.bufferDeclaration_.text() % {
            'functionReturnType' : self.functionReturnType_.apply(func.returnValue()),
            'functionDeclaration' : func.parameterList().generate(self.functionDeclaration_),
            'functionName' : func.name() }

    #############################################
    # serializer interface
    #############################################

    def serialize(self, serializer):
        """load/unload class state to/from serializer object."""
        super(CppAddin, self).serialize(serializer)
        serializer.serializeProperty(self, 'serializationBase')

