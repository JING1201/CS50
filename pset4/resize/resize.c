/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4 ||!isdigit(argv[1][0]))
    {
        fprintf(stderr, "Usage: ./copy factor infile outfile\n");
        return 1;
    }
    
    // record factor
    int factor=argv[1][0]-'0';
    
    if (factor<1 || factor>100){
        fprintf(stderr, "Factor must be an integer from 1 to 100, inclusive");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    BITMAPFILEHEADER bfLarge;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfLarge=bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    BITMAPINFOHEADER biLarge;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biLarge=bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    biLarge.biWidth=bi.biWidth*factor;
    biLarge.biHeight=bi.biHeight*factor;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingLarge = (4 - (biLarge.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    //new size
    biLarge.biSizeImage=((sizeof(RGBTRIPLE)*biLarge.biWidth)+paddingLarge)* abs(biLarge.biHeight);
    bfLarge.bfSize=biLarge.biSizeImage+sizeof(BITMAPFILEHEADER)+sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bfLarge, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biLarge, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int k=0;k<factor-1;k++){
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                
                for (int y = 0; y < factor; y++){
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
                
            }
            
            // then add padding to outfile
            for (int y = 0; y < paddingLarge; y++)
            {
                fputc(0x00, outptr);
            }
            
            long offset=bi.biWidth * sizeof(RGBTRIPLE);
            
            fseek(inptr, -offset, SEEK_CUR);
        }
        
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                
            for (int y = 0; y < factor; y++){
                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
                
        }
        
        // then add padding to outfile
        for (int y = 0; y < paddingLarge; y++)
        {
            fputc(0x00, outptr);
        }
        
        // skip over padding of infile
        fseek(inptr, padding, SEEK_CUR);

        
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
