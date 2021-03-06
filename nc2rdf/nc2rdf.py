import argparse
import os
import subprocess
import tempfile 
import netCDF4
import numpy as np
import bald

def nc2rdf(ncfilename, outformat, baseuri=None):  
    #print("nc2rdf test")
    #print(ncfile)
    root_container = bald.load_netcdf(ncfilename, baseuri=baseuri)
    ttl = root_container.rdfgraph().serialize(format=outformat).decode("utf-8")
    print(ttl)

def cdl2rdf(cdl_file, outformat, baseuri=None): 
    #print("cdl2rdf test")
    #print(cdl_file)
    tfile, tfilename = tempfile.mkstemp('.nc')
    #print(tfilename)
    subprocess.check_call(['ncgen', '-o', tfilename, cdl_file])

    nc2rdf(tfilename, outformat, baseuri=baseuri)

    os.close(tfile)
    os.remove(tfilename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert netCDF metadata to RDF.')
    parser.add_argument('-o', action="store", dest="format", default='n3', help="RDF output format (n3 *default, ttl, xml)")
    parser.add_argument('--baseuri', action="store", dest="baseuri", help="Base URI for the graph")
    parser.add_argument('--cdl', action="store_true", dest="isCDL", default=False, help="Flag to indicate file is CDL")
    parser.add_argument('--nc', action="store_true", dest="isNC", default=False, help="Flag to indicate file is netCDF")
    parser.add_argument("ncfile", help="Path for the netCDF file")

    args = parser.parse_args()

    if(args.isCDL or args.ncfile.endswith(".cdl") or args.ncfile.endswith('.CDL')):
        cdl2rdf(args.ncfile, args.format, baseuri=args.baseuri)
    elif(args.isNC or args.ncfile.endswith(".nc") or args.ncfile.endswith('.NC')):
        nc2rdf(args.ncfile, args.format, baseuri=args.baseuri)
    else:
        print("Unrecognised file suffix. Please indicate if CDL or NC via --cdl or --nc");
