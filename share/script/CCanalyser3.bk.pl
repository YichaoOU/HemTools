#!/usr/bin/perl -w

use strict;
use Cwd;
use Data::Dumper;
use Getopt::Long;
use Pod::Usage;
#use List::MoreUtils 'true';

=head1 NAME

 CCanalyser.pl

=head1 SYNOPSIS

  This script uses a sam file as input.  This needs to have been generated as follows:
  1.	Perform adaptor trimming of the raw fastq files if this has not been performed by the sequencer.  I tend to use trim_galore to do this with the paired settings.   For example: nohup trim_galore --paired Paired_end_1.fastq Paired_end_2.fastq&

  2.	If you are using 150 bp paired end reads from the Miseq then the overlapping reads need to be merged.  I use FLASH to do this.  For example
	module load flash
	nohup flash --interleaved-output Paired_end_1.fq Paired_end_2.fq&
	Then concatenate the separate files of merged and unmerged reads:
	cat out.notCombined.fastq out.extendedFrags.fastq -> Combined_reads.fastq
	
  3.	If you sequence the data with reads that are shorter than the fragments then you may not need to merge the reads with flash but you will need to merge the reads from the PE1 and PE2 by interleaving them making sure that the order of the reads is maintained.
	I have written a 
 
  4.	I normally align the fastq files with bowtie using one processor only because it is crucial that the reads are kept in strict order otherwise the script will not function properly.
	If you use more than one processor then it is crucial the reads are sorted so that they are ordered by name.
	The script only parses the first digit in the cigar string, which should be fine with bowtie but be careful with other aligners (it will only take the first digit if the cigar is 20M29M
	I tend to use m2, best and strata Ð but this is partly because m2 is needed otherwise all of the reads for alpha globin will be thrown (because of the gene duplication) so you may well want to use your own setting.
	I would use 'best' so that each read can only align once otherwise each read could be counted many times. 
	For example:
	nohup bowtie -p 1 -m 2 --best --strata --sam --chunkmb 256 --sam /databank/indices/bowtie/mm9/mm9 Sample_REdig.fastq Sample_REdig.sam &

  The script needs to have two other input files:
  1. 	A file of all of the restriction enzyme fragments in the genome.  This is best made using the script dpngenome.pl.
	The coordinates are of the middle of the restriction fragment in the format chr:start-stop
  
  2. 	A file of the input coordinates of the capture oligonucleotides it needs to in the following 9 column tab separated format.
	Be careful to ensure the /n new line is used rather than /r (as can be inserted by excel for example).
          1. Name of capture (avoid spaces in the names please)
          2. Chromosome of capture fragment
          3. Start coordinate of capture fragment
          4. End of capture fragment
          5. Chromosome of proximity exclusion
          6. Start coordinate of proximity exclusion
          7. End coordinated of proximity exclusion
          8. Position of SNP
          9. Base of SNP

  The script requires the perl modules Data::Dumper; Getopt::Long and Pod::Usage and it needs wigToBigWig.
  Depending on your system setup you may need to load wigToBigWig BEFORE running this script with the command module load ucsctools
  
  This script will create a subdirectory (of the directory the script is in) named after the sample and it will put into this wig, windowed wig and sam files of all of the reads that are to be reported
  It also outputs a sam file of all of the reads mapping to the capture region.
  In addition it outputs 2 report files.  One containing the statistics and the other containing the data relating to exclusion of duplicates.
  The script will convert the wig files to bigwig, copy them to your public folder and generate a track hub so that all you need to do is paste the url
  for the track hub into the UCSC genome browser to see the data.

=head1 EXAMPLE

 CCanalyser.pl -f input_sam_file.sam -o input_oligo_file.txt -r input_restriction_enzyme_coordinates_file.txt -s short_sample_name -pf public_folder -pu public_url
 

=head1 OPTIONS

 -f		Input filename 
 -r		Restriction coordinates filename 
 -o		Oligonucleotide position filename 
 -pf		Your public folder (e.g. /hts/data0/public/username)
 -pu		Your public url (e.g. sara.molbiol.ox.ac.uk/public/username)
 -s		Sample name (and the name of the folder it goes into)
 -w		Window size (default = 2kb)
 -i		Window increment (default = 200bp)
 -dump		Print file of unaligned reads (sam format)
 -snp		Force all capture points to contain a particular SNP
 -limit		Limit the analysis to the first n reads of the file
 -genome	Specify the genome (mm9 / hg18)
 -globin	Combines the two captures from the gene duplicates (HbA1 and HbA2)


=head1 AUTHOR

 Original release written by James Davies June 2014 (CC2)
 This release modified based on CC2 release by Jelena Telenius October 2015 (CC3)
 

=cut

# Hardcoded parameters :
my $email = 'jelena.telenius@gmail.com';
my $version = "CC3";

# Obligatory parameters :
my $oligo_filename = "UNDEFINED";
my $bigwig_folder = "/t1-data/user/config/bigwig";
my $restriction_enzyme_coords_file ="UNDEFINED";#Specifies filename of restriction coordinates (file made by dpngenome2.pl)
my $genome = "UNDEFINED";

# Optional parameters :
my $public_folder = "DATA_FOR_PUBLIC_FOLDER";
my $public_url = "UNDETERMINED_SERVER/DATA_FOR_PUBLIC_FOLDER";

# Parameters with hardcoded default value :
my $window = 2000;
my $increment = 200;
my $sample = "CaptureC";
my $use_dump =0; #whether to create an output file with all of the non-aligning sequences
my $use_snp=0; #whether to use the SNP specified in the the input file
my $use_limit=0; #whether to limit the script to analysing the first n lines
my $globin = 0; #whether to include the part of the script that combines the HbA1 and 2 tracks
my $stringent = 0;

# Code excecution start values :
my $analysis_read;
my $last_read="first";
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(); #defines the start time of the script (printed out into the report file later on)

# Without default values - defined here for visibility reasons
my $input_path;
my $help=0;
my $man=0;

# Arrays
my @oligo_data; # contains the data for the positions of the oligos and the exclusion limits
my @samheadder; # contains the headder of the sam file

# Hashes of arrays
my %dpn_data; # contains the list of DpnII fragments in the genome

# Hashes
my %data; # contains the parsed data from the sam file
my %samhash; # contains the output data for a sam file
my %fraghash; # contains the output data for each fragment, which is used to generate a wig and a mig file
my %coords_hash=(); # contains a list of all the coordinates of the mapped reads to exclude duplicates
my %counters;  # contains the data for all the counters in the script, which is outputted into the report file
my %counter_helpers; # contains some counters, for which values are iterated over the while loop, and then in the end added ot %counters hash for printing
my %cap_samhash;
my %duplicates;

# Looper testers

my $analysedReads=0;
my $notlastFragments=0;

# The GetOptions from the command line
&GetOptions
(
  	"b=s"=>\ $bigwig_folder, 			# -b		Location of UCSC genome files $genome_sizes.txt		 
	"f=s"=>\ my $input_filename_path, 		# -f		Input filename 
	"r=s"=>\ $restriction_enzyme_coords_file,	# -r		Restriction coordinates filename 
	"o=s"=>\ $oligo_filename,			# -o		Oligonucleotide position filename 
	"pf=s"=>\ $public_folder,			# -pf		Your public folder (e.g. /hts/data0/public/username)
	"pu=s"=>\ $public_url,				# -pu		Your public url (e.g. sara.molbiol.ox.ac.uk/public/username)
	"s=s"=>\ $sample,				# -s		Sample name (and the name of the folder it goes into)
	"w=i"=>\ $window,				# -w		Window size (default = 2kb)
	"i=i"=>\ $increment,				# -i		Window increment (default = 200bp)
        "dump"=>\ $use_dump,				# -dump		Print file of unaligned reads (sam format)
	"snp"=>\ $use_snp,				# -snp		Force all capture points to contain a particular SNP
	"limit=i"=>\ $use_limit,			# -limit		Limit the analysis to the first n reads of the file
	"genome=s"=>\ $genome,				# -genome	Specify the genome (mm9 / hg18)
	"globin=i"=>\ $globin,				# -globin	Combines the two captures from the gene duplicates (HbA1 and HbA2=1 ; Both alpha and beta globin =2)
	'h|help'=>\$help,				# -h or -help 	Help - prints the manual
	'man'=>\$man,					# -man  	prints the manual
	'stringent'=>\$stringent,			# -stringent 	enforces additional stringency - forces all reported subfragments to be unique
);

pod2usage(1) if $help;
pod2usage(-verbose=>2) if $man;

# Printing out the parameters in the beginning of run - Jelena added this 220515

print STDOUT "\n" ;
print STDOUT "Capture C analyser - version $version !\n" ;
print STDOUT "Developer email $email\n" ;
print STDOUT "\n" ;

print STDOUT "Starting run with parameters :\n" ;
print STDOUT "\n" ;

print STDOUT "public_folder $public_folder \n" ;
print STDOUT "public_url $public_url \n";
print STDOUT "bigwig_folder $bigwig_folder\n" ;
print STDOUT "email $email\n" ;

print STDOUT "input_filename_path $input_filename_path\n";
print STDOUT "oligo_filename $oligo_filename\n";
print STDOUT "sample $sample\n" ;
print STDOUT "restriction_enzyme_coords_file $restriction_enzyme_coords_file \n";
print STDOUT "version $version\n";
print STDOUT "window $window \n";
print STDOUT "increment $increment \n";
print STDOUT "use_dump $use_dump\n";
print STDOUT "use_snp $use_snp\n";
print STDOUT "use_limit $use_limit\n";
print STDOUT "genome $genome\n";
print STDOUT "globin $globin \n"; 
print STDOUT "stringent $stringent \n";

my $parameter_filename = "parameters_for_filtering.log";
unless (open(PARAMETERLOG, ">$parameter_filename")){die "Cannot open file $parameter_filename $! , stopped "};

print PARAMETERLOG "public_folder $public_folder \n" ;
print PARAMETERLOG "input_filename_path $input_filename_path\n";
print PARAMETERLOG "oligo_filename $oligo_filename\n";
print PARAMETERLOG "sample $sample\n" ;
print PARAMETERLOG "restriction_enzyme_coords_file $restriction_enzyme_coords_file \n";
print PARAMETERLOG "version $version\n";
print PARAMETERLOG "genome $genome\n";
print PARAMETERLOG "globin $globin \n";

pod2usage(2) unless ($input_filename_path); 

# Check parameters - fail if obligatory ones not given :

pod2usage(2) unless ($input_filename_path);
if ( ($oligo_filename eq "UNDEFINED") or ($restriction_enzyme_coords_file eq "UNDEFINED") or ($genome eq "UNDEFINED") ) { pod2usage(2);}

print STDOUT "\n";
print STDOUT "Generating output folder.. \n";

# Creates a folder for the output files to go into - this will be a subdirectory of the file that the script is in
my $current_directory = cwd;
my $output_path= "$current_directory/$sample\_$version";

print PARAMETERLOG "datafolder $output_path \n";

if (-d $output_path){}
else {mkdir $output_path};
# We don't want to chdir - as otherwise RELATIVE file paths will not work.
#chdir $output_path;



# If user did not define public folder - setting public files to be saved in the output folder :
if ( $public_folder eq "DATA_FOR_PUBLIC_FOLDER" )
{
  mkdir "$output_path/DATA_FOR_PUBLIC_FOLDER"; 
  #print STDOUT "\nPublic url and/or public folder location not set - printing visualisation files to output directory $output_path/VISUALISATION_FILES\n";
  print STDOUT "\nPublic folder location not set - printing visualisation files to output directory $output_path/DATA_FOR_PUBLIC_FOLDER\n";
  $public_folder="$output_path/DATA_FOR_PUBLIC_FOLDER";
}

print STDOUT "Opening input and output files.. \n";

#Splits out the filename from the path
my $input_filename=$input_filename_path;
if ($input_filename =~ /(.*)\/(\V++)/) {$input_path = $1; $input_filename = $2};

unless ($input_filename =~ /(.*).sam/) {die"filename does not match .sam, stopped "};

# Creates files for the a report and a fastq file for unaligned sequences to go into
my $prefix_for_output = $1."_$version";
print PARAMETERLOG "dataprefix $prefix_for_output \n";
close PARAMETERLOG ;

my $outputfilename = "$sample\_$version/$prefix_for_output";

my $report_filename = "$sample\_$version/".$1."_report_$version.txt";
my $all_sam_filename = "$sample\_$version/".$1."_all_capture_reads_$version.sam";
my $all_typed_sam_filename = "$sample\_$version/".$1."_all_typed_reads_$version.sam";
my $cap_sam_filename = "$sample\_$version/".$1."_reported_capture_reads_$version.sam";
my $coord_filename = "$sample\_$version/".$1."_coordstring_$version.txt";

unless (open(REPORTFH, ">$report_filename")){die "Cannot open file $report_filename, stopped "}; print REPORTFH "\n\nStatistics\n";
if ($use_dump) {
unless (open(DUMPOUTPUT, ">$outputfilename\_dump.fastq")){die "Cannot open file $outputfilename\_dump.sam , stopped ";}
}
unless (open(ALLSAMFH, ">$all_sam_filename")){die "Cannot open file $all_sam_filename , stopped ";};
unless (open(ALLTYPEDSAMFH, ">$all_typed_sam_filename")){die "Cannot open file $all_sam_filename , stopped ";};
unless (open(CAPSAMFH, ">$cap_sam_filename")){die "Cannot open file $cap_sam_filename , stopped ";}; 
unless (open(COORDSTRINGFH, ">$coord_filename")){die "Cannot open file $coord_filename , stopped ";};

print STDOUT "Loading in oligo coordinate file.. \n";

# Uploads coordinates of capture oligos and exclusion regions into the array @oligo_data
# 0=name; 1=capture chr; 2 = capture start; 3 = capture end; 4= exclusion chr; 5 = exclusion start; 6 = exclusion end; 7 = snp position; 8 = SNP sequence
open(OLIGOFH, $oligo_filename) or die "Cannot open file $oligo_filename , stopped ";
#Splits out the filename from the path
my $oligo_file=$oligo_filename; my $oligo_path;
if ($oligo_file =~ /(.*)\/(\V++)/) {$oligo_path = $1; $oligo_file = $2};
unless ($oligo_file =~ /(.*)\.(.*)/) {die"Cant regex oligo filename"};
my $oligo_bed_out_filename = "$sample\_$version/".$1.".bed";

unless (open(OLIGOBED, ">$oligo_bed_out_filename")){die "Cannot open oligo_bed out file $oligo_bed_out_filename\n";}
print OLIGOBED "track name=CaptureC_oligos description=CaptureC_oligos visibility=1 itemRgb=On\n";

if ($use_snp)
{
print STDOUT "\nname\tchr\tstr\tstp\tchr\tstr\tstp\tpos\tbase\toligoLinesIn\toligoLinesSaved\n";
}
else
{
print STDOUT "\nname\tchr\tstr\tstp\tchr\tstr\tstp\toligoLinesIn\toligoLinesSaved\n";
}

my $temp_line_counter=0; 
while ( <OLIGOFH> )
{
  $counters{"01 Number of capture sites loaded:"}++;
  chomp;
  my @line = split /\s++/;
        push @oligo_data, [ @line ];
  $temp_line_counter++;
	
  # And now - check for existence for all columns..
  unless (defined($line[0]) && defined($line[1]) && exists($line[2]) &&  exists($line[3]) && defined($line[4]) && exists($line[5]) && exists($line[6])) {die "Cannot parse oligo coordinate file (cannot find the 7 first columns)\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  if ($use_snp) {
    unless ( exists($line[7]) && defined($line[8])) {die "Cannot parse SNP columns of oligo coordinate file \n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  }
  # File format check and cleanup for wrong kind of data :
  # Oligo file format is :
  # 0    1   2   3   4   5   6   7   8
  # name chr str stp chr str stp pos base
  
  #str stp str stp
  if ( ! ( ($line[2] =~ /^\d+$/) || ($line[2] == 0) ) ) {die "Oligo RE fragment start coordinate (3rd column) not numeric\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  if ( ! ( ($line[3] =~ /^\d+$/) || ($line[3] == 0) ) ) {die "Oligo RE fragment end coordinate (4th column) not numeric\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  if ( ! ( ($line[5] =~ /^\d+$/) || ($line[5] == 0) ) ) {die "Exclusion region start coordinate (6th column) not numeric\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";} 
  if ( ! ( ($line[6] =~ /^\d+$/) || ($line[6] == 0) ) ) {die "Exclusion region end coordinate (7th column) not numeric\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  
  # chr chr
  #if ( ! ($line[1] =~ /^chr\w+$/) ) {die "Chromosome name of RE fragment (2nd column) not proper format \n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  #if ( ! ($line[4] =~ /^chr\w+$/) ) {die "Chromosome name of exclusion region(5th column) not proper format In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  if ( ! ( ($line[1] =~ /^\w+$/)) ) {die "Chromosome name of RE fragment (2nd column) not proper format \n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  if ( ! ( ($line[4] =~ /^\w+$/)) ) {die "Chromosome name of exclusion region(5th column) not proper format In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  
  if ( ! ($line[1] eq $line[4]) ) {die "Chromosome of RE fragment and its exclusion (2nd column and 5th column) are different chromosomes - not allowed ! \n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}

  # name - all weird characters plus whitespace is worth of death :)
  if ( !($line[0] =~ /^[a-zA-Z0-9\-\_]+$/ )  ) {die "Oligo name contains whitespace or weird characters. Only allowed to have numbers[0-9], letters[a-zA-Z] and underscore [_] \n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  
  if ($use_snp) {
    if ( ! ( ($line[7] =~ /^\d+$/) || ($line[7] == 0) ) ) {die "SNP coordinate (8th column) not numeric\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
    if ( !($line[8] =~ /^[ATCG]$/) ) {die "SNP base (9th column) is not [ATCG]\n In file:\n".$oligo_path."/".$oligo_file." , stopped ";}
  }
  
  print OLIGOBED "chr$line[1]\t".($line[2]-1)."\t$line[3]\t$line[0]\t1\t+\t$line[2]\t$line[3]\t133,0,122\n";
  print OLIGOBED "chr$line[4]\t".($line[5]-1)."\t$line[6]\t$line[0]\t1\t+\t$line[5]\t$line[6]\t133,0,0\n";
  
  print STDOUT "Oligo number : $temp_line_counter ------------------------------------------------------------------";
  if ($use_snp)
  {
  print STDOUT "\n$line[0]\t$line[1]\t$line[2]\t$line[3]\t$line[4]\t$line[5]\t$line[6]\t$line[7]\t$line[8]\t$temp_line_counter\t".scalar(@oligo_data)."\n";
  }
  else
  {
  print STDOUT "\n$line[0]\t$line[1]\t$line[2]\t$line[3]\t$line[4]\t$line[5]\t$line[6]\t$temp_line_counter\t".scalar(@oligo_data)."\n";
  }
  print STDOUT "---------------------------------------------------------------------------------------------------";

};
# print Dumper (\@oligo_data);

print STDOUT "\nLoading in in-silico restriction enzyme digested genome.. \n";

# Opens the file of dpnII fragment coordinates and puts them into the hash of arrays %dpn_data, which is of the format dpn_data{chr}[fragment_start1....]
# The dpnII coordinates are generated by the script dpngenome2.pl.  This file is in the format chr:start-stop
# NB. The start and stop sequences are in the middle of the restriction enzyme fragments (the binary search function will need to be altered if you change to a 6 cutter)
open(DPNFH, "$restriction_enzyme_coords_file") or die "Cannot find restriction enzyme data file:$restriction_enzyme_coords_file , stopped ";

while (my $line = <DPNFH>)
{
  if ($line =~ /(.*):(\d++)-(\d++)/)
  {
    push @{$dpn_data{$1}}, $2;  #generates a hash of arrays in the format dpn_data{chr}[all dpn II frag start positions in ascending order]
    $counters{"02 Restriction enzyme fragments loaded:"}++
  }
  else {$counters{"02e lines from Restriction enzyme data failing to load:"}++;}
};

# Sorts the restriction enzyme coordinates in ascending numerical order 
my @chr_index = keys %dpn_data;
foreach my $chr(@chr_index) {@{$dpn_data{$chr}} = sort {$a <=> $b} @{$dpn_data{$chr}};}

# TESTERS FOR RE INPUT FILE INTEGRITY :

my $coord_sizes_filename = "$bigwig_folder/$genome\_sizes.txt";
#my $coord_sizes_filename = "$bigwig_folder";

unless (open(GENOMESIZESFH, "$coord_sizes_filename")){die "Cannot open chromosome sizes file $coord_sizes_filename for genome $genome , stopped "; }; print REPORTFH "\n\nStatistics\n";
my $chr_count=0;
while (my $line = <GENOMESIZESFH>)
{
  if (($line =~ /chr/) and ($line =~ /random/i))
  {
    $chr_count++;
  }
}

# print out how many chrs were found, and which chrs they were.
print STDOUT "\nRed in restriction enzyme fragments:\n";
if (keys %dpn_data) {
  my $temp_size = keys %dpn_data;
  print STDOUT "Found data in ". $temp_size ."chromosomes.\n";
  # Warn about suspiciously small amount of chromosomes :
  if ($temp_size < $chr_count) {
    print STDOUT "WARNING : Found data in only ". $temp_size ."chromosomes! (There are $chr_count non-random-scaffold chromosomes in $genome genome). - Are you sure your RE fragment file is not corrupted ?\n";
  }
  else
  {
  print STDOUT "Found data in ". $temp_size ."chromosomes.\n";
  }
  
  print STDOUT "\nChr\tFragment count\n";
  foreach my $chr (sort keys %dpn_data)
  {
    my $temp_size = @{$dpn_data{$chr}};
    print STDOUT "chr$chr\t". $temp_size."\n";
  }
  
}
else
{
  die "Cannot find any data in restriction enzyme coordinate file:$restriction_enzyme_coords_file, stopped ";
}


print STDOUT "\n";
print STDOUT "Starting the main loop - over the SAM file, analysing the data on the fly.. \n";
print STDOUT "\n";

# Opens input sam file 
unless (open(INFH, "$input_path\/$input_filename")) {die "Cannot open file $input_path\/$input_filename , stopped ";};

my $samDataLineCounter=0;

# Opening empty block for the WHILE variables - we have to call them outside the while once,
# to deal with the fragments of the last read.
{

my $saveLine; my $saveReadname;
  
while (my $line = <INFH>)  #loops through all the lines of the sam file
{
    chomp $line;
    # Saving this for the last read - being handled outside the while loop
    $saveLine=$line;
    
  if ($line =~ /^(@.*)/){push @samheadder, $line; print ALLSAMFH $line."\n"; $counters{"03 Lines in sam file header:"}++; next} #removes headder of sam file and stores it in the arragy @samheadder
 
   if ( $samDataLineCounter == 0) {
    my $tempPrinter=$counters{"03 Lines in sam file header:"};
    print STDOUT "Sam header red - found $tempPrinter header lines.\n";
  }
  
  # Informing user every time we have analysed a million reads
  $counters{"04 Data lines in sam file:"}++;
  $samDataLineCounter++;
  if ( $samDataLineCounter % 1000000 == 0) {
    my $millionReads= $samDataLineCounter/1000000;
    print STDOUT "$millionReads 000 000 sam data lines red and analysed ..\n";
  }
  
  
  my ($name, $bitwise, $chr, $readstart, $mapq, $cigar, $cola, $colb, $colc, $sequence, $qscore, $resta, $restb, $restc) = split /\t/, $line;   # splits the line of the sam file
  # Saving these for the last read - being handled outside the while loop
  
  # If we have wrongly parsing read name, we have to skip the line (our CUSTOM NAME FORMAT is needed for read parsing ) :
  if ( not ($name =~ /(.*):PE(\d++):(\d++)$/ ) )
  {
    if ($use_dump eq 1){print DUMPOUTPUT $line."\n";} #"$name\n$sequence\n+\n$qscore\n"};
    $counters{"05 Discarded fragments with wrongly parsing SAM file name:"}++; next
  }
  else
  #if (($chr =~ /chr(.*)/) and ($cigar =~/(\d++)(.*)/) and ($name =~ /(.*):PE(\d++):(\d++)$/)) # checks that the sam file matches the name, cigar string etc (non aligned reads will not do this)
  {
    
    # Setting the "data" hash up along our custom sam read-name format :
    
    $name =~ /(.*):PE(\d++):(\d++)$/; 
    my $readname=$1; my $pe = $2; my $readno= $3;
    # Saving this for the last read - being handled outside the while loop
    $saveReadname=$readname;

    #-----------------------------------------------------------------------------------------
    # If we have introns in CIGAR or non-mapping read, we save the read for duplicate filter, but discard it otherwise.

    if (($bitwise & 4 ) == 4)
    {
      $counters{"06 Unmapped fragments in SAM file:"}++;
      #push @{$data{$readname}{"coord array"}}, "unmapped";
      if ($use_dump eq 1){print DUMPOUTPUT $line."\n"} #"$name\n$sequence\n+\n$qscore\n"};
    }
    
    elsif ( $cigar =~/\d++\w++\d++/ )
    {
      $counters{"06e Fragments with CIGAR strings failing to parse (containing introns or indels) :"}++;
      #push @{$data{$readname}{"coord array"}}, "cigarfail";
      if ($use_dump eq 1){print DUMPOUTPUT $line."\n"} #"$name\n$sequence\n+\n$qscore\n"};     
    }
    
    #-----------------------------------------------------------------------------------------
    
    # The rest of the reads are now parse-able :
    else{
    
            $counters{"07 Mapped fragments:"}++;
	    
            #Checks that the read name matches the end of the read name has been altered by the script that performs the in silico digestion of the DpnII file
	    #This gives the reads names in the format PE1:0 ... PE2:4 depending on which paired end read and how many times the read has been digested
	    
	    #The hash structure is a little complex but follows what is happening in the reads it is as follows:
	    
	    #Where the data needs to be stored for each split / paired end read it is done as follows:
	    #	$data{$readname}{$pe}{$readno}{"seqlength"}
	    #	$data{$readname}{$pe}{$readno}{"readstart"}
	    #	$data{$readname}{$pe}{$readno}{"readlength"}
	    #	$data{$readname}{$pe}{$readno}{"sequence"}
	    #Things are also stored for the whole group of reads as follows:
	    #	$data{$readname}{"captures"}
	    #	$data{$readname}{"number of captures"}
	    #	@{data{$readname}{"coordinate array"}} - it is necessary to use a hash of arrays because the duplicate reads from the forward and reverse strands need to be excluded
	    #	and the order of the reads changes depending on which strand the reads come from.
            
	    # Assigns the entire line of the sam file to the hash
	    $data{$readname}{$pe}{$readno}{"whole line"}= $line;       
	    
	    # Parses the chromosome from the $chr - nb without the chr in front
            $chr =~ /chr(.*)/; $chr = $1;
            $data{$readname}{$pe}{$readno}{"chr"} = $1;
	    
	    # Parses out the original strand from the "bitwise" flag
	    # - if it was reverse complemented in sam (meaning that the read in fastq mapped in minus strand), it should  have bit "10" lit.
	    # This is needed for the duplicate filter later (it is not duplicate if the fragment is the same but reverse complement)
	    if ($bitwise & 0x0010) { $data{$readname}{$pe}{$readno}{"strand"} = "minus";}
	    else { $data{$readname}{$pe}{$readno}{"strand"} = "plus";}
	    
	    #This adds the start of the sequence and the end of the read to the hash
            $cigar =~/(\d++)(.*)/;
	    
            $data{$readname}{$pe}{$readno}{"seqlength"} = $1;
            $data{$readname}{$pe}{$readno}{"readstart"} = $readstart;
            $data{$readname}{$pe}{$readno}{"readend"} = $readstart+length($sequence)-1; #minus1 due to 1 based sam file input.
	    $data{$readname}{$pe}{$readno}{"sequence"} = $sequence;
	    
	    #Generates a string of the coordinates of all the split paired end reads to allow duplicates to be excluded
	    $data{$readname}{"number of reads"}++;
	    push @{$data{$readname}{"coord array"}}, $data{$readname}{$pe}{$readno}{"chr"}.":".$data{$readname}{$pe}{$readno}{"readstart"}."-".$data{$readname}{$pe}{$readno}{"readend"}."-".$data{$readname}{$pe}{$readno}{"strand"};
	    $data{$readname}{$pe}{$readno}{"Proximity_exclusion"}="no";
	    
#------------------------------------------------------------------------------------------------------------------
# OLIGO FILE FOR LOOPS - whether our fragment is a CAPTURE or EXCLUSION fragment
#------------------------------------------------------------------------------------------------------------------

#This part of the code defines whether the read is a capture or reporter read or whether it is proximity excluded

	    my $captureFlag=0;
            my $exclusionFlag=0;
	    
	    #Loops through the @oligo_data array to see whether the fragment meets the criteria to be a capture or exclusion fragment
            for (my$i=0; $i< scalar (@oligo_data); $i++)
            {
                #Defines if the fragment lies within the exclusion limits around the capture
                if ($data{$readname}{$pe}{$readno}{"chr"} eq $oligo_data[$i][4] and $data{$readname}{$pe}{$readno}{"readstart"}>=$oligo_data[$i][5] and $data{$readname}{$pe}{$readno}{"readend"}<=$oligo_data[$i][6]) 
                {
		  $exclusionFlag=1;
		}
                # Defines if the fragment lies within the capture region (trumping the exclusion limits)
		# NB this version of the script requires the whole read to be contained within the capture area
                #print"Outside if:$i\t$oligo_data[$i][1]\t$oligo_data[$i][2]\t$oligo_data[$i][3]\n";
		if (($data{$readname}{$pe}{$readno}{"chr"} eq $oligo_data[$i][1]) and ($data{$readname}{$pe}{$readno}{"readstart"}>=$oligo_data[$i][2] and $data{$readname}{$pe}{$readno}{"readend"}<=$oligo_data[$i][3])) 
		{
		  if ($use_snp ==1) #checks if the specified snp is in the capture read
		  {
		    if (snp_caller($data{$readname}{$pe}{$readno}{"chr"}, $data{$readname}{$pe}{$readno}{"readstart"}, $data{$readname}{$pe}{$readno}{"sequence"},$oligo_data[$i][1], $oligo_data[$i][7], $oligo_data[$i][8]) eq "Y")
		    {
                    $captureFlag=1;
		    }
		  }
		  else #if SNP is not specified
		  {
                    $captureFlag=1;
		  }
		  
                }
		
            }


# If we found a capture
if ($captureFlag == 1) {
 $data{$readname}{$pe}{$readno}{"type"}="capture";
 $data{$readname}{"number of capture fragments"}++;
}

# If we found proximity exclusion
elsif ($exclusionFlag ==1) {

  $data{$readname}{$pe}{$readno}{"type"} = "proximity exclusion";
  $counters{"09 Proximity exclusion fragments (Pre PCR duplicate removal):"}++;
  $data{$readname}{"number of exclusions"}++;  
}
else
# If neither of the above, marking it as reporter.
{
  $data{$readname}{$pe}{$readno}{"type"}="reporter";
  $data{$readname}{"number of reporters"}++;
  $counters{"10 Reporter fragments (Pre PCR duplicate removal):"}++;

}

}

#------------------------------------------------------------------------------------------------------------------
# COMBINING ALL ligated FRAGMENTS within a single sequenced READ, under a common name, into the storage hash
#------------------------------------------------------------------------------------------------------------------

# Changed upto here JT 220615

#------------------------------------------------------------------------------------------------------------------
# COMBINING ALL ligated FRAGMENTS within a single sequenced READ, under a common name, into the storage hash
#------------------------------------------------------------------------------------------------------------------


# Checks whether the name of the read has changed compared to the last one.  If there is no change it continues to loop through all the fragments of the read until it changes.
# If the readname has changed it loads the data into the output hashes and deletes the lines from the %data hash.

    if ($last_read eq "first"){$last_read=$readname} #deals with the first read
    
    if($readname ne $last_read){
      #checks whether the read name has changed and moves on to the next line in the sam file if the read names are the same

      # This whole thing is done in a big fat subroutine, as it needs to be repeated after the loop - otherwise the LAST READ of sam file gets un-analysed..
      # The parameter is needed to feed the $line to the data dumper (debugger) 
      # All the analysed data is hashed to a global hash - so, all that stuff is available to the sub automatically.
      $analysis_read = $last_read;
      &readAnalysisLoop($line);
      $last_read = $readname;
      $analysedReads++;
    }
  else  {
    $notlastFragments++;
  } # this is the end else of "last fragment of this read" - the if in the beginning was empty to make "next", i.e. the else is the "real deal analysis" when we did change read name.
  } # this is the readname parser else end - the if in the beginning was to skip over wrongly parsing read names.
LOOP_END:    
unless ($use_limit ==0){if ($counters{"02 Aligning sequences:"}) { if ($counters{"02 Aligning sequences:"}>$use_limit){last}  }}   # This limits the script to the first n lines
} # this is the main SAM file while end

# Analysing last read of sam file !
#my $saveLine; my $saveReadname;
#All other variables are inside hashes - and thus already available to the subroutines
$analysis_read = $saveReadname;
print STDOUT "Last read analysis. Enter analysis round. Analysis read name : ".$analysis_read."\n";
&readAnalysisLoop($saveLine);

# Closing the empty block - making inside-while variables invisible again : my $saveLine; my $saveChr; my $saveReadstart; my $saveReadname; 
}

PRINTOUT:
#print Dumper(\%data); #used for debugging
#print Dumper(\%coords_hash); #used for debugging
#print Dumper(\%fraghash); #used for debugging
#print Dumper(\%cap_samhash); #used for debugging


# Prints the statistics into the report file
print REPORTFH "Input path/file: $input_path/$input_filename\nRestriction enzyme coords file: $restriction_enzyme_coords_file\nOligo coordinate input file: $oligo_filename\nPublic folder: $public_folder\nPublic URL: $public_url\nSample name: $sample \nScript version:$version\n";
print REPORTFH "Script started at: $mday/$mon/$year $hour:$min:";
print REPORTFH "\n\nStatistics\n";
output_hash(\%counters, \*REPORTFH);
output_hash(\%coords_hash, \*COORDSTRINGFH);
#output_hash(\%duplicates, \*COORDSTRINGFH);

#makes the mig, wig and sam files using the subroutines wigout and wigtobigwig
for (my $i=0; $i< (scalar (@oligo_data)); $i++)
{
frag_to_wigout(\%fraghash, $outputfilename."_".$oligo_data[$i][0],"full",$oligo_data[$i][0]);
frag_to_windowed_wigout(\%fraghash, $outputfilename."_".$oligo_data[$i][0],"full",$oligo_data[$i][0], $window, $increment);
frag_to_migout(\%fraghash, $outputfilename."_".$oligo_data[$i][0],"full",$oligo_data[$i][0]);
output_hash_sam(\%samhash, $outputfilename."_".$oligo_data[$i][0],$oligo_data[$i][0],\@samheadder);
output_hash_sam(\%cap_samhash, $outputfilename."_capture_".$oligo_data[$i][0],$oligo_data[$i][0],\@samheadder)
}

#makes a combined track of HbA1 and A2 
if ($globin ==1 or $globin == 2)
{

my @tracks_to_combine = qw(Hba-1 Hba-2);
my $combined_name = "HbaCombined";
my @combined_name = ("HbaCombined", 11, 320000, 330000, 11, 320000, 320000);
push @oligo_data, [@combined_name];

foreach my $storedChr(sort keys %{$fraghash{"full"}{$tracks_to_combine[0]}})
    {
    foreach my $storedposition(sort keys %{$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}})
        {         
              $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"value"}=$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}{$storedposition}{"value"};
	      $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"end"}=$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}{$storedposition}{"end"}
	}
    }

foreach my $storedChr(sort keys %{$fraghash{"full"}{$tracks_to_combine[1]}})
    {
    foreach my $storedposition(sort keys %{$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}})
        {         
              $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"value"}+=$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}{$storedposition}{"value"};
	      $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"end"}=$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}{$storedposition}{"end"}
	}
    }
