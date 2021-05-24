#! /usr/bin/perl -w

use strict;
use warnings;
use FindBin qw($Bin);
#use DB_File;
use DBI;
use Switch;
use Getopt::Long;
use Time::HiRes qw[gettimeofday tv_interval];
use Fcntl qw(:flock);

my $start = time;
my $startTime = [gettimeofday()];

my $indexSNPList;
my $refDIR;
my $cubeIDFile;
my $r2Threshold;
my $ldWindowSize;
my $annotatedList;
my $nonannotatedList;
my $rsidSNPList;
my $indexSNPLDList;
my $logFile;
my $help;
		  
Getopt::Long::GetOptions(
      'indexSNPList=s' => \$indexSNPList,
      'refDIR=s' => \$refDIR,
      'cubeIDFile=s' => \$cubeIDFile,
      'r2Threshold=f' => \$r2Threshold,
      'ldWindowSize=i' => \$ldWindowSize,
      'annotatedList=s' => \$annotatedList,
      'nonannotatedList=s' => \$nonannotatedList,
      'rsidSNPList=s' => \$rsidSNPList,
      'indexSNPLDList=s' => \$indexSNPLDList,
      'logFile=s' => \$logFile,
			'help' => \$help);

if (defined($help))
{
	print "perl annotate.index.snp.pl --indexSNPList indexSNPList --refDIR refDIR --cubeIDFile cubeIDFile --r2Threshold r2Threshold --ldWindowSize ldWindowSize --annotatedList annotatedList --nonannotatedList nonannotatedList --rsidSNPList rsidSNPList --indexSNPLDList indexSNPLDList --logFile logFile\n";
	print "perl annotate.index.snp.pl --help\n";
				  
	exit(0);
}

if (!defined($indexSNPList))
{
	print "No define indexSNPList!\n";

	exit(1);
}
elsif (!(-e $indexSNPList))
{
	print "$indexSNPList doesn't exist!\n";

	exit(1);
}

if (!defined($refDIR))
{
	print "No define reference directory!\n";

	exit(1);
}
elsif (!(-e $refDIR))
{
	print "refDIR($refDIR) doesn't exist!\n";

	exit(1);
}

if ($refDIR !~ /\/$/)
{
	$refDIR = $refDIR."/";
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

if (!defined($annotatedList))
{
	print "No define annotatedList!\n";

	exit(1);
}

if (!defined($nonannotatedList))
{
	print "No define nonannotatedList!\n";

	exit(1);
}

if (!defined($rsidSNPList))
{
	print "No define rsidSNPList!\n";

	exit(1);
}

if (!defined($indexSNPLDList))
{
	print "No define indexSNPLDList!\n";

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

my %mafIDHash;
my %distIDHash;
my %ldnumIDHash;

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
		$mafIDHash{$value} = $id;
	}
	elsif ($hashid eq "dist")
	{
		$distIDHash{$value} = $id;
	}
	elsif ($hashid eq "ldnum")
	{
		$ldnumIDHash{$value} = $id;
	}
}

close IN;

use lib "$Bin/../lib";

use SNPDictionary;

my $dictObj = new SNPDictionary;

$dictObj->setVer("hg19");
$dictObj->{"driver"} = "SQLite";
$dictObj->{"database"} = $refDIR."snp.db";;
$dictObj->{"dsn"} = "";
$dictObj->{"userid"} = "";
$dictObj->{"password"} = "";

$dictObj->openSNPDB($refDIR);

sub Annotate
{
	my ($snp,$r2Threshold,$ldWindowSize) = @_;

	$snp =~ s/^chr//i;

	my $maf = "NA";
	my $dist = "NA";
	my $ldnum = 0;
	my @LDArr;
	undef @LDArr;

	if ($snp =~ /^(\d+):(\d+)$/)
	{
		my $chr = $1;
		my $pos = $2;

		my $driver		= "SQLite";
		my $database	=	$refDIR."CHR$chr.db";
		my $dsn				= "DBI:$driver:dbname=$database";
		my $userid		= "";
		my $password	= "";

		if (-e $database)
		{
			my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) or die $DBI::errstr;
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
				$maf = $row[4];
				$dist = $row[5];

				my @fields = split(/\|/,$row[7]);

				for (my $i = 0; $i < int(@fields); $i++)
				{
					my @tmp = split(/\+/,$fields[$i]);
					my $ldpos = $tmp[0];
					my $r2 = $tmp[1];

					my $lddist = abs($pos - $ldpos);

					if (($r2 > $r2Threshold)&&($lddist <= $ldWindowSize))
					{
						my $k = int(@LDArr);
						$LDArr[$k] = $ldpos;
					}
				}
			}
			
			$dbh->disconnect();
		}
	}

	$ldnum = int(@LDArr);

	return ($maf,$dist,$ldnum,@LDArr);
}

