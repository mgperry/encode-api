import requests
from pprint import pprint

ENCODE_HOME = "https://www.encodeproject.org"


def encode_query(params):
    url = ENCODE_HOME + "/search/?" + "&".join(f"{x}={y}" for x, y in params.items())
    print(f"Fetching {url}...")
    r = requests.get(url)
    return r.json()


def encode_experiment(acc):
    url = f"{ENCODE_HOME}/experiment/{acc}/?format=json"
    print(f"Fetching data for /experiment/{acc}/...")
    return requests.get(url).json()


def match(subject, query):
    for k, v in query.items():
        if subject[k] != v:
            return False
    else:
        return True


experiment_spec = {
    "id": "@id",
    "accession": "accession",
    "cell_line": "biosample_ontology",
    "biosample_summary": "biosample_summary",
    "assay": "assay_term_name",
    "target": "target",
    "files": "files",
}


file_spec = {
    "id": "@id",
    "accession": "accession",
    "assembly": "assembly",
    "cell_line": "biosample_ontology",
    "experiment": "dataset",
    "assay": "assay_term_name",
    "technical_replicates": "technical_replicates",
    "biological_replicates": "biological_replicates",
    "target": "target",
    "file_format": "file_format",
    "output_type": "output_type",
    "assembly": "assembly",
    "cloud_metadata": "cloud_metadata",
}


def parse_json(d, info):
    return {k: d.get(v, "") for k, v in info.items()}


experiment = lambda d: parse_json(d, experiment_spec)
file = lambda d: parse_json(d, file_spec)


class Query:
    type = "Experiment"
    perturbed = "false"
    assembly = "GRCh38"
    status = "released"
    frame = "object"
    format = "json"
    limit = "all"

    default_params = ["type", "perturbed", "assembly", "status", "frame", "format", "limit"]

    def __init__(self, params, fetch_files=True) -> None:
        defaults = {x: getattr(self, x) for x in self.default_params}
        ps = {**defaults, **params}

        print("Querying experiments...")
        self.json = encode_query(ps)["@graph"]

        self.experiments = [experiment(x) for x in self.json]
        print(f"Found {len(self.experiments)} experiments.")

        self.files = []

        if fetch_files:
            self.fetch_files()

    def file_types(self):
        file_types = set((f["output_type"], f["file_format"]) for f in self.files)
        return [{"output_type": t[0], "file_format": t[1]} for t in file_types]

    def filter_files(self, query):
        return [f for f in self.files if match(f, query)]

    def fetch_files(self):
        for e in self.experiments:
            acc = e["accession"]
            fs = [file(f) for f in encode_experiment(acc)["files"]]
            self.files.extend(fs)


class HistoneQuery(Query):
    assay_title = "Histone+ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


class TFQuery(Query):
    assay_title = "TF+ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


class ExpressionQuery(Query):
    pass


def download(acc):
    url = f"{ENCODE_HOME}/file/{acc}/?format=json"
    print(f"Fetching {url}...")
    info = requests.get(url).json()
    return info["cloud_metadata"]["url"]


if __name__ == "__main__":

    k562_tf_query = {
        "biosample_ontology.term_name": "K562",
        "limit": 1,
    }

    q = TFQuery(k562_tf_query)
    js = q.json

    pprint(q.file_types())

    peaks = q.filter_files(
        {
            "output_type": "IDR thresholded peaks",
            "file_format": "bed",
            "biological_replicates": [1, 2],
        }
    )

    js2 = download(peaks[0]["accession"])
    pprint(js2)