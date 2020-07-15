raw=dlmread("summary.txt","\t,");
COL_ID        =1;
COL_FRAMENUM  =2;
COL_START      =3;
COL_STOP     =4;
COL_DIRECTION   =5;
COL_WIDTH      =6;
COL_POSITION    =7;

MAX_PASS= 2000.0;

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
save traffic-summary.csv traffic