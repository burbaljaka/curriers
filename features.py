from typing import List


def make_polygon_from_list(list_of_coords: List[List[float]]):
    list_of_str_coords = [" ".join(map(str, coord_pair)) for coord_pair in list_of_coords]
    str_coords = ", ".join(list_of_str_coords)
    res = f"POLYGON(({str_coords}))"
    return res
