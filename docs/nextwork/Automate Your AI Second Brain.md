---
title: "Automate Your AI Second Brain"
source: "https://nextwork.ai/projects/ca88d155-c925-508c-88eb-ef48455c1a98?track=high"
author:
  - "[[the end of this project]]"
  - "[[you'll have:]]"
published:
created: 2026-10-09
description: "Turn your Obsidian vault into a daily operating system with Claude Code."
tags:
  - "clippings"
---
## Welcome Winchy! How can I help you today?

[Still stuck? Get help from a human](https://discord.gg/8A3mX3CDz5)

## Automate Your AI Second Brain

Turn your Obsidian vault into a daily operating system with Claude Code.

![Profile image](https://s.gravatar.com/avatar/903b38320ee480849386a70a2d987f8c?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fot.png) ![Profile image](https://lh3.googleusercontent.com/a/ACg8ocKKXNTeY-hxpR39jTDcYiHHt3gBmkoko70ncrGiE5eh31PK3A=s96-c) ![Profile image](https://lh3.googleusercontent.com/a/ACg8ocJLRzRaoPJwW7SBE1QbKBq1W5k64zYCzXSe_hHHr9DnX9cHNg=s96-c) 20+ completed

DIFFICULTY

easy

TIME

1h

REFRESHED

18th Sep '26

COST

Free

OS

### ⚡️ 30 Second Summary

Every morning you piece together your day from scattered sources: calendar invites, unread messages, yesterday's notes, and a to-do list that never quite matches reality.

In this project, you will transform your AI second brain into a daily operating system that briefs you each morning, captures your day each evening, backs up your vault to

GitHub

, and connects

Claude Code Desktop

to your real-world tools with

MCP

Connectors.

### What You'll Build

You will add

Git

version control,

MCP

Connectors, and two new

Claude Code

slash commands to your

Obsidian

vault, turning it into a system that actively works for you every day.

![Architecture diagram showing an Obsidian vault backed up to a private GitHub repository, with Claude Code connected to Google Calendar, Linear, and Notion via MCP Connectors, powering /briefing and /debrief slash commands](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/architecture-diagram-showing-an-obsidian-vault-backed-up-to-a-private-github-repository-with-claude-code-connected-to-google-calendar-linear-and-notion-via-mcp-connectors-powering-briefing-and-debrief-slash-commands1776972338036.webp)

Architecture diagram showing an Obsidian vault backed up to a private GitHub repository, with Claude Code connected to Google Calendar, Linear, and Notion via MCP Connectors, powering /briefing and /debrief slash commands

**By the end of this project, you'll have:**

- 🔐 A **private GitHub repository** backing up your vault with automatic syncing via the Obsidian Git plugin.
- 🔌 **MCP Connectors** linking Claude Code to your everyday tools like Google Calendar, Linear, and Notion.
- 🔄 A **/pull-sources slash command** that auto-ingests Claude Code sessions, Gmail, and Granola transcripts straight into your vault.
- ☀️ **/briefing and /debrief slash commands** that generate a personalized morning brief from your wiki, calendar, and priorities, then capture your day, update your wiki, and log progress each evening.
- 💎 **Secret Mission:** Schedule **/briefing as a Cloud Routine** so it runs every weekday morning on Anthropic's cloud and lands in your vault before you open your laptop.

Want a complete demo of how to do this project, from start to finish? Check out our 🎬 [walkthrough with Maximus](https://www.youtube.com/watch?v=AogwEfWZVds)

![](https://www.youtube.com/watch?v=AogwEfWZVds)

> 💡 Are there any prerequisites?
> 
> This is Part 2 of the [AI Second Brain](https://learn.nextwork.org/projects/ai-second-brain-claude-code) series. Complete Part 1 first to set up your Obsidian vault, CLAUDE.md schema, and the
> 
> /ingest
> 
> ,
> 
> /query
> 
> ,
> 
> /lint
> 
> , and
> 
> /log
> 
> slash commands before starting here.

Not sure if this project is right for you? Check if it matches your goals

If you're up for a bit of a challenge, **quiz yourself** on the key concepts up ahead in this project.

1. [Part 1: Build an AI Second Brain with Claude Code](https://learn.nextwork.org/projects/ai-second-brain-claude-code)
2. Part 2: You are here!

## Start Your Project Here

Pick the learning style that fits you best.

## Step-by-Step Guidance

Welcome to the Step-by-Step Guidance version of this project. Let's do this!

If you're ever stuck, [ask the NextWork community](https://community.nextwork.ai/). Learners like you are already asking questions about this project.

👀 Step #0

### Before We Start...

#### ✍️ What are we doing in this project?

🔧 Step #1

### Get Your Vault Ready

In Part 1, you used

Claude Code

in your terminal to build an AI second brain. In Part 2, we're going to wire that same vault into your live tools with

MCP Connectors

so Claude can see your calendar, chat, and docs.

Before that works, your setup needs to be in the right spot. Whether you finished Part 1 yesterday or you're jumping in fresh today, this step ends with you at the same starting point:

Claude Code Desktop

open on a

second-brain

vault that already has CLAUDE.md and four

slash commands

in place.

**In this step, get ready to:**

#### ✍️ What are we doing in this step?

Edit answer

**Install Claude Code Desktop**

Claude Code Desktop

is the same AI coding agent you used in Part 1, but packaged as a desktop app. It reads the exact same config as the CLI (your CLAUDE.md, your

.claude/commands/

, your hooks and skills), so everything you built in Part 1 travels with you.

![The Code tab selected in the Claude Code Desktop left sidebar](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-code-tab-selected-in-the-claude-code-desktop-left-sidebar1776786540527.webp)

The Code tab selected in the Claude Code Desktop left sidebar

- At the bottom of the prompt box, check the model selector. Set it to **Sonnet** for this project.

> 💡 Why Sonnet instead of Opus?
> 
> This project is mostly note reasoning and file I/O, not deep code architecture, so Sonnet handles it well and uses far less of your plan's usage limit than Opus. You can always switch to Opus later if you're scaling this out or chaining complex logic, but for every slash command you'll run in this project, Sonnet is plenty.
> 
> 💡 **Why switch from the CLI?**
> 
> Claude Code Desktop shares the exact same config as the CLI. It reads your CLAUDE.md,
> 
> .claude/commands/
> 
> , hooks, and skills from the same folders, so nothing you built in Part 1 breaks. The reason for the switch is the graphical
> 
> MCP Connectors
> 
> UI you'll use in Step 2.
> 
> 🙋♀️ **Using Linux?**
> 
> Claude Code Desktop isn't available on Linux yet. Ask about your options.

**Bring or Build Your Vault**

Now the big branch. The rest of Part 2 assumes you have a

second-brain

vault with a CLAUDE.md and four

slash commands

(

/ingest

,

/query

,

/lint

,

/log

) already inside it. If you finished Part 1, you just point

Claude Code Desktop

at your vault. If you're starting fresh, you'll scaffold the whole thing in one prompt.

Pick the tab that matches your situation:

Your Part 1 vault already has everything Claude needs. You just need to point

Claude Code Desktop

at it.

- In the **Code** tab, select **Local** as your environment.

![The Code tab with Local selected as the environment](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-code-tab-with-local-selected-as-the-environment1776786550423.webp)

The Code tab with Local selected as the environment

- Navigate to your Part 1
	second-brain
	vault (for example,
	~/Documents/second-brain
	) by clicking **Select folder**.
- Click **Open**.

![Claude Code Desktop folder selector pointing at the second-brain vault](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776786558655.webp)

Claude Code Desktop folder selector pointing at the second-brain vault

- Set the permission mode to **Ask permissions**.
- In the session toolbar above the prompt box, make sure **worktree** is **NOT** selected (you want the plain
	second-brain
	project selected, not an isolated worktree copy).

![The Claude Code Desktop prompt box with the second-brain vault loaded as the active project](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-claude-code-desktop-prompt-box-with-the-second-brain-vault-loaded-as-the-active-project1776798017202.webp)

The Claude Code Desktop prompt box with the second-brain vault loaded as the active project

> 💡 Why "Ask permissions"?
> 
> Ask permissions is the safest default. Claude pauses before reading files, writing changes, or running commands so you can see exactly what the agent is doing on your vault.
> 
> 💡 **Why turn worktree off?**
> 
> Worktree mode runs your session in an isolated copy of the repo. That means Claude writes files to that copy, not to your real
> 
> second-brain
> 
> vault at
> 
> ~/Documents/second-brain
> 
> . If worktree is on, your
> 
> slash commands
> 
> and
> 
> raw/
> 
> files end up somewhere else, and
> 
> /pull-sources
> 
> won't find your
> 
> Claude Code
> 
> session files in
> 
> ~/.claude/projects/
> 
> under the path you expect. Keep it off for this project so everything lands in your actual
> 
> second-brain
> 
> vault.

No Part 1 vault? No problem. You'll create a brand new

Obsidian

vault and let Claude scaffold the whole Part 1 structure, CLAUDE.md, and four

slash commands

in a single prompt.

**Install Obsidian**

Obsidian

is the Markdown knowledge base your vault lives inside. It reads plain

.md

files on disk, which is exactly what

Claude Code Desktop

wants to work with.

**Create the second-brain Vault**

- In Obsidian's welcome window, click **Create new vault**.
- Set **Vault name** to
	second-brain
	.
- Set **Location** to
	~/Documents
	(so the final path is
	~/Documents/second-brain
	).
- Click **Create**.

![Obsidian create vault dialog with the name second-brain and location set to Documents](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/obsidian-create-vault-dialog-with-the-name-second-brain-and-location-set-to-documents1776970282028.webp)

Obsidian create vault dialog with the name second-brain and location set to Documents

**Open the Vault in Claude Code Desktop**

- Switch to
	Claude Code Desktop
	.
- In the **Code** tab, select **Local** as your environment.
- Navigate to
	~/Documents/second-brain
	by clicking **Select folder**.
- Click **Open**.
- Set the permission mode to **Ask permissions**.
- In the session toolbar above the prompt box, make sure **worktree** is **NOT** selected (you want the plain
	second-brain
	project selected, not an isolated worktree copy).

![Folder picker showing the second-brain vault selected as the project folder](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776786558655.webp)

Folder picker showing the second-brain vault selected as the project folder

**Paste the Scaffolding Prompt**

This single prompt creates the whole Part 1 vault in one pass: the directory structure, CLAUDE.md, and four

slash commands

.

- Paste this entire prompt into the Claude Code Desktop prompt box and press **Enter**:

```js
I'm setting up an AI second brain in this Obsidian vault. Create this structure and content:

raw/ (with .gitkeep)
wiki/
  index.md (one-paragraph intro: wiki maintained by Claude Code, raw notes in raw/, compiled pages here)
  concepts/ (with .gitkeep)
  people/ (with .gitkeep)
  projects/ (with .gitkeep)
  log.md (just "# Log" heading)
CLAUDE.md with 4 sections:
  1. ## Project Structure: raw/ (source material) and wiki/ (Claude-maintained cross-linked pages by topic).
  2. ## Page Conventions: YAML frontmatter (title, type, last-updated), Title Case titles, [[Wiki Links]], bullets end with full stops.
  3. ## Style Guide: second person, plain English, one idea per sentence, no em dashes, bold for emphasis.
  4. ## Domain Context: ask me 3-4 questions about my work domain and put my answers here for slash command context.
.claude/commands/ with 4 slash commands:
  - ingest.md: reads raw/, creates/updates wiki pages per conventions, appends an ingest run entry to wiki/log.md.
  - query.md: answers questions by searching wiki/ first then raw/, cites every claim by wiki page name.
  - lint.md: scans wiki/ for broken [[links]], missing frontmatter, empty pages, returns a health report.
  - log.md: appends a timestamped entry to wiki/log.md. Uses $ARGUMENTS if provided.

Ask me the 4 Domain Context questions before writing CLAUDE.md. Then write every file in one pass and ask me to approve each.
```

**Answer Claude's Domain Context Questions**

Claude pauses and asks you 3-4 questions about your work domain before writing anything. This is what personalises your second brain.

- Answer each question honestly and in your own words. Vague answers produce a vague CLAUDE.md.
- When Claude has enough context, it starts proposing files.

![Claude Code Desktop asking domain context questions during the vault scaffold](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/vault-scaffold-domain-questions.webp)

Claude Code Desktop asking domain context questions during the vault scaffold

**Approve Each File**

Because you chose **Ask permissions**, Claude pauses and asks before writing every file.

- Review each file Claude proposes.
- Click **Approve** for each one.
- Keep approving until Claude reports the scaffold is complete.
- Quit
	Obsidian
	and reopen it.
	Claude Code Desktop
	wrote the new folders and files directly to disk, and Obsidian's file explorer only picks up the full structure (including
	CLAUDE.md
	and the
	wiki/
	tree) after a fresh launch.

> 💡 Where are my slash commands?
> 
> Obsidian hides folders that start with a dot by default, so you won't see
> 
> .claude/commands/
> 
> in the file explorer. That's expected. The files are on disk and
> 
> Claude Code Desktop
> 
> reads them from there.

**Drop in Some Raw Notes**

A scaffolded vault is an empty vault. Give Claude something real to work with.

- Drop 3-5 Markdown files (notes from anywhere, hand-written or from
	Notion
	,
	Granola
	, or another tool) into
	raw/
	.
- If you have a Claude.ai or ChatGPT
	JSON
	export, paste this prompt into Claude Code Desktop to convert it:

```js
Convert ~/Downloads/claude-export.json into Markdown files in raw/, named by conversation title (kebab-case .md). Each file has YAML frontmatter (source, exported-date, original-title) and a ## Messages section with each turn as a subheading. Skip conversations with fewer than 2 messages. Show me the first 3 files before writing the rest.
```

- Run
	/ingest 2
	in Claude Code Desktop to test the workflow on two files.
- Approve the proposed
	wiki
	pages, then run
	/ingest
	with no number to process the rest.

#### 📸 Take a screenshot of your second-brain vault open in Claude Code Desktop with the wiki/ folder populated.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

**Verify Everything Works**

Last check. Whether you brought your Part 1 vault or just scaffolded a new one,

Claude Code Desktop

should now see the same CLAUDE.md and four

slash commands

. Let's prove it.

- Paste this prompt into Claude Code Desktop, then press **Enter**:

```js
List the slash commands available in this vault and summarize CLAUDE.md in one paragraph each.
```

- If macOS shows a privacy prompt asking to allow **"claude"** to access files in your **Documents** folder, click **Allow**.

![macOS privacy dialog prompting to allow claude to access files in the Documents folder](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/macos-privacy-dialog-prompting-to-allow-claude-to-access-files-in-the-documents-folder1776786607540.webp)

macOS privacy dialog prompting to allow claude to access files in the Documents folder

- Wait for Claude's response.

> 💡 What is this prompt?
> 
> macOS protects your
> 
> Documents
> 
> folder behind a one-time privacy gate.
> 
> Claude Code Desktop
> 
> triggers it the first time it reads files from your vault, because your vault lives inside
> 
> ~/Documents/
> 
> . Click **Allow** once and you will not see it again for this vault. Windows has no equivalent prompt.

#### 📸 Take a screenshot of Claude Code Desktop showing the four slash commands listed and the CLAUDE.md summary.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### ✍️ Which four slash commands are you carrying into the rest of Part 2, and what is each one for?

1/2

Your vault is loaded with CLAUDE.md, four

slash commands

, and real notes. Next up, you'll protect it with a

GitHub

backup and wire Claude up to your live tools so your briefings have real data to work with.

🔍 Step #2

### Back Up and Connect Your Tools

Your vault is loaded and

/ingest

has stitched your raw material into a proper

wiki

. Beautiful, but everything still lives on one laptop, and Claude still only knows what's inside that folder.

So next we give your second brain a home on the internet and a window into the real world. You'll push your vault to

GitHub

so it has a full history, a backup if your laptop dies, and a place the cloud can run your briefing from when we automate it later. The

Obsidian Git

plugin auto-syncs every 10 minutes in the background. Then you'll wire in at least one

MCP Connector

so Claude can actually read your calendar, chat, or docs.

**In this step, get ready to:**

#### ✍️ What are we doing in this step, and how do backups and live data work together to power your daily operating system?

**Push Your Vault to GitHub**

Heads up, most of this substep happens in your **terminal**, not

Claude Code Desktop

. You're setting up the backup plumbing first. You'll jump back into Claude Code Desktop later in this step to wire up

MCP Connectors

.

Before your vault can back up anywhere, your machine needs

Git

installed and configured. Git is the

version control

tool that actually tracks every change to your files.

GitHub

is the cloud service that stores those changes remotely.

- Open your terminal and run:

```bash
git --version
```

![Terminal showing a Git version number confirming Git is installed](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/terminal-showing-a-git-version-number-confirming-git-is-installed1776786827889.webp)

Terminal showing a Git version number confirming Git is installed

You're ready to go.

No worries, let's install it.

- Install
	Homebrew
	if you don't already have it by following the instructions at [brew.sh](https://brew.sh/).
- Install Git with:

```bash
brew install git
```

- Close and reopen your terminal, then re-run
	git --version
	to confirm.

- Download the installer from [git-scm.com/download/win](https://git-scm.com/download/win).
- Run the installer and accept the defaults.
- Close and reopen your terminal, then re-run
	git --version
	to confirm.

- Configure your Git identity so every commit is stamped with your name and email. In your terminal, run these commands once, replacing the placeholders:

```bash
git config --global user.name ""
git config --global user.email ""
```

> 💡 Why configure name and email?
> 
> Git
> 
> attaches your name and email to every commit so your vault's history shows who made each change. Even on a solo repo, this stamps your authorship on
> 
> GitHub
> 
> and makes your contribution graph light up.

With Git ready, you'll create an empty

GitHub

repo as the remote destination, then initialize your vault locally and push it up.

- Go to [github.com/new](https://github.com/new).
- Under **Owner**, select your own
	GitHub
	account from the dropdown.
- Name the repository
	second-brain
	.
- Add a **Description**, like
	My AI second brain vault, synced with Claude Code
	.
- Set visibility to **Private**.
- Leave **Add a README**, **Add.gitignore**, and **Choose a license** all unchecked. You want an empty repo to push into.
- Click **Create repository**.

![The GitHub new repository form with second-brain entered as the name and Private selected](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-github-new-repository-form-with-second-brain-entered-as-the-name-and-private-selected1776787204922.webp)

The GitHub new repository form with second-brain entered as the name and Private selected

> 💡 Why private?
> 
> Your vault holds your notes, priorities, and half-formed ideas. You want that backed up, but not world-readable. Private repos are free on
> 
> GitHub
> 
> and keep your second brain yours.

Now that the empty remote is waiting, swing back to your terminal to add a

.gitignore

and push your first commit. Before the first commit, tell Git which files to skip. Some files inside your vault are device-specific noise that would only cause merge conflicts across machines.

- Still in your terminal, move into your vault and create the
	.gitignore
	file:

```bash
cd ~/Documents/second-brain
touch .gitignore
```

- Open
	.gitignore
	in your default text editor:

```bash
open -e .gitignore
```

The

\-e

flag opens the file in TextEdit.

```bash
notepad .gitignore
```

This opens the file in Notepad.

```bash
nano .gitignore
```

Or swap

nano

for your preferred terminal editor.

- Paste in:

```js
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
```

- Save the file (**Cmd+S**) and close the editor window.

> 💡 What are we excluding?
> 
> **.obsidian/workspace.json**
> 
> and**
> 
> .obsidian/workspace-mobile.json
> 
> **save your personal Obsidian layout, like which notes are open, how your panes are arranged, and where your cursor is. That's specific to the device you're on, so syncing it would overwrite your layout every time you switched machines.
> 
> **.trash/**
> 
> is Obsidian's recycling bin for deleted notes. Pushing it to GitHub would save every deleted note forever, which defeats the point of deleting them.

- Initialize your vault as a Git repo and make your first commit. In your terminal, run these commands one at a time from inside your
	second-brain
	vault directory (
	cd ~/Documents/second-brain
	):

```bash
cd ~/Documents/second-brain
git init
git add .
git commit -m "Initial vault backup"
```

- Go back to your
	second-brain
	repo page on
	GitHub
	and copy the commands under **…or push an existing repository from the command line**.

![GitHub Quick setup page with push existing repository section highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/github-empty-repo-quick-setup-page-with-the-push-an-existing-repository-from-the-command-line-section-highlighted1776791144860.webp)

GitHub Quick setup page with push existing repository section highlighted

- Paste them into your terminal and run them.

![Terminal showing git push output with the vault pushed successfully to the main branch](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/terminal-showing-git-push-output-with-the-vault-pushed-successfully-to-the-main-branch1776791188174.webp)

Terminal showing git push output with the vault pushed successfully to the main branch

- Refresh your GitHub repo page to confirm your files are there. You should see
	CLAUDE.md
	,
	raw/
	,
	wiki/
	, and
	.claude/commands/
	.

![GitHub repo page showing CLAUDE.md, raw, wiki, and .claude folders in the second-brain repository](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/github-repo-page-showing-claudemd-raw-wiki-and-claude-folders-in-the-second-brain-repository1776791254378.webp)

GitHub repo page showing CLAUDE.md, raw, wiki, and.claude folders in the second-brain repository

> 💡 Why two sets of commands?
> 
> Pushing a vault to
> 
> GitHub
> 
> takes two parts.
> 
> **Part 1 (local):**
> 
> git init
> 
> ,
> 
> git add.
> 
> , and
> 
> git commit
> 
> turn your
> 
> second-brain
> 
> vault into a
> 
> Git
> 
> repo on your laptop and save your first snapshot. None of this touches
> 
> GitHub
> 
> .
> 
> **Part 2 (GitHub):**
> 
> git remote add origin
> 
> links your local repo to your empty
> 
> GitHub
> 
> repo, and
> 
> git push
> 
> uploads the snapshot. This is the part that actually sends your vault to the cloud.
> 
> 🙋♀️ **Getting an authentication error?**
> 
> GitHub no longer accepts password login on the command line. You need a
> 
> personal access token
> 
> or
> 
> SSH
> 
> key instead. How do I set this up?
> 
> 🙋♀️ **Seeing**
> 
> **remote origin already exists**
> 
> **or
> 
> Repository not found
> 
> ?**
> 
> You probably ran the commands once with a typo or before filling in your username, which saved a broken remote URL. Replace it (don't re-add it) and try pushing again:
> 
> ```bash
> git remote set-url origin https://github.com//second-brain.git
> git push -u origin main
> ```

#### 📸 Take a screenshot of your GitHub second-brain repository showing your vault files after the initial push.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

**Set Up Auto-Sync with Obsidian Git**

Pushing once is nice. Pushing every 10 minutes, forever, without thinking about it, is the real win. That's what the

Obsidian Git

plugin does. It runs

Git

from inside

Obsidian

on a schedule, so every edit you make flows up to

GitHub

automatically.

- Open
	Obsidian
	with your
	second-brain
	vault.
- Go to **Settings** (the gear icon in the bottom left).

![Obsidian sidebar showing the Settings gear icon in the bottom left](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791319883.webp)

Obsidian sidebar showing the Settings gear icon in the bottom left

- Click **Community plugins** in the left sidebar.

![Obsidian Settings panel with Community plugins highlighted in the left sidebar](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791326917.webp)

Obsidian Settings panel with Community plugins highlighted in the left sidebar

- If this is your first community plugin, click **Turn on community plugins**.

![Obsidian Community plugins page with the Turn on community plugins button](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791331635.webp)

Obsidian Community plugins page with the Turn on community plugins button

- Click **Browse**.

![Obsidian Community plugins page with the Browse button highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791336479.webp)

Obsidian Community plugins page with the Browse button highlighted

- Search for
	Git
	.
- Select the **Git** plugin by **Vinzent** (also listed as Denis Olehov).
- Click **Install**, then click **Enable**.

![The Obsidian community plugins browser showing the Git plugin by Vinzent highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-obsidian-community-plugins-browser-showing-the-git-plugin-by-vinzent-highlighted1776791360923.webp)

The Obsidian community plugins browser showing the Git plugin by Vinzent highlighted

- Quit
	Obsidian
	fully and reopen it. The Git plugin adds a **Source Control** icon to Obsidian's left ribbon (the vertical toolbar on the far left of the window), and it only shows up after a restart.
- Back in **Settings**, look for a new **Community plugins** section in the left sidebar (below **Core plugins**) with **Git** listed under it. Click **Git** to open its settings.
- Set **Auto commit-and-sync interval (minutes)** to
	10
	.

![Obsidian Git plugin settings showing the auto commit-and-sync interval set to 10 minutes](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791382293.webp)

Obsidian Git plugin settings showing the auto commit-and-sync interval set to 10 minutes

- Turn on **Auto commit-and-sync after stopping file edits**.
- Turn on **Pull on startup**.

![Obsidian Git plugin settings with the Pull on startup toggle enabled](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776791413454.webp)

Obsidian Git plugin settings with the Pull on startup toggle enabled

- Turn on **Push on commit-and-sync**.

![The Obsidian Git plugin settings panel with the 10-minute interval and the three toggles enabled](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-obsidian-git-plugin-settings-panel-with-the-10-minute-interval-and-the-three-toggles-enabled1776791420776.webp)

The Obsidian Git plugin settings panel with the 10-minute interval and the three toggles enabled

> 💡 What does each setting do?
> 
> Auto commit-and-sync interval
> 
> is how often the plugin commits and pushes on its own.
> 
> Stopping file edits
> 
> triggers a sync a few seconds after you stop typing.
> 
> Pull on startup
> 
> grabs any changes from another machine when you open Obsidian.
> 
> Push on commit-and-sync
> 
> makes sure every commit also reaches
> 
> GitHub
> 
> .

- Test the plugin. Open any note in your vault and add a small change (a new heading works fine). Save the note.
- Press **Cmd+P** (macOS) or **Ctrl+P** (Windows) to open the command palette.
- Type
	Git: Commit and sync
	and select it.

![The Obsidian command palette with Git: Commit and sync selected](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-obsidian-command-palette-with-git-commit-and-sync-selected1776791434244.webp)

The Obsidian command palette with Git: Commit and sync selected

- Refresh your GitHub repo page.

#### 📸 Take a screenshot of a GitHub commit made automatically by the Obsidian Git plugin (not your initial manual push).

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

**Add a Connector**

Your vault is versioned and safe. Now let's give Claude a window into the world outside your vault.

MCP Connectors

are the bridge.

> 💡 What is an MCP Connector?
> 
> MCP
> 
> (Model Context Protocol) is an open standard
> 
> Claude Code
> 
> uses to connect to external tools. A Connector is one of those connections, letting Claude read live data from a tool you already use.

- In
	Claude Code Desktop
	, click the **+** icon next to the prompt box.
- Select **Connectors** from the menu that opens.

![The plus menu in Claude Code Desktop with the Connectors option highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-plus-menu-in-claude-code-desktop-with-the-connectors-option-highlighted1776791456061.webp)

The plus menu in Claude Code Desktop with the Connectors option highlighted

- A **Connectors** panel opens showing any Connectors you already have set up. Click **Add connectors** to browse the available tools.

![Claude Code Desktop Connectors panel with the Add connectors button highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-connectors-panel-with-the-add-connectors-button-highlighted1776791458313.webp)

Claude Code Desktop Connectors panel with the Add connectors button highlighted

- Scroll through the list and pick the tool you want to connect. Choose one that you actually use every day so Step 4's briefings have real material to pull from.

- In the **Connectors** list, click **Google Calendar**.
- Click **Connect**. A browser window opens.
- Sign in with the Google account that holds your calendar.
- Review the permissions Google asks for and click **Allow**.
- Return to
	Claude Code Desktop
	. The Google Calendar connector should now show as active.

![Claude Code Desktop showing Google Calendar connected with a green active indicator](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-showing-google-calendar-connected-with-a-green-active-indicator1776791462237.webp)

Claude Code Desktop showing Google Calendar connected with a green active indicator

- In the prompt box, run:

```js
What meetings do I have today?
```

- Wait for Claude's response. You should see your actual calendar events for today.

![Claude Code Desktop response listing today's real Google Calendar meetings](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-response-listing-todays-real-google-calendar-meetings1776791559993.webp)

Claude Code Desktop response listing today's real Google Calendar meetings

- In the **Connectors** list, click **Linear**.
- Click **Connect**. A browser window opens.
- Sign in to the Linear workspace you want to connect.
- Review the
	OAuth
	permissions Linear asks for and click **Allow**.
- Return to
	Claude Code Desktop
	. The Linear connector should now show as active.

![Claude Code Desktop showing Linear connected with a green active indicator](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-showing-linear-connected-with-a-green-active-indicator1776791466843.webp)

Claude Code Desktop showing Linear connected with a green active indicator

- In the prompt box, run:

```js
List my open Linear issues assigned to me.
```

- Wait for Claude's response. You should see a list of your actual Linear issues.

![Claude Code Desktop response listing open Linear issues assigned to the user](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-response-listing-open-linear-issues-assigned-to-the-user1776791636063.webp)

Claude Code Desktop response listing open Linear issues assigned to the user

- In the **Connectors** list, click **Notion**.
- Click **Connect**. A browser window opens.
- Sign in to Notion.
- Pick which pages or workspaces to share with Claude, then click **Allow access**.
- Return to
	Claude Code Desktop
	. The Notion connector should now show as active.

![Claude Code Desktop showing Notion connected with a green active indicator](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-showing-notion-connected-with-a-green-active-indicator1776791470371.webp)

Claude Code Desktop showing Notion connected with a green active indicator

- In the prompt box, run:

```js
List the Notion pages I've updated most recently.
```

- Wait for Claude's response. You should see your actual recent Notion activity.

- In the **Connectors** list, pick any other tool that you use every day (GitHub, Linear, Asana, and more may be available).
- Click **Connect**. A browser window opens.
- Sign in and grant the permissions the tool asks for.
- Return to
	Claude Code Desktop
	. The connector should now show as active.
- In the prompt box, ask Claude a question that only that tool could answer (for example, "List my open GitHub pull requests" or "What are my active Linear issues?").
- Wait for Claude's response. You should see real data from the connected tool.

> 🙋♀️ Connector stuck on "Connecting..."?
> 
> The
> 
> OAuth
> 
> window sometimes hides behind other apps. Check all your open browser tabs and windows. If you dismissed the window, click **Connect** again. Still not connecting?

#### 📸 Take a screenshot of Claude Code Desktop returning live data from the MCP Connector you just added.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### ✍️ Which Connector did you add, and what live data did Claude pull?

1/2

Your vault is versioned, synced, and plugged into your real-world tools. Next up, you'll tell Claude what actually matters to you by writing a priorities document.

✨ Step #3

### Auto-Ingest Your Sources

Your vault is backed up and

Claude Code

can reach your tools live through

MCP

Connectors. But reach is read-only. Every briefing still starts with a cold vault unless you drop fresh notes into

raw/

yourself, which is exactly the copy-paste grind a second brain is supposed to replace.

So here's the missing piece: a

slash command

that captures from your real sources on demand and hands them straight to

/ingest

. That's what takes your

wiki

from "something you maintain" to "something that maintains itself."

**In this step, get ready to:**

#### ✍️ What are we doing in this step, and why does auto-ingesting your sources make a bigger difference than just having more MCP Connectors?

> 💡 How much does this step cost?
> 
> Both
> 
> /pull-sources
> 
> and
> 
> /ingest
> 
> run through your
> 
> Claude Code
> 
> subscription (Pro, Max, Team, or Enterprise), not a separate API bill. They spend against your plan's usage limit.
> 
> **/pull-sources**
> 
> is light. It mostly reads local files and MCP data, then writes Markdown. Minimal reasoning, minimal tokens.
> 
> **/ingest**
> 
> is heavier. Claude reads every file in
> 
> raw/
> 
> , dedupes, cross-references, and writes new wiki pages. Expect it to eat a noticeable chunk of your daily quota, especially the first run when
> 
> raw/
> 
> is full. You can always track your usage from inside
> 
> Claude Code Desktop
> 
> under **Settings** > **Usage**. Worried about hitting your plan limit?

**Build /pull-sources**

Slash commands

are just Markdown files in

.claude/commands/

. You'll write one that spells out where to look, what to write, and how to hand off to

/ingest

. Before you paste the prompt, skim the sources you're starting with so you know what the command is reaching into. You can add more later.

> 💡 Pull what you'll read, not what's available
> 
> Every file your command pulls becomes a file
> 
> /ingest
> 
> processes, a
> 
> wiki
> 
> page it might create, and context a future
> 
> /briefing
> 
> might read. The default posture here is selective, not greedy. When you set up each source below, pick a realistic volume cap and name what to skip. Widening the net later is easy; shrinking a bloated wiki is hard.
> 
> 💡 **Let Claude tailor this command to your tools**
> 
> Rather than filling in placeholders yourself, the prompt below asks
> 
> Claude Code
> 
> to interview you about which sources you want (your
> 
> MCP Connectors
> 
> , local folders, or anything else), then writes a
> 
> /pull-sources
> 
> command that matches. That way the file reflects the tools you actually live in.

- Open
	Claude Code Desktop
	with your
	second-brain
	vault selected.
- Paste this prompt into the chat and press **Enter**:

```js
Create .claude/commands/pull-sources.md that pulls fresh material from my real-world sources into raw/ and then suggests /ingest.

Before writing the file, interview me:

1) Ask which sources I want beyond Claude Code sessions. Offer Gmail, Granola, Linear, Notion, a local folder, or anything else I name.

2) For each source I pick, confirm:
   - where it lives (the MCP Connector name, or a local file path)
   - what to pull (e.g. last 7 days of messages, meeting transcripts, issues, pages, files)
   - a volume cap so runs stay lean (e.g. max 20 items per run, top 10 most recent, no more than 5 per sender)
   - an include filter (e.g. only emails where I am in To or Cc, only meetings longer than 10 minutes, only Linear issues assigned to me or mentioning my name)
   - an exclude filter (e.g. skip noreply and automation emails, skip calendar notifications, skip meetings titled "Daily Standup", skip Linear issues already in Done)
   - naming pattern for the Markdown files (e.g. date-sender-subject in kebab-case)
   - YAML frontmatter keys to include beyond source and captured (e.g. thread_id, meeting_title, issue_id)

Once I've answered, write pull-sources.md so the command:

- Always includes Claude Code sessions as source 1: read JSONL files from the last 7 days in ~/.claude/projects/ (all subdirectories), apply the cap and filters I chose, write one Markdown file per session to raw/claude-sessions/ named by session start date and a short auto-generated slug, YAML frontmatter: source (claude-code), captured (ISO date), session_id.
- Adds one block per additional source I confirmed. Each block pulls the last 7 days of items, then applies the volume cap and include/exclude filters BEFORE anything is written to raw/<source-slug>/. Use YAML frontmatter with source, captured (ISO date), and my chosen keys. If a source is missing or not configured, skip that block and print a one-line note.
- Writes the cap and filter rules as explicit instructions inside each source block (not as comments), so a future me reading the file can see exactly what gets pulled and what gets skipped.
- Skips files that already exist in raw/ (match by source plus id) so reruns do not duplicate material.
- At the very top of every file written to raw/, above the YAML frontmatter, writes a one-line triage header in the format: \`> <source>: <who or what>, <subject or title>. <one-sentence summary of what's inside>.\` This header exists so a future me can skim raw/ in Obsidian's preview pane and decide what to keep before running /ingest.
- After all sources finish, appends a single timestamped entry to wiki/log.md noting how many files landed per source and how many were filtered out.
- Ends by reminding me to triage raw/ first (skim the headers, delete anything I don't want) and then run /ingest on what's left.

Leave a clearly labelled comment block at the end titled "# Add your own source here" with a scaffolded block showing the full selective-ingestion shape: read from path, volume cap, include filter, exclude filter, write to raw/<source>/, frontmatter keys, dedupe check. Do not add a real extra source yet.

Ask me to approve the file before writing.
```

- Answer
	Claude Code
	's questions about your sources. It will confirm the locations, naming patterns, and frontmatter keys it plans to use.
- When
	Claude Code
	is ready to create the file, a permission dialog appears asking **Allow Claude to write pull-sources.md?**. Click **Allow once** (or **Always allow** if you plan to let Claude manage this file going forward).

![Permission dialog asking to allow writing pull-sources.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-permission-dialog-asking-to-allow-writing-pull-sourcesmd-with-deny-allow-once-and-always-allow-buttons1776795498781.webp)

Permission dialog asking to allow writing pull-sources.md

- Open
	.claude/commands/pull-sources.md
	and skim the file.
	Obsidian
	hides the
	.claude/
	folder by default (anything starting with a dot), so open it from your terminal instead:

```bash
open -e ~/Documents/second-brain/.claude/commands/pull-sources.md
```

```bash
notepad %USERPROFILE%\Documents\second-brain\.claude\commands\pull-sources.md
```

```bash
nano ~/Documents/second-brain/.claude/commands/pull-sources.md
```

- Each source should have its own block, and the **Add your own source here** comment block should sit at the bottom.

![pull-sources.md in Obsidian showing Claude sessions, Gmail, Granola blocks](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-pull-sourcesmd-slash-command-open-in-obsidian-showing-blocks-for-claude-sessions-gmail-granola-and-the-add-your-own-source-placeholder1776795506103.webp)

pull-sources.md in Obsidian showing Claude sessions, Gmail, Granola blocks

> 💡 Why write a command instead of pulling sources in-session?
> 
> A
> 
> slash command
> 
> gives you one repeatable step you can run in 3 seconds, schedule later, or call from another command. Pulling sources inline means rewriting the same prompt every morning and getting a slightly different answer each time.
> 
> 🙋♀️ **Only want one or two sources?**
> 
> Open
> 
> .claude/commands/pull-sources.md
> 
> in
> 
> Obsidian
> 
> and delete the source blocks you do not want. The file is a plain Markdown prompt, so deleting a block just removes that source from the run. Need help trimming it?
> 
> 🙋♀️ **Pulled too much (or missed things) on the first run?**
> 
> That is the signal to tune, not to accept the noise. Open
> 
> .claude/commands/pull-sources.md
> 
> and adjust the volume cap or filters on the source that over-pulled or under-pulled. Shrinking the cap, adding an exclude rule, or tightening the include filter changes what the next run captures. Walk me through tuning filters.

#### 📸 Take a screenshot of.claude/commands/pull-sources.md open in Obsidian showing your source blocks and the 'Add your own source here' placeholder.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### ✍️ Which source are you most excited to auto-ingest, and what would you add in the 'Add your own source here' block first?

1/2

**Run /pull-sources and Verify**

Running the command end-to-end is where the "second brain captures itself" story stops being theoretical. You want to see new files land in

raw/

, then watch

/ingest

turn them into real

wiki

pages.

- Close your current
	Claude Code Desktop
	session so it picks up the new command.
- Open a fresh session pointed at your
	second-brain
	vault.

![Fresh Claude Code Desktop session pointed at the second-brain vault](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776795600836.webp)

Fresh Claude Code Desktop session pointed at the second-brain vault

- Type
	/pull-sources
	and press **Enter**.
- Approve each file write when
	Claude Code
	asks (you are still on **Ask permissions**).
- Wait for
	Claude Code
	to report how many files landed per source. This usually takes **5 to 10 minutes** depending on how many sources you connected and how much material is in each one.

![Claude Code Desktop finishing a /pull-sources run and reporting per-source file counts in wiki/log.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-finishing-a-pull-sources-run-and-reporting-per-source-file-counts-in-wikilogmd1776798058245.webp)

Claude Code Desktop finishing a /pull-sources run and reporting per-source file counts in wiki/log.md

- Switch to
	Obsidian
	and open the
	raw/
	folder.
- Confirm the new subfolders exist where sources landed:
	raw/claude-sessions/
	, plus
	raw/gmail/
	if Gmail was connected, plus
	raw/granola/
	if Granola was present.
- Open one file from each subfolder and confirm it has the
	YAML frontmatter
	your prompt specified.

![Raw folder in Obsidian with claude-sessions, gmail, granola subfolders populated](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-raw-folder-in-obsidian-showing-claude-sessions-gmail-and-granola-subfolders-populated-with-new-markdown-files1776798108331.webp)

Raw folder in Obsidian with claude-sessions, gmail, granola subfolders populated

**Triage Before You Ingest**

/pull-sources

was deliberately permissive. It captured everything that passed your filters, even if half of it isn't worth keeping long term. This is where you decide.

Every pulled file starts with a one-line triage header at the very top, above the YAML frontmatter. You don't have to open each file to know what's inside, just skim the headers in

Obsidian

's preview pane and delete what doesn't earn a place in your

wiki

.

- Open
	raw/
	in
	Obsidian
	.
- Click through each source subfolder (
	raw/claude-sessions/
	,
	raw/gmail/
	,
	raw/granola/
	, and any others you configured).
- For each file, skim the triage header. If it's noise, a duplicate, or something you wouldn't want surfacing in a morning brief, right-click and **Delete**.
- Only the files you want promoted should be left in
	raw/
	before you run
	/ingest
	.

> 💡 Why triage before /ingest, not after?
> 
> /ingest
> 
> pays
> 
> tokens
> 
> to read every file it processes. Triaging beforehand means
> 
> /ingest
> 
> never sees the noise, so your token cost scales with signal, not volume. Letting
> 
> /ingest
> 
> promote everything and then pruning the
> 
> wiki
> 
> later costs you twice: once to read the noise, then again to clean it up.
> 
> 💡 **Why you, not Claude?**
> 
> Claude Code
> 
> can filter by the rules you wrote into
> 
> /pull-sources
> 
> (volume caps, include, exclude), but it can't tell that yesterday's flurry of messages about a launch matters while last Tuesday's "sync cancelled" calendar notice does not. That judgement is yours, and it takes about 30 seconds a day. Noise in
> 
> raw/
> 
> becomes bloat in
> 
> wiki/
> 
> becomes cost in every future
> 
> /briefing
> 
> . Catching it here is the cheapest place in the pipeline.

Now let

/ingest

do its job and watch the wiki grow.

- Back in
	Claude Code Desktop
	, run
	/ingest
	.
- Approve proposed
	wiki
	pages as
	Claude Code
	promotes the raw material.
- Open
	wiki/
	in
	Obsidian
	and confirm new or updated pages appear: concepts from your sessions, people from your emails, meetings from your Granola transcripts.

![Wiki folder in Obsidian after /ingest runs with updated pages](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-wiki-folder-in-obsidian-after-ingest-runs-showing-new-or-updated-pages-grounded-in-material-from-the-auto-pulled-sources1776798117186.webp)

Wiki folder in Obsidian after /ingest runs with updated pages

> 💡 What about scheduling /pull-sources?
> 
> /pull-sources
> 
> reads local files (Claude sessions, Granola transcripts), so it has to run on your machine, not the cloud. You'll wire your morning
> 
> Cloud Routine
> 
> to
> 
> /briefing
> 
> in the final step. If you want
> 
> /pull-sources
> 
> to run on its own schedule too, set it up as a
> 
> Desktop scheduled task
> 
> after you finish the project.
> 
> 🙋♀️ **/pull-sources ran but raw/ is empty?**
> 
> Check that
> 
> permission mode
> 
> is set to **Ask permissions** rather than **Plan**. Plan mode proposes writes without making them. Also confirm the source paths exist on your OS (Granola's path is different on Windows). Walk me through this.

#### 📸 Take a screenshot of your raw/ folder populated by /pull-sources alongside your wiki/ folder updated by /ingest.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

Your vault now captures itself on your terms. Every time you run

/pull-sources

, your sessions, inbox, and meetings flow into

raw/

. You triage in 30 seconds,

/ingest

promotes the survivors into

wiki/

, and future briefings get smarter without you copy-pasting a thing or paying tokens on noise you didn't want. Next up, you'll write the priorities.md file that tells Claude what to actually focus on when it reads all that fresh context.

📝 Step #4

### Create Your Priorities Document

Your vault captures itself now.

Claude Code

sessions, inbox threads, meeting transcripts and more all flow into

raw/

on demand, and

/ingest

promotes them into

wiki/

. But a vault full of context is still not a vault that knows what you care about. If you asked Claude Code for a morning briefing right now, it would pull every event, every unread thread, and every scrap of context it could find, with no way to tell what actually matters to you this week.

So what does your AI second brain still need? A steering wheel. A place where you write down your real priorities so Claude can ground its briefings in what matters right now, not just what's noisy.

In this step, you'll create priorities.md with five sections that give Claude a clean way to separate deadlines from long-term responsibilities from background context.

**In this step, get ready to:**

#### ✍️ What are we doing in this step, and why does your AI assistant need a priorities document before it can generate useful briefings?

**Create priorities.md**

- Open
	Claude Code
	Desktop with your
	second-brain
	vault.
- Paste this prompt into the chat:

```js
Create priorities.md at the vault root (next to CLAUDE.md) with these five sections in this order:

## Projects
Short-term efforts with a clear end state. 2-5 bullets. Each one should have a deliverable and a target date.

## Areas
Ongoing responsibilities I maintain, no end date. One-line each.

## Resources
Topics I'm actively learning or reference for my work. One-line each.

## Archive
Projects and Areas I've completed or paused. Leave empty if I'm starting fresh.

## Key People
People I interact with most and the context I need about each (role, current focus, how they relate to a Project or Area). One-line each.

Ask me 3-4 short questions about my current work before writing so each section reflects real priorities, not generic placeholders. At the top of the file, include a brief comment block that tells me to edit this file weekly: update Projects and Key People, move completed items to Archive.
```

- Answer Claude's follow-up questions honestly. Vague answers produce a vague file, so be specific. "Ship the v2 launch by Friday" gives Claude a concrete target. "Work on the product" gives Claude nothing.
- Approve the file creation when Claude proposes the final
	priorities.md
	.
- Open
	priorities.md
	in
	Obsidian
	and review all five sections. Edit anything directly in Obsidian if a priority is off.

![priorities.md in Obsidian with Projects, Areas, Resources, Archive, Key People sections](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/prioritiesmd-open-in-obsidian-showing-the-five-sections-projects-areas-resources-archive-and-key-people-filled-in1776893965073.webp)

priorities.md in Obsidian with Projects, Areas, Resources, Archive, Key People sections

> 💡 Why isn't this a wiki page?
> 
> In Part 1, you built
> 
> raw/
> 
> and
> 
> wiki/
> 
> . Claude owns the wiki. It writes and rewrites pages there every time you run
> 
> /ingest
> 
> . priorities.md is different. **You** write and maintain it, and Claude only reads it for context. That's why it sits at the vault root next to CLAUDE.md, not inside
> 
> wiki/
> 
> .
> 
> Keep it fresh by editing in place (not by creating a new file each week). Do a weekly review on Monday to refresh Projects and Key People, move anything finished into Archive, and adjust mid-week if a priority flips.
> 
> Obsidian Git
> 
> auto-syncs the change within 10 minutes, and the
> 
> wiki
> 
> captures history through
> 
> /ingest
> 
> and
> 
> /debrief
> 
> , so
> 
> priorities.md
> 
> only needs to reflect the present.

#### 📸 Take a screenshot of your priorities.md open in Obsidian showing all four sections filled in.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### ✍️ What is the most specific priority you wrote, and why does specificity matter for Claude's briefings?

1/2

**Update CLAUDE.md to Reference priorities.md**

Your

priorities.md

exists, but

Claude Code

does not know to read it yet. Time to wire it in so every

slash command

you build next grounds itself in your

Domain Context

.

- Back in Claude Code Desktop, paste this prompt:

```js
Update CLAUDE.md's Project Structure section in TWO places:

1. Add \`priorities.md\` as a new line inside the ASCII tree diagram itself, at the vault root level (alongside \`raw/\`, \`wiki/\`, \`journal/\`, \`content/\`). Use the same spacing and comment style as the existing tree entries, with a short comment like "# User-maintained priorities (read at start of /briefing and /debrief)".

2. Add a new bullet to the description list below the tree, matching the style of the existing bullets: "priorities.md is the user's priorities file at the vault root. It contains Projects (short-term deliverables with target dates), Areas (ongoing responsibilities), Resources (topics for reference), Archive (completed or paused items), and Key People. Read this file at the start of every /briefing and /debrief. Prioritise signals tied to Projects and Areas; use Resources for background context; skip anything in Archive."

Both updates must land inside the Project Structure section, not elsewhere in the file. Do not modify any other section.
```

- Approve the edit when Claude proposes it.
- Open
	CLAUDE.md
	in
	Obsidian
	and scroll to the Project Structure section. You should see
	priorities.md
	**inside the tree diagram** alongside
	raw/
	,
	wiki/
	,
	journal/
	, and
	content/
	, **and** a matching bullet below the tree with the read instruction.

![CLAUDE.md in Obsidian with priorities.md added to Project Structure tree](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claudemd-open-in-obsidian-with-the-project-structure-tree-diagram-showing-prioritiesmd-added-inside-the-tree-alongside-raw-wiki-journal-and-content-plus-a-matching-description-bullet-below-the-tree1776894105053.webp)

CLAUDE.md in Obsidian with priorities.md added to Project Structure tree

> 💡 What should I see?
> 
> Two things should be updated inside Project Structure. First,
> 
> priorities.md
> 
> should appear **inside the ASCII tree diagram** at the vault root level, alongside
> 
> raw/
> 
> ,
> 
> wiki/
> 
> ,
> 
> journal/
> 
> , and
> 
> content/
> 
> . Second, a **new bullet** should sit below the tree with the read instruction. If only the bullet got added and the tree is untouched, Claude did half the job, reprompt it.
> 
> 🙋♀️ **Claude only added the bullet, not the tree entry?**
> 
> This is the most common miss. Ask Claude Code to fix it.
> 
> 🙋♀️ **Claude put the line in the wrong section?**
> 
> If Claude dropped the reference somewhere outside Project Structure, move it yourself in Obsidian or re-prompt Claude to fix it. Ask Claude Code for help.

Your priorities document is alive and Claude knows where to find it. Next up, you'll build the two

slash commands

that turn it into a daily operating system.

🚀 Step #5

### Build and Run Your Daily Loop

Your

priorities.md

is in place and your

MCP

Connectors are wired up. Now it's time to turn that groundwork into a daily operating system: a morning

slash command

that hands you your day, an evening

slash command

that captures what happened, and one full run of the loop end-to-end to prove it actually works.

But what actually makes a

slash command

, and how does

Claude Code

know to read your

priorities.md

before generating anything?

**In this step, get ready to:**

#### ✍️ What are we doing in this step, and why does running the full briefing + debrief loop matter more than building each command in isolation?

**Build and Test /briefing**

Slash commands

in

Claude Code

are just Markdown files living in

.claude/commands/

. When you type

/briefing

,

Claude Code

reads the matching

briefing.md

file and runs it as a prompt. That means you can spec out your morning brief in plain English and Claude will execute it every time.

- Open
	Claude Code Desktop
	.
- In the left sidebar, click the **Code** tab.
- Select **Local** as your environment, then click **Select folder** and pick your
	second-brain
	vault (for example,
	~/Documents/second-brain
	). Click **Open**.
- Set the permission mode to **Ask permissions**.
- In the session toolbar above the prompt box, make sure **worktree** is **NOT** selected. You want the plain
	second-brain
	project active, not an isolated worktree copy, because this session will write a real file into your vault.
- Paste this prompt into
	Claude Code
	:

```markdown
Create .claude/commands/briefing.md that:

1) Reads priorities.md for my current focus.
2) Checks today's calendar (via the MCP Connector if configured; otherwise skip this section).
3) Scans wiki/log.md for the last 3 entries.
4) Reads wiki pages related to my active projects.
5) Generates a brief with sections: Today's Schedule, Active Threads, Priority Reminders, Suggested Actions.
6) Appends a timestamped entry to wiki/log.md noting the briefing ran.
```

- Press **Enter**.
- Claude Code
	will show a permission prompt asking **"Allow Claude to write briefing.md?"** with the file path
	.claude/commands/briefing.md
	inside your
	second-brain
	vault.
- Click **Allow once** (or press
	⌘↵
	on macOS /
	Ctrl+Enter
	on Windows) to approve the file creation.

![Permission prompt asking to allow Claude to write briefing.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-permission-prompt-asking-allow-claude-to-write-briefingmd-with-deny-and-allow-once-buttons1776894139671.webp)

Permission prompt asking to allow Claude to write briefing.md

> 💡 What is a slash command doing under the hood?
> 
> When you type
> 
> /briefing
> 
> ,
> 
> Claude Code
> 
> looks in
> 
> .claude/commands/
> 
> for a file named
> 
> briefing.md
> 
> . It reads the whole file as a prompt and runs it, just like you had pasted the instructions in manually. The filename becomes the command name, and any extra text you type after the command is passed in via
> 
> $ARGUMENTS
> 
> .

- Fully quit
	Claude Code Desktop
	. Closing the window is not enough, the app keeps running in the background.
- Reopen
	Claude Code Desktop
	from your **Applications** folder (macOS) or **Start** menu (Windows).
- In the left sidebar, click the **Code** tab.
- Select **Local** as the environment.
- Click **Select folder** and pick your
	second-brain
	vault at
	~/Documents/second-brain
	, then click **Open**.
- Set the permission mode to **Ask permissions**.
- In the session toolbar above the prompt box, confirm **worktree** is **NOT** selected.
- Type
	/briefing
	and press **Enter**.

![/briefing output with Schedule, Threads, Reminders, and Suggested Actions sections](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-showing-the-briefing-command-output-with-todays-schedule-active-threads-priority-reminders-and-suggested-actions-sections1776894152547.webp)

/briefing output with Schedule, Threads, Reminders, and Suggested Actions sections

> 💡 Why fully quit and reopen?
> 
> Claude Code Desktop
> 
> scans
> 
> .claude/commands/
> 
> when the app launches, not when you start a new session. Opening a new session in the same app won't pick up
> 
> briefing.md
> 
> . A full quit-and-reopen is the only way
> 
> /briefing
> 
> becomes callable.

- Open
	wiki/log.md
	in
	Obsidian
	and scroll to the bottom.
- Confirm there's a new timestamped entry noting the briefing ran.

![wiki/log.md in Obsidian showing a new timestamped entry logging that /briefing ran](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/wikilogmd-in-obsidian-showing-a-new-timestamped-entry-logging-that-briefing-ran1776894187976.webp)

wiki/log.md in Obsidian showing a new timestamped entry logging that /briefing ran

> 🙋♀️ The /briefing command doesn't appear?
> 
> Slash commands
> 
> only load when
> 
> Claude Code Desktop
> 
> launches. Fully quit the app (not just the session) and reopen it. Also confirm the file lives at exactly
> 
> .claude/commands/briefing.md
> 
> in your vault root. Still not showing up?

#### 📸 Take a screenshot of your /briefing command output showing the generated morning brief.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

**Build and Test /debrief**

/briefing

is a one-shot read that hands you context.

/debrief

is different. It's a conversation. It asks you a few short questions, writes a structured entry to your

wiki

, and can propose updates to other pages before making changes. Because the prompt is bigger, you'll have

Claude Code Desktop

write the command file for you.

- In
	Claude Code Desktop
	, confirm your vault project is selected.
- Paste this prompt into the chat and press **Enter**:

```markdown
Create .claude/commands/debrief.md that:

1) Reads priorities.md for today's focus.
2) Asks me 3-4 short questions one at a time: What did you accomplish? What conversations mattered? Did priorities shift? Any ideas to capture?
3) Writes a structured entry to wiki/log.md with a timestamp and "type: debrief" tag. The entry must be 3 to 5 bullets of signal only: what shifted, what blocked, what to carry forward. Do not transcribe my answers. If I said something that is context but not signal, leave it out.
4) If answers mention existing wiki pages, update them. If something new surfaces, propose a new page but ask first.
5) If priorities shifted, suggest updates to priorities.md but ask first.
6) End with a one-line summary of the day.

$ARGUMENTS is optional. If provided, skip the questions and use $ARGUMENTS as a quick summary (still write it as 3 to 5 bullets of signal, not a raw paste).
```

- Claude Code
	will show a permission prompt asking **"Allow Claude to write debrief.md?"** with the file path
	.claude/commands/debrief.md
	inside your
	second-brain
	vault.
- Click **Allow once** (or press
	⌘↵
	on macOS /
	Ctrl+Enter
	on Windows) to approve the file creation.

![Permission prompt asking to allow Claude to write debrief.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-permission-prompt-asking-allow-claude-to-write-debriefmd-with-deny-and-allow-once-buttons1776894202098.webp)

Permission prompt asking to allow Claude to write debrief.md

> 💡 Why bullets, not transcripts?
> 
> wiki/log.md
> 
> is re-read by tomorrow's
> 
> /briefing
> 
> , and every briefing after that. Every line you write today is context you will keep paying for. A debrief that dumps everything you said is a debrief that turns your log into noise; a debrief that extracts 3 to 5 bullets of signal keeps the log worth re-reading. The point of the log is not to remember everything, it is to remember what matters.
> 
> 💡 **What makes /debrief different from /briefing?**
> 
> /briefing
> 
> is a one-shot read. It gathers context and hands it to you.
> 
> /debrief
> 
> is a two-way conversation. It asks questions, writes a structured log entry, can update multiple
> 
> wiki
> 
> pages, propose new ones, and suggest changes to
> 
> priorities.md
> 
> , all after checking with you first.

- Fully quit
	Claude Code Desktop
	and reopen it so
	/debrief
	loads (same steps as before: on macOS, **Claude → Quit Claude** or
	⌘Q
	; on Windows, right-click the Claude icon in the system tray and select **Quit**).
- Reopen
	Claude Code Desktop
	, load your
	second-brain
	vault (**Code** tab → **Local** →
	~/Documents/second-brain
	→ **Ask permissions** → worktree **OFF**).
- Type
	/debrief
	and press **Enter**.
- Answer Claude's questions one at a time. A sentence or two each is enough.

![Interactive /debrief flow confirming entry appended to wiki/log.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-running-the-interactive-debrief-flow-and-confirming-the-entry-was-appended-to-wikilogmd1776894214048.webp)

Interactive /debrief flow confirming entry appended to wiki/log.md

- Switch to
	Obsidian
	(in the dock or with
	⌘Tab
	on macOS /
	Alt+Tab
	on Windows).
- In the left-hand file explorer, expand the
	wiki/
	folder.
- Click
	log.md
	to open it.
- Scroll to the bottom of the file.
- Confirm the newest entry has three things: a timestamp at the top (e.g.
	2026-04-22 17:30
	), a
	type: debrief
	tag, and 3 to 5 bullets of signal (not a full transcript of your answers).

Now try the quick mode.

$ARGUMENTS

lets you skip the questions and pass a one-line summary straight through.

- In the same session (or a new one), run:

```bash
/debrief Shipped the onboarding redesign, 1:1 with Alex on Q3, need to revisit pricing
```

- Claude Code
	skips the questions and writes a second debrief entry from your summary.

![wiki/log.md in Obsidian showing interactive and quick debrief entries with timestamps](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/wikilogmd-in-obsidian-showing-both-the-interactive-debrief-entry-and-the-quick-debrief-entry-stacked-with-timestamps-and-type-debrief-tags1776894285365.webp)

wiki/log.md in Obsidian showing interactive and quick debrief entries with timestamps

- Confirm the quick entry also has a timestamp and
	type: debrief
	tag. Same structure as the interactive one, just faster to create.

> 🙋♀️ Debrief ran but wiki didn't update?
> 
> Check that your
> 
> permission mode
> 
> is set to **Ask permissions**, not Plan mode. Plan mode proposes changes without writing them, so
> 
> wiki/log.md
> 
> stays empty. Walk me through this.

#### 📸 Take a screenshot of wiki/log.md showing both a briefing entry and a debrief entry from your run.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### ✍️ When would you use the quick /debrief mode versus the interactive mode, and what kind of day calls for each?

1/2

**Confirm Everything Synced to GitHub**

You've just written new entries to

wiki/log.md

from both

/briefing

and

/debrief

. The

Obsidian Git

plugin should be pushing those changes to your

second-brain

repository automatically. A debrief that never syncs is worse than no system at all, so verify it one time now.

- Open a browser and go to [github.com](https://github.com/). Sign in if you're not already.
- Navigate to your
	second-brain
	repository. Either:
	- Go directly to \[\[[https://github.com/\[\[GITHUB\_USERNAME="enter\](https://github.com/\[\[GITHUB\_USERNAME=)\](https://github.com/\[\[GITHUB\_USERNAME=](https://github.com/[[GITHUB_USERNAME=%22enter]\(https://github.com/[[GITHUB_USERNAME=\)]\(https://github.com/[[GITHUB_USERNAME=)) your github username"\]\]/second-brain.
		- Or click your profile picture in the top-right, select **Your repositories**, and click
		second-brain
		in the list.

![GitHub profile dropdown showing Your repositories with the second-brain repo listed](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776894604644.webp)

GitHub profile dropdown showing Your repositories with the second-brain repo listed

- In the repository file list, click the
	wiki/
	folder, then click
	log.md
	to open it.

![GitHub repository file list showing the wiki folder with log.md inside](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776894634111.webp)

GitHub repository file list showing the wiki folder with log.md inside

- Confirm your latest briefing and debrief entries are at the bottom of the file, timestamped and tagged.

![The second-brain GitHub repository showing wiki/log.md with the latest briefing and debrief entries](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-second-brain-github-repository-showing-wikilogmd-with-the-latest-briefing-and-debrief-entries1776894628135.webp)

The second-brain GitHub repository showing wiki/log.md with the latest briefing and debrief entries

> 🙋♀️ No new commits on GitHub?
> 
> The
> 
> Obsidian Git
> 
> plugin syncs on a schedule, so your push may not have fired yet. To force a sync now, open the
> 
> Obsidian
> 
> command palette with **Cmd+P** (macOS) or **Ctrl+P** (Windows) and run **Git: Commit and sync**. Refresh GitHub. Still not pushing?
> 
> 💡 **Pro tip**: build the habit
> 
> The value compounds. After a week of daily briefings and debriefs, each debrief makes tomorrow's briefing smarter. Your
> 
> wiki
> 
> thickens with real context, your
> 
> priorities.md
> 
> stays honest, and
> 
> Claude Code
> 
> gets more useful every day.

#### 📸 Take a screenshot of your GitHub second-brain repository showing the latest commit including the briefing and debrief updates.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

Your daily operating system is live. Every morning

/briefing

hands you your day, every evening

/debrief

captures what happened, and everything syncs to

GitHub

automatically. Ready for a stretch? The Secret Mission hands

/briefing

over to a

Cloud Routine

so it runs on Anthropic's cloud every weekday, before you've even opened your laptop.

💎 SECRET MISSION

### Schedule Your Briefing as a Cloud Routine

Your daily loop works when you open

Claude Code

and run

/briefing

yourself. That's fine as a prototype, but a real operating system shouldn't need you to flip the switch every morning.

In this secret mission, you'll hand

/briefing

over to a

Cloud Routine

so it runs every weekday morning on Anthropic's cloud infrastructure, commits the brief to

wiki/log.md

, and syncs into your vault before you even open your laptop.

**In this secret mission, get ready to:**

#### 🤫 What are we doing in this secret mission, and why does moving /briefing from a manual command to an automated Cloud Routine turn your vault into a real operating system?

**Create Your Cloud Routine**

A

Cloud Routine

is a

scheduled task

that runs against a fresh clone of your

GitHub

repo on Anthropic's cloud infrastructure. You get two ways to create one. Pick whichever feels more natural for you.

- In
	Claude Code Desktop
	, click **Routines** in the left sidebar (below **New session**).

![The Routines page open in Claude Code Desktop with the New routine button visible](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-routines-page-open-in-claude-code-desktop-with-the-new-routine-button-visible1776894307872.webp)

The Routines page open in Claude Code Desktop with the New routine button visible

- Click **New routine** in the top-right. A dropdown appears with two options: **Local** (runs on this machine) and **Remote** (runs on Anthropic's cloud infrastructure against a clone of your
	GitHub
	repo).

![The New routine button expanded to show the Local and Remote dropdown options](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776894343578.webp)

The New routine button expanded to show the Local and Remote dropdown options

- Select **Remote**.

![New routine dropdown showing Local and Remote options with Remote highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-new-routine-dropdown-in-claude-code-desktop-showing-the-local-and-remote-options-with-remote-highlighted1776894318595.webp)

New routine dropdown showing Local and Remote options with Remote highlighted

A **New remote routine** form opens. Fill it in from top to bottom.

**Name the routine**

- In the **Name** field, type
	Morning briefing
	.

**Paste the prompt**

- In the prompt box below ("Describe what Claude should do in each session"), paste:

```js
Run the /briefing slash command against this repository. Read priorities.md, scan wiki/log.md, and read the wiki pages relevant to my active projects. Generate a morning briefing with Today's Schedule (from my calendar if the connector is available), Active Threads, Priority Reminders, and Suggested Actions. Append the full briefing as a new timestamped entry to wiki/log.md. Commit directly to the main branch and push. Do not create a branch or pull request. This is a personal vault, not a code review flow.
```

- Click the model selector (it defaults to **Opus 4.7 Adaptive**) and switch it to **Sonnet**.

> 💡 Why Sonnet for this routine?
> 
> /briefing
> 
> is a read-and-summarise task, not a deep-reasoning one. Sonnet is faster and cheaper than Opus while still handling this kind of work well. You'll run this routine every weekday, so the savings add up, and a faster model means the briefing lands in your vault sooner.

**Pick the repository**

Find the repository row. It has two buttons: **Select a repository** on the left (the GitHub icon) and **Set up** on the right.

![Repository row with Select a repository button and Set up button](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-repository-row-in-the-new-remote-routine-form-showing-the-select-a-repository-button-on-the-left-and-the-set-up-button-on-the-right1776959686236.webp)

Repository row with Select a repository button and Set up button

> 💡 Why two buttons?
> 
> Claude hasn't been authorised for your
> 
> second-brain
> 
> repo yet, so **Select a repository** on the left won't find it. **Set up** on the right is what kicks off the install.
> 
> Cloud Routines
> 
> clone your repo on Anthropic's infrastructure at run time, so this one-time authorisation is what grants that access. Install it now without leaving the flow.

**Open the install page**

- On the repository row, click **Set up** (on the right, not **Select a repository** on the left, which is for repos Claude already has access to).
- Your browser opens to
	https://github.com/apps/claude/installations/new
	. Sign in to
	GitHub
	if it asks.

**Pick the account**

- If GitHub shows an account picker (your personal account plus any organisations you belong to), click the account that owns your
	second-brain
	repo.

![The GitHub app install page showing the account picker with a personal account highlighted](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-github-app-install-page-showing-the-account-picker-with-a-personal-account-highlighted1776958218393.webp)

The GitHub app install page showing the account picker with a personal account highlighted

**Grant access to second-brain only**

- You land on the **Install & Authorize Claude** page. Confirm the header shows the right account (e.g.
	Install & Authorize on your personal account enter your github username
	). If it's wrong, go back and pick the right account.
- Under **for these repositories**, select **Only select repositories** (safer than **All repositories**).
- In the dropdown that appears, type
	second-brain
	and click it to select.
- Leave the **with these permissions** section alone. Those are the scopes Claude needs to clone your repo and commit back to it.

![Install and Authorize Claude page with second-brain repository selected](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-repository-access-section-with-only-select-repositories-chosen-and-second-brain-picked-from-the-dropdown1776958253048.webp)

Install and Authorize Claude page with second-brain repository selected

**Install & Authorize**

- Scroll to the bottom and click **Install & Authorize**.
- GitHub redirects you back to
	Claude Code Desktop
	. If the redirect doesn't happen, close the GitHub tab and switch back to the app manually.

**Return to the form and select the repo**

- Back in the **New remote routine** form, the repository row now has the **Select a repository** button on the left available (now that Claude has access). Click it.

![The Select a repository button now active on the repository row after GitHub app authorisation](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776960588243.webp)

The Select a repository button now active on the repository row after GitHub app authorisation

- In the search dropdown, type
	second-brain
	. It now appears in the list.
- Click it to select.

![The repository search dropdown showing second-brain in the list, ready to select](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776960542167.webp)

The repository search dropdown showing second-brain in the list, ready to select

> 🙋♀️ Still not showing up after install?
> 
> The dropdown sometimes caches an empty result right after an install. Close the **New remote routine** form (your draft is kept), reopen it from **Routines → New routine → Remote**, and try the search again. If it still isn't there, visit [github.com/settings/installations](https://github.com/settings/installations), click **Configure** on the Claude app, and confirm
> 
> second-brain
> 
> is listed under **Repository access**. Still stuck?

**Set the trigger**

- Under **Select a trigger**, click **Schedule** ("Run on a recurring cron schedule").

![The Select a trigger section with Schedule selected for a recurring cron schedule](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776961073168.webp)

The Select a trigger section with Schedule selected for a recurring cron schedule

- A cron input appears. Enter an expression that fires **2 minutes from your current time**.
- Example: if it's 15:42 on Tuesday, enter
	44 15 \* \* 2
	.

![The Schedule trigger cron input filled with an expression firing two minutes from now](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776961079953.webp)

The Schedule trigger cron input filled with an expression firing two minutes from now

> 💡 You'll change this later
> 
> After the test run works, you'll switch the cron to
> 
> 0 8 \* \* 1-5
> 
> (weekdays at 8am). Testing against 8am tomorrow means waiting until tomorrow to find out something's broken.

**Prune the connectors**

- Scroll to the **Connectors** section. By default, every
	MCP
	Connector from Step 2 is included.
- Click the **X** on any connector
	/briefing
	doesn't need.
- Keep your calendar connector (for Today's Schedule).
- Remove everything else (chat apps, docs, analytics).

![The Connectors section pruned to keep only the calendar connector for the briefing](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776961117390.webp)

The Connectors section pruned to keep only the calendar connector for the briefing

> 🚨 Why pruning connectors matters
> 
> Cloud Routines
> 
> run Claude with **write access to every included connector, without asking permission during the run**. A connector you forgot about can send emails, update tickets, or write to Linear on your behalf. It also burns
> 
> tokens
> 
> because every connector loads its tool definitions into the system prompt every run. Leave only what
> 
> /briefing
> 
> reads.

**Create**

- Click **Create** at the bottom of the form.

![Completed New remote routine form with Morning briefing name, prompt, repo, cron schedule, calendar connector](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-completed-new-remote-routine-form-with-name-set-to-morning-briefing-the-briefing-prompt-pasted-second-brain-repo-selected-schedule-trigger-with-a-cron-1-minute-in-the-future-and-connectors-trimmed-to-calendar-only1776961151815.webp)

Completed New remote routine form with Morning briefing name, prompt, repo, cron schedule, calendar connector

- In a
	Claude Code Desktop
	session pointed at your
	second-brain
	folder, type:

```js
/schedule
```

- Press **Enter**.
- When
	Claude Code
	asks what to schedule, describe the routine conversationally. Use a time **2 minutes from now** for this first test (you'll switch to a real morning time after confirming it works):

```js
Two minutes from now, run /briefing against this repo and append the result to wiki/log.md. Commit directly to the main branch and push. No branch, no PR.
```

- When prompted for the routine type, choose **remote** so it runs as a
	Cloud Routine
	without your machine on.
- Confirm the schedule when
	Claude Code
	repeats it back to you.

![Claude Code Desktop confirming new Cloud Routine scheduled two minutes from now](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-completed-new-remote-routine-form-with-name-set-to-morning-briefing-the-briefing-prompt-pasted-second-brain-repo-selected-schedule-trigger-with-a-cron-1-minute-in-the-future-and-connectors-trimmed-to-calendar-only1776961151815.webp)

Claude Code Desktop confirming new Cloud Routine scheduled two minutes from now

> 💡 Why a Cloud Routine, not a Desktop task?
> 
> Desktop
> 
> scheduled tasks
> 
> need your machine awake and
> 
> Claude Code
> 
> open to fire. A
> 
> Cloud Routine
> 
> runs on Anthropic's cloud infrastructure, cloning your
> 
> GitHub
> 
> repo on the schedule you picked. That is how the briefing lands in your vault before you are even awake.
> 
> 💡 **Where does the briefing actually go?**
> 
> The
> 
> Cloud Routine
> 
> commits the briefing to
> 
> wiki/log.md
> 
> and pushes to
> 
> GitHub
> 
> . When you open
> 
> Obsidian
> 
> , the
> 
> Obsidian Git
> 
> plugin pulls the latest commit and the new briefing appears at the bottom of your log, ready to read with your coffee.

#### 🤫 Take a screenshot of your Routines page in Claude Code Desktop showing the /briefing Cloud Routine with its schedule.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

**Watch the Routine Fire and Verify It Landed**

Because you set the schedule 2 minutes from your current time, the routine should fire on its own any second now. Watch it run end-to-end, then trace the briefing from Anthropic's cloud all the way into your

Obsidian

vault.

- Open the **Routines** page in the left sidebar and find your briefing routine.
- Wait for the status to flip from **scheduled** to **running**, then to **complete**. This usually takes 30 to 90 seconds.

![Claude Code Desktop showing the briefing routine status flip from scheduled to running to complete](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/claude-code-desktop-showing-the-briefing-routine-status-flip-from-scheduled-to-running-to-complete1776961182332.webp)

Claude Code Desktop showing the briefing routine status flip from scheduled to running to complete

> 💡 Don't want to wait? Fire it manually
> 
> If you'd rather trigger the routine right now instead of waiting the last few seconds, select the briefing routine on the **Routines** page and click **Run now**. Or run
> 
> /schedule run
> 
> in any
> 
> Claude Code Desktop
> 
> session and pick it from the list. Same result.

- Go to [github.com](https://github.com/) in your browser and sign in if you aren't already.
- Click your profile picture in the top-right and select **Your repositories**.
- In the repository search, type
	second-brain
	and click the repo in the results to open it.
- Confirm a new commit appears on
	main
	with an updated
	wiki/log.md
	.

![second-brain GitHub repo showing Cloud Routine commit appending briefing to wiki/log.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-second-brain-github-repo-showing-the-new-commit-from-the-cloud-routine-with-the-briefing-appended-to-wikilogmd1776963308715.webp)

second-brain GitHub repo showing Cloud Routine commit appending briefing to wiki/log.md

- Switch to
	Obsidian
	and wait a few seconds for
	Obsidian Git
	to pull.
- If nothing shows up, open the command palette with **Cmd+P** (macOS) or **Ctrl+P** (Windows) and run **Git: Commit and sync** to force a pull.
- Open
	wiki/log.md
	and scroll to the bottom.

![wiki/log.md open in Obsidian with today's Cloud Routine briefing as the newest entry](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/wikilogmd-open-in-obsidian-with-todays-cloud-routine-briefing-as-the-newest-entry1776963489893.webp)

wiki/log.md open in Obsidian with today's Cloud Routine briefing as the newest entry

The newest entry is today's briefing, generated automatically on Anthropic's infrastructure and synced into your vault without you lifting a finger.

> 🙋♀️ Routine ran but nothing appeared in my vault?
> 
> Check that the
> 
> Obsidian Git
> 
> plugin has **Pull on startup** enabled (you turned this on in Step 2) and force-pull via the command palette. Also open the routine's run log on the **Routines** page to confirm it actually pushed to
> 
> GitHub
> 
> . Walk me through this.
> 
> 💡 **What if my machine is off at 8am?**
> 
> That is the whole point.
> 
> Cloud Routines
> 
> run on Anthropic's infrastructure, so your briefing runs whether your laptop is open, asleep, or across the country. When you open your machine,
> 
> Obsidian Git
> 
> pulls the latest commit and your briefing is waiting.

#### 🤫 Take a screenshot of wiki/log.md in Obsidian showing the briefing entry generated automatically by the Cloud Routine.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### 🤫 How will you build a habit of reading the briefing each morning, and what will you change in priorities.md or your commands if the briefing ever misses the mark?

1/2

**Switch the Schedule to Your Real Morning Time**

Your 2-minute test proved the routine works. Now edit the schedule so it fires every weekday at the time you actually want your briefing.

- On the **Routines** page, click your
	Morning briefing
	routine to open it.

![The Morning briefing routine selected on the Routines page ready for editing](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776963669539.webp)

The Morning briefing routine selected on the Routines page ready for editing

- Click the pencil icon to open up the editing console.

![The routine detail view with the pencil edit icon highlighted to open the editing console](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/image1776963632928.webp)

The routine detail view with the pencil edit icon highlighted to open the editing console

- Scroll to the **Schedule** trigger and update the cron expression from your 2-minute test value to
	0 8 \* \* 1-5
	(every weekday at 8am). Swap
	8
	for whichever hour you prefer in 24-hour time.
- Click **Save** at the bottom of the form.

![The Routines page showing the briefing routine schedule updated to weekday mornings](https://nextwork.ai/projects/static/ai-second-brain-claude-code-2/the-routines-page-showing-the-briefing-routine-schedule-updated-to-weekday-mornings1776963629396.webp)

The Routines page showing the briefing routine schedule updated to weekday mornings

> 💡 Picking the right time
> 
> Pick a time 10 to 15 minutes before you usually start working. That gives
> 
> Obsidian Git
> 
> time to pull the fresh commit so the briefing is already waiting in
> 
> wiki/log.md
> 
> when you open
> 
> Obsidian
> 
> with your coffee.

Your second brain is now a genuine daily operating system. It briefs you automatically every morning, captures your day every evening, backs itself up to

GitHub

, and stays connected to your live tools, all without you lifting a finger.

![keyhole](https://nextwork.ai/static/keyhole-black.svg)

## 🤫 Secret Mission

Ready for a challenge? Secret Missions are for learners looking to showcase more advanced skills.

🗑 Before you go

### Clean Up Your Resources

Decide whether to keep your resources running, pause them to come back later, or delete them entirely. This project runs locally with a free GitHub private repo, so there are no ongoing costs beyond your Claude subscription.

**Resources you used:**

#### ✅ What were the key tools and concepts you learnt in this project?

#### ✅ How long did it take you to complete this project?

#### ❤️ Thanks for doing this project!

1/3

🎉 Mission Accomplished

### Nice Work!

Nice work! 🚀 You just turned your AI second brain from a static folder of notes into a daily operating system. Every morning, you can type

/briefing

and get a personalized rundown of your day. Every evening,

/debrief

captures what happened and feeds it back into your knowledge base. Your vault backs itself up to

GitHub

automatically, and

Claude Code

can reach into your calendar, Linear, or Notion without you copying a thing.

**You've learned how to:**

- 🔐 Back up your
	Obsidian
	vault to a private
	GitHub
	repository with automatic syncing via the
	Obsidian Git
	plugin, so your knowledge base is safe and versioned.
- 🔌 Connect
	Claude Code
	to your everyday tools using
	MCP
	Connectors, giving Claude live access to your calendar, messages, or project management tools.
- 🔄 Build a
	/pull-sources
	slash command
	that auto-ingests
	Claude Code
	sessions,
	Gmail
	, and
	Granola
	transcripts straight into your vault, with a built-in slot for any other source you want to add.
- ☀️ Build a
	/briefing
	slash command
	that pulls from
	priorities.md
	, your wiki, and connected tools to create a personalized morning brief.
- 🌙 Build a
	/debrief
	slash command
	that captures your day, updates your wiki, and logs progress against your priorities for a complete morning-to-evening workflow.
- 💎 Schedule
	/briefing
	as a
	Cloud Routine
	in the Secret Mission, so it runs every weekday morning on Anthropic's cloud infrastructure and the fresh brief lands in your
	wiki/log.md
	before you open your laptop.

Ready to quiz yourself? 💪

## AI Second Brain Concepts

6 questions

3 minutes

Test your understanding of key concepts in building an AI second brain with Claude Code and Obsidian.

> 💡 p.s. Does it say "Still tasks to complete!" at the bottom of the screen?
> 
> This means you still have screenshots left to upload, or questions left to answer!
> 
> 1. Press Ctrl+F (Windows) or Command+F (Mac) on your keyboard.
> 2. Search for the text **Return to later**.
> 3. Jump straight to your incomplete tasks!
> 4. 🙋♀️ Still stuck? [Ask the community!](https://discord.gg/gexhP97ySu)

## Setting Up My Vault

In this step, I'm setting up Claude code desktop, and I 'l also going to bring in part one of the vault and scaffold an new claude MD file with four slaches commands. Then I'm going to verify that everything works, and this will get me to the point where I should have been if i had part one