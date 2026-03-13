function subsets(arr,index,subset){
    if(arr.length==index)
        {
            console.log(subset);
            return
        }
        subsets(arr,index+1,subset.concat(arr[index]));
        subsets(arr,index+1,subset);
}

subsets([1,2,3],0,[])