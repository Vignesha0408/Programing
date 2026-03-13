//very easy
// pick k max element and sum it
var arrs=[],i=0
let k = 2;
function subsets(index,str,subset)
{
    if(index==str.length)
    {
        arrs[i++]=subset
        return
    }
    subsets(index+1,str,subset.concat(str[index]))
    subsets(index+1,str,subset)
}

subsets(0,[1,2,3,4,5,6],[])




let max=0,sum=0
for(let i=0;i<arrs.length;i++)
    if(arrs[i].length==k)
    {
        sum=0
        for(let j=0;j<arrs[i].length;j++)
            sum=sum+arrs[i][j]
        if(sum>max)
            max=sum
        
    }
console.log(max)