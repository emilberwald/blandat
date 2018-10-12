! Copyright (C) 2017 Your name.
! See http://factorcode.org/license.txt for BSD license.
USING: tools.test derivatives ;
QUALIFIED: math
QUALIFIED: math.order
QUALIFIED: syntax
IN: derivatives.tests
{ syntax:t } [ 3 0.001 1 [ math:* ] [ math:+ ] [ math:sq ] [ math:- ] [ math:/ ] FiniteDifferenceUsingDirection 6 6.001 math.order:between? ] unit-test

