#! /usr/bin/perl -w

package Overlap;

use strict;
use warnings;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(checkBedObj cleanBedObj verifyBedFile sortBedFile createBedArrayOnChr overlap);

sub new
{
	my $self = {};

	$self->{"bedFile"} = "NA";
	$self->{"sortedBedFile"} = "NA";

	$self->{"chrNo"} = "NA";
	$self->{"bedOnChr"} = [];

	$self->{"inBedSNPHash"} = {};

	$self->{"error"} = "Error";

	bless $self;

	return $self;
}

sub checkBedObj
{
	my $self = shift;

	$self->{"error"} = "NA";

	if ($self->{"chrNo"} !~ /^\d+$/)
	{
		$self->{"error"} = "Please define chromosome No.!";

		print $self->{"error"}."\n";
	}
	else
	{
		my $chr = $self->{"chrNo"};
		
		if (($chr < 1) || ($chr > 22))
		{
			$self->{"error"} = "The chromosome No. is not between 1 to 22!";

			print $self->{"error"}."\n";
		}
	}

	if ($self->{"bedFile"} eq "NA")
	{
		$self->{"error"} = "Please define the bed file!";

		print $self->{"error"}."\n";
	}
	else
	{
		if (!(-e $self->{"bedFile"}))
		{
			my $bedfile = $self->{"bedFile"};
			$self->{"error"} = "The bed file($bedfile) doesn't exist!";

			print $self->{"error"}."\n";
		}
	}

	if ($self->{"sortedBedFile"} eq "NA")
	{
		$self->{"error"} = "Please define the sorted bed file!";

		print $self->{"error"}."\n";
	}
	else
	{
		if (!(-e $self->{"sortedBedFile"}))
		{
			my $sortedBedFile = $self->{"sortedBedFile"};
			$self->{"error"} = "The sorted bed file($sortedBedFile) doesn't exist!";

			print $self->{"error"}."\n";
		}
	}

}

sub verifyBedFile
{
	my $self = shift;

	$self->{"error"} = "NA";

	if ($self->{"bedFile"} eq "NA")
	{
		$self->{"error"} = "Please define the bed file!";

		print $self->{"error"}."\n";
	}
	else
	{
		if (!(-e $self->{"bedFile"}))
		{
			my $bedFile = $self->{"bedFile"};
			$self->{"error"} = "The bed file($bedFile) doesn't exist!";

			print $self->{"error"}."\n";
		}
		else
		{
			my $bedFile = $self->{"bedFile"};
			
			my $type = getFileType($bedFile);
			
			if ($type eq "ASCII")
			{
				my $cmd = `wc -l $bedFile`;
				chomp $cmd;
				my @fields = split(/\ +/,$cmd);
				my $lines = $fields[0];

				if ($lines > 5)
				{
					$lines = 5;
				}

				open (IN,$bedFile) || die "can't open the file:$!\n";

				my $readline;

				for (my $i = 0; $i < $lines; $i++)
				{
					$readline = <IN>;

					chomp $readline;

					my @fields = split(/\t/,$readline);

					my $chr = $fields[0];
					my $start = $fields[1];
					my $end = $fields[2];

					$chr =~ s/chr//i;

					if (($chr !~ /^\d+$/)||($start !~ /^\d+$/)||($end !~ /^\d+$/))
					{
						$self->{"error"} = "$bedFile has the wrong format!";

						print $self->{"error"}."\n";

						$i = $lines;
					}
				}

				close IN;
			}
			else
			{
				$self->{"error"} = "$bedFile is not an ASCII file!";

				print $self->{"error"}."\n";
			}
		}
	}
}

sub cleanBedObj
{
	my $self = shift;

	undef @{$self->{"bedOnChr"}};

	undef %{$self->{"inBedSNPHash"}};
}

sub InsertBedToArray
{
	my ($list,$s,$e) = @_;

	my $k = @{$list};

	$list->[$k][0] = $$s;
	$list->[$k][1] = $$e;
}

