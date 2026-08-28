# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class DimensionalAffect(BaseModel):
    valence: float = Field(..., description="Valence dimension in continuous affect space. Positive = pleasant, negative = unpleasant.")
    arousal: float = Field(..., description="Arousal dimension in continuous affect space. Positive = activated, negative = calm.")


class Report(BaseModel):
    face_dimensional_affect: list[DimensionalAffect]

    model_config = ConfigDict(
        title="face/dimensional_affect",
        json_schema_extra={
            "x-brief": "Continuous valence-arousal affect dimensions alongside discrete expressions and Action Units.",
            "examples": [{
                "face_dimensional_affect": [
                    {
                        "valence": 0.85,
                        "arousal": 0.32,
                    }
                ]
            }]
        }
    )
