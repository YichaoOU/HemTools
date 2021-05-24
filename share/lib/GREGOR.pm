#! /usr/bin/perl -w

package GREGOR;

use strict;
use warnings;
use FindBin qw($Bin);

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(ReadConf VerifyConf ReadReferenceLDBuddyThreshold CheckBedFiles CheckSNPList CreateMakeFile CreateTopNBedMakeFile);

sub new
{
	my $self = {};

	$self->{"conf"} = {};

	bless $self;

	return $self;
}

sub ReadConf
{
	my $self = shift;

	my (%conf) = @_;

	if ($conf{"INDEX_SNP_FILE"} ne "")
	{
		$self->{"conf"}->{"INDEX_SNP_FILE"} = $conf{"INDEX_SNP_FILE"};
	}

	if ($conf{"BED_FILE_INDEX"} ne "")
	{
		$self->{"conf"}->{"BED_FILE_INDEX"} = $conf{"BED_FILE_INDEX"};
	}

	if ($conf{"REF_DIR"} ne "")
	{
		if ($conf{"REF_DIR"} =~ /\/$/)
		{
			$self->{"conf"}->{"REF_DIR"} = $conf{"REF_DIR"};
		}
		else
		{
			$self->{"conf"}->{"REF_DIR"} = $conf{"REF_DIR"}."/";
		}
	}

	if ($conf{"R2THRESHOLD"} ne "")
	{
		$self->{"conf"}->{"R2THRESHOLD"} = $conf{"R2THRESHOLD"};
	}

	$self->{"conf"}->{"DEFAULTR2THRESHOLD"} = -1;

	if ($conf{"LDWINDOWSIZE"} ne "")
	{
		$self->{"conf"}->{"LDWINDOWSIZE"} = $conf{"LDWINDOWSIZE"};
	}

	$self->{"conf"}->{"DEFAULTLDWINDOWSIZE"} = -1;

	if ($conf{"MIN_NEIGHBOR_NUM"} ne "")
	{
		$self->{"conf"}->{"MIN_NEIGHBOR_NUM"} = $conf{"MIN_NEIGHBOR_NUM"};
	}

	if ($conf{"OUT_DIR"} ne "")
	{
		if ($conf{"OUT_DIR"} =~/\/$/)
		{
			$self->{"conf"}->{"OUT_DIR"} = $conf{"OUT_DIR"};
		}
		else
		{
			$self->{"conf"}->{"OUT_DIR"} = $conf{"OUT_DIR"}."/";
		}
	}

	if ($conf{"BEDFILE_IS_SORTED"} ne "")
	{
		if ($conf{"BEDFILE_IS_SORTED"} =~ /^true/i)
		{
			$self->{"conf"}->{"BEDFILE_IS_SORTED"} = "True";
		}
		else
		{
			$self->{"conf"}->{"BEDFILE_IS_SORTED"} = "False";
		}
	}

	$self->{"conf"}->{"SORTED_BED_FILE_DIR"} = $self->{"conf"}->{"OUT_DIR"}."sortedBedFiles/";

	if ($conf{"POPULATION"} ne "")
	{
		$self->{"conf"}->{"POPULATION"} = $conf{"POPULATION"};

		$self->{"conf"}->{"REF_DIR"} =  $self->{"conf"}->{"REF_DIR"}.$self->{"conf"}->{"POPULATION"}."/";
	}

	if (defined($conf{"BATCHOPTS"}))
	{
		$self->{"conf"}->{"BATCHOPTS"} = " ".$conf{"BATCHOPTS"}." ";
	}
	else
	{
		$self->{"conf"}->{"BATCHOPTS"} = "";
	}

	my $batchtype = $conf{"BATCHTYPE"};

	if ($batchtype =~ /^MOSIX$/i)
	{
		$self->{"conf"}->{"BATCHTYPE"} = "mosbatch";

		$self->{"conf"}->{"BATCHCMD"} = $self->{"conf"}->{"BATCHTYPE"}." ".$self->{"conf"}->{"BATCHOPTS"}." ";
	}
	elsif ($batchtype =~ /^slurm$/i)
	{
		$self->{"conf"}->{"BATCHTYPE"} = "srun";
		$self->{"conf"}->{"BATCHCMD"} = $self->{"conf"}->{"BATCHTYPE"}." ".$self->{"conf"}->{"BATCHOPTS"}." ";
	}
	elsif ($batchtype =~ /^local$/i)
	{
		$self->{"conf"}->{"BATCHTYPE"} = "local";
		$self->{"conf"}->{"BATCHCMD"} = " ";
	}
	else
	{
		$self->{"conf"}->{"BATCHTYPE"} = "error";
	}

	if ($conf{"TOPNBEDFILES"} ne "")
	{
		$self->{"conf"}->{"TOPNBEDFILES"} = $conf{"TOPNBEDFILES"};
	}

	if ($conf{"JOBNUMBER"} ne "")
	{
		$self->{"conf"}->{"JOBNUMBER"} = $conf{"JOBNUMBER"};
	}

	$self->{"conf"}->{"INDEX_DIR"} = $self->{"conf"}->{"OUT_DIR"}."index_SNP/";
	$self->{"conf"}->{"NEIGHBOR_DIR"} = $self->{"conf"}->{"OUT_DIR"}."neighbor_SNP/";
	$self->{"conf"}->{"CUBE_DIR"} = $self->{"conf"}->{"OUT_DIR"}."cube/";
	
	$self->{"conf"}->{"SCRIPT_DIR"} = "$Bin/../script/";
}

