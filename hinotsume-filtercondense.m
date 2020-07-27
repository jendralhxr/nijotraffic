log1=dlmread("label1.log","\t, ");
log0=dlmread("label0.log","\t, ");

COL_ID        =1;
COL_FRAMENUM  =2;
COL_START      =3;
COL_STOP     =4;
COL_DIRECTION   =5; # right is 0, left is 1
COL_WIDTH      =6;
COL_POSITION    =7;

new0= sortrows(log0, [1 2]);
new1= sortrows(log1, [1 2]);

for i=1:size(new0,1)
  new0(i, COL_WIDTH)= new0(i, COL_STOP) - new0(i, COL_START);
  new0(i, COL_POSITION)= (new0(i, COL_STOP) + new0(i, COL_START)) /2;
endfor

for i=1:size(new1,1)
  new1(i, COL_WIDTH)= new1(i, COL_STOP) - new1(i, COL_START);
  new1(i, COL_POSITION)= (new1(i, COL_STOP) + new1(i, COL_START)) /2;
endfor
  
MAX_PASS= 2000.0;

raw=new1;
clear traffic;
start= 1;
n=1;
for i=2:size(raw,1)
  if (raw(start,COL_ID) != raw(i,COL_ID)) || (raw(start,COL_DIRECTION) != raw(i,COL_DIRECTION)) ||  (( raw(i,COL_FRAMENUM) - raw(start,COL_FRAMENUM)) > MAX_PASS )
    stop= i-1;
    traffic(n,1)= raw(start, COL_ID);
    traffic(n,2)= raw(start, COL_FRAMENUM);
    traffic(n,3)= raw(start, COL_DIRECTION);
    traffic(n,4)= mean(raw(start:stop, COL_WIDTH));
    traffic(n,5)= raw(stop, COL_FRAMENUM) - raw(start, COL_FRAMENUM);
    traffic(n,6)= raw(start, COL_POSITION);
    traffic(n,7)= raw(stop, COL_POSITION);
    start=i;
  n+=1;
  end
endfor

traffic=sortrows(traffic, [2]); # sort from framenum/time of occurence

for n=1:size(traffic,1)
    if traffic(n,3)==1 && traffic(n,7)<traffic(n,6)
        traffic(n,:) = [];
	endif
	if traffic(n,3)==0 && traffic(n,7)>traffic(n,6) 
        traffic(n,:) = [];
	endif
endfor

save traffic1.csv traffic
