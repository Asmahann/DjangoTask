# 🤖 GitHub Activity & Mini-Project Bot

Automate your GitHub profile activity graph by generating organic mini-projects, utility modules, computer science algorithms, and developer learning logs (TIL notes) in private repositories.

---

## 🔑 Crucial Setup: Display Private Contributions

By default, GitHub only shows contributions in **public** repositories on your profile heatmap. To display contributions from your **private** repositories:

1. Go to your GitHub profile page (`https://github.com/your-username`).
2. Above your contribution graph heatmap on the right, click **Contribution settings** dropdown.
3. Check **"Private contributions"**.

Now, every commit made by the bot in your private repository will immediately light up your contribution graph!

---

## 🚀 Mode 1: Zero-Maintenance Cloud Automation (GitHub Actions)

This repository includes a pre-configured GitHub Actions workflow in `.github/workflows/daily_activity.yml` that runs automatically in GitHub's cloud **1-2 times per day**.

### Repository Settings Configuration:
1. Open your repository on GitHub.
2. Click **Settings** -> **Actions** -> **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Click **Save**.

That's it! GitHub Actions will automatically generate and commit realistic code snippets every day without requiring your laptop to be on.

---

## 💻 Mode 2: Local CLI Execution

You can also run the bot manually on your local computer to generate mini-projects on demand.

### Test run (without committing):
```bash
python github_bot/bot.py --dry-run
```

### Generate a specific mini-project type locally:
```bash
# Generate a Python utility script
python github_bot/bot.py --type utils

# Generate an Algorithm / Data Structure implementation
python github_bot/bot.py --type algo

# Generate a Developer Learning Note / TIL
python github_bot/bot.py --type notes

# Generate a Web Component / JavaScript utility
python github_bot/bot.py --type web
```

### Commit and Push automatically:
```bash
python github_bot/bot.py --type random --push
```

---

## 📂 Generated Structure

The bot automatically organizes generated code under:
- `projects/python_utils/` — Python helper modules, parsers, decorators, caching utilities.
- `projects/algorithms/` — Clean implementations of trees, graph traversals, tries, search algorithms.
- `projects/web_snippets/` — Micro JS/CSS/HTML utilities & events.
- `notes/` — Structured Markdown developer notes and cheat sheets with executable code.

---

## 🎨 Customizing Commit Schedule

To change the times or frequency of automated cloud commits, edit the cron lines in `.github/workflows/daily_activity.yml`:

```yaml
schedule:
  - cron: '17 8 * * *'  # Runs daily at 08:17 UTC
  - cron: '42 17 * * *' # Runs daily at 17:42 UTC
```
