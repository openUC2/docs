---
sidebar_label: ImSwitch architecture
sidebar_position: 50
---

# ImSwitch architecture

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
This page is the bridge from user docs into the Developers section.
:::

## The big picture

- Browser frontend ↔ Python backend ↔ hardware (via managers/controllers) ↔ firmware.
- REST API exposes the backend for scripting/integration.

## Managers and the modular model

- How devices (cameras, lasers/LEDs, positioners, objectives) are abstracted as managers.
- How the configuration JSON selects and parameterises them.

## Where things live

- Frontend, backend, config, firmware repos.

:::note TODO
Source: `ImSwitch_Functionality_Overview.md` in the ImSwitch repo (has a full feature
breakdown). Add a simple architecture diagram.
:::

## Related (developers)

- [Extending ImSwitch](../../developers/software/architecture/README.md)
- [Add a device driver](../../developers/software/add-a-device/README.md)
- [REST API](../../developers/applications/rest-api/README.md)
