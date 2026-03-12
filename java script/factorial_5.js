//to display nth fibb  num use recur
//0 1 1 2 3 5 8
function fibon(n)
{
    if(n==0)
        return 0
    else if(n==1)
        return 1
    else 
        return fibon(n-2)+fibon(n-1);
}


    console.log(fibon(5))