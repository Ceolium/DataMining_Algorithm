## Programming Assignment #2
*Decision Tree*
1. Decision Tree Algorithm 

> Classification algorithm trains a classifier model from train data which has both attributes and label. Then it classifies a test data which only contains attributes to each label based on the trained algorithm. The train of decision tree algorithm starts with finding the best attribute. In this case, the best attribute means it draws the best information gain among given attributes. Then it splits the train set into left and right node with respect to the best attribute. 
It repeats this single process ‘recursively’ until some conditions are achieved. One is that there are no data to split and the other is the information gain you get after the split is minus.   

> Run <br>$</code>python dt.py --train dt_train1.txt --test dt_test1.txt --result dt_result1.txt <br> on terminal or command line 
<br> 
[Caution] python should be 2.7    # python3 will cause error




