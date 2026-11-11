---
sidebar_label: Data output
sidebar_position: 80
---

# Data output and export

Where ImSwitch stores data on the FRAME and how to get it off the machine.

## Where files are stored

- ImSwitch writes every image to the storage of the Raspberry Pi while the acquisition runs. Nothing is kept only in memory.
- The default storage is the micro SD card. It is slow and small: a tile scan fills it quickly.
- A USB drive can be plugged in and chosen as the target.
- The Raspberry Pi sits on an NVMe base. With an M.2 SSD in it, writing is much faster. Ask openUC2 which size fits your unit.

Scans of the *Wellplate* app land in the folder `ExperimentController`, one folder per run.

## Formats

| Format | Use |
|---|---|
| OME-Zarr | scans with tiles, channels, Z and time; holds the stage position of every tile |
| OME-TIFF or TIFF | single images and small series; opens directly in Fiji |
| PNG, JPEG | snapshots for a quick look |

Switch on one or several formats in the *Output* step of the *Wellplate* app. Every format that is switched on is written.

## Get the data off the machine

- **File Manager** in ImSwitch: open the run's folder, right-click, download. A folder comes as one archive.
- **USB drive**: copy the folder in the File Manager.
- **napari**: with the `napari-ome-zarr` plugin, napari opens the OME-Zarr folder of a downloaded run.

Tiles saved as TIFF are stitched in Fiji, for example with *Grid/Collection stitching*.

## Related

- [Acquire and save your first dataset](../../../tutorials/day-2/acquire-data/README.md)
- [Run a large-area scan on a slide](../../../tutorials/day-2/stitching-scan-on-a-slide/README.md)
