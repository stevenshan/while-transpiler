// Two ways for printing the absolute value of a number

x = -42;
if (x < 0) {
    x = -x;
}

print x; // should be 42

x = -1999;
y = 0;
if (x > 0) {
    y = x;
}
while (x < 0) {
    x = x + 1;
    y = y + 1;
}

print(y); // should be 1999

