#! /usr/bin/perl -w

############################################################################
##
##  CopyRight (c) 2011 Regents of the University of Michigan
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
############################################################################

use strict;
use warnings;
use Getopt::Long;
use FindBin qw($Bin);
use threads;
use threads::shared;

my $startTime = timePoint();;
			
my %hConf;

#############################################################################
## loadConf() : load configuration file and build hash table for configuration
## CopyRight of this subroutine belongs to Hyun Min Kang
#############################################################################
sub loadConf
{
	my $conf = shift;
	
	%hConf = ();
	open(IN,$conf) || die "Cannot open $conf file for reading";
	while(<IN>)
	{
		next if ( /^#/ );  # if the line starts with #, regard them as comment line
		s/#.*$//;          # trim in-line comment lines starting with #
		my ($key,$val);
		if ( /^([^=]+)=(.+)$/ )
		{
			($key,$val) = ($1,$2);
		}
		else
		{
			die "Cannot parse line $_ at line $. in $conf\n";
		}
		
		$key =~ s/^\s+//;  # remove leading whitespaces
		$key =~ s/\s+$//;  # remove trailing whitespaces
		
		if ( !defined($val) )
		{
			$val = "";     # if value is undefined, set it as empty string
		}
		else
		{
			$val =~ s/^\s+//;
			$val =~ s/\s+$//;
		}
		
		# check if predefined key exist and substitute it if needed
		while ( $val =~ /\$\((\S+)\)/ )
		{
			my $subkey = $1;
			my $subval = &getConf($subkey);
			if ($subval eq "")
			{
				die "Cannot parse configuration value $val at line $. of $conf\n";
			}
			$val =~ s/\$\($subkey\)/$subval/;
		}
		$hConf{$key} = $val;
	}
}

my $conf = "";

my $optResult = GetOptions("conf=s",\$conf);

my $usage = <<END;
----------------------------------------------------------------------------------
GREGOR.pl : Functional annotation of trait-associated variants
----------------------------------------------------------------------------------
This program tests for enrichment of an input list of trait-associated index
SNPs ([chr:pos] format or rsID, hg19) in experimentally annotated regulatory 
domains (BED files).

Note: the index SNPs should be hg19 version. All maf and LD data are from 1000G
EUR samples! (Release date : May 21, 2011)

Version : 1.3.1

Report Bug(s) : jich[at]umich[dot]edu
----------------------------------------------------------------------------------
Usage : perl GREGOR.pl --conf [conf.file]
----------------------------------------------------------------------------------
END

unless (($optResult)&&($conf))
{
	die "$usage\n";
}

if (!(-e $conf))
{
	print "can't find the file: $conf!\n";

	exit(1);
}

loadConf($conf);

print "--------------------------------------------------------------------------------------------------------\n";
print "Please check your parameters :\n\n";
while (my ($k,$v) = each %hConf)
{
	print "$k\t$v\n";
}
print "--------------------------------------------------------------------------------------------------------\n\n";

use lib "$Bin/../lib";

use GREGOR;

my $GREGORInstance = new GREGOR;

# Read all configurations to hash. $self->{"conf"}
$GREGORInstance->ReadConf(%hConf);

# Read reference LD Buddy threshold
$GREGORInstance->ReadReferenceLDBuddyThreshold();

# Verify all parameters in config file
$GREGORInstance->VerifyConf();

# Verify all bed files
$GREGORInstance->CheckBedFiles();

# Verify index SNPs
$GREGORInstance->CheckSNPList();

#Create result directories
$GREGORInstance->CreateAllDIR();

# Create and run make files
$GREGORInstance->CreateMakeFile();

print "Running ... ...\n";
print "You can check the status in the log file: ".$GREGORInstance->{"conf"}->{"OUT_DIR"}."GREGOR.log\n\n";

my $jobs = $GREGORInstance->{"conf"}->{"JOBNUMBER"};
my $makeFile = $GREGORInstance->{"conf"}->{"OUT_DIR"}."MakeFile";
my $topNBed = $GREGORInstance->{"conf"}->{"TOPNBEDFILES"};

if (!(defined($topNBed)))
{
	$topNBed = 0;
}

my $thread_num : shared = 0;

my $logFile = $GREGORInstance->{"conf"}->{"OUT_DIR"}."GREGOR.log";
my $totalTaskes = `grep touch $makeFile | wc -l`;
$totalTaskes = $totalTaskes + $topNBed * 22 + 1;

=pod
my $thread = threads->create(\&progressBar,$logFile,$totalTaskes);
$thread_num ++;
$thread->detach();

$thread = threads->create(\&runMakeFile,$makeFile,$jobs);
$thread_num ++;
$thread->detach();
=cut

`make -f $makeFile -j$jobs`;

=pod
while ($thread_num > 1)
{
	sleep(5);
}
=cut

if ($topNBed > 0)
{
	$GREGORInstance->CreateTopNBedMakeFile();

	$makeFile = $GREGORInstance->{"conf"}->{"OUT_DIR"}."TopNBed.MakeFile";

	`make -f $makeFile -j$jobs`;

=pod
	$thread = threads->create(\&runMakeFile,$makeFile,$jobs);
	$thread_num ++;
	$thread->detach();
=cut
}

=pod
while ($thread_num > 1)
{
	sleep(5);
}

print "\r $totalTaskes / $totalTaskes (100%)\n";
=cut

my $endTime = timePoint();

print "start at $startTime; finish at $endTime\n";

sub runMakeFile
{
	my ($thisMakeFile,$thisJobs) = @_;

	`make -f $thisMakeFile -j$thisJobs`;

	$thread_num --;

	return 1;
}

sub progressBar
{
	my ($log,$taskes) = @_;

	my $n = 0;

	while ($thread_num >= 1)
	{
		local $| = 1;
	
		my @progress_symbol = ('-','\\','|','/');

		my $lines = 0;

		if (-e $log)
		{
			$lines = `wc -l $log`;
			my @fields = split(/\ /,$lines);
			$lines = $fields[0];
		}

		my $percent = $lines / $taskes;
		$percent = int($percent * 100);

		print "\r $progress_symbol[$n] $lines / $taskes ($percent%)";
		
		$n = ($n>=3)? 0:$n+1;
		
		select(undef, undef, undef, 0.1); # sleep 0.2 sec
	
		local $| = 0;
	}

	local $| = 0;

	print "\r\n";

	$thread_num --;

	return 1;
}

sub	timePoint
{
	my ($sec,$min,$hour,$day,$mon,$year,$weekday,$yeardate,$savinglightday) = (localtime(time));
	
	$sec = ($sec < 10)? "0$sec":$sec;
	$min = ($min < 10)? "0$min":$min;
	$hour = ($hour < 10)? "0$hour":$hour;
	$day = ($day < 10)? "0$day":$day;
	$mon = ($mon < 9)? "0".($mon+1):($mon+1);
	$year += 1900;
	
	my $time = "$year-$mon-$day $hour:$min:$sec";

	return ($time);
}

exit(0);