sub ReadReferenceLDBuddyThreshold
{
	my $self = shift;

	my $refDIR = $self->{"conf"}->{"REF_DIR"};

	my $refLDBuddyThresholdFile = $refDIR."reference.LD.buddy.threshold.txt";

	if (!(-e $refLDBuddyThresholdFile))
	{
		print "Can't find reference LD buddy Threshold file. Please re-download reference data!\n";

		exit(1);
	}

	open (SUBIN,$refLDBuddyThresholdFile) || die "can't open the file:$refLDBuddyThresholdFile!\n";

	my $subreadline;

	while (defined($subreadline=<SUBIN>))
	{
		chomp $subreadline;

		my @fields = split(/\=/,$subreadline);

		if ($fields[0] eq "DEFAULTR2THRESHOLD")
		{
			$self->{"conf"}->{"DEFAULTR2THRESHOLD"} = $fields[1];
		}

		if ($fields[0] eq "DEFAULTLDWINDOWSIZE")
		{
			$self->{"conf"}->{"DEFAULTLDWINDOWSIZE"} = $fields[1];
		}
	}

	close SUBIN;
}

sub VerifyConf
{
	my $self = shift;

	if (!(defined($self->{"conf"}->{"INDEX_SNP_FILE"})))
	{
		print "You need define index SNP file!\n";

		exit(1);
	}
	else
	{	
		if (!(-e $self->{"conf"}->{"INDEX_SNP_FILE"}))
		{
			print "Index SNP file doesn't exist!\n";

			exit(1);
		}
	}

	if (!(defined($self->{"conf"}->{"BED_FILE_INDEX"})))
	{
		print "You need define index of bed files!\n";

		exit(1);
	}
	else
	{
		if (!(-e $self->{"conf"}->{"BED_FILE_INDEX"}))
		{
			print "Bed file index doesn't exist!\n";

			exit(1);
		}
	}

	if (!defined($self->{"conf"}->{"REF_DIR"}))
	{
		print "Please specify the directory of reference files!\n";

		exit(1);
	}
	else
	{
		if (!(-e $self->{"conf"}->{"REF_DIR"}))
		{
			print "The reference directory (".$self->{"conf"}->{"REF_DIR"}.") which you defined in config file doesn't exist!\n";

			exit(1);
		}
	}

	if (!defined($self->{"conf"}->{"R2THRESHOLD"}))
	{
		print "Please specify r2 threshold for LD buddy!\n";

		exit(1);
	}
	elsif ($self->{"conf"}->{"R2THRESHOLD"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
	{
		print "r2 threshold for LD buddy should be a number!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"DEFAULTR2THRESHOLD"}))
	{
		print "Can't read reference r2 threshold for LD buddy!\n";

		exit(1);
	}
	
	if ($self->{"conf"}->{"DEFAULTR2THRESHOLD"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
	{
		print "The reference r2 threshold for LD buddy should be a number!\n";

		exit(1);
	}
		
	if (($self->{"conf"}->{"DEFAULTR2THRESHOLD"} <= 0) || (1 <= $self->{"conf"}->{"DEFAULTR2THRESHOLD"}))
	{
		print "The reference r2 threshold for LD buddy should be in (0,1)!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"LDWINDOWSIZE"}))
	{
		print "Please specify LD window size for LD buddy!\n";

		exit(1);
	}
	elsif ($self->{"conf"}->{"LDWINDOWSIZE"} !~ /^\d+$/)
	{
		print "LD window size should be a number!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"DEFAULTLDWINDOWSIZE"}))
	{
		print "Can't read reference LD buddy window size threshold!\n";

		exit(1);
	}
	
	if ($self->{"conf"}->{"DEFAULTLDWINDOWSIZE"} !~ /^\d+$/)
	{
		print "The reference LD buddy window size threshold should be a number!\n";

		exit(1);
	}
		
	if ($self->{"conf"}->{"DEFAULTLDWINDOWSIZE"} <= 0)
	{
		print "The reference LD buddy window size threhold should be greater than 0!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"OUT_DIR"}))
	{
		print "Please specify out result directory!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"MIN_NEIGHBOR_NUM"}))
	{
		print "Please specify the number of SNP neighbors!\n";

		exit(1);
	}
	elsif ($self->{"conf"}->{"MIN_NEIGHBOR_NUM"} !~ /^\d+$/)
	{
		print "MIN_NEIGHBOR_NUM should be a number!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"BEDFILE_IS_SORTED"}))
	{
		print "Please specify bed file is soretd or not!\n";
		
		exit(1);
	}

	if (!(defined($self->{"conf"}->{"POPULATION"})))
	{
		print "Please define the population to EUR, AFR, AMR, ASN or SAN!\n";

		exit(1);
	}

	if (($self->{"conf"}->{"POPULATION"} ne "EUR")&&($self->{"conf"}->{"POPULATION"} ne "AFR")&&($self->{"conf"}->{"POPULATION"} ne "AMR")&&($self->{"conf"}->{"POPULATION"} ne "ASN")&&($self->{"conf"}->{"POPULATION"} ne "SAN"))
	{
		print "The population should be defined to EUR, AFR, AMR, ASN or SAN!\n";

		exit(1);
	}

	if (!defined($self->{"conf"}->{"BATCHTYPE"}))
	{
		print "Please specify BATCHTYPE for parallel computing!\n";

		exit(1);
	}

	if ($self->{"conf"}->{"BATCHTYPE"} =~ /^error$/i)
	{
		print "Please define BATCHTYPE to mosbatch, slurm or local!\n";

		exit(1);
	}

	if (defined($self->{"conf"}->{"TOPNBEDFILES"}))
	{
		if ($self->{"conf"}->{"TOPNBEDFILES"} !~ /^\d+$/)
		{
			print "Please specify top N bed files! It should be a number!\n";

			exit(1);
		}
	}

	if (defined($self->{"conf"}->{"JOBNUMBER"}))
	{
		if ($self->{"conf"}->{"JOBNUMBER"} !~ /^\d+$/)
		{
			print "Please specify the job number when runing!\n";

			exit(1);
		}
	}
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

sub CheckBedFiles
{
	my $self = shift;

	print "We only test whether the bed file exist and the first 10 lines are bed file format (chr	start	end	...)!\n";

	print "If the other lines in bed file are not this format, the tool will be crashed!\n\n";

	my $bedFileIndex = $self->{"conf"}->{"BED_FILE_INDEX"};

	open (IN,$bedFileIndex) || die "can't open the bed file index!\n";

	my $readline;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		if (-e $readline)
		{
			my $type = getFileType($readline);

			if ($type ne "ASCII")
			{
				print "The bed file ($readline) is not a ASCII file! If it is gz file, please unzip it firstly!\n";

				exit(1);
			}
			else
			{
				open (BEDIN,$readline) || die "can't open the file!\n";

				my $thisLine;

				for (my $i = 0; $i < 10; $i++)
				{
					if (defined($thisLine=<BEDIN>))
					{
						my @fields = split(/\t/,$thisLine);

						if (int(@fields) < 3)
						{
							print "One line ($thisLine) in bed file ($readline) doesn't have the bed information!\n";

							print "Please remove this line from bed file firstly!\n";

							exit(1);
						}
						else
						{
							my $chr = $fields[0];
							my $start = $fields[1];
							my $end = $fields[2];

							$chr =~ s/^chr//i;

							if ($chr =~ /^x$/i)
							{
								$chr = 23;
							}
							elsif ($chr =~ /^y$/i)
							{
								$chr = 24;
							}

							if (($chr !~ /^(\d+)$/)||($start !~ /^(\d+)$/)||($end !~ /^(\d+)$/))
							{
								print "One line ($thisLine) in bed file ($readline) doesn't have the bed information!\n";

								print "Please remove this line from bed file firstly!\n";

								exit(1);
							}
						}
					}
				}

				close BEDIN;

				print "Bed file ($readline) passes the test!\n";
			}
		}
		else
		{
			print "One bed file ($readline) in your index of bed files doesn't exist!\n";

			exit(1);
		}
	}

	close IN;
}

sub CheckSNPList
{
	my $self = shift;

	my $snpList = $self->{"conf"}->{"INDEX_SNP_FILE"};

	open (IN,$snpList) || die "can't open the index SNP List!\n";

	my $readline;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		$readline =~ s/^chr//i;

		if ($readline =~ /^rs/i)
		{
			my $tmp = $readline;
			$tmp =~ s/^rs//i;

			if ($tmp !~ /^\d+$/)
			{
				print "$readline is not a SNP or wrong format!\n";

				print "The format of index SNP should be chrZ:ZZZ or rsZZZZ!\n";

				exit(1);
			}
		}
		else
		{
			if ($readline !~ /^(X|x|Y|y|(\d+)):(\d+)$/)
			{
				print "$readline is not a SNP or wrong format!\n";

				print "The format of index SNP should be chrZ:ZZZ or rsZZZZ!\n";

				exit(1);
			}
		}
	}

	close IN;
}

sub CreateAllDIR
{
	my $self = shift;

	`mkdir --p $self->{"conf"}->{"OUT_DIR"}`;
	`mkdir --p $self->{"conf"}->{"INDEX_DIR"}`;
	`mkdir --p $self->{"conf"}->{"NEIGHBOR_DIR"}`;
	`mkdir --p $self->{"conf"}->{"CUBE_DIR"}`;
	`mkdir --p $self->{"conf"}->{"SORTED_BED_FILE_DIR"}`;
}

sub CreateMakeFile
{
	my $self = shift;

	my $makefile = $self->{"conf"}->{"OUT_DIR"}."MakeFile";

	my $logFile = $self->{"conf"}->{"OUT_DIR"}."GREGOR.log";

	my $perlCMD = "perl";

	my $infileDIR;
	my $outfileDIR;

	my $refDIR							= $self->{"conf"}->{"REF_DIR"};
	my $scriptDIR						= $self->{"conf"}->{"SCRIPT_DIR"};
	my $r2Threshold					= $self->{"conf"}->{"R2THRESHOLD"};
	my $defaultR2Threshold	= $self->{"conf"}->{"DEFAULTR2THRESHOLD"};
	my $ldWindowSize				= $self->{"conf"}->{"LDWINDOWSIZE"};
	my $defaultLdWindowSize	= $self->{"conf"}->{"DEFAULTLDWINDOWSIZE"};
	my $minNeighborNum			= $self->{"conf"}->{"MIN_NEIGHBOR_NUM"};
	my $bedFileIndex				= $self->{"conf"}->{"BED_FILE_INDEX"};
	my $sortedBedFileDIR		= $self->{"conf"}->{"SORTED_BED_FILE_DIR"};

	my @unsortBedFiles;
	undef @unsortBedFiles;
	my @sortedBedFiles;
	undef @sortedBedFiles;
	my @sortedBedOKFiles;
	undef @sortedBedOKFiles;
	my @bedFileResultDIR;
	undef @bedFileResultDIR;

	if ($r2Threshold < $defaultR2Threshold)
	{
		print "R2THRESHOLD in config file should not be less than $defaultR2Threshold!\n ";

		exit(1);
	}

	my $batchcmd	= "";
	my $cmdSuffix	= "";

	if ($self->{"conf"}->{"BATCHCMD"} =~ /mosbatch/i)
	{
		$batchcmd = $self->{"conf"}->{"BATCHCMD"}." \'";
		$cmdSuffix = " \' ";
	}
	elsif ($self->{"conf"}->{"BATCHCMD"} =~ /srun/i)
	{
		$batchcmd = $self->{"conf"}->{"BATCHCMD"}." ";
		$cmdSuffix = " ";
	}
	else ## run on local
	{                                                                                                                                                                                                                                     
		$batchcmd = " ";
		$cmdSuffix = " ";
	}


## Read Bed Files from Bed index File
	open (IN,$bedFileIndex) || die "can't open the file $bedFileIndex";

	my $readline;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		my $k = int(@unsortBedFiles);

		$unsortBedFiles[$k] = $readline;
	}

	close IN;

	if ($self->{"conf"}->{"BEDFILE_IS_SORTED"} ne "True")
	{
		 for (my $i = 0; $i < int(@unsortBedFiles); $i++)
		 {
			 my @fields = split(/\//,$unsortBedFiles[$i]);
			 my $k = int(@fields) - 1;
			 my $bedFileName = $fields[$k];
				
			 $sortedBedFiles[$i] = $sortedBedFileDIR.$bedFileName.".sorted";

			 $sortedBedOKFiles[$i] = $sortedBedFileDIR.$bedFileName.".sorted.OK";
		 }		
	}
	else
	{
		for (my $i = 0; $i < int(@unsortBedFiles); $i++)
		{
			my @fields = split(/\//,$unsortBedFiles[$i]);
			my $k = int(@fields) - 1;
			my $bedFileName = $fields[$k];

			$sortedBedFiles[$i] = $unsortBedFiles[$i];

			$sortedBedOKFiles[$i] = $sortedBedFileDIR.$bedFileName.".sorted.OK";
		}
	}

	for (my $i = 0; $i < int(@unsortBedFiles); $i++)
	{
		my @fields = split(/\//,$unsortBedFiles[$i]);
		my $k = int(@fields) - 1;
		my $bedFileName = $fields[$k];

		$bedFileResultDIR[$i] = $self->{"conf"}->{"OUT_DIR"}.$bedFileName."/";

		`mkdir --p $bedFileResultDIR[$i]`;
	}

	open (OUT,">".$makefile) || die "can't write to the file $makefile!\n";

	if (($r2Threshold != $defaultR2Threshold)||($ldWindowSize != $defaultLdWindowSize))
	{
############################################################################################

		print OUT ".DELETE_ON_ERROR:\n\n";

		print OUT "all\t:\t".$self->{"conf"}->{"OUT_DIR"}."StatisticSummaryFile.txt.OK\n\n";

############################################################################################
		$outfileDIR = $self->{"conf"}->{"OUT_DIR"};

		print OUT $outfileDIR."StatisticSummaryFile.txt.OK\t:";
		
		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			print OUT "\t".$bedFileResultDIR[$i]."PValue.txt.OK";
		}
		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."create.statistic.summary.file.pl --statisticSummaryFile ".$outfileDIR."StatisticSummaryFile.txt --resultDIR ".$outfileDIR." --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch $outfileDIR"."StatisticSummaryFile.txt.OK\n\n";

############################################################################################
		$infileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			print OUT $bedFileResultDIR[$i]."PValue.txt.OK\t:\t".$sortedBedOKFiles[$i];

			for (my $j = 1; $j < 23; $j++)
			{
				print OUT "\t".$bedFileResultDIR[$i]."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK";
			}
			print OUT "\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."calculatePvalue.pl --BedFilesDIR $bedFileResultDIR[$i] --neighborFile $infileDIR"."index.snp.neighbors.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch $bedFileResultDIR[$i]"."PValue.txt.OK\n\n";
		}


############################################################################################
		my $indexDIR = $self->{"conf"}->{"INDEX_DIR"};
		my $neighborDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			for (my $j = 1; $j < 23; $j++)
			{
				print OUT $bedFileResultDIR[$i]."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK\t:\t".$sortedBedOKFiles[$i]."\t".$indexDIR."index.snp.txt.OK\t".$neighborDIR."neighbor.chr$j.LDbuddy.txt.OK\n";

				print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."overlap.pl --indexSNPList ".$indexDIR."index.snp.LD.txt --neighborSNPList ".$neighborDIR."neighbor.chr$j.LDbuddy.txt --chrid $j --sortedBedFile $sortedBedFiles[$i] --resultDIR $bedFileResultDIR[$i]  --logFile $logFile".$cmdSuffix."\n";
				print OUT "\ttouch $bedFileResultDIR[$i]"."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK\n\n";
			}
		}

############################################################################################

		if ($self->{"conf"}->{"BEDFILE_IS_SORTED"} ne "True")
		{
			for (my $i = 0; $i < int(@unsortBedFiles); $i++)
			{
				print OUT $sortedBedOKFiles[$i]."\t:\t".$unsortBedFiles[$i]."\n";

				print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."sort.bed.file.pl --bedFile ".$unsortBedFiles[$i]." --sortedBedFile ".$sortedBedFiles[$i]." --logFile $logFile".$cmdSuffix."\n";
				print OUT "\ttouch ".$sortedBedOKFiles[$i]."\n\n";
			}
		}
		else
		{
			for (my $i = 0; $i < int(@sortedBedFiles); $i++)
			{
				print OUT $sortedBedOKFiles[$i]."\t:\t".$sortedBedFiles[$i]."\n";
				print OUT "\ttouch ".$sortedBedOKFiles[$i]."\n\n";
			}
		}

############################################################################################

		$infileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};
		$outfileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT $outfileDIR."neighbor.chr$i.LDbuddy.txt.OK\t:\t$infileDIR"."index.snp.neighbors.txt.OK\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."find.neighbors.LDbuddy.pl --neighborlist ".$infileDIR."index.snp.neighbors.txt --refDIR $refDIR --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --chrid $i --neighborLDlist ".$outfileDIR."neighbor.chr$i.LDbuddy.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch ".$outfileDIR."neighbor.chr$i.LDbuddy.txt.OK\n\n";
		}

############################################################################################

		$infileDIR = $self->{"conf"}->{"CUBE_DIR"};
		$outfileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		print OUT $outfileDIR."index.snp.neighbors.txt.OK\t:\t".$self->{"conf"}->{"INDEX_DIR"}."index.snp.txt.OK";

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT "\t".$infileDIR."chr$i.maf.dist.ldnum.id.txt.OK";
		}

		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."find.neighbors.pl --indexSNPFile ".$self->{"conf"}->{"INDEX_DIR"}."annotated.index.snp.txt --cubeFileDIR ".$infileDIR." --minNeighbor ".$minNeighborNum." --indexSNPNeighborFile ".$outfileDIR."index.snp.neighbors.txt --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$outfileDIR."index.snp.neighbors.txt.OK\n\n";

############################################################################################

		$infileDIR = $self->{"conf"}->{"CUBE_DIR"};
		$outfileDIR = $self->{"conf"}->{"INDEX_DIR"};

		print OUT $outfileDIR."index.snp.txt.OK\t:\t".$self->{"conf"}->{"INDEX_SNP_FILE"}." ".$infileDIR."cube.id.txt.OK\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."annotate.index.snp.pl --indexSNPList ".$self->{"conf"}->{"INDEX_SNP_FILE"}." --refDIR $refDIR --cubeIDFile ".$infileDIR."cube.id.txt --r2Threshold ".$r2Threshold." --ldWindowSize ".$ldWindowSize." --annotatedList ".$outfileDIR."annotated.index.snp.txt --nonannotatedList ".$outfileDIR."nonannoted.index.snp.txt --rsidSNPList ".$outfileDIR."rsid.index.snp.txt --indexSNPLDList ".$outfileDIR."index.snp.LD.txt --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$outfileDIR."index.snp.txt.OK\n\n";

############################################################################################

		$infileDIR = $self->{"conf"}->{"CUBE_DIR"};
		$outfileDIR = $self->{"conf"}->{"CUBE_DIR"};

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT $outfileDIR."chr$i.maf.dist.ldnum.id.txt.OK\t:\t".$infileDIR."cube.id.txt.OK ".$infileDIR."chr$i.maf.dist.ldnum.txt.OK\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."put.snp.in.cubes.pl --chrfile ".$infileDIR."chr$i.maf.dist.ldnum.txt --chrid $i --cubeIDFile ".$infileDIR."cube.id.txt --out ".$outfileDIR."chr$i.maf.dist.ldnum.id.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch ".$outfileDIR."chr$i.maf.dist.ldnum.id.txt.OK\n\n";
		}

############################################################################################

		$infileDIR = $self->{"conf"}->{"CUBE_DIR"};
		$outfileDIR = $self->{"conf"}->{"CUBE_DIR"};

		print OUT $outfileDIR."cube.id.txt.OK\t:";

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT "\t".$outfileDIR."chr$i.maf.dist.ldnum.txt.OK";
		}

		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."calculate.cube.id.pl --chrDIR ".$outfileDIR." --out ".$outfileDIR."cube.id.txt --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$outfileDIR."cube.id.txt.OK\n\n";


############################################################################################

		$infileDIR = $self->{"conf"}->{"REF_DIR"};
		$outfileDIR = $self->{"conf"}->{"CUBE_DIR"};

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT $outfileDIR."chr$i.maf.dist.ldnum.txt.OK\t:\t".$infileDIR."CHR$i.db\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."calculate.maf.dist.ldnum.pl --chrid ".$i." --refDIR $refDIR --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --chrout ".$outfileDIR."chr$i.maf.dist.ldnum.txt --distributionFile ".$outfileDIR."chr$i.distribution.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch ".$outfileDIR."chr$i.maf.dist.ldnum.txt.OK\n\n";
		}
	}
	else
	{
############################################################################################

		print OUT ".DELETE_ON_ERROR:\n\n";

		print OUT "all\t:\t".$self->{"conf"}->{"OUT_DIR"}."StatisticSummaryFile.txt.OK\n\n";

############################################################################################
		$outfileDIR = $self->{"conf"}->{"OUT_DIR"};

		print OUT $outfileDIR."StatisticSummaryFile.txt.OK\t:";
		
		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			print OUT "\t".$bedFileResultDIR[$i]."PValue.txt.OK";
		}
		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."create.statistic.summary.file.pl --statisticSummaryFile ".$outfileDIR."StatisticSummaryFile.txt --resultDIR ".$outfileDIR." --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch $outfileDIR"."StatisticSummaryFile.txt.OK\n\n";

############################################################################################
		$infileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			print OUT $bedFileResultDIR[$i]."PValue.txt.OK\t:\t".$sortedBedOKFiles[$i];

			for (my $j = 1; $j < 23; $j++)
			{
				print OUT "\t".$bedFileResultDIR[$i]."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK";
			}
			print OUT "\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."calculatePvalue.pl --BedFilesDIR $bedFileResultDIR[$i] --neighborFile $infileDIR"."index.snp.neighbors.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch $bedFileResultDIR[$i]"."PValue.txt.OK\n\n";
		}


############################################################################################
		my $indexDIR = $self->{"conf"}->{"INDEX_DIR"};
		my $neighborDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 0; $i < int(@sortedBedOKFiles); $i++)
		{
			for (my $j = 1; $j < 23; $j++)
			{
				print OUT $bedFileResultDIR[$i]."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK\t:\t".$sortedBedOKFiles[$i]."\t".$indexDIR."index.snp.txt.OK\t".$neighborDIR."neighbor.chr$j.LDbuddy.txt.OK\n";

				print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."overlap.pl --indexSNPList ".$indexDIR."index.snp.LD.txt --neighborSNPList ".$neighborDIR."neighbor.chr$j.LDbuddy.txt --chrid $j --sortedBedFile $sortedBedFiles[$i] --resultDIR $bedFileResultDIR[$i]  --logFile $logFile".$cmdSuffix."\n";
				print OUT "\ttouch $bedFileResultDIR[$i]"."neighbor.on.chr$j.LDbuddy.in.bed.txt.OK\n\n";
			}
		}

############################################################################################

		if ($self->{"conf"}->{"BEDFILE_IS_SORTED"} ne "True")
		{
			for (my $i = 0; $i < int(@unsortBedFiles); $i++)
			{
				print OUT $sortedBedOKFiles[$i]."\t:\t".$unsortBedFiles[$i]."\n";

				print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."sort.bed.file.pl --bedFile ".$unsortBedFiles[$i]." --sortedBedFile ".$sortedBedFiles[$i]." --logFile $logFile".$cmdSuffix."\n";
				print OUT "\ttouch ".$sortedBedOKFiles[$i]."\n\n";
			}
		}
		else
		{
			for (my $i = 0; $i < int(@sortedBedFiles); $i++)
			{
				print OUT $sortedBedOKFiles[$i]."\t:\t".$sortedBedFiles[$i]."\n";
				print OUT "\ttouch ".$sortedBedOKFiles[$i]."\n\n";
			}
		}

############################################################################################

		$infileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};
		$outfileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT $outfileDIR."neighbor.chr$i.LDbuddy.txt.OK\t:\t$infileDIR"."index.snp.neighbors.txt.OK\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."find.neighbors.LDbuddy.pl --neighborlist ".$infileDIR."index.snp.neighbors.txt --refDIR $refDIR --r2Threshold $r2Threshold --ldWindowSize $ldWindowSize --chrid $i --neighborLDlist ".$outfileDIR."neighbor.chr$i.LDbuddy.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch ".$outfileDIR."neighbor.chr$i.LDbuddy.txt.OK\n\n";
		}

