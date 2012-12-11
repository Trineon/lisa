# -*- coding: utf-8 -*-
"""
================================================================================
Name:        uiBinaryClosingAndOpening
Purpose:     (CZE-ZCU-FAV-KKY) Liver medical project

Author:      Pavel Volkovinsky (volkovinsky.pavel@gmail.com)

Created:     08.11.2012
Copyright:   (c) Pavel Volkovinsky 2012
Licence:     <your licence>
================================================================================
"""

import sys
sys.path.append("../src/")
sys.path.append("../extern/")

import logging
logger = logging.getLogger(__name__)

import numpy
#import scipy.misc
#import scipy.io
import scipy.ndimage

#import unittest
#import argparse

import matplotlib.pyplot as matpyplot
import matplotlib
from matplotlib.widgets import Slider#, Button, RadioButtons

"""
================================================================================
uiBinaryClosingAndOpening
================================================================================
"""
class uiBinaryClosingAndOpening:

    def __init__(self, imgUsed, initslice = 0, cmap = matplotlib.cm.Greys_r):

        inputDimension = numpy.ndim(imgUsed)
        #print('Dimenze vstupu: ',  inputDimension)
        self.cmap = cmap
        self.imgChanged1 = imgUsed
        self.imgChanged2 = imgUsed
        
        if(inputDimension == 2):
            
            self.imgUsed = imgUsed
            self.imgChanged = imgUsed
                
            """
            self.imgChanged1 = self.imgUsed
            self.imgChanged2 = self.imgUsed
            self.imgChanged3 = self.imgUsed
            """
            
            # Zakladni informace o obrazku (+ statisticke)
            """
            print('Image dtype: ', imgUsed.dtype)
            print('Image size: ', imgUsed.size)
            print('Image shape: ', imgUsed.shape[0], ' x ',  imgUsed.shape[1])
            print('Max value: ', imgUsed.max(), ' at pixel ',  imgUsed.argmax())
            print('Min value: ', imgUsed.min(), ' at pixel ',  imgUsed.argmin())
            print('Variance: ', imgUsed.var())
            print('Standard deviation: ', imgUsed.std())
            """
            
            # Ziskani okna (figure)
            self.fig = matpyplot.figure()
            # Pridani subplotu do okna (do figure)
            self.ax1 = self.fig.add_subplot(111)
            """
    #        self.ax0 = self.fig.add_subplot(232)
            self.ax1 = self.fig.add_subplot(131)
            self.ax2 = self.fig.add_subplot(132)
            self.ax3 = self.fig.add_subplot(133)
            """
            # Upraveni subplotu
            self.fig.subplots_adjust(left = 0.1, bottom = 0.25)
            # Vykresli obrazek
    #        self.im0 = self.ax0.imshow(imgUsed)
            self.im1 = self.ax1.imshow(self.imgChanged, self.cmap)
            """
            self.im2 = self.ax2.imshow(imgUsed)
            self.im3 = self.ax3.imshow(imgUsed)
            """
     #       self.fig.colorbar(self.im1)
    
            # Zakladni informace o slideru
            axcolor = 'white' # lightgoldenrodyellow
            axmin = self.fig.add_axes([0.25, 0.16, 0.495, 0.03], axisbg = axcolor)
            axmax  = self.fig.add_axes([0.25, 0.12, 0.495, 0.03], axisbg = axcolor)
            """
            axopening = self.fig.add_axes([0.25, 0.08, 0.495, 0.03], axisbg = axcolor)
            axclosing = self.fig.add_axes([0.25, 0.04, 0.495, 0.03], axisbg = axcolor)
            """
            
            # Vytvoreni slideru
                # Minimalni pouzita hodnota v obrazku
            min0 = imgUsed.min()
                # Maximalni pouzita hodnota v obrazku
            max0 = imgUsed.max()
                # Vlastni vytvoreni slideru
            self.smin = Slider(axmin, 'Minimal threshold', min0, max0, valinit = min0)
            self.smax = Slider(axmax, 'Maximal threshold', min0, max0, valinit = max0)
            """
            self.sopen = Slider(axopening, 'Binary opening', 0, 10, valinit = 0)
            self.sclose = Slider(axclosing, 'Binary closing', 0, 10, valinit = 0)
            """
            
            # Udalost pri zmene hodnot slideru - volani updatu
            self.smin.on_changed(self.updateImg2D)
            self.smax.on_changed(self.updateImg2D)
        
        elif(inputDimension == 3):
            
            # Zakladni informace o obrazcich (+ statisticke)
            """
            print('Image dtype: ', imgUsed.dtype)
            print('Image size: ', imgUsed.size)
            print('Image shape: ', imgUsed.shape[0], ' x ',  imgUsed.shape[1], ' x ',  imgUsed.shape[2])
            print('Max value: ', imgUsed.max(), ' at pixel ',  imgUsed.argmax())
            print('Min value: ', imgUsed.min(), ' at pixel ',  imgUsed.argmin())
            print('Variance: ', imgUsed.var())
            print('Standard deviation: ', imgUsed.std())
            """
            
            self.imgUsed = imgUsed
            self.imgChanged = self.imgUsed
            self.imgChanged1 = self.imgChanged
            self.imgChanged2 = self.imgChanged
            
            #self.imgMin = numpy.min(self.imgUsed)
            #self.imgMax = numpy.max(self.imgUsed)
            
            self.imgShape = list(self.imgUsed.shape)
            
            self.fig = matpyplot.figure()
            # Pridani subplotu do okna (do figure)
            self.ax1 = self.fig.add_subplot(121)
            self.ax2 = self.fig.add_subplot(122)
            
            # Upraveni subplotu
            self.fig.subplots_adjust(left = 0.1, bottom = 0.3)
            
            # Nalezeni a pripraveni obrazku k vykresleni
     #       imgShowPlace = numpy.round(self.imgShape[2] / 2).astype(int)
     #       self.imgShow = self.imgUsed[:, :, imgShowPlace]
            self.imgShow = numpy.amax(self.imgChanged, 2)
            
            # Vykreslit obrazek
            self.im1 = self.ax1.imshow(self.imgShow, self.cmap)
            self.im2 = self.ax2.imshow(self.imgShow, self.cmap)
    
            # Zakladni informace o slideru
            axcolor = 'white' # lightgoldenrodyellow
            axopening1 = self.fig.add_axes([0.25, 0.16, 0.495, 0.03], axisbg = axcolor)
            axclosing1 = self.fig.add_axes([0.25, 0.12, 0.495, 0.03], axisbg = axcolor)
            axopening2 = self.fig.add_axes([0.25, 0.04, 0.495, 0.03], axisbg = axcolor)
            axclosing2 = self.fig.add_axes([0.25, 0.08, 0.495, 0.03], axisbg = axcolor)
            
            # Vytvoreni slideru
            self.sopen1 = Slider(axopening1, 'Binary opening 1', 0, 100, valinit = 0)
            self.sclose1 = Slider(axclosing1, 'Binary closing 1', 0, 100, valinit = 0)
            self.sopen2 = Slider(axopening2, 'Binary opening 2', 0, 100, valinit = 0)
            self.sclose2 = Slider(axclosing2, 'Binary closing 2', 0, 100, valinit = 0)
            
            self.sopen1.on_changed(self.updateImg1Binary3D)
            self.sclose1.on_changed(self.updateImg1Binary3D)
            self.sopen2.on_changed(self.updateImg2Binary3D)
            self.sclose2.on_changed(self.updateImg2Binary3D)
            
        else:
            
            print('Spatny vstup.\nDimenze vstupu neni 2 ani 3.\nUkoncuji prahovani.')

    def showPlot(self):
        
        # Zobrazeni plot (figure)
        matpyplot.show()
        
        return (self.imgChanged1, self.imgChanged2)

    def updateImg2D(self, val):
        
        # Prahovani (smin, smax)
        img1 = self.imgUsed.copy() > self.smin.val
        self.imgChanged = img1 #< self.smax.val
        
        # Predani obrazku k vykresleni
        self.im1 = self.ax1.imshow(self.imgChanged, self.cmap)
        # Prekresleni
        self.fig.canvas.draw()
        
    def updateImg1Binary3D(self, val):
        
        self.sopen1.valtext.set_text('{}'.format(int(self.sopen1.val)))
        self.sclose1.valtext.set_text('{}'.format(int(self.sclose1.val)))
        
        self.fig.canvas.draw()
        
        imgChanged1 = self.imgChanged
        
        if(self.sopen1.val >= 0.5):
            imgChanged1 = scipy.ndimage.binary_opening(self.imgChanged, structure = None, iterations = int(numpy.round(self.sopen1.val, 0)))
        else:
            imgChanged1 = self.imgChanged1
            
        if(self.sclose1.val >= 0.5):
            self.imgChanged1 = scipy.ndimage.binary_closing(imgChanged1, structure = None, iterations = int(numpy.round(self.sclose1.val, 0)))
        else:
            self.imgChanged1 = imgChanged1
            
        # Predani obrazku k vykresleni
        self.imgShow1 = numpy.amax(self.imgChanged1, 2)
        self.im1 = self.ax1.imshow(self.imgShow1, self.cmap)
        
        # Prekresleni
        self.fig.canvas.draw()
        
    def updateImg2Binary3D(self, val):
        
        self.sclose2.valtext.set_text('{}'.format(int(self.sclose2.val)))
        self.sopen2.valtext.set_text('{}'.format(int(self.sopen2.val)))
        
        self.fig.canvas.draw()
        
        imgChanged2 = self.imgChanged
        
        if(self.sclose2.val >= 0.5):
            imgChanged2 = scipy.ndimage.binary_closing(self.imgChanged, structure = None, iterations = int(numpy.round(self.sclose2.val, 0)))
        else:
            imgChanged2 = self.imgChanged
        
        if(self.sopen2.val >= 0.5):
            self.imgChanged2 = scipy.ndimage.binary_opening(imgChanged2, structure = None, iterations = int(numpy.round(self.sopen2.val, 0)))
        else:
            self.imgChanged2 = imgChanged2
            
        # Predani obrazku k vykresleni
        self.imgShow2 = numpy.amax(self.imgChanged2, 2)
        self.im2 = self.ax2.imshow(self.imgShow2, self.cmap)
        
        # Prekresleni
        self.fig.canvas.draw()
    
"""
================================================================================
main
================================================================================
"""
"""
if __name__ == "__main__":
    
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    logging.basicConfig(format='%(message)s')

    formatter = logging.Formatter("%(levelname)-5s [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description='Segment vessels from liver')
    parser.add_argument('-f','--filename',
            default = 'lena',
            help='*.mat file with variables "data", "segmentation" and "threshod"')
    parser.add_argument('-d', '--debug', action='store_true',
            help='run in debug mode')
    parser.add_argument('-t', '--tests', action='store_true',
            help='run unittest')
    parser.add_argument('-o', '--outputfile', type=str,
        default='output.mat',help='output file name')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.tests:
        sys.argv[1:]=[]
        unittest.main()

    if args.filename == 'lena':
        data = scipy.misc.lena()
    else:
        mat = scipy.io.loadmat(args.filename)
        logger.debug(mat.keys())

        dataraw = scipy.io.loadmat(args.filename)
        
        data = dataraw['data'] * (dataraw['segmentation'] == 1)

    ui = uiThreshold(data)
    output = ui.showPlot()

    scipy.io.savemat(args.outputfile, {'data':output})
"""



