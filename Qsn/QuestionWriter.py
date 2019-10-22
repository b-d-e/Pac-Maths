from random import randint

### A procedure to return the length of a file / number of lines ###
def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

### Iterates through each file and formats it to be empty ###
f = open("AddQ.txt", "w")
f.close()
f = open("SubQ.txt", "w")
f.close()
f = open("MultQ.txt", "w")
f.close()
f = open("DivQ.txt", "w")
f.close()
f = open("AddA.txt", "w")
f.close()
f = open("SubA.txt", "w")
f.close()
f = open("MultA.txt", "w")
f.close()
f = open("DivA.txt", "w")
f.close()

### main loop ###
go = True
while go:
    if file_len("AddQ.txt") < 101:
        print("Add")
        typenum = 1
    elif file_len("SubQ.txt") < 101:
        print("Sub")
        typenum = 2
    elif file_len("MultQ.txt") < 101:
        print("Mult")
        typenum = 3
    elif file_len("DivQ.txt") < 101:
        print("Div")
        typenum = 4
    else:
        print("All done!")
        typenum = 0 
        go = False
    if typenum == 1:
        qname = "AddQ.txt"
        aname = "AddA.txt"
    elif typenum == 2:
        qname = "SubQ.txt"
        aname = "SubA.txt"
    elif typenum == 3:
        qname = "MultQ.txt"
        aname = "MultA.txt"
    elif typenum == 4:
        qname = "DivQ.txt"
        aname = "DivA.txt"
    else:
        print("Invalid input")
        continue
    num1 = randint(1,100)
    num2 = randint(1, 100)
    if typenum == 1:
        q = (str(num1)+" + "+str(num2))
        a = int(num1) + int(num2)
    elif typenum == 2:
        if num2>num1:
            temp = num2
            num2 = num1
            num1 = temp
        q = (str(num1)+" - "+str(num2))
        a = int(num1) - int(num2)
    elif typenum == 3:
        num1 = randint(1,20)
        num2 = randint(1, 10)
        q = (str(num1)+" x "+str(num2))
        a = int(num1) * int(num2)
    elif typenum == 4:
        num1 = randint(12, 30)
        num2 = randint(2,10)
        if num1 % num2 == 0:
            q = (str(num1)+" ÷ "+str(num2))
            a = int(int(num1) / int(num2))
        else:
            print("Invalid input")
            continue
    f = open(qname, "a")
    f.write(q+"\n")
    f.close()
    f = open(aname, "a")
    f.write(str(a)+"\n")
    f.close()
