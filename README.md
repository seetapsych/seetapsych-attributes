# SeetaPsych Attributes

> Face and body based psychology analysis

SeetaPsych Lib is a Python library for face- and body-based psychology analysis.
It provides a modular Pipeline/Runner runtime and an optional Streamlit WebUI.

This project is used to manage the specifications for various attribute outputs,
providing a unified standard so that different algorithm implementations can produce interchangeable and reusable module outputs.

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

## Catalog

- [face/detection](#facedetection) Face detection results as rectangular bounding boxes.
- [face/landmarks](#facelandmarks) Facial landmarks for basic alignment: L-eye, R-eye, nose, L-mouth, R-mouth (10 interleaved floats).
- [face/selection](#faceselection) Selected face PID. Selected face order is reflected in face/detection and face/landmarks.
- [face/action_units](#faceaction_units) Indicate the confidence level of each Action Unit. Not all Action Units' results may be output.
- [face/expression](#faceexpression) Indicate the confidence level of each expression.
- [face/dense_landmarks](#facedense_landmarks) 280-point dense facial landmarks (560 interleaved [x,y] floats).
- [face/mesh](#facemesh) 468-point 3D face mesh landmarks in normalized coordinates.
- [face/gaze_screen](#facegaze_screen) Per-eye screen-space point-of-gaze coordinates in pixels and camera-space point-of-gaze coordinates in millimeters. Camera-space coordinates may be 2D or 3D depending on the algorithm; origin is at the camera center.
- [face/heart_rate](#faceheart_rate) Heart rate (BPM) estimated from buffered face video frames.
- [face/dimensional_affect](#facedimensional_affect) Continuous valence-arousal affect dimensions alongside discrete expressions and Action Units.
- [head/detection](#headdetection) Multi-person head bounding box detection results.
- [head/selection](#headselection) Top-N head selection result (count + original indices), reordering head_detection.
- [head/gaze_point](#headgaze_point) Per-head 2D scene gaze target point with associated likelihood heatmap.
- [head/social_gaze](#headsocial_gaze) Dyadic social gaze relations between two detected people. Class set: share, mutual, single, miss, void.

<a id="facedetection"></a>

## face/detection

*Face detection results as rectangular bounding boxes.*

### Properties

- <a id="properties/face_detection"></a>**`face_detection`** *(array, required)*
  - <a id="properties/face_detection/items"></a>**Items**: Refer to *[BBox](#defs-BBox)*.

### Definitions

- <a id="defs-BBox"></a>**`BBox`** *(object)*
  - <a id="%24defs/BBox/properties/xyxy"></a>**`xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/BBox/properties/xyxy/items"></a>**Items** *(number)*
  - <a id="%24defs/BBox/properties/score"></a>**`score`** *(number, required)*

### Examples

  ```json
  {
      "face_detection": [
          {
              "score": 0.5,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ]
  }
  ```



<a id="facelandmarks"></a>

## face/landmarks

*Facial landmarks for basic alignment: L-eye, R-eye, nose, L-mouth, R-mouth (10 interleaved floats).*

### Properties

- <a id="properties/face_landmarks"></a>**`face_landmarks`** *(array, required)*
  - <a id="properties/face_landmarks/items"></a>**Items**: Refer to *[Landmarks](#defs-Landmarks)*.

### Definitions

- <a id="defs-Landmarks"></a>**`Landmarks`** *(object)*
  - <a id="%24defs/Landmarks/properties/landmarks"></a>**`landmarks`** *(array, required)*: Length must be equal to 10.
    - <a id="%24defs/Landmarks/properties/landmarks/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "face_landmarks": [
          {
              "landmarks": [
                  100,
                  100,
                  200,
                  200,
                  300,
                  300,
                  400,
                  400,
                  500,
                  500
              ]
          }
      ]
  }
  ```



<a id="faceselection"></a>

## face/selection

*Selected face PID. Selected face order is reflected in face/detection and face/landmarks.*

### Properties

- <a id="properties/face_selection"></a>**`face_selection`** *(required)*: Refer to *[Selection](#defs-Selection)*.

### Definitions

- <a id="defs-Selection"></a>**`Selection`** *(object)*
  - <a id="%24defs/Selection/properties/pid"></a>**`pid`** *(integer, required)*: PID of selected face detection (1-based).

### Examples

  ```json
  {
      "face_detection": [
          {
              "score": 0.5,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ],
      "face_selection": {
          "pid": 1
      }
  }
  ```



<a id="faceaction_units"></a>

## face/action_units

*Indicate the confidence level of each Action Unit. Not all Action Units' results may be output.*

### Properties

- <a id="properties/face_action_units"></a>**`face_action_units`** *(array, required)*
  - <a id="properties/face_action_units/items"></a>**Items**: Refer to *[ActionUnits](#defs-ActionUnits)*.

### Definitions

- <a id="defs-ActionUnits"></a>**`ActionUnits`** *(object)*
  - <a id="%24defs/ActionUnits/properties/AU1"></a>**`AU1`**: `[0, 1]`. Inner Brow Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU1/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU1/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU2"></a>**`AU2`**: `[0, 1]`. Outer Brow Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU2/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU2/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU4"></a>**`AU4`**: `[0, 1]`. Brow Lowerer. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU4/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU4/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU5"></a>**`AU5`**: `[0, 1]`. Upper Lid Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU5/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU5/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU6"></a>**`AU6`**: `[0, 1]`. Cheek Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU6/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU6/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU7"></a>**`AU7`**: `[0, 1]`. Lid Tightener. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU7/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU7/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU9"></a>**`AU9`**: `[0, 1]`. Nose Wrinkler. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU9/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU9/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU10"></a>**`AU10`**: `[0, 1]`. Upper Lip Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU10/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU10/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU12"></a>**`AU12`**: `[0, 1]`. Lip Corner Puller. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU12/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU12/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU15"></a>**`AU15`**: `[0, 1]`. Lip Corner Depressor. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU15/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU15/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU17"></a>**`AU17`**: `[0, 1]`. Chin Raiser. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU17/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU17/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU20"></a>**`AU20`**: `[0, 1]`. Lip Stretcher. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU20/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU20/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU23"></a>**`AU23`**: `[0, 1]`. Lip Tightener. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU23/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU23/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU24"></a>**`AU24`**: `[0, 1]`. Lip Pressor. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU24/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU24/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU25"></a>**`AU25`**: `[0, 1]`. Lips Part. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU25/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU25/anyOf/1"></a>*null*
  - <a id="%24defs/ActionUnits/properties/AU26"></a>**`AU26`**: `[0, 1]`. Jaw Drop. Default: `null`.
    - **Any of**
      - <a id="%24defs/ActionUnits/properties/AU26/anyOf/0"></a>*number*
      - <a id="%24defs/ActionUnits/properties/AU26/anyOf/1"></a>*null*

### Examples

  ```json
  {
      "face_action_units": [
          {
              "AU1": 0.5,
              "AU10": 0.5,
              "AU12": 0.5,
              "AU15": 0.5,
              "AU17": 0.5,
              "AU2": 0.5,
              "AU20": 0.5,
              "AU23": 0.5,
              "AU24": 0.5,
              "AU25": 0.5,
              "AU26": 0.5,
              "AU4": 0.5,
              "AU5": 0.5,
              "AU6": 0.5,
              "AU7": 0.5,
              "AU9": 0.5
          }
      ]
  }
  ```



<a id="faceexpression"></a>

## face/expression

*Indicate the confidence level of each expression.*

### Properties

- <a id="properties/face_expression"></a>**`face_expression`** *(array, required)*
  - <a id="properties/face_expression/items"></a>**Items**: Refer to *[Expression](#defs-Expression)*.

### Definitions

- <a id="defs-Expression"></a>**`Expression`** *(object)*
  - <a id="%24defs/Expression/properties/neutral"></a>**`neutral`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/neutral/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/neutral/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/anger"></a>**`anger`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/anger/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/anger/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/disgust"></a>**`disgust`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/disgust/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/disgust/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/fear"></a>**`fear`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/fear/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/fear/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/happy"></a>**`happy`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/happy/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/happy/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/sad"></a>**`sad`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/sad/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/sad/anyOf/1"></a>*null*
  - <a id="%24defs/Expression/properties/surprise"></a>**`surprise`**: Confidence in `[0, 1]`. Default: `null`.
    - **Any of**
      - <a id="%24defs/Expression/properties/surprise/anyOf/0"></a>*number*
      - <a id="%24defs/Expression/properties/surprise/anyOf/1"></a>*null*

### Examples

  ```json
  {
      "face_expression": [
          {
              "anger": 0.01,
              "disgust": 0.01,
              "fear": 0.01,
              "happy": 0.94,
              "neutral": 0.01,
              "sad": 0.01,
              "surprise": 0.01
          }
      ]
  }
  ```



<a id="facedense_landmarks"></a>

## face/dense_landmarks

*280-point dense facial landmarks (560 interleaved [x,y] floats).*

### Properties

- <a id="properties/face_dense_landmarks"></a>**`face_dense_landmarks`** *(array, required)*
  - <a id="properties/face_dense_landmarks/items"></a>**Items**: Refer to *[DenseLandmarks](#defs-DenseLandmarks)*.

### Definitions

- <a id="defs-DenseLandmarks"></a>**`DenseLandmarks`** *(object)*
  - <a id="%24defs/DenseLandmarks/properties/landmarks"></a>**`landmarks`** *(array, required)*: Length must be equal to 560.
    - <a id="%24defs/DenseLandmarks/properties/landmarks/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "face_dense_landmarks": [
          {
              "landmarks": "[100.0] * 560"
          }
      ]
  }
  ```



<a id="facemesh"></a>

## face/mesh

*468-point 3D face mesh landmarks in normalized coordinates.*

### Properties

- <a id="properties/face_mesh"></a>**`face_mesh`** *(array, required)*
  - <a id="properties/face_mesh/items"></a>**Items**: Refer to *[MeshLandmarks](#defs-MeshLandmarks)*.

### Definitions

- <a id="defs-MeshLandmarks"></a>**`MeshLandmarks`** *(object)*
  - <a id="%24defs/MeshLandmarks/properties/normalized_3d_landmarks"></a>**`normalized_3d_landmarks`** *(array, required)*: Length must be equal to 1404.
    - <a id="%24defs/MeshLandmarks/properties/normalized_3d_landmarks/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "face_mesh": [
          {
              "normalized_3d_landmarks": "[0.5] * 1404"
          }
      ]
  }
  ```



<a id="facegaze_screen"></a>

## face/gaze_screen

*Per-eye screen-space point-of-gaze coordinates in pixels and camera-space point-of-gaze coordinates in millimeters. Camera-space coordinates may be 2D or 3D depending on the algorithm; origin is at the camera center.*

### Properties

- <a id="properties/face_gaze_screen"></a>**`face_gaze_screen`** *(array, required)*
  - <a id="properties/face_gaze_screen/items"></a>**Items**: Refer to *[GazeScreen](#defs-GazeScreen)*.

### Definitions

- <a id="defs-GazeData"></a>**`GazeData`** *(object)*: Gaze estimation result for a single face.
  - <a id="%24defs/GazeData/properties/success"></a>**`success`** *(boolean, required)*: Whether gaze estimation succeeded for this face.
  - <a id="%24defs/GazeData/properties/gaze_screen_px"></a>**`gaze_screen_px`** *(required)*: Per-eye point-of-gaze coordinates in screen-space pixels. The origin is at the left top corner of the screen. The coordinate system is shown as [Fig. 1](#facegaze_screen-figure-1). Refer to *[GazePoint](#defs-GazePoint)*.
  - <a id="%24defs/GazeData/properties/gaze_camera_mm"></a>**`gaze_camera_mm`** *(required)*: Per-eye point-of-gaze coordinates in the camera coordinate system, measured in millimeters. The coordinate origin is located at the camera optical center. Depending on the gaze estimation algorithm, the point-of-gaze can be represented either as a 2D coordinate on the camera image plane or as a 3D point in camera space. The coordinate definitions for 2D and 3D gaze_camera_mm are illustrated in [Fig. 2](#facegaze_screen-figure-2) and [Fig. 3](#facegaze_screen-figure-3), respectively. Different algorithms may natively output in different coordinate frames; all values are normalized to the conventions documented here before being returned. Refer to *[GazePoint](#defs-GazePoint)*.
- <a id="defs-GazePoint"></a>**`GazePoint`** *(object)*: Point-of-gaze coordinates for two eyes in either screen-pixel or camera-millimeter space.
  - <a id="%24defs/GazePoint/properties/left_eye"></a>**`left_eye`** *(array, required)*: Gaze-screen-px [x,y] or gaze-camera-mm [x,y(,z)]; 2D or 3D depending on algorithm; empty list if unavailable. Length must be between 0 and 3 (inclusive).
    - <a id="%24defs/GazePoint/properties/left_eye/items"></a>**Items** *(number)*
  - <a id="%24defs/GazePoint/properties/right_eye"></a>**`right_eye`** *(array, required)*: Screen-px [x,y] or camera-mm [x,y(,z)]; 2D or 3D depending on algorithm; empty list if unavailable. Length must be between 0 and 3 (inclusive).
    - <a id="%24defs/GazePoint/properties/right_eye/items"></a>**Items** *(number)*
- <a id="defs-GazeScreen"></a>**`GazeScreen`** *(object)*: Wrapper for per-face gaze data in face/gaze_screen schema.
  - <a id="%24defs/GazeScreen/properties/gaze"></a>**`gaze`** *(required)*: Refer to *[GazeData](#defs-GazeData)*.

<figure id="facegaze_screen-figure-1" style="text-align: center; margin: 1em 0;">
  <a id="facegaze_screen-figure-1"></a>
  <img src="https://raw.githubusercontent.com/seetapsych/seetapsych-attributes/main/assets/gaze_screen_px.png" alt="Coordinate system for gaze_screen_px" width="200px" />
  <figcaption style="margin-top: 0.5em; font-size: 0.9em; color: #555;">Figure 1. Coordinate system for <strong>gaze_screen_px</strong></figcaption>
</figure>

<figure id="facegaze_screen-figure-2" style="text-align: center; margin: 1em 0;">
  <a id="facegaze_screen-figure-2"></a>
  <img src="https://raw.githubusercontent.com/seetapsych/seetapsych-attributes/main/assets/gaze_camera_mm_2d.png" alt="Coordinate system for gaze_camera_mm(2D)" width="200px" />
  <figcaption style="margin-top: 0.5em; font-size: 0.9em; color: #555;">Figure 2. Coordinate system for <strong>gaze_camera_mm(2D)</strong></figcaption>
</figure>

<figure id="facegaze_screen-figure-3" style="text-align: center; margin: 1em 0;">
  <a id="facegaze_screen-figure-3"></a>
  <img src="https://raw.githubusercontent.com/seetapsych/seetapsych-attributes/main/assets/gaze_camera_mm_3d.png" alt="Coordinate system for gaze_camera_mm(3D)" width="200px" />
  <figcaption style="margin-top: 0.5em; font-size: 0.9em; color: #555;">Figure 3. Coordinate system for <strong>gaze_camera_mm(3D)</strong></figcaption>
</figure>

### Examples

  ```json
  {
      "face_gaze_screen": [
          {
              "gaze": {
                  "gaze_camera_mm": {
                      "left_eye": [
                          155.0,
                          50.0,
                          25.0
                      ],
                      "right_eye": [
                          155.0,
                          50.0,
                          25.0
                      ]
                  },
                  "gaze_screen_px": {
                      "left_eye": [
                          960.0,
                          540.0
                      ],
                      "right_eye": [
                          960.0,
                          540.0
                      ]
                  },
                  "success": true
              }
          }
      ]
  }
  ```



<a id="faceheart_rate"></a>

## face/heart_rate

*Heart rate (BPM) estimated from buffered face video frames.*

### Properties

- <a id="properties/face_heart_rate"></a>**`face_heart_rate`** *(required)*: Refer to *[HeartRate](#defs-HeartRate)*.

### Definitions

- <a id="defs-HeartRate"></a>**`HeartRate`** *(object)*
  - <a id="%24defs/HeartRate/properties/fps"></a>**`fps`** *(number, required)*: Current estimated frames per second.
  - <a id="%24defs/HeartRate/properties/wait_seconds"></a>**`wait_seconds`** *(number, required)*: Seconds remaining until enough data is buffered. 0.0 when HR is ready.
  - <a id="%24defs/HeartRate/properties/hr_bpm"></a>**`hr_bpm`**: Estimated heart rate in beats per minute. Present only when ready. Default: `null`.
    - **Any of**
      - <a id="%24defs/HeartRate/properties/hr_bpm/anyOf/0"></a>*number*
      - <a id="%24defs/HeartRate/properties/hr_bpm/anyOf/1"></a>*null*

### Examples

  ```json
  {
      "face_heart_rate": {
          "fps": 30.0,
          "hr_bpm": 72.5,
          "wait_seconds": 0.0
      }
  }
  ```

  ```json
  {
      "face_heart_rate": {
          "fps": 30.0,
          "wait_seconds": 5.2
      }
  }
  ```



<a id="facedimensional_affect"></a>

## face/dimensional_affect

*Continuous valence-arousal affect dimensions alongside discrete expressions and Action Units.*

### Properties

- <a id="properties/face_dimensional_affect"></a>**`face_dimensional_affect`** *(array, required)*
  - <a id="properties/face_dimensional_affect/items"></a>**Items**: Refer to *[DimensionalAffect](#defs-DimensionalAffect)*.

### Definitions

- <a id="defs-DimensionalAffect"></a>**`DimensionalAffect`** *(object)*
  - <a id="%24defs/DimensionalAffect/properties/valence"></a>**`valence`** *(number, required)*: Valence dimension in continuous affect space. Positive = pleasant, negative = unpleasant.
  - <a id="%24defs/DimensionalAffect/properties/arousal"></a>**`arousal`** *(number, required)*: Arousal dimension in continuous affect space. Positive = activated, negative = calm.

### Examples

  ```json
  {
      "face_dimensional_affect": [
          {
              "arousal": 0.32,
              "valence": 0.85
          }
      ]
  }
  ```



<a id="headdetection"></a>

## head/detection

*Multi-person head bounding box detection results.*

### Properties

- <a id="properties/head_detection"></a>**`head_detection`** *(array, required)*
  - <a id="properties/head_detection/items"></a>**Items**: Refer to *[HeadBBox](#defs-HeadBBox)*.

### Definitions

- <a id="defs-HeadBBox"></a>**`HeadBBox`** *(object)*
  - <a id="%24defs/HeadBBox/properties/xyxy"></a>**`xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/HeadBBox/properties/xyxy/items"></a>**Items** *(integer)*
  - <a id="%24defs/HeadBBox/properties/score"></a>**`score`** *(number, required)*

### Examples

  ```json
  {
      "head_detection": [
          {
              "score": 0.85,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ]
  }
  ```



<a id="headselection"></a>

## head/selection

*Top-N head selection result (count + original indices), reordering head_detection.*

### Properties

- <a id="properties/head_selection"></a>**`head_selection`** *(required)*: Refer to *[HeadSelection](#defs-HeadSelection)*.

### Definitions

- <a id="defs-HeadSelection"></a>**`HeadSelection`** *(object)*
  - <a id="%24defs/HeadSelection/properties/count"></a>**`count`** *(integer, required)*: Number of selected head detections.
  - <a id="%24defs/HeadSelection/properties/selected_indices"></a>**`selected_indices`** *(array, required)*: Indices of selected detections in the original head_detection list, before sorting.
    - <a id="%24defs/HeadSelection/properties/selected_indices/items"></a>**Items** *(integer)*

### Examples

  ```json
  {
      "head_detection": [
          {
              "score": 0.85,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ],
      "head_selection": {
          "count": 1,
          "selected_indices": [
              0
          ]
      }
  }
  ```



<a id="headgaze_point"></a>

## head/gaze_point

*Per-head 2D scene gaze target point with associated likelihood heatmap.*

### Properties

- <a id="properties/head_gaze_point"></a>**`head_gaze_point`** *(array, required)*
  - <a id="properties/head_gaze_point/items"></a>**Items**: Refer to *[HeadGazePoint](#defs-HeadGazePoint)*.

### Definitions

- <a id="defs-HeadGazePoint"></a>**`HeadGazePoint`** *(object)*
  - <a id="%24defs/HeadGazePoint/properties/head_location_xyxy"></a>**`head_location_xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/HeadGazePoint/properties/head_location_xyxy/items"></a>**Items** *(integer)*
  - <a id="%24defs/HeadGazePoint/properties/gaze_point_px"></a>**`gaze_point_px`** *(array, required)*: Length must be equal to 2.
    - <a id="%24defs/HeadGazePoint/properties/gaze_point_px/items"></a>**Items** *(number)*
  - <a id="%24defs/HeadGazePoint/properties/heatmap"></a>**`heatmap`** *(array, required)*: 2D gaze likelihood heatmap over the scene. Runtime type: numpy.ndarray of float32, shape [image_height, image_width], values in [0, 1] probability range.
    - <a id="%24defs/HeadGazePoint/properties/heatmap/items"></a>**Items** *(array)*
      - <a id="%24defs/HeadGazePoint/properties/heatmap/items/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "head_gaze_point": [
          {
              "gaze_point_px": [
                  640.0,
                  360.0
              ],
              "head_location_xyxy": [
                  100,
                  200,
                  300,
                  400
              ],
              "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) -- 2D [0,1] gaze likelihood heatmap"
          }
      ]
  }
  ```



<a id="headsocial_gaze"></a>

## head/social_gaze

*Dyadic social gaze relations between two detected people. Class set: share, mutual, single, miss, void.*

### Properties

- <a id="properties/head_social_gaze"></a>**`head_social_gaze`** *(required)*: Refer to *[HeadSocialGaze](#defs-HeadSocialGaze)*.

### Definitions

- <a id="defs-HeadSocialGaze"></a>**`HeadSocialGaze`** *(object)*
  - <a id="%24defs/HeadSocialGaze/properties/principal"></a>**`principal`**: Left-side / primary person in dyadic interaction. Default: `null`.
    - **Any of**
      - <a id="%24defs/HeadSocialGaze/properties/principal/anyOf/0"></a>: Refer to *[SocialGazePerson](#defs-SocialGazePerson)*.
      - <a id="%24defs/HeadSocialGaze/properties/principal/anyOf/1"></a>*null*
  - <a id="%24defs/HeadSocialGaze/properties/associate"></a>**`associate`**: Right-side / secondary person in dyadic interaction. Default: `null`.
    - **Any of**
      - <a id="%24defs/HeadSocialGaze/properties/associate/anyOf/0"></a>: Refer to *[SocialGazePerson](#defs-SocialGazePerson)*.
      - <a id="%24defs/HeadSocialGaze/properties/associate/anyOf/1"></a>*null*
  - <a id="%24defs/HeadSocialGaze/properties/success"></a>**`success`** *(boolean)*: Whether at least two heads were detected for social gaze inference. Default: `true`.
- <a id="defs-SocialGazePerson"></a>**`SocialGazePerson`** *(object)*
  - <a id="%24defs/SocialGazePerson/properties/head_location_xyxy"></a>**`head_location_xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/SocialGazePerson/properties/head_location_xyxy/items"></a>**Items** *(integer)*
  - <a id="%24defs/SocialGazePerson/properties/gaze_point_px"></a>**`gaze_point_px`** *(array, required)*: Length must be equal to 2.
    - <a id="%24defs/SocialGazePerson/properties/gaze_point_px/items"></a>**Items** *(number)*
  - <a id="%24defs/SocialGazePerson/properties/heatmap"></a>**`heatmap`** *(array, required)*: 2D gaze likelihood heatmap. Runtime type: numpy.ndarray of float32, shape [image_height, image_width], values in [0, 1] probability range.
    - <a id="%24defs/SocialGazePerson/properties/heatmap/items"></a>**Items** *(array)*
      - <a id="%24defs/SocialGazePerson/properties/heatmap/items/items"></a>**Items** *(number)*
  - <a id="%24defs/SocialGazePerson/properties/social_gaze_id"></a>**`social_gaze_id`** *(integer, required)*: Integer class ID of the social gaze relation. Ordered mapping: 0=share, 1=mutual, 2=single, 3=miss, 4=void.
  - <a id="%24defs/SocialGazePerson/properties/social_gaze_label"></a>**`social_gaze_label`** *(string, required)*: Human-readable social gaze relation label. Possible values: share, mutual, single, miss, void. Index of the value matches social_gaze_id.

### Examples

  ```json
  {
      "head_social_gaze": {
          "associate": {
              "gaze_point_px": [
                  200.0,
                  300.0
              ],
              "head_location_xyxy": [
                  600,
                  200,
                  800,
                  400
              ],
              "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) -- 2D [0,1] gaze likelihood heatmap",
              "social_gaze_id": 1,
              "social_gaze_label": "mutual"
          },
          "principal": {
              "gaze_point_px": [
                  800.0,
                  300.0
              ],
              "head_location_xyxy": [
                  100,
                  200,
                  300,
                  400
              ],
              "heatmap": "numpy.ndarray(shape=[H, W], dtype=float32) -- 2D [0,1] gaze likelihood heatmap",
              "social_gaze_id": 1,
              "social_gaze_label": "mutual"
          },
          "success": true
      }
  }
  ```

  ```json
  {
      "head_social_gaze": {
          "success": false
      }
  }
  ```
