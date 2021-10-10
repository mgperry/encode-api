import requests
from pprint import pprint

ENCODE_URL = "https://www.encodeproject.org/search/?"

experiment_spec = {
    "id": "@id",
    "accession": "accession",
    "cell_line": "biosample_ontology",
    "assay": "assay_term_name",
    "target": "target",
    "files": "files",
}


file_spec = {
    "id": "@id",
    "accession": "accession",
    "cell_line": "biosample_ontology",
    "experiment": "dataset",
    "assay": "assay_term_name",
    "technical_replicates": "technical_replicates",
    "biological_replicates": "biological_replicates",
    "target": "target",
    "file_format": "file_format",
    "assembly": "assembly",
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

    default_params = ["type", "perturbed", "assembly", "status", "frame", "format"]

    def __init__(self, params) -> None:
        defaults = {x: getattr(self, x) for x in self.default_params}
        ps = {**defaults, **params}
        url = ENCODE_URL + "&".join(f"{str(x)}={str(y)}" for x, y in ps.items())

        print("Querying experiments...")
        r = requests.get(url)

        self.json = r.json()["@graph"]
        self.experiments = [experiment(x) for x in self.json]
        print(f"Found {len(self.experiments)} experiments.")


class HistoneQuery(Query):
    assay_title = "Histone+ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


class TFQuery(Query):
    assay_title = "TF+ChIP-seq"
    default_params = Query.default_params + ["assay_title"]


class ExpressionQuery(Query):
    pass


if __name__ == "__main__":

    k562_tf_query = {
        "type": "Experiment",
        "biosample_ontology.term_name": "K562",
        "limit": 5,
    }

    q = TFQuery(k562_tf_query)
    js = q.json

    pprint(q.experiments)
