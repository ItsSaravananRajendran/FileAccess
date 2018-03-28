#include &lt;stdio.h&gt;
#include &lt;string.h&gt;

int main(void)
{
    char buff[15asdf saf 
    int pass = 0;

    printf(&#34;
 Enter the password : 
&#34;);
    gets(buff);

    if(strcmp(buff, &#34;thegeekstuff&#34;))
    {
        printf (&#34;
 Wrong Password 
&#34;);
    }
    else
    {
        printf (&#34;
 Correct Password 
&#34;);
        pass = 1;
    }

    if(pass)
    {
       /* Now Give root or admin rights to user*/
        printf (&#34;
 Root privileges given to the user 
&#34;);
    }

    return 0;
}
