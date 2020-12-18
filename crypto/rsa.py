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
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a: int, m: int, log: bool = False) -> int:
    '''
    Modular inverse: a*a^-1 ≡ 1 [m]

    Output: a^-1

    Special Case:
    • if a and m are not coprime, a^-1 doesn't exist
    '''

    # a*a^-1 ≡ 1 [m] ⇔ a*a^-1 + k*m = 1, with k ∈ Z
    # Solving the bezout equation au + km = 1 in u gives a^-1
    g, x, _ = egcd(a, m)

    if g != 1:
        raise Exception('Modular inverse does not exist: number {a} is not coprime to modulus {m}')
    else:
        return x % m


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
    Folds an iterable from its left side to its right side, sequentially passing the operation through the accumulator and the next element.
    
    Exemples:
      • sum(numbers)  = foldl(lambda a,b: a+b, 0, numbers)
      • prod(factors) = foldl(lambda a,b: a*b, 1, factors)
      • reduce(iterable,  op) = foldl(op, iterable[0], iterable[1:])
      • reduce(generator, op) = foldl1(op, generator)
    '''
    for elem in iterable:
        accumulator = operation(accumulator, elem)

    return accumulator


def foldl1(operation, generator):
    '''
    Convenience method for foldl using first element outputed by the generator as the accumulator
    Equivalent to:
      • foldl(operation, next(generator), generator)

    Note:
      • Doesn't support non-generator iterables, either compose with iter or use foldl(operation, subscriptable[0], subscriptable[1:]) instead
    '''
    foldl(operation, next(generator), generator)


def prod(factors):
    '''
    Product: p = factors[0]*factors[1]*...*factors[len(factors) -1]

    Output: p

    Disambiguation:
      • Supports any iterable, not just subscriptables
    '''
    return foldl(lambda a,b: a*b, 1, factors)


def rsa_compute_n(*factors: int, log: bool = True) -> int:
    '''
    RSA's public key n: n = p*q

    Output: n

    In case of multiprime RSA, n = r*p*q instead
    '''
    factors = tuple(factors)
    if len(factors) < 1 or any(map(lambda x: x < 1, factors)):
        raise Exception("Cannot compute modulus n: Invalid factor (all should be strictly positive)")

    n = prod(factors)
    if log:
        print('n:', n)
    
    return n


def rsa_compute_phi(*factors: int, method: str = 'euler', log: bool = True) -> int:
    '''
    RSA's private key d computation step, find φ(n):
      • PHI_EULER_TOTIENT:      φ(n) = (p - 1)(q - 1)
      • PHI_CARMICHAEL_TOTIENT: φ(n) = lcm(p - 1, q - 1)

    Output: φ(n)

    Note:
      • Above formulaes for φ(n) are extended when dealing with multiprime RSA
      • Also known as λ(n) when using Carmichael's totient function
    '''
    if method.lower() not in {'euler', 'carmichael'}:
        raise Exception('Unknown method "{method}" to compute RSA\'s phi(n). Use either "euler" or "carmichael".')

    if len(factors) < 1 or any(map(lambda x: x < 1, factors)):
        raise Exception('Cannot compute phi: Invalid factor (all should be strictly positive).')

    if log:
        print(f"> Computing phi using {method.title()}'s totient function")
    
    if method.lower() == 'euler':
        return prod(map(lambda x: x-1, factors))

    return foldl1(lcm, map(lambda x: x-1, factors))


def rsa_compute_d(e: int, phi: int = -1, factors: list = None, phi_method = PHI_EULER_TOTIENT, log: bool = True) -> int:
    '''
    RSA's private key d: e*d ≡ 1 [φ(n)]

    Output: d

    Arguments (either of below):
      • φ(n)
      • factors (p and q for classic RSA)
          • optional: phi_method, see rsa_compute_phi
    '''
    if phi < 1:
        phi = rsa_compute_phi(*factors, method=phi_method, log=log)

    if e < 1:
        raise Exception('Cannot compute private key d: Invalid exponent (should be strictly positive)')

    d = modinv(e, phi)
    
    if log:
        print('d:', d)
    
    return d


def rsa_decrypt(ct: int, d: int = -1, n: int = -1, e: int = -1, factors: list = [], phi: int = -1, phi_method: str = PHI_EULER_TOTIENT, log: bool = True) -> int:
    '''
    Decrypt RSA: plain ≡ cipher^d [n]

    Output: plain

    Arguments (either of below) -> computing n:
      • n
      • p, q

    Arguments (either of below) -> computing d:
      • d
      • e, φ(n)
      • e, factors (p and q for classic RSA)
          • optional: phi_method (see rsa_compute_phi)
    '''
    if n < 1:
        n = rsa_compute_n(*factors, log=log)

    if d < 1:
        d = rsa_compute_d(e=e, phi=phi, factors=factors, log=log)

    return pow(ct, d, n)


def rsa_encrypt(pt: int, e: int, n: int = -1, factors: list = []) -> int:
    '''
    Encrypt RSA: cipher ≡ plain^e [n]

    Output: cipher

    Arguments (either of below):
      • n
      • factors (p and q for classic RSA)
    '''
    if n < 1:
        n = rsa_compute_n(*factors)
    
    return pow(pt, e, n)
