# Lsystems
An L-System file is made up of statements and rules

# Rules
Rules

# Statements
A statement defines behaviour during the production.

## define
```
Syntax: define <name> <alias> <value>
Examples: 
define z as 0.9
define value as 100.01
```
<kbd>define</kbd> defines a variable which can then be used inside of
expressions in the file.

## expose
```
Syntax: expose <List[Expression]> |Optional| <with> <List[Expression]> 
Example:
expose (a, b, c)
expose (a, b, c) with ("a > b > c", "b > 2")
```
<kbd>expose</kbd> exposes variables such that if another file calls this file.

TODO
think about: does the use of condition at expose makes sense

## group
```
Syntax: group <Special_Token> <alias> <List[Token]>
group Γ as (A, B, C)
group Ψ as (Γ, D)
```
<kbd>group</kbd> groups multiple Tokens under the alias of a special token.

## ignore
```
Syntax: ignore <List[Token]>
ignore (A, B)
```
<kbd>ignore</kbd> ignores tokens during context evaluation.

## include
```
Syntax: include <Path> <alias> <Special_Token>
include ./leaf.l as Π
```
<kbd>include</kbd> includes another file as a special token and at the end of production
replaces the token by the specified production parameters of the file.
