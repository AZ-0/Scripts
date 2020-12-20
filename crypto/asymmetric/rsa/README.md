# RSA
> Written by [A~Z](https://github.com/AZ-0)

> [Home](../../../README.md)

## Principle
[Source](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
### Key Generation
1. Find `p` and `q`, two distinct large prime numbers.
1. Compute the modulus `n`: `n = pq`
1. Choose either one of these modes: ─ we will note the result `φ(n)` in the following steps
  - Compute Carmichael's totient function in `n`, `λ(n) = lcm(p - 1, q - 1)`
  - Compute Euler's totient function in `n`, `φ(n) = (p - 1)(q - 1)`
1. Find the public exponent `e` such that:
  - `1 < e < φ(n)`
  - `e` and `φ(n)` are coprime
  - Note: the most common public exponent is `2^16 + 1 = 65537` (prime)
1. Compute the private exponent `d` as the modular inverse of `e` modulo `φ(n)`

The public key is the couple `(e, n)` and the private key is the couple `(d, n)`.
The security of the RSA scheme lies in that there is no known method to factor `n` in any reasonable time,
however several attacks exist in specific instances of the problem.
If one were to factor `n`, they could find `φ(n)` hence deduce the private exponent `d`.

### Encryption
Convert your plaintext message to an integer `m` such that `0 <= m < n` using a bijection, that is you should be able to translate a given m to plaintext back and forth.
Usually one would represent the message in hexadecimal charcodes, and let m be the generated number.
(it is possible to split the message in chunks encrypted separately if m is larger than n).

For a given m, we can find the associated ciphertext `c` with: `c ≡ m^e [n]`.
We would then send `c` to whoever needs to read it (they will be the only one able to decrypt it).

### Decryption
For a given ciphertext `c`, compute `m` with: `m ≡ c^d [n]`. This equality holds because of [Euler's theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem).
You can then reverse `m` to the plaintext message using the same bijection.

### Multiprime RSA
Instead of choosing `p` and `q`, choose any number `k` of distinct primes `p_i`. The above formulaes are then extended as:
  - `n = Π(p_i)`
  - `λ(n) = lcm(p_1 - 1, p_2 - 1, ..., p_k - 1)`
  - `φ(n) = Π(p_i - 1)`

Encryption and decryption remain the same. Multiprime RSA (MPRSA) possess variants (such as Batch Multiprime RSA) that are faster than classic RSA,
however it is much faster and easier to factor `n`.

## Implementation Details

### [Python](rsa.py)
- Encryption
- Decryption
- Multiprime RSA support
- Various computations (e.g computing `d` or `φ(n)`)