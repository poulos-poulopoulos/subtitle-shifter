# subtitle shifter

Subtitle shifter is a simple command line Python program that allows the user to shift (backward or forward) all the subtitles inside a .srt or .vtt file by a specified time interval.

## operation description

While the program runs the following steps are repeatedly executed.

- A `file name: ` prompt appears. The user gives the input file's path/name. If nothing is given the program exits.
- A `new name: ` prompt appears. The user gives the output file's path/name without the file extension. If the given string starts with `*`, the previous path/name is used appended with what follows `*`. Giving just `*` means modifying the input file. Giving nothing is equivalent to giving `*-`.
- A `time interval: ` prompt appears. The user gives the time interval by which all subtitles will be shifted. It starts with `-` or `+`, indicating shifting backward or forward, respectively. Then follows its value given in hours, minutes, seconds and milliseconds, separated by `,`. If some of these sub-values are empty, they are assumed to be 0. If less than 4 sub-values are given, an appropriate amount of initial sub-values all of which are 0 is used.
- The conversion takes place, producing the specified results.

When executing the program a `-rw` option is available, which affects how the case of same input and output file is treated. If this option is absent, the file's contents will be copied to RAM memory and then new data will be written to the file. If the option is present, the file will be modified "in place".

## example run

```
>python subtitle_shifter.py -rw
file name: C:\A\B\a.srt
new name: *_shifted
time interval: -1,30,,

file name: ..\a.vtt
new name: *
time interval: +1,,500

file name: a.vtt
new name: b
time interval: -250

file name: a.srt
new name:
time interval: +2,

file name:

>
```
