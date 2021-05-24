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

my $indexSNPLDFile;
my $sortedBedFile;
my $chrid;
my $SNPInBedFile;
my $logFile;
my $help;

Getopt::Long::GetOptions(
       'indexSNPLDFile=s' => \$indexSNPLDFile,
       'sortedBedFile=s' => \$sortedBedFile,
       'chrid=i' => \$chrid,
       'SNPInBedFile=s' => \$SNPInBedFile,
       'logFile=s' => \$logFile,
       'help' => \$help);

if (defined($help))
{
	print "perl check.index.snp.and.lds.in.bed.pl --indexSNPLDFile indexSNPLDFile --sortedBedFile sortedBedFile --chrid chrid --SNPInBedFile SNPInBedFile --logFile logFile\n";
	print "perl check.index.snp.and.lds.in.bed.pl --help\n";
	
	exit(0);
}

if (!defined($indexSNPLDFile))
{
	print "Please define indexSNPLDFile!\n";

	exit(1);
}
else
{
	if (!(-e $indexSNPLDFile))
	{
		print "$indexSNPLDFile doesn't exist!\n";

		exit(1);
	}
}

if (!defined($sortedBedFile))
{
	print "Please define sortedBedFile!\n";

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

if (!defined($chrid))
{
	print "Please define chrid!\n";

	exit(1);
}
else
{
	if ($chrid !~ /^\d+$/)
	{
		print "$chrid is not a number!\n doesn't exist!\n";

		exit(1);
	}
	else
	{
		if (($chrid < 1)||($chrid > 22))
		{
			print "$chrid should be between 1 and 22!\n";

			exit(1);
		}
	}
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

my $bedObj = new Overlap;

$bedObj->cleanBedObj();

$bedObj->{"chrNo"} = $chrid;
$bedObj->{"bedFile"} = $sortedBedFile;
$bedObj->{"sortedBedFile"} = $sortedBedFile;

$bedObj->checkBedObj();

$bedObj->createBedArrayOnChr();

open (IN,$indexSNPLDFile) || die "can't open the file: $indexSNPLDFile\!n";
open (OUT,">".$SNPInBedFile) || die "can't write to the file: $SNPInBedFile!\n";

my $readline = <IN>;

if ($chrid == 1)
{
	print OUT "indexSNP\tLD\tstart\tend\n";
}

while (defined($readline=<IN>))
{
	chomp $readline;
	my @fields = split(/\t/,$readline);

	my $index = $fields[0];
	my $lds = $fields[1];

	@fields = split(/\:/,$index);
	my $chr = $fields[0];
	my $pos = $fields[1];

	if ($chr =~ /^\d+$/)
	{
		if (($chr > 0)&&($chr < 23))
		{
			if ($chr == $chrid)
			{
#				my ($start,$end) = $bedObj->overlap($chr,$pos);

#				print OUT "$chr:$pos\t$chr:$pos\t$start\t$end\n";

				@fields = split(/\|/,$lds);

				for (my $i = 0; $i < int(@fields); $i++)
				{
					my $ldpos = $fields[$i];

					my ($start,$end) = $bedObj->overlap($chr,$ldpos);

					print OUT "$chr:$pos\t$chr:$ldpos\t$start\t$end\n";
				}
			}
		}
	}
}

close IN;
close OUT;

my $endRunning = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl check.index.snp.and.lds.in.bed.pl --indexSNPLDFile $indexSNPLDFile --sortedBedFile $sortedBedFile --chrid $chrid --SNPInBedFile $SNPInBedFile --logFile $logFile start=$startRunning end=$endRunning runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
