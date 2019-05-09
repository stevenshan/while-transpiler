n = 6;
k = 4;
numerator = 1;
denominator = 1; 

n_minus_k = n - k;

while (n_minus_k > 0) {
    denominator = n_minus_k * denominator;
    
    n_minus_k = n_minus_k - 1;
} // should calculate the denominator of n permute k 


while (n > 0) {
    numerator = n * numerator;
    
    n = n - 1;
} // should calculate the numerator of n permute k 

permute = numerator/denominator;

print(permute); // should print n permute k