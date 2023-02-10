# Knowledge Script Virtual Machine
KSVM is a virtual machine for executing Knowledge Scripts. Knowledge Scripts are a simple, declarative language for representing knowledge and do reasoning over it.

## Syntax
### Concepts
to define a concept, use the `cpt` keyword followed by the concept name, then the concept's datatype or the value options seperated by `/`.
example:
if we want to define a concept named `color` with the value options `red`, `green` and `blue`, we would write:
```
cpt color red/green/blue
```
if we want to define a concept named `age` which is a number, we would write:
```
cpt age num
```
if we want to define a concept named `isAlive` which is a boolean, we would write:
```
cpt isAlive bool
```
### Rules
rules are written in the following format:
```
if <condition> then <bool concept>
```

#### Operations
the following operations are supported:
* `and` - logical and
* `or` - logical or
* `gt` - greater than
* `lt` - less than
* `eq` - equal to

#### Conditions
conditions are written in the following format:
```
<concept> <operation> <value>
```
example:
if we want to define a rule that says that if the color is red and the age is greater than 18, then the person is an adult, we would write:
```
if (color eq red) and (age gt 18) then isAdult
```
note that the parentheses are used to define the order of operations.

isAdult is a boolean concept, so we can use it in other rules.

### Examples
define a concept named `color` with the value options `red`, `green` and `blue` and a concept named `age` which is a number

if the color is red and the age is greater than 18, then the person is an adult, if the person is an adult and the color is red, then the person is dead.

```
cpt color red/green/blue
cpt age num

if (color eq red) and (age gt 18) then isAdult
if (isAdult eq true) and (color eq red) then isDead
```

## Compiling
build using nuitka3
```
nuitka3 --standalone ksvm.py
```
## Demo
run the demo with the compiled executable
```
./ksvm.dist/ksvm demo.ks
```
or with python3
```
python3 ksvm.py demo.ks
```