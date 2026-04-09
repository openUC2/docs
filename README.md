# openUC2 Documentation

This repository is used to build and deploy openUC2's documentation site.

## Usage

People who are just end-users of openUC2 products & projects should go to [docs.openuc2.com](https://docs.openuc2.com).

Developers should view the current state of the [openUC2/docs](https://github.com/openUC2/docs) repo at [docs-dev.openuc2.com](https://docs-dev.openuc2.com).
That site should be treated as a developer preview which can have disruptive changes without any prior notice; thus, customers should not be sent to `docs-dev.openuc2.com`.

[docs-staging.openuc2.com](https://docs-staging.openuc2.com) should be used as an intermediate "beta preview" version of `docs.openuc2.com`: it is more stable (i.e. has less accidental disruption) compared to `docs-dev.openuc2.com`, but it may still have a few subtle problems which need to be discovered and fixed before the changes are generally exposed to all customers.
It's okay to link certain customers to certain pages in `docs-staging.openuc2.com`, but only if those customers need to have a preview of newer versions of those specific pages before those changes are ready to be made generally available at `docs.openuc2.com`.

For further explanation, please refer to [DN 17](https://www.notion.so/DN-17-Customer-facing-documentation-system-2854e612c78a80a3a1bdcc223bf030c0?source=copy_link#3134e612c78a80c7b3cff5533bb67e15).

## Development

### Local preview

Run:

```
npm install
npm run start
```

Then open: <http://localhost:3000>

## Deployment

The openUC2 docs site has three GitHub Pages deployments, each with its own repository:

- development/edge release channel: the `master` branch of [openUC2/docs](https://github.com/openUC2/docs); deploys to [docs-dev.openuc2.com](https://docs-dev.openuc2.com).
- staging/beta release channel: the `staging` branch of openUC2/docs; automatically mirrored to the `deploy` branch of [openUC2/docs-staging](https://github.com/openUC2/docs-staging), which deploys to [docs-staging.openuc2.com](https://docs-staging.openuc2.com)
- prod/stable release channel: the `prod` branch of openUC2/docs; automatically mirrored to the `deploy` branch of [openUC2/docs-prod](https://github.com/openUC2/docs-prod), which deploys to [docs.openuc2.com](https://docs.openuc2.com).

After cloning the openUC2/docs repo, then you can fast-forward your local `staging` and `prod` branches to the desired commits on your local `master` branch.
Then you can deploy changes to the staging and prod release channels by pushing your updated local `staging` and `prod` branches, respectively, up to the openUC2/docs repository.
The deployment process should usually be done as follows:

1. Fast-forward the `staging` branch of the openUC2/docs repo to whichever commit of the `master` branch that we want to publish.
2. Wait for it to build and deploy, then look at `docs-staging.openuc2.com` and fix any problems.
3. Once the version in the `docs-staging` repo is stable and mature enough for publication, fast-forward the `prod` branch of the openUC2/docs repo to the publication-ready commit of the `staging` branch.
