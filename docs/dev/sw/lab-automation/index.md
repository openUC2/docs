---
title: Lab automation (SiLA 2)
sidebar_position: 0
description: The openUC2 FRAME as a SiLA 2 device in a lab-automation workcell - what it offers, how a robot hands plates over, and where it is going.
---

# Lab automation with SiLA 2

An openUC2 FRAME running ImSwitch can be one station in a **lab-automation workcell**: a robot
arm brings a well plate from the incubator, the microscope images it, the robot takes it on to
the next device. A scheduler runs the workflow; the microscope offers its functions over
[SiLA 2](https://sila-standard.com), the open standard for laboratory devices.

![The microscope in a workcell](./img/workcell-layers.svg)

The microscope is a *passive* device in this picture. It does not plan the experiment; it
exposes what it can do - move, focus, illuminate, image, run saved acquisition jobs, take and
release a plate - with units, clear refusals and a lock, so that any SiLA-capable scheduler can
drive it. ImSwitch keeps what only the instrument knows: its stage frame and travel limits, the
taught positions, its objectives and its saved jobs.

| You want to | Start here |
|---|---|
| See it work without hardware | [A plate through the virtual microscope](./tutorials/virtual-workcell.md) |
| Put a FRAME into a workcell | [Connect a FRAME to a workcell](./how-to/connect-frame-to-workcell.md) |
| Look up a command, error or setting | [SiLA features of ImSwitch](./reference/sila-features.md) |
| Understand the design and the plan | [Architecture](./explanation/architecture.md) · [Vision](./explanation/vision.md) |

## What the microscope offers

| Feature | For |
|---|---|
| Stage Controller | Position, moves in µm, loading position, homing, stop |
| Imaging Controller | Snap (JPEG preview), save (OME-TIFF), exposure, illumination, autofocus, objectives |
| Experiment Controller | Plate types, plate origin, move to a well, image a list of wells, any ImSwitch experiment |
| Job Controller | Run a saved ImSwitch job (Aufgaben) by name with parameters |
| Labware Transfer Site Controller | SiLA standard plate hand-over with a robot |
| Lock Controller | SiLA standard lock: the workcell claims the microscope, the ImSwitch UI can only watch and stop |

Every element is described in the [reference](./reference/sila-features.md).

## Contents

| Type | Pages |
|---|---|
| Tutorial | [A plate through the virtual microscope](./tutorials/virtual-workcell.md) |
| How-to | [Connect a FRAME to a workcell](./how-to/connect-frame-to-workcell.md) |
| Reference | [SiLA features of ImSwitch](./reference/sila-features.md) |
| Explanation | [Architecture](./explanation/architecture.md), [Vision](./explanation/vision.md) |
