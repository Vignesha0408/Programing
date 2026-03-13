//to find max sum of given arr of len n=  3 (subarray) 
let a =[1,2,3,4,1,2,9]
var max=0
for(let i=0;i<a.length-2;i++)
            if(a[i]+a[i+1]+a[i+2] > max)
                max=a[i]+a[i+1]+a[i+2]
console.log(max)