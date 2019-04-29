// Euclidean method for finding GCD
// Prints the GCD of x and y.

///////////////////////////////////////////////////////////
// Test Case 1
///////////////////////////////////////////////////////////

x = 3;
y = 3;

while (x != 0) {
    temp = x;
    x = y % x;
    y = temp;
}

print(y); // should be 3

///////////////////////////////////////////////////////////
// Test Case 2
///////////////////////////////////////////////////////////

x = 3; y = 7;
while (x != 0) {
    temp = x;
    x = y % x;
    y = temp;
}

print(y); // should be 1

///////////////////////////////////////////////////////////
// Test Case 3
///////////////////////////////////////////////////////////

x = 8; y = 12;
loop_condition = 1;
if (x != 0) {
    while (loop_condition == 1) {
        temp = x;
        x = y % x;
        y = temp;

        if (x == 0) {
            loop_condition = 0;
        }
    }
}

print(y); // should be 4

///////////////////////////////////////////////////////////
// Test Case 4
///////////////////////////////////////////////////////////

x = 213; y = 2;
loop_condition = 1776;
if (x == 0) {
    loop_condition = 42;
}
while (loop_condition != 42) {
    temp = x;
    x = y % x;
    y = temp;

    if (x == 0) {
        loop_condition = 42;
    }
}

print(y); // should be 1

///////////////////////////////////////////////////////////
// Test Case 5
///////////////////////////////////////////////////////////

x = 100; y = 15;
loop_condition = 1776;
if (x == 0 or false) {
    loop_condition = 42;
}
while (loop_condition != 42 and true) {
    temp = x;
    x = y % x;
    y = temp;

    if (x == 0) {
        loop_condition = 42;
    }
}

print(y); // should be 5
