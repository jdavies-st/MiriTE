#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

An extension to the standard STScI data model for MIRI IPC kernel data, 
based on the base MIRI data model.

:Reference:

The STScI jwst.datamodels documentation. See
http://ssb.stsci.edu/doc/jwst/jwst/datamodels/index.html

:History:

28 Oct 2014: Created
09 Jul 2015: Fixed initialisation bug.
19 Aug 2015: Duplicated parts of schema now reference STScI model.
15 Jun 2017: meta.reffile schema level removed to match changes in the
             JWST build 7.1 data models release. meta.reffile.type also
             changed to meta.reftype. TYPE keyword replaced by DATAMODL.
12 Jul 2017: Replaced "clobber" parameter with "overwrite".

@author: Vincent Geers (DIAS)

"""
# For consistency, import the same Python V3 features as the STScI data model.
from __future__ import absolute_import, unicode_literals, division, print_function

import numpy as np

# Import the MIRI data model.
from miri.datamodels.dqflags import insert_value_column
from miri.datamodels.miri_model_base import MiriDataModel

# List all classes and global functions here.
__all__ = ['MiriIPCModel']


class MiriIPCModel(MiriDataModel):
    """
    
    A data model for MIRI IPC kernel data.
        
    :Parameters:
    
    init: shape tuple, file path, file object, pyfits.HDUList, numpy array
        An optional initializer for the data model, which can have one
        of the following forms:
        
        * None: A default data model with no shape. (If a data array is
          provided in the mask parameter, the shape is derived from the
          array.)
        * Shape tuple: Initialize with empty data of the given shape.
        * File path: Initialize from the given file.
        * Readable file object: Initialize from the given file object.
        * pyfits.HDUList: Initialize from the given pyfits.HDUList.
        
    data: numpy array (optional)
        An array containing the last frame data.
        If a data parameter is provided, its contents overwrite the
        data initialized by the init parameter.
    \*\*kwargs:
        All other keyword arguments are passed to the DataModel initialiser.
        See the jwst.datamodels documentation for the meaning of these keywords.
    
    """
    schema_url = "miri_ipc.schema.yaml"

    def __init__(self, init=None, data=None, **kwargs):
        """
        
        Initialises the MiriIPCModel class.
        
        Parameters: See class doc string.

        """
        super(MiriIPCModel, self).__init__(init=init, **kwargs)

        # Data type is IPC.
        self.meta.model_type = 'IPC'
        self.meta.reftype = 'IPC'
        
        # The default pedigree is 'GROUND'
        if not self.meta.pedigree:
            self.meta.pedigree = 'GROUND'
            
        # A USEAFTER date must exist. If not relevant, set it to an
        # impossibly early date.
        if not self.meta.useafter:
            self.meta.useafter = '2000-01-01T00:00:00'
            
        if data is not None:
            self.data = data

#
# A minimal test is run when this file is run as a main program.
# For a more substantial test see miri/datamodels/tests.
#
if __name__ == '__main__':
    print("Testing the MiriIPCModel module.")

    PLOTTING = False
    SAVE_FILES = False

    data3x3 = np.array([[1.0,1.2,1.1],[1.3,1.2,1.0],[1.1,0.8,0.9]])

    print("IPC model with data :")
    with MiriIPCModel( data=data3x3 ) as testdata:
        print(testdata)
        if PLOTTING:
            testdata.plot(description="testdata")
        if SAVE_FILES:
            testdata.save("test_ipc_model1.fits", overwrite=True)
        del testdata

    print("Test finished.")