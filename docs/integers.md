## Ints

Integers in CartLang are like every other language. Declare them like this:

```Odin
foo : int = 0;
```

A _very_ important thing of note, however, is how mathematics is done with CartLang. CartLang is a very basic interpreter, it does not recognise things ahead in a mathematical statement. For instance:

```Odin
1 + 3 * 4
```
For CartLang, this expression will evaluate to 16 as it first calculates the addition before realising there is a multiplication operator.
This can be circumvented, however, through a simple use of brackets:
```Odin
1 + (3 * 4)
```
The above statement will evaluate to what is more commonly expected from the first statement: `13`. If in doubt, just add brackets!

Integer functions and operations can also be accessed by calling the `int` class like so:

```Odin
foo : string = "12";
int.to_int(foo);
// converts string to int
```
