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

my $bedFileName;
my $inDIR;
my $outDIR;
my $logFile;
my $help;

Getopt::Long::GetOptions(
       'bedFileName=s' => \$bedFileName,
       'inDIR=s' => \$inDIR,
       'outDIR=s' => \$outDIR,
       'logFile=s' => \$logFile,
       'help' => \$help);

if (defined($help))
{
	print "perl merge.index.SNP.and.LD.in.bed.pl --bedFileName bedFileName --inDIR inDIR --outDIR outDIR  --logFile logFile\n";
	print "perl merge.index.SNP.and.LD.in.bed.pl --help\n";
	
	exit(0);
}

if (!defined($bedFileName))
{
	print "Please define bedFileName!\n";

	exit(1);
}

if (!defined($inDIR))
{
	print "Please define inDIR!\n";

	exit(1);
}
else
{
	if (!(-e $inDIR))
	{
		print "$inDIR doesn't exist!\n";

		exit(1);
	}
}

if (!defined($outDIR))
{
	print "Please define outDIR!\n";

	exit(1);
}
else
{
	if (!(-e $outDIR))
	{
		`mkdir $outDIR`;
	}
}

if ($inDIR !~ /\/$/)
{
	$inDIR = $inDIR."/";
}

if ($outDIR !~ /\/$/)
{
	$outDIR = $outDIR."/";
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

my $outFile = $outDIR."index.SNP.and.LD.in.bed.".$bedFileName.".txt";

my $txt = " ";

for (my $i = 1; $i < 23; $i++)
{
	my $file = $inDIR.$bedFileName.".chr$i.txt";

	$txt = $txt." ".$file;
}

my $cmd = `cat $txt > $outFile`;

my $endRunning = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl merge.index.SNP.and.LD.in.bed.pl --bedFileName $bedFileName --inDIR $inDIR --outDIR $outDIR --logFile $logFile start=$startRunning end=$endRunning runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
