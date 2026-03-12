let s="racecar",start=0,end=s.length-1

function palin(s)
{
    while(start<end)
    {
        if(s[start]!=s[end])
            return false
        start++;
        end--;
    }
    return true
}
console.log(palin(s))