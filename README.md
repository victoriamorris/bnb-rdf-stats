# bnb_rdf_stats
A tool to produce various statistics from files of BNB RDF data.

## Requirements

The command-line utility grep (e.g. from https://www.gnu.org/software/grep/) should be present in an executable file-path.

## Installation

From GitHub:

    git clone https://github.com/victoriamorris/bnb_rdf_stats
    cd bnb_rdf_stats

To install as a Python package:

    python setup.py install
    
To create stand-alone executable (.exe) files for individual scripts:

    python setup.py py2exe
    
Executable files will be created in the folder bnb_rdf_stats\dist, and should be copied to an executable path.

## Usage

### Running scripts

The following scripts can be run from anywhere, once the package is installed:

#### bnb_rdf_stats

Produce various statistics from files of BNB RDF data.
    
    Usage: bnb_rdf_stats [OPTIONS]

    Options:
      -c        CONFIG_PATH - Path to config file.
      -o        OUTPUT_PATH - Path to save output file.
      --help    Show help message and exit.
    
    CONFIG_PATH should provide the location of rdf files to be analysed.
    If CONFIG_PATH is not set, the default is bnb_rdf_stats.cfg
    If OUTPUT_PATH is not set, the default is bnb_rdf_stats_<date>.txt

##### Format of config file
The config file specified in CONFIG_PATH must be formatted as in the example below:

    Books: D:\Triples\February2016_Books
    Serials: D:\Triples\February2016_Serials

i.e. with different file types on separate lines. The file type should appear first, followed by a semi-colon, then the path to the folder where the relevant files are located.

##### Statistics produced
The following statistics are included:

  * Total number of files in each folder
  * Total number of RDF triples
  * Number of unique BNB numbers
  * Number of links to Dewey information  
    Indicated by:
      \<http://www.w3.org/2004/02/skos/core#broader> OR \<http://www.w3.org/2002/07/owl#sameAs>
      AND \<http://bnb.data.bl.uk/id/concept/ddc/e2 AND http://dewey.info/class/
  * Number of links to VIAF records for people  
    Indicated by \<http://www.w3.org/2002/07/owl#sameAs> AND \<http://viaf.org/viaf/ AND \<http://bnb.data.bl.uk/id/person/
  * Number of links to VIAF records for organizations  
    Indicated by \<http://www.w3.org/2002/07/owl#sameAs> AND \<http://viaf.org/viaf/ AND \<http://bnb.data.bl.uk/id/organization/
  * Number of links to ISNI records for people  
    Indicated by \<http://www.loc.gov/mads/rdf/v1#isIdentifiedByAuthority> AND \<http://isni.org/isni/ AND \<http://bnb.data.bl.uk/id/person/
  * Number of links to ISNI records for organizations  
    Indicated by \<http://www.loc.gov/mads/rdf/v1#isIdentifiedByAuthority> AND \<http://isni.org/isni/ AND \<http://bnb.data.bl.uk/id/organization/
  * Number of links to LCSH for topics  
    Indicated by \<http://id.loc.gov/authorities/subjects/ AND \<http://bnb.data.bl.uk/id/concept/lcsh/
  * Number of links to LCSH for places  
    Indicated by \<http://id.loc.gov/authorities/subjects/ AND \<http://bnb.data.bl.uk/id/concept/place/lcsh/
