# pylint: disable=import-error

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsField, QgsGeometry
from re import sub

class Point:
    """
    A 3D point in a string file.
    """

    description_count = 0

    def __init__(self, x, y, z, str_id=None, descriptions=None):
        self.x = x
        self.y = y
        self.z = z
        if descriptions:
            self.descriptions = sub(r'\s*,\s*', ',', descriptions).split(',')
        else:
            self.descriptions = []
        self.str_id = str_id
        if Point.description_count < len(self.descriptions):
            Point.description_count = len(self.descriptions)

    def coordinates(self):
        return f'{self.x} {self.y} {self.z}'


class Segment:
    """
    Line string segment composed of Points with identical str_id
    """

    def __init__(self, points):
        self.str_id = None
        self.point_list = points
        self.description_list = [None] * 100
        for point in self.point_list:
            if not self.str_id:
                self.str_id = point.str_id
            else:
                if self.str_id != point.str_id:
                    raise Exception('String id of points do not match.')
            for i in range(0, len(point.descriptions)):
                if self.description_list[i]:
                    self.description_list[i] +=  f', {point.descriptions[i]}'
                else:
                    self.description_list[i] =  point.descriptions[i]

    def asQgsFeature(self):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(self.asWKT()))
        attributes = [self.str_id]
        attributes.extend(self.getAttributes())
        feature.setAttributes(attributes)
        return feature

    def asWKT(self):
        coordinates = [point.coordinates() for point in self.point_list]
        return 'LINESTRING (' + ','.join(coordinates) + ')'

    def getAttributes(self):
        return self.description_list[0:Point.description_count]

    @staticmethod
    def qgsFields():
        fields = [QgsField('string', QVariant.Int)]
        if Point.description_count > 0:
            fields.extend([QgsField(f'd{i}', QVariant.String) for i in range(1, Point.description_count + 1)])
        return fields
