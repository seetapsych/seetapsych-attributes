# SeetaPsych Attributes

> Attribute Contracts for Behavior-based Psychological Measurement

SeetaPsych Attributes is the contract layer of the SeetaPsych ecosystem. It defines and maintains the
specifications for every attribute output — an attribute representing the result of an algorithm or
processing step — so that all algorithm modules across the project produce interchangeable, reusable,
and type-consistent payloads. The shared contracts are referenced by the core runtime
[SeetaPsych Lib](https://github.com/seetapsych/seetapsych-lib) and registered in the global module
registry at [SeetaPsych Configs](https://github.com/seetapsych/seetapsych-configs).

## TypedDict Type Hints

Alongside the JSON schemas documented below, this project ships a set of ready-to-use
`TypedDict` declarations under `seetapsych_attributes.types` so that your IDE can
provide auto-completions and static type checks directly on the runner's `report` dict:

```python
# -*- coding: utf-8 -*-
import json

import cv2

from seetapsych_lib.runtime.factory import Factory
from seetapsych_lib.runtime.pipeline import Pipeline
from seetapsych_lib.runtime.runner import Runner

from seetapsych_attributes.types import Report, BBox, FaceDetection


def main():
    factory = Factory()
    factory.load_builtin_modules()

    pipeline = Pipeline(factory, attributes=["face/detection"])
    pipeline.solve()
    pipeline.install_requirements()
    pipeline.cache_models()

    runner = Runner(pipeline)

    report: Report = runner.run(data={"default": cv2.imread("data/a.jpg")})

    # IDE autocompletion + type inference for every attribute key:
    detections: FaceDetection | None = report.get("face_detection")
    if detections:
        first: BBox = detections[0]
        x1, y1, x2, y2 = first["xyxy"]
        score: float = first["score"]
        print(f"face at ({x1},{y1})-({x2},{y2}), score = {score:.3f}")

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

The top-level `Report` TypedDict includes every attribute key defined in the
catalog (all fields are optional, because a pipeline may only request a subset).
Per-attribute element types such as `BBox`, `Landmarks`, `Selection`,
`ActionUnits`, `Expression`, `HeartRate`, `HeadSocialGaze`, etc. are also
exported individually.

{{CATALOG}}

{{ARTICLES}}
