## Getting Started

The syntax for CartLang is heavily inspired by both C and Python. Generally sticking to the rules of those languages won't steer you too wrong.

For instance, comments in CartLang work like C:  

```Odin
// this is a comment!
```
Aside from this, all lines also need a ';':

```Odin
print("hello world");
```
If you want something multiline, simply leave off the ';'!

```Odin
print("hello 
world!");
```

### Interactive Terminal Mode

When running the CartLang interpreter you can run it in _Interactive Terminal Mode_ which can be useful for beginners. Designed to be a simple REPL mode, running it allows you to actively enter commands and see their affect immediately 
(similar to Python's 'Interactive Shell/Session' or NodeJS's REPL mode). There are only two additional commands available in this mode when running it - `clear()` and `quit()`.

When running in _Interactive Terminal Mode_ you can write your commands in as many lines as you like. For instance, `print("yes");` could be written like this:
```Odin
print(
"
yes
"
);
```
and accomplish the same thing.

This is where `clear()` comes into effect, if you make a mistake in your multiline command running `clear()` will simply clear the recent memory of the terminal without forgetting variable values and declared functions, etc.

`quit()` is fairly self explanatory and will simply let you quit once you are finished.

### Datatypes

CartLang only contains the following Datatypes at the moment:

`string`, `int`, `float`

### Variables
Variables in CartLang are declared as follows:
```Odin
foo : int = 0;
```
you will notice that the syntax is first name, type, and then the value.  
If you want to assign an already declared variable, you don't declare the type, like so:
```Odin
foo : int = 0;
foo = 4;
```
Assignment for ints, strings and floats can also be done with the `+=` and `-=` operators.  
```Odin
foo -= 2;
// sets foo to -2 of its current value.

foo += 2;
// sets foo to +2 of its current value.
```
These assignments **NEED** to have spaces between them to work. They will not work if truncated.  

#### All variables in CartLang are _full scope_ - this includes variables created _inside loops_! 

If you want to deallocate a variable after using it (or perhaps you simply want to reassign it with a new type) you can use either the `del` or `delete` statements:

```Odin
foo : int = 0;
del foo;

// both del and delete act the same in CartLang
bar : string = "a";
delete bar;

bar : int = 10;
// now that var 'bar' has been deallocated you can now redeclare it with a new type.
```
