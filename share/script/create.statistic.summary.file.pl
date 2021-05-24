#! /usr/bin/perl -w

use strict;
use warnings;
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $statisticSummaryFile;
my $resultDIR;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'statisticSummaryFile=s' => \$statisticSummaryFile,
			'resultDIR=s' => \$resultDIR,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl create.statistic.summary.file.pl --statisticSummaryFile statisticSummaryFile --resultDIR resultDIR --logFile logFile\n";
	print "perl create.statistic.summary.file.pl --help\n";

	exit(0);
}

if (!defined($statisticSummaryFile))
{
	print "No define statisticSummaryFile!\n";

	exit(1);
}

if (!defined($resultDIR))
{
	print "No define resultDIR!\n";

	exit(1);
}
else
{
	if (!(-e $resultDIR))
	{
		print "$resultDIR doesn't exist!\n";

		exit(1);
	}
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

my $cmd = `find $resultDIR -name "PValue.txt"`;

my @files = split(/\n/,$cmd);
my @bedFiles;
undef @bedFiles;

for (my $i = 0; $i < int(@files); $i++)
{
	my $bedFile = $files[$i];

	my @fields = split(/\//,$files[$i]);

	my $k = int(@fields) - 2;

	$bedFiles[$i] = $fields[$k];
}

open (OUT,">".$statisticSummaryFile) || die "can't write to the file $statisticSummaryFile!\n";

#print OUT "Bed_File\tInBed_Index_SNP\tAvg_InBed_RandomSNP\tMoreThanIndexSNP\tPermutation\tObserved_PValue\tEstimate_PValue\tStandard_Err\n";
print OUT "Bed_File\tInBed_Index_SNP\tExpectNum_of_InBed_SNP\tPValue\n";

for (my $i = 0; $i < int(@files); $i++)
{
	open (IN,$files[$i]) || die "can't open the file $files[$i]!\n";

	my $readline;

	my $inBedIndexSNPNum = "NA";
	my $expectedNumInBedSNP = "NA";
	my $pvalue = "NA";

	while (defined($readline=<IN>))
	{
		chomp $readline;

		if ($readline =~ /^inBedIndexSNPNum\t=\t/)
		{
			$readline =~ s/^inBedIndexSNPNum\t=\t//;

			$inBedIndexSNPNum = $readline;
		}

		if ($readline =~ /^expectedS\t=\t/)
		{
			$readline =~ s/^expectedS\t=\t//;

			$expectedNumInBedSNP = $readline;
		}

		if ($readline =~ /^p3\t=\t/)
		{
			$readline =~ s/^p3\t=\t//;

			$pvalue = $readline;
		}
	}

	print OUT "$bedFiles[$i]\t$inBedIndexSNPNum\t$expectedNumInBedSNP\t$pvalue\n";

	close IN;
}

close OUT;

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl create.statistic.summary.file.pl --statisticSummaryFile $statisticSummaryFile --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
