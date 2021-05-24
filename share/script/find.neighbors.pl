#! /usr/bin/perl -w

use strict;
use warnings;
#use FindBin qw($Bin);
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $indexSNPFile;
my $cubeFileDIR;
my $minNeighbor;
my $indexSNPNeighborFile;
my $logFile;
my $help;
		  
Getopt::Long::GetOptions(
      'indexSNPFile=s' => \$indexSNPFile,
      'cubeFileDIR=s' => \$cubeFileDIR,
      'minNeighbor=i' => \$minNeighbor,
      'indexSNPNeighborFile=s' => \$indexSNPNeighborFile,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl find.neighbors.pl --indexSNPFile indexSNPFile --cubeFileDIR cubeFileDIR --minNeighbor minNeighbor --indexSNPNeighborFile indexSNPNeighborFile --logFile logFile\n";
	print "perl find.neighbors.pl --help\n";
				  
	exit(0);
}

if (!defined($indexSNPFile))
{
	print "No define indexSNPFile!\n";

	exit(1);
}
elsif (!(-e $indexSNPFile))
{
	print "$indexSNPFile doesn't exist!\n";

	exit(1);
}

if (!defined($cubeFileDIR))
{
	print "No define cubeFileDIR!\n";

	exit(1);
}
elsif (!(-e $cubeFileDIR))
{
	print "$cubeFileDIR doesn't exist!\n";

	exit(1);
}

if (!defined($minNeighbor))
{
	print "No define minNeighbor!\n";

	exit(1);
}
elsif ($minNeighbor !~ /^\d+$/)
{
	print "minNeighbor should be a number!\n";

	exit(1);
}

if (!defined($indexSNPNeighborFile))
{
	print "No define indexSNPNeighborFile!\n";
	
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

my %indexSNPHash;

open (IN,$indexSNPFile) || die "can't the file $indexSNPFile!\n";

my $readline=<IN>;

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);

	my $indexSNP = $fields[0];
	my $mafid = $fields[4];
	my $distid = $fields[5];
	my $ldnumid = $fields[6];

	my $key = "$mafid\t$distid\t$ldnumid";

	if (exists($indexSNPHash{$key}))
	{
		$indexSNPHash{$key} = $indexSNP."|".$indexSNPHash{$key};
	}
	else
	{
		$indexSNPHash{$key} = $indexSNP;
	}
}

close IN;

my $cubeid = $cubeFileDIR."cube.id.txt";

open (IN,$cubeid) || die "can't open the file $cubeid!\n";

$readline = <IN>;
chomp $readline;
my @fields = split(/\t/,$readline);
my $maxDistID = $fields[1] - 1;
my $maxLDNumID = $fields[1] - 1;

close IN;

my %cubeHash;
my %neighborsHash;

for (my $i = 1; $i < 23; $i++)
{
	my $cubeOnChrFile = $cubeFileDIR."chr$i.maf.dist.ldnum.id.txt";

	if (-e $cubeOnChrFile)
	{
		open (IN,$cubeOnChrFile) || die "can't open the file $cubeOnChrFile!\n";

		$readline = <IN>;

		while (defined($readline=<IN>))
		{
			chomp $readline;

			my @fields = split(/\t/,$readline);

			my $mafid = $fields[0];
			my $distid = $fields[1];
			my $ldnumid = $fields[2];
			my $neighbors = $fields[3];

			my $key = "$mafid\t$distid\t$ldnumid";

			if (exists($cubeHash{$key}))
			{
				$cubeHash{$key} = $cubeHash{$key}."|".$neighbors;
			}
			else
			{
				$cubeHash{$key} = $neighbors;
			}
		}

		close IN;
	}
}

while (my ($key,$indexSNP) = each %indexSNPHash)
{
	if (exists($cubeHash{$key}))
	{
		$neighborsHash{$key} = $cubeHash{$key};
	}
}

while (my ($key,$neighbors) = each %neighborsHash)
{
	my @tmp = split(/\|/,$neighbors);

	my $num = int(@tmp);

	my $step = 1;

	while ($num < $minNeighbor)
	{
		my @fields = split(/\t/,$key);

		my $mafid = $fields[0];
		my $distid = $fields[1];
		my $ldnumid = $fields[2];

		my $xstart = $distid - $step;
		my $xend = $distid + $step;
		my $ystart = $ldnumid - $step;
		my $yend = $ldnumid + $step;

		if ($xstart < 0)
		{
			$xstart = 0;
		}

		if ($xend > $maxDistID)
		{
			$xend = $maxDistID;
		}

		if ($ystart < 0)
		{
			$ystart = 0;
		}

		if ($yend > $maxLDNumID)
		{
			$yend = $maxLDNumID;
		}

		$step = $step + 1;

		$neighbors = "";

		for (my $i = $xstart; $i <= $xend; $i++)
		{
			for (my $j = $ystart; $j <= $yend; $j++)
			{
				my $thiskey = "$mafid\t$i\t$j";

				if (exists($cubeHash{$thiskey}))
				{
					if ($neighbors eq "")
					{
						$neighbors = $cubeHash{$thiskey};
					}
					else
					{
						$neighbors = $neighbors."|".$cubeHash{$thiskey};
					}
				}
			}
		}

		$neighborsHash{$key} = $neighbors;

		@tmp = split(/\|/,$neighbors);
		
		$num = int(@tmp);
	}
}

open (OUT,">".$indexSNPNeighborFile) || die "can't write the file $indexSNPNeighborFile!\n";

print OUT "index_SNP_num_in_cube\tindex_SNP_in_cube\tmafid\tdistid\tldnumid\tneighbors\n";

while (my ($key,$neighbors) = each %neighborsHash)
{
	my @fields = split(/\t/,$indexSNPHash{$key});
	@fields = split(/\|/,$fields[0]);
	my $num = int(@fields);

	print OUT "$num\t$indexSNPHash{$key}\t$key\t$neighbors\n";
}

close OUT;

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl find.neighbors.pl --indexSNPFile $indexSNPFile --cubeFileDIR $cubeFileDIR --minNeighbor $minNeighbor --indexSNPNeighborFile $indexSNPNeighborFile --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
