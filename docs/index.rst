
.. raw:: html

    <style> .salmon {color:IndianRed; font-weight:bold; font-size:48px} </style>

.. role:: salmon

.. raw:: html

    <style> .bgblue {background-color:LightBlue; width:100px} </style>

.. role:: bgblue


:salmon:`Autofile`

*A Package of the AutoMech Suite*

Andreas V. Copan, Kevin B. Moore III, Sarah N. Elliott, and Stephen J. Klippenstein

--------------------------------------------------------------------------------------

.. toctree::
    :glob:
    :maxdepth: 1

    index
--------------------------------------------------------------------------------------

Overview
~~~~~~~~

Autofile directs the filesystem framework for the AutoMech suite.  It uses a dual architecture: the run/save filesystems. 
Under each, Autofile defines rigid Dataseries trunks, branches, and leaves that each can stores specific data.

.. image:: autofile.png
  :width: 800


Getting Started
~~~~~~~~~~~~~~~
Installation
^^^^^^^^^^^^^
.. code-block:: python

    >>> conda install autofile -c auto-mech


Tutorial
^^^^^^^^
The first step is to make sure the installation was successful by importing autofile

.. code-block:: python

    >>> import autofile


Then we can move on to using the autofile module:

* Species filesystem\: :ref:`spc-tutorial-doc`
* Theory filesystem\: :ref:`thy-tutorial-doc`
* Conformer filesystem\: :ref:`cnf-tutorial-doc`
* Z-matrix filesystem\: :ref:`zmat-tutorial-doc`
* Scan filesystem\: :ref:`scn-tutorial-doc`
* Reaction filesystem\: :ref:`rxn-tutorial-doc`
* TS filesystem\: :ref:`ts-tutorial-doc`


Documentation
~~~~~~~~~~~~~
    .. toctree::
        :maxdepth: 4
    
        submodule_fs
        submodule_model
        submodule_schema
        submodule_data_types
        submodule_info
        submodule_io
        submodule_json


