---
sidebar_position: 100
---

# Updates

## How to upgrade

### to the latest development version

1. [Enter the machine's terminal](../day-1/access.md#the-machines-terminal).
2. Run the following command:
   ```bash
   forklift pallet upgrade @edge
   ```
3. Reboot or soft-reboot the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

If the above command fails with an error message that you have changes which are not yet saved in a Git commit or which might not be in a remote Git repo:

1. Run the following command to check for uncommitted changes:
   ```bash
   git -C ~/.local/share/forklift/pallet/ status
   ```

2. Run the following command to check for unpushed commits:
   ```bash
   git -C ~/.local/share/forklift/pallet/ log
   ```

3. Decide whether you want to `git commit` and `git push` any changes listed in the output of that command before performing the software upgrade.

4. Run the following command:
   ```bash
   forklift pallet upgrade --force @edge
   ```

   :::warning

   This command will permanently delete any local changes you've made!
   You'll lose any changes which you haven't already backed up (e.g. by committing and pushing them to GitHub).

   :::

5. Reboot or soft-reboot the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```
