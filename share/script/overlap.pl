#! /usr/bin/perl -w

use strict;
use warnings;
use FindBin qw($Bin);
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $startRunning = time;
my $startTime = [gettimeofday()];

my $indexSNPList;
my $neighborSNPList;
my $chrid;
my $sortedBedFile;
my $resultDIR;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'indexSNPList=s' => \$indexSNPList,
			'neighborSNPList=s' => \$neighborSNPList,
			'chrid=i' => \$chrid,
			'sortedBedFile=s' => \$sortedBedFile,
			'resultDIR=s' => \$resultDIR,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl overlap.pl --indexSNPList indexSNPList --neighborSNPList neighborSNPList --chrid chrid --sortedBedFile sortedBedFile --resultDIR resultDIR --logFile logFile\n";	
	print "perl overlap.pl --help\n";

	exit(0);
}

if (!defined($indexSNPList))
{
	print "Please define indexSNPList!\n";

	exit(1);
}
else
{
	if (!(-e $indexSNPList))
	{
		print "$indexSNPList doesn't exist!\n";

		exit(1);
	}
}

if (!defined($neighborSNPList))
{
	print "Please define neighborSNPList!\n";

	exit(1);
}
else
{
	if (!(-e $neighborSNPList))
	{
		print "$neighborSNPList doesn't exist!\n";

		exit(1);
	}
}

if (!defined($chrid))
{
	print "Please define chrid!\n";

	exit(1);
}
else
{
	if ($chrid !~ /^\d+$/)
	{
		print "chrid is not a number!\n";

		exit(1);
	}
	elsif (($chrid < 1)||($chrid > 22))
	{
		print "chrid should be between 1 to 22!\n";

		exit(1);
	}
}

if (!defined($sortedBedFile))
{
	print "No define $sortedBedFile!\n";

	exit(1);
}
else
{
	if (!(-e $sortedBedFile))
	{
		print "$sortedBedFile doesn't exist!\n";

		exit(1);
	}
}

if (!defined($resultDIR))
{
	print "No define $resultDIR!\n";

	exit(1);
}

if (!defined($logFile))
{
	print "No define $logFile!\n";
	
	exit(1);
}

my ($sec,$min,$hour,$day,$mon,$year,$weekday,$yeardate,$savinglightday) = (localtime(time));
$sec = ($sec < 10)? "0$sec":$sec;
$min = ($min < 10)? "0$min":$min;
$hour = ($hour < 10)? "0$hour":$hour;
$day = ($day < 10)? "0$day":$day;
$mon = ($mon < 9)? "0".($mon+1):($mon+1);
$year += 1900;

my $now = "$year-$mon-$day $hour:$min:$sec";

my $logFileLock = $logFile.".lck";

use lib "$Bin/../lib";

use Overlap;

sub DIRExist
{
	my ($dir) = @_;
	
	`mkdir --p $dir`;
}

my $bedObj = new Overlap;

$bedObj->cleanBedObj();

$bedObj->{"chrNo"} = $chrid;
$bedObj->{"bedFile"} = $sortedBedFile;
$bedObj->{"sortedBedFile"} = $sortedBedFile;

$bedObj->checkBedObj();

$bedObj->createBedArrayOnChr();

if ($resultDIR !~ /\/$/)
{
	$resultDIR = $resultDIR."/";
}

DIRExist($resultDIR);

sub SNPorLDInBed
{
	my ($snp,$LDstr,$chrid) = @_;

	my $inBedPos = -1;
	my $start = -1;
	my $end = -1;

	if ($snp =~ /^chr/i)
	{
		$snp =~ s/^chr//i;
	}

	if ($snp =~ /^(\d+):(\d+)$/)
	{
		my $chr = $1;
		my $pos = $2;

		if ($chr == $chrid)
		{
			($start,$end) = $bedObj->overlap($chr,$pos);

			if (($start != -1)&&($end != -1))
			{
					$inBedPos = $pos;
			}

			if (($start == -1)||($end == -1))
			{
				if ($LDstr ne "NA")
				{
					my @fields = split(/\|/,$LDstr);

					for (my $i = 0; $i < int(@fields); $i++)
					{
						my $ldpos = $fields[$i];

						($start,$end) = $bedObj->overlap($chr,$ldpos);

						if (($start != -1)&&($end != -1))
						{
								$inBedPos = $ldpos;

								$i = int(@fields);
						}
					}
				}
			}
		}
	}

	return ($inBedPos,$start,$end);
}

# Create index SNP on chrid in bed file
my $indexSNPInBedFile = $resultDIR."index.snp.LD.on.chr$chrid.in.bed.txt";

open (IN,$indexSNPList) || die "can't open the file $indexSNPList!\n";
open (OUT,">".$indexSNPInBedFile) || die "can't write to the file $indexSNPInBedFile!\n";

my $readline = <IN>;
chomp $readline;

print OUT "$readline\tinBedPos\tstart\tend\n";

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);

	my $indexSNP = $fields[0];
	my $LDs = $fields[1];

	my ($posInBed,$start,$end) = SNPorLDInBed($indexSNP,$LDs,$chrid);

	if (($indexSNP eq "3:156797609")&&($chrid == 3))
	{
#		print "indexSNP = $indexSNP\tLDs = $LDs\tposInBed = $posInBed\tstart = $start\tend = $end\n";
	}

	if (($posInBed != -1)&&($start != -1)&&($end != -1))
	{
		print OUT "$readline\t$posInBed\t$start\t$end\n";
	}
}

close IN;
close OUT;

# Create neighbor SNPs on chrid in bed file
my $neighborSNPInBedFile = $resultDIR."neighbor.on.chr$chrid.LDbuddy.in.bed.txt";

open (IN,$neighborSNPList) || die "can't open the file $neighborSNPList!\n";
open (OUT,">".$neighborSNPInBedFile) || die "can't write to the file $neighborSNPInBedFile!\n";

$readline = <IN>;
chomp $readline;

print OUT "$readline\tinBedPos\tstart\tend\n";

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);
	my $neighborSNP = $fields[0];
	my $LDs = $fields[1];

	my ($posInBed,$start,$end) = SNPorLDInBed($neighborSNP,$LDs,$chrid);

	if (($posInBed != -1)&&($start != -1)&&($end != -1))
	{
		print OUT "$readline\t$posInBed\t$start\t$end\n";
	}
}

close IN;
close OUT;

my $endRunning = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl overlap.pl --indexSNPList $indexSNPList --neighborSNPList $neighborSNPList --chrid $chrid --sortedBedFile $sortedBedFile --resultDIR $resultDIR --logFile $logFile start=$startRunning end=$endRunning runningTime=$runningTime\n";	

close OUT;

close(SEM);

exit(0);
