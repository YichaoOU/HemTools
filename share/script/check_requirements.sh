#!/bin/bash
#
#   Check the system for files needed by GREGOR
#
#   Usgae:   check_requirements.sh
#
#

DIR=$PWD

EXAMPLE=$DIR/../example

banner="#============================================================"

#================================================================
#   Check on Redhat or CentOS systems
#================================================================
if [ ! -d /etc/apt ]; then
    echo $banner
    echo "#   We are not ready for non-Debian systems"
    echo $banner
    exit 1
else
		echo "Good, you are in Debian system"
fi

#================================================================
#   Check on Debian systems
#================================================================
inst='sudo apt-get install'

#   Sanity checks
t=`which perl`
if [ "$t" = "" ]; then
  echo $banner
  echo "#   'perl' is not installed, do go to 'www.perl.org' to download and install perl on your system"
  echo $banner
	exit 1
else
  echo "Good, you appear to have 'perl' installed"
fi

t=`which make`
if [ "$t" = "" ]; then
  echo $banner
  echo "#   'make' is not installed, do '$inst make'"
  echo $banner
	exit 1
else
  echo "Good, you appear to have 'make' installed"
fi

t=`which sqlite3`
if [ "$t" = "" ]; then
	echo $banner
	echo "#   'sqlite3' is not installed, do go to 'www.sqlite.org' to download and install sqlite3 on your system"
	echo $banner
	exit 1
else
	echo "Good, you appear to have 'sqlite3' installed"
fi

t=`sqlite3 --version`
ARR=($t)
version=$ARR
OLD_IFS="$IFS"
IFS="."
ARR=($version)
IFS="$OLD_IFS"

if [ ${ARR[0]} -lt 3 ]; then
	echo $banner
	echo "#   The version of sqlite3 on your system is older than 3.7.9. We strong suggest you upgrade the sqlite3 before running GREGOR"
	echo $banner
	exit 1
else
	if [ ${ARR[1]} -lt 7 ]; then
		echo $banner
		echo "#   The version of sqlite3 on your system is older than 3.7.9. We strong suggest you upgrade the sqlite3 before running GREGOR"
		echo $banner
		exit 1
	else
		if [ ${ARR[2]} -lt 9 ]; then
			echo $banner
			echo "#   The version of sqlite3 on your system is older than 3.7.9. We strong suggest you upgrade the sqlite3 before running GREGOR"
			echo $banner
			exit 1
		else
			echo "Good, you appear the have right version of sqlite3"
		fi
	fi
fi

if [ -d $EXAMPLE ]; then
  echo "Good, you appear to have 'GREGOR-example' installed"
  echo "Test this example:  perl $DIR/GREGOR.pl --conf $EXAMPLE/example.conf"
else
  echo $banner
  echo "#   '$DIR/example' does not exist so you cannot do example demo test in this install"
  echo $banner
	exit 1
fi

exit
