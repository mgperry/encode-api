ENCODE API Tool
===============

Intro
-----

ENCODE Data Structure
---------------------

Objects
~~~~~~~

/experiment/

/file/

/target/

/biosample/

Queries
-----

NB A lot of this should go into docstrings at some point but I haven't got around to this.

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
