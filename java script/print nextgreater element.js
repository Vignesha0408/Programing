//next greater element
let arr=[4,5,2,10]
//output=[5,10,10,-1]
let a=[]
let j=-1;
function nextgrater(x)
{
    j++;
    for(let i=j;i<arr.length;i++)
      {  if(arr[i]>x)
        
            return arr[i];
      }
      
    return -1;
    
}

for(let i=0;i<arr.length;i++)
    a[i]=nextgrater(arr[i])
console.log(a)