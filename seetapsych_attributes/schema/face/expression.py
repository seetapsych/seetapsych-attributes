# -*- coding: utf-8 -*-


from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class Expression(BaseModel):
    neutral: float | None = Field(None, description="Confidence in `[0, 1]`.")
    anger: float | None = Field(None, description="Confidence in `[0, 1]`.")
    disgust: float | None = Field(None, description="Confidence in `[0, 1]`.")
    fear: float | None = Field(None, description="Confidence in `[0, 1]`.")
    happy: float | None = Field(None, description="Confidence in `[0, 1]`.")
    sad: float | None = Field(None, description="Confidence in `[0, 1]`.")
    surprise: float | None = Field(None, description="Confidence in `[0, 1]`.")


class Report(BaseModel):
    face_expression: list[Expression]

    model_config = ConfigDict(
        title="face/expression",
        json_schema_extra={
            "description": "Indicate the confidence level of each expression.",
            "examples": [
                {
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
                }
            ],
        },
    )
