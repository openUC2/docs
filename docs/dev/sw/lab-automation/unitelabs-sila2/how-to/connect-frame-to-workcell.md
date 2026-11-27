---
title: Connect a FRAME to a workcell
sidebar_position: 1
description: Switch on the SiLA 2 server of a FRAME, put it on the workcell network, teach the hand-over position and plate origins, and check it step by step.
---

# Connect a FRAME to a workcell

*How-to.* For a FRAME running ImSwitch that should become a station in a SiLA 2 workcell. The
steps that move the stage or switch light on are marked; do them with the stage free and nobody
looking into the light path.

## 1. Switch the SiLA server on

In the FRAME's setup file (`~/ImSwitchConfig/imcontrol_setups/<your setup>.json`) add `"SiLa2"`
to `availableWidgets` and a `sila2` block, then restart ImSwitch:

```json
"sila2": {
  "serverName": "FRAME 12",
  "serverPort": 50052,
  "discovery": true
}
```

Check it in a browser or with curl:

```bash
curl http://<frame>:8001/imswitch/api/SiLa2Controller/getSiLA2Status
```

`running: true` and the UUID mean the server is up. All keys are in the
[reference](../reference/sila-features.md#setup).

## 2. Network

- The workcell must reach TCP port 50052 (gRPC) on the FRAME.
- Discovery uses mDNS (UDP 5353 multicast). Guest Wi-Fi, VPNs and separate VLANs often block
  it; then give the workcell the FRAME's address and port instead.
- Give the FRAME a fixed host name or address. The server UUID is derived from host name and
  port; set `serverUUID` in the `sila2` block if the host name will change.
- For TLS set `tls: true` with `certificateChain` and `privateKey` (paths or PEM text); the
  client then needs the CA certificate.

## 3. Teach the hand-over position (motion)

The robot puts the plate on the stage at the **loading position**. Teach it once:

1. In the ImSwitch UI, jog the stage until the stage insert sits where the gripper can reach it
   without touching the objective or the condenser. Lower Z if the gripper needs room.
2. Save the position, from the workcell (SiLA `StageController/TeachLoadingPosition`) or over
   HTTP:

```bash
curl -X POST "http://<frame>:8001/imswitch/api/PositionerController/setSampleLoadingPosition?useCurrent=true"
```

It is stored in the setup (`sampleLoadingPositionX/Y/Z` of the positioner). From now on
`PrepareForInput` and `PrepareForOutput` switch the light off and drive there.

## 4. Teach each plate type (motion)

So that the workcell can say "well B3", the microscope must know where plates of a type sit:

1. Put a plate of the type on the stage, centre a well you can recognise (e.g. A1) in the live
   view.
2. Call `ExperimentController/SetPlateOrigin(Labware, Well)` with the plate's load name (see the
   `Labware` property, e.g. `corning_96_wellplate_360ul_flat`) and that well.

The origin is saved per plate type in the setup (`sila2.plateOrigins`); `CalibratedLabware`
lists the taught types. Teach again after you change the stage insert.

## 5. Check it, in three rounds {#check}

`imswitch-sila-check` calls every SiLA command, the way the workcell will. Run it from any
computer that reaches the FRAME (it needs only `pip install unitelabs-sila` and ImSwitch's
`sila_check.py`). First see whether the FRAME is found on the network, with its LAN address:

```bash
imswitch-sila-check --list
```

```bash
imswitch-sila-check --discover --name "FRAME 12"
```

Or, without discovery:

```bash
imswitch-sila-check --host <frame> --port 50052
```

Round 1 moves nothing and switches no light. Then, with the stage free:

```bash
imswitch-sila-check --host <frame> --port 50052 --motion --light --intensity 10
```

and only on purpose, because it drives every axis to its end switch:

```bash
imswitch-sila-check --host <frame> --port 50052 --home
```

`--teach` would overwrite the taught plate origin and loading position; leave it off on a taught
instrument. `--json report.json` writes the results to a file. Every `FAIL` line names the
command and the error.

## 6. Hand it to the workcell

Give the workcell team the server name, UUID, address and port, the hand-over position name
(`Stage`) and the taught plate types. Their scheduler locks the microscope for each workflow;
while locked, the ImSwitch UI can watch and stop but not move or light up.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| The UI says *423 Locked* | A workcell holds the lock. Wait for its workflow, or after a crash free it: `curl -X POST http://<frame>:8001/imswitch/api/SiLa2Controller/releaseWorkcellLock` |
| Discovery finds nothing | Multicast blocked; connect by address. Check that `discovery` is `true`. |
| `StageLimitReached` | The target lies outside the stage travel limits; the limit is the answer, check the plate origin or the position. |
| `PlateNotCalibrated` | Teach the plate type (step 4). |
| `InstrumentBusy` | An acquisition, job or calibration runs in ImSwitch; wait or stop it. |
| `NotConfirmed` on RunJob | The job homes or changes the objective; run it with `Confirmed` set. |
| `getSiLA2Status` shows an `error` | The server did not start, e.g. the port is taken; the ImSwitch log has the details. |

## Let an AI agent test it as an outsider

Before handing a FRAME to a workcell team, let a coding agent that has never seen ImSwitch build
its own client, the way an integrator would. Give it only the running server and the
[UniteLabs client tutorial](https://docs.unitelabs.io/connector-development/tutorial/build-a-sila-client/):

> Build a test client that locates the SiLA server "FRAME 12" on the network by discovery,
> connects to it, and tests all of its endpoints, following the tutorial. Treat the server as a
> black box: learn its features from GetFeatureDefinition. Read every property, take a value
> from every observable property, call every command, and provoke every declared error.
> Report coverage, failures, and everything in the feature definitions that made the client
> hard to write.

Do this on the virtual microscope, or on a FRAME with the stage free. The first such run found
eight faults the built-in check had missed (see [Architecture](../explanation/architecture.md#testing-every-command)).
Fold what it finds into `imswitch-sila-check` (`imswitch/sila_check.py`), so the next run of the
check catches it too.
