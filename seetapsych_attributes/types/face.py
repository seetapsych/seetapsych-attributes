# -*- coding: utf-8 -*-

from typing import TypedDict


__all__ = [
    'BBox',
    'FaceDetection',
    'Landmarks',
    'FaceLandmarks',
    'Selection',
    'FaceSelection',
    'ActionUnits',
    'FaceActionUnits',
    'Expression',
    'FaceExpression',
    'DenseLandmarks',
    'FaceDenseLandmarks',
    'MeshLandmarks',
    'FaceMesh',
    'GazePoint',
    'GazeData',
    'GazeScreen',
    'FaceGazeScreen',
    'HeartRate',
    'FaceHeartRate',
    'DimensionalAffect',
    'FaceDimensionalAffect',
]


class BBox(TypedDict):
    """Rectangular face detection result with confidence score."""

    # [x1, y1, x2, y2] -- pixel-coordinate bounding box
    xyxy: list[float]
    # detection confidence in [0, 1]
    score: float


# List of all detected faces (bounding boxes).
FaceDetection = list[BBox]


class Landmarks(TypedDict):
    """Basic 5-point facial landmarks used for rough alignment."""

    # 5-point interleaved [x,y]: L-eye, R-eye, nose, L-mouth, R-mouth
    landmarks: list[float]


# List of basic 5-point landmarks per detected face.
FaceLandmarks = list[Landmarks]


class Selection(TypedDict):
    """Result of face selection, referencing a single picked detection."""

    # selected face PID, auto-incremented starting from 1
    pid: int


# Alias: face-level selection output.
FaceSelection = Selection


class ActionUnits(TypedDict, total=False):
    """Facial Action Unit activations (FACS). All fields optional."""

    # [0,1] -- Inner Brow Raiser
    AU1: float
    # [0,1] -- Outer Brow Raiser
    AU2: float
    # [0,1] -- Brow Lowerer
    AU4: float
    # [0,1] -- Upper Lid Raiser
    AU5: float
    # [0,1] -- Cheek Raiser
    AU6: float
    # [0,1] -- Lid Tightener
    AU7: float
    # [0,1] -- Nose Wrinkler
    AU9: float
    # [0,1] -- Upper Lip Raiser
    AU10: float
    # [0,1] -- Lip Corner Puller
    AU12: float
    # [0,1] -- Lip Corner Depressor
    AU15: float
    # [0,1] -- Chin Raiser
    AU17: float
    # [0,1] -- Lip Stretcher
    AU20: float
    # [0,1] -- Lip Tightener
    AU23: float
    # [0,1] -- Lip Pressor
    AU24: float
    # [0,1] -- Lips Part
    AU25: float
    # [0,1] -- Jaw Drop
    AU26: float


# Per-face list of Action Unit confidence results.
FaceActionUnits = list[ActionUnits]


class Expression(TypedDict, total=False):
    """Discrete 7-class expression confidence scores. All fields optional."""

    # confidence in [0, 1]
    neutral: float
    # confidence in [0, 1]
    anger: float
    # confidence in [0, 1]
    disgust: float
    # confidence in [0, 1]
    fear: float
    # confidence in [0, 1]
    happy: float
    # confidence in [0, 1]
    sad: float
    # confidence in [0, 1]
    surprise: float


# Per-face list of discrete expression results.
FaceExpression = list[Expression]


class DenseLandmarks(TypedDict):
    """280-point dense facial landmarks for detailed alignment."""

    # 280-point interleaved [x,y], 560 floats total
    landmarks: list[float]


# Per-face list of dense landmark results.
FaceDenseLandmarks = list[DenseLandmarks]


class MeshLandmarks(TypedDict):
    """468-point 3D face mesh in normalized coordinates."""

    # 468 pts x [x,y,z] = 1404 normalized floats
    normalized_3d_landmarks: list[float]


# Per-face list of 3D mesh landmark results.
FaceMesh = list[MeshLandmarks]


class GazePoint(TypedDict):
    """Per-eye gaze point in either screen-pixel or camera-centimeter space."""

    # screen-px [x,y] or camera-cm [x,y,z]; empty list if unavailable
    left_eye: list[float]
    # same format as left_eye
    right_eye: list[float]


class GazeData(TypedDict):
    """Complete gaze estimation bundle for a single detected face."""

    # whether gaze estimation succeeded for this face
    success: bool
    # per-eye screen-space gaze coordinates in pixels
    gaze_screen_px: GazePoint
    # per-eye camera-space gaze direction vectors in centimeters
    gaze_cm: GazePoint


class GazeScreen(TypedDict):
    """Wrapper carrying one face's gaze result entry in the per-face list."""

    # per-face gaze estimation payload
    gaze: GazeData


# List of per-face gaze screen results.
FaceGazeScreen = list[GazeScreen]


class HeartRate(TypedDict, total=False):
    """Heart rate estimation in BPM.

    Fields are optional until enough video frames have been buffered.
    """

    # estimated FPS of the incoming stream
    fps: float
    # seconds until buffer is fully populated; 0.0 means HR is ready
    wait_seconds: float
    # estimated BPM; present only when estimation is ready
    hr_bpm: float


# Alias: face-level heart-rate output.
FaceHeartRate = HeartRate


class DimensionalAffect(TypedDict):
    """Continuous valence/arousal coordinates in Russell's affect space."""

    # valence axis: positive = pleasant, negative = unpleasant
    valence: float
    # arousal axis: positive = activated, negative = calm
    arousal: float


# Per-face list of continuous valence/arousal results.
FaceDimensionalAffect = list[DimensionalAffect]
