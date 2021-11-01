ENCODE API Tool
===============

All of the ENCODE data is hosted on www.encodeproject.org, and it has a
graphical search function which is pretty good. The paramaters from user queries
are also visible in the URL, which makes it easy to see how to do common searches.
Passing `?format=json` to the query returns json instead of the web page, and the
results of the search (ie. the individual Experiments or Files) are returned in
the '@graph' field.

ENCODE Data Structure
---------------------

From the way the results are returned, it looks like their database is a document store,
with multiple different types of document. I think for us the most important are
Experiments, Files and Biosamples (i.e. cell lines), and Targets (relevant for ChIP-seq
data, usually a transcription factor, or histone modification, targetted by an
antibody). Each document has an "accession" field (e.g. "ENCFF005MCX"), and an "@id"
field, which includes the type (e.g. "/file/ENCFF005MCX/") along with some forward
slashes. There is also a lot of information about the grant awards, PIs, labs and
publications which we're not interested in.

You can access information for a particular File, Experiment, Target etc. by going to
"www.encodeproject.com/{type}/{accession}", e.g. "www.encodeproject/file/ENCFF005MCX".
This can also be used to retrieve the JSON document corresponding to a particular 
entity.

It's easiest to navigate the data by Experiment, since this contains the most
information about our experiments. The "assay.type" field is very important, along with
the biosample (searchable using several different identifiers, confusingly), and the
target (for ChIP-seq) experiments.

Once we have a list of experiments, we can then use the experiment's "@id" field to
search for file belonging to that experiment, and additionally we can narrow down the
selection of files by file type, replicate information, output and (importantly!) genome
assembly. The way the file_search function is currently written, this uses the server's
query engine. An alternative approcah is to fetch the experiment by `@id`, and then
fetch the files individually using the accessions in `experiment["files"]` but this is
slow as it runs a separate query for each. Unfortunately, certain queries aren't
possible so you still have to filter the returned File objects in python.

NB There is a very nice graphical display of how files are generated within each
experiment, visible on the experiment's page.

Queries
-----

NB A lot of this should go into docstrings at some point but I haven't got around to
this.

Common Properties
-----------------

Just dump everything here from my scripts

File Storage
------------

This part probably isn't relevant to Regulation as a whole, it's designed for
data analysis projects. The idea is essentially to list only metadata within
projects (principally the ENCODE accession but anything else relevant, from the
DB or added manually), so that the files used by the project can be logged in
version control. The class `EncodeDataStore` would then be used either to retrieve
the files from a local cache, or download them. This also allows files to be
reused (locally) between projects, analagous to the Object Store we run in EHK.
