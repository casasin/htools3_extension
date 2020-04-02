---
layout: default
title: Set style data
---

Set data for individual styles in selected fonts.


fonts
-----

Select on which fonts to set data.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchSetData_0.png)
</div>

<div class='col' markdown='1'>
target fonts
: a list of open and/or closed fonts for selection

add all open fonts
: add all open fonts to the list

select all
: select all fonts in the list

add fonts folder
: add a folder with UFOs to the list

clear font lists
: empties the list of fonts
</div>

</div>

style data
----------

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchSetData_1.png)
</div>

<div class='col' markdown='1'>
import style data
: import style data from JSON file

style data
: edit imported style data manually if needed

set data
: set style data in selected fonts

preflight
: simulate the action before applying it
</div>

</div>

data format (example)
---------------------

### style-data.json

```json
{

  "featuresDir"   : "feaFolder",
  "features"      : ["features.fea"],

  "15.ufo": {
    "features"         : ["15.fea"],
    "weight"           : 100,
    "width"            : 5,
    "blue zones"       : [-200, -190, -10, 0, 465, 475, 605, 615, 675, 685],
    "stems vertical"   : [70],
    "stems horizontal" : [60]
  }

}
```
