def is_inside(point, edges):
    # Checks to see if a point is within a polygon
    xp, yp = point
    count = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1) / (y2 - y1) * (x2 - x1)):
            count += 1
    return count % 2 == 1


def get_edges(area_of_interest):
    # Creates edges based on a list of points
    edges = []
    for i in range(0, len(area_of_interest)):
        if i != len(area_of_interest) - 1:
            edges.append((area_of_interest[i], area_of_interest[i + 1]))
        else:
            edges.append((area_of_interest[i], area_of_interest[0]))
    return edges