############################################################################################

		$infileDIR = $refDIR;
		$outfileDIR = $self->{"conf"}->{"NEIGHBOR_DIR"};

		print OUT $outfileDIR."index.snp.neighbors.txt.OK\t:\t".$self->{"conf"}->{"INDEX_DIR"}."index.snp.txt.OK";

		for (my $i = 1; $i < 23; $i++)
		{
			print OUT "\t".$infileDIR."chr$i.maf.dist.ldnum.id.txt";
		}

		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."find.neighbors.pl --indexSNPFile ".$self->{"conf"}->{"INDEX_DIR"}."annotated.index.snp.txt --cubeFileDIR ".$infileDIR." --minNeighbor ".$minNeighborNum." --indexSNPNeighborFile ".$outfileDIR."index.snp.neighbors.txt --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$outfileDIR."index.snp.neighbors.txt.OK\n\n";

############################################################################################

		$infileDIR = $refDIR;
		$outfileDIR = $self->{"conf"}->{"INDEX_DIR"};

		print OUT $outfileDIR."index.snp.txt.OK\t:\t".$self->{"conf"}->{"INDEX_SNP_FILE"}." ".$infileDIR."cube.id.txt\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."annotate.index.snp.pl --indexSNPList ".$self->{"conf"}->{"INDEX_SNP_FILE"}." --refDIR $refDIR --cubeIDFile ".$infileDIR."cube.id.txt --r2Threshold ".$r2Threshold." --ldWindowSize ".$ldWindowSize." --annotatedList ".$outfileDIR."annotated.index.snp.txt --nonannotatedList ".$outfileDIR."nonannoted.index.snp.txt --rsidSNPList ".$outfileDIR."rsid.index.snp.txt --indexSNPLDList ".$outfileDIR."index.snp.LD.txt --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$outfileDIR."index.snp.txt.OK\n\n";
	}

	close OUT;
}

