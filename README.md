# Lambdifier
Lambdifier is a Python obfuscation tool that transforms normal* python scripts into a one liner that uses only lambdas and function applications.
Here is what the `examples/simple.py` script comes out when obfuscated
```py
(lambda _0: _0(37))(lambda _1: (lambda _2: _2(lambda _3: lambda _4: _3 == _4))(lambda _5: (lambda _6: _6(lambda _7: lambda _8: _7 + _8))(lambda _9: (lambda _10: _10(print))(lambda _11: (lambda _12: _12('Hello World!'))(lambda _13: (lambda _14: _14(_11(_13)))(lambda _15: lambda _16: _16))))))
```

(\*) Not really, see below.

## Usage
```
usage: lambdifier.py [-h] [-l {0,1,2,3}] [-d] input_file

positional arguments:
  input_file            input file to obfuscate

options:
  -h, --help            show this help message and exit
  -l {0,1,2,3}, --level {0,1,2,3}
                        obfuscation level:
                            - 0: curry transform
                            - 1: normalize
                            - 2: bind functions
                            - 3: obfuscate names
                            
  -d, --deobfuscate     deobfuscate instead of obfuscate
```

Input scripts are split by a
```py
# obfuscate
```
comment. All the things that come before it will not be obfuscated, and will be copied as they are in the output script.

## How it works
The obfucator applies a pipeline of four abstract syntax tree transformations.
1. All the lambda functions definitions and function applications are transformed into their curryed version, to enable doing partial application. This is crucial for example for achieving recursion using the fixpoint combinator.
2. All the constant symbols and function applications are recursively extracted from the original expressions and put into their own definitions. Since the function calls are curried, function calls with multiple arguments are split between different assignments.
3. All assignments are converted into their lambda forms, exploiting lambda variable binding.
4. All names are obfuscated and transformed into meaningless numbers.

Using the `-l` flag it is possible to inspect the intermediate forms of the script.

The flag `-d` basically applies an inverse transformation of the third step, making the obfuscated script much more readable (or at least a bit comprehensible).

## Limitations

Input scripts have to respect certain conditions, namely
- there must be only assignments at top level,
- only lambda functions are supported (who would have guessed),
- recursion is not supported, but you can get recursion by using the fixpoint point combinator,
- assignments must have unique names (basically only let semantics is supported without shadowing),
- other random python features break this tool pretty bad, so use with caution.

