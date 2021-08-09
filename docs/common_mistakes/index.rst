Common errors and mistakes for using HemTools
=========

.. toctree::
   :maxdepth: 1
   :glob:

   *

Most of the errors and mistakes listed here are not HemTools-specific, rather, these are general mistakes due to file types and/or noisy input (noisy input may lead to noisy output or simply no output).

The MOST MOST MOST common error is that you are running HemTools in a login node (e.g. ``splprhpc05`` or ``splprhpc06``). Please do ``hpcf_interactive``. our HPC allows maximal two interative jobs, if you ``hpcf_interactive`` is ``pending`` for more than 1 minute, it's likely that you already have two interative jobs. You can close all your terminals and start over.
