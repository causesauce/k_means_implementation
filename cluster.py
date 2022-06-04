# from main import calc_dist_squared


class Cluster:

    def __init__(self, cluster_id):
        self.id = cluster_id
        self.cluster_points = []
        self.centroid = []

    def calculate_centroid(self):
        self.centroid = []
        cluster_points = self.cluster_points
        if len(cluster_points) < 1:
            return

        sum_every_attr = [
            0 for _ in range(len(cluster_points[0].coords))
        ]

        for point in self.cluster_points:
            point_coords = point.coords
            for index in range(len(point_coords)):
                sum_every_attr[index] += point_coords[index]

        for index in range(len(sum_every_attr)):
            self.centroid.append(
                sum_every_attr[index] / len(cluster_points)
            )
        # print(f'cluster id={self.id}, {self.centroid=}')

    def print_distances_sum(self):

        sum_of_distances = sum(
            calc_dist_squared(point.coords, self.centroid) for point in self.cluster_points
        )

        print(f'cluster id={self.id}, {sum_of_distances=}')

    def print_purity(self, labels):
        labels_counter = dict()
        for label in labels.values():
            labels_counter[label] = 0
        #print(labels_counter)

        for point in self.cluster_points:
            labels_counter[point.label] += 1

        for label in labels.values():
            labels_counter[label] /= len(self.cluster_points) / 100

        final_labels = dict()

        for label in labels:
            intermidiate_label = labels[label]
            final_labels[label] = labels_counter[intermidiate_label]

        print(f'cluster id={self.id} purity:', final_labels)


def calc_dist_squared(vector1, vector2):
    distance = sum(
        (a - b) ** 2 for a, b in zip(vector1, vector2)
    )
    return distance
