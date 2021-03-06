# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""

import popupcad
import PySide.QtCore as qc
import PySide.QtGui as qg
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy
#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')


class GLObjectViewer(qg.QWidget):

    def __init__(self, *args, **kwargs):
        super(GLObjectViewer, self).__init__(*args, **kwargs)

        self.view = GLViewWidget(self)

        self.slider = qg.QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setTickInterval(1)
        self.slider.setValue(self.view.z_zoom)
        self.slider.valueChanged.connect(self.view.update_zoom)

        self.slider2 = qg.QSlider()
        self.slider2.setMinimum(-1)
        self.slider2.setMaximum(1000)
        self.slider2.setTickInterval(1)
        self.slider2.setValue(self.view.transparency)
        self.slider2.valueChanged.connect(self.view.update_transparency)


        layout = qg.QHBoxLayout()

        layout.addWidget(self.view)
        layout.addWidget(self.slider)
        layout.addWidget(self.slider2)
        self.setLayout(layout)
#    def screenshot(self):
#        self.view.screenshot()
#


class GLViewWidget(gl.GLViewWidget):

    def __init__(self, *args, **kwargs):
        super(GLViewWidget, self).__init__(*args, **kwargs)
        self.transparency = -1
        self.z_zoom = 500
        self.opts['center'] = qg.QVector3D(0,0,0)
        self.opts['distance'] = 20
        self.opts['elevation'] = 60
        self.opts['azimuth'] = -90
#        self.setMinimumSize(300,300)
        self.setSizePolicy(
            qg.QSizePolicy.Policy.MinimumExpanding,
            qg.QSizePolicy.Policy.MinimumExpanding)
#        c = pg.mkColor(120,120,200)
        c = pg.mkColor(1, 1, 1)
#        print(c)
        self.setBackgroundColor(c)

    def clear(self):
        while len(self.items) > 0:
            self.removeItem(self.items[0])

    def add_grid(self):
        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        self.addItem(g)
#    def screenshot(self):
#        import popupcad
#        import os

    def update_object(self, zvalue, triangles_by_layer, layers):
        self.triangles_by_layer = triangles_by_layer
        self.layers = layers
        self.zvalue = zvalue
        self.build_object()

        for item in self.meshitems:
            self.addItem(item)
        self.update_layer_z()
        self.update_transparency_inner()

    def update_zoom(self, value):
        self.z_zoom = value
        self.update_layer_z()
    def update_layer_z(self):
        zoom_act = (self.z_zoom/1000)**2*500
        for layer, item in zip(self.layers, self.meshitems):
            item.resetTransform()
            z = self.zvalue[layer] * (1+zoom_act)
            item.translate(0, 0, z)

    def update_transparency(self,value):
        self.transparency = value
        self.update_transparency_inner()
    def update_transparency_inner(self):
        for layer, item in zip(self.layers, self.meshitems):
            color = list(layer.color)
            transparency = self.transparency
            if transparency>=0:
                color[3] = transparency/1000
            item.setColor(color)

    def build_object(self):
        self.clear()
#        self.add_grid()
        self.meshitems = []
        for layer in self.layers:
            tri = numpy.array(self.triangles_by_layer[layer])
            if len(tri) > 0:
                z = numpy.zeros((tri.shape[0], tri.shape[1], 1))
                tri = numpy.concatenate((tri, z), 2)
                color = layer.color
#                print(color)
                colors = numpy.zeros((tri.shape[0], 3, 4))
                for ii in range(tri.shape[0]):
                    for jj in range(3):
                        colors[ii, jj] = color
#                m = gl.GLMeshItem(vertexes=tri,vertexColors=colors,edgeColor=(1,1,1,1),computeNormals=True)
                m = gl.GLMeshItem(vertexes=tri,computeNormals=False)
                m.setGLOptions('translucent')
                self.meshitems.append(m)
#                self.addItem(m)

    def add_default_item(self):
        verts = numpy.empty((36, 3, 3), dtype=numpy.float32)
        theta = numpy.linspace(0, 2 * numpy.pi, 37)[:-1]
        verts[:, 0] = numpy.vstack(
            [2 * numpy.cos(theta), 2 * numpy.sin(theta), [0] * 36]).T
        verts[:, 1] = numpy.vstack(
            [4 * numpy.cos(theta + 0.2), 4 * numpy.sin(theta + 0.2), [-1] * 36]).T
        verts[:, 2] = numpy.vstack(
            [4 * numpy.cos(theta - 0.2), 4 * numpy.sin(theta - 0.2), [1] * 36]).T

        colors = numpy.random.random(size=(verts.shape[0], 3, 4))
        m2 = gl.GLMeshItem(
            vertexes=verts,
            vertexColors=colors,
            smooth=False,
            shader='balloon',
            drawEdges=True,
            edgeColor=(
                1,
                1,
                0,
                1))
        m2.translate(-5, 5, 0)
        self.addItem(m2)

    def sizeHint(self):
        return qc.QSize(300, 300)


if __name__ == '__main__':
    import sys
    app = qg.QApplication(sys.argv)
    mw = GLObjectViewer()
    mw.view.add_default_item()
    mw.show()
#    sys.exit(app.exec_())
