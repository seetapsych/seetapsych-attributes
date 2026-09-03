# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict

__all__ = [
    "Report",
]


class Report(BaseModel):
    face_feature: list[list[float]]

    model_config = ConfigDict(
        title="face/feature",
        json_schema_extra={
            "description": (
                "Per-face L2-normalized feature embeddings for recognition, "
                "clustering, or similarity search. Each inner list corresponds to one "
                "aligned face in face/landmarks order; vector dimension is "
                "algorithm-specific (typically 512 for ArcFace)."
            ),
            "examples": [
                {
                    "face_feature": [
                        [0.0412, -0.0187, 0.0934, 0.0052, -0.0621],
                        [-0.0298, 0.0745, 0.0102, -0.0881, 0.0356],
                    ]
                }
            ],
        },
    )