frag_to_wigout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name);
frag_to_windowed_wigout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name, $window, $increment);
frag_to_migout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name);
}

#makes a combined track of HbB1 and B2 
if ($globin ==2)
{
my @tracks_to_combine = qw(Hbb-b1 Hbb-b2);
my $combined_name = "HbbCombined";
my @combined_name = ("HbbCombined", 7, 110961967, 110962817, 7, 110961967, 110962817);
push @oligo_data, [@combined_name];
foreach my $storedChr(sort keys %{$fraghash{"full"}{$tracks_to_combine[0]}})
    {
    foreach my $storedposition(sort keys %{$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}})
        {         
              $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"value"}=$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}{$storedposition}{"value"};
	      $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"end"}=$fraghash{"full"}{$tracks_to_combine[0]}{$storedChr}{$storedposition}{"end"}
	}
    }

foreach my $storedChr(sort keys %{$fraghash{"full"}{$tracks_to_combine[1]}})
    {
    foreach my $storedposition(sort keys %{$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}})
        {         
              $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"value"}+=$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}{$storedposition}{"value"};
	      $fraghash{"full"}{$combined_name}{$storedChr}{$storedposition}{"end"}=$fraghash{"full"}{$tracks_to_combine[1]}{$storedChr}{$storedposition}{"end"}
	}
    }
