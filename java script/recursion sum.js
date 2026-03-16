function sum(arr,i=0)
{
    if(arr.length==i)
        return 0
    return arr[i]+sum(arr,i+1)
}

console.log(sum([1,2,3,4]))