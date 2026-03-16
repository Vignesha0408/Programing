function power(n,m)
{
    if(m==0)
        return 1;
    return n*power(n,m-1);
}

console.log(power(2,5))