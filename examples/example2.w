x = 11;

// Code for primality checking

a = 2;
is_prime = 1;
while (a * a <= x and is_prime != 0) {
    if (x % a == 0) {
        is_prime = 0;
    }
    a = a + 1;
}

if (is_prime == 1) {
    print x;
}

x = 9;

// Code for primality checking

a = 2;
is_prime = 1;
while (a * a <= x and is_prime != 0) {
    if (x % a == 0) {
        is_prime = 0;
    }
    a = a + 1;
}

if (is_prime == 1) {
    print x;
}