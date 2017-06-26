# 1.	Summary of Algorithm

> Clustering algorithm classifies input data which doesn’t have classification label.  Initially, all objects in a given data set D are marked as “unvisited.” DBSCAN randomly selects an unvisited object p, marks p as “visited,” and checks whether the ε-neighborhood of p contains at least MinPts objects. If not, p is marked as a noise point. To find the next cluster, DBSCAN randomly selects an unvisited object from the remaining ones. The clustering process continues until all objects are visited. 

