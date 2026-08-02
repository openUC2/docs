---
sidebar_label: Fluorescence
sidebar_position: 50
---

# Acquire your first fluorescence image

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
:::

*Learning-oriented, for users (biologists).* If your FRAME is equipped with laser
illumination, this tutorial captures a single fluorescence channel and then a
multi-channel image.

:::danger Laser safety — read first
- Draft the safety rules for the installed lasers (405 / 488 / 520 / 635 nm): never look
  into the beam, interlocks, eyewear if applicable, who may operate.
:::
:::note TODO
Fill in the exact laser classes and the required safety wording for the FRAME.
:::

## Step 1 — Select a channel

- Which laser matches which dye (405 - DAPI, 488 - GFP, 635 - AlexaFluor 647, etc.).
- Turn off LED/brightfield, enable the fluorescence channel.

![](./IMAGES/illumination-panel-placeholder.png)
:::note TODO image
Illumination panel with fluorescence channel selected. Notion / existing source:
`tutorials/day-1/first-sample` already shows the Illumination section with 488 nm.
:::

## Step 2 — Set exposure and power, avoid bleaching

- Balancing laser power vs. exposure; keeping power low to reduce photobleaching.

## Step 3 — Multi-channel acquisition

- Sequentially acquire several channels; how they are combined/saved.

## Step 4 — Save

- Channel metadata in OME-TIFF; opening in Fiji.

## Related

- [Illumination and contrast explained](../../../explanations/illumination-and-contrast/README.md)
- Reference: [Specifications - lasers](../../../reference/specifications/README.md)
