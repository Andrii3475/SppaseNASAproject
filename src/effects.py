"""Зоряне небо. Жодної логіки сценарію."""

import random

from panda3d.core import (Geom, GeomNode, GeomPoints, GeomVertexData,
                          GeomVertexFormat, GeomVertexWriter, Vec3)


class StarField:
    RADIUS = 300.0

    def __init__(self, base, count, world):
        self.base = base
        self.count = count
        self.world = world
        self.node = None

    def build(self):
        vformat = GeomVertexFormat.getV3c4()
        vdata = GeomVertexData("stars", vformat, Geom.UHStatic)
        vdata.setNumRows(self.count)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        for _ in range(self.count):
            x, y, z = random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
            length = (x * x + y * y + z * z) ** 0.5 or 1.0
            vertex.addData3(Vec3(x / length, y / length, z / length) * self.RADIUS)
            b = random.uniform(0.4, 1.0)
            color.addData4(b, b, b, 1.0)

        prim = GeomPoints(Geom.UHStatic)
        prim.addNextVertices(self.count)
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        gnode = GeomNode("stars")
        gnode.addGeom(geom)

        self.node = self.world.attachNewNode(gnode)
        self.node.setRenderModeThickness(2.0)
        self.node.setRenderModePerspective(True)
        self.node.setLightOff()