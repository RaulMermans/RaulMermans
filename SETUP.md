# Install your GitHub profile refresh

GitHub profile repository: https://github.com/RaulMermans/RaulMermans

## Upload all three files

Do not upload only the README. The banner is stored in `assets/hero.gif`, so the README image will appear broken if that file is absent. The contribution snake requires the workflow at `.github/workflows/snake.yml`.

For a local Git workflow:

1. Clone `https://github.com/RaulMermans/RaulMermans.git`.
2. Extract this ZIP into the root of the cloned `RaulMermans` folder, preserving directory paths.
3. Run the following commands from inside the folder:

```bash
git add README.md assets/hero.gif .github/workflows/snake.yml
git commit -m "Redesign GitHub profile with animated AI engineer banner"
git push origin main
```

If direct pushes are restricted, create a branch and open a pull request instead.

## Start the contribution snake

Once the commit is on `main`, the new GitHub Actions workflow should run automatically. If it does not, go to **Actions > Generate contribution snake > Run workflow**. The workflow writes the SVG assets into the `output` branch, where the README references them.

If the workflow reports insufficient permissions, inspect **Settings > Actions > General > Workflow permissions** and your repository policy; the workflow requests `contents: write` and uses the automatic `GITHUB_TOKEN`.

## Notes

- The banner is an animated GIF rather than an SVG so it works reliably in GitHub's README image rendering.
- The former third-party activity graph was removed because it did not load in the screenshot. GitHub stats remain optional and can fail when the external service is unavailable.
- The banner contains no invented GitHub stats, accolades, or performance claims.
