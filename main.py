import random

from cluster import Cluster, calc_dist_squared
from point import Point


def translate_and_categorize(file_path):
    f = open(file_path)
    labels_dict = dict()
    dataset = list()
    number = 1
    for i in f:
        tmp_data_row, tmp_label = i.split(',')[:-1], i.split(',')[-1].strip()
        if tmp_label not in labels_dict.keys():
            labels_dict[tmp_label] = float(number)
            number += 1
        tmp_data_row = [float(j) for j in tmp_data_row]
        tmp_data_row.append(float(labels_dict[tmp_label]))
        dataset.append(Point(tmp_data_row))

    f.close()
    return labels_dict, dataset


def min_distance(clusters_data):
    min_dist = float('inf')
    result = clusters_data[0]
    for data in clusters_data:
        if data[0] < min_dist:
            result = data
            min_dist = data[0]

    return result[1]


def process_k_means(clusters, data_points, labels):
    go = True
    memory = None
    counter = 0
    while go:
        counter += 1
        memory_tmp = []
        if memory is not None:
            go = False
            for cluster in clusters:
                if cluster.cluster_points not in memory:
                    go = True
                    break
        if go:
            for cluster in clusters:
                cluster.calculate_centroid()
                print('total points:', len(cluster.cluster_points))
                print(cluster.centroid)
                cluster.print_distances_sum()
                cluster.print_purity(labels)
                print('-------------------------------------------------------------')

                memory_tmp.append(cluster.cluster_points)
                cluster.cluster_points = []

            for point in data_points:
                clusters_data = []
                for cluster in clusters:
                    distance = calc_dist_squared(point.coords, cluster.centroid)
                    cluster_data_tmp = [distance, cluster.id]
                    clusters_data.append(cluster_data_tmp)
                min_distance_cluster_id = min_distance(clusters_data)
                clusters[min_distance_cluster_id].cluster_points.append(point)

            memory = memory_tmp
        else:
            print('---------------------finished--------------------------------')
            for cluster in clusters:
                cluster.print_distances_sum()
                print('total points:', len(cluster.cluster_points))
                cluster.print_purity(labels)
                print('-------------------------------------------------------------')



if __name__ == '__main__':

    k = 3  # input("provide k number: ")
    k = int(k)
    clusters = []
    for i in range(k):
        clusters.append(Cluster(i))

    data_file = 'data/train.txt'

    labels_dict, data_points = translate_and_categorize(data_file)

    # clusters[0].cluster_points.append(data_points[0])
    # clusters[0].cluster_points.append(data_points[1])
    # clusters[0].cluster_points.append(data_points[2])
    # clusters[1].cluster_points.append(data_points[3])
    # clusters[1].cluster_points.append(data_points[4])
    random.seed(1)
    for point in data_points:
        random_cluster_index = random.randint(0, k - 1)
        clusters[random_cluster_index].cluster_points.append(point)

    process_k_means(clusters, data_points, labels_dict)
