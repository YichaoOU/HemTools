Remove <U+FEFF> character in your file
=============

Sometimes you will see "<U+FEFF>" when your open a file. Here is how to remove it.

Ref: https://gist.github.com/szydan/b225749445b3602083ed


::

	vim your_file

	type SHIFT + ;

	type set nobomb

	type SHIFT + ;

	type wq

