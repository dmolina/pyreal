use strict;
my @fun = (1..6, 8..25);

for my $fun (@fun) {
    `rm population*.png 2>/dev/null`;
    my $fname = "cec2005_f${fun}";
    print "Function: $fun\n";
    `python moviepop.py $fun $fname` unless (-f "${fname}.avi");
}
