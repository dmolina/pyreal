use strict;

for my $f (3..25) {
    `rm population*.png 2>/dev/null`;
    `python moviepop.py $f cec2005_f${f}`;
}
