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

my $neighborlist;
my $refDIR;
my $r2Threshold;
my $ldWindowSize;
my $chrid;
my $neighborLDlist;
my $logFile;
my $help;
		  
Getopt::Long::GetOptions(
      'neighborlist=s' => \$neighborlist,
      'refDIR=s' => \$refDIR,
      'r2Threshold=f' => \$r2Threshold,
      'ldWindowSize=i' => \$ldWindowSize,
      'chrid=i' => \$chrid,
      'neighborLDlist=s' => \$neighborLDlist,
			'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl find.neighbors.LDbuddy.pl --neighborlist neighborlist --refDIR refDIR --r2Threshold r2Threshold --ldWindowSize ldWindowSize --chrid chrid --neighborLDlist neighborLDlist --logFile logFile\n";
	print "perl find.neighbors.LDbuddy.pl --help\n";
				  
	exit(0);
}

if (!defined($neighborlist))
{
	print "No define neighborlist!\n";

	exit(1);
}
elsif (!(-e $neighborlist))
{
	print "$neighborlist doesn't exist!\n";

	exit(1);
}

if (!defined($refDIR))
{
	print "No define refDIR!\n";

	exit(1);
}
elsif (!(-e $refDIR))
{
	print "refDIR ($refDIR) doesn't exist!\n";

	exit(1);
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

if (!defined($ldWindowSize))
{
	print "No define ldWindowSize!\n";

	exit(1);
}

if (!defined($chrid))
{
	print "No define chrid!\n";

	exit(1);
}

if (!defined($neighborLDlist))
{
	print "No define neighborLDlist!\n";

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
	print "Please make sure you have downloaded all reference files!\nCan't find CHR$chrid.db!\n";
	
	exit(1);
}

my $driver   = "SQLite";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) or die $DBI::errstr;

my %neighborHash;

open (IN,$neighborlist) || die "can't the file $neighborlist!\n";
open (OUT,">".$neighborLDlist) || die "can't the file $neighborLDlist!\n";

print OUT "neighbor_SNP\tLD_buddy_pos\n";

my $readline = <IN>;

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);
	my @neighbors = split(/\|/,$fields[5]);

	for (my $i = 0; $i < int(@neighbors); $i++)
	{
		my $thisNeighbor = $neighbors[$i];

		if ($thisNeighbor =~ /^($chrid):(\d+)/)
		{
			my $chr = $chrid;
			my $pos = $2;

			if (!exists($neighborHash{$thisNeighbor}))
			{
				my @LDArr;
				undef @LDArr;

				my $stmt = qq(SELECT * from CUBE where POS=$pos;);
				
				my $sth = $dbh->prepare( $stmt );
				my $rv = $sth->execute() or die $DBI::errstr;
				
				if($rv < 0)
				{
					print $DBI::errstr;
					
					exit(1);
				}

				while(my @row = $sth->fetchrow_array())
				{
					@fields = split(/\|/,$row[7]);
		      
					for (my $i = 0; $i < int(@fields); $i++)
		      {
						my @tmp = split(/\+/,$fields[$i]);
						my $ldpos = $tmp[0];
						my $r2 = $tmp[1];
					
						print "pos = $pos\nldpos = $ldpos\n";

						my $lddist = abs($pos - $ldpos);
						
						if (($r2 > $r2Threshold)&&($lddist <= $ldWindowSize))
						{
							my $k = int(@LDArr);
							$LDArr[$k] = $ldpos;
						}
					}
				}

				my $numofld = int(@LDArr);

				if ($numofld > 0)
				{
					print OUT "$thisNeighbor\t$LDArr[0]";

					for (my $j = 1; $j < int(@LDArr); $j++)
					{
						print OUT "|$LDArr[$j]";
					}

					print OUT "\n";
				}

				$neighborHash{$thisNeighbor} = 1;
			}
		}
	}
}

close IN;
close OUT;

$dbh->disconnect();

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl find.neighbors.LDbuddy.pl --neighborlist $neighborlist --refDIR refDIR --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --chrid $chrid --neighborLDlist $neighborLDlist --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
