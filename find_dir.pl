#!/usr/bin/perl -w

my $searchdir = "/home/alankritha";
my $filename = "alan.txt";
my $found = 0;

searchfile ($searchdir, $filename);

sub searchfile {

    my $searchdir = shift;
    my $searchfile = shift;

    print "searching dir $searchdir \n";

    #open close dir
    opendir DIR,$searchdir or die "cannot open dir $!";
    my @files = readdir(DIR);
    closedir (DIR);

    foreach my $filename (@files) {

        # ignore filenames starting with "." ".." etc
        next if ($filename =~ /^\./);
 
        if ($filename eq $searchfile) {
            print "found $searchfile in $searchdir location \n";
            $found = 1;
        }
        if (-d "$searchdir/$filename") {
           # call recursive function module for all dir names
           searchfile ("$searchdir/$filename", $searchfile);
        }
    }
    if(!$found) {
         print "no $filename found \n";
    }
}
