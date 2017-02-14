#!/usr/bin/env python
# -*- coding: utf8 -*-

"""A tool to produce various statistics from files of BNB RDF data."""

# Import required modules
# These should all be contained in the standard library
import datetime
import gc
import getopt
import locale
import os
import re
import subprocess
import sys

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'

# Set locale to assist with sorting
locale.setlocale(locale.LC_ALL, '')

# Set threshold for garbage collection (helps prevent the program run out of memory)
gc.set_threshold(300, 3, 3)

# ====================
#  Regular expressions
# ====================

RE_ALEPH_SYS_NO = re.compile('^.*<http://bnb.data.bl.uk/id/resource/([0-9]{9})>.*$', flags=re.DOTALL | re.IGNORECASE)


# ====================
#       Classes
# ====================


class Counters:
    """Class for counting the number of lines within a file having particular properties."""
    
    def __init__(self):
        self.c = {
            'RDF':  0,
            'BNB': 0,
            'Dewey': 0,
            'VIAFPers': 0,
            'VIAFOrg': 0,
            'ISNIPers': 0,
            'ISNIOrg': 0,
            'LCSHTopic': 0,
            'LCSHPlace': 0,
        }

# ====================
#      Functions
# ====================


def exit_prompt(message=''):
    """Function to exit the program after prompting the use to press Enter"""
    if message != '':
        print(str(message))
    input('\nPress [Enter] to exit...')
    sys.exit()


def file_len(filename):
    """Function to get the number of lines in a file
    Returns 1 less than number of lines, but last line is usually blank in this application"""
    i = 0
    with open(filename, mode='r', encoding='utf-8', errors='replace') as f:
        for i, l in enumerate(f): pass
    return i


def check_file_location(file_path, function, file_ext='', exists=False):
    """Function to check whether a file exists and has the correct file extension."""
    folder, file, ext = '', '', ''
    if file_path == '':
        exit_prompt('Error: Could not parse path to {} file'.format(function))
    try:
        file, ext = os.path.splitext(os.path.basename(file_path))
        folder = os.path.dirname(file_path)
    except:
        exit_prompt('Error: Could not parse path to {} file'.format(function))
    if file_ext != '' and ext != file_ext:
        exit_prompt('Error: The specified file should have the extension {}'.format(file_ext))
    if exists and not os.path.isfile(os.path.join(folder, file + ext)):
        exit_prompt('Error: The specified {} file cannot be found'.format(function))
    return folder, file, ext


def usage():
    """Function to print information about the script"""
    print('Correct syntax is:')
    print('bnb_rdf_stats [OPTIONS]')
    print('\nOptions:')
    print('    -c       CONFIG_PATH - Path to config file.')
    print('    -o       OUTPUT_PATH - Path to save output file.')
    print('    --help   Display this help message and exit.')
    print('\nCONFIG_PATH should provide the location of rdf files to be analysed.')
    print('If CONFIG_PATH is not set, the default is bnb_rdf_stats.cfg')
    print('If OUTPUT_PATH is not set, the default is bnb_rdf_stats_<date>.txt')
    print('\n\nCommand-line utility grep should be present in an executable file-path.')
    exit_prompt()

# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    config_path, output_path = '', ''
    i = datetime.datetime.now()

    print('========================================')
    print('bnb_rdf_stats')
    print('========================================')
    print('A tool to produce various statistics from files of BNB RDF data\n')

    try:
        opts, args = getopt.getopt(argv, 'c:o:', ['config_path=', 'output_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help':
            usage()
        elif opt in ['-c', '--config_path']:
            config_path = arg
        elif opt in ['-o', '--output_path']:
            output_path = arg
        else: exit_prompt('Error: Option {} not recognised'.format(opt))

    # Check file locations
    if config_path == '':
        config_path = 'bnb_rdf_stats.cfg'
    config_folder, config_file, config_ext = check_file_location(config_path, 'config file', '.cfg', True)
    if output_path != '':
        output_folder, output_file, output_ext = check_file_location(output_path, 'output file', '.txt', False)
    else:
        output_folder, output_file, output_ext = '', 'bnb_rdf_stats_{}'.format(str(i.strftime('%Y-%m-%d'))), '.txt'

    try: subprocess.call('grep --help 1>nul', shell=True)
    except: exit_prompt('Error: Command-line utility grep should be present in an executable file-path')

    # --------------------
    # Config file found => try reading
    # --------------------

    print('\nReading config file ...')
    print('----------------------------------------')
    print(str(datetime.datetime.now()))

    a = {}

    cfile = open(os.path.join(config_folder, config_file + config_ext), mode='r', encoding='utf-8', errors='replace')
    for filelineno, line in enumerate(cfile):
        if ':' in line:
            filetype, d = line.strip().split(':', 1)[0].strip(), line.strip().split(':', 1)[1].strip()
            if filetype != '' and os.path.isdir(d):
                a[filetype] = d
            else:
                print('The specified {} directory could not be found'.format(filetype))
    cfile.close()

    # Create stats file to write to
    ofile = open(os.path.join(output_folder, output_file + output_ext), mode='w', encoding='utf-8', errors='replace')
    ofile.write('Statistics for BNB RDF data\n')     
    ofile.write(str(i.strftime('%Y-%m-%d %H:%M:%S')) + '\n\n')
    ofile.write('==============================')

    for filetype, d in a.items():
        print('\nReading files in the {} directory ...'.format(filetype))
        print('----------------------------------------')
        print(str(datetime.datetime.now()))
        print(str(d) + '\n')
        i = 0
        counters = Counters()

        # Remove temporary files for storing matches
        for f in ['ids', 'links']:
            if os.path.isfile(f): os.remove(f)
        
        for (dirname, dirs, files) in os.walk(d):
            for filename in files:
                if filename.endswith('.nt'):
                    i += 1
                    print('Reading from file ' + str(filename))
                    try: counters.c['RDF'] += file_len(os.path.join(dirname, filename))
                    except: print('\nError: {0}\n'.format(str(sys.exc_info())))
                    subprocess.call('grep "<http://www.bl.uk/schemas/bibliographic/blterms#bnb>" "' 
                                    + str(os.path.join(dirname, filename)) + '" >>ids', shell=True)
                    subprocess.call('grep "http://www.w3.org/2004/02/skos/core#broader" "' 
                                    + str(os.path.join(dirname, filename)) + '" >>links', shell=True)
                    subprocess.call('grep "http://www.w3.org/2002/07/owl#sameAs" "' 
                                    + str(os.path.join(dirname, filename)) + '" >>links', shell=True)
                    subprocess.call('grep "http://www.loc.gov/mads/rdf/v1#isIdentifiedByAuthority" "' 
                                    + str(os.path.join(dirname, filename)) + '" >>links', shell=True)

        print('\nCounting BNB numbers ...')
        counters.c['BNB'] = file_len('ids') + 1
        print('{} BNB numbers found'.format(str(counters.c['BNB'])))
        
        with open('links', mode='r', encoding='utf-8', errors='replace') as f:
            print('\nCounting links ...')
            for line in f:
                if ('<http://www.w3.org/2004/02/skos/core#broader>' in line
                    or '<http://www.w3.org/2002/07/owl#sameAs>' in line) \
                   and '<http://bnb.data.bl.uk/id/concept/ddc/e2' in line \
                   and 'http://dewey.info/class/' in line:
                    counters.c['Dewey'] += 1
                elif '<http://www.w3.org/2002/07/owl#sameAs>' in line:
                    if '<http://viaf.org/viaf/' in line:
                        if '<http://bnb.data.bl.uk/id/person/' in line:
                            counters.c['VIAFPers'] += 1
                        elif '<http://bnb.data.bl.uk/id/organization/' in line:
                            counters.c['VIAFOrg'] += 1
                    elif '<http://id.loc.gov/authorities/subjects/' in line:
                        if '<http://bnb.data.bl.uk/id/concept/lcsh/' in line:
                            counters.c['LCSHTopic'] += 1
                        elif '<http://bnb.data.bl.uk/id/concept/place/lcsh/' in line:
                            counters.c['LCSHPlace'] += 1
                elif '<http://www.loc.gov/mads/rdf/v1#isIdentifiedByAuthority>' in line \
                     and '<http://isni.org/isni/' in line:
                    if '<http://bnb.data.bl.uk/id/person/' in line:
                        counters.c['ISNIPers'] += 1
                    elif '<http://bnb.data.bl.uk/id/organization/' in line:
                        counters.c['ISNIOrg'] += 1

        print('There are {} .nt files in the {} directory'.format(str(i), filetype))
        # Write stats to output file
        ofile.write('\n\nStats for {}:\n'.format(filetype))
        ofile.write('Books directory: {}\n'.format(str(dir)))
        ofile.write('Number of files: {}\n'.format(str(i)))
        ofile.write('{}\t RDF triples\n'.format(str(counters.c['RDF'])))
        ofile.write('{}\t BNB numbers\n'.format(str(counters.c['BNB'])))
        ofile.write('{}\t links to Dewey info\n'.format(str(counters.c['Dewey'])))
        ofile.write('{}\t links to VIAF records for people\n'.format(str(counters.c['VIAFPers'])))
        ofile.write('{}\t links to VIAF records for organizations\n'.format(str(counters.c['VIAFOrg'])))
        ofile.write('{}\t links to ISNI records for people\n'.format(str(counters.c['ISNIPers'])))
        ofile.write('{}\t links to ISNI records for organizations\n'.format(str(counters.c['ISNIOrg'])))
        ofile.write('{}\t links to LCSH for topics\n'.format(str(counters.c['LCSHTopic'])))
        ofile.write('{}\t links to LCSH for places\n'.format(str(counters.c['LCSHPlace'])))

    ofile.close()
    # Remove temporary files for storing matches
    for f in ['ids', 'links']:
        if os.path.isfile(f): os.remove(f)

    print('\n\nAll processing complete')
    print('----------------------------------------')
    print(str(datetime.datetime.now()))
    input('\nPress [Enter] to exit...')
    sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
