import requests
from .utils import select, match
from pprint import pprint

ENCODE_HOME = "https://www.encodeproject.org"


def escape(x):
    return str(x).replace(" ", "+")


def encode_query(params):
    url = (
        ENCODE_HOME
        + "/search/?format=json&"
        + "&".join(f"{x}={escape(y)}" for x, y in params.items())
    )
    print(f"Fetching {url}...")
    r = requests.get(url)
    return r.json()["@graph"]


# TODO refactor this into a generic encode object getter, and add type
def encode_experiment(acc):
    url = f"{ENCODE_HOME}/experiment/{acc}/?format=json"
    print(f"Fetching data for /experiment/{acc}/...")
    return requests.get(url).json()


# TODO get rid of the specs, they are probably causing more harm than good.
experiment_spec = [
    "@id",
    "accession",
    "biosample_ontology",
    "biosample_summary",
    "assay_term_name",
    "target",
    "files",
]


file_spec = [
    "@id",
    "accession",
    "assembly",
    "biosample_ontology",
    "dataset",
    "assay_term_name",
    "technical_replicates",
    "biological_replicates",
    "target",
    "file_format",
    "output_type",
    "assembly",
    "cloud_metadata",
]


experiment = lambda d: select(d, experiment_spec)
file = lambda d: select(d, file_spec)


class Query:
    type = "Experiment"
    perturbed = "false"
    assembly = "GRCh38"
    status = "released"
    frame = "object"
    limit = "all"

    default_params = ["type", "perturbed", "assembly", "status", "frame", "limit"]

    def __init__(self, params) -> None:
        defaults = {x: getattr(self, x) for x in self.default_params}
        self.params = {**defaults, **params}

        print("Querying experiments...")
        self.experiments = encode_query(self.params)
        print(f"Found {len(self.experiments)} experiments.")

    def file_types(self):
        if not self.files:
            self.fetch_files()

        file_types = set((f["output_type"], f["file_format"]) for f in self.files)
        return [{"output_type": t[0], "file_format": t[1]} for t in file_types]

    # local filtering of files
    def filter_files(self, query):
        return [f for f in self.files if match(f, query)]

    def fetch_files(self, params=None, replicated=False):
        self.files = []

        if params is None:
            params = {}

        for e in self.experiments:
            fs = encode_query(
                {"type": "File", "frame": "object", "dataset": e["@id"], **params}
            )

            if replicated:
                fs = [f for f in fs if len(f["biological_replicates"]) > 1]

            self.files.extend(fs)


class HistoneQuery(Query):
    assay_title = "Histone ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


class TFQuery(Query):
    assay_title = "TF ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


# TODO
class ExpressionQuery(Query):
    pass


# TODO replace this with a better example, also tests
if __name__ == "__main__":

    q = TFQuery(
        {
            "biosample_ontology.term_name": "K562",
            "limit": 5,
        }
    )

    q.fetch_files(
        {
            "assembly": "GRCh38",
            "output_type": "IDR thresholded peaks",
            "file_format": "bed",
        },
        replicated=True,
    )

    pprint(q.files)
