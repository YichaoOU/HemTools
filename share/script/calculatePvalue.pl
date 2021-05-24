#! /usr/bin/perl -w

use strict;
use warnings;
use FindBin qw($Bin);
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $bedFilesDIR;
my $neighborFile;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'bedFilesDIR=s' => \$bedFilesDIR,
			'neighborFile=s' => \$neighborFile,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl calculatePvalue.pl --bedFilesDIR bedFilesDIR --neighborFile neighborFile --logFile logFile\n";	
	print "perl calculatePvalue.pl --help\n";

	exit(0);
}

if (!defined($bedFilesDIR))
{
	print "Please define bedFilesDIR!\n";

	exit(1);
}

if (!(-e $bedFilesDIR))
{
	print "$bedFilesDIR doesn't exist!\n";

	exit(1);
}

if (!defined($neighborFile))
{
	print "Please define neighborFile!\n";

	exit(1);
}

if (!(-e $neighborFile))
{
	print "$neighborFile doesn't exist!\n";

	exit(1);
}

if (!defined($logFile))
{
	print "Please define logFile!\n";
	
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

if ($bedFilesDIR !~ /\/$/)
{
	$bedFilesDIR = $bedFilesDIR."/";
}

## Read inBed index SNP
my %inBedSNPHash;
undef %inBedSNPHash;

for (my $i = 1; $i < 23; $i++)
{
	my $infile = $bedFilesDIR."index.snp.LD.on.chr$i.in.bed.txt";

	open (IN,$infile) || die "can't open the file $infile!\n";

	my $readline = <IN>;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		my @fields = split(/\t/,$readline);
		my $snp = $fields[0];

		$inBedSNPHash{$snp} = 1;
	}

	close IN;
}

## Read inBed neighbor SNP
for (my $i = 1; $i < 23; $i++)
{
	my $infile = $bedFilesDIR."neighbor.on.chr$i.LDbuddy.in.bed.txt";

	open (IN,$infile) || die "can't open the file $infile!\n";

	my $readline = <IN>;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		my @fields = split(/\t/,$readline);
		my $neighbor = $fields[0];

		$inBedSNPHash{$neighbor} = 1;
	}

	close IN;
}

use lib "$Bin/../lib";

use BinomialRandomDistribution;
my $BinomialRandomDistributionObj = new BinomialRandomDistribution;

## Read neighborhood of index SNPs
open (IN,$neighborFile) || die "can't open the file $neighborFile!\n";

my $totalIndexSNPNum = 0;
my $totalIndexSNPInBedNum = 0;
my $k = 0;

my $readline = <IN>;

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);
	my $indexSNPNum = $fields[0];
	my $indexSNPs = $fields[1];
	my $neighbors = $fields[5];

	my $indexSNPInBedNum = 0;
	my $neighborSNPInBedNum = 0;

	@fields = split(/\|/,$indexSNPs);
	for (my $i = 0; $i < int(@fields); $i++)
	{
		my $index = $fields[$i];

		if (exists($inBedSNPHash{$index}))
		{
			$indexSNPInBedNum = $indexSNPInBedNum + 1;
		}
	}

	@fields = split(/\|/,$neighbors);
	my $neighborSNPNum = int(@fields);
	for (my $i = 0; $i < $neighborSNPNum; $i++)
	{
		my $neighbor = $fields[$i];

		if (exists($inBedSNPHash{$neighbor}))
		{
			$neighborSNPInBedNum = $neighborSNPInBedNum + 1;
		}
	}

	$BinomialRandomDistributionObj->{"s"}[$k] = $indexSNPNum;
	$BinomialRandomDistributionObj->{"p"}[$k] = $neighborSNPInBedNum / $neighborSNPNum;

	$totalIndexSNPNum = $totalIndexSNPNum + $indexSNPNum;
	$totalIndexSNPInBedNum = $totalIndexSNPInBedNum + $indexSNPInBedNum;

	$k = $k + 1;
}

close IN;

$BinomialRandomDistributionObj->{"k"} = $totalIndexSNPInBedNum;

## Write to neighbor hood file 
my $neighborhoodFile = $bedFilesDIR."neighborhoodFile.txt";
$BinomialRandomDistributionObj->{"neighborhoodFile"} = $neighborhoodFile;

open (OUT,">".$neighborhoodFile) || die "can't write to the file $neighborhoodFile!\n";

print OUT $BinomialRandomDistributionObj->{"k"}."\n";

for (my $i = 0; $i < int(@{$BinomialRandomDistributionObj->{"s"}}); $i++)
{
	print OUT $BinomialRandomDistributionObj->{"s"}[$i]."\t";
	print OUT $BinomialRandomDistributionObj->{"p"}[$i]."\n";
}

close OUT;

$BinomialRandomDistributionObj->calculatePValue();

my $result = $bedFilesDIR."PValue.txt";
$BinomialRandomDistributionObj->{"pValueFile"} = $result;
$BinomialRandomDistributionObj->writeToFile();

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl calculatePvalue.pl --bedFilesDIR $bedFilesDIR --neighborFile $neighborFile --logFile $logFile start=$start end=$end runningTime=$runningTime\n";	

close OUT;

close(SEM);

exit(0);
