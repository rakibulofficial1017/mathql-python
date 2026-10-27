import mathql_rust

code = """
let i = 10
let mut i = 0o30
f(x)=10x
"""

tokens = (mathql_rust.tokenize(
    code
))

for i in tokens:
    print(i)