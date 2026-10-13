---
name: commit-push
description: Commit the current work to Git with a task-numbered message, then push it to GitHub. Use only when the owner says the step works and asks to commit and push.
disable-model-invocation: true
argument-hint: "[task number, e.g. M3-T2] [short description]"
---

# Commit and push to GitHub

The owner has asked to save the current work to Git and GitHub. Following `CLAUDE.md`, this skill is only used after the owner says the step works. Explain everything in plain English, with no jargon.

## Steps

1. **Check what changed.** Run `git status` and `git diff --stat` (PowerShell terminal). Tell the owner, in plain words, which files are new or changed.

2. **Safety check before saving.** Stop and tell the owner if any of these appear:
   - `.env` or any file that looks like it holds a password, key or token
   - anything inside `storage/` (it must stay out of Git)
   - files that look like real patient data
   - very large files (over about 20 MB)

   Never use `git add -A` blindly. Add files by name or folder, and leave out anything above.

3. **Work out the task number.** Use the one in the arguments (`$ARGUMENTS`). If none was given, infer it from the work just done (for example `M3-T2`). If you cannot tell, give 2 or 3 likely options with a recommendation and ask.

4. **Write the commit message** in this form:

   ```
   M3-T2: kidney and liver adjustments

   Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
   ```

   The first line is the task number, a colon, and a short plain description. Use a heredoc so the lines are kept.

5. **Show the owner the message and the file list, then commit.** Do not amend earlier commits. Do not skip hooks. If a hook fails, explain why and fix the cause.

6. **Check the GitHub link.** Run `git remote -v` and `git branch --show-current`.
   - If there is no remote, stop. Tell the owner the repository is not yet linked to GitHub and give the exact command to type: `git remote add origin <repo URL>` (the company account is Appbay-AI). Ask for the URL. Do not guess it.
   - If the branch is `main`, that is fine for this project. Say which branch is being pushed.

7. **Push.** Run `git push`. If the branch has no upstream yet, run `git push -u origin <branch>`. Never use `--force`. If the push is rejected, explain in plain words and offer 2 or 3 options with a recommendation.

8. **Report.** Show the actual output of the commit and the push (short hash, branch, and the result line). Then say in one or two sentences what it means, for example: "Your work for M3-T2 is now saved and backed up on GitHub."

## Rules

- Never commit or push without the owner's go-ahead in this conversation.
- Never print the contents of `.env` or any secret.
- Never force-push or rewrite history.
- If the owner is not signed in to GitHub, tell them to type `! gh auth login` in the prompt and follow the steps, then retry.
