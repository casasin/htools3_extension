---
layout: default
title: Print glyph names
---

Print the names of selected glyphs in different formats.

<div class='container'>

<div class='screenshot'>
  <img src='{{ site.url }}/images/glyphs/namesPrint.png' />
</div>

<div class='captions' markdown='1'>
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
A B C D a b c d one three two zero
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
one
three
two
zero
```

### Python string

```
A B C D a b c d one three two zero
```

### Python list

```
["A", "B", "C", "D", "a", "b", "c", "d", "one", "three", "two", "zero"]
```

- - -

### to-do

- add option to print *characters*
