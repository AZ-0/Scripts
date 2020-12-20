# Written by A~Z
from math import gcd

PHI_EULER_TOTIENT = 'euler'
PHI_CARMICHAEL_TOTIENT = 'carmichael'

def egcd(a: int, b: int) -> tuple:
    '''
    Extended euclidean algorithm: au + bv = gcd(a,b)

    Output: gcd(a,b), u, v
    '''
    if a == 0:
        return (b, 0, 1)
    else:
        g, v, u = egcd(b % a, a)
        return g, u - (b // a) * v, v


def modinv(a: int, m: int, log: bool = False) -> int:
    '''
    Modular inverse: a*a^-1 ≡ 1 [m]

    Output: a^-1

    Special Case:
      • if a and m are not coprime, a^-1 doesn't exist
    '''

    # a*a^-1 ≡ 1 [m] ⇔ a*a^-1 + k*m = 1, with k ∈ Z
    # Solving the bezout equation au + km = 1 in u gives a^-1
    g, u, _ = egcd(a, m)

    if g != 1:
        raise Exception('Modular inverse does not exist: number {a} is not coprime to modulus {m}')
    else:
        return u % m


def lcm(a: int, b: int) -> int:
    '''
    Least common multiple: gcd(a,b) = ab/m
    
    Output: m

    Special Case:
      • if a and b are coprime, lcm(a,b) = a*b
    '''
    return a*b // gcd(a, b)


def foldl(operation, accumulator, iterable):
    '''
    Fold left: Folds an iterable by iterating over its elements and accumulating it through the operation
    
    Examples:
      • sum(numbers)  = foldl(lambda a,b: a+b, 0, numbers)
      • prod(factors) = foldl(lambda a,b: a*b, 1, factors)
      • reduce(iterable,  op) = foldl(op, iterable[0], iterable[1:])
      • reduce(generator, op) = foldl1(op, generator)

    Note:
      • operation should be a binary function
    '''
    for elem in iterable:
        accumulator = operation(accumulator, elem)

    return accumulator


def foldl1(operation, generator):
    '''
    Fold left 1st: Convenience method for foldl using first element outputed by the generator as the accumulator

    Equivalent to:
      • foldl(operation, next(generator), generator)

    Note:
      • Doesn't support non-generator iterables, either compose with iter or use foldl(operation, subscriptable[0], subscriptable[1:]) instead
    '''
    return foldl(operation, next(generator), generator)


def prod(factors):
    '''
    Product: p = factors[0]*factors[1]*...*factors[len(factors) -1]

    Output: p

    Disambiguation:
      • Supports any iterable, not just subscriptables
    '''
    return foldl(lambda a,b: a*b, 1, factors)


def compute_n(*factors: int, log: bool = True) -> int:
    '''
    RSA's modulus n: n = prod(factors)

    Output: n

    Note:
      • Use p and q for classic RSA
    '''
    factors = tuple(factors)
    if len(factors) < 1:
        raise Exception("Cannot compute modulus n: Not enough factors")

    n = prod(factors)
    if log:
        print('n:', n)
    
    if n < 1:
        raise Exception("Could not compute modulus n: Invalid modulus (should be strictly positive)")
    
    return n


def compute_phi(*factors: int, method: str = PHI_EULER_TOTIENT, log: bool = True) -> int:
    '''
    RSA's private exponent d computation step, find φ(n):
      • using Euler's totient function:      φ(n) = (p - 1)(q - 1)
      • using Carmichael's totient function: φ(n) = lcm(p - 1, q - 1)

    Output: φ(n)

    Note:
      • Above formulaes for φ(n) are extended when dealing with multiprime RSA
      • Also known as λ(n) when using Carmichael's totient function
    '''
    if method.lower() not in {PHI_EULER_TOTIENT, PHI_CARMICHAEL_TOTIENT}:
        raise Exception('Unknown method "{method}" to compute phi(n). Supported: PHI_EULER_TOTIENT; PHI_CARMICHAEL_TOTIENT.')

    if len(factors) < 1:
        raise Exception('Cannot compute phi: Not enough factors')

    if log:
        print(f"> Computing phi using {method.title()}'s totient function")
    
    if method.lower() == PHI_EULER_TOTIENT:
        return prod(map(lambda x: x-1, factors))

    phi = foldl1(lcm, map(lambda x: x-1, factors))
    if log:
        print('phi:', phi)

    return phi


def compute_d(e: int, phi: int = -1, factors: list = None, phi_method = PHI_EULER_TOTIENT, log: bool = True) -> int:
    '''
    RSA's private exponent d: ed ≡ 1 [φ(n)]

    Output: private exponent d

    Arguments (either of below):
      • public exponent e, φ(n)
      • public exponent e, factors (p and q for classic RSA)
          • optional: phi_method (see compute_phi)
    '''
    if phi < 1:
        phi = compute_phi(*factors, method=phi_method, log=log)

    if e < 1:
        raise Exception('Cannot compute private key d: Invalid exponent (should be strictly positive)')

    d = modinv(e, phi)
    
    if log:
        print('d:', d)
    
    return d


def decrypt(ct: int, d: int = -1, n: int = -1, e: int = -1, factors: list = [], phi: int = -1, phi_method: str = PHI_EULER_TOTIENT, log: bool = True) -> int:
    '''
    Decrypt RSA: plain ≡ cipher^d [n]

    Output: plain

    Arguments (either of below) -> computing modulus n:
      • modulus n
      • factors (p and q for classic RSA)

    Arguments (either of below) -> computing private exponent d:
      • private exponent d
      • public exponent e, φ(n)
      • public exponent e, factors (p and q for classic RSA)
          • optional: phi_method (see compute_phi)
    '''
    if n < 1:
        n = compute_n(*factors, log=log)

    if d < 1:
        d = compute_d(e=e, phi=phi, factors=factors, log=log)

    return pow(ct, d, n)


def encrypt(pt: int, e: int, n: int = -1, factors: list = []) -> int:
    '''
    Encrypt RSA: cipher ≡ plain^e [n]

    Output: cipher

    Arguments (either of below):
      • public exponent e, modulus n
      • public exponent e, factors (p and q for classic RSA)
    '''
    if n < 1:
        n = compute_n(*factors)
    
    return pow(pt, e, n)
