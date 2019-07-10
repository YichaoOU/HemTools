How to download folders in sourceforge
======================================



go to a folder webpage in sourceforge, click on the RSS button, replace the ``URL`` with the RSS url in your browser, and run the command below.


.. code:: bash

	curl URL | grep "<link>.*</link>" | sed 's|<link>||;s|</link>||' | while read url; do url=`echo $url | sed 's|/download$||'`; wget $url ; done



