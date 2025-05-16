# README

## Updating git submodules

```bash
cd src/mkslides/assets/highlight.js
git fetch --tags
git tag # Optional to see the available tags
git checkout tags/11.11.1
cd src/mkslides/assets/reveal.js
git fetch --tags
git tag # Optional to see the available tags
cd src/ # Or anywhere else in the mkslides repo, but not in a git submodule
```

```console
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/mkslides/assets/highlight.js (new commits)
        modified:   src/mkslides/assets/reveal.js (new commits)

no changes added to commit (use "git add" and/or "git commit -a")
```

```console
$ git add src/mkslides/assets/highlight.js src/mkslides/assets/reveal.js
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/mkslides/assets/highlight.js
        modified:   src/mkslides/assets/reveal.js
```
