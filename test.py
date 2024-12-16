otpt = []

with open("wordlist.txt") as f:
    words = f.readlines()
    for i in words:
        if(len(i.strip()) == 4):
            otpt.append(i)

with open("wordlist.txt", "w") as f:
    f.writelines(otpt)
