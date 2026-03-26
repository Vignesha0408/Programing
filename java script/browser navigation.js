//use stack,, browser navigate
//a. visit a new page: push
//b. pop top url
//c. current page--return top of stack


var back=[];
var forward=[];
var i=0,j=0;
function visit(a)
{
    i++;
    back[i]=a;
}

function url()
{
    console.log(back[i])
}

function backward()
{
    if (i==0)
    {console.log("empty stack")
    }
    else
    {
    forward[j++]=back[i--];
    }
}



visit("hello.com")
visit("youtube.com")
visit("insta.com")
backward();
url()
