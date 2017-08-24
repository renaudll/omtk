.. omtk documentation master file, created by
   sphinx-quickstart2 on Mon Nov 21 21:57:37 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to omtk's documentation!
================================

OMTK (Open Maya Toolkit) is a generic modular autorig for Maya that relly heavily on metadata for storing informations about the generated rig. This allow any part of the rig to be unbuilt and rebuilt at ease without loss of information. This is usefull for productions that need lots of iterations where rebuilding or modifying the rig can have drastic effect on the roadmap.

Like any other modular Autorig, OMTK rely on 'modules'.
Modules can be used inside other modules which can fake encapsulation, a feature that is greatly missing in Maya. 

Contents:

.. toctree::
   :maxdepth: 3

   installation
   development
   class_nomenclature
   glossary
   component_registration

.. automodule:: omtk.modules.rigIK


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

