n = 6;
k = 4;
numerator = 1;
denominator = 1; 


while (k > 0) {
    denominator = k * denominator;
    
    k = k - 1;
} 

n_minus_k = 2;

while (n_minus_k > 0) {
    denominator = n_minus_k * denominator;
    
    n_minus_k = n_minus_k - 1;
} // should calculate the denominator of n choose k 


while (n > 0) {
    numerator = n * numerator;
    
    n = n - 1;
} // should calculate the numerator of n choose k 

choose = numerator/denominator;

print(choose); // should print n choose k

x = 1;
y = 5;

x_pow = 1;
y_pow = 1;

n_minus_k = 2;
k = 4;

while ( n_minus_k > 0 or k > 0) {
    if (n_minus_k != 0) {
        x_pow = x * x_pow;
        n_minus_k = n_minus_k - 1;
    }
    
    if (k != 0) {
        y_pow = y * y_pow;
        k = k - 1;
    }
}

// x_pow should be x^(n-k)
// y_pow should be y^k

print(choose * x_pow * y_pow);
