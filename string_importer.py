# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level

from qgis.core import QgsProject, QgsVectorLayer
from re import search
from .geom import Point, Segment

point_pattern = "^(\\d+)\\s*,\\s*(\\d+\\.?\\d*)\\s*,\\s*(\\d+\\.?\\d*)\\s*,\\s*(-?\\d+\\.?\\d*)\\s*,\\s*(.*)\\s*"

def import_str(string_file):
    points = []
    segments = []
    with open(string_file) as sf:
        has_axis_record = False
        for line in sf:
            regex = search(point_pattern, line.strip())
            if regex:
                if has_axis_record:
                    str_id = int(regex.group(1))
                    x = float(regex.group(3))
                    y = float(regex.group(2))
                    z = float(regex.group(4))
                    d = regex.group(5)
                    if str_id > 0:
                        points.append(Point(x, y, z, str_id, d))
                    else:
                        if len(points) > 1:
                            segments.append(Segment(points))
                        points = []
                else:
                    has_axis_record = True

    if len(segments) > 0:
        vl = QgsVectorLayer('LineStringZ', 'imported_string_file', 'memory')
        vl.setCrs(QgsProject.instance().crs())
        pr = vl.dataProvider()
        pr.addAttributes(Segment.qgsFields())
        vl.updateFields()
        pr.addFeatures([segment.asQgsFeature() for segment in segments])
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)
    else:
        return
