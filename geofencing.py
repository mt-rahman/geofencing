from haversine import (
    Unit,
    Direction,
    haversine,
    inverse_haversine,
)
from shapely import (
    Point,
    Polygon,
    LineString,
    buffer,
)

def is_within_circle(
    obj1_lat:float,
    obj1_lon:float,
    obj2_lat:float,
    obj2_lon:float,
    radius_km:float,
) -> bool:
    """Creates a circular geofence around an object
    and checks whether the other object is within the geofence.

    Args:
        obj1_lat (float): latitude of object 1
        obj1_lon (float): longitude of object 1
        obj2_lat (float): latitude of object 2
        obj2_lon (float): longitude of object 2
        radius_km (float): radius of geofence circle in km

    Returns:
        bool: True if object is located within the circular geofence
    """

    return haversine((obj1_lat, obj1_lon), (obj2_lat, obj2_lon), Unit.KILOMETERS) <= radius_km

def is_within_rectangle(
    obj_lat:float,
    obj_lon:float,
    poi_lat:float=None,
    poi_lon:float=None,
    rectangle_height_km:float=None,
    rectangle_width_km:float=None,
    north_boundary:float=None,
    south_boundary:float=None,
    west_boundary:float=None,
    east_boundary:float=None,
) -> bool:
    """Creates a rectangular geofence and checks whether the object is within the geofence.

    Args:
        obj_lat (float): latitude of object
        obj_lon (float): longitude of object
        poi_lat (float, optional): latitude of point of interest
        poi_lon (float, optional): longitude of point of interest
        rectangle_height_km (float, optional): length of rectangle from north to south in km
        rectangle_width_km (float, optional): length of rectangle from west to east in km
        north_boundary (float, optional): north latitude of rectangle
        south_boundary (float, optional): south latitude of rectangle
        west_boundary (float, optional): west longitude of rectangle
        east_boundary (float, optional): east longitude of rectangle

    Returns:
        bool: True if object is located within the rectangular geofence
    """
    try:
        # rectangular geofence boundaries (latitudes and longitudes)
        north_boundary = inverse_haversine((poi_lat, poi_lon), (rectangle_height_km / 2), Direction.NORTH, Unit.KILOMETERS)[0]
        south_boundary = inverse_haversine((poi_lat, poi_lon), (rectangle_height_km / 2), Direction.SOUTH, Unit.KILOMETERS)[0]
        east_boundary = inverse_haversine((poi_lat, poi_lon), (rectangle_width_km / 2), Direction.EAST, Unit.KILOMETERS)[1]
        west_boundary = inverse_haversine((poi_lat, poi_lon), (rectangle_width_km / 2), Direction.WEST, Unit.KILOMETERS)[1]

    except:
        pass

    try:
        return (south_boundary <= obj_lat <= north_boundary) and (west_boundary <= obj_lon <= east_boundary)

    except:
        print('Exception: Rectangle not specified!')

def is_within_polygon(
    obj_lat:float,
    obj_lon:float,
    polygon_coordinates:list[tuple[float,float]],
) -> bool:
    """Creates a polygonal geofence and checks whether the object is within the geofence.

    Args:
        obj_lat (float): latitude of object
        obj_lon (float): longitude of object
        polygon_coordinates (list[tuple[float,float]]): list of tuples containing coordinates of polygon

    Returns:
        bool: True if object is located within the rectangular geofence
    """

    return Polygon(polygon_coordinates).contains(Point(obj_lat, obj_lon))

def is_within_corridor(
    obj_lat:float,
    obj_lon:float,
    route_coordinates:list[tuple[float,float]],
    geofence_radius:float,
) -> bool:
    """Creates a corridor geofence and checks whether the object is within the geofence.

    Args:
        obj_lat (float): latitude of object
        obj_lon (float): longitude of object
        route_coordinates (list[tuple[float,float]]): list of tuples containing coordinates of polyline
        geofence_radius (float): width of the corridor geofence

    Returns:
        bool: True if object is located within the rectangular geofence
    """

    route_geofence = buffer(
        geometry=LineString(route_coordinates),
        distance=geofence_radius,
    )

    return route_geofence.contains(Point(obj_lat, obj_lon))
