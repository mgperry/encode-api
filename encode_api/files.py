import re
from pathlib import Path

ENCODE_ACCESSION = re.compile(r"^ENC[A-Z]{2}[0-9]{3}[A-Z]{3}")


class EncodeDataStore:
    def __init__(self, path: Path):
        self.path = path
        self.files = {}
        self.refresh()

    # check for duplicates
    def refresh(self):
        for f in self.path.iterdir():
            hit = ENCODE_ACCESSION.search(f.name)
            if hit:
                self.files[hit.group()] = f

    def find(self, accession):
        return self.files.get(accession, "")


if __name__ == "__main__":
    encode_dir = EncodeDataStore(Path.home() / "Data" / "ENCODE" / "files")

    files = [
        {
            "accession": "ENCFF804RVA",
            "cell_line": "K562",
            "file_type": "narrowPeak",
            "TF": "EP300",
            "type": "TF ChIP-seq",
            "output": "IDR Threshold Peaks",
        }
    ]

    scaffold = {
        "acession": "ENCFF503GCK",
        "file_type": "tsv",
        "output": "Consensuse DNase regions from all ENCODE experiments",
    }

    accession = files[0]["accession"]

    path = encode_dir.find(accession)

    print(f"Found {accession} at {path}")
