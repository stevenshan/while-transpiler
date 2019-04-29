// Euclidean algorithm for finding GCD
// Prints the GCD of x and y.

x = 21;
y = 49;

while (x != 0) {
    temp = x;
    x = y % x;
    y = temp;
}

print(y); // should be 7
