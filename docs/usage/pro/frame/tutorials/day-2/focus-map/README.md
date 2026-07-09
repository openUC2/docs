---
sidebar_label: Focus Map
sidebar_position: 40
---

# Keep a big scan in focus with a focus map

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
:::

*Learning-oriented, for users.* Over a large sample the focus drifts because the slide
or plate is never perfectly flat. A focus map samples the focus at a few points and
interpolates the correct Z everywhere in between — so a big scan stays sharp without
running a full Z-stack at every tile.

## The idea

- Sample tilt/curvature across a large area; interpolate a focus surface.

<iframe width="560" height="315" src="https://www.youtube.com/embed/dD1ns-K_2Cc?si=aAFWlC9M1zTDFZIN" title="Focus Mapping" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

:::note TODO
This Focus Mapping video was previously on the Day-*n* guides page; it lives here now as
the tutorial. Decide whether to keep the video, replace with screenshots, or both.
:::

## Step 1 — Place focus points

- How to add focus reference points across the region and focus each one.

![](./IMAGES/focus-points-placeholder.png)
:::note TODO image
Focus-map point placement UI. Notion source:
`FRAME_DOKU_FROM_NOTION/FAT FRAME #0007 Korea - Part 8 (1)`
("Testing large area scan 20x Fokus Map").
:::

## Step 2 — Run the mapped scan

- Start the scan using the interpolated focus; how it differs from single-Z.

## When to use focus map vs. autofocus vs. Z-stack

- Comparison table prompt: speed, robustness, data size, sample type.

## Related

- [Autofocus how-to](../../../guides/day-2/autofocus/README.md)
- [Autofocus explained](../../../explanations/autofocus-explained/README.md)
