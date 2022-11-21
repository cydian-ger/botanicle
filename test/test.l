expose (x, y, z) as (a, b ,c) with ("a > b > c")
include leaf.l as λ
define z as 0.9
group (A, B, C) as β
group (β, C) as γ
ignore (0, 1, 2, 3, 4)

# comment
# →A(1, z)
.test A(a, a2) < B(b)       : b == a            → A(1, 1)B(1 + b)
Z(z) < Y(y) > Z(zz)         : z == zz           → X(1)
L(a)                        : (a == b)          → L(a + 1, $a)
$prev((b), (a)) < A(a)      :                   → $weighted((@test, _), (1, 2))
.test                                           → X(1)
# This is a comment