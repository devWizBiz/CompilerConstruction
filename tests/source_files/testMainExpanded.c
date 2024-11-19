int foo;

int testReturnIntFunction(){
    return 12;
}

float testReturnFloatFunction(){
    return 3.14;
}

int calculateSumOfInts(){
    int a = 10;
    int b = 2;
    int sum;
    sum = a + b;
    return sum;
}

int calculateDifferenceOfInts(){
    int a = 10;
    int b = 2;
    int difference = a - b * 2;
    return difference;
}

int calculateProductOfInts(){
    int a = 10;
    int b = 2;
    int product = a * b;
    return product;
}

int calculateQuotientOfInts(){
    int a = 10;
    int b = 2;
    int quotient = a / b;
    return quotient;
}

float calculateSumOfFloats(){
    float a = 10.1;
    float b = 2.1;
    float sum = a + b;
    return sum;
}

float calculateDifferenceOfFloats(){
    float a = 10.1;
    float b = 2.2;
    float difference = a - b;
    return difference;
}

float calculateProductOfFloats(){
    float a = 10.1;
    float b = 2.1;
    float product = a * b;
    return product;
}

float calculateQuotientOfFloats(){
    float a = 10.1;
    float b = 2.1;
    float quotient = a / b;
    return quotient;
}

int main(){
    int tmp = 12;                   // Integer \n variable
    float t_VarOne = 3.14;           // Float variable
    int a = 2;
    int b = 10;
    int p = 3 + 4 * tmp + (b/a);

    int k;
    k = 1;

    if ( a <= b )
    {
        k = a * 2;
        return k;
    }
    else
    {
        k = b * 2;
        return k + 1;
    }

    /* This is a test block of "code" commented out.
    It expands at least more than one line in this test case. \n
    A multi-line can be only one line as well*/
    return 0;
}