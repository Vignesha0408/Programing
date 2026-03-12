//large over small

function hannoi(n,start,end,temp)
{
    if(n==1)
        console.log(start+"->"+end);
    else
    {
    hannoi(n-1,start,temp,end);
    console.log(start+"->"+end);
    hannoi(n-1,temp,end,start);
    }
}
console.log("goal:")
hannoi(5," start "," end   "," temp  ")