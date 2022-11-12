##

### LToken
Ltoken in matches can be groups or generics,
while a Ltoken that appears in a result must be definitive:
e.g. using a generic when there is no generic in the match section is invalid.
#### Identity
Two LToken are considered equal only when the axiom name matches and the two have the same amount of arguments

##### Group Identity
```
group (A, B) as β
A(a)    == β(b) is True because A is in the Group
C(c)    == β(b) is False because A is in the Group
β(a)    == β(a) is True as the groups are the same
β(a, b) == β(b) is False as the amount of arguments are missmatched
```

#### Overloading
1 LToken can be overloaded with different iterations on the condition
that there are no two LTokens with the same name and the same amount of parameters.

### Rule
A rule consists of up to 4 parts.
```
.rule1 A(a) < B(b) > C(c)    : c == b == a   → B(b + 1)
```
Any given rule can either apply or not apply.
A rule only applies if the match (including Context) as well as the condition are fulfilled.

#### Assignment
The name assignment / line assignment of a rule is optional,
however if the rule is to be used in another rule e.g. using <kbd>$weighted</kbd> 
having a unique identifier is necessary in order to call the rule.

#### Match
The match consists of up to 3 parts of which only 1 is necessary: The Token Match
The token match can only consist 1 Axiom or catch group.
```
A < B > C
   ^^^
This part is the Token-Match
```

##### Context
The other two optional parts are lists of Context Matches.
There is right context ">", and left context "<".

Right context would be followed by {1..n} LTokens while left context would be preceded by
{1..n} LTokens.



### Keywords
#### Group
A group allows matching a limited amount of characters
that have the same amount of variables.
```
group {A, B} as β

β(a) : => β(a + 1)
β(a, b) : => β(a + b, b + 1)
```
<kbd>β(a)</kbd> would match <kbd>B(n)</kbd> and <kbd>A(n)</kbd> 
but not <kbd>A(n, m)</kbd> or <kbd>C(n)</kbd>.
The name of the match as well as the variable count have to match the Rule.

The matched axiom can be retrieved with the letter.
```
β(a) > β(b, c) : => β(a + b + c)
```
This is a valid expression since both <kbd>β</kbd> are considered different axioms

This is done because value retrieval of matches would be impossible if the number
of variables can change depending on the match.
