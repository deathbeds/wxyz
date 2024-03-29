---
name: Release
about: Prepare for a release
labels: maintenance
---

- [ ] merge all outstanding PRs
- [ ] ensure the versions have been bumped (check with `doit test:integrity`)
- [ ] ensure the `CHANGELOG.md` is up-to-date
  - [ ] move the new release to the top of the stack
- [ ] validate on binder
- [ ] validate on ReadTheDocs
- [ ] wait for a successful build of `main`
- [ ] download the `dist` archive and unpack somewhere (maybe a fresh `dist`)
- [ ] create a new release through the GitHub UI
  - [ ] paste in the relevant `CHANGELOG.md` entries
  - [ ] upload the artifacts
- [ ] actually upload to npm.com, pypi.org
  ```bash
  cd dist
  twine upload *.tar.gz *.whl
  npm login
  npm publish deathbeds-*-$VERSION.tgz
  npm logout
  ```
- [ ] postmortem
  - [ ] handle `conda-forge` feedstock tasks
  - [ ] validate on binder via simplest-possible gists
  - [ ] bump to next development version
  - [ ] bump the `CACHE_EPOCH`
  - [ ] rebuild `yarn.lock`
  - [ ] update release procedures with lessons learned
