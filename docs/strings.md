## Strings

Strings in CartLang are pretty simple. They are declared as follows:
```Odin
foo : string = "hello";
```
and can be multiline too!

```Odin
foo : string = "hello
    world this 
    is 
    a multiline 
    CartLang 
    string!";
```

### Strings in CartLang are also compatible with `-` and `+` operators:  
Addition simply combines the two strings:  

```Odin
foo : string = "h" + "ello";
// creates "hello"

// or you can do:
foo : string = "h";
foo += "ello";
```
Subtraction removes the item from the second string from the first string if it is at the start or end:  

```Odin
foo : string = "hello" - "ello";
// creates "h"

// or you can do:
foo : string = "hello";
foo -= "ello";

// this will fail though:
foo : string = "hello" - "s";
// as foo does not contain string "s"
```
String functions and operations can also be accessed by calling the `string` class like so:

```Odin
foo : int = 99;
string.to_string(foo);
// converts int to string
```
