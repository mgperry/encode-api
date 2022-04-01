import polars as pl
from functools import partial

filetypes = {
    "bed": {
        "header": False,
        "columns": {
            "chr": str,
            "start": int,
            "end": int,
            "name": str,
            "score": float,
            "strand": str,
        }
    },

    "narrowPeak": {
        "header": False,
        "columns": {
            "chr": str,
            "start": int,
            "end": int,
            "name": str,
            "score": float,
            "strand": str,
            "signalValue": float,
            "pValue": float,
            "qValue": float,
            "peak": int,
        }
    },

    "scaffold": {
        "header": True,
        "columns": {
            "seqname": str,
            "start": int,
            "end": int,
            "identifier": str,
            "mean_signal": float,
            "numsamples": int,
            "summit": int,
            "core_start": int,
            "core_end": int,
            "component": str,
        }
    },
}

# can also check that column names are correct rather than erasing
def autoload(format, f):
    return pl.read_csv(
        f,
        has_header=format["header"],
        new_columns = list(format["columns"].keys()),
        dtypes = format["columns"]
    )

read_bed = partial(autoload, filetypes["bed"])
read_narrowPeak = partial(autoload, filetypes["narrowPeak"])
read_scaffold = partial(autoload, filetypes["scaffold"])
