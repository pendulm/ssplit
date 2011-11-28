{
    for (i = 2; i <= NF; ++i) {
        split($i, a, "/")
        printf(a[1])
    }
    print ""
}
