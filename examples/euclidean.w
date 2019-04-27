// Euclidean method for finding GCD
// Prints the GCD of x and y.

x = 18;
y = 81;

while (x != 0) {
    temp = x;
    x = y % x;
    y = temp;
}

print(x);

