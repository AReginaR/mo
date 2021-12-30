import random
import sys
import math
import pygame


class Point:
    def __init__(self, x, y, color='red'):
        self.x = x
        self.y = y
        self.color = color


def dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def generate_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def new_points(x, y, points):
    for i in range(5):
        angle = random.uniform(*[0, 2 * math.pi])
        radius = random.randint(*[0, 15])
        points.append(Point(x + math.sin(angle) * radius, y + math.cos(angle) * radius))


def cluster_color(i, cache_colors):
    if i >= len(cache_colors):
        for j in range(len(cache_colors) - i + 1):
            cache_colors.append(generate_color())
    return cache_colors[i]


def dbscan(points):
    greens = []
    yellows = []
    boarded = {}
    cache_colors = []

    cache_points = [*points]

    for point1 in cache_points:
        neighbour_count = 0
        for point2 in points:

            if point1 == point2:
                continue

            if dist(point1, point2) <= 15:
                neighbour_count += 1

        if neighbour_count >= 3:
            point1.color = 'green'
            greens.append(point1)

    for green in greens:
        cache_points.remove(green)

    for point1 in cache_points:
        min_dist = math.inf
        nearest = None

        for point2 in points:

            if point1 == point2:
                continue

            if point2.color == 'green':

                if dist(point1, point2) > 15:
                    continue

                current_dist = dist(point1, point2)
                if current_dist <= min_dist:
                    min_dist = current_dist
                    nearest = point2

        if nearest is not None:
            point1.color = 'yellow'
            yellows.append(point1)
            boarded.setdefault(nearest, []).append(point1)

    for yellow in yellows:
        cache_points.remove(yellow)

    clusters = []
    while len(greens) > 0:
        cluster = [greens.pop(0)]

        for point1 in cluster:
            for point2 in greens:
                if point1 is point2:
                    continue

                if dist(point1, point2) <= 15:
                    if point2 not in cluster:
                        greens.remove(point2)
                        cluster.append(point2)

        yellows_in_cluster = []
        for green in cluster:
            if green in boarded:
                yellows_in_cluster.extend(boarded[green])
        cluster.extend(yellows_in_cluster)
        clusters.append(cluster)

    for cluster_index, cluster in enumerate(clusters):
        rng_color = cluster_color(cluster_index, cache_colors)

        for p in cluster:
            p.color = rng_color


if __name__ == '__main__':

    FPS = 60
    points_list = []
    pygame.init()
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 600))
    is_on = True
    while is_on:
        screen.fill((0, 0, 0))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            is_on = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_on = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                new_points(*pygame.mouse.get_pos(), points_list)
                dbscan(points_list)

        for point in points_list:
            pygame.draw.circle(screen, point.color, (point.x, point.y), 2)

        pygame.display.update()

    pygame.quit()
    sys.exit()
