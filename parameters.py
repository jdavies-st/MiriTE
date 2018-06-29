#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

This file contains all the global parameters describing the MIRI instrument,
its capabilities and modes of operation. It exists to ensure the 

09 Oct 2013: Created within datamodels.util
28 Jun 2018: Moved to miri.parameters

@author: Steven Beard (UKATC)

"""

# --------------------------------------------------------------------------
# Dictionary of available detector readout modes.
#
# The tuple contains default values for:
# samplesum = number of A/D samples per reading
# sampleskip = number of A/D samples skipped before reading a pixel.
# refpixsampleskip = number of A/D samples skipped before reading a reference pixel.
# nframes = number of frames averaged per group.
# groupgap = number of frames dropped between groups.
# ngroups  = default number of readout groups per integration.
# nints    = default number of integrations per exposure.
# avggrps  = number of groups averaged to reduce data rate.
# avgints  = number of integrations averaged to reduce data rate.
#
#                                      r
#                                      e
#                                      f
#                                      p
#                                      i
#                                      x
#                                  s   s
#                              s   a   a
#                              a   m   m       g
#                              m   p   p   n   r   n       a   a
#                              p   l   l   f   o   g       v   v
#                              l   e   e   r   u   r   n   g   g
#                              e   s   s   a   p   o   i   g   i
#                              s   k   k   m   g   u   n   r   n
#                              u   i   i   e   a   p   t   p   t
#                              m   p   p   s   p   s   s   s   s
READOUT_MODE = {}
READOUT_MODE['SLOW'] =       (8,   1,  3,  1,  0, 10,  1,  1,  1)
READOUT_MODE['FAST'] =       (1,   0,  3,  1,  0,  1, 10,  1,  1)
READOUT_MODE['FASTINTAVG'] = (1,   0,  3,  1,  0,  1,  4,  1,  4)
READOUT_MODE['FASTGRPAVG'] = (1,   0,  3,  1,  0,  4,  1,  4,  1)
# The following four readout modes were used for MIRI testing only, and they
# will upset the JWST pipeline software if used.
# READOUT_MODE['SLOWINTAVG'] = (8,   1,  3,  1,  0,  1,  4,  1,  4)
# READOUT_MODE['SLOWGRPAVG'] = (8,   1,  3,  1,  0,  4,  1,  4,  1)
# READOUT_MODE['SLOWGRPGAP'] = (8,   1,  3,  4,  8,  4,  1,  1,  1)
# READOUT_MODE['FASTGRPGAP'] = (1,   0,  3,  4,  8,  4,  1,  1,  1)

# --------------------------------------------------------------------------
# Dictionary of available subarray options.
#
# REFERENCE:
# The Mid-Infrared Instrument for the James Webb Space Telescope,
# VIII: The MIRI Focal Plane System; M. E. Ressler et al.,
# Publications of the Astronomical Society of Pacific, Volume 127,
# Issue 953, pp. 675 (2015)
#
# Each tuple contains
# (first column, first row, number of columns, number of rows).
#                               s    s
#                               t    t     c
#                               a    a     o
#                               r    r     l
#                               t    t     u     r
#                               c    r     m     o
#                               o    o     n     w
#                               l    w     s     s
SUBARRAY = {}
SUBARRAY['FULL'] =          (   1,   1, 1032, 1024 )
SUBARRAY['GENERIC'] =       (   1,   1, 1032, 1024 )
SUBARRAY['MASK1140'] =      (   1, 245,  288,  224 )
SUBARRAY['MASK1550'] =      (   1, 467,  288,  224 )
SUBARRAY['MASK1065'] =      (   1,  19,  288,  224 )
SUBARRAY['MASKLYOT'] =      (   1, 717,  320,  304 )
SUBARRAY['BRIGHTSKY'] =     ( 457,  51,  512,  512 )
SUBARRAY['SUB256'] =        ( 413,  51,  256,  256 )
SUBARRAY['SUB128'] =        (   1, 889,  136,  128 )
SUBARRAY['SUB64'] =         (   1, 779,   72,   64 )
SUBARRAY['SLITLESSPRISM'] = (   1, 529,   72,  416 )

# --------------------------------------------------------------------------
# Lists of selections, as defined on the "MiriCalfileMetaData" page.
MIRI_MODELS = ['VM', 'JPL', 'FM']

MIRI_DETECTORS = ['MIRIMAGE', 'MIRIFULONG', 'MIRIFUSHORT']
MIRI_DETECTORS_EXTRAS = ['IM', 'LW', 'SW'] # For backwards compatibility only.

MIRI_SETTINGS = ['RAL1', 'JPL1']

MIRI_READPATTS = ['SLOW', 'FAST', 'FASTGRPAVG']

# Also = list(SUBARRAY.keys()) - ['FULL', 'GENERIC']
MIRI_SUBARRAYS = ['MASK1140', 'MASK1550', 'MASK1065', 'MASKLYOT',
                  'BRIGHTSKY', 'SUB256', 'SUB128', 'SUB64', 'SLITLESSPRISM']

MIRI_CHANNELS = ['1', '2', '3', '4', '12', '34']

MIRI_BANDS = ['SHORT', 'MEDIUM', 'LONG', 'SHORT-MEDIUM',  'SHORT-LONG',
              'MEDIUM-SHORT', 'MEDIUM-LONG', 'LONG-SHORT', 'LONG-MEDIUM']
MIRI_BANDS_EXTRAS = ['A', 'B', 'C'] # For backwards compatibility only.

# Note that 'FLENS' and 'F2550WR' are allowed values for the filter metadata,
# but there are no CDP files for these filters.
MIRI_FILTERS = ['F560W','F770W','F1000W','F1130W', 'F1280W','F1500W','F1800W',
                'F2100W', 'F2550W', 'F2550WR','F1065C', 'F1140C', 'F1550C',
                'F2300C','P750L','FLENS', 'FND', 'OPAQUE']

# Rules for testing compulsory CDP metadata
CDP_METADATA = [['TELESCOP', 'JWST'],
                ['INSTRUME', 'MIRI'],
                ['MODELNAM', MIRI_MODELS + ['N/A']],
                ['DETECTOR', MIRI_DETECTORS + ['N/A']],
                # DETSETNG is removed from STSCI CDP specification
#                 ['DETSETNG', MIRI_SETTINGS + ['ANY']],
                ['READPATT', MIRI_READPATTS + ['ANY', 'N/A']],
                ['SUBARRAY', MIRI_SUBARRAYS + ['FULL', 'GENERIC', 'N/A']],
                ['FASTAXIS', 1],
                ['SLOWAXIS', 2],
                ['PEDIGREE', ['GROUND', 'DUMMY', 'SIMULATION']],
                ['USEAFTER', []],  # Empty list means any value accepted.
                ['DESCRIP', []],  # Empty list means any value accepted.
                ['AUTHOR', []],  # Empty list means any value accepted.
                ['DATE', []],  # Empty list means any value accepted.
                ['VERSION', []],  # Empty list means any value accepted.
                ]
# Additional compulsory metadata for non-GENERIC subarrays
CDP_SUBARRAY = [['SUBSTRT1', []], # Empty list means any value accepted.
                ['SUBSTRT2', []], # Empty list means any value accepted.
                ['SUBSIZE1', []], # Empty list means any value accepted.
                ['SUBSIZE2', []], # Empty list means any value accepted.
                ]
# Keywords used in HISTORY records
CDP_HISTORY = ['DOCUMENT', 'SOFTWARE', 'DATA USED', 'DIFFERENCES']
#
# Dictionary of the relationship between known detector settings
#                         Name -> (FRMRSETS, ROWRSETS, RPCDELAY)
DETECTOR_SETTINGS_DICT = {'RAL1': (0, 3, 24),
                          'JPL1': (3, 4, 90)}



