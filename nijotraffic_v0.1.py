import time

checkpoint = 0
comparevar = "1"
#print(type(comparevar))
a =int(comparevar)
reed1 = open("/sys/class/gpio/gpio2/value", "r");


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

   
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 19:54:24 2018

@author: Loka
"""
from guizero import App, Box, Text, TextBox, PushButton


t1 = cp2time
t2 = cp3time
t3 = cp4time

def do_kecepatan():
    t1 = int(t1_box.value)
    s1 = int(s1_box.value)
    
    t2 = int(t2_box.value)
    s2 = int(s2_box.value)
    
    t3 = int(t3_box.value)
    s3 = int(s3_box.value)
    
    
    v1 = s1/t1;
    v2 = s2/t2;
    v3 = s3/t3;
    
    v1_text.value = " v1 : "+ str(round(v1,5))
    v2_text.value = " v2 : "+ str(round(v2,5))
    v3_text.value = " v3 : "+ str(round(v3,5))
    
    print("pressed")
    
def do_percepatan():
    dv1 = int(dv1_box.value)
    dt1 = int(dt1_box.value)
    
    dv2 = int(dv2_box.value)
    dt2 = int(dt2_box.value)
    
    dv3 = int(dv3_box.value)
    dt3 = int(dt3_box.value)
    
    
    a1 = dv1/dt1;
    a2 = dv2/dt2;
    a3 = dv3/dt3;
    
    a1_text.value = " a1 : "+ str(round(a1,5))
    a2_text.value = " a2 : "+ str(round(a2,5))
    a3_text.value = " a3 : "+ str(round(a3,5))
    
    print("pressed")
def do_gaya():
    m1 = int(m1_box.value)
    a1 = int(a1_box.value)
    
    
    a2 = int(a2_box.value)
    a3 = int(a3_box.value)
    
    
    f1 = m1*a1;
    f2 = m1*a2;
    f3 = m1*a3;
    
    f1_text.value = " F1 : "+ str(round(f1,5))
    f2_text.value = " F2 : "+ str(round(f2,5))
    f3_text.value = " F3 : "+ str(round(f3,5))
    print("pressed")
    
    
    
app = App(title="Program Speed Tracker", width=350,height=730, layout="auto")
text = Text(app, text="________________________________________")
text = Text(app, text="TABEL WAKTU")
text = Text(app, text="---------------------")
box1 = Box(app, layout="grid")

text = Text(box1, text="No", grid=[0,0])
text = Text(box1, text="t (sec)", grid=[1,0])
#text = Text(box1, text="s (cm)", grid=[2,0])
text = Text(box1, text="------",grid=[0,1])
text = Text(box1, text="------",grid=[1,1])
#text = Text(box1, text="------",grid=[2,1])
text = Text(box1, text="1", grid=[0,2])
text = Text(box1, text=t1, grid=[1,2])
#text = Text(box1, text=s1, grid=[2,2])

text = Text(box1, text="2", grid=[0,3])
text = Text(box1, text=t2, grid=[1,3])
#text = Text(box1, text=s2, grid=[2,3])

text = Text(box1, text="3", grid=[0,4])
text = Text(box1, text=t3, grid=[1,4])
#text = Text(box1, text=s3, grid=[2,4])


text = Text(app, text="________________________________________")

text = Text(app, text="KECEPATAN")
boxkecepatan = Box(app,layout="grid", align = "left")

text = Text(boxkecepatan, text="t1(s) :", grid=[0,0])
t1_box = TextBox(boxkecepatan, text=t1, grid = [1,0])
text = Text(boxkecepatan, text="s1(m) :", grid=[2,0])
s1_box = TextBox(boxkecepatan, grid = [3,0])
v1_text = Text(boxkecepatan, text=" v1(m/sec) :", grid=[4,0])

text = Text(boxkecepatan, text="t2(s) :", grid=[0,1])
t2_box = TextBox(boxkecepatan, text=t2, grid = [1,1])
text = Text(boxkecepatan, text="s2(m) :", grid=[2,1])
s2_box = TextBox(boxkecepatan, grid = [3,1])
v2_text = Text(boxkecepatan, text=" v2(m/sec) :", grid=[4,1])

text = Text(boxkecepatan, text="t3(s) :", grid=[0,2])
t3_box = TextBox(boxkecepatan, text=t3, grid = [1,2])
text = Text(boxkecepatan, text="s3(m) :", grid=[2,2])
s3_box = TextBox(boxkecepatan, grid = [3,2])
v3_text = Text(boxkecepatan, text=" v1(m/sec) :", grid=[4,2])





button = PushButton(app,text="Hitung Kecepatan", command=do_kecepatan)

text = Text(app, text="________________________________________")

text = Text(app, text="PERCEPATAN")


boxpercepatan = Box(app,layout="grid")

text = Text(boxpercepatan, text="\u0394v1(m/s) :", grid=[0,0])
dv1_box = TextBox(boxpercepatan, grid = [1,0])
text = Text(boxpercepatan, text="\u0394t1(s) :", grid=[2,0])
dt1_box = TextBox(boxpercepatan, grid = [3,0])
a1_text = Text(boxpercepatan, text=" a1(m/s2) :", grid=[4,0])

text = Text(boxpercepatan, text="\u0394v2(m/s) :", grid=[0,1])
dv2_box = TextBox(boxpercepatan, grid = [1,1])
text = Text(boxpercepatan, text="\u0394t2(s) :", grid=[2,1])
dt2_box = TextBox(boxpercepatan, grid = [3,1])
a2_text = Text(boxpercepatan, text=" a2(m/s2) :", grid=[4,1])

text = Text(boxpercepatan, text="\u0394v3(m/s) :", grid=[0,2])
dv3_box = TextBox(boxpercepatan, grid = [1,2])
text = Text(boxpercepatan, text="\u0394t3(s) :", grid=[2,2])
dt3_box = TextBox(boxpercepatan, grid = [3,2])
a3_text = Text(boxpercepatan, text=" a3(m/s2) :", grid=[4,2])

button = PushButton(app,text="Hitung Percepatan", command=do_percepatan)

text = Text(app, text="________________________________________")

text = Text(app, text="GAYA")
boxgaya = Box(app,layout="grid")

text = Text(boxgaya, text="m(kg) :", grid=[0,0])
m1_box = TextBox(boxgaya, grid = [1,0])
text = Text(boxgaya, text="a1(m/s2) :", grid=[2,0])
a1_box = TextBox(boxgaya, grid = [3,0])
f1_text = Text(boxgaya, text=" F1(N) :", grid=[4,0])

text = Text(boxgaya, text="a2(m/s2) :", grid=[2,1])
a2_box = TextBox(boxgaya, grid = [3,1])
f2_text = Text(boxgaya, text=" F2(N) :", grid=[4,1])


text = Text(boxgaya, text="a3(m/s2) :", grid=[2,2])
a3_box = TextBox(boxgaya, grid = [3,2])
f3_text = Text(boxgaya, text=" F3(N) :", grid=[4,2])

button = PushButton(app,text="Hitung Gaya", command=do_gaya)


app.display()


