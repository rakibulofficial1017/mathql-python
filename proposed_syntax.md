# MathQL: Language Specification & Examples

# 1. Philosophy

MathQL is an interpreted programming language implemented in Rust, designed for mathematics, numerical computation, symbolic mathematics and general purpose programming

MathQL's principals:
- Everything that makes sense to evaluate should produce a value
- Blocks return the value of their final expression.
- Control-flow expressions can be assigned to variables.
- Mathematical operations should support exact results where possible
- Types should be checked at runtime by the intterpreter
- Mathematical structures (like vectors and matrices) must be first-class values
- Syntax should remain readable without being Java (synonym for verbose)

# 2. Printing and expressions
```
// Printing and evaluation

"Hello world!"
'Hello world!'
5 + 5

// Expressions evaluate to values
2 + 3 * 4             // 14
(2 + 3) * 4           // 20

// The REPL displays the result of each expression
x := 10
x                     // 10

// Explicit printing
print("Hello world!")
print(5 + 5)

// The previous result
ans * 4               // Uses the previous evaluated result
```
**ans** stores the value of the previous successfully evaluated expression, Reading **ans** does not change it

# 3. Comments
```
// this is a single line comment
/* 
this is a multiline comment
It can span multiple lines
*/
```
# 4. Variables and constants
```
// Variable declaration

let x = 10
let name = "John"

x                      // 10
name                   // "John"

// Reassignment

x := 20
x                      // 20

// Constants

const pi = 3.141592653589793
const greeting = "Hello"

// This is an error because pi is a constant
// pi := 3

// Multiple variables

let a = 10
let b = 20
let c = a + b

// Simultaneous assignment, if supported
a, b := b, a           // Swaps a and b
```
### Assignment and equality
```
let x = 10
y := 15
y = 15 // True

x = 10                 // True: equality comparison
x != 10                // False

let x = 20              // Reassignment
x := 15                 // Reassignment
x = 15                 // True

```
= compares values. := assigns or reassigns a value.

let declares a variable, while const declares a constant. Redeclaring a name in the same scope is an error unless an explicit shadowing rule permits it.

# 5. Scopes
```
let x = 10

{
    let x = 40
    x               // 40
}

x                   // 10
```
a block creates a lexical scope. a variable declared insode a block does not replace the variable in the outer scope unless the global keyword is used

let x = 10

{
    let global x = 10
    x               // 40
}

x                   // 40
```

If a block evaluates to an expression, the final expression is returned, an empty block returns a null value

let result = {
    let a = 10
    let b = 10
    a + b
}

result       // 30

# 6. Data types

```
// Numeric types

let a = 10             // integer
let b = 10.5           // real
let c = 1 / 3          // exact rational, where supported
let d = 3 + 4i         // complex
```

// Other types

let text = "Hello"     // string
let active = true      // boolean
let nothing = null     // null

// Type inspection

type(10)               // integer
type(10.5)             // real
type(3 + 4i)           // complex
type("Hello")          // string
type(true)             // boolean
```
### Optional type constraints
```
let integer x = 10
let real y = 3.14
let complex z = 2 + 3i
let text name = "John"
let boolean valid = true

// Runtime type errors

let integer x = 3.5
let real y = "Hello"
complex z := true 
```
Type annotations specify the types a value must satisfy. Since MathQL is interpreted, the interpreter checks these constraints at runtime.


### Mathematical type relationships

```
integer ⊆ rational ⊆ real ⊆ complex

// Examples

let integer n = 5
let rational r = 1 / 3
let real x = sqrt(2)
let complex z = 2 + 3i
```

Conversion rules should be explicit and consistent.
```
// A complex number can be converted to a real number
// only if the conversion rules permit discarding its
// imaginary component.

convert(3 + 0i, real)       // 3.0

// A nonzero imaginary component should not be
// silently discarded in a strict conversion.
// convert(3 + 4i, real)    // TypeError
```

