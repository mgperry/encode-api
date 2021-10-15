#%%
import json
from encode_api.query import *
import pandas as pd

all_tfs = TFQuery({"limit": "all"}, fetch_files=False)

print(f"{len(all_tfs.experiments)} TF experiments found.")

tf_chip = pd.DataFrame(all_tfs.experiments)

#%%
cell_lines = tf_chip.groupby("cell_line") \
    .apply(lambda x: len(x["target"].unique())) \
    .sort_values(ascending=False)[0:10]


#%% 20 factors with coverage in all of the top 10 cell lines
targets = tf_chip[tf_chip["cell_line"].isin(cell_lines.index)] \
    .groupby("target").size() \
    .sort_values(ascending=False)[0:10]


# %%
experiments = tf_chip[tf_chip["cell_line"].isin(cell_lines.index) & \
        tf_chip["target"].isin(targets.index)]

experiments.to_csv("pilot_experiments.csv", index=False)

#%%
peak_files = []

IDR_PEAKS = {
    "output_type": "IDR thresholded peaks",
    "file_format": "bed",
    "biological_replicates": [1, 2],
}

def filter_dict(q, s):
    return list(filter(lambda f: match(f, s), q))

for e in experiments["accession"].to_list():
    fs = [file(f) for f in encode_experiment(e)["files"]]
    # print(q.files)
    # break

    peaks = filter_dict(fs, IDR_PEAKS)

    peak_files.extend(peaks)

for f in peak_files:
    f["url"] = f["cloud_metadata"]["url"]
    del f["cloud_metadata"]

with open("pilot_files.json", 'w') as fh:
    json.dump(peak_files, fh, indent=4)

# %%
