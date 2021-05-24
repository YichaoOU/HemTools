#! /usr/bin/perl -w

package SNPDictionary;

use strict;
use warnings;
#use FindBin qw($Bin);
#use DB_File;
use DBI;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(setVer openSNPDB closeSNPDB rsToChrPos ChrPosTors);

sub new
{
	my $self = {};

	$self->{"driver"} = "SQLite";
	$self->{"database"} = "";
	$self->{"dsn"} = "";
	$self->{"userid"} = "";
	$self->{"password"} = "";

	$self->{"ver"} = "Not_Set";
	
	bless $self;

	return $self;
}

sub setVer
{
	my $self = shift;

	my ($ver) = @_;

	if ($ver =~ /^hg18$/i)
	{
		$self->{"ver"} = "hg18";
	}
	elsif ($ver =~ /^hg19$/)
	{
		$self->{"ver"} = "hg19";
	}
}

sub openSNPDB
{
	my $self = shift;

	my ($refDIR) = @_;

	if (!(-e $refDIR))
	{
		print "reference file directory doesn't exist!\n";

		exit(1);
	}
	else
	{
		if ($refDIR !~ /\/$/)
		{
			$refDIR = $refDIR."/";
		}
	}

	print "Please wait for connecting with SNP database ......\n";

=pod
	my $rs2chrposfile;
	my $chrpos2rsfile;

	undef %{$self->{"rs2chrpos"}};
	undef %{$self->{"chrpos2rs"}};

	if ($self->{"ver"} eq "hg18")
	{
		$rs2chrposfile = $refDIR."rsidToCHRPOS.hg18.dbm";
		$chrpos2rsfile = $refDIR."CHRPOSTorsid.hg18.dbm";
	}
	elsif ($self->{"ver"} eq "hg19")
	{
		$rs2chrposfile = $refDIR."rsidToCHRPOS.hg19.dbm";
		$chrpos2rsfile = $refDIR."CHRPOSTorsid.hg19.dbm";
	}

	if (-e $rs2chrposfile)
	{
		dbmopen (%{$self->{"rs2chrpos"}},$rs2chrposfile,0644) or die "can't open the $rs2chrposfile!\n";
	}
	else
	{
		print "$rs2chrposfile doesn't exist! Please make sure you have downloaded all reference files!\n";

		exit(0);
	}

	if (-e $chrpos2rsfile)
	{
		dbmopen (%{$self->{"chrpos2rs"}},$chrpos2rsfile,0644) or die "can't open the $chrpos2rsfile!\n";
	}
	else
	{
		print "$chrpos2rsfile doesn't exist! Please make sure you have downloaded all reference files!\n";

		exit(0);
	}
=cut
}

sub closeSNPDB
{
	my $self = shift;

	print "Please wait for closing the SNP database ......\n";
	
=pod
	dbmclose(%{$self->{"rs2chrpos"}});
	dbmclose(%{$self->{"chrpos2rs"}});
=cut
}

sub rsToChrPos
{
	my $self = shift;

	my ($rsid) = @_;

	my $snp = "NA";

	my $driver = $self->{"driver"};
	my $database = $self->{"database"};
	my $dsn = "DBI:$driver:dbname=$database";
	my $userid = $self->{"userid"};
	my $password = $self->{"password"};
	my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) or die $DBI::errstr;

	print "driver = $driver\n";
	print "database = $database\n";
	print "dsn = $dsn\n";
	print "userid = $userid\n";
	print "password = $password\n";
	my $stmt = qq(SELECT * from SNP where RSID=\"$rsid\";);
	
	my $sth = $dbh->prepare( $stmt );
	
	my $rv = $sth->execute() or die $DBI::errstr;
	
	if($rv < 0)
	{
		print $DBI::errstr;

		exit(1);
	}
			 
	while(my @row = $sth->fetchrow_array())
	{
		my $chr = $row[1];
		my $pos = $row[2];

		$snp = $chr.":".$pos;
	}
	
	$dbh->disconnect();

	return ($snp);
}

sub ChrPosTors
{
	my $self = shift;

	my ($snp) = @_;

	$snp =~ s/^chr//;
	
	if ($snp =~ /^(\d+|X|x|Y|y):(\d+)$/)
	{
		my $chr = $1;
		my $pos = $2;
		
		if ($chr =~ /^x$/i)
		{
			$chr = 23;
		}
		elsif ($chr =~ /^y$/i)
		{
			$chr = 24;
		}
		
		$snp = $chr.":".$pos;
	}

	my $rsid = "NA";

	if (exists($self->{"chrpos2rs"}->{$snp}))
	{
		$rsid = $self->{"chrpos2rs"}->{$snp};
	}
	
	return ($rsid);
}
	
1;
