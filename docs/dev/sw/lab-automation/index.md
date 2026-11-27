---
title: Lab automation
sidebar_position: 0
description: Run an openUC2 FRAME as one station of an automated lab - in a UniteLabs workcell over SiLA 2 today, with Arkitekt to follow.
---

# Lab automation

An openUC2 FRAME running ImSwitch can be driven by lab-automation software instead of a person
at the screen: a robot brings the plate, a workflow decides what to image, the results go on to
the next step. ImSwitch connects to that software through one integration per platform. Each
one calls the same ImSwitch controllers as the ImSwitch UI, so travel limits, refusals while
something else runs and the OME-Zarr / OME-TIFF writers are the same everywhere.

| Integration | Standard | What it is for | Status |
|---|---|---|---|
| [UniteLabs workcell (SiLA 2)](./unitelabs-sila2/index.md) | SiLA 2 over gRPC | The FRAME as a SiLA device in a UniteLabs workcell: plate hand-over with a robot, imaging wells, saved jobs, a lock against the ImSwitch UI | Tested on the virtual microscope and with UniteLabs GroundControl; first runs on a FRAME |
| Arkitekt | Arkitekt actions | The FRAME as an app in an Arkitekt server: image analysis and workflows on the acquired data | In ImSwitch (`ArkitektController`); docs follow |
