# L3 V1 — pixel and geometry proofs

L3 validates the exact source and composed PNG/RGB24 pairs. It uses a standard-library PNG decoder with CRC checking and RGB/RGBA8 filter reconstruction. It requires byte identity between each decoded PNG RGB plane and its paired raw RGB24 file.

It checks 720x1280, RGB24 stride 2160, 2,764,800 bytes, the approved content rectangle 504x896 at (108,192), and exact-black top/bottom bands plus left/right gutters. It does not recompute or recompose the QImage output.
