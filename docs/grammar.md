# Supported Grammar

This document outlines the supported grammar for tokenization.

## 1. **Keywords**
The following keywords are supported:

- `auto`, `break`, `case`, `char`, `const`, `continue`, `do`, `default`, `else`, `enum`
- `extern`, `float`, `for`, `if`, `inline`, `int`, `long`, `register`, `restrict`, `return`
- `short`, `signed`, `sizeof`, `static`, `switch`, `typedef`, `union`, `unsigned`, `void`
- `volatile`, `while`

## 2. **Punctuators**
Supported punctuators include:

- `[ ]`, `( )`, `{ }`
- `.`, `...`, `->`, `-`, `+=`, `++`, `--`, `&&`, `&=`, `*`, `*=`, `~`, `!`, `!=`, `/`, `/=`, `%`, `%=`
- `<`, `<=`, `:<`, `=`, `==`, `^`, `|`, `||`, `|=`, `?`, `:`, `;`, `,`

## 3. **Identifiers**
Identifiers follow the C-like naming conventions:

- Any sequence of alphanumeric characters or underscores, starting with an alphabet or underscore.

## 4. **Integer Constants**
- Supported integer constants are non-decimal integers.

## 5. **Floating-Point Constants**
- Supported floating-point constants are decimal numbers with at least one digit after the decimal point.

## 6. **String Constants**
- String constants enclosed in double quotes.

## 7. **Character Constants**
- Single characters enclosed in single quotes, excluding escape sequences or newlines.

## 8. **Single-Line Comments**
- Single-line comments starting with `//`.

## 9. **Multiline Comments**
- Multiline comments enclosed in `/*` and `*/`.

## 10. **Whitespace**
- Any sequence of whitespace characters (spaces, tabs, newlines).

## 11. **Unsupported Characters**
- Any character or sequence not supported by the above rules.
