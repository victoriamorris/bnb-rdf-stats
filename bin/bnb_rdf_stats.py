#!/usr/bin/env python
# -*- coding: utf8 -*-

"""A tool to produce various statistics from files of BNB RDF data."""

import bnb_rdf_stats
import sys

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'

bnb_rdf_stats.main(sys.argv[1:])
