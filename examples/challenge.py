import sys
sys.setrecursionlimit(10000000)

# obfuscate


p = 37

eq = lambda x, y: x == y
add = lambda x, y: x + y
mod = lambda x, y: x % y
mul = lambda x, y: x * y
xor = lambda x: lambda y: x ^ y
mul_p = lambda x, y: mod(mul(x, y), p)
add_p = lambda x, y: mod(add(x, y),  p)

# fix point combinator to make recursion possible
F = lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y)))

fact = lambda f, x: 1 if eq(0, x) else mul(x, f(add(-1, x)))
gen_perm = lambda f, x: [] if eq(0, x) else add(f(x - 1), [add_p(x, mul_p(F(fact, 4), x))])
permute = lambda f, x, y: [] if eq(0, len(y)) else add(f(x, y[1:]), [x[y[0]]])
map_ = lambda f, ff, y: [] if eq(0, len(y)) else add([ff(y[0])], f(ff, y[1:]))

group = lambda f, x, y: [] if eq(0, len(y)) else add([y[:x]], f(x, y[x:]))
pad = lambda s, x: s + mul('X',(mod(add(x, -len(s)), x)))
string_to_int = lambda f, s: 0 if eq(0, len(s)) else add(ord(s[0]), mul(256, f(s[1:])))

_a = print("Give me the flag...")
inp = input('λ >')

permuted_ = F(permute, inp, F(gen_perm, p))
permuted = ''.join(permuted_)
padded = pad(permuted, 5)
grouped = F(group, 5, padded)
xorred = xor(mul(0xcafebabe, 42))
mapped1 = F(map_, F(string_to_int), grouped)
mapped2 = F(map_, xorred, mapped1)

res = []
x_1 = res.append(541982718533)
x_2 = res.append(541752425566)
x_3 = res.append(541920185944)
x_4 = res.append(507556842335)
x_5 = res.append(288512657218)
x_6 = res.append(542133179466)
x_7 = res.append(305508892749)
x_8 = res.append(520052997187)

_res = print("That's it!" if eq(res, mapped2) else "Nope!")

# the flag is ifctf{What?_You_want_more_lambdas?__}