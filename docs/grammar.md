
### Grammar Definitions

```
program                := <functions> | <global variable declarations>
function               := <statements>
statement              := return <expr> 
                        | assignment <expr> 
                        | declaration 
                        | declaration_assignment <expr>
return                 := <expr>
assignment             := <expr>
declaration            := TYPE IDENTIFIER
declaration_assignment := TYPE IDENTIFIER = <expr>
expr                   := term 
                        | expr + term 
                        | expr - term
term                   := value 
                        | term * value 
                        | term / value
value                  := (expr) 
                        | CONSTANT 
                        | ID 
                        | - value
```
