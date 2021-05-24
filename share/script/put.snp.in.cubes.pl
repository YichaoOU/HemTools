#! /usr/bin/perl -w

use strict;
use warnings;
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $chrfile;
my $chrid;
my $cubeIDFile;
my $out;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'chrfile=s' => \$chrfile,
			'chrid=i' => \$chrid,
			'cubeIDFile=s' => \$cubeIDFile,
			'out=s' => \$out,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl put.snp.in.cubes.pl --chrfile chrfile --chrid chrid --cubeIDFile cubeIDFile --out out --logFile logFile\n";	
	print "perl put.snp.in.cubes.pl --help\n";

	exit(0);
}

if (!defined($chrfile))
{
	print "No define chrfile!\n";

	exit(1);
}
elsif (!(-e $chrfile))
{
	print "$chrfile doesn't exist!\n";

	exit(1);
}

if (!defined($chrid))
{
	print "No define chrid!\n";

	exit(1);
}

if (!defined($out))
{
	print "No define out!\n";
	
	exit(1);
}

if (!defined($cubeIDFile))
{
	print "No define cubeIDFile!\n";
	
	exit(1);
}
elsif (!(-e $cubeIDFile))
{
	print "$cubeIDFile doesn't exist!\n";

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

open (IN,$cubeIDFile) || die "can't open the file $cubeIDFile!\n";

my $readline;

for (my $i = 0; $i < 3; $i++)
{
	$readline = <IN>;
}

while (defined($readline=<IN>))
{
	chomp $readline;
	my @fields = split(/\t/,$readline);

	my $hashid = $fields[0];
	my $value = $fields[1];
	my $id = $fields[3];

	if ($hashid eq "maf")
	{
		$mafHash{$value} = $id;
	}
	elsif ($hashid eq "dist")
	{
		$distHash{$value} = $id;
	}
	elsif ($hashid eq "ldnum")
	{
		$ldnumHash{$value} = $id;
	}
}

close IN;

my %cubeHash;

open (IN,$chrfile) || die "can't open the file $chrfile!\n";

$readline = <IN>;

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);

	my $pos = $fields[0];
	my $maf = $fields[1];
	my $dist = $fields[2];
	my $ldnum = $fields[3];

	my $mafid = "NA";
	my $distid = "NA";
	my $ldnumid = "NA";

	if (exists($mafHash{$maf}))
	{
		$mafid = $mafHash{$maf};
	}

	if (exists($distHash{$dist}))
	{
		$distid = $distHash{$dist};
	}

	if (exists($ldnumHash{$ldnum}))
	{
		$ldnumid = $ldnumHash{$ldnum};
	}

	my $key = "$mafid\t$distid\t$ldnumid";

	if (exists($cubeHash{$key}))
	{
		$cubeHash{$key} = $cubeHash{$key}."|".$chrid.":".$pos;
	}
	else
	{
		$cubeHash{$key} = $chrid.":".$pos;
	}
}

close IN;

open (OUT,">".$out) || die "can't write to the file $out!\n";

print OUT "mafID\tdistID\tldnumID\tSNPs\n";

while (my ($k,$v) = each %cubeHash)
{
	print OUT "$k\t$v\n";
}

close OUT;

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl put.snp.in.cubes.pl --chrfile $chrfile --chrid $chrid --cubeIDFile $cubeIDFile --out $out --logFile $logFile start=$start end=$end runningTime=$runningTime\n";	

close OUT;

close(SEM);


exit(0);
