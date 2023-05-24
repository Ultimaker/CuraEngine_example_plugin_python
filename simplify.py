from pathlib import Path

from svgpathtools import svg2paths

from CuraEngineGRPC.cura.plugins.v0.polygons_pb2 import Polygon, Polygons, Point2D, FilledPath

def extract_points_from_svg(svg_content):
    paths, attributes = svg2paths(svg_content)

    points_collection = []
    for path in paths:
        points = []
        for segment in path:
            points.append((int(segment.start.real * 1000), int(segment.start.imag * 1000)))
        points_collection.append(points)

    return points_collection

def create_filled_path(points):
    filled_path = FilledPath()
    for point in points:
        point2d = Point2D()
        point2d.x = point[0]
        point2d.y = point[1]
        filled_path.path.append(point2d)
    return filled_path

def create_polygon_outline(points):
    polygon = Polygon()
    filled_path = create_filled_path(points)
    polygon.outline.CopyFrom(filled_path)
    return polygon

def create_polygons(outline_points):
    polygons = Polygons()
    for poly in outline_points:
        polygons.polygons.append(create_polygon_outline(poly))
    return polygons

def simplify(received_points):
    points = extract_points_from_svg(Path(__file__).parent.joinpath("UltiMaker.svg"))
    return create_polygons(points)
