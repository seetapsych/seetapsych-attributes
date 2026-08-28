# -*- coding: utf-8 -*-


from pydantic import BaseModel

from . import face
from . import head

schema: dict[str, type[BaseModel]] = {
    'face/detection': face.detection.Report,
    'face/landmarks': face.landmarks.Report,
    'face/selection': face.selection.Report,
    'face/action_units': face.action_units.Report,
    'face/expression': face.expression.Report,
    'face/dense_landmarks': face.dense_landmarks.Report,
    'face/mesh': face.mesh.Report,
    'face/gaze_screen': face.gaze_screen.Report,
    'face/heart_rate': face.heart_rate.Report,
    'face/dimensional_affect': face.dimensional_affect.Report,
    'head/detection': head.detection.Report,
    'head/selection': head.selection.Report,
    'head/gaze_point': head.gaze_point.Report,
    'head/social_gaze': head.social_gaze.Report,
}
