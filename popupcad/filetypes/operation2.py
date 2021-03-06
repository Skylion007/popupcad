# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""

from dev_tools.acyclicdirectedgraph import Node
from popupcad.filetypes.userdata import UserData
from popupcad.filetypes.operationoutput import OperationOutput


class Operation2(Node, UserData):
    name = 'Operation'

    def __init__(self):
        Node.__init__(self)
        UserData.__init__(self)

    def editdata(self, operation_links, sketch_links, design_links):
        self.operation_links = operation_links
        self.sketch_links = sketch_links
        self.design_links = design_links
        self.clear_output()

    def clear_output(self):
        try:
            del self.output
        except AttributeError:
            pass

    def parentrefs(self):
        a = []
        for key, values in self.operation_links.items():
            b = [operation_ref for operation_ref, output_index in values]
            a.extend(b)
        return a

    def subdesignrefs(self):
        a = []
        for key, values in self.design_links.items():
            a.extend(values)
        return a

    def sketchrefs(self):
        a = []
        for key, values in self.sketch_links.items():
            a.extend(values)
        return a

    def replace_op_refs(self, refold, refnew):
        for key, list1 in self.operation_links.items():
            while refold in list1:
                list1[list1.index(refold)] = refnew
        self.clear_output()

    def replace_sketch_refs(self, refold, refnew):
        for key, list1 in self.sketch_links.items():
            while refold in list1:
                list1[list1.index(refold)] = refnew
        self.clear_output()

#    def copy(self,*args,**kwargs):
#        return self

    def upgrade(self, *args, **kwargs):
        return self

    def getoutputref(self):
        try:
            return self._outputref
        except AttributeError:
            self._outputref = 0
            return self._outputref

    def generate(self, design):
        result = self.operate(design)
        output = OperationOutput(result, 'default', self)
        self.output = [output]

    @classmethod
    def new(cls, parent, design, currentop, newsignal):
        dialog = cls.buildnewdialog(design, currentop)
        if dialog.exec_() == dialog.Accepted:
            operation = cls(*dialog.acceptdata())
            newsignal.emit(operation)

    def edit(self, parent, design, editedsignal):
        dialog = self.buildeditdialog(design)
        if dialog.exec_() == dialog.Accepted:
            self.editdata(*dialog.acceptdata())
            editedsignal.emit(self)

    def description_get(self):
        try:
            return self._description
        except AttributeError:
            self._description = ''
            return self._description

    def description_set(self, value):
        self._description = value

    description = property(description_get, description_set)

    def edit_description(self):
        import PySide.QtGui as qg
        result, ok = qg.QInputDialog.getText(
            None, 'description', 'label', text=self.description)
        if ok:
            self.description = result

    def copy_internals(self, new):
        new.id = self.id
        new.customname = self.customname
        new.description = self.description
        return new

    def copy_wrapper(self):
        new = self.copy()
        self.copy_internals(new)
        return new

    def upgrade_wrapper(self):
        new = self.upgrade()
        self.copy_internals(new)
        return new


class LayerBasedOperation(object):

    @staticmethod
    def convert_layer_links(layer_links, layerdef_old, layerdef_new):
        layer_links_new = [
            layer2.id for layer1,
            layer2 in zip(
                layerdef_old.layers,
                layerdef_new.layers) if layer1.id in layer_links]
        return layer_links_new
