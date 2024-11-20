
.. yamcs_flatsat_utils documentation main file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to yamcs_flatsat_utils's documentation!
========================================================================================

Dev Guide - Getting Started
---------------------------

Before installing any dependencies or writing code, it's a great idea to create a
virtual environment. LINCC-Frameworks engineers primarily use `conda` to manage virtual
environments. If you have conda installed locally, you can run the following to
create and activate a new environment.

.. code-block:: console

   >> conda create env -n <env_name> python=3.12
   >> conda activate <env_name>


Once you have created a new environment, you can install this project for local
development using the following commands:

.. code-block:: console

   >> pip install -e .'[dev]'
   >> pre-commit install
   >> conda install pandoc


Notes:

1) The single quotes around ``'[dev]'`` may not be required for your operating system.
2) ``pre-commit install`` will initialize pre-commit for this local repository, so
   that a set of tests will be run prior to completing a local commit. For more
   information, see the Python Project Template documentation on
   `pre-commit <https://lincc-ppt.readthedocs.io/en/latest/practices/precommit.html>`_.
3) Installing ``pandoc`` allows you to verify that automatic rendering of Jupyter notebooks
   into documentation for ReadTheDocs works as expected. For more information, see
   the Python Project Template documentation on
   `Sphinx and Python Notebooks <https://lincc-ppt.readthedocs.io/en/latest/practices/sphinx.html#python-notebooks>`_.

.. toctree::
   :hidden:

   Home page <self>
   API Reference <autoapi/index>

.. toctree::
   :maxdepth: 1
   :caption: Yamcs
   :hidden:

   Yamcs-Quickstart-Interface </yamcs/Quickstar-yamcs-interface>
   Yamcs-IO-Interface </yamcs/yamcs-interface>
   Yamcs-Client </yamcs/yamcs-client>

.. toctree::
   :maxdepth: 1
   :caption: How To
   :hidden:

   How To - Manage Issue Reports </HowTo/HowToIssueProcess>
   How To - OBC software </HowTo/Obc_software_installations>
   How To - Skylab GUI </HowTo/HowToSkyEGSE>
   How To - SSH Connection to FlatSat PC </HowTo/HowToSshFlatSatPC>

.. toctree::
  :maxdepth: 1
  :caption: Learning
  :hidden:

  Template "How to" </learning/template>
  Ressources </learning/ressources>
