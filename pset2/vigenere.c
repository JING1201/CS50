#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

int getIndex(char k);

int main(int argc, string argv[]){
    if (argc!=2){
        printf("YOU HAVE TO ENTER THE KEY!!\n");
        return 1;
    }
    string key=argv[1];
    for (int i=0;i<strlen(key);i++){
        if (!isalpha(key[i])){
            printf("ENTER A VALID KEY!!\n");
            return 1;
        } 
    }
    string input=GetString();
    
    
    char temp;
    int dif;
    int k;
    int count=0;
    for (int i=0, n=strlen(input);i<n;i++){
        if (!isalpha(input[i])){
            printf("%c",input[i]);
        }
        
        else{
            k=getIndex(key[count]);
            //printf(" %d %c ", k, key[count]);
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
            
            count++;
            if (count>=strlen(key)) count=0;
        }
        
    }
    
    printf("\n");
    
    return 0;
}

int getIndex(char k){
        
    string upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string lower="abcdefghijklmnopqrstuvwxyz";
    if (isupper(k)){
        for (int i=0;i<strlen(upper);i++){
            if (k==upper[i]) return i;
        }
    }
    else{
        for (int i=0;i<strlen(lower);i++){
            if (k==lower[i]) return i;
        }
    }
    return 0;
}

