n = 21;

// finds nth Fibonnaci number (1st number is 0, 2nd is 1, and so on)

n1 = 0;
n2 = 1;

if (n == 1) {
	print(0);
}

if (n > 1 and n == 2) {
	print(1);
}

if (n > 2) {
    count = 2; 

    while (count < n) {
    	nth = n1 + n2;
    	//print nth;
    	n1 = n2;
    	n2 = nth;
    	count = count + 1;
    }
    
    print(nth);
}