sub sortBedFile
{
	my $self = shift;

	my $bedFile = $self->{"bedFile"};
	my $sortedBedFile = $self->{"sortedBedFile"};

	if ($bedFile eq "NA")
	{
		print "Please define bedFile!\n";

		exit(1);
	}
	elsif (!(-e $bedFile))
	{
		print "$bedFile doesn't exist!\n";

		exit(1);
	}

	if ($sortedBedFile eq "NA")
	{
		print "Please define sortedBedFile!\n";

		exit(1);
	}

	system `sort -k1,1 -k2,2n $bedFile > $sortedBedFile` or die "can't sort the bed file $bedFile\n";
}

sub getFileType
{
	my ($file) = @_;

	my $cmd = `file $file`;

	my $type = "NA";

	if ($cmd =~ /ASCII\ text/)
	{
		$type = "ASCII";
	}
	elsif ($cmd =~ /gzip\ compressed\ data/)
	{
		$type = "gzip";
	}

	return ($type);
}

sub createBedArrayOnChr
{
	my $self = shift;

	my $inputfile = $self->{"sortedBedFile"};
	my $chrid = $self->{"chrNo"};

	if ($self->{"error"} eq "NA")
	{
		open (IN,$inputfile)||die "can not open the file:$!";

		my $readline;

		my $thisStart = "NA";
		my $thisEnd = "NA";

		while (defined ($readline=<IN>))
		{
			chomp $readline;

			my @fields = split(/\t/,$readline);
			my $chr = $fields[0];
			my $start = $fields[1];
			my $end = $fields[2];

			if ($chr =~ /^chr/)
			{
				$chr =~ s/^chr//;
			}

			if ($chr =~ /^\d+$/)
			{
				if ($chr == $chrid)
				{
					if (($thisStart eq "NA")&&($thisEnd eq "NA"))
					{
						$thisStart = $start;
						$thisEnd = $end;
					}
					else
					{
						if ($thisEnd < $start)
						{
							&InsertBedToArray($self->{"bedOnChr"},\$thisStart,\$thisEnd);
							$thisStart = $start;
							$thisEnd = $end;
						}
						else
						{
							if ($thisEnd < $end)
							{
								$thisEnd = $end;
							}
						}
					}
				}
			}
		}

		if (($thisStart ne "NA")&&($thisEnd ne "NA"))
		{
			&InsertBedToArray($self->{"bedOnChr"},\$thisStart,\$thisEnd);
		}

		close IN;
	}
}

sub overlap
{
	my $self = shift;

	my ($chr,$pos) = @_;

	if ($chr =~ /^chr/i)
	{
		$chr =~ s/^chr//i;
	}

	my $start = -1;
	my $end = -1;

	if ($chr == $self->{"chrNo"})
	{
		if (exists($self->{"inBedSNPHash"}{$pos}))
		{
			my @fields = split(/\:/,$self->{"inBedSNPHash"}{$pos});

			$start = $fields[0];
			$end = $fields[1];
		}
		else
		{
			my $num = int(@{$self->{"bedOnChr"}});
			my $head = 0;
			my $tail = $num - 1;
			my $mid = int (($tail - $head) / 2);

			if ($num <= 0)
			{
				$start = -1;
				$end = -1;										
			}
			else
			{
				if (($pos < $self->{"bedOnChr"}->[$head][0])||($self->{"bedOnChr"}->[$tail][0] < $pos))
				{					
					$start = -1;
					$end = -1;						
				}									
				else
				{	
					while (($tail - $head) > 1)
					{
						if ($self->{"bedOnChr"}->[$mid][0] > $pos)
						{											
							$tail = $mid;
						}							
						else
						{	
							$head = $mid;
						}							
						$mid = int(($tail - $head) / 2 + $head);
					}																						
				}		
		
				if (($self->{"bedOnChr"}->[$head][0] <= $pos)&&($self->{"bedOnChr"}->[$head][1] >= $pos))       
				{				         
					$start = $self->{"bedOnChr"}->[$head][0];
					$end = $self->{"bedOnChr"}->[$head][1];																							
				}	       
				else
				{		
					$start = -1;
					$end = -1;						
				}
			}

			$self->{"inBedSNPHash"}{$pos} = $start.":".$end;
		}
	}

	return ($start,$end);
}

1;
