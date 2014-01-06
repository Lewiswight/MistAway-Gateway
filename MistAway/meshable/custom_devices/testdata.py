def onecomp(number):
    number = int(number)
    
    string = bin(number)
    
    
    string = string.split("b")
    
    string = string[1]
    newstr = "0b"
    for i in string:
        print i 
        if i == "0":
            newstr += "1"
        if i == "1":
            newstr += "0"
            
    return int(newstr, 2)

print onecomp(35779)
#29756