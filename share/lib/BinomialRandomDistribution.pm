#! /usr/bin/perl -w

package BinomialRandomDistribution;

use strict;
use warnings;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(readFromFile writeToFile initialRange solveEquation perCalculation calculateKU calculateKDU calculateKD2U calculateKD3U calculateKD4U calculateW calculateU1 calculateKD2ZEROKD3ZERO calculateUppercasePhi calculateLowcasePhi calculateU2 calculateK3 calculateK4 calculateP3 calculateP4 calculatePValue);

use constant PI	=>	4 * atan2(1, 1);

sub new
{
	my $self = {};

	$self->{"neighborhoodFile"} = "NA";
	$self->{"pValueFile"} = "NA";

	$self->{"s"} = [];
	$self->{"p"} = [];
	$self->{"q"} = [];

	$self->{"x1"} = -1;
	$self->{"x2"} = 1;

	$self->{"k"} = "NA";
	$self->{"e"} = 1e-200;

	$self->{"u"} = "NA";
	$self->{"fu"} = "NA";

	$self->{"expu"} = "NA";

	$self->{"expectedS"} = "NA";

	$self->{"ku"} = "NA";
	$self->{"kdu"} = "NA";
	$self->{"kd2u"} = "NA";
	$self->{"kd3u"} = "NA";
	$self->{"kd4u"} = "NA";
	
	$self->{"kd2Zero"} = "NA";
	$self->{"kd3Zero"} = "NA";
	
	$self->{"w"} = "NA";
	$self->{"u1"} = "NA";

	$self->{"uppercasePhiW"} = "NA";
	$self->{"lowcasePhiW"} = "NA";

	$self->{"p3"} = "NA";
	
	$self->{"u2"} = "NA";
	$self->{"k3"} = "NA";
	$self->{"k4"} = "NA";

	$self->{"p4"} = "NA";

	$self->{"error"} = "Error";

	bless $self;

	return $self;
}

sub readFromFile
{
	my $self = shift;

	if ($self->{"neighborhoodFile"} eq "NA")
	{
		$self->{"error"} = "No define neighborhood file!";
	}
	else
	{
		my $file = $self->{"neighborhoodFile"};

		if (!(-e $file))
		{
			$self->{"error"} = "neighborhood file doesn't exist!";	
		}
		else
		{
			undef @{$self->{"s"}};
			undef @{$self->{"p"}};
			undef @{$self->{"q"}};

			$self->{"x1"} = -1;
			$self->{"x2"} = 1;
	
			$self->{"k"} = "NA";
			$self->{"e"} = 1e-200;
	
			$self->{"u"} = "NA";
			$self->{"fu"} = "NA";
	
			$self->{"expu"} = "NA";

			$self->{"expectedS"} = "NA";
	
			$self->{"ku"} = "NA";
			$self->{"kdu"} = "NA";
			$self->{"kd2u"} = "NA";
			$self->{"kd3u"} = "NA";
			$self->{"kd4u"} = "NA";
	
			$self->{"kd2Zero"} = "NA";
			$self->{"kd3Zero"} = "NA";
	
			$self->{"w"} = "NA";
			$self->{"u1"} = "NA";
	
			$self->{"uppercasePhiW"} = "NA";
			$self->{"lowcasePhiW"} = "NA";
	
			$self->{"p3"} = "NA";

			$self->{"u2"} = "NA";
			$self->{"k3"} = "NA";
			$self->{"k4"} = "NA";
			
			$self->{"p4"} = "NA";
	
			$self->{"error"} = "NA";

			open (IN,$file) || die "can't open the file:$!\n";

			my $readline = <IN>;

			chomp $readline;

			if ($readline =~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
			{
				$self->{"k"} = $readline;
			}
			else
			{
				$self->{"error"} = "neighborhood file is wrong!";
			}

			while (defined($readline=<IN>))
			{
				chomp $readline;
				
				my @fields = split(/\t/,$readline);

				my $k = int(@{$self->{"s"}});

#				if (($fields[0] =~ /^(\d+)$/)&&($fields[1] =~ /^(\d+)(\.?)(\d+)/))
				if (($fields[0] =~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($fields[1] =~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/))
				{
					$self->{"s"}[$k] = $fields[0];
					$self->{"p"}[$k] = $fields[1];
				}
				else
				{
					$self->{"error"} = "neighborhood file is wrong!";
				}
			}
				
			close IN;
		}
	}
}

sub writeToFile
{
	my $self = shift;
	
	if ($self->{"pValueFile"} eq "NA")
	{
		$self->{"error"} = "No define pvalue file!";
	}
	else
	{
		my $file = $self->{"pValueFile"};

		open (OUT,">".$file) || die "can't write to the file:$!\n";

		print OUT "inBedIndexSNPNum\t=\t".$self->{"k"}."\n";

		print OUT "expectedS\t=\t".$self->{"expectedS"}."\n";

		print OUT "x1\t=\t".$self->{"x1"}."\n";
		print OUT "x2\t=\t".$self->{"x2"}."\n";
		
		print OUT "u\t=\t".$self->{"u"}."\n";
		print OUT "fu\t=\t".$self->{"fu"}."\n";

		print OUT "ku\t=\t".$self->{"ku"}."\n";
		print OUT "kdu\t=\t".$self->{"kdu"}."\n";
		print OUT "kd2u\t=\t".$self->{"kd2u"}."\n";
		print OUT "kd3u\t=\t".$self->{"kd3u"}."\n";
		print OUT "kd4u\t=\t".$self->{"kd4u"}."\n";
		
		print OUT "kd2Zero\t=\t".$self->{"kd2Zero"}."\n";
		print OUT "kd3Zero\t=\t".$self->{"kd3Zero"}."\n";
		
		print OUT "w\t=\t".$self->{"w"}."\n";
		print OUT "u1\t=\t".$self->{"u1"}."\n";
		
		print OUT "uppercasePhiW\t=\t".$self->{"uppercasePhiW"}."\n";
		print OUT "lowcasePhiW\t=\t".$self->{"lowcasePhiW"}."\n";
		
		print OUT "p3\t=\t".$self->{"p3"}."\n";

		print OUT "u2\t=\t".$self->{"u2"}."\n";
		print OUT "k3\t=\t".$self->{"k3"}."\n";
		print OUT "k4\t=\t".$self->{"k4"}."\n";

		print OUT "p4\t=\t".$self->{"p4"}."\n";
		
		print OUT "error\t=\t".$self->{"error"}."\n";

		close OUT;
	}
}

sub fifdint
{
	my ($x) = @_;
	
	my $ret = int($x);
	
	return ($ret);
}

sub cumnor
{
	my ($z) = @_;
	
	my $p = "NA";
	my $q = "NA";
	
	my @a;
	$a[0] = 2.2352520354606839287e00;
	$a[1] = 1.6102823106855587881e02;
	$a[2] = 1.0676894854603709582e03;
	$a[3] = 1.8154981253343561249e04;
	$a[4] = 6.5682337918207449113e-2;
		
	my @b;
	$b[0] = 4.7202581904688241870e01;
	$b[1] = 9.7609855173777669322e02;
	$b[2] = 1.0260932208618978205e04;
	$b[3] = 4.5507789335026729956e04;
	
	my @c;
	$c[0] = 3.9894151208813466764e-1;
	$c[1] = 8.8831497943883759412e00;
	$c[2] = 9.3506656132177855979e01;
	$c[3] = 5.9727027639480026226e02;
	$c[4] = 2.4945375852903726711e03;
	$c[5] = 6.8481904505362823326e03;
	$c[6] = 1.1602651437647350124e04;
	$c[7] = 9.8427148383839780218e03;
	$c[8] = 1.0765576773720192317e-8;
	
	my @d;
	$d[0] = 2.2266688044328115691e01;
	$d[1] = 2.3538790178262499861e02;
	$d[2] = 1.5193775994075548050e03;
	$d[3] = 6.4855582982667607550e03;
	$d[4] = 1.8615571640885098091e04;
	$d[5] = 3.4900952721145977266e04;
	$d[6] = 3.8912003286093271411e04;
	$d[7] = 1.9685429676859990727e04;
	
	my $half = 0.5e0;
	
	my @p;
	$p[0] = 2.1589853405795699e-1;
	$p[1] = 1.274011611602473639e-1;
	$p[2] = 2.2235277870649807e-2;
	$p[3] = 1.421619193227893466e-3;
	$p[4] = 2.9112874951168792e-5;
	$p[5] = 2.307344176494017303e-2;
	
	my $one = 1.0e0;

	my @q;
	$q[0] = 1.28426009614491121e00;
	$q[1] = 4.68238212480865118e-1;
	$q[2] = 6.59881378689285515e-2;
	$q[3] = 3.78239633202758244e-3;
	$q[4] = 7.29751555083966205e-5;
	
	my $sixten = 1.60e0;
	my $sqrpi = 3.9894228040143267794e-1;
	my $thrsh = 0.66291e0;
	my $root32 = 5.656854248e0;
	my $zero = 0.0e0;
	my $K1 = 1;
	my $K2 = 2;
	my $i;
	my $del;
	my $eps;
	my $temp;
	my $x;
	my $xden;
	my $xnum;
	my $y;
	my $xsq;
	my $min;
	
	my $result;
	my $ccum;
	
	$eps = 1.11022e-16;
	$min = 2.22507e-308;
	$x = $z;
	$y = abs($x);
	
	if($y <= $thrsh) #Evaluate  anorm  for  |X| <= 0.66291
	{
		$xsq = $zero;
		
		if($y > $eps)
		{
			$xsq = $x * $x;
		}
		
		$xnum = $a[4] * $xsq;
		$xden = $xsq;
		
		for (my $i = 0; $i < 3; $i++ )
		{
			$xnum = ($xnum + $a[$i]) * $xsq;
			$xden = ($xden + $b[$i]) * $xsq;
		}
		
		$result = $x * ($xnum + $a[3]) / ($xden + $b[3]);
		$temp = $result;
		$result = $half + $temp;
		$ccum = $half - $temp;
	}
	elsif($y <= $root32)   # Evaluate  anorm  for 0.66291 <= |X| <= sqrt(32)
	{
		$xnum = $c[8] * $y;
		$xden = $y;
		
		for (my $i = 0; $i < 7; $i++ )
		{
			$xnum = ($xnum + $c[$i]) * $y;
			$xden = ($xden + $d[$i]) * $y;
		}
		
		$result = ($xnum + $c[7]) / ($xden + $d[7]);
		$xsq = fifdint($y * $sixten) / $sixten;
		$del = ($y - $xsq) * ($y + $xsq);
		$result = exp(-($xsq * $xsq * $half))*exp(-($del * $half)) * $result;
		$ccum = $one - $result;
		
		if($x > $zero)
		{
			$temp = $result;
			$result = $ccum;
			$ccum = $temp;
		}
	}
	else                    # Evaluate  anorm  for |X| > sqrt(32)
	{
		$result = $zero;
		$xsq = $one / ($x * $x);
		$xnum = $p[5] * $xsq;
		$xden = $xsq;
		
		for (my $i = 0; $i < 4; $i++ )
		{
			$xnum = ($xnum + $p[$i]) * $xsq;
			$xden = ($xden + $q[$i]) * $xsq;
			
		}
		
		$result = $xsq * ($xnum + $p[4]) / ($xden + $q[4]);                                 
		
		$result = ($sqrpi - $result) / $y;

    $xsq = fifdint($x * $sixten) / $sixten;

    $del = ($x - $xsq) * ($x + $xsq);

    $result = exp(-($xsq * $xsq * $half)) * exp(-($del * $half)) * $result;

    $ccum = $one - $result;

    if($x > $zero)
    {
	    $temp = $result;
	    $result = $ccum;
	    $ccum = $temp;
	  }
	}
	
	if($result < $min)
	{
		$result = 0.0e0;
	}
	
	if($ccum < $min) # Fix up for negative argument, erf, etc.
	{
		$ccum = 0.0e0;
	}
	
	return ($result,$ccum);
}

sub functionF
{
	my $self = shift;

	my ($x) = @_;

	my @numerator;
	undef @numerator;
	my @denominator;
	undef @denominator;
	
	my $ret = "NA";
	
	my $denominatorIsZero = "false";

	my $expx = exp($x);
	
	for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
	{
		my $pi = $self->{"p"}[$i];

		$denominator[$i] = 1 - $pi + $pi * $expx;
	
		if ($denominator[$i] == 0)
		{
			$denominatorIsZero = "true";
			
			$i = int(@{$self->{"p"}});
		}
	}
	
	if ($denominatorIsZero eq "false")
	{
		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			my $ni = $self->{"s"}[$i];
			my $pi = $self->{"p"}[$i];

			$numerator[$i] = $ni * $pi * $expx;
		}
		
		$ret = 0;
		
		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			$ret = $ret + $numerator[$i] / $denominator[$i];
		}
		
		$ret = $ret - $self->{"k"};
	}
	
	return ($ret);
}

sub fDerivative
{
	my $self = shift;

	my ($x) = @_;
	
	my @numerator;
	undef @numerator;
	my @denominator;
	undef @denominator;
	
	my $ret = "NA";
	
	my $denominatorIsZero = "false";
	
	for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
	{
		$denominator[$i] = 1 - $self->{"p"}[$i] + $self->{"p"}[$i] * exp($x);
		
		$denominator[$i] = $denominator[$i] * $denominator[$i];
		
		if ($denominator[$i] == 0)
		{
			$denominatorIsZero = "true";
			
			$i = int(@{$self->{"p"}});
		}
	}
	
	if ($denominatorIsZero eq "false")
	{
		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			$numerator[$i] = (1 - $self->{"p"}[$i]) * $self->{"s"}[$i] * $self->{"p"}[$i] * exp($x);
		}
		
		$ret = 0;
		
		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			$ret = $ret + $numerator[$i] / $denominator[$i];
		}
	}
	
	return ($ret);
}

sub initialRange
{
	my $self = shift;

	$self->{"error"} = "NA";

	my $NTRY = 50;
	my $FACTOR = 1.6;
	my $tol = 1e-15;

	my $x1 = $self->{"x1"};
	my $x2 = $self->{"x2"};
	my $k = $self->{"k"};
	
	my $foundRange = "can't find the range of x!";

	if ($x1 == $x2)
	{
		return ($foundRange);
	}

	my $fx1 = $self->functionF($x1);
	my $fx2 = $self->functionF($x2);

	for (my $i = 0; $i < $NTRY; $i++)
	{
		if (abs($fx1) <= $tol)
		{
			$self->{"x1"} = $x1;
			$self->{"x2"} = $x2;

			$self->{"u"} = $x1;
			$self->{"fu"} = $fx1;

			$foundRange = "solved!";

			return ($foundRange);
		}

		if (abs($fx2) <= $tol)
		{
			$self->{"x1"} = $x1;
			$self->{"x2"} = $x2;

			$self->{"u"} = $x2;
			$self->{"fu"} = $fx2;

			$foundRange = "solved!";

			return ($foundRange);
		}

		my $tmp = $fx1 * $fx2;

		if ($tmp < 0)
		{
			$self->{"x1"} = $x1;
			$self->{"x2"} = $x2;

			$foundRange = "found!";

			return ($foundRange);
		}

		if (abs($fx1) < abs($fx2))
		{
			$x1 = $x1 + $FACTOR * ($x1 - $x2);
			$fx1 = $self->functionF($x1);
		}
		else
		{
			$x2 = $x2 + $FACTOR * ($x2 - $x1);
			$fx2 = $self->functionF($x2);
		}
	}

	return ($foundRange);
}

