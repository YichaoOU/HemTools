#!/usr/bin/env perl
use warnings;
use POSIX;

my $maxCPUs = 1;

sub printCMD() {
	print STDERR "\n\tUsage: tagDir2hicFile.pl <tag directory> [options]\n";
	print STDERR "\n\tBy default, this program will output a file in \"HiC summary\" format to stdout:\n";
	print STDERR "\t\tid<tab>chr1<tab>pos1<tab>strand1<tab>chr2<tab>pos2<tab>strand2\n";
	print STDERR "\n\tOptions below can be set to help output a *.hic file for use with juicebox/juicer\n";
	print STDERR "\n\tOptions (most are for use with juicer):\n";
	print STDERR "\t\t-juicer <filename.hic> (create *.hic file with juicer, \"-juicer auto\" places file in tagdir)\n";
	print STDERR "\t\t-genome <genome> (genome is passed on to juicer_tools - if using a normal genome, i.e. hg38,\n";
	print STDERR "\t\t\tmm10, etc. it's probably best to specify the genome code - if juicer_tools can recognize it.\n";
	print STDERR "\t\t\tOtherwise specify the path to a chrom.sizes file instead of the genome code)\n";
	print STDERR "\t\t-juicerExe <\"command to run juicer_tools\"> (executable for running juicer_tools,\n";
	print STDERR "\t\t\tby default assumes \"juicer_tools\" is in the executable PATH)\n";
	print STDERR "\t\t-juicerOpt <\"juicer options\"> (command line options to pass to juicer, use quotes \"...\")\n";
	print STDERR "\t\t-p <#> (number of CPUs to use during sort command for juicer file creation, default: $maxCPUs)\n";
	print STDERR "\t\t-short <filename> (output read pairs in \"short format\" for processing with juicer,\n";
	print STDERR "\t\t\tbut don't run juicer_tools. This file will not be sorted the way juicer wants it)\n";
	print STDERR "\n";
	exit;
}

if (@ARGV < 1) {
	printCMD();
}
my $tagDir = $ARGV[0];
my $tagDirName = $ARGV[0];
$tagDirName =~ s/\/+$//;
$tagDirName =~ s/.*\///;
$tagDirName =~ s/\s/\-/g;

my $setLen = -1;
my $sepFlag = 0;
my $juicerFlag = 0;
my $shortFile = '';
my $juicerExe = "juicer_tools";
my $juicerOptions = "";
my $juicerGenome = "";
my $hicFile = '';
for (my $i=1;$i<@ARGV;$i++) {
	if ($ARGV[$i] eq '-len') {
		$setLen = $ARGV[++$i];
		print STDERR "\tSetting read lengths to $setLen\n";
	} elsif ($ARGV[$i] eq '-separate') {
		$sepFlag = 1;
		print STDERR "\tWill output separate reads if more than one tag is found per position\n";
	} elsif ($ARGV[$i] eq '-short') {
		$juicerFlag = 1;
		$shortFile = $ARGV[++$i];
		print STDERR "\tWill output reads in the juicer pre short format to file: $shortFile\n";
	} elsif ($ARGV[$i] eq '-genome') {
		$juicerGenome = $ARGV[++$i];
	} elsif ($ARGV[$i] eq '-juicerOpt') {
		$juicerOptions = $ARGV[++$i];
	} elsif ($ARGV[$i] eq '-juicer') {
		$hicFile = $ARGV[++$i];
		if ($hicFile eq 'auto') {
			$hicFile = $tagDir . "/" . $tagDirName . ".hic";
			print STDERR "\tWill use \"$hicFile\" for hic output file\n";
		}
		$juicerFlag = 1;
		print STDERR "\tWill output a juicer hic file to $hicFile\n";
	} elsif ($ARGV[$i] eq '-juicerExe') {
		$juicerExe = $ARGV[++$i];
		print STDERR "\tWill use \"$juicerExe\" to execute juicer.\n";
	} elsif ($ARGV[$i] eq '-p' || $ARGV[$i] eq '-cpu') {
		$maxCPUs = $ARGV[++$i];
	} else {
		print STDERR "What is $ARGV[$i]??\n";
		printCMD();
	}
}

if ($juicerFlag ==1 && $shortFile eq '' && $juicerGenome eq '') {
	print STDERR "!!! Error - you must specify a genome (-genome <...>) to work with juicer\n";
	printCMD();
}

my $dname = "ID";
my $count = 1;

my $rand = rand();
my $file = $rand . ".tmp";
my $file2 = $rand . ".2.tmp";

`ls "$ARGV[0]/"*.tags.tsv > "$file"`;	
my @files = ();
open IN, "$file";
while (<IN>) {
	chomp;
	s/\r//g;
	push(@files, $_);
}
close IN;
`rm "$file"`;

if ($juicerFlag) {
	open OUT, ">$file";
}

my $zzz = 0;

for (my $i=0;$i<@files;$i++) {
	my $tagFile = $files[$i];
	open IN, "$tagFile";
	while (<IN>) {
		chomp;
		s/\r//g;
		my @line = split /\t/;
		next if (@line < 10);
		my $name = $line[0];
		my $chr = $line[1];
		my $pos = $line[2];
		my $dir = $line[3];
		my $v = $line[4];
		my $len = $line[5];
		my $chr2 = $line[6];
		my $pos2 = $line[7];
		my $dir2 = $line[8];
		my $len2 = $line[9];


		my $cmp1 = $chr cmp $chr2;
		next if ($cmp1 > 0);
		if ($cmp1 == 0) {
			my $cmp2 = $pos <=> $pos2;
			next if ($cmp2 > 0);
		}

		if ($v == floor($v)) {
			$v = floor($v);
		}
	
		if ($juicerFlag) {
			print OUT "$dir\t$chr\t$pos\t0\t$dir2\t$chr2\t$pos2\t1\n";
			$zzz++;
			#print "R$zzz\t$dir\t$chr\t$pos\t0\t$dir2\t$chr2\t$pos2\t1\t255\t255\n";
	
		} else {
			if ($dir == 1) {
				$dir = "-";
			} else {
				$dir = '+';
			}
			if ($dir2 == 1) {
				$dir2 = "-";
			} else {
				$dir2 = '+';
			}
			print "$dname$count\t$chr\t$pos\t$dir\t$chr2\t$pos2\t$dir2\n";
		}
		$count++;

	
	}
	close IN;
}

if ($juicerFlag) {
	close OUT;

	if ($shortFile ne '') {
		`mv "$file" "$shortFile"`;
		print STDERR "\tConsider sorting file by chormosome interaction block to work with juicer...\n";
		print STDERR "\t\ti.e. sort --parallel=$maxCPUs -k2,2d -k6,6d $shortFile > output.txt\n";
		print STDERR "\tFinished.\n";
		exit;
	}
	print STDERR "\tSorting file by chormosome interaction block to work with juicer...\n";
	print STDERR "\t\ti.e. sort --parallel=$maxCPUs -k2,2d -k6,6d $file > $file2\n";
	`sort --parallel=$maxCPUs -k2,2d -k6,6d "$file" > "$file2"`;
	print STDERR "\tDone sorting, now creating *.hic file with $juicerExe:\n";
	`$juicerExe pre $juicerOptions "$file2" "$hicFile" "$juicerGenome"`;
	print STDERR "\tFinished.\n";

	#print STDERR "\tIf everything worked fine, be sure to delete the following temporary files:\n";
	#print STDERR "\t\trm \"$file\" \"$file2\"\n";
	`rm "$file" "$file2"`;
}

