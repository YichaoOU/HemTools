Bioinformatics Data Organization Guidelines
===========================================


Purpose
^^^^^^^

The purpose of these guidelines is (1) to help you organize your working directory so that it is well structured and can be easilly understood by other people; (2) to help you hand over a project better. There is no doubt that you can finish small projects without attention to these guidelines. But, keep in mind that you are likely going to give these projects to someone else in the future or re-check something in your old analyses, in those cases, it will be much efficient with these guidelines.


Suppose you do all work in working dir, process raw data and generate data, as usual.

The next thing to do is to create the following dirs.

project dir
- raw_data 
	if there is a centralized place, use softlinks
- processed_data
	you can create different kind of subdirs, e.g., bam_files
	use softlinks from working dir
- scripts
- working dir
	this folder can look messy
- readme.md
- history.txt


.. bash:

	

Reference
^^^^^^^^^

http://oucsace.cs.ohio.edu/~chelberg/classes/361/style-guide.html




