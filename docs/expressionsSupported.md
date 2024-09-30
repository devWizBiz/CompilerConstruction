# Supported Expressions in `parser.py`

## 1. **Variable Declarations**

### Global Scope:
- **Syntax**:  
  ```int identifier;```
  - **Example**:  
    ```int a;```

### Function Scope:
- **Syntax**:  
  ```int identifier;```
  - **Example**:  
    ```int x;```

- **Array Declaration**:
  - **Syntax**:  
    ```int identifier[];```
    - **Example**:  
      ```int arr[];```

## 2. **Variable Assignments**

### Supported Types:
- **Integer** (`int`)
- **Floating-point** (`float`)
- **Character** (`char`)
- **String** (in conjunction with `char[]`)

### Assignment without expression:
- **Syntax**:  
  ```identifier = constant;```
  - **Example**:  
    ```a = 5;```

### Assignment with basic arithmetic expressions:
- **Syntax**:  
  ```identifier = expression;```
  - **Example**:  
    ```a = 5 + 3;```  
    ```a = b * 2;```

- **Supported Arithmetic Operators**:
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - Division (`/`)

### Array Assignment:
- **Syntax**:  
  ```identifier[] = string_constant;```
  - **Example**:  
    ```charArray[] = "hello";```

## 3. **Function Declarations**

- **Supported Return Types**:
  - `int`, `void`, `char`, `float`

- **Syntax**:  
  ```type identifier() { ... }```
  - **Example**:  
    ```int main() { ... }```

- **Return Statements**:
  - **Syntax**:  
    ```return constant;```
    - **Example**:  
      ```return 0;```

  - **Return of identifiers** is supported:
    - **Syntax**:  
      ```return identifier;```

## 4. **Control Structures (to be added)**

_Currently, no control structures (if-else, loops, etc.) are explicitly supported by the parser._

## 5. **Error Handling**

### Errors Triggered by the Parser:
- Invalid token after function or variable declaration (`Expected "(", ";", instead received ...`)
- Invalid identifier in a statement (`Expected an IDENTIFIER ...`)
- Unsupported tokens in assignment expressions (`Expected "int", "float", instead received ...`)
- Missing closing braces in function declarations (`Expected closing "}" but not found`)
