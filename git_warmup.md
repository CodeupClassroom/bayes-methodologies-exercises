# Git Warmup

Between each step below, run `git status` to check the state of the repository.

1. Create a directory named `git_warmup` within `~/codeup-data-science`.

1. Create a git repository in the directory you just made.

1. Use VS Code to create a file named `numbers.txt`. It should have the
   following contents:

   ```
   one
   two
   three
   four
   ```

1. Add and commit the `numbers.txt` file with a descriptive commit message.

1. What does `working tree clean` mean?

1. Add a new line to `numbers.txt` that contains `five`. What does `git status`
   tell you now?

1. Run `git diff` and inspect the output. What do you notice.

1. Run `git add numbers.txt`, then run `git diff` again. What do you notice?

    Recall that when we run `git add`, the added files are *staged*, and will be
    added to the next commit. Run `git diff` again, but add the `--cached` flag
    to the command.

1. Commit the changes you've made with a descriptive commit message.

1. Delete the first line of the file, and change the word `two` to the number 2.

1. Run `git diff` and inspect the output. What do you notice?

1. Add and commit your changes with a descriptive commit message.

1. Run `git log` and inspect the output. What do you see?

1. For every unique hash from the output of the command above, do the following:

    - Run `git show HASH`. What information does this give you?
    - Run `git diff HASH`. What information does this give you?

   What is the difference between `git show` and `git diff`?

1. Change `three` to the number `3`.

1. Uh oh, you decided that you want to undo the change you made.

   Run

   ```
   git checkout numbers.txt
   ```

   Now look at the contents of `numbers.txt`. What do you notice? What did the `git checkout` command do?

## Summary

- `git log`: view a history of commits
- `git diff`: view the difference between our current state and the last commit; with a hash specified, view the difference between our current state and the specified hash
- `git show`: view the changes introducted in a specific commit

```
git checkout filename.txt
```

Discard any changes to `filename.txt`, go back to the version of `filename.txt` as it was at the most recent commit

```
git checkout HASH -- filename.txt
```

Bring back the version of `filename.txt` as it existed at `HASH`
