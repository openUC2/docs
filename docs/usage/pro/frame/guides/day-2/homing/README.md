---
sidebar_label: Homing
sidebar_position: 50
---

# Homing

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
:::

*How-to, for operators.* Re-establish the stage's reference position.

## When homing is needed

- After power-up, after hitting an endstop, when coordinates look wrong.

## How to home

- Manual homing per axis; full homing; what to expect (motion, sounds, duration).

![](./IMAGES/homing-placeholder.png)
:::note TODO image
Homing control + the "machine has not been homed" prompt. Notion source:
`FAT FRAME #0007 Korea - Part 1` and `Part 4` (homing after power cycle).
:::

## Known issues and recovery

- Axis stuck at an endstop; coordinates wrong after Y homing.

:::note TODO
Notion sources: `TASK-FR004 no homing during boot`, `TASK-FR005 manual Z homing`,
`TASK-FR008 Homing Y makes coordinates wrong`, `TASK-FR010 axis stuck at endstop`,
`TASK-FR006 stage motion must not damage`. Decide which are fixed vs. user-facing.
Cross-link: [troubleshooting / motion](../../troubleshooting/motion-homing/README.md).
:::