frag_to_wigout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name);
frag_to_windowed_wigout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name, $window, $increment);
frag_to_migout(\%fraghash, $outputfilename."_".$combined_name,"full",$combined_name);
}



#########################################################################################################################################################################
# Creates a track hub in my public folder - clearly this will need to be changed to allow the public folder to be specified
unless (open(TRACKHUBA, ">$public_folder/$sample\_$version\_hub.txt")){die "Cannot open file $public_folder/$sample\_$version\_tracks.txt, stopped ";}
unless (open(TRACKHUBB, ">$public_folder/$sample\_$version\_genomes.txt")){die "Cannot open file $public_folder/$sample\_$version\_tracks.txt, stopped ";}
unless (open(TRACKHUBC, ">$public_folder/$sample\_$version\_tracks.txt")){die "Cannot open file $public_folder/$sample\_$version\_tracks.txt, stopped ";}

print TRACKHUBA "hub $sample\_$version
shortLabel $sample\_$version
longLabel $sample\_$version\_CaptureC
genomesFile http://$public_url/$sample\_$version\_genomes.txt
email $email";

print TRACKHUBB "genome $genome
trackDb http://sara.molbiol.ox.ac.uk$public_folder/$sample\_$version\_tracks.txt";


print REPORTFH "\nThe track hub can be found at:
http://$public_url/$sample\_$version\_hub.txt
This URL just needs to be pasted into the UCSC genome browser\n\n";

# Loops throught the different capture points and converts the wig to a bigwig if the file is over 1000 bytes and updates the track hub tracks.txt file
for (my$i=0; $i< (scalar (@oligo_data)); $i++)
{
  my $filename_out = $outputfilename."_".$oligo_data[$i][0].".wig";
  my $filesize = 0;
  if ( -f $filename_out ){ $filesize = -s $filename_out; }# checks the filesize
  print "$filename_out\t$filesize\n";
  
  #if ($filesize >1000)	# ensures that wigtobigwig is not run on files containing no data
  if ($filesize >0)	# ensures that wigtobigwig is not run on files containing no data
  {
    wigtobigwig($outputfilename."_".$oligo_data[$i][0], \*REPORTFH, $public_folder, $public_url, "CaptureC_gene_$oligo_data[$i][0]");
    wigtobigwig($outputfilename."_".$oligo_data[$i][0]."_win", \*REPORTFH, $public_folder, $public_url, "CaptureC_gene_$oligo_data[$i][0]");
    
    my $short_filename = $outputfilename."_".$oligo_data[$i][0];
    if ($short_filename =~ /(.*)\/(\V++)/) {$short_filename = $2};
    
    print TRACKHUBC
"track $sample\_$oligo_data[$i][0]
type bigWig
longLabel CC_$sample\_$oligo_data[$i][0]
shortLabel $sample\_$oligo_data[$i][0]
bigDataUrl http://$public_url/$short_filename.bw
visibility hide
priority 200
color 0,0,0
autoScale on
alwaysZero on

track win_$sample\_$oligo_data[$i][0]
type bigWig
longLabel CC_win_$sample\_$oligo_data[$i][0]
shortLabel win_$sample\_$oligo_data[$i][0]
bigDataUrl http://$public_url/".$short_filename."_win.bw
visibility hide
priority 200
color 0,0,0
autoScale on
alwaysZero on

"
  }

}

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(); print REPORTFH "Script finished at: $mday/$mon/$year $hour:$min \n";

print REPORTFH "Analysed reads (last fragments): $analysedReads, not-last-fragments :$notlastFragments \n";

exit;

#########################################################################################################################################################################

# MAIN READ ANALYSIS LOOP - as a subroutine, as it needs to be repeated once after the last read (otherwise last SAM read never gets analysed)

# These variables need to go in as parameters (all other stuff is accessible via the hashes already)
# $line
# $chr
# $readstart
# $readname

sub readAnalysisLoop
{
      my ($line) = @_;
      my %reporter_dpn = ();
      
      $counters{"11 Total number of reads entering the analysis :"}++;
      
      my $weHaveCaptures=0;
      if (defined $data{$analysis_read}{"number of capture fragments"} and $data{$analysis_read}{"number of capture fragments"}>0 )
      {	$counters{"11b Total number of capture-containing reads entering the analysis :"}++;
      $weHaveCaptures=1;
      }
      
      my $weHaveReporters=0;
      if (defined $data{$analysis_read}{"number of reporters"} and $data{$analysis_read}{"number of reporters"}>0 )
      {	
      $weHaveReporters=1;
      }
      
      my $weAnalyseThisRead=0;
      if ($weHaveCaptures==1 and $weHaveReporters==1 )
      {	
      $weAnalyseThisRead=1;
      $counters{"11c Total number of capture-and-reporter-containing reads entering the analysis :"}++;
      }
      else
      {
      $counters{"11d Total number of reads lacking either captures or reporters, excluded from the analysis :"}++;
      }
      
      my $exclusioncount=0;
      my $reportercount=0;
      my $capturename="";
      my $capturecomposition="";
      my %capturenames;
      
      if ($weAnalyseThisRead==1)
      {
      #---------------------------------------------------------------------------------------
      # Resolving the identity of the capture fragments.
      
      for (my $pe=1;$pe<=2;$pe++)  # loops through PE1 and PE2 
      {
	for (my $readno=0; $readno<4; $readno++) # loops through up to 4 fragments in each paired end read
        {
	  if (defined $data{$analysis_read}{$pe}{$readno}{"type"})
	  {
	  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "capture")
	  {
	    for (my $oligo=0; $oligo< (scalar (@oligo_data)); $oligo++)
	    {
	      if (($data{$analysis_read}{$pe}{$readno}{"chr"} eq $oligo_data[$oligo][1]) and ($data{$analysis_read}{$pe}{$readno}{"readstart"}>=$oligo_data[$oligo][2] and $data{$analysis_read}{$pe}{$readno}{"readend"}<=$oligo_data[$oligo][3]))
	      {
	      my $tempname="".$oligo_data[$oligo][0]."";
	      $capturenames{$tempname}++;
	      }
	    }
	  }
	  }
	  
	}
      }
      
      # Resolving the count of exclusion fragments.
      
      for (my $pe=1;$pe<=2;$pe++)  # loops through PE1 and PE2 
      {
	for (my $readno=0; $readno<4; $readno++) # loops through up to 4 fragments in each paired end read
        {
	  if (defined $data{$analysis_read}{$pe}{$readno}{"type"})
	  {
	  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "proximity exclusion")
	  {
	      $exclusioncount++;
	  }
	  }
	  
	}
      }
      
      # Resolving the count of reporter fragments.
      
      for (my $pe=1;$pe<=2;$pe++)  # loops through PE1 and PE2 
      {
	for (my $readno=0; $readno<4; $readno++) # loops through up to 4 fragments in each paired end read
        {
	  if (defined $data{$analysis_read}{$pe}{$readno}{"type"})
	  {
	  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "reporter")
	  {
	      $reportercount++;
	  }
	  }
	  
	}
      }
      
      foreach my $foundoligo (sort keys %capturenames)
      {
	$capturename.="".$foundoligo."";
	$capturecomposition.=$foundoligo.":".$capturenames{$foundoligo}." " ;
      }
      
      }
      
      # Resolving the identity of the capture fragments - DONE.
      #---------------------------------------------------------------------------------------
      
      # Now we need to take into account the "weird ones" which leak through and claim to  have composition ""
      
      # If we have only whitespace in $capturename..
      if ($capturename =~ /^\s*$/)
      {
        $weAnalyseThisRead=0;
      }
      
      # If we have only "" in $capturename..
      if ($capturename eq '')
      {
        $weAnalyseThisRead=0;
      }
      
      # Then we take care of the ones which leak through and have 0 reporter fragments
      
      if ($reportercount==0)
      {
        $weAnalyseThisRead=0;
      }
      
      #---------------------------------------------------------------------------------------
      # Now, printing out what we have - after all the above filters
      if ($weAnalyseThisRead==1)
      {
      $counters{"11e Total number of reads having captures in composition $capturecomposition : "}++;
      $counters{"11ee Total number of reads having captures in composition $capturecomposition , having $reportercount reporters and $exclusioncount exclusion fragments : "}++;
      
      #---------------------------------------------------------------------------------------
      # Last filter before analysis : double captures are excluded :
      
      # Now we check again, if we REALLY want to analyse this read - if it is a double capture, we kick it out now.
      # We allow for reads which have multicapture in SAME capture oligo, though.
      
      if (scalar keys %capturenames == 1 )
      {	
      $weAnalyseThisRead=1;
      $counters{"11f Total number of single-capture reads included to the analysis :"}++;
      $data{$analysis_read}{"captures"}="".$capturename."";
      }
      else
      {
      
      # If we planned to analyse - but it was double capture after all, we count these in separate counter
      $counters{"11g Total number of multi-capture reads excluded from the analysis :"}++;
      
      # We set in any case, that none of these continue in analysis.
      $weAnalyseThisRead=0;
      }
      }
      
    ##########################################################################################################
    # So, the rest of the things are done only to fragments, which have at least one capture, and one reporter.
    ##########################################################################################################
    
    if ($weAnalyseThisRead==1)
      {
    $counters{"12 Total number of reads entering duplicate-filtering - should be same count as 11f :"}++;
    
    # If we have some data in the read - i.e. something else than "unknown" fragments due to unmapping reads or unparse-able cigar strings.
    # my $count = true { /pattern/ } @list_of_strings;
    
    # The line below does not work, as List:MoreUtils did not load properly - genmailed that, and now need to write a manual for loop for this.
    #my $countOfUnknowns = true { /^unknown$/ } @{$data{$analysis_read}{"coord array"}}
    
    # Manual loop over array 0 as List::MoreUtils fails to load :
    my $countOfUnknowns = 0;
    foreach (@{$data{$analysis_read}{"coord array"}})
    {
      my $thisRound=$_;
      if (($thisRound eq "unmapped") || ($thisRound eq "cigarfail" )){ $countOfUnknowns++;}
    }
    
    # Counters for fragment lenght distribution :
    my $tempSize= scalar(@{$data{$analysis_read}{"coord array"}});
    $counters{"14a Reads having $tempSize fragments:"}++;
    $tempSize=$tempSize-$countOfUnknowns;
    $counters{"14b Reads having $tempSize informative fragments:"}++;
    
    foreach (@{$data{$analysis_read}{"coord array"}}) {$counters{"13 Count of fragments in Reads having at least one informative fragment :"}++;};
   
#------------------------------------------------------------------------------------------------------------------
# DUPLICATE FILTER - requires same ligation order and same strand of all fragments, before gets marked duplicate.
#------------------------------------------------------------------------------------------------------------------
      
      # We generate coordinate join. This is purely for duplicate filtering.
      # (if all fragments are in same order, and same strand, this is a duplicate entry).
      
      # 2 arrays : "coordinate string" (coordinates and strand for all ligation fragments within this sequenced read)
      #            "reverse coord string" (the same - but to the other direction. same ligation fragment - red from the "other end")
      
      #-----------------------------------------------------------------------------------------
      # Making the "coordinate string"
      
      # We get rid of this fanciness - as we do the "original duplicate filter" here..
      
      s/-plus$// for @{$data{$analysis_read}{"coord array"}};
      s/-minus$// for @{$data{$analysis_read}{"coord array"}};
      
      # Here the old duplicate filter. this over-rules the above "VS2 duplicate filter".
      $data{$analysis_read}{"coord string"}= join( "_", sort {$a cmp $b} @{$data{$analysis_read}{"coord array"}}); #this line sorts the array in the hash and converts it into a string with the sequences in ascending order
      
      #$data{$analysis_read}{"coord string"}= join( "_", @{$data{$analysis_read}{"coord array"}}); #we don't want to sort, as ligation order is important to us
      
      #-----------------------------------------------------------------------------------------
      # Making the "reverse coordinate string"
      
      # Now we make the coord string upside down :
      #s/oldtext/newtext/ for @config;
      
      #s/_plus$/_TEMP/ for @{$data{$analysis_read}{"coord array"}};
      #s/_minus$/_plus/ for @{$data{$analysis_read}{"coord array"}};
      #s/_TEMP$/_minus/ for @{$data{$analysis_read}{"coord array"}};
      
      #$data{$analysis_read}{"reverse coord string"}= join( "_", reverse @{$data{$analysis_read}{"coord array"}}); #we don't want to sort, as ligation order is important to us
      
      # We return the coord array to original order (if we want to print it out later and not be confused)
      #s/_plus$/_TEMP/ for @{$data{$analysis_read}{"coord array"}};
      #s/_minus$/_plus/ for @{$data{$analysis_read}{"coord array"}};
      #s/_TEMP$/_minus/ for @{$data{$analysis_read}{"coord array"}};
      
      #-----------------------------------------------------------------------------------------
      # Now - using the coordinate strings to jump over duplicates in the analysis :
      
      #if (defined $coords_hash{$data{$analysis_read}{"coord string"}} or defined $coords_hash{$data{$analysis_read}{"reverse coord string"}}) 
      #{$coords_hash{$data{$analysis_read}{"coord string"}}++; $counters{"15 Duplicate reads:"}++;
      # if ($use_dump eq 1){print DUMPOUTPUT $line."\n"} #"$name\n$sequence\n+\n$qscore\n"};
      #}
      #-----------------------------------------------------------------------------------------
      
      # If it wasn't a duplicate - we start the "real deal" analysis :
      
      if (exists $coords_hash{$data{$analysis_read}{"coord string"}}){$coords_hash{$data{$analysis_read}{"coord string"}}++; $counters{"06c Duplicate reads:"}++}
      
      
#------------------------------------------------------------------------------------------------------------------
# REPORTING THE COUNTS AFTER DUPLICATE FILTER - only for reads which made it this far..
#------------------------------------------------------------------------------------------------------------------
      
      else 
      {
	  $coords_hash{$data{$analysis_read}{"coord string"}}++;
	  $counters{"16 Non-duplicated reads:"}++;
	  
	  $counters{"16b Non-duplicated reads having captures in composition $capturecomposition : "}++;
	  $counters{"16bb Non-duplicated reads having captures in composition $capturecomposition , having $reportercount reporters and $exclusioncount exclusion fragments : "}++;
	  
	  #Counters for informative and un-informative fragments :
	  my $informativeCounter=0;
	  my $allFragCounter=0;	  
	  
	  # Counters for capture and exclusion fragments after duplicate-removal
	  for (my $pe=1;$pe<=2;$pe++)  # loops through PE1 and PE2 
                    {
		      for (my $readno=0; $readno<4; $readno++) # loops through up to 4 fragments in each paired end read
		      {
			
			
			$allFragCounter++;
			if (defined $data{$analysis_read}{$pe}{$readno}{"type"})
			{
			  $informativeCounter++;
			  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "capture"){$counters{"16b Capture fragments (After PCR duplicate removal):"}++;}
			  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "proximity exclusion"){$counters{"16c Proximity exclusion fragments (After PCR duplicate removal):"}++;}
			  if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "reporter"){$counters{"16d Reporter fragments (After PCR duplicate removal):"}++;}  
			}
		      }
		    }
	  
	  $counters{"16g Reads having ".$informativeCounter." informative fragments (after PCR duplicate whole-read removal):"}++;
	  $counters{"16f Total fragment count (after PCR duplicate removal):"}++;
	  

#------------------------------------------------------------------------------------------------------------------
# THE REAL DEAL REPORTING FOR LOOPS - here the destiny of the reads is finally made..
#------------------------------------------------------------------------------------------------------------------

		  for (my $pe=1;$pe<=2;$pe++)  # loops through PE1 and PE2 
                    {
		      
                        for (my $readno=0; $readno<4; $readno++) # loops through up to 4 fragments in each paired end read
                            {
				if (defined $data{$analysis_read}{$pe}{$readno}{"whole line"}){print ALLSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"}."\n";}
				if (defined $data{$analysis_read}{$pe}{$readno}{"type"}) # checks that the fragment is not CIGAR parse error or unmapped read
                                {
				    print ALLTYPEDSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"}."\n";
				    
#------------------------------------------------------------------------------------------------------------------
# ANALYSING THE REPORTER FRAGMENTS - step 1) - if clauses to restrict to non-duplicates (if STRINGENT requested)
#------------------------------------------------------------------------------------------------------------------
				    
				    my $duplicate_string;
				    
				    if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "reporter")
				    {
				      $counters{"23 Reporters before final filtering steps"}++ ;
				      $counters{$data{$analysis_read}{"captures"}." 12 Reporters before final filtering steps"}++ ;
				      
	      			      $duplicate_string = $data{$analysis_read}{"captures"}.$data{$analysis_read}{$pe}{$readno}{"chr"}.":".$data{$analysis_read}{$pe}{$readno}{"readstart"}."-".$data{$analysis_read}{$pe}{$readno}{"readend"} ;
				      
				      if (defined $duplicates{$duplicate_string})
				      {
					$counters{"24 Duplicate reporters (duplicate-excluded if stringent was on)"}++ ;
					$counters{$data{$analysis_read}{"captures"}." 13 Duplicate reporters (duplicate-excluded if stringent was on)"}++ ;
				      }
				      
				      
				      if(($stringent ==1) and (defined $duplicates{$duplicate_string}))
				      {
					# We jump over duplicates if we have stringent on.
					$duplicates{$duplicate_string}++;
					
					print CAPSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"};
					print CAPSAMFH "\tCO:Z:";
					print CAPSAMFH $data{$analysis_read}{"captures"};
					print CAPSAMFH "_REPDUPSTR\n";
				      }
				      else
				      {
					# This is not only ++ but also "make this to exist" - the counterpart of the above if exists duplicates{duplString}
					$duplicates{$duplicate_string}++;
					
#------------------------------------------------------------------------------------------------------------------
# ANALYSING THE REPORTER FRAGMENTS - step 2) - comparing to DpnII fragments, and reporting those.
#------------------------------------------------------------------------------------------------------------------
					
					#print COORDSTRINGFH "$pe:$readno\t".$analysis_read."\t".$data{$analysis_read}{"captures"}."\t".$data{$analysis_read}{$pe}{$readno}{"type"}."\n"; #For debugging reads that are reported
					#print "$pe:$readno\t".$analysis_read."\t".$data{$analysis_read}{"captures"}."\t".$data{$analysis_read}{$pe}{$readno}{"type"}."\n";
				      
					#This maps the fragment onto the dpnII fragment using the binary search subroutine, which returns the position of the matching fragment in the
					#hash of arrays %dpn_data - which is in the format %dpn_data{chromosome}[start position]
				      
					my $chr = $data{$analysis_read}{$pe}{$readno}{"chr"};
					my $readstart = $data{$analysis_read}{$pe}{$readno}{"readstart"};				      
				      
					my ($start, $end) = binary_search(\@{$dpn_data{$chr}}, $data{$analysis_read}{$pe}{$readno}{"readstart"}, $data{$analysis_read}{$pe}{$readno}{"readend"}, \%counters);
				      
					#print "returned values: $start-$end\t";
				      
					if (($start eq "error") or ($end eq "error"))
					{
					  $counters{"25e Error in Reporter fragment assignment to in silico digested genome (see 24ee for details)"}++;
					  $counters{$data{$analysis_read}{"captures"}." 14e Error in Reporter fragment assignment to in silico digested genome (see 25ee for details)"}++;					 
					}
					elsif (defined $reporter_dpn{"$chr:$start-$end"})
					{
					  $reporter_dpn{"$chr:$start-$end"}++; $counters{"25 Reporter fragments reporting the same RE fragment within a single read (duplicate-excluded)"}++;
					  $counters{$data{$analysis_read}{"captures"}." 14 Reporter fragments reporting the same RE fragment within a single read (duplicate-excluded)"}++;
					  
					  print CAPSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"};
					  print CAPSAMFH "\tCO:Z:";
					  print CAPSAMFH $data{$analysis_read}{"captures"};
					  print CAPSAMFH "_REPDUP\n";
					  
					}
					else
					{
					$reporter_dpn{"$chr:$start-$end"}++;
					
					$data{$analysis_read}{$pe}{$readno}{"fragstart"} = $start;
					$data{$analysis_read}{$pe}{$readno}{"fragend"} = $end;
				      
					#This transfers the positions of the dpnII fragments into the hash %fraghash
					# 				%fraghash{"full"}{chromosome}{fragment start}{"value"}= value
					# 				%fraghash{"full"}{chromosome}{fragment start}{"end"}= fragment end
				      
					$fraghash{"full"}{$data{$analysis_read}{"captures"}}{$data{$analysis_read}{$pe}{$readno}{"chr"}}{$data{$analysis_read}{$pe}{$readno}{"fragstart"}}{"value"}++;
					$fraghash{"full"}{$data{$analysis_read}{"captures"}}{$data{$analysis_read}{$pe}{$readno}{"chr"}}{$data{$analysis_read}{$pe}{$readno}{"fragstart"}}{"end"}= $data{$analysis_read}{$pe}{$readno}{"fragend"};
				      
					#This puts the data for the matching lines into the %samhash
					push @{$samhash{$data{$analysis_read}{"captures"}}}, $data{$analysis_read}{$pe}{$readno}{"whole line"};
					
					print CAPSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"};
					print CAPSAMFH "\tCO:Z:";
					print CAPSAMFH $data{$analysis_read}{"captures"};
					print CAPSAMFH "_REP\n";
				      
					$counters{"26 Actual reported fragments :"}++;
					$counters{$data{$analysis_read}{"captures"}." 17 Reporter fragments (final count) :"}++;
					}
				      }
				    }
#------------------------------------------------------------------------------------------------------------------
# ANALYSING THE CAPTURE FRAGMENTS 
#------------------------------------------------------------------------------------------------------------------
				    if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "capture")
				    {
				      push @{$cap_samhash{$data{$analysis_read}{"captures"}}}, $data{$analysis_read}{$pe}{$readno}{"whole line"};
				      $counters{$data{$analysis_read}{"captures"}." 15 Capture fragments (final count):"}++;
					push @{$samhash{$data{$analysis_read}{"captures"}}}, $data{$analysis_read}{$pe}{$readno}{"whole line"}; $counters{"Counters with reporters"}++;
				       	print CAPSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"};
					print CAPSAMFH "\tCO:Z:";
					print CAPSAMFH $data{$analysis_read}{"captures"};
					print CAPSAMFH "_CAP\n";
				       
				      
				    }
#------------------------------------------------------------------------------------------------------------------
# ANALYSING THE PROXIMITY EXCLUSION FRAGMENTS 
#------------------------------------------------------------------------------------------------------------------
				    if ($data{$analysis_read}{$pe}{$readno}{"type"} eq "proximity exclusion")
				    {
				      $counters{$data{$analysis_read}{"captures"}." 16 Proximity exclusions (final count):"}++;
				      print CAPSAMFH $data{$analysis_read}{$pe}{$readno}{"whole line"};
				      print CAPSAMFH "\tCO:Z:";
				      print CAPSAMFH $data{$analysis_read}{"captures"};
				      print CAPSAMFH "_EXC\n";
				    }
				    
                                }
#------------------------------------------------------------------------------------------------------------------
# The "end elses" for RESTRICTING ANALYSIS to only reads and fragments of interest - various if clauses to dig deeper only if we really want to..
#------------------------------------------------------------------------------------------------------------------
				
                            } # This is the FRAGMENTS for loop end 			    
                    } # This is the PE for loop end 
		} # We passed duplicate filter
    
      
#------------------------------------------------------------------------------------------------------------------
# The ends of the rest of the main loops / ifs..
#------------------------------------------------------------------------------------------------------------------
      
    } # this is the end of else "no data in this read" - we need to have at least one capture and one reporter in order to avoid failing here..
  
  # In the end - we clear the data from the hash, avoiding to take the whole sam file into the memory..
  delete $data{$analysis_read};
}


#########################################################################################################################################################################
#Subroutines

sub snp_caller
{
my ($chr, $read_start, $sequence, $snp_chr, $snp_position, $snp) = @_;
if ($chr ne $snp_chr){return "out"};
if ($read_start>$snp_position or $snp_position > ($read_start + (length $sequence))){return "out"}

my $snp_read_pos = $snp_position - $read_start;
my $base_at_snp_pos = substr($sequence, $snp_read_pos,1);

if ($snp eq $base_at_snp_pos)
  {
    #print "Y\t$base_at_snp_pos\t".substr($sequence, $snp_read_pos-4,9)."\n";
    return "Y"
  }
else
  {
    #print "N\t$base_at_snp_pos\t".substr($sequence, $snp_read_pos-4,9)."\n";
    return $base_at_snp_pos
  }  
}


# This performs a binary search of a sorted array returning the start and end coordinates of the fragment 1 based - using the midpoints of the RE cut site
sub binary_search
{
    my ($arrayref, $start, $end, $counter_ref) = @_;
    #print "\n searching for $start - $end\t";
    my $value = ($start + $end)/2;
    my $array_position_min = 0;
    my $array_position_max = scalar @$arrayref-1; #needs to be -1 for the last element in the array
    my $counter =0;
    if (($value < $$arrayref[$array_position_min]) or ($value > $$arrayref[$array_position_max])){$$counter_ref{"25ee Binary search error - search outside range of restriction enzyme coords:"}++; return ("error", "error")}
    
    for (my $i=0; $i<99; $i++)
    {
    my $mid_search = int(($array_position_min+$array_position_max)/2);
    
    if ($$arrayref[$mid_search]>$$arrayref[$mid_search+1]){$$counter_ref{"25ee Binary search error - restriction enzyme array coordinates not in ascending order:"}++; return ("error", "error")}
    

    if (($$arrayref[$mid_search] <= $value) and  ($$arrayref[$mid_search+1] > $value)) # maps the mid point of the read to a fragment
    {
      if (($$arrayref[$mid_search] <= $start+2) and  ($$arrayref[$mid_search+1] >= $end-2)) # checks the whole read is on the fragment +/-2 to allow for the dpnII overlaps
	{
	  return ($$arrayref[$mid_search], $$arrayref[$mid_search+1]-1)
	}
      else{$$counter_ref{"25ee Binary search error - fragment overlapping multiple restriction sites:"}++; return ("error", "error");}
    }
    
    elsif ($$arrayref[$mid_search] > $value){$array_position_max = $mid_search-1}    
    elsif ($$arrayref[$mid_search] < $value){$array_position_min = $mid_search+1}
    else {$$counter_ref{"25ee Binary search error - end of loop reached:"}++}
    }
    $$counter_ref{"25ee Binary search error - couldn't map read to fragments:"}++;
    return ("error", "error")
}

