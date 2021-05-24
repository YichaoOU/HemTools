#! /usr/bin/perl -w

use strict;
use warnings;
#use FindBin qw($Bin);
#use DB_File;
use DBI;
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $chrid;
my $refDIR;
my $r2Threshold;
my $ldWindowSize;
my $chrout;
my $distributionFile;
my $logFile;
my $help;

Getopt::Long::GetOptions(
			'chrid=i' => \$chrid,
			'refDIR=s' => \$refDIR,
			'r2Threshold=f' => \$r2Threshold,
			'ldWindowSize=i' => \$ldWindowSize,
			'chrout=s' => \$chrout,
			'distributionFile=s' => \$distributionFile,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl calculate.maf.dist.ldnum.pl --chrid chrid --refDIR refDIR --r2Threshold r2Threshold --ldWindowSize ldWindowSize --chrout chrout --distributionFile distributionFile --logFile logFile\n";	
	print "perl calculate.maf.dist.ldnum.pl --help\n";

	exit(0);
}

if (!defined($chrid))
{
	print "No define chrid!\n";

	exit(1);
}

if (!defined($refDIR))
{
	print "No define refDIR!\n";

	exit(1);
}
else
{
	if (!(-e $refDIR))
	{
		print "refDIR ($refDIR) doesn't exist!\n";

		exit(1);
	}
}

if ($refDIR !~ /\/$/)
{
	$refDIR = $refDIR."/";
}

if (!defined($r2Threshold))
{
	print "No define r2Threshold!\n";

	exit(1);
}
elsif ($r2Threshold < 0.7)
{
	print "Please change your r2 threshold! It should be greater than 0.7!\n";

	exit(1);
}

if (!defined($ldWindowSize))
{
	print "No define ldWindowSize!\n";

	exit(1);
}
elsif ($ldWindowSize > 1000000)
{
	print "Please change your LD Window Size. It should be less than 1MB(1000000)!\n";

	exit(1);
}

if (!defined($chrout))
{
	print "No define chrout!\n";
	
	exit(1);
}

if (!defined($distributionFile))
{
	print "No define distributionFile!\n";
	
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

my $database = $refDIR."CHR$chrid.db";

if (!(-e $database))
{
	print "Please make sure you have download all reference files!\nCan't find CHR$chrid.db!\n";

	exit(1);
}

my $driver   = "SQLite";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) or die $DBI::errstr;

my $stmt = qq(SELECT * from CUBE;);

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die $DBI::errstr;

if($rv < 0)
{
	print $DBI::errstr;

	exit(1);
}

open (OUT,">".$chrout) || die "can't write to the file $chrout!\n";

my %mafHash;
my %distHash;
my %ldnumHash;

print OUT "pos\tmaf\tdist2Gene\tLDNum\n";

while(my @row = $sth->fetchrow_array())
{
	my $pos = $row[0];
	my $maf = $row[4];
	my $dist = $row[5];
	my $lds = $row[7];

	my @ldArr = split(/\|/,$lds);

	my $ldnum = 0;

	for (my $i = 0; $i < int(@ldArr); $i++)
	{
		my @tmp = split(/\+/,$ldArr[$i]);

		my $ldpos = $tmp[0];
		my $r2 = $tmp[1];

		my $lddist = abs($pos - $ldpos);

		if (($r2 > $r2Threshold)&&($lddist <= $ldWindowSize))
		{
			$ldnum = $ldnum + 1;
		}
	}

	if ($ldnum > 0)
	{
		print OUT "$pos\t$maf\t$dist\t$ldnum\n";

		if (exists($mafHash{$maf}))
		{
			$mafHash{$maf} = $mafHash{$maf} + 1;
		}
		else
		{
			$mafHash{$maf} = 1;
		}

		if (exists($distHash{$dist}))
		{
			$distHash{$dist} = $distHash{$dist} + 1;
		}
		else
		{
			$distHash{$dist} = 1;
		}

		if (exists($ldnumHash{$ldnum}))
		{
			$ldnumHash{$ldnum} = $ldnumHash{$ldnum} + 1;
		}
		else
		{
			$ldnumHash{$ldnum} = 1;
		}
	}
}

$dbh->disconnect();

close OUT;

open (OUT,">".$distributionFile) || die "can't write to the file $distributionFile!\n";

while (my ($maf,$num) = each %mafHash)
{
	print OUT "maf\t$maf\t$num\n";
}

while (my ($dist,$num) = each %distHash)
{
	print OUT "dist\t$dist\t$num\n";
}

while (my ($ldnum,$num) = each %ldnumHash)
{
	print OUT "ldnum\t$ldnum\t$num\n";
}

close OUT;

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl calculate.maf.dist.ldnum.pl --chrid $chrid --refDIR refDIR --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --chrout $chrout --distributionFile $distributionFile --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
