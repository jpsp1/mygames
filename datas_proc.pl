while(<>)
{
    chomp;
    s{\'}{}g;
    if( /^(\d)(\d)\s+(\d)(\d)$/) {
	print "$_,$1,$2,$3,$4\n";
    } elsif( /^(\d)(\d)\s+(\d)(\d)\s+(\d+)\-(\d+)$/) {
	print "$_,$1,$2,$3,$4,$5,$6\n";
    }else{
	print "$_\n";
    }
}
