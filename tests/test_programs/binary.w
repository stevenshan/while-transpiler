if (true and true) {
    print 0; // this
} else {
    print 1;
}

if (false and true) {
    print 2;
} else {
    print 3; // this
}

if (true and false) {
    print 4;
} else {
    print 5; // this
}

if (false and false) {
    print 6;
} else {
    print 7; // this
}

if (true or true) {
    print 8; // this
} else {
    print 9;
}

if (false or true) {
    print 10; // this
} else {
    print 11;
}

if (true or false) {
    print 12; // this
} else {
    print 13;
}

if (false or false) {
    print 14;
} else {
    print 15; // this
}

if (1 << 3 > 1 and false) {
    print 16;
} else {
    print 17; // this
}

if (1 << 3 > 1 and true) {
    print 18; // this
} else {
    print 19;
}

if (false or 1 << 3 > 1) {
    print 20; // this
} else {
    print 21;
}
