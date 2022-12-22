expose (a, b, c) with ("a > b > c + Turtle.heading")
include ./leaf.l as λ
define z as 0.9
group Γ as (A, B, C)
group Ψ as (β, D)
ignore (0, 1, 2, 3, 4)

# comment
.start → A(1.0)B(1.0)
.name → A(1.9)

.test A(a) < Γ > A                      : "a == b"               → A("a", "a / b + a + seed(1.0, 1.0, 1)")B(1 + b)
Z(z1) < Y(y) > Z(z2) A                  : "z == zz"             → X(1.0)
L(a)                                    : ("a == b", "b == c")  → L(a + 1.0)
# $prev((b), (a)) < A(a)                  :                       → $weighted((@test, _), (1, 2))
.test2  B                                                       → X(1.0)
.abba A < B > C                         :                       → D
.damp A < B > C(c)                      :                       → E
# This is a comment