text-to-number conversion should parse the entire text unless a separate parsing function explicitly allows partial parsing.

convert("32", integer)      // 32
convert("3.14", real)      // 3.14

// Invalid input
// convert("32abc", integer) // ConversionError

# 8. Complext numbers and the Imaginary number

```
let z = 3 + 4i
let w = 2i

z + w                       // 3 + 6i
z * w                       // -8 + 6i
abs(z)                      // 5
```
The imaginary unit satisfies `i^2 = -1`

### Variables named `i`

The imaginary unit and a user variable named i can conflict. MathQL resolves this consistently.

```
let i = 4

i                          // 4: explicitly refers to the variable
2 + i                      // 6

2 + \i                       // 2 + 1i in an unambiguous
                             // mathematical expression
```
# 9. Arithmetic
```
5 + 3                       // 8
5 - 3                       // 2
5 * 3                       // 15
5 / 2                       // 5/2 when exact rational
5 ^ 3                       // 125
5 %% 2                      // 1

sqrt(16)                    // 4
abs(-5)                     // 5
floor(3.8)                  // 3
ceil(3.2)                   // 4
round(3.14159, 2)           // 3.14
```

Remember all builtin functions, and variables (even if shadowed) are still available as \name such as \sin, \cos, \max

Exponentiation uses ^

Division should preserve exactness where possible. For example, 1 / 3 can produce an exact rational rather than an approximation, while operations requiring floating-point evaluation may produce a real approximation.

# 10. Infinity, Undefined Results and Errors

```
// Mathematical special values

Inf + 1                     // Inf
Inf + Inf                   // Inf

Inf - Inf                   // NaN
Inf / Inf                   // NaN
Inf * 0                     // NaN
```

# 11. Strings
```
let text = "Hello"
let other = 'world'

text + " " + other          // "Hello world"

let multiline = "This is a
multiline string."

len(text)                   // 5
"ell" in text               // true
```
### Escape sequences
```
"\n"                        // Newline
"\t"                        // Tab
"\r"                        // Carriage return
"\\"                        // Backslash
"\""                        // Double quote
"\'"                        // Single quote
```
String concatenation should accept strings. Automatic conversion is not allowed

`"Value: " + convert(10, string)  // "Value: 10"`

# 12. Boolean Logic and Comparisons
```
10 > 5                      // true
10 < 5                      // false
10 = 10                     // true
10 != 5                     // true
10 >= 10                    // true
10 <= 5                     // false

true and false              // false
true or false               // true
true xor false              // true
not true                    // false
```

Logical operators should use short-circuit evaluation where appropriate.
```
false and some_function()   // Does not call the function
true or some_function()     // Does not call the function
```

Comparisons between incompatible types should produce a clear error rather than an arbitrary result.

# 13. Conditional Expressions
```
let a = 33
let b = 200

let message = if b > a {
    "b is greater than a"
} else if a = b {
    "a and b are equal"
} else {
    "a is greater than b"
}

message
```
The entire conditional is an expression. It returns the value of the branch that executes.

let absolute = if x < 0 {
    -x
} else {
    x
}
All branches of a value-producing conditional should return compatible types. A branch that performs no meaningful computation can return null.

# 14. Loops as expressions
### While loops
```
let i = 0

while i < 5 {
    print(i)
    i += 1
}
```


A while loop without a break value returns null.

### For loops
```
for i in 1..5 {
    print(i)
}
```
Ranges are inclusive at both ends unless explicitly specified otherwise.

### Collecting values
```
let squares = for i in 1..10 {
    i ^ 2
}


squares
// [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

let even_squares = for i in 1..10 {
    if i %% 2 = 0 {
        i ^ 2
    }
}

// The exact filtering behaviour should be explicit:
// either null results are retained, or a separate
// filter expression is used.

```
When used as an expression, a for loop collects the value of its final expression on each completed iteration into a list.

### Break and continue