sub solveEquation
{
	my $self = shift;

	my $foundRange = $self->initialRange();

	if ($foundRange eq "can't find the range of x!")
	{
		$self->{"error"} = "can't find the range of x!";

		return;
	}
	elsif ($foundRange eq "solved!")
	{
		$self->{"error"} = "NA";

		return;
	}

	my $MAXIT = 100;
	my $tol = 1e-15;

	my $x1 = $self->{"x1"};
	my $x2 = $self->{"x2"};
	my $k = $self->{"k"};

	my $fl = $self->functionF($x1);
	my $fh = $self->functionF($x2);

	if ((($fl > 0) && ($fh > 0)) || (($fl < 0) && ($fh < 0)))
	{
		$self->{"u"} = "NA";
		$self->{"fu"} = "NA";
		
		$self->{"error"} = "x range is not right!";
		
		return;
	}

	if (abs($fl) <= $tol)
	{
		my $u = $x1;
		my $fu = $self->functionF($u);

		$self->{"u"} = $u;
		$self->{"fu"} = $fu;

		$self->{"error"} = "NA";

		return;
	}

	if (abs($fh) <= $tol)
	{
		my $u = $x2;
		my $fu = $self->functionF($u);

		$self->{"u"} = $u;
		$self->{"fu"} = $fu;

		$self->{"error"} = "NA";

		return;
	}

	my $xl = "NA";
	my $xh = "NA";

	if ($fl < 0)
	{
		$xl = $x1;
		$xh = $x2;
	}
	else
	{
		$xh = $x1;
		$xl = $x2;
	}

	my $rts = 0.5 * ($x1 + $x2);
	my $dxold = abs($x2 - $x1);
	my $dx = $dxold;

	my $f = $self->functionF($rts);
	my $df = $self->fDerivative($rts);

	for (my $i = 0; $i < $MAXIT; $i++)
	{
#		print "rts = $rts\tdxold = $dxold\tdx = $dx\tf = $f\tdf =$df\txl = $xl\txh = $xh\n";

		if ((((($rts - $xh) * $df - $f) * (($rts - $xl) * $df - $f)) > 0) || (abs(2.0 * $f) > abs($dxold * $df)))
		{
			$dxold = $dx;
			$dx = 0.5 * ($xh - $xl);
			$rts = $xl + $dx;

			if (abs($xl - $rts) < $tol)
			{
				my $u = $rts;
				my $fu = $self->functionF($u);

				$self->{"u"} = $u;
				$self->{"fu"} = $fu;

				$self->{"error"} = "NA";

				return;
			}
		}
		else
		{
			$dxold = $dx;
			$dx = $f / $df;
			my $tmp = $rts;
			$rts = $rts - $dx;

			if (abs($tmp - $rts) < $tol)
			{
				my $u = $rts;
				my $fu = $self->functionF($u);

				$self->{"u"} = $u;
				$self->{"fu"} = $fu;

				$self->{"error"} = "NA";

				return;
			}
		}

#		if ((abs($xl - $xh) < 1e-15)||(abs($dx) < $self->{"e"}))
#		if (abs($dx) < $self->{"e"})
		if (abs($dx) < $tol)
		{
			my $u = $rts;
			my $fu = $self->functionF($u);

			$self->{"u"} = $u;
			$self->{"fu"} = $fu;

			$self->{"error"} = "NA";

			return;
		}

		$f = $self->functionF($rts);
		$df = $self->fDerivative($rts);

		if ($f < 0)
		{
			$xl = $rts;
		}
		else
		{
			$xh = $rts;
		}
	}

	$self->{"u"} = "NA";
	$self->{"fu"} = "NA";

	$self->{"error"} = "can't solve the equation!";

  return;
}

