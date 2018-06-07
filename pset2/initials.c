#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

string getTrueString();
void getInitials(string name);

int main(void){
    string name=GetString();
    getInitials(name);
}

string getTrueString(){
    string n;
    n=GetString();
    
    return n;
}

void getInitials(string name){
    char ans[10]="";
    string temp=name;
    
    ans[0]=toupper(temp[0]);
    int k=1;
    for (int i=0;i<strlen(name);i++){
        if (temp[i]==' '){
            ans[k]=toupper(temp[i+1]);
            k++;
            
        }
    }
    string final=ans;
    printf("%s\n",final);
}