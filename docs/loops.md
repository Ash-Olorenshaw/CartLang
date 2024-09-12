## Loops

### while

`while` loops work similarly to Python:

```Odin
goob : int = 0;

while (goob < 5) {
    goob = goob + 1;
}
```
The code inside the `while` loop will run as long as the statement inside the brackets will evaluate `true`.

Checkout `statements.md` for further info on what operations you can use!

### for

`for` loops also work similarly to Python:

```Odin
for (num in 9) {
    print(num);
}
```

`for` loops can be run with iterables or integers to loop through. If provided with an integer the associated variable will start as 0 and then repeat for the size of the provided integer (the above statement will provide a count from 0 - 8).

CartLang does not currently include arrays or lists, but you can also iterate over strings:
```Odin
for (c in "yes") {
    print(c);
}
```

In addition to this, if you prefer to not use the word `in`, you can also use the operator `->`:

```Python
for (c -> "yes") {
    print(c);
}
```

