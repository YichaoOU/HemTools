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

my $bedFile;
my $sortedBedFile;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'bedFile=s' => \$bedFile,
			'sortedBedFile=s' => \$sortedBedFile,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl sort.bed.file.pl --bedFile bedFile --sortedBedFile sortedBedFile --logFile logFile\n";	
	print "perl sort.bed.file.pl --help\n";

	exit(0);
}

if (!defined($bedFile))
{
	print "No define bedFile!\n";

	exit(1);
}
else
{
	if (!(-e $bedFile))
	{
		print "$bedFile doesn't exist!\n";

		exit(1);
	}
}

if (!defined($sortedBedFile))
{
	print "No define sortedBedFile!\n";

	exit(1);
}

if (!defined($logFile))
{
	print "No define logFile!\n";
	
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

my $bedObj = new Overlap;

$bedObj->{"bedFile"} = $bedFile;
$bedObj->{"sortedBedFile"} = $sortedBedFile;

$bedObj->sortBedFile();

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl sort.bed.file.pl --bedFile $bedFile --sortedBedFile $sortedBedFile --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