```
let result = while true {
    if x = 10 {
        break x
    }
    x += 1
}

// result receives the break value
```
break value exits the nearest enclosing loop and supplies its result.

```
for i in 1..10 {
    if i = 5 {
        continue
    }
    print(i)
}
```
continue skips the rest of the current iteration.

Loop result rules

- A for loop normally returns a list of iteration results.
- A while loop normally returns null.
- break value returns the explicit break value.
- break without a value returns null.
- continue advances to the next iteration.

These rules are consistent even when loops are nested.


# 15. Blocks and Final Expressions
```
let result = {
    let x = 10
    let y = 20
    x * y
}

result // 200

let result = {
    let x = 10
    let y = 20
    print(x)
}
result // null
let result = {
    let x = 10
    let y = 20
    x * y
    print(x)
}
result // null
let result = {
    let x = 10
    let y = 20
    x * y
    print(x);
}
result // 200
```

# 16. Functions

There are 4 (or 5) different ways to define functions in MathQL

```
func add(x, y) {
    x + y
}
let sub = func(x, y){
    x - y
}
let mul = lambda x, y: x*y // or even λx.λy.(x*y)

let div(x, y) = x/y

func factorial(n) {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}

factorial(5)                // 120
```
Explicit return
```
func greet(name) {
    return "Hello " + name
}

greet("John")               // "Hello John"
```
return exits the current function and supplies its return value.
func greet(name = "human") {
    "Hello " + name
}

greet()                     // "Hello human"
greet("John")               // "Hello John"

### Functions as values
```
let add = func(x, y) {
    x + y
}

add(3, 4)                   // 7
```


Named functions and anonymous functions should share the same calling semantics

# 17. Collections

### Lists

Lists are ordered, resizable collections.
```
let numbers = [1, 2, 3, 4]
let mixed = ["apple", 10, true]

numbers[0]                  // 1
numbers[-1]                 // 4
```
List indexing is zero-based. Negative indices count from the end.
```
numbers[0] := 10
numbers + [5, 6]            // Concatenated list
```

### Tuples

Tuples represent fixed-size collections that may contain different types.
```
let person = ("John", 16)
person[0]                   // "John"
```
### Sets

Sets contain unique values.
```
let unique = set{1, 2, 2, 3}
unique                      // {1, 2, 3}, display format may vary

2 in unique                 // true
```
Set iteration order is not guaranteed unless the implementation specifies otherwise.

### Maps

Maps associate keys with values.
```
let scores = map{
    "Math": 95,
    "CS": 98
}

scores["Math"]              // 95
```
Map keys must satisfy the language's rules for equality and hashing.

Typed collections
```
let list<integer> numbers = [1, 2, 3]
let list<string> names = ["John", "Mary"]
let map<string, integer> scores = map{"Math": 95}
```
The interpreter checks the declared element or key/value types at runtime.

# 18. Vectors and Matrices

Vectors and matrices are mathematical structures, not merely ordinary lists.
```
let vector<real> v = [1, 2, 3]
let vector<real> w = [4, 5, 6]

dot(v, w)                   // 32
norm(v)                     // sqrt(14)
cross(v, w)                 // [-3, 6, -3]
```
Scalar multiplication:
```
2 * v                       // [2, 4, 6]
```
Matrices
```
let A = matrix([[1, 2], [3, 4]])
let B = matrix([[5, 6], [7, 8]])

A + B
A * B                       // Matrix multiplication
transpose(A)
det(A)                      // -2
inverse(A)
identity(3)
```
Matrix dimensions must be validated before operations. Matrix multiplication is only valid when the number of columns in the first matrix equals the number of rows in the second.

Element-wise multiplication should have a separate, clearly documented operator or function.

