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