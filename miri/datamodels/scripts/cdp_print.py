#!/usr/bin/env python
#
# :History:
# 
# 29 Jul 2013: Created.
# 31 Jul 2013: Simplified the first pass through the file.
# 13 Aug 2013: Include all kinds of flux conversion model.
# 12 Sep 2013: Added the --datatype option to override the
#              data type in the original file.
# 09 Oct 2013: Added MiriJumpModel.
# 31 Oct 2013: Removed imports that are not needed.
# 12 Dec 2013: Switch to using the datamodels.open function.
# 29 Sep 2014: Check for REFTYPE before checking for TYPE.
# 20 Jan 2017: Replaced "clobber" parameter with "overwrite".
# 30 Jun 2017: meta.reffile schema level removed to match changes in the
#              JWST build 7.1 data models release. meta.reffile.type also
#              changed to meta.reftype. TYPE keyword replaced by DATAMODL.
# 02 Nov 2018: Added ability to display metadata info and/or a data summary
#              instead of the full data listing.
#
# @author: Steven Beard (UKATC)
#
"""

Script `cdp_print` displays the contents of any FITS file containing a
MIRI calibration data product.

By default, the entire contents of the data model are displayed. If the
full display is too long, a shorter summary will be displayed if the
--info and/or --summary parameters are included. For example:

    cdp_verify.py MIRI_FM_MIRIMAGE_GAIN_04.00.00.fits
        Show the entire contents of the specified CDP

    cdp_verify.py MIRI_FM_MIRIMAGE_GAIN_04.00.00.fits --info
        Show the metadata contained in the specified CDP only

    cdp_verify.py MIRI_FM_MIRIMAGE_GAIN_04.00.00.fits --summary
        Show a summary of the data contained in the specified CDP only

    cdp_verify.py MIRI_FM_MIRIMAGE_GAIN_04.00.00.fits --info --summary
        Show a summary of the metadata and data contained in the specified CDP only

The following command arguments are defined by position::

    inputfile[0]
        The path+name of the CDP file to be read. Compulsory.

The command also takes the following options::

    --datatype <type-string>
        The name of the data type to be used to read the product.
        If specified, this option overrides the TYPE keyword
        contained in the input file.
    --verbose or -v
        Generate more verbose output.
    --plot or -p
        Plot the data.
    --info-only or --info or -i
        Display metadata information only
    --stats-only or --summary or -s
        Display statistics only
    --write or -w
        Write the data structure to a new file called <oldfile>_copy.fits
    --overwrite or -o
        Overwrite any existing FITS file.

"""

import optparse
import sys, time

# Import all the data models that might be contained in the file.
#from miri.datamodels.miri_measured_model import MiriMeasuredModel
import miri.datamodels        

if __name__ == "__main__":
    # Parse arguments
    help_text = __doc__
    usage = "%prog [opt] inputfile\n"
    usage += "Lists the contents of a FITS file compatible with "
    usage += "any MIRI calibration data product."
    parser = optparse.OptionParser(usage)
    parser.add_option("", "--datatype", dest="datatype", type="string",
                     default=None, help="Data type to use (overriding TYPE)"
                     )
    parser.add_option("-v", "--verbose", dest="verb", action="store_true",
                      help="Verbose mode"
                     )
    parser.add_option("-p", "--plot", dest="makeplot", action="store_true",
                      help="Plot the data"
                     )
    parser.add_option("-i", "--info-only", dest="infoonly", action="store_true",
                      help="Display metadata info only"
                     )
    parser.add_option("", "--info", dest="info", action="store_true",
                      help="Display metadata info only"
                     )
    parser.add_option("-s", "--stats-only", dest="statsonly", action="store_true",
                      help="Display statistics only"
                     )
    parser.add_option("", "--summary", dest="summary", action="store_true",
                      help="Display data summary only"
                     )
    parser.add_option("-w", "--write", dest="writefile", action="store_true",
                      help="Make a copy of the file"
                     )
    parser.add_option("-o", "--overwrite", dest="overwrite", action="store_true",
                      help="Overwrite the copy of the file if it already exists"
                     )

    (options, args) = parser.parse_args()

    try:
        inputfile = args[0]
    except IndexError:
        print(help_text)
        time.sleep(1) # Ensure help text appears before error messages.
        parser.error("Not enough arguments provided")
        sys.exit(1)

    verb = options.verb
    makeplot = options.makeplot
    infoonly = options.infoonly or options.info
    statsonly = options.statsonly or options.summary
    writefile = options.writefile
    if writefile:
        outputfile = inputfile + "_copy.fits"
    else:
        outputfile = None
    overwrite = options.overwrite

    if options.datatype:
        # Use the data type specified
        datatype = str(options.datatype)
        print("Forcing the data model to be opened with type \'%s\'" % datatype)
    else:
        datatype = ''

    # Display the data model using the class derived from the
    # data type.
    with miri.datamodels.open( init=inputfile, astype=datatype ) as datamodel:
        if hasattr(datamodel.meta, 'reftype'):
            datatype = datamodel.meta.reftype
            strg = "The data model is of type \'%s\'" % str(datatype)
        elif hasattr(datamodel.meta, 'datatype'):
            datatype = datamodel.meta.datatype
            strg = "The data model is of (pre-CDP-3) type \'%s\'" % str(datatype)
        else:
            strg = "The data model class name is \'%s\'" % \
                datamodel.__class__.__name__
            
        detector = datamodel.meta.instrument.detector
        if detector:
            strg += " for detector \'%s\'" % str(detector)
        mirifilter = datamodel.meta.instrument.filter
        if mirifilter:
            strg += " and filter \'%s\'" % str(mirifilter)
        print(strg)
        displayed = False
        if infoonly and hasattr(datamodel, 'get_title_and_metadata'):
            if verb:
                print("Showing metadata only...")
            print( datamodel.get_title_and_metadata() )
            displayed = True
        if statsonly and hasattr(datamodel, 'stats'):
            if verb:
                print("Calculating statistics...")
            print( datamodel.stats() )
            displayed = True
        if not displayed:
            print( str(datamodel) )
          
        if makeplot and hasattr(datamodel, 'plot'):
            if verb:
                print("Plotting...")
            datamodel.plot()
        
        if writefile:
            if verb:
                print("Saving a copy to \'%s\'." % outputfile)
            datamodel.save( outputfile, overwrite=overwrite )
        del datamodel
