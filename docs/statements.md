## Statements

There are all the classic statements in CartLang, as follows:

### if

if statements work just like C:

```Odin
if (foo > 10) {
    print("foo is > than 10!")
}
// if whatever is in the brackets evaluates 'true' then what is in the {} will be executed.

//for example, this will always run:
if (true) {
    print("yes!")
}
```
In CartLang you can use all the typical operators for comparisons: `==`, `>`, `<`, `>=`, `<=`
And also chain these with `||` and `&&`.

However, CartLang also introduces a new operator, the `circa operator`:  

```Odin
if (foo ~5 10) {
    // within 5 ints of 10
    print("true");
}
```
The circa operator `~` requires an integer after it to specify within what range you expect from the supplied variable and then another integer for what the middle point for the range is. This example best describes what the circa operator can simplify:
```Odin
if (foo <= 15 && foo >= 5) { print("true") }
if (foo ~5 10) { print("true") }
```
Both of the above statements provide the same result, with the circa operator simplifying things slightly.