sub CreateTopNBedMakeFile
{
	my $self = shift;

	my $scriptDIR = $self->{"conf"}->{"SCRIPT_DIR"};

  my $makefile = $self->{"conf"}->{"OUT_DIR"}."TopNBed.MakeFile";

  my $logFile = $self->{"conf"}->{"OUT_DIR"}."GREGOR.log";

	my $perlCMD = "perl";

	my $bedFileIndex = $self->{"conf"}->{"BED_FILE_INDEX"};
	my $sortedBedFileDIR = $self->{"conf"}->{"SORTED_BED_FILE_DIR"};
	my $StatisticSummaryFile = $self->{"conf"}->{"OUT_DIR"}."StatisticSummaryFile.txt";

	my $batchcmd  = "";
	my $cmdSuffix = "";
	
	if ($self->{"conf"}->{"BATCHCMD"} =~ /mosbatch/i)
	{
		$batchcmd = $self->{"conf"}->{"BATCHCMD"}." \'";
		$cmdSuffix = " \' ";
	}
	elsif ($self->{"conf"}->{"BATCHCMD"} =~ /srun/i)
	{
		$batchcmd = $self->{"conf"}->{"BATCHCMD"}." ";
		$cmdSuffix = " ";
	}
	else ## run on local
	{
		$batchcmd = " ";
		$cmdSuffix = " ";
	}

	open (IN,$StatisticSummaryFile) || die "can't open the file!\n";

	my $readline = <IN>;

	my %pValueHash;
	undef %pValueHash;

	while (defined($readline=<IN>))
	{
		chomp $readline;

		my @fields = split(/\t/,$readline);
		my $bedFile = $fields[0];
		my $pvalue = $fields[3];

		if ($pvalue =~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
		{
			$pValueHash{$bedFile} = $pvalue;
		}
	}

	close IN;

	my @pValueArr;
	undef @pValueArr;

	foreach my $bedFile (sort{$pValueHash{$a}<=>$pValueHash{$b}} keys %pValueHash)
	{
		my $k = int(@pValueArr);
		$pValueArr[$k] = $bedFile;
	}

	my $topN = $self->{"conf"}->{"TOPNBEDFILES"};

	if ($topN > int(@pValueArr))
	{
		$topN = int(@pValueArr);
	}

	my @sortedBedFiles;
	my @sortedBedOKFiles;
	undef @sortedBedFiles;
	undef @sortedBedOKFiles;

	if ($self->{"conf"}->{"BEDFILE_IS_SORTED"} ne "True")
	{
		for (my $i = 0; $i < int(@pValueArr); $i++)
		{
			my $bedFileName = $pValueArr[$i];
			
			$sortedBedFiles[$i] = $self->{"conf"}->{"OUT_DIR"}."sortedBedFiles/".$bedFileName.".sorted";
			
			$sortedBedOKFiles[$i] = $self->{"conf"}->{"OUT_DIR"}."sortedBedFiles/".$bedFileName.".sorted.OK";
		}
	}
	else
	{
## Read Bed Files from Bed index File
		open (IN,$bedFileIndex) || die "can't open the file $bedFileIndex";
		
		my %bedFileHash;
		undef %bedFileHash;

		while (defined($readline=<IN>))
		{
			chomp $readline;
			my @fields = split(/\//,$readline);
			my $k = int(@fields) - 1;
			my $bedFileName = $fields[$k];

			$bedFileHash{$bedFileName} = $readline;
		}
		
		close IN;

		for (my $i = 0; $i < int(@pValueArr); $i++)
		{
			my $bedFileName = $pValueArr[$i];
			
			if (exists($bedFileHash{$bedFileName}))
			{
				$sortedBedFiles[$i] = $bedFileHash{$bedFileName};
			
				$sortedBedOKFiles[$i] = $self->{"conf"}->{"OUT_DIR"}."sortedBedFiles/".$bedFileName.".sorted.OK";
			}
			else
			{
				print "can't find the bed file: $bedFileName in bed index file!\n";

				exit(1);
			}
		}
	}

	my $topNDIR = $self->{"conf"}->{"OUT_DIR"}."index.SNP.and.LD.for.top.$topN.bed/";

	`mkdir --p $topNDIR`;

	open (OUT,">".$makefile) || die "can't write to the file:$makefile!\n";

## create MakeFile
############################################################################################
	print OUT ".DELETE_ON_ERROR:\n\n";

	print OUT "all\t:\t".$self->{"conf"}->{"OUT_DIR"}."top.$topN.bed.OK\n\n";

############################################################################################
	
	print OUT $self->{"conf"}->{"OUT_DIR"}."top.$topN.bed.OK\t:";

	for (my $i = 0; $i < $topN; $i++)
	{
		print OUT "\t".$topNDIR."index.SNP.and.LD.in.bed.".$pValueArr[$i].".txt.OK";	
	}

	print OUT "\n";

	print OUT "\ttouch ".$self->{"conf"}->{"OUT_DIR"}."top.$topN.bed.OK\n\n";

############################################################################################

	for (my $i = 0; $i < $topN; $i++)
	{
		print OUT $topNDIR."index.SNP.and.LD.in.bed.".$pValueArr[$i].".txt.OK\t:";

		for (my $j = 1; $j < 23; $j++)
		{
			print OUT "\t".$topNDIR.$pValueArr[$i].".chr$j.txt.OK";
		}

		print OUT "\n";

		print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."merge.index.SNP.and.LD.in.bed.pl --bedFileName $pValueArr[$i] --inDIR $topNDIR --outDIR $topNDIR --logFile $logFile".$cmdSuffix."\n";
		print OUT "\ttouch ".$topNDIR.$pValueArr[$i].".txt.OK\n\n";
	}

############################################################################################
	for (my $i = 0; $i < $topN; $i++)
	{
		for (my $j = 1; $j < 23; $j++)
		{
			print OUT $topNDIR.$pValueArr[$i].".chr$j.txt.OK\t:\t".$self->{"conf"}->{"OUT_DIR"}."StatisticSummaryFile.txt.OK\n";

			print OUT "\t".$batchcmd." $perlCMD ".$scriptDIR."check.index.snp.and.lds.in.bed.pl --indexSNPLDFile ".$self->{"conf"}->{"OUT_DIR"}."index_SNP/index.snp.LD.txt --sortedBedFile $sortedBedFiles[$i] --chrid $j --SNPInBedFile $topNDIR"."$pValueArr[$i].chr$j.txt --logFile $logFile".$cmdSuffix."\n";
			print OUT "\ttouch ".$topNDIR.$pValueArr[$i].".chr$j.txt.OK\n\n";
		}
	}

	close OUT;
}

1;
