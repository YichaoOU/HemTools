All errors and how it was solved
=====================



shell: line 65: source: activate: file not found
^^^^^^^^^^^^^^^^

Likely caused by conda init in your ``.bashrc`` file. Your automatic login looks like ``(base) [yli11@noderome111``, always has the ``base``

open ``.bashrc`` file and delete conda init commands, several lines.


Faster way to grep
^^^^^^^^^^^^

::

	grep -R --include='*log' TERM_MEMLIMIT . > mem.issue




Other python versions are loaded
^^^^^^^^^^^^^^^^^^^^^^^^

::

	Traceback (most recent call last):
	  File "/home/yli11/HemTools/bin/run_lsf.py", line 7, in <module>
	    from utils import *
	  File "/research/rgs01/home/clusterHome/yli11/HemTools/utils/utils.py", line 3, in <module>
	    import matplotlib
	  File "/hpcf/apps/python/install/2.7.13/lib/python2.7/site-packages/matplotlib/__init__.py", line 105, in <module>
	    from matplotlib.externals import six
	  File "/hpcf/apps/python/install/2.7.13/lib/python2.7/site-packages/matplotlib/externals/six.py", line 27, in <module>
	    import operator
	ImportError: /hpcf/apps/python/install/2.7.13/lib/python2.7/lib-dynload/operator.so: undefined symbol: _PyUnicodeUCS4_AsDefaultEncodedString


