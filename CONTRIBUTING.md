# Contribution Guidelines

Beware! This project and the provided scripts are all distributed under the [Unlicense](https://unlicense.org).
That is, by contributing you accept to waive all rights on your contribution and put it in the public domain.
We still keep track of who has contributed to what to some extent though.

If you still want to contribute, please read the following!

## Structure
- Each topic must have its dedicated folder.
- You can nest folders for subtopics.
- You can implement a script in any programming lanfunguage.
- You can provide several implementations of the same script in different languages.
- Each implementation of the same script must have the same name, differentiated by file extension only.
- Each topic/subtopic must contain a `README.md` with a table of contents and list of contributors.
- An entry in a table of contents must link to the related file or folder
- Each script requires an explanation of its underlying principles and/or its goal.
- The explanation of a script must be a markdown file which name is the same as the script's.

## Content
Anything (as long as it's legal and safe for work :p).
By using the provided scripts, you are to follow the laws applicable in your country, and cannot hold the contributors of this repository responsible if you break said laws.

## Format

### Scripts
The author and contributors of a script are to be mentioned in said script ─ if they so wish.
For instance, add comments containing: `Written by <contributor 1>, <contributor 2>` at the start of the file or a function.
> *Replace `<contributor N>` with the name of the contributor n°N, ordered in ascending order by date of contribution*

A function/method in the script must be properly documented, with at least:
- The expected behavior of the function
- The output of the function
- The arguments of the function, if it isn't obvious from its definition

Example:
```python
# RSA python implementation
# Written by A~Z

def encrypt(plaintext: int, e: int, n: int = -1, factors: list = []):
    '''
    Encrypt RSA: ciphertext ≡ plaintext^e [n]

    Output: ciphertext

    Arguments (either of below):
      • plaintext, public exponent e, modulus n
      • plaintext, public exponent e, factors (p and q for classic RSA)
    '''
    # put code here
    ...
```

### Explanations
The author and contributors (note that contributors of an explanation may differ from contributors of related scripts) of an explanation are to be mentioned in said explanation ─ if they so wish.
For instance, add `> Written by [<Contributor 1>](github link), [<Contributor 2>](github link)` below the explanation's title.

An explanation must (as its name implies) explain the behavior of a script and/or the principles of the script.
If a script implements several principles, an explanation is required for each of them.

The main explanation's name should be `README.md`.

Example:
```md
# RSA
> Written by [A~Z](https://github.com/AZ-0)

## Principle
[Source](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
### Key Generation
...
### Encryption
...
### Decryption
...
### Multiprime RSA
...

## Implementation Details

### [Python](rsa.py)
- Encryption
- Decryption
- Multiprime RSA support
- Step computations (e.g computing d or φ(n))
- Message encoding/decoding
```

### Commits
Every format is accepted granted it is readable and clear, but [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) are preferred.

### Pull Requests
A pull request may only refer to one script (possibly several of its implementation and its explanation). The only exception to this is the restructuration of a topic or subtopic.

A pull request's name must follow this format: `<action> topic/.../<script name> <languages>: <content>`
- `<action>` is the type of the action: `Add`, `Remove`, `Clean`, `Restructure`
- `<script name>` is the name of the script (I mean obviously)
- `<languages>` are the concerned language
- `<content>` is a brief description of the requested change

Examples:
- `Add crypto/asymmetric/rsa python & cpp: implementation`
- `Add crypto/asymmetric/rsa python: multiprime rsa support`
- `Restructure crypto: comply with guidelines`


## Process
1. Fork it!
1. Clone it!
1. Create a new branch pertaining to your desired changes (e.g: rsa-python-implem).
1. Make your changes, following the above contribution rules.
1. Propose it through a pull-request ─ again, make sure it complies with the guidelines. ;)
1. Wait for a review.
1. If any change are required, either argue or comply, but eventually go back to the previous step anyway.
1. Everything is fine, your request should be merged into the main branch!.
