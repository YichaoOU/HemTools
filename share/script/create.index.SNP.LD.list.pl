#! /usr/bin/perl -w

use strict;
use warnings;
use FindBin qw($Bin);
use Switch;
use Getopt::Long;

my $GREGORResultDIR;
my $out;

Getopt::Long::GetOptions(
			'GREGORResultDIR=s' => \$GREGORResultDIR,
			'out=s' => \$out);

my $usage = <<END;
------------------------------------------------------------------------------------
comsensus.bed.files.pl
------------------------------------------------------------------------------------
Version : 1.1.0

Report Bug(s) : jich[at]umich.com
------------------------------------------------------------------------------------
Usage : perl create.index.SNP.LD.list.pl --GREGORResultDIR GREGORResultDIR --out out
------------------------------------------------------------------------------------
END

unless (($GREGORResultDIR)&&($out))
{
	die "$usage\n";
}

if (!(-e $GREGORResultDIR))
{
	print "GREGORResultDIR($GREGORResultDIR) doesn't exist!\n";

	exit(1);
}

if ($GREGORResultDIR !~ /\/$/)
{
	$GREGORResultDIR = $GREGORResultDIR."/";
}

my $LDFile = $GREGORResultDIR."index_SNP/index.snp.LD.txt";

if (!(-e $LDFile))
{
	print "can't find the index SNP LD file ($LDFile)!\n";

	exit(1);
}

open (IN,$LDFile) || die "can't open the file:$LDFile!\n";
open (OUT,">".$out) || die "can't write to the file:$out!\n";

my $readline = <IN>;

print OUT "index_SNP\tLD_buddy\n";

while (defined($readline=<IN>))
{
	chomp $readline;

	my @fields = split(/\t/,$readline);

	my $indexSNP = $fields[0];
	my @lds = split(/\|/,$fields[1]);;
	
	@fields = split(/\:/,$indexSNP);
	my $chr = $fields[0];
	my $pos = $fields[1];

	$chr =~ s/^chr//i;

	print OUT "$chr:$pos\t$chr:$pos\n";

	for (my $i = 0; $i < int(@lds); $i++)
	{
		if ($lds[$i] != $pos)
		{
			print OUT "$chr:$pos\t$chr:$lds[$i]\n";
		}
	}
}

close IN;
close OUT;

exit(0);