# 19. Ranges
```
1..5                        // [1, 2, 3, 4, 5]
1..10                       // Inclusive range
range(0, 10, 2)             // [0, 2, 4, 6, 8, 10]
0..2..10                    // [0, 2, 4, 6, 8, 10]
```
Ranges should ideally be lazy iterable values rather than allocating an entire list immediately.
```
for i in 1..1000000 {
    // Iterates without needing a million-element list
}
```
If the range is inclusive, its endpoint is included only when reached by the chosen step.

# 20. Mathematical Functions

Arithmetic and algebra
```
abs(x)
sqrt(x)
exp(x)
pow(x, y)
log(x, base)
ln(x)
mod(x, y)
sign(x)
```
Trigonometry
```
sin(x)
cos(x)
tan(x)
asin(x)
acos(x)
atan(x)
atan2(y, x)
```
Hyperbolic functions
```
sinh(x)
cosh(x)
tanh(x)
```
Functions should support complex inputs when mathematically defined and implemented.
```
cos(1i)                     // cosh(1), for radian input
```
Angles are measured in radians by default.

Calculus
```
diff(f(x), x)                  // Derivative, if supported
diff(f(x), x, 2)                // Derivative evaluated at x = 2
f'(2)                          // Does the exact same thing as the previous line
integrate(f(x), a, b, x)       // Definite numerical integral
limit(f(x), x, target)         // Limit as x approaches target
```
The language should distinguish symbolic differentiation from numerical differentiation and exact integration from numerical approximation.

Equation solving
```
solve(3*x = 4, x)            // x = 4/3
solve(x^2 = 9, x)            // Multiple solutions
```
A solver should distinguish exact symbolic solutions from numerical approximations.

When multiple solutions exist, it should return a collection of solutions or require an explicit selection rule. It should not silently choose one arbitrary solution.

A solver should distinguish exact symbolic solutions from numerical approximations.

When multiple solutions exist, it should return a collection of solutions or require an explicit selection rule. It should not silently choose one arbitrary solution.

# 21. Linear Algebra and Statistics
```
mean([1, 2, 3, 4, 5])       // 3
median([1, 2, 3, 4, 5])     // 3
sum([1, 2, 3, 4, 5])        // 15
product([1, 2, 3, 4])       // 24
variance([1, 2, 3, 4, 5])
stddev([1, 2, 3, 4, 5])

```
Linear algebra:
```
dot(v, w)
cross(v, w)
norm(v)
det(A)
inverse(A)
transpose(A)
eigenvalues(A)
eigenvectors(A)
```
The standard library should document whether statistical variance and standard deviation use population or sample formulas.

# 22. Iteration and Functional Operations

let numbers = [1, 2, 3, 4, 5]

map(numbers, func(x) {
    x ^ 2
})

filter(numbers, func(x) {
    x %% 2 = 0
})

sum(numbers)

These operations provide alternatives to explicit loops while preserving the same expression-oriented design.

23. Error Handling

// Invalid operations should produce clear errors

// 10 + "hello"              // TypeError
// sqrt("hello")             // TypeError
// unknown_variable          // NameError

Runtime errors should report the relevant expression and location when available.

The interpreter should distinguish:

- Syntax errors
- Name-resolution errors
- Type errors
- Mathematical domain errors
- Runtime errors

Invalid operations should not return null unless the function's documented semantics explicitly require it.


24. Implementation Principles

MathQL is interpreted by Rust.

The interpreter should evaluate an abstract syntax tree into runtime values rather than requiring MathQL source code to be compiled into machine code.

A runtime value may represent:

- Integers and exact rationals
- Real and complex numbers
- Booleans, strings, and null
- Lists, tuples, sets, and maps
- Vectors and matrices
- Functions and other supported runtime objects

Expression evaluation should return either a value or an error. Control-flow operations such as break, continue, and return must also propagate correctly through nested expressions.

Type constraints are checked by the interpreter at runtime. The language may later add static analysis, but it should not depend on compilation to enforce its basic semantics.

The core evaluator should be designed around a single principle:

Every ordinary expression evaluates to a value, and every control-flow construct has clearly defined rules for producing or propagating that value.