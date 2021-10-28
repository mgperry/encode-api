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


def select_keys(d, info):
    return {k: d.get(k, "") for k in info}

experiment = lambda d: select_keys(d, experiment_spec)
file = lambda d: select_keys(d, file_spec)


ENSG = re.compile(r"ENSEMBL:(ENSG[0-9]+)")


def get_target_info(x):
    if len(x["genes"]) > 1:
        raise Exception("Each ChIP-seq experiment should target 1 TF.")

    for g in x["genes"][0]["dbxrefs"]:
        if ENSG.match(g):
            ensg = ENSG.match(g).groups()[0]
            break
    else:
        ensg = ""

    return {"type": "target", "id": x["@id"], "label": x["label"], "ENSG": ensg}

