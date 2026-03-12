let a="malayalam",start=0,end=a.length-1;
let count=true;
while(start<end)
{
    if(a[start]!=a[end])
    {
        count=false;
        break;   
    }
    else
    {
        start++;
        end--; 
    }
}

if(count)
    console.log(true);
else
    console.log(false)