#!/usr/bin/env perl

#in_silico_pcr.pl
#Copyright (C) 2017-2019 Egon A. Ozer
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see [http://www.gnu.org/licenses/].

my $version = "0.5";

## changes from v0.4
## fixed bug where if amplicons started at the same position on multiple different contigs, only one would be reported

## changes from v0.3
## can take a list of primer sequences. This can save time on repeatedly reading the sequence file.
## changed output format somewhat
## when only one primer is bound and the -c option is given, only output sequence from the primer up to the maximum band length (-l)
## fixed some bugs that could have resulted in incorrect reverse complementation if there was in indel in the first primer sequence

## changes from v0.2
## when using option -c, will now output all primer binding results, regardless of whether the distance from the primer to the end of the sequence is less than the maximum amplicon length or not. 
## added ability to find primer sequences with up to one indel

use strict;
use Cwd;
use warnings;

## Usage
my $usage = "
in_silico_PCR.pl

Adapted from Joseba Bikandi's php script
(http://www.biophp.org/minitools/pcr_amplification/)

Required:
  -s <string>   Sequence file in fasta format (can be gzipped, must have .gz suffix)
  
Options:
  -a <string>   Forward primer
  -b <string>   Reverse primer
    OR
  -p            file with multiple primer sets
                Format should be:
                    forward_primer<tab>reverse_primer<tab>output_prefix
                with one primer set per line.
                If this option is given, values given to -a and -b will be
                ignored
  -l <number>   Maximum length of the resulting \"band\" (default: 3000 bases)
  -m            Allow up to one mismatch per primer sequence
                (default, no mismatches)
  -i            Allow up to one insertion or deletion per primer sequence
                (default, no indels)
  -e            Exclude primer sequences from amplicon sequence, position, and
                length (default: primer sequences included)
  -r            Ensure that amplicons are in the orientation given by the order
                of the primers, i.e. forward primer at 5' end, reverse primer
                at 3' end (default: amplicons will be output in the orientation
                found in the input sequence)
  -c            If no amplicons are found in the sequence, will instead output
                all primer hits followed by sequence to the end of the sequence
                unit or the maximum \"band\" length, whichever is shorter. Could
                be helpful when trying to amplify across a sequencing contig
                break.

";


use Getopt::Std;
use vars qw( $opt_s $opt_a $opt_b $opt_p $opt_l $opt_m $opt_i $opt_e $opt_r $opt_c);
getopts('s:a:b:p:l:mierc');

die $usage unless ($opt_s);
die $usage unless (($opt_a and $opt_b) or $opt_p);

my $seqfile     = $opt_s if $opt_s;
my $primer1     = $opt_a if $opt_a;
my $primer2     = $opt_b if $opt_b;
my $pfile       = $opt_p if $opt_p;
my $maxlength   = $opt_l ? $opt_l : 3000;

my $in;
if ($seqfile =~ m/\.gz$/){
    open ($in, "gzip -cd '$seqfile' |") or die "Can't open $seqfile: $!\n";
} else {
    open ($in, "<", $seqfile) or die "Can't open $seqfile\n";
}
my %sequences;
my ($id, $seq);
while (my $line = <$in>){
    chomp $line;
    if ($line =~ m/^>/){
        if ($id){
            $sequences{$id} = $seq;
            $seq = "";
        }
        $id = substr($line,1);
        $id =~ s/\s.*$//; #delete everything after the first space
        next;
    }
    $line = uc($line);
    $line =~ s/\s|\W|\d//g;
    $seq .= $line;
}
close ($in);
$sequences{$id} = $seq;
$seq = "";

my @iupac = (["R", "[AG]"],
             ["Y", "[CT]"],
             ["S", "[GC]"],
             ["W", "[AT]"],
             ["K", "[GT]"],
             ["M", "[AC]"],
             ["B", "[CGT]"],
             ["D", "[AGT]"],
             ["H", "[ACT]"],
             ["V", "[ACG]"],
             ["N", "."],
             ["U", "T"]);

my @prims;
if ($pfile){
    open (my $pin, "<", $pfile) or die "Can't open $pfile: $!\n";
    while (my $fline = <$pin>){
        $fline =~ s/\R/\012/g; #converts to UNIX-style line endings
        my @lines = split("\n", $fline); #need to split lines by line-ending character in the case of Mac-formatted files which only have CR line terminators, not both CR and LF like DOS
        while (@lines){
            my $line = shift @lines;
            my ($for, $rev, $ipref) = split("\t", $line);
            $for =~ s/\s//g;
            $rev =~ s/\s//g;
            push @prims, ([$for, $rev, $ipref]);
        }
    }
    close ($pin);
} else {
    push @prims, ([$primer1, $primer2, ""]);
}

print "AmpId\tSequenceId\tPositionInSequence\tLength\n";

foreach my $slice (@prims){
    my $pref;
    ($primer1, $primer2, $pref) = @{$slice};
    
    ## All non-word characters (\W) and digits(\d) are removed from primers and from sequence file
    ## I'll need to modify a bit to accept multi-contig files
    
    $primer1 = uc($primer1);
    $primer1 =~ s/\W|\d//g;
    $primer2 = uc($primer2);
    $primer2 =~ s/\W|\d//g;
    
    ##SET PATTERNS FROM PRIMERS
    my $pattern1 = $primer1;
    my $pattern2 = $primer2;
    ## If one missmatch is allowed, create new pattern
    ## example: pattern="ACGT"; to allow one missmatch pattern=".CGT|A.GT|AC.T|ACG."
    if ($opt_m){
        $pattern1 = includeN($primer1);
        $pattern2 = includeN($primer2);
    }
    ## If one indel is allowed, create new pattern
    ## example: pattern="ACGT"; to allow one indel pattern="A.CGT|AC.GT|ACG.T|AGT|ACT"
    ## will only add indels to original sequence, not sequences with mismatches
    my ($indel1, $indel2);
    if ($opt_i){
        $indel1 = indel($primer1);
        $indel2 = indel($primer2);
    }
    
    ## Change non-standard nucleotides in primers
    for my $i (0 .. $#iupac){
        my ($from, $to) = @{$iupac[$i]};
        $pattern1 =~ s/$from/$to/g;
        $pattern2 =~ s/$from/$to/g;
        if ($opt_i){
            $indel1 =~ s/$from/$to/g;
            $indel2 =~ s/$from/$to/g;
        }
    }
    
    ## SET PATTERN
    my $start_pattern = "$pattern1|$pattern2";
    my $end_pattern = reverse ($start_pattern);
    $end_pattern =~ tr/ACTG[]/TGAC][/;
    my ($full_start, $full_end) = ($start_pattern, $end_pattern);
    if ($opt_i){
        my $start_indel = "$indel1|$indel2";
        my $end_indel = reverse($start_indel);
        $end_indel =~ tr/ACTG[]/TGAC][/;
        $full_start .= "|$start_indel";
        $full_end .= "|$end_indel";
    }
    ## For determining strand
    my ($for_pattern, $rev_pattern) = ($pattern1, $pattern2);
    if ($opt_i){
        $for_pattern .= "|$indel1";
        $rev_pattern .= "|$indel2";
    }
    
    my %results_hash = Amplify($full_start, $full_end, $maxlength, $for_pattern);
    
    ## PRINT RESULTS
    if (scalar keys %results_hash > 0){
        my $count = 0;
        foreach my $id (sort {$a cmp $b} keys %results_hash){
            foreach my $key (sort {$a<=>$b} keys %{$results_hash{$id}}){
                $count++;
                my ($val, $rc) = @{$results_hash{$id}{$key}};
                my $sequence = $sequences{$id};
                my $amp = substr($sequence, $key, $val);
                if ($opt_i){
                    #check to make sure that an extra base wasn't added to the end of the sequence due to an indel pattern
                    my @check = split(/($start_pattern)/, $amp);
                    if (length($check[0]) == 1){
                        $amp = substr($amp, 1);
                        $val--;
                        $key++;
                    } elsif (length($check[$#check]) == 1){
                        $amp = substr($amp, 0, length($amp) - 1);
                        $val--;
                    }
                    my @check2 = split(/$end_pattern/, $amp);
                    if (length($check2[0]) == 1){
                        $amp = substr($amp, 1);
                        $val--;
                        $key++;
                    } elsif (length($check2[$#check2]) == 1){
                        $amp = substr($amp, 0, length($amp) - 1);
                        $val--;
                    }
                }
                my $ampID;
                $ampID = "$pref\_" if $pref;
                $ampID .= "amp_$count";
                print "$ampID\t$id\t". ($key + 1) ."\t$val";
                if ($opt_r){
                    print "\tcomplement" if $rc eq "y";
                }
                print "\n";
                if ($opt_r and $rc eq "y"){
                    $amp = reverse($amp);
                    $amp =~ tr/ACTGRYKMBVDHactgrykmbvdh/TGACYRMKVBHDtgacyrmkvbhd/;
                }
                print STDERR ">$ampID\n$amp\n";
            }
        } 
    } else {
        if ($opt_c){
            my @c_array = C_amplify($for_pattern, $rev_pattern, $maxlength);
            if (scalar @c_array > 0){
                @c_array = sort{$a->[0] cmp $b->[0]} @c_array;
                foreach my $slice (@c_array){
                    my ($type, $id, $pos, $seq) = @{$slice};
                    if ($opt_i){
                        #check to make sure that an extra base wasn't added to the end of the sequence due to an indel pattern
                        my @check = split(/($start_pattern)/, $seq);
                        if (length($check[0]) == 1){
                            $seq = substr($seq, 1);
                            $pos++;
                        } elsif (length($check[$#check]) == 1){
                            $seq = substr($seq, 0, length($seq) - 1);
                        }
                        my @check2 = split(/$end_pattern/, $seq);
                        if (length($check2[0]) == 1){
                            $seq = substr($seq, 1);
                            $pos++;
                        } elsif (length($check2[$#check2]) == 1){
                            $seq = substr($seq, 0, length($seq) - 1);
                        }
                    }
                    $type = "$pref\_$type" if $pref;
                    my $seqleng = length($seq);
                    if ($seqleng > $maxlength){
                        $seq = substr($seq, 0, $maxlength);
                        $seqleng = $maxlength;
                    }
                    print "$type\t$id\t$pos\t$maxlength\n";
                    print STDERR ">$type\n$seq\n";
                }
            } else {
                print "$pref\t" if $pref;
                print "No amplification\n";
            }
        } else {
            print "$pref\t" if $pref;
            print "No amplification\n";
        }
    }
}

#----------------------------------------------------------------------
sub includeN {
    my $pattern = shift;
    my $new_pattern;
    if (length($pattern) > 2){
        $new_pattern = "." . substr($pattern, 1);
        my $pos = 1;
        while ($pos < length($pattern)){
            $new_pattern .= "|" . substr($pattern, 0, $pos) . "." . substr($pattern, $pos+1);
            $pos++;
        }
    }
    return ($new_pattern);
}

sub indel {
    my $pattern = shift;
    my ($ins, $del, $indel);
    if (length($pattern) > 2){
        $ins = substr($pattern, 0, 1) . "." . substr($pattern, 1);
        my $pos = 1;
        while ($pos < length($pattern) - 1){
            $ins .= "|" . substr($pattern, 0, 1 + $pos) . "." . substr($pattern, 1 + $pos);
            $pos++;
        }
        
        $del = substr($pattern, 0, 1) . substr($pattern, 2);
        $pos = 2;
        while ($pos < length($pattern) - 1){
            $del .= "|" . substr($pattern, 0, $pos) . substr($pattern, 1 + $pos);
            $pos++;
        }
        
        $indel = $ins . "|" . $del;
    }
    return ($indel);
}

sub Amplify {
    my $start_pattern = shift;
    my $end_pattern = shift;
    my $maxlength = shift;
    my $for_pattern = shift;
    
    my %results_hash;
    ## SPLIT SEQUENCE BASED IN $start_pattern (start positions of amplicons)
    
    foreach my $id (sort keys %sequences){
        my $sequence = $sequences{$id};
        my @fragments = split(/($start_pattern)/, $sequence);
        my $maxfragments = scalar @fragments;
        my $position = length($fragments[0]);
        if ($maxfragments > 1){
            for (my $m = 1; $m < $maxfragments ; $m+= 2){
                my $subfragment_to_maximum = substr($fragments[$m + 1], 0, $maxlength);
                my @fragments2 = split(/($end_pattern)/, $subfragment_to_maximum);
                
                if (scalar @fragments2 > 1){
                    my $lenfragment = length($fragments[$m].$fragments2[0].$fragments2[1]);
                    my $rc = "y";
                    if ($opt_r){
                        my $amp = substr($sequence, $position, $lenfragment);
                        if ($amp =~ m/^$for_pattern/){ #check if the amplicon begins with primer1
                            $rc = "n";
                        }
                    }
                    if (!$opt_e){
                        $results_hash{$id}{$position} = ([$lenfragment, $rc]);
                    } else {
                        my $new_pos = $position + length $fragments[$m];
                        my $new_len = length $fragments2[0];
                        $results_hash{$id}{$new_pos} = ([$new_len, $rc]);
                    }
                }
                $position += length($fragments[$m]) + length($fragments[$m+1]);
            }
        }
    }
    return(%results_hash);
}

sub C_amplify {
    my $pattern1 = shift;
    my $pattern2 = shift;
    my $maxlength = shift;
    
    my $pattern1_rc = reverse($pattern1);
    $pattern1_rc =~ tr/ACTG[]/TGAC][/;
    my $pattern2_rc = reverse($pattern2);
    $pattern2_rc =~ tr/ACTG[]/TGAC][/;
    
    my @results;
    my @counts = (0) x 4;
    
    foreach my $id (sort keys %sequences){
        my $sequence = $sequences{$id};
        my @fragments = split(/($pattern1)/, $sequence);
        my $maxfragments = scalar @fragments;
        my $position = 0;
        #$position = length($fragments[0]) if ($fragments[0] !~ m/$pattern1/);
        if (@fragments > 1){
            while (@fragments){
                my $frag = shift @fragments;
                my $newpos = $position + length($frag);
                if ($frag =~ m/$pattern1/){
                    my $outpos = $position;
                    $outpos = $newpos if $opt_e;
                    my $subfragment = substr($sequence, $outpos);
                    $counts[0]++;
                    push @results, (["p1\_$counts[0]", $id, $outpos, $subfragment]);
                }
                $position = $newpos;
            }
        }
        
        @fragments = split(/($pattern1_rc)/, $sequence);
        $maxfragments = scalar @fragments;
        $position = 0;
        #$position = length($fragments[0]) if ($fragments[0] !~ m/$pattern1_rc/);
        if (@fragments > 1){
            while (@fragments){
                my $frag = shift @fragments;
                my $newpos = $position + length($frag);
                if ($frag =~ m/$pattern1_rc/){
                    my $outpos = $newpos;
                    $outpos = $position if $opt_e;
                    my $subfragment = substr($sequence, 0, $outpos);
                    $subfragment = reverse($subfragment);
                    $subfragment =~ tr/ACTGRYKMBVDHactgrykmbvdh/TGACYRMKVBHDtgacyrmkvbhd/;
                    $counts[1]++;
                    push @results, (["p1rc_$counts[1]", $id, $outpos, $subfragment]);
                }
                $position = $newpos;
            }
        }
        
        @fragments = split(/($pattern2)/, $sequence);
        $maxfragments = scalar @fragments;
        $position = 0;
        #$position = length($fragments[0]) if ($fragments[0] !~ m/$pattern2/);
        if (@fragments > 1){
            while (@fragments){
                my $frag = shift @fragments;
                my $newpos = $position + length($frag);
                if ($frag =~ m/$pattern2/){
                    my $outpos = $position;
                    $outpos = $newpos if $opt_e;
                    my $subfragment = substr($sequence, $outpos);
                    $subfragment = reverse($subfragment);
                    $subfragment =~ tr/ACTGRYKMBVDHactgrykmbvdh/TGACYRMKVBHDtgacyrmkvbhd/;
                    $counts[2]++;
                    push @results, (["p2_$counts[2]", $id, $outpos, $subfragment]);
                }
                $position = $newpos;
            }
        }
        
        @fragments = split(/($pattern2_rc)/, $sequence);
        $maxfragments = scalar @fragments;
        $position = 0;
        #$position = length($fragments[0]) if ($fragments[0] !~ m/$pattern2_rc/);
        if (@fragments > 1){
            while (@fragments){
                my $frag = shift @fragments;
                my $newpos = $position + length($frag);
                if ($frag =~ m/$pattern2_rc/){
                    my $outpos = $newpos;
                    $outpos = $position if $opt_e;
                    my $subfragment = substr($sequence, 0, $outpos);
                    $counts[3]++;
                    push @results, (["p2rc_$counts[3]", $id, $outpos, $subfragment]);
                }
                $position = $newpos;
            }
        }
    }
    return(@results);
}

