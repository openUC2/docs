"""Grab PLF intensity frames from FLIM Imager's headless server and save them as .npy.

usage: python grab_plf_frames.py out.npy [n_frames] [timeout_per_frame_s] [width] [height]

Needs the flim-server running on localhost:5249 (FLIM Imager, src-tauri/server:
`cargo run --features native-zest` on macOS) with no other client on /data, and ImSwitch installed
for its FLIMLabsClient. Card settings of the bench test: channel 2, SMA, sync-in 40 MHz, PLF.
The first published frame can be partial and is dropped.
"""
import sys
import time
import numpy as np
from imswitch.imcontrol.model.interfaces.flimlabsclient import FLIMLabsClient

out = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
tmo = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
W = int(sys.argv[4]) if len(sys.argv) > 4 else 256
H = int(sys.argv[5]) if len(sys.argv) > 5 else 256

c = FLIMLabsClient('localhost', 5249, W, H, timeout=20)
assert c.health(), 'flim-server not reachable'
fw = c.resolve_firmware(sync='in', frequency_mhz=40, channels=[2], reconstruction='PLF')
c.start(c.build_imaging_payload(fw, step='scouting', frequency_mhz=40, reconstruction='PLF',
                                image_width=W, image_height=H,
                                channels=[False, True] + [False] * 6, max_frames=n + 3), W, H)
frames = []
try:
    for k in range(n + 1):
        f = c.wait_for_next_frame(timeout=tmo)
        if f is None:
            print('timeout waiting for frame', k)
            break
        if k:
            frames.append(np.asarray(f))
finally:
    c.stop(close_socket=True)
if frames:
    a = np.stack(frames)
    np.save(out, a)
    print(f'saved {a.shape} -> {out}; counts/frame {a.reshape(len(a), -1).sum(1).tolist()}')
