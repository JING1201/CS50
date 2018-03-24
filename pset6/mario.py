
while True:
    height = int(input("Height: "))
    if height>0 and height<23:
        break
    
for i in range (1, height+1):
    for j in range (height+1-i):
        print(" ", end="")
    for k in range (i):
        print("#", end="")
    print("  ",end="")
    for k in range (i):
        print("#", end="")
    print()


    