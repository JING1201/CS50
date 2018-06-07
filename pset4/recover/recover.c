#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[]){
    
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    
    if (file == NULL)
    {
        fprintf(stderr, "Could not open file.");
        return 2;
    }
    
    int count=0;
    
    //output file
    FILE *img=NULL;
    
    uint8_t buffer[512];
    
    while (fread(&buffer, 1, 512, file) >= 512){
        if (buffer[0]==0xff &&
            buffer[1]==0xd8 &&
            buffer[2]==0xff &&
            (buffer[3]&0xf0)==0xe0){
                if (img!=NULL){
                    fclose(img);
                }
                char filename[8];
                sprintf(filename,"%03i.jpg",count);
                img=fopen(filename,"w");
                count++;
        }
        if (img!=NULL){
            fwrite(&buffer,512,1,img);
        }
    }
    
    if (img!=NULL){
        fclose(img);
    }
    fclose(file);
    
    return 0;
    
}