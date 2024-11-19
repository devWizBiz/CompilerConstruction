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
        int y;
        k = a * 2;
        if ( k == b )
        {
            int z = 12;
            if ( z != b)
            {
                return a;
            }
            return b;
        }
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