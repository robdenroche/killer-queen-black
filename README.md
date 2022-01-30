# Crankt's killer-queen-black repo

A collection of scripts used to collect, visualize and upload awards for Killer Queen Black's Bee Game League.

## beeder-board.py

beeder-board.py works off a query to the matches url of the BGL API.  It collects all the associated results and then parses out individual stat categories.  Two html pages are generated for the standard and experimental award categories that include the winner and 5 runner ups.

TODO:
 * The code must be modified to specify the matches url and output file name (when selecting season and circuit, for example)... would be better to have CLI options for these.

## bee-matrix.py

This script reuses much of the code from beeder-board.py, but outputs the stats for every player into `queenMatrix.tsv` and `workerMatrix.tsv` files.  These can be pasted into a google sheets document to share with the community (e.g. https://docs.google.com/spreadsheets/d/1TvXi5rWieVSOVy4g45QfVA_ckeXMXBzY26c48aOsH94)

## bee-awarder.py

bee-awarder.py takes a csv of awards and POSTs them to the BGL API.  IMPORTANT: the code does not check if an award has already been uploaded, so care must be taken to not duplicate awards.

TODO:
 * Removed auth token from the script, but haven't added code to read it from a file yet.
 * beeder-board.py could be updated to produce an awards csv so that weekly awards could be uploaded.

## scout-bee.py

Similary to beeder-board.py, this script works off a matches url.  It collects team and individual stats into an html summary.