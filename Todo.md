# Common Turtle Instructions .cti
Simplify the output into move / rotate / stack commands etc

Move-commands A-Z are -> Move(+x)
M(amount: Optional<float>)  # Put 1 if no value is given

Turn-commands yaw, roll, pitch -> Turn(+yaw, +roll, +pitch)
T(yaw: float, r: float, p: float)

Brush-Commands Brush-Size-Increase, Brush-Size-Decrease -> Brush(+size)
B(size: float)  # Maybe int

Pen-Commands pen-up, pen-down -> Pen(Command)
P(command: Enum)  # Enum: pen-up, pen-down

Stack-Commands Stack-Push, Stack-Pop -> Stack(Command)
S(command: Enum)  # Enum: stack-push, stack-pop

S, T, P, B, S

## Example:
```
11[1[0]0]1[0]0 -(without reduction)-> 

[HEADER-DATA]
[
(M, (1)),
(M, (1)),
(S, (PUSH)),
(M, (1)),
(S, (PUSH)),
(M, (1)),
(S, (POP)),
(M, (1)),
(S, (POP)),
(M, (1)),
(S, (PUSH)),
(M, (1)),
(S, (POP)),
(M, (1))
]
```

## Reduction
Repeating valued-commands of the same type get concatenated into one
```
11[1] ->
# 
[
(M, (2)),
(S, (POP)),
(S, (PUSH))
]
```

A valued command is any command that does not have an enum but a float as its value
so Move and Rotate and Brush Size.

However there are some extra rules
A Stack Push <kbd>[</kbd> followed by a Stack Pop <kbd>]</kbd>
will be removed from the final list since it does not have an impact.

Same goes for Pen Up followed by Pen down, though the opposite is also true
So Pen Down followed by Pen Up is also removed from the final .cti