my %indexSNPHash;

open (IN,$indexSNPList) || die "can't the file $indexSNPList!\n";
open (ANNOTATEDOUT,">".$annotatedList) || die "can't the file $annotatedList!\n";
open (NONANNOTATEDOUT,">".$nonannotatedList) || die "can't the file $nonannotatedList!\n";
open (RSIDSNPOUT,">".$rsidSNPList) || die "can't the file $rsidSNPList!\n";
open (INDEXSNPLDOUT,">".$indexSNPLDList) || die "can't the file $indexSNPLDList!\n";

print ANNOTATEDOUT "index_SNP\tmaf\tdistance_to_nearest_gene\tLD_buddy_num\tmafid\tdistid\tldnumid\n";

print NONANNOTATEDOUT "The following SNPs can't be annotated:\n";
print NONANNOTATEDOUT "index_SNP\n";

print RSIDSNPOUT "The following SNPs can't be translated to chr:pos\n";
print RSIDSNPOUT "rsid\n";

print INDEXSNPLDOUT "index_SNP\tLD_buddy_pos\n";

while (defined($readline=<IN>))
{
	chomp $readline;

	my $indexSNP = $readline;

	if ($indexSNP =~ /^rs/i)
	{
		$indexSNP =~ s/^rs/rs/i;

		my $rsid = $indexSNP;

		$indexSNP = $dictObj->rsToChrPos($rsid);

		if ($indexSNP eq "NA")
		{
			print RSIDSNPOUT "$rsid\n";
		}
	}

	if ($indexSNP ne "NA")
	{
		if (!exists($indexSNPHash{$indexSNP}))
		{
			my $maf;
			my $dist;
			my $ldnum;
			my @LDArr;
			undef @LDArr;

			($maf,$dist,$ldnum,@LDArr) = Annotate($indexSNP,$r2Threshold,$ldWindowSize);
		
			my $mafid = "NA";
			my $distid = "NA";
			my $ldnumid = "NA";

			if (exists($mafIDHash{$maf}))
			{
				$mafid = $mafIDHash{$maf};
			}

			if (exists($distIDHash{$dist}))
			{
				$distid = $distIDHash{$dist};
			}

			if (exists($ldnumIDHash{$ldnum}))
			{
				$ldnumid = $ldnumIDHash{$ldnum};
			}

			if (($mafid ne "NA")&&($distid ne "NA")&&($ldnumid ne "NA"))
			{
				print ANNOTATEDOUT "$indexSNP\t$maf\t$dist\t$ldnum\t$mafid\t$distid\t$ldnumid\n";

				print INDEXSNPLDOUT "$indexSNP\t$LDArr[0]";

				for (my $j = 1; $j < int(@LDArr); $j++)
				{
					print INDEXSNPLDOUT "|$LDArr[$j]";
				}

				print INDEXSNPLDOUT "\n";
			}
			else
			{
				print NONANNOTATEDOUT "$indexSNP\n";
			}

			$indexSNPHash{$indexSNP} = 1;
		}
	}
}

close IN;
close ANNOTATEDOUT;
close NONANNOTATEDOUT;
close RSIDSNPOUT;
close INDEXSNPLDOUT;

$dictObj->closeSNPDB();

my $end = time;

my $runningTime = tv_interval($startTime) * 1000;

open(SEM,">$logFileLock") or die "Can't create semaphore: $!";

flock(SEM,LOCK_EX) or die "Lock failed: $!";

open (OUT,">>".$logFile) || die "can't write to the file:$!\n";

print OUT "$now perl annotate.index.snp.pl --indexSNPList $indexSNPList --refDIR $refDIR --cubeIDFile $cubeIDFile --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --annotatedList $annotatedList --nonannotatedList $nonannotatedList --rsidSNPList $rsidSNPList --indexSNPLDList $indexSNPLDList --logFile $logFile start=$start end=$end runningTime=$runningTime\n";

close OUT;

close(SEM);

exit(0);
