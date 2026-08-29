# -*- coding: utf-8 -*-

from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class Expression(BaseModel):
    neutral: float = Field(None, description="Confidence in `[0, 1]`.")
    anger: float = Field(None, description="Confidence in `[0, 1]`.")
    disgust: float = Field(None, description="Confidence in `[0, 1]`.")
    fear: float = Field(None, description="Confidence in `[0, 1]`.")
    happy: float = Field(None, description="Confidence in `[0, 1]`.")
    sad: float = Field(None, description="Confidence in `[0, 1]`.")
    surprise: float = Field(None, description="Confidence in `[0, 1]`.")


class Report(BaseModel):
    face_expression: list[Expression]

    model_config = ConfigDict(
        title="face/expression",
        json_schema_extra={
            "description": "Indicate the confidence level of each expression.",
            "examples": [{
                "face_expression": [
                    {
                        "neutral": 0.01,
                        "anger": 0.01,
                        "disgust": 0.01,
                        "fear": 0.01,
                        "happy": 0.94,
                        "sad": 0.01,
                        "surprise": 0.01,
                    },
                ],
            }]
        }
    )
