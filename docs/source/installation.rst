Installation
~~~~~~~~~~~~

To install OMTK you will need to clone OMTK and libSerialization Git repositories.

.. note:: 

    In our example, we take in consideration that the installation path is *"~/dev"*.
    If you are on Windows, replace ~/dev by something similar like *"C:/dev/"*

.. warning::
    
    Maya 2017 is not yet supported!

.. code-block:: bash

    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/SqueezeStudioAnimation/omtk.git
    git clone https://github.com/SqueezeStudioAnimation/libSerialization.git

You'll then need to ensure that the omtk and libSerialization path are visible by Python.
This can easily be done by modifying the PYTHONPATH environement variable.
You can also temporary add them to python sys.path.

    >>> import sys
    >>> sys.path.append('~/dev/omtk')
    >>> sys.path.append('~/dev/libSerialization')
    >>> import omtk  # should work!


