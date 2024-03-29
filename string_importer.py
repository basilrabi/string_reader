# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level

from qgis.core import Qgis, QgsProject, QgsVectorLayer
from re import search
from .geom import Point, Segment

message_duration = 30
point_pattern = "^(\\d+)\\s*,\\s*(\\d+\\.?\\d*)\\s*,\\s*(\\d+\\.?\\d*)\\s*,\\s*(-?\\d+\\.?\\d*)\\s*,\\s*(.*)\\s*"

def import_str(string_file: str, is_point: bool, iface) -> None:
    points = []
    segments = []
    vertex_counter = 0
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
                        vertex_counter += 1
                    else:
                        if len(points) > 1:
                            if not is_point:
                                segments.append(Segment(points))
                            elif is_point and vertex_counter > 1:
                                iface.messageBar().pushMessage("Error", f"{string_file} not imported. Point string file is selected but it contains segments.", level=Qgis.Critical, duration=message_duration)
                                return
                        if not is_point:
                            points = []
                        vertex_counter = 0
                else:
                    has_axis_record = True

    if len(segments) > 0 and not is_point:
        vl = QgsVectorLayer('LineStringZ', f'String {string_file}', 'memory')
        vl.setCrs(QgsProject.instance().crs())
        pr = vl.dataProvider()
        pr.addAttributes(Segment.qgsFields())
        vl.updateFields()
        pr.addFeatures([segment.asQgsFeature() for segment in segments])
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)
        return
    if len(segments) == 0 and is_point:
        vl = QgsVectorLayer('PointZ', f'String {string_file}', 'memory')
        vl.setCrs(QgsProject.instance().crs())
        pr = vl.dataProvider()
        pr.addAttributes(Segment.qgsFields())
        vl.updateFields()
        pr.addFeatures([point.asQgsFeature() for point in points])
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)
        return
    else:
        iface.messageBar().pushMessage("Error", f"{string_file} not imported. String file does not contain any segments.", level=Qgis.Critical, duration=message_duration)
        return
