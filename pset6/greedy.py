print("O hai! ", end="")
while True:
    change=float(input("How much change is owed?\n"))
    if change>0 :
        break

temp=int(change*100)
minCoin=0
while temp>0:
    if temp>=25:
        temp-=25
    elif temp>=10:
        temp-=10
    elif temp>=5:
        temp-=5
    elif temp>=1:
        temp-=1;
    minCoin+=1

print(minCoin);