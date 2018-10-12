! Copyright (C) 2017 Your name.
! See http://factorcode.org/license.txt for BSD license.
USING: locals kernel help.syntax help.markup sequences fry ;
IN: derivatives
QUALIFIED: math
CONSTANT: ℝ0 0
ALIAS: ℝ+ math:+
ALIAS: ℝ- math:-
ALIAS: ℝ* math:*
ALIAS: ℝ/ math:/

: $explanation ( element -- ) "Explanation" $heading [ values-row ] map $table ;

! Press Ctrl+w to step in the code

DEFER: p
DEFER: t
DEFER: X
DEFER: *
DEFER: +
DEFER: F
DEFER: - 
DEFER: /
:: FiniteDifferenceUsingDirection ( p t X * + F - / -- N )
 p t X * call + call F call
 p F call
 - call t / call ; inline
 HELP: FiniteDifferenceUsingDirection
 { $explanation 
    { p ( -- M ) } 
    { t ( -- K ) } 
    { X ( -- M ) } 
    { * ( K M -- M ) } 
    { + ( M M -- M ) } 
    { F ( M -- N ) } 
    { p ( -- M ) } 
    { F ( M -- N ) } 
    { - ( N N -- N ) } 
    { t ( -- K ) } 
    { / ( N K -- N ) } 
 } 
 { $warning "M and N must be topological vector spaces over the same field of scalars K" }
 { $example "USING: derivatives ;" "QUALIFIED: math " " 3 0.001 1 [ math:* ] [ math:+ ] [ math:sq ] [ math:- ] [ math:/ ] FiniteDifferenceUsingDirection" "6.000999999999479" }
 { $url "https://en.wikipedia.org/wiki/G%C3%A2teaux_derivative#Definition" }
;

DEFER: dirt
DEFER: γ
DEFER: φ
DEFER: φ⁻¹
DEFER: F
:: FiniteDifferenceOnManifoldUsingCurve ( t dirt γ φ φ⁻¹ F -- ℝ )
 ℝ0 t dirt [ ℝ* ] [ ℝ+ ] [ γ call φ call φ⁻¹ call F call ] [ ℝ- ] [ ℝ/ ] FiniteDifferenceUsingDirection ; inline
 HELP: FiniteDifferenceOnManifoldUsingCurve 
 { $curious "The curves γ that in the limit t->0 gives the same value are members of the equivalence class for the tangent vector (often called γ'(0) )." }
 { $warning "Requires that the curve γ satisfies ℝ0 γ = p" }
 { $examples "This example uses ℝⁿ as the manifold. It computes the finite version of ∂_{(0,1)}‖·‖↾_{(1,3)}"
  { $example 
     "USING: fry derivatives ;" 
     "QUALIFIED: math "
     "QUALIFIED: math.vectors "
     ": Curve ( R -- M ) '[ V{ } _ 1 math:* 1 math:+ suffix 3 suffix ] call ;"
     ": Chart ( Rn -- Rn ) ;" 
     ": ChartInverse ( Rn -- Rn ) ;"
     ": F ( V -- M ) math.vectors:norm ;"
     " 0.001 1 [ Curve ] [ Chart ] [ ChartInverse ] [ F ] FiniteDifferenceOnManifoldUsingCurve"
     "0.3163700542794246"
  }
 }
 { $explanation 
    { ℝ0 ( -- ℝ ) } 
    { t ( -- ℝ ) } 
    { dirt ( -- ℝ ) } 
    { ℝ* ( ℝ ℝ -- ℝ ) } 
    { ℝ+ ( ℝ ℝ -- ℝ ) } 
    { γ ( ℝ -- M ) } 
    { φ ( M -- ℝⁿ ) } 
    { φ⁻¹ ( ℝⁿ -- M ) } 
    { F ( M -- ℝ ) }
    { ℝ- ( ℝ ℝ -- ℝ ) } 
    { ℝ/ ( ℝ ℝ -- ℝ ) } 
 }
;

:: DerivativeOnManifoldUsingCurve  ( γ φ φ⁻¹ F -- ℝ )
! TODO: Make it a limit
  0.001 1 [ γ call ] [ φ call ] [ φ⁻¹ call ] [ F call ] FiniteDifferenceOnManifoldUsingCurve ; inline
 HELP: DerivativeOnManifoldUsingCurve 
 { $curious "The curves γ that in the limit t->0 gives the same value are members of the equivalence class for the tangent vector (often called γ'(0) )." }
 { $warning "Requires that the curve γ satisfies ℝ0 γ = p" }
 { $examples "This example uses ℝⁿ as the manifold. It computes the limit version of ∂_{(0,1)}‖·‖↾_{(1,3)}"
  { $code 
     "USING: fry derivatives ;" 
     "QUALIFIED: math "
     "QUALIFIED: math.vectors "
     ": Curve ( R -- M ) '[ V{ } _ 1 math:* 1 math:+ suffix 3 suffix ] call ;"
     ": Chart ( Rn -- Rn ) ;" 
     ": ChartInverse ( Rn -- Rn ) ;"
     ": F ( V -- M ) math.vectors:norm ;"
     " [ Curve ] [ Chart ] [ ChartInverse ] [ F ] DerivativeOnManifoldUsingCurve"
  }
 }
 { $explanation 
    { γ ( ℝ -- M ) } 
    { φ ( M -- ℝⁿ ) } 
    { φ⁻¹ ( ℝⁿ -- M ) } 
    { F ( M -- ℝ ) }
 }
;

 DEFER: H
 DEFER: γ
 DEFER: F
 :: PushForward ( H -- N ) '[ [ _ H call ] _ _ _ DerivativeOnManifoldUsingCurve ] ;
 HELP: PushForward 
 { $values 
    { H ( M -- N ) } 
 }
  { $notes "TODO: is this wrong? See i.e. https://math.stackexchange.com/a/1277317/68036" }
;