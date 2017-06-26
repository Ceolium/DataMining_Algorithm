import sys
import math

# Global variable for checking and noise
UNCHECKED = None
NOISE = -1


def FileReader(file_path):
    df = []
    file_iter = open(file_path, 'rU')
    for row in file_iter:
        row = row.strip().rstrip('\t')
        tup = row.split('\t')
        df.append(tup)
    return df


def euclidean_dist(p, q):
    # As we read input file as string, should transform data type to float
    x_1 = float(p[0])
    y_1 = float(p[1])
    x_2 = float(q[0])
    y_2 = float(q[1])

    # Return Euclidean distance of given two points
    return math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))


def is_neighbor(p, q, eps):
    # Return true when the distance 
    # to the target point is within epsilon
    return euclidean_dist(p, q) < eps


def make_family(data, point, eps):
    n_points = len(data)
    family = []
    # Check every other points
    for i in xrange(n_points):
        # Whether they are neighbor or not
        if is_neighbor(data[point][1:], data[i][1:], eps):
            # Add to family if it is neighbor
            family.append(i)
    return family


def diffusion(data, cluster_labels, point, cluster_id, eps, min_points):
    # Make family with given point
    family = make_family(data, point, eps)
    # Family number smaller than minPts
    if len(family) < min_points:
        # Classify as noise
        cluster_labels[point] = NOISE
        return False
    else:
        # Else, classify as current cluster_id
        cluster_labels[point] = cluster_id
        # Classify child as current cluster_id, either
        for id in family:
            cluster_labels[id] = cluster_id
        

        # Expand family with child other than first point

        while len(family) > 0:
            # Pass if current point and original point is same
            current_point = family[0]
            results = make_family(data, current_point, eps)

            if len(results) >= min_points:

                for i in xrange(len(results)):
                    result_point = results[i]
                    if cluster_labels[result_point] == UNCHECKED or cluster_labels[result_point] == NOISE:
                        family.append(result_point)
                        cluster_labels[result_point] = cluster_id

            family = family[1:]


        return True


def dbscan(data, eps, min_points):
    # Designate first cluster id as 0
    cluster_id = 0
    n_points = len(data)
    print "DBSCAN Clustering initializing..."
    # Make cluster labels with same length
    cluster_labels = [UNCHECKED] * n_points
    for point in xrange(n_points):

        if cluster_labels[point] == UNCHECKED:
            if diffusion(data, cluster_labels, point, cluster_id, eps, min_points):

                print "Cluster No.%s classified" % (cluster_id)
                cluster_id = cluster_id + 1

    return cluster_labels


def write_file(labels, f, cluster_id):
    # Loop through each element 
    # and separate with its cluster id

    for i in xrange(len(labels)):
        if labels[i] == cluster_id:
            row = ""
            row += "%s\n" % (i)
            f.write(row)

    return f


if __name__ == "__main__":
    input_name = sys.argv[1]
    n = int(sys.argv[2])
    eps = int(sys.argv[3])
    min_points = int(sys.argv[4])


    # Read input file
    train = FileReader(input_name)

    # Run dbscan algorithm and draw cluster information 
    labels = dbscan(train, eps, min_points)
    # In case the number of cluster is larger than n
    # Modify the extra cluster(with least number of elements) to final one
    for i in xrange(len(labels)):
        if labels[i] > (n - 1):
            labels[i] = (n - 1)
    print "Excessive cluster truncated"
    name = input_name.replace('.txt', '')

    # For each cluster in labels make output file
    for cl_id in xrange(n):
        file_name = name + '_cluster_' + str(cl_id) + '.txt'
        out_file = open(file_name, 'w')
        Result = write_file(labels, out_file, cl_id)
        out_file.close()

    print "Finished"

    