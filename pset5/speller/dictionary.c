/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <stdio.h>
#include <ctype.h>
#include <string.h>

node *root;

unsigned int dictSize=0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    
    //set up tracker
    node *tracker=root;
    
    int charIndex;
    
    //loop every character in the word
    for (int i=0;i<strlen(word);i++){
        charIndex=getCharIndex(word[i]);
        //if this character of word is NULL in dictionary (word doesnt exist)
        if (tracker->children[charIndex]==NULL){
            return false;
        }
        //update tracker
        tracker=tracker->children[charIndex];
    }
    return tracker->isWord;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    //assign root memory
    root=malloc(sizeof(node));
    
    //open dictionary
    FILE *dict=fopen(dictionary, "r");
    if (dict==NULL){
        printf("Could not open %s.\n", dictionary);
        return false;
    }
    
    //set up for loop
    node *tracker=root;
    int c=fgetc(dict);
    
    //loop to load words
    while(c!=EOF){
        
        //end of word
        if (c=='\n'){
            tracker->isWord=true;
            //increment dictSize
            dictSize++;
            //go back to start of tree
            tracker=root;
        }
        
        else{
            //get character index for children array
            int charIndex=getCharIndex(c);
            
            //if the character is not in the array yet
            if (tracker->children[charIndex]==NULL){
                //create node
                tracker->children[charIndex]=malloc(sizeof(node));
            }
            
            //move the tracker to next node
            tracker=tracker->children[charIndex];
        }
        
        //move onto next character
        c=fgetc(dict);
    }
    
    fclose(dict);
    
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return dictSize;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    node *tracker=root;
    return freeTries(tracker);
}

//new function to pass in argument for recursion
bool freeTries(node *tracker){
    
    //to run through children array
    for (int i=0;i<27;i++){
        //run freeTries on children that are not null
        if (tracker->children[i]!=NULL){
            freeTries(tracker->children[i]);
        }
    }
    free (tracker);
    return true;
}

//CHECKED
int getCharIndex(char c){
    if (c=='\''){
        return 26;
    }
    else{
        return tolower(c)-'a';
    }
}
