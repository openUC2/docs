---
sidebar_label: Software / ImSwitch
sidebar_position: 20
---

# Troubleshooting: software / ImSwitch

:::note Draft outline
Scaffold. One entry per issue: symptom, cause, fix. Delete this banner when done.
:::

:::note TODO — source reports (decide publish / drop / known-limitation)
- `TASK-FR014` ImSwitch unable to shut down the machine
- `TASK-FR016` ImSwitch reports a misleading message
- `TASK-FR017` GUI bug while trying to switch
- `TASK-FR019` ImageJ is impractical for use case
Each Notion folder has screenshots to reuse.
:::

## ImSwitch will not shut down the machine

- Symptom / cause / fix. Cross-link: [shutdown tutorial](../../../tutorials/day-1/shutdown/README.md).

## Misleading status / error message

- Symptom / cause / fix.

## GUI switching bug

- Symptom / cause / fix.

## Live view is frozen

- **Symptom:** the live image stops updating while the stage and the lamp still react.
- **Cause:** the video stream to the browser stalled.
- **Fix:** stop and start the stream in the *Live View*. If it stays frozen, reload the page.

## A scan pauses for several seconds

- **Symptom:** a scan stops between tiles and continues by itself.
- **Cause:** not confirmed. Seen at a commissioning in November 2026 while frames were written to the micro SD card.
- **Fix:** the data is complete. Write to a USB drive or an SSD if it happens often, and report it with the log.

## Related

- [ImSwitch UI reference](../../../reference/imswitch-ui-reference/README.md)