# This subroutine generates a gff file from the data 
sub frag_to_migout  
{
    my ($hashref, $filenameout, $fragtype, $capture) = @_;
    my %bins;
    
    if (keys %{$$hashref{$fragtype}{$capture}})
    {
      
    unless (open(MIGOUTPUT, ">$filenameout.gff")){print STDERR "Cannot open file $filenameout.gff\n";}
    foreach my $storedChr (sort keys %{$$hashref{$fragtype}{$capture}})  #{ $hash{$b} <=> $hash{$a} }  { {$hash{$storedChr}{$b}} <=> {$hash{$storedChr}{$a}} }
    {
    foreach my $storedposition (sort keys %{$$hashref{$fragtype}{$capture}{$storedChr}})
        {         
              print MIGOUTPUT "chr$storedChr\t$version\t$capture\t$storedposition\t".$$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"end"}."\t".$$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"value"}."\t+\t0\t.\n"
        }
    }
    
    }
}

#This subroutine generates a windowed wig track based on using the midpoint of the fragment to represent all of the reads mapping to that fragment
sub frag_to_windowed_wigout  
{
    my ($hashref, $filenameout, $fragtype, $capture, $window_size, $window_incr) = @_;
    my %bins;
    
    if (keys %{$$hashref{$fragtype}{$capture}})
    {
    
    unless (open(WIGOUTPUT, ">$filenameout\_win.wig")){print STDERR "Cannot open file $filenameout.wig\n";}
    foreach my $storedChr (sort keys %{$$hashref{$fragtype}{$capture}})  #{ $hash{$b} <=> $hash{$a} }  { {$hash{$storedChr}{$b}} <=> {$hash{$storedChr}{$a}} }
    {
    foreach my $storedposition (sort keys %{$$hashref{$fragtype}{$capture}{$storedChr}})
        {   
        
              my $startsamm = $storedposition +(($$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"end"}-$storedposition)/2);  #finds the midpoint of the fragment / half fragment
              my $int = int($startsamm / $window_size);
              my $start_bin = ($int * $window_size);
              my $diff = $startsamm - $start_bin;
              my $incr = (int(($window_size - $diff) / $window_incr) * $window_incr);
              $start_bin -= $incr;
	
		for (my $bin=$start_bin; $bin<($start_bin+$window_size); $bin+=$window_incr)
		{
			unless (($storedChr =~ /M|m/)||($bin <= 0))
			{
			$bins{$storedChr}{$bin} += $$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"value"};
			}
		}
        }
    }       
    foreach my $storedChr (sort keys %bins)  #{ $hash{$b} <=> $hash{$a} }  { {$hash{$storedChr}{$b}} <=> {$hash{$storedChr}{$a}} }
    {
    print WIGOUTPUT "variableStep  chrom=chr$storedChr  span=$window_incr\n";
    foreach my $storedposition (sort keys %{$bins{$storedChr}})
        {   
            print WIGOUTPUT "$storedposition\t".$bins{$storedChr}{$storedposition}."\n";
        }
    }
    
    }
}



# This subroutine outputs the data from a hash of dpnII fragments of format %hash{$fragtype}{$capture}{$chr}{$fragment_start}{"end"/"value"} to wig format
sub frag_to_wigout  
{
    my ($hashref, $filenameout, $fragtype, $capture) = @_;
    
    if (keys %{$$hashref{$fragtype}{$capture}})
    {
    
    unless (open(WIGOUTPUT, ">$filenameout.wig")){print STDERR "Cannot open file $filenameout.wig\n";}
    foreach my $storedChr (sort keys %{$$hashref{$fragtype}{$capture}})  
    {
    print WIGOUTPUT "variableStep  chrom=chr$storedChr\n";
    
    foreach my $storedposition (sort keys %{$$hashref{$fragtype}{$capture}{$storedChr}})
        {   
        for (my $i=$storedposition; $i<=$$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"end"}; $i++)
            {
            print WIGOUTPUT "$i\t".$$hashref{$fragtype}{$capture}{$storedChr}{$storedposition}{"value"}."\n";
            }
        }
    }
    
    }
}


#This subroutine generates a mig/gff file (hash reference, reference to the array of the information for the 9th column, output filename)
sub migout
{
    my ($hashref, $refarray, $filenameout) = @_;
    
    #if (keys %{$$hashref{$fragtype}{$capture}})
    #{
    
    unless (open(MIGOUTPUT, ">$filenameout.gff")){print STDERR "Cannot open file $filenameout.mig\n";}
    foreach my $storedChr (sort keys %$hashref)  #{ $hash{$b} <=> $hash{$a} }  { {$hash{$storedChr}{$b}} <=> {$hash{$storedChr}{$a}} }
    {
    foreach my $storedposition (sort keys %{$$hashref{$storedChr}})
        {   
        print MIGOUTPUT "Chr$storedChr\tMIG\tsequence_feature\t$storedposition\t".$$hashref{$storedChr}{$storedposition}{"fragend"}."\t.\t.\t.\t";
        for (my $i=0; $i<scalar(@$refarray); $i++)
            {
                print MIGOUTPUT $$refarray[$i]."=".$$hashref{$storedChr}{$storedposition}{$$refarray[$i]}.";";
            }
        print MIGOUTPUT "\n"    
        }
    }
    
    #}
    
}

#This subroutine generates a mig/gff file (hash reference, reference to the array of the information for the 9th column, output filename)
sub fragtable_out
{
    my ($hashref, $refarray, $refgenomehash, $sample, $filenameout) = @_;
    unless (open(OUTPUT, ">$filenameout.txt")){print STDERR "Cannot open file $filenameout.txt\n";}
    foreach my $storedChr (sort keys %$refgenomehash)  #{ $hash{$b} <=> $hash{$a} }  { {$hash{$storedChr}{$b}} <=> {$hash{$storedChr}{$a}} }
    {
    foreach my $storedposition (sort keys %{$$hashref{$storedChr}})
        {   
        print OUTPUT "Chr$storedChr\tMIG\tsequence_feature\t$storedposition\t".$$hashref{$storedChr}{$storedposition}{"fragend"}."\t.\t.\t.\t";
        for (my $i=0; $i<scalar(@$refarray); $i++)
            {
                print OUTPUT $$refarray[$i]."=".$$hashref{$storedChr}{$storedposition}{$$refarray[$i]}.";";
            }
        print MIGOUTPUT "\n"    
        }
    }    
    
}



#wigtobigwig (Filename (filename without the .wig extension), Filename for report (full filename), Description for UCSC)
#This subroutine converts a wig file into big wig format and copies it into the public folder.  It also generates a small file with the line to paste into UCSC
#if this fails to work try running: module add ucsctools  at the unix command line
sub wigtobigwig 
{
    my ($filename, $report_filehandle, $public_folder, $public_url, $description) = @_;
    print $report_filehandle "track type=bigWig name=\"$filename\" description=\"$description\" bigDataUrl=http://$public_url/$filename.bw\n";
    print "track type=bigWig name=\"$filename\" description=\"$description\" bigDataUrl=http://$public_url/$filename.bw\n";
    
    system ("wigToBigWig -clip $filename.wig $bigwig_folder/$genome\_sizes.txt $filename.bw") == 0 or print STDOUT "couldn't bigwig $genome file $filename\n";
    my $short_filename = $filename.".bw";
    if ($short_filename =~ /(.*)\/(\V++)/) {$short_filename = $2};
    system ("mv $filename.bw $public_folder/$short_filename") == 0 or print STDOUT "couldn't move $genome file $filename\n";		
    system ("chmod 755 $public_folder/$short_filename") == 0 or print STDOUT "couldn't chmod $genome file $filename\n";    
}

#This ouputs a the hash of arrays in the format: samhash{name of capture}[line of sam file]
#It uses the an array taken from the top of the input sam file to generate the headder of the sam file

sub output_hash_sam
{
  my ($hashref, $filenameout, $capture, $samheadder_arrayref) = @_;
  unless (open(HASHOUTPUT, ">$filenameout.sam")){print STDERR "Cannot open file $filenameout\n";}
  for (my $i=0; $i < scalar @$samheadder_arrayref; $i++){print HASHOUTPUT $$samheadder_arrayref[$i]."\n";}  #Prints out the headder from the original sam file
    foreach my $value (@{$$hashref{$capture}})
    {
      print HASHOUTPUT $value."\n";
    }        
}

#This ouputs a 2column hash to a file
sub output_hash
{
    my ($hashref, $filehandleout_ref) = @_;
    foreach my $value (sort keys %$hashref)
    {
    print $filehandleout_ref "$value\t".$$hashref{$value}."\n";
    }        
}


#James Davies 2014
