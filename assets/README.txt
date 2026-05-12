Facial enrollment image for OPSIIE
===================================

Place a clear, front-facing photograph of the enrolled operator at:

  enrollment.jpg

The path is referenced from `kun.py` (template user `Demo Operator`). The
`face_recognition` library loads this still image at boot and compares live
camera encodings against it.

Replace the file with your own portrait before running authentication. Do not
commit personal biometric enrollment images to a public repository; keep them
local or in a private credential store.
