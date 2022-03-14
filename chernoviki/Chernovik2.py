import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from pyqtgraph.flowchart import Flowchart, Node
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart.library.common import CtrlNode
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class Main(QMainWindow):
    check_box = None
    tray_icon = None
    def __init__(self):
        super(Main, self).__init__()
        loadUi("UI/Main.ui",self)

## Create an empty flowchart with a single input and output
        fc = Flowchart(terminals={
            'dataIn': {'io': 'in'},
            'dataOut': {'io': 'out'}
        })
        w = fc.widget()

        self.LayOut1.addWidget(fc.widget(), 0, 0, 2, 1)

## Create two ImageView widgets to display the raw and processed data with contrast
## and color control.
        v1 = pg.ImageView()
        v2 = pg.ImageView()
        self.LayOut1.addWidget(v1, 0, 1)
        self.LayOut1.addWidget(v2, 1, 1)

## generate random input data
        data = np.random.normal(size=(100, 100))
        data = 25 * pg.gaussianFilter(data, (5, 5))
        data += np.random.normal(size=(100, 100))
        data[40:60, 40:60] += 15.0
        data[30:50, 30:50] += 15.0
        library = fclib.LIBRARY.copy()  # start with the default node set
        library.addNodeType(UnsharpMaskNode, [('Image',),
                                              ('Submenu_test', 'submenu2', 'submenu3')])
        fc.setLibrary(library)

        ## Now we will programmatically add nodes to define the function of the flowchart.
        ## Normally, the user will do this manually or by loading a pre-generated
        ## flowchart file.
        fNode = fc.createNode('UnsharpMask', pos=(0, 0))
        fc.connectTerminals(fc['dataIn'], fNode['dataIn'])
        fc.connectTerminals(fNode['dataOut'], fc['dataOut'])

        fc.setInput(dataIn=data)


class ImageViewNode(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'ImageView'

    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io': 'in'}})

    def setView(self, view):  ## setView must be called by the program
        self.view = view

    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.

        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1, 1)))  # give a blank array to clear the view
            else:
                self.view.setImage(data)

## We will define an unsharp masking filter node as a subclass of CtrlNode.
## CtrlNode is just a convenience class that automatically creates its
## control widget based on a simple data structure.
class UnsharpMaskNode(CtrlNode):
    """Return the input data passed through an unsharp mask."""
    nodeName = "UnsharpMask"
    uiTemplate = [
        ('sigma', 'spin', {'value': 1.0, 'step': 1.0, 'bounds': [0.0, None]}),
        ('strength', 'spin', {'value': 1.0, 'dec': True, 'step': 0.5, 'minStep': 0.01, 'bounds': [0.0, None]}),
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),  # each terminal needs at least a name and
            'dataOut': dict(io='out'),  # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, dataIn, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}
        sigma = self.ctrls['sigma'].value()
        strength = self.ctrls['strength'].value()
        output = dataIn - (strength * pg.gaussianFilter(dataIn, (sigma, sigma)))
        return {'dataOut': output}

app = QApplication(sys.argv)
mainW = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.show()
app.exec()
