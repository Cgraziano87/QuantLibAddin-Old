/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006, 2007, 2015 Ferdinando Ametrano
 Copyright (C) 2007 Chiara Fornarola
 Copyright (C) 2006, 2007 Marco Bianchetti
 Copyright (C) 2006, 2007 Cristina Duminuco
 Copyright (C) 2006, 2007 Giorgio Facchinetti
 Copyright (C) 2015 Paolo Mazzocchi

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
*/

#ifndef qla_abcd_hpp
#define qla_abcd_hpp

#include <oh/libraryobject.hpp>
#include <ql/types.hpp>

namespace QuantLib {
    class AbcdFunction;
    class AbcdCalibration;
    class AbcdCalibration2;
    class EndCriteria;
    class OptimizationMethod;
    class PolynomialCalibration;

    template <class T>
    class Handle;
}

namespace QuantLibAddin {

    class AbcdFunction :
            public ObjectHandler::LibraryObject<QuantLib::AbcdFunction> {
      public:
        AbcdFunction(
            const boost::shared_ptr<ObjectHandler::ValueObject>& properties,
            QuantLib::Real a,
            QuantLib::Real b,
            QuantLib::Real c,
            QuantLib::Real d,
            bool permanent);
    };

    class AbcdCalibration :
            public ObjectHandler::LibraryObject<QuantLib::AbcdCalibration> {
      public:
        AbcdCalibration(
             const boost::shared_ptr<ObjectHandler::ValueObject>& properties,
             const std::vector<QuantLib::Time>& times,
             const std::vector<QuantLib::Volatility>& blackVols,
             QuantLib::Real a,
             QuantLib::Real b,
             QuantLib::Real c,
             QuantLib::Real d,
             bool aIsFixed,
             bool bIsFixed,
             bool cIsFixed,
             bool dIsFixed,
             bool vegaWeighted = false,
             const boost::shared_ptr<QuantLib::EndCriteria> endCriteria
                 = boost::shared_ptr<QuantLib::EndCriteria>(),
             const boost::shared_ptr<QuantLib::OptimizationMethod> method
                 = boost::shared_ptr<QuantLib::OptimizationMethod>(),
             bool permanent = false);
    };

    class AbcdCalibration2 :
        public ObjectHandler::LibraryObject<QuantLib::AbcdCalibration2> {
    public:
        AbcdCalibration2(
            const boost::shared_ptr<ObjectHandler::ValueObject>& properties,
            const std::vector<QuantLib::Time>& t,
            const std::vector<QuantLib::Rate>& r,
            const std::vector<QuantLib::Real>& w,
            std::vector<QuantLib::Real> coeff,
            const std::vector<bool>& fixedCoeff,
            const boost::shared_ptr<QuantLib::EndCriteria> endCriteria,
            const boost::shared_ptr<QuantLib::OptimizationMethod> method,
            bool permanent);
    };

    class PolynomialCalibration :
        public ObjectHandler::LibraryObject<QuantLib::PolynomialCalibration> {
    public:
        PolynomialCalibration(
               const boost::shared_ptr<ObjectHandler::ValueObject>& properties,
               const std::vector<QuantLib::Time>& t,
               const std::vector<QuantLib::Rate>& rates,
               const std::vector<QuantLib::Real>& weights,
               std::vector<QuantLib::Real> coeff,
               const std::vector<bool>& fixedCoeff,
               const boost::shared_ptr<QuantLib::EndCriteria> endCriteria,
               const boost::shared_ptr<QuantLib::OptimizationMethod> method,
               bool permanent);
    };

}

#endif
