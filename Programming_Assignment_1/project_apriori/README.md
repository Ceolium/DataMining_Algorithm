**[Assignment report]**

### Make Sure to use python 2.7 !!!<br>
## Association Rule by Apriori Algorithm<br>

2012023871<br>
경영학과<br>
강민철<br>


### 1. Summary of Algorithm

Apriori algorithm finds frequent item sets by generating confined candidate set. First, the algorithm extract frequent itemsets(L1) with one elements from the given minimum support by scanning the input.txt file. It proceeds to generate candidate set(C2) from L1 and filter L2 set by rejecting itemsets whose support is lower than the minimum support. The finding of each  requires one full scan of the database which can be massively expensive as the occasion demands. 

### 2. Instructions for compiling the source codes

**[Step 1]**: Copy the repository and change directory to ~/project_apriori/<br>
>Copy my gitlab repository by using git clone or download the zip file from the website. [http://hconnect.hanyang.ac.kr/2017_ITE4005_10065/2017_ITE4005_2012023871] <br>
>go the the project_apriori directory by ‘cd’ command. <br>

**[Step 2]**: Print help message about arguments<br>
>type $python apriori.py –h on command line then it returns the help message of Apriori.py. <br>
>-s is for minimum support and you should give the value by percentage (%) <br>
>-i is for input file name. The input file must be in the _same directory_.<br>
>-o is for the output file name.  <br>

**[Step 3]**: Actually run the code by python **2.7**<br>
><pre><code>$python apriori.py –s 12 -i input.txt –o output.txt</code></pre> on terminal or command line<br>
>Then you will see the “output.txt’’ file has been made in the same directory. 









