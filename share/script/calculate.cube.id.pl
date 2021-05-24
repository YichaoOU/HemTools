#! /usr/bin/perl -w

use strict;
use warnings;
use Switch;
use Getopt::Long;
use Fcntl qw(:flock);
use Time::HiRes qw[gettimeofday tv_interval];

my $start = time;
my $startTime = [gettimeofday()];

my $chrDIR;
my $out;
my $logFile;
my $help;
		  
Getopt::Long::GetOptions(
      'chrDIR=s' => \$chrDIR,
      'out=s' => \$out,
      'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl calculate.cube.id.pl --chrDIR chrDIR --out out --logFile logFile\n";
	print "perl calculate.cube.id.pl --help\n";
				  
	exit(0);
}

if (!defined($chrDIR))
{
	print "No define chrDIR!\n";

	exit(1);
}
elsif (!(-e $chrDIR))
{
	print "$chrDIR doesn't exist!\n";

	exit(1);
}

if (!defined($out))
{
	print "No define out!\n";
	
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

my %mafHash;
my %distHash;
my %ldnumHash;

if ($chrDIR !~ /\/$/)
{
	$chrDIR = $chrDIR."/";
}

for (my $i = 1; $i < 23; $i++)
{
	my $in = $chrDIR."chr$i.distribution.txt";

	open (IN,$in) || die "can't open the file $in!\n";

	my $readline;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		my @fields = split(/\t/,$readline);
		my $hashid = $fields[0];
		my $value = $fields[1];
		my $num = $fields[2];

		if ($hashid eq "maf")
		{
			if (exists($mafHash{$value}))
			{
				$mafHash{$value} = $mafHash{$value} + $num;
			}
			else
			{
				$mafHash{$value} = $num;
			}
		}
		elsif ($hashid eq "dist")
		{
			if (exists($distHash{$value}))
			{
				$distHash{$value} = $distHash{$value} + $num;
			}
			else
			{
				$distHash{$value} = $num;
			}
		}
		elsif ($hashid eq "ldnum")
		{
			if (exists($ldnumHash{$value}))
			{
				$ldnumHash{$value} = $ldnumHash{$value} + $num;
			}
			else
			{
				$ldnumHash{$value} = $num;
			}
		}
	}

	close IN;
}

open (OUT,">".$out) || die "can't write to the file $out!\n";

my $mafNum = keys %mafHash;
my $distMax = -1;
my $ldnumMax = -1;

while (my ($dist,$num) = each %distHash)
{
	if ($distMax < $dist)
	{
		$distMax = $dist;
	}
}

while (my ($ldnum,$num) = each %ldnumHash)
{
	if ($ldnumMax < $ldnum)
	{
		$ldnumMax = $ldnum;
	}
}

print OUT "mafNum\t$mafNum\n";
print OUT "distMax\t$distMax\n";
print OUT "ldnumMax\t$ldnumMax\n";

my $id = 0;

foreach my $key (sort{$a<=>$b} keys %mafHash)
{
	print OUT "maf\t$key\t$mafHash{$key}\t$id\n";

	$id = $id + 1;
}

my $step = $distMax / $mafNum;

foreach my $key (sort{$a<=>$b} keys %distHash)
{
	my $id = int($key / $step);

	if ($id >= $mafNum)
	{
		$id = $mafNum - 1;
	}
	
	print OUT "dist\t$key\t$distHash{$key}\t$id\n";
}

$step = $ldnumMax / $mafNum;

foreach my $key (sort{$a<=>$b} keys %ldnumHash)
{
	my $id = int($key / $step);

	if ($id >= $mafNum)
	{
		$id = $mafNum - 1;
	}

	print OUT "ldnum\t$key\t$ldnumHash{$key}\t$id\n";
}

close OUT;

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl calculate.cube.id.pl --chrDIR $chrDIR --out $out --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
