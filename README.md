# Autofile
[//]: # (Badges)
[![CircleCI](https://circleci.com/gh/snelliott/autofile/tree/dev.svg?style=shield)](https://circleci.com/gh/snelliott/autofile/tree/dev)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autofile/badges/version.svg)](https://anaconda.org/auto-mech/autofile)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autofile/badges/platforms.svg)](https://anaconda.org/auto-mech/autofile)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autofile/badges/installer/conda.svg)](https://conda.anaconda.org/auto-mech/autofile)

Andreas V. Copan, Kevin B. Moore III, Sarah N. Elliott, and Stephen J. Klippenstein

File system schema and interface for AutoMech

## Filesystem Description
The dual run/save filesystem is designed to distinguish species by their inchi, multiplicity, and charge. Similarly it houses unique transition states by the inchi, multipliciy, and charge of the reactants and products for the reaction that passes through it.  Each of these branches will further branch off into theory specifiers and then into specific types of tasks (single points, projections, etc). 
![alt text](https://github.com/snelliott/autofile/blob/dev/docs/autofile.png?raw=true)
