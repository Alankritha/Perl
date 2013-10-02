#!/usr/bin/perl -w

my $searchdir = "/home/alankritha";
my $searchword = "perl";
my $found = 0;

mysearchword($searchdir,$searchword);

sub mysearchword {
    my $searchdir = shift;
    my $searchword = shift;

    opendir DIR, $searchdir or die "cannot open dir $!";
    my @files = readdir(DIR); 
    closedir (DIR);

    foreach my $file (@files) {
       
        next if (($file eq ".") || ($file eq ".."));
        my $ret = open (fp, $file);
        if (!$ret) {
            print "Cannot open file $file\n";
            next;
        }

        foreach my $line (<fp>) {
            if ($line =~ /$searchword/ig) {
                print "$searchword is present in $searchdir/$file \n";
                $found = 1;
            }
        close fp;
        }
        if(-d "$searchdir/$file") {
            mysearchword("$searchdir/$file",$searchword);
        }
   }
   if (!$found) {
    print "cannot find word $searchword \n";                   
   }  
}

