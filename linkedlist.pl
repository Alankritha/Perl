#!/usr/bin/perl -w

my $hash = {};

$hash->{'data'} = 10;


if (!defined ($hash->{'anext'})) {
    print "raghu\n";

}

my $root = $hash;
my $tail = $hash;

$hash = {};
$hash->{'data'} = 30;
$tail->{'next'} = $hash;
$tail = $hash;

$hash = {};
$hash->{'data'} = 20;
$tail->{'next'} = $hash;
$tail = $hash;

$hash = {};
$hash->{'data'} = 15;
$tail->{'next'} = $hash;
$tail = $hash;

$hash = {};
$hash->{'data'} = 70;
$tail->{'next'} = $hash;
$tail = $hash;


$hash = $root;
while (defined ($hash)) {

    print $hash->{'data'}."\n";

    $hash = $hash->{'next'};

}
