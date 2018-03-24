import sys

if len(sys.argv)!=2:
    print("Usage: ./caesar k")
    exit(1)

k=int(sys.argv[1])%26
words=input("plaintext: ")
original=""

for i in range (len(words)):
    if (not words[i].isalpha()):
        original+=words[i]
    else:
        if (words[i].isupper()):
            temp=ord(words[i])+k
            if temp>90:
                temp=temp-90+65-1
            original+=chr(temp)
        elif (words[i].islower()):
            temp=ord(words[i])+k
            if temp>122:
                temp=temp-122+97-1
            original+=chr(temp)

print("ciphertext: "+original)
