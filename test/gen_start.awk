BEGIN { FS = "/" }
!/^\s*$/ { 
    idx = 0
#    for (i = 2; i <= NF; ++i) {
    for (i = 1; i <= NF; ++i) {
        printf("%d%s", idx, i == NF ? "\n" : " ")
#        split($i, a, "/")
#        idx += length(a[1])
        idx += length($i)
    }
}
