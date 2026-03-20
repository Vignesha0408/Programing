function isprime(n)
{
    if(n==0 || n==1)
        return false
    for(let i=2;i<n;i++)
        if(n%i==0)
            return false
        return true
}

for(let i=0;i<=100;i++)
    if(isprime(i))
        console.log(i)