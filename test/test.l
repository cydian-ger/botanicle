expose (a, b ,c) with ("a > b > c")
include ./leaf.l as λ
define z as 0.9
group β as (A, B, C)
group γ as (β, D)
ignore (0, 1, 2, 3, 4)

# comment
# →A(1, z)
.test A(a) < B                          : a == b            → A("a", "a / (b - 1)")B(1 + b)
Z(z1) < Y(y) > Z(z2) A                   : z == zz          → X(1,,)
L(a)                                    : (a == b, b == c)  → L(a + 1)
# $prev((b), (a)) < A(a)                  :                   → $weighted((@test, _), (1, 2))
.test2  B                                                   → X(1)
.abba A < B > C : → D
.damp A < B > C(c) : → E
# This is a comment