sub perCalculation
{																				# expu = exp(u); qi = pi*exp(u)/(1-pi+pi*exp(u)); di = 1-pi+pi*exp(u);
	my $self = shift;

	if ($self->{"u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
	{
		$self->{"error"} = "equation hasn't been solved!";
	}

	if ($self->{"error"} eq "NA")
	{
		my $expu = exp($self->{"u"});
		$self->{"expu"} = $expu;

		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			my $pi = $self->{"p"}[$i];
			
			my $tmp = $pi * $expu;
			$tmp = $tmp - $pi;
			$self->{"d"}[$i] = 1 + $tmp;

			if ($self->{"d"}[$i] != 0)
			{
				$tmp = $pi * $expu;
				$self->{"q"}[$i] = $tmp / $self->{"d"}[$i];
			}
			else
			{
				$self->{"q"}[$i] = "NA";

				$self->{"error"} = "1-pi+pi*exp(u) equals to Zero (i = $i\tpi = $pi\tu = ".$self->{"u"}.")!";

				$i = int(@{$self->{"p"}});
			}
		}

## calculate expected S
		$self->{"expectedS"} = 0;

		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			my $pi = $self->{"p"}[$i];
			my $ni = $self->{"s"}[$i];

			if ($pi !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
			{
				$self->{"error"} = "pi(i = $i) is not a number!";
			}
			elsif ($ni !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
			{
				$self->{"error"} = "ni(i = $i) is not a number!";
			}
			else
			{
				$self->{"expectedS"} = $self->{"expectedS"} + $pi * $ni;
			}
		}
	}
}

sub calculateKU
{																				#	K(u) = sigma[si*ln(1-pi+pi*exp(u))]
	my $self = shift;

	$self->{"ku"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $ku = 0;
	
		for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
		{
			my $ni = $self->{"s"}[$i];
			my $di = $self->{"d"}[$i];
		
			if ($di > 0)
			{
				$di = log($di);
				$di = $ni * $di;
				
				$ku = $ku + $di;
			}
			else
			{
				$self->{"error"} = "1-pi+pi*exp(u) is less than or equals to Zero (i = $i\t1-pi+pi*exp(u) = $di)!";
			
				$i = int(@{$self->{"s"}});
			}
		}

		if ($self->{"error"} eq "NA")
		{
			$self->{"ku"} = $ku;
		}
	}
}

sub calculateKDU
{																				# Calculate K'(u);  K'(u) = $self->{"k"}
	my $self = shift;

	$self->{"kdu"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $kdu = "NA";

		if ($self->{"k"} =~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
		{
			$kdu = $self->{"k"};
		}
		else
		{
			$self->{"error"} = "kdu is not a number!";
		}

		if ($self->{"error"} eq "NA")
		{
			$self->{"kdu"} = $kdu;
		}
	}
}

sub calculateKD2U
{																				#	K''(u) = sigma(si*qi(1-qi)), where qi = [pi*exp(u)] / [1 -pi + pi * exp(u)]
	my $self = shift;

	$self->{"kd2u"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $kd2u = 0;

		for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
		{
			my $si = $self->{"s"}[$i];
			my $qi = $self->{"q"}[$i];

			my $tmp = 1 - $qi;
			$tmp = $qi * $tmp;
			$tmp = $si * $tmp;

			$kd2u = $kd2u + $tmp;
		}

		$self->{"kd2u"} = $kd2u;
	}
}

sub calculateKD3U
{																				#	K'''(u) = sigma[si*qi*(1-qi)*(1-2*qi)]
	my $self = shift;

	$self->{"kd3u"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $kd3u = 0;

		for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
		{
			my $si = $self->{"s"}[$i];
			my $qi = $self->{"q"}[$i];

			my $tmp = $si * $qi * (1 - $qi) * (1 - 2 * $qi);
			$kd3u = $kd3u + $tmp;
		}

		$self->{"kd3u"} = $kd3u;
	}
}

sub calculateKD4U
{																				#	K''''(u) = sigma[si*qi*(1-qi)*(1-6*qi*(1-qi))]
	my $self = shift;

	$self->{"kd4u"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $kd4u = 0;

		for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
		{
			my $si = $self->{"s"}[$i];
			my $qi = $self->{"q"}[$i];

			my $tmp = $si * $qi * (1 - $qi) * (1 - 6 * $qi * (1 - $qi));
			$kd4u = $kd4u + $tmp;
		}

		$self->{"kd4u"} = $kd4u;
	}
}

sub calculateW
{																				#	w = (u/|u|)*sqrt(2*(u*K'(u)-K(u)))
	my $self = shift;

	if (($self->{"ku"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKU();
	}

	if (($self->{"kdu"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKDU();
	}

	if ($self->{"error"} eq "NA")
	{
		my $u = $self->{"u"};
		my $ku = $self->{"ku"};
		my $kdu = $self->{"kdu"};

		my $tmp = 2 * ($u * $kdu - $ku);

		if ($tmp < 0)
		{
			$self->{"error"} = "(2uK'(u) - 2K(u)) is less than zero(u = $u\tK'(u) = $kdu\tK(u) = $ku)!";
		}
		else
		{
			$tmp = sqrt($tmp);

			my $w = "NA";

			if ($u == 0)
			{
				$w = 0;
			}
			else
			{
				if ($u < 0)
				{
					$w = -1 * $tmp;
				}
				else
				{
					$w = $tmp;
				}
			}

			$self->{"w"} = $w;
		}
	}
}

sub calculateU1
{																				# Calculate u1;  u1 = {1 - [1 / exp(u)]} * sqrt(K''(u))
	my $self = shift; 

	$self->{"u1"} = "NA";

	if (($self->{"kd2u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD2U();
	}

	if ($self->{"error"} eq "NA")
	{
		my $kd2u = $self->{"kd2u"};

		if ($self->{"kd2u"} < 0)
		{
			$self->{"error"} = "kd2u is less than zero!";
		}
		else
		{
			my $tmp = $self->{"expu"};
			$tmp = 1 / $tmp;
			$tmp = 1 - $tmp;
			
			my $u1 = $tmp * sqrt($kd2u);

			$self->{"u1"} = $u1;
		}
	}
}

sub calculateKD2ZEROKD3ZERO
{																				# Calculate K''(0); K''(0) = sigma[si * pi * (1 - pi)]; Calculate K'''(0); K'''(0) = sigma[si * pi * (1 - pi) * (1 - 2 * pi)]
	my $self = shift;

	$self->{"kd2Zero"} = "NA";
	$self->{"kd3Zero"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		my $kd2Zero = 0;
	  my $kd3Zero = 0;
		
		for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
		{
			my $si = $self->{"s"}->[$i];
			my $pi = $self->{"p"}->[$i];
			
			my $tmp1 = $si * $pi * (1 - $pi);		# tmp1 = si * pi * (1 - pi)
			
			my $tmp2 = $tmp1 * (1 - 2 * $pi);   # tmp2 = si * pi * (1 - pi) * (1 - 2 * pi)
			
			$kd2Zero = $kd2Zero + $tmp1;
			$kd3Zero = $kd3Zero + $tmp2;
		}

		$self->{"kd2Zero"} = $kd2Zero;
		$self->{"kd3Zero"} = $kd3Zero;
	}
}

sub calculateUppercasePhiW
{																				# Calculate uppercasePhi(w); uppercasePhi(w) = 0.5 * (1 + erf(z))
	my $self = shift;

	$self->{"uppercasePhiW"} = "NA";

	if (($self->{"w"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateW();
	}

	if ($self->{"error"} eq "NA")
	{
		my ($p,$q) = cumnor($self->{"w"});

		$self->{"uppercasePhiW"} = $p;
	}
}

sub calculateLowcasePhiW
{																				# Calculate lowcasePhi(w); lowcasePhi(w) = exp(-1 * w^2 / 2) / sqrt(2 * pi)
	my $self = shift;

	$self->{"lowcasePhiW"} = "NA";

	if (($self->{"w"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateW();
	}

	if ($self->{"error"} eq "NA")
	{
		my $lowcasePhiW = $self->{"w"} * $self->{"w"};
		$lowcasePhiW = $lowcasePhiW * 0.5;
		$lowcasePhiW = -1 * $lowcasePhiW;
		$lowcasePhiW = exp($lowcasePhiW);
	  
		my $tmp = PI;
		$tmp = 2 * $tmp;
		$tmp = sqrt($tmp);
		
		$lowcasePhiW = $lowcasePhiW / $tmp;
		
		$self->{"lowcasePhiW"} = $lowcasePhiW;
	}
}

sub calculateU2
{
	my $self = shift;

	$self->{"u2"} = "NA";

	if (($self->{"kd2u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD2U();
	}

	if ($self->{"error"} eq "NA")
	{
		my $u = $self->{"u"};
		my $kd2u = $self->{"kd2u"};

		if ($kd2u < 0)
		{
			$self->{"error"} = "kd2u is less than zero!";
		}
		else
		{
			$self->{"u2"} = $u * sqrt($kd2u);
		}
	}
}

sub calculateK3
{																				#	k3 = K'''(u) *((K''(u))^(-1.5))
	my $self = shift;

	$self->{"k3"} = "NA";

	if (($self->{"kd2u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD2U();
	}

	if (($self->{"kd3u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD3U();
	}

	if ($self->{"error"} eq "NA")
	{
		my $kd2u = $self->{"kd2u"};
		my $kd3u = $self->{"kd3u"};
		
		if ($kd2u == 0)
		{
			$self->{"error"} = "kd2u is zero!";
		}
		else
		{
			my $tmp = $kd2u**(-1.5);
			my $k3 = $kd3u * $tmp;

			$self->{"k3"} = $k3;
		}
	}
}

sub calculateK4
{																				#	k4 = K''''(u) * ((K''(u))^(-2))
	my $self = shift;

	$self->{"k4"} = "NA";

	if (($self->{"kd2u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD2U();
	}

	if (($self->{"kd4u"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateKD4U();
	}

	if ($self->{"error"} eq "NA")
	{
		my $kd2u = $self->{"kd2u"};
		my $kd4u = $self->{"kd4u"};

		if ($kd2u == 0)
		{
			$self->{"error"} = "kd2u is zero!";
		}
		else
		{
			my $tmp = $kd2u**(-2);
			my $k4 = $kd4u * $tmp;

			$self->{"k4"} = $k4;
		}
	}
}

sub calculateP3
{
	my $self = shift;

	$self->{"p3"} = "NA";

	if ($self->{"error"} eq "NA")
	{
		if (($self->{"w"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
		{
			$self->calculateW();
		}

		if (($self->{"u1"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
		{
			$self->calculateU1();
		}

		if ($self->{"error"} eq "NA")
		{
			my $u = $self->{"u"};
			my $w = $self->{"w"};
			my $u1 = $self->{"u1"};

			if (($u == 0)||($w == 0)||($u1 == 0))
			{
				if ((($self->{"kd2Zero"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)||($self->{"kd3Zero"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/))&&($self->{"error"} eq "NA"))
				{
					$self->calculateKD2ZEROKD3ZERO();
				}

				if ($self->{"error"} eq "NA")
				{
					my $kd2Zero = $self->{"kd2Zero"};
					my $kd3Zero = $self->{"kd3Zero"};

					if ($kd2Zero == 0)
					{
						$self->{"error"} = "kd2Zero is zero!";
					}
					else
					{
						my $tmp1 = $kd3Zero * ($kd2Zero**(-1.5)) / 6;
						my $tmp2 = 0.5 * ($kd2Zero**(-0.5));

						my $p3 = 0.5 - ((2 * PI)**(-0.5)) * ($tmp1 - $tmp2);

						$self->{"p3"} = $p3;
					}
				}
			}
			else
			{
				if (($self->{"uppercasePhiW"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
				{
					$self->calculateUppercasePhiW();
				}

				if (($self->{"lowcasePhiW"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
				{
					$self->calculateLowcasePhiW();
				}

				if ($self->{"error"} eq "NA")
				{
					my $uppercasPhiW = $self->{"uppercasePhiW"};
					my $lowcasePhiW = $self->{"lowcasePhiW"};

					my $p3 = 1 - $uppercasPhiW - $lowcasePhiW * (1 / $w - 1 / $u1);

					if ((0 <= $p3)&&($p3 <= 1))
					{
						$self->{"p3"} = $p3;
					}
					else
					{
						$self->{"w"} = 0;
						$self->{"u1"} = 0;

						if ((($self->{"kd2Zero"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)||($self->{"kd3Zero"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/))&&($self->{"error"} eq "NA"))
						{
							$self->calculateKD2ZEROKD3ZERO();
						}

						if ($self->{"error"} eq "NA")
						{
							my $kd2Zero = $self->{"kd2Zero"};
							my $kd3Zero = $self->{"kd3Zero"};

							if ($kd2Zero == 0)
							{
								$self->{"error"} = "kd2Zero is zero!";
							}
							else
							{
								my $tmp1 = $kd3Zero * ($kd2Zero**(-1.5)) / 6;
								my $tmp2 = 0.5 * ($kd2Zero**(-0.5));

								my $p3 = 0.5 - ((2 * PI)**(-0.5)) * ($tmp1 - $tmp2);

								$self->{"p3"} = $p3;
							}
						}
					}
				}
			}
		}
	}
}

sub calculateP4
{
	my $self = shift;

	$self->{"p4"} = "NA";

	if (($self->{"p3"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateP3();
	}

	if (($self->{"w"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateW();
	}

	if (($self->{"lowcasePhiW"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateLowcasePhiW();
	}

	if (($self->{"u2"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateU2();
	}

	if (($self->{"k3"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateK3();
	}

	if (($self->{"k4"} !~ /^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)&&($self->{"error"} eq "NA"))
	{
		$self->calculateK4();
	}

	if ($self->{"error"} eq "NA")
	{
		my $p3 = $self->{"p3"};
		my $u2 = $self->{"u2"};
		my $k3 = $self->{"k3"};
		my $k4 = $self->{"k4"};
		my $w = $self->{"w"};
		my $kd2u = $self->{"kd2u"};
		my $lowcasePhiW = $self->{"lowcasePhiW"};

		if (($w == 0)||($u2 == 0))
		{
			$self->{"p4"} = $p3;
		}
		else
		{
			if ($u2 == 0)
			{
				$self->{"error"} = "u2 is zero!";
			}
			else
			{
				if ($w == 0)
				{
					$self->{"error"} = "w is zero!";
				}
				else
				{
					if ($kd2u <= 0)
					{
						$self->{"error"} = "kd2u is less than zero!";
					}
					else
					{
						my $tmp1 = ($k4 / 8 - 5 * $k3 * $k3 / 24) / $u2;
						my $tmp2 = 1 / ($u2**3);
						my $tmp3 = $k3 / (2 * $u2 * $u2);
						my $tmp4 = 1 / ($w**3);
						my $tmp5 = $tmp1 - $tmp2 - $tmp3 + $tmp4;
				
						my $p4 = $p3 - $lowcasePhiW * $tmp5;
				
						$self->{"p4"} = $p4;

						if ((0 <= $p4)&&($p4 <= 1))
						{
							$self->{"p4"} = $p4;
						}
						else
						{
							my $es = 0;
							for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
							{
								my $ni = $self->{"s"}[$i];
								my $pi = $self->{"p"}[$i];

								$es = $es + $ni * $pi;
							}

							my $bottom = $self->{"k"} - 1;
							my $top = $self->{"k"} + 1;

							if (($bottom <= $es)&&($es <= $top))
							{
								$self->{"p4"} = $self->{"p3"};
							}
							else
							{
								$self->{"w"} = 0;
								$self->{"u1"} = 0;

								$self->calculateP3();

								$self->{"p4"} = $self->{"p3"};
							}
						}
					}
				}
			}
		}
	}
}

sub calculatePValue
{
	my $self = shift;

	my $sigmaSi = 0;
	my $k = $self->{"k"};

	for (my $i = 0; $i < int(@{$self->{"s"}}); $i++)
	{
		$sigmaSi = $sigmaSi + $self->{"s"};
	}

	if ($k == 0)
	{
		my $pvalue = 1;

		$self->{"p4"} = $pvalue;
	}
	elsif ($sigmaSi == $self->{"k"})
	{
		my $pvalue = 1;

		for (my $i = 0; $i < int(@{$self->{"p"}}); $i++)
		{
			my $ni = $self->{"s"}[$i];
			my $pi = $self->{"p"}[$i];

			my $tmp = $pi**$ni;
			$pvalue = $pvalue * $tmp;
		}

		$self->{"p4"} = $pvalue;
	}
	else
	{
		$self->solveEquation();

		$self->perCalculation();

#		$self->calculateP4();
		$self->calculateP3();
	}
}

1;
