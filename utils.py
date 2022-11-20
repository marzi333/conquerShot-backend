def get_neigh_dist(center):
    """
    center: (x,y) coordinate
    """
    neighbors = []
    x, y = center
    for i in range(-2,3):
        for j in range(-2,3):
            neighbors.append((x + i,y + j,max(abs(i),abs(j))))

    return neighbors

def get_neigh_dist_without_corners(center):
    neighbors = []
    x, y = center
    for i in range(-2,3):
        for j in range(-2,3):
            if (i == j == 2) or (i == j == -2) or (i == 2 and j == -2) or (i == -2 and j == 2):
                continue
            else:
                neighbors.append((x + i,y + j,max(abs(i),abs(j))))
    return neighbors