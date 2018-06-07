#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[]){
    if (argc!=2){
        printf("YOU HAVE TO ENTER THE KEY!!\n");
        return 1;
    }
    
    string input=GetString();
    int k=atoi(argv[1]);
    k=k%26;
    
    char temp;
    int dif;
    for (int i=0, n=strlen(input);i<n;i++){
        if (!isalpha(input[i])){
            printf("%c",input[i]);
        }
        else{
            temp=input[i];
            if (temp>='A'&& temp<='Z'){
                if(k>('Z'-temp)){
                    dif=k-('Z'-temp);
                    temp='A'+dif-1;
                }
                else temp+=k;
            }
            else{
                if(k>('z'-temp)){
                    dif=k-('z'-temp);
                    temp='a'+dif-1;
                }
                else temp+=k;
            }
            printf("%c",temp);
        }
    }
    
    printf("\n");
    
    return 0;
}