---
layout: default
title: Print glyph names
---

Print the names of selected glyphs in different formats.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/glyphs/namesPrint.png)
</div>

<div class='col' markdown='1'>
mode
: choose one of the available output modes

print
: print the names of the selected glyphs to the Output Window

sort names
: sort the glyph names alphabetically
</div>

</div>

### plain string

```
A B C D a b c d zero one two three
```

### plain list

```
A
B
C
D
a
b
c
d
zero
one
two
three
```

### Python string

```
A B C D a b c d zero one two three
```

### Python list

```
["A", "B", "C", "D", "a", "b", "c", "d", "zero", "one", "two", "three"]
```

- - -

> - add option to print *characters*: `A B C D a b c d 0 1 2 3`
{: .todo }
