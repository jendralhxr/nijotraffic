log0=dlmread("log0.txt","\t, ");
log1=dlmread("log1.txt","\t, ");

# video0 is 82381 frames
# video1 is 82494 frames

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
  
MAX_PASS= 3000.0;

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

# sort from framenum/time of occurence
traffic=sortrows(traffic, [2]); 

do
    # filter the wrong-direction output (opposite-end detection)
    size_prev= size(traffic,1);    
        for n=1:size(traffic,1)-1
            if traffic(n,3)==1 && traffic(n,7)<traffic(n,6)
                traffic(n,:) = [];
            endif
            if traffic(n,3)==0 && traffic(n,7)>traffic(n,6) 
                traffic(n,:) = [];
			if traffic(n,5)<10
                traffic(n,:) = [];	
            endif
        endfor
    size_cur= size(traffic,1);
until (size_cur==size_prev)
    
traffic1=traffic;

#---------

traffic=dlmread("ba.txt","\t");
TIME_CLUSTER= 3 # mins

traffic(:, COL_FRAMENUM) /= 3600; # now in minutes
COL_DIRECTION=3;

#count per direction
clear sum_count;
sum_count(2, ceil(max(traffic(:,COL_FRAMENUM)) / TIME_CLUSTER))=1;
for i=1:size(traffic,1)
	if ( traffic(i, COL_DIRECTION) < 1)
	    sum_count(1, ceil(traffic(i,COL_FRAMENUM)/TIME_CLUSTER) ) += 1;
	else
	    sum_count(2, ceil(traffic(i,COL_FRAMENUM)/TIME_CLUSTER) ) += 1;
	endif
endfor

timestamp= 0:TIME_CLUSTER:max(traffic(:,COL_FRAMENUM));
plot(timestamp, sum_count);