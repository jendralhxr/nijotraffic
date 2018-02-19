import time

checkpoint = 0
comparevar = "1"
#print(type(comparevar))
a =int(comparevar)
reed1 = open("/sys/class/gpio/gpio2/value", "r");
#if a == b:
 #   print("yatuhantu")

print('0' in reed1.read())

while True:
    while checkpoint == 0:
        reed1 = open("/sys/class/gpio/gpio2/value", "r");
       # print("sensor 1 : ",reed1.read())  
        checker = '0' in reed1.read()
       # print(checker)
        if checker:
            checkpoint=1
        del checker
        reed1.close   
    print("checkpoint1")

    start = time.time()

    while checkpoint == 1:
        reed2 = open("/sys/class/gpio/gpio3/value", "r");
#        print("sensor 2 : ",reed2.read())
        checker = '0' in reed2.read()
        if checker:
            checkpoint = 2
        del checker
        reed2.close()
        
    print("checkpoint2")
    cp2start = time.time()
    cp2time = cp2start - start
    print("check point 2 time : ",cp2time)
    while checkpoint ==2:    
        reed3 = open("/sys/class/gpio/gpio17/value", "r");
      #  print("sensor 3 : ",reed3.read())
        checker = '0' in reed3.read()
        if checker:
            checkpoint = 3
        del checker
        reed3.close()
        
    print("checkpoint3")
    cp3start = time.time()
    cp3time  = cp3start - cp2start
    print("check point 3 time : ",cp3time)
    while checkpoint == 3:    
        reed4 = open("/sys/class/gpio/gpio27/value", "r");
       # print("sensor 4 : ",reed4.read())
        checker = '0' in reed4.read()
        if checker:
            checkpoint = 4
        del checker
        reed4.close()
    cp4start = time.time()
    cp4time  = cp4start - cp3start
    print("check point 4 time : ",cp4time)

    print("finish")
    print("total time : ",cp2time+cp3time+cp4time)
    break

   
