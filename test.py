import json
from pathlib import Path
from nemo_library.model.metric import Metric

path = Path(".") / "metadata_conservative" / "metrics.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

metrics = []
for element in data:
    metrics.append(Metric(**element))  
    
with open(path, "w", encoding="utf-8") as file:
    json.dump(
        [metric.to_dict() for metric in metrics], file, indent=4, ensure_ascii=True
    )

