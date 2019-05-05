x = 0;
y = 15;

// print even numbers between x and y inclusive

if (x <= y) {
    a = x;
    while (a <= y) {
        if (a % 2 == 0) {
            print a;
        }
        a = a + 1;
    }
}

// print odd numbers between x and y inclusive

if (x <= y) {
    b = x;
    while (b <= y) {
        if (b % 2 == 1) {
            print b;
        }
        b = b + 1;
    }
}