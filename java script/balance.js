function balanced(str)
{
        console.log()
        let stack= []

        for(let i=0;i<str.length;i++)
           if(str[i]=="(")
              stack.push("(");
        
           else if(str[i]==")")
               {
                   if(stack.length==0)
                   return false;
                   stack.pop();

               }
    
 return stack.length==0;

}
console.log(balanced("()(())("))