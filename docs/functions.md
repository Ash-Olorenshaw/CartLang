## Functions

Functions in CartLang are pretty much like C or Python. You can declare one like this:

```Java
func add_one(val : int) {
    return val + 1;
}
```
Each argument for a function requires a declared type like the argument here `val` which is an `int`.

Currently you do not need to specify a return type.

`return` does what you think and returns what is between it and its ';'.

Functions are then called by simply calling their name with their associated arguments:
```Odin
foo : int = add_one(5);
```
