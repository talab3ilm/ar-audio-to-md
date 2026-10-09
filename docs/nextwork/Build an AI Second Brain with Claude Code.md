---
title: "Build an AI Second Brain with Claude Code"
source: "https://nextwork.ai/projects/3c934ac2-caa3-544c-bccb-a3aa89b1a1cc?track=high"
author:
  - "[[the end of this project]]"
  - "[[you'll have:]]"
published:
created: 2026-10-09
description: "Set up an AI-powered knowledge base using Karpathy's LLM Wiki pattern with Claude Code and Obsidian."
tags:
  - "clippings"
---
[Still stuck? Get help from a human](https://discord.gg/8A3mX3CDz5)

Set up an AI-powered knowledge base using Karpathy's LLM Wiki pattern with Claude Code and Obsidian.

![Profile image](https://lh3.googleusercontent.com/a/ACg8ocIPi6QB7hlUbr3cTz6aVmfEMWNCI4Ye3lW8IDlhzQ-sUV0RHg=s96-c) ![Profile image](https://lh3.googleusercontent.com/a/ACg8ocKWOJ2rdTwTJe--hwnmcGzeVnCsNjn4pNKtAFlBTYRkFPsMg_fW=s96-c) ![Profile image](https://lh3.googleusercontent.com/a/ACg8ocKe-yk_KClIEaiW0xvtUBE-2aDvhxKU7KIE3oe6hAnI8PRevA=s96-c) 120+ completed

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

We all consume more information than we can remember, scattered across AI chats, note apps, and browser tabs that we never revisit.

In this project, you will build an AI-powered knowledge base using

Claude Code

and

Obsidian

that ingests your notes from multiple sources and compiles them into a searchable, cross-linked wiki maintained entirely by AI. Over time, every new note cross-links with what you already have, so the vault gets sharper the longer you use it.

### What You'll Build

A structured

Obsidian

vault with a raw-source archive and an AI-compiled wiki, powered by a

CLAUDE.md

schema file that turns

Claude Code

into a disciplined wiki maintainer with custom slash commands.

![Architecture diagram showing notes flowing from your everyday tools (Claude, ChatGPT, Granola, Notion, and more) into a raw folder, then compiled by Claude Code into cross-linked wiki pages in Obsidian](https://nextwork.ai/projects/static/ai-second-brain-claude-code/architecture-diagram-showing-notes-flowing-from-your-everyday-tools-claude-chatgpt-granola-notion-and-more-into-a-raw-folder-then-compiled-by-claude-code-into-cross-linked-wiki-pages-in-obsidian1776281307015.webp)

Architecture diagram showing notes flowing from your everyday tools (Claude, ChatGPT, Granola, Notion, and more) into a raw folder, then compiled by Claude Code into cross-linked wiki pages in Obsidian

By the end of this project, you'll have:

- 🗂️ A **structured Obsidian vault** with separate
	raw/
	and
	wiki/
	directories that keep your original sources untouched.
- 🤖 A **CLAUDE.md schema** plus a
	.claude/commands/
	folder with four real
	Claude Code
	slash commands (
	/ingest
	,
	/query
	,
	/lint
	,
	/log
	).
- 🔗 A **compiled wiki** with cross-linked pages visible in
	Obsidian
	's graph view.
- ⚡ A working
	/ingest
	cycle that turns your raw notes into structured, cited wiki pages.
- 💎 **Secret Mission:** Put
	/query
	,
	/lint
	, and
	/log
	to work on your freshly ingested wiki.

Want a complete demo of how to do this project, from start to finish? Check out our 🎬 [walkthrough with Maximus](https://www.youtube.com/watch?v=d5-eFi4YWmQ)

![](https://www.youtube.com/watch?v=d5-eFi4YWmQ)

> 💡 Are there any prerequisites?
> 
> No prior experience is required. You will need a paid
> 
> Claude
> 
> account (Pro, Max, Team, Enterprise, or Console) so you can use
> 
> Claude Code
> 
> , plus
> 
> Obsidian
> 
> , which is free for personal use.

Not sure if this project is right for you? Check if it matches your goals

If you're up for a bit of a challenge, **quiz yourself** on the key concepts up ahead in this project.

## AI Second Brain Fundamentals

5/6

Answers correct

April 30, 2026

Test your understanding of Obsidian, Claude Code, vault architecture, and the ingest process.

This project is part of a series:

1. Part 1: You are here!

## Start Your Project Here

Pick the learning style that fits you best.

## Step-by-Step Guidance

Welcome to the Step-by-Step Guidance version of this project. Let's do this!

If you're ever stuck, [ask the NextWork community](https://community.nextwork.ai/). Learners like you are already asking questions about this project.

👀 Step #0

### Before We Start...

#### ✍️ What are we doing in this project?

Edit answer

🔧 Step #1

### Install Your Tools

To build our AI second brain, we need two tools working together:

Obsidian

as the visual interface for our wiki, and

Claude Code

as the AI agent that maintains it. Both tools will point at the same folder on your computer.

In this step, we'll install both tools so they're ready to work together in Step 2.

**In this step, get ready to:**

#### ✍️ What are we doing in this step?

Edit answer

**Install Obsidian and Create Your Vault**

Obsidian

is a free note-taking app that stores everything as plain

Markdown

files in a folder on your computer. That folder is called a "vault."

![Empty Obsidian vault with the second-brain name visible](https://nextwork.ai/projects/static/ai-second-brain-claude-code/empty-obsidian-vault-with-the-second-brain-name-visible1775851556456.webp)

Empty Obsidian vault with the second-brain name visible

You should see an empty vault with no files. That's exactly what we want.

> 💡 What is an Obsidian vault?
> 
> A vault is just a regular folder on your computer. Obsidian reads and writes Markdown files inside it. Because it's a plain folder, other tools (like Claude Code) can access the same files directly.
> 
> 💡 **Is Obsidian free?**
> 
> Yes. Obsidian is free for personal use. Paid add-ons like Sync and Publish are optional and not needed for this project.

#### 📸 Take a screenshot of your empty Obsidian vault.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_qw9n3t5y?t=1791555846460)

mySecondBrain.png

100% uploaded

Edit answer

**Install the Obsidian Web Clipper (Optional)**

The

Web Clipper

is a browser extension that lets you save web pages directly into your vault. It's not required for this project, but it's handy if you want to clip articles later.

> 💡 Why a Web Clipper?
> 
> A second brain is most powerful when you can capture ideas quickly. The Web Clipper lets you save any web page as a Markdown note in your vault with one click.

**Install Claude Code and Connect to Your Vault**

Claude Code

is a command-line AI agent that can read, create, and edit files on your computer. We'll point it at the same vault folder so it can manage your wiki pages.

You can skip the install step.

- Open your terminal and confirm your version:

```bash
claude --version
```

You should see a version number. If the command is not found, switch to the **I need to install Claude Code** tab.

- Open your terminal.

- Copy and paste the following command, then press **Enter**:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

- Open **PowerShell**.
- Copy and paste the following command, then press **Enter**:

```powershell
irm https://claude.ai/install.ps1 | iex
```

> 💡 Windows prerequisite
> 
> Claude Code on Windows requires Git for Windows. If you don't have it, download it from [gitforwindows.org](https://gitforwindows.org/) first.

- Verify the installation by running:

```bash
claude --version
```

> 💡 What Claude account do I need?
> 
> Claude Code requires a Pro, Max, Team, Enterprise, or Console account. A free Claude account will not work.

#### ✍️ What version of Claude Code did you install?

Edit answer

Your tools are installed. Next up, you'll point Claude Code at your vault and start building the structure of your second brain.

🔍 Step #2

### Build Your Vault Architecture

You have

Obsidian

and

Claude Code

installed, both pointing at the same folder. Nice work getting set up. Now it is time to give your vault some structure.

Before you can start importing notes or asking Claude to synthesize knowledge, you need a solid foundation. The directory structure you build now is the backbone of Karpathy's

LLM

Wiki pattern. The most important decision is the separation between

raw/

and

wiki/

. Nearly every mistake in early reimplementations of this pattern traces back to blurring the two folders.

**In this step, get ready to:**

#### ✍️ What are we doing in this step and why is the raw/ vs wiki/ separation important?

Edit answer

**Navigate to Your Vault**

- Open your terminal.
- Navigate to your vault folder.

```bash
cd ~/Documents/second-brain
```

Terminal with cd ~/Documents/second-brain run to enter the vault directory

**Ask Claude Code to Build the Structure**

- Start a new
	Claude Code
	session in your vault folder.

```bash
claude
```

- First time using Claude Code? Follow the prompts to sign in with your Claude account.
- Claude Code will ask for permission to access this folder. Select **1\. Yes, I trust this folder**.

![Claude Code asking for permission to access your second-brain vault folder on first launch](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-asking-for-permission-to-access-your-second-brain-vault-folder-on-first-launch1775851971448.webp)

Claude Code asking for permission to access your second-brain vault folder on first launch

- Fill in the
	MY\_SOURCES
	variable in the prompt below with the source categories you want inside
	raw/
	. Use short, folder-safe names separated by commas (for example:
	claude-exports, notion-exports, granola-exports
	). Claude will create a subfolder inside
	raw/
	for each name you list.
- Paste the completed prompt into
	Claude Code
	:

```js
Create the following directory structure for my second brain vault:

second-brain/
├── raw/                # MY source documents, never modified by you
├── wiki/               # YOUR domain, you create and maintain these pages
│   ├── index.md        # Master catalog of all wiki pages
│   ├── log.md          # Append-only activity log
│   ├── concepts/       # Concept and topic pages
│   ├── projects/       # Project-specific pages
│   └── people/         # People dossiers
├── journal/            # Daily notes (Part 2)
└── content/            # Content pipeline (Part 2)

Then create these subfolders inside raw/, one per source I want to bring into this second brain:

e.g. claude-exports, chatgpt-exports, notion-exports, granola-exports, articles, notes

Add a brief README.md in every folder you create (including each raw/ subfolder) explaining what belongs there and, where relevant, where to export it from.
```

When prompted, include the subfolders you'd like under

raw/

. Here are some ideas to steal from:

- **AI chat**:
	claude-exports
	,
	chatgpt-exports
	,
	perplexity
	,
	raycast-ai
	,
	cursor-chats
	,
	copilot-chats
- **AI notes & meetings**:
	granola-exports
	,
	mem
	,
	reflect
	,
	fathom
	,
	otter
	,
	fireflies
	,
	loom
- **Docs & wikis**:
	notion-exports
	,
	google-docs
	,
	apple-notes
	,
	evernote
	,
	bear
	,
	roam
- **Reading**:
	readwise
	,
	kindle-highlights
	,
	apple-books
	,
	pocket
	,
	instapaper
	,
	matter
- **Media**:
	podcast-transcripts
	,
	youtube-transcripts
	,
	voice-memos
	,
	substack
- **Work**:
	slack-exports
	,
	linear
	,
	jira
	,
	email-archives
- **Research**:
	pdfs
	,
	arxiv-papers
	,
	zotero
- **Plus**:
	articles
	(web clippings),
	notes
	(personal notes), or anything else you want

Claude Code will ask for your permission before running commands and creating files. You'll see prompts like "Do you want to proceed?" and "Do you want to create \[file\]?"

![Claude Code asking for permission to run a bash command to create the directory structure](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-asking-for-permission-to-run-a-bash-command-to-create-the-directory-structure1775852776648.webp)

Claude Code asking for permission to run a bash command to create the directory structure

- Select **Yes** each time, or select **Yes, allow all edits during this session** to let Claude create all the folders and files without asking again.

![Claude Code asking for permission to create a README.md file, with options to allow all edits during the session](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-asking-for-permission-to-create-a-readmemd-file-with-options-to-allow-all-edits-during-the-session1775852780650.webp)

Claude Code asking for permission to create a README.md file, with options to allow all edits during the session

![Claude Code creating the vault folder structure](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-creating-the-vault-folder-structure1775852596945.webp)

Claude Code creating the vault folder structure

Claude creates a brief

README.md

in each folder explaining its purpose. This matters because Obsidian only shows folders that contain at least one file.

> 💡 What did Claude just build?
> 
> Two top-level folders with opposite ownership rules. This is the foundation of the LLM Wiki pattern. You own
> 
> raw/
> 
> and drop source material into it; Claude Code only reads from it. Claude owns
> 
> wiki/
> 
> and writes curated, interlinked pages based on what it finds in
> 
> raw/
> 
> . You read
> 
> wiki/
> 
> , Claude writes it.

```js
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│  1. YOUR MESSY NOTES   │      │   2. CLAUDE ORGANISES  │      │   3. YOUR SECOND BRAIN │
│  ────────────────────  │      │   ───────────────────  │      │   ───────────────────  │
│                        │      │                        │      │                        │
│   raw/                 │      │   Reads raw/, follows  │      │   wiki/                │
│   • claude-chat.md     │ ───► │   rules in CLAUDE.md,  │ ───► │   • index.md           │
│   • chatgpt-chat.md    │      │   writes wiki/         │      │   • concepts/          │
│   • meeting-notes.md   │      │                        │      │   • people/            │
│   • notion-export.md   │      │   Commands you run:    │      │   • projects/          │
│                        │      │     /ingest  /query    │      │                        │
│   YOU drop notes here. │      │     /lint    /log      │      │   YOU read here, in    │
│                        │      │                        │      │   Obsidian.            │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘

      scattered across               turns mess into               ask questions, spot
      5 different apps               linked knowledge              patterns, never lose
                                                                   an idea again
```

> 💡 Why the raw/wiki split is the load-bearing rule
> 
> Out of everything in Karpathy's LLM Wiki pattern (the schema, the slash commands, the frontmatter), the one thing you cannot compromise on is the
> 
> raw/
> 
> vs
> 
> wiki/
> 
> separation.
> 
> raw/
> 
> is your memory of record.
> 
> wiki/
> 
> is Claude's interpretation of that memory. If Claude is ever allowed to edit
> 
> raw/
> 
> , its synthesis gets layered on top of your original notes and you lose the ability to trust either side. Keep them strictly separate and you can always re-ingest from a clean copy of your sources, roll back a bad session, or swap Claude out for a different model later without losing your ground truth.

**Verify in Obsidian**

- Switch to
	Obsidian
	and check the left sidebar for your new folders.

![Obsidian sidebar showing the new vault folder structure](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-sidebar-showing-the-new-vault-folder-structure1775852792252.webp)

Obsidian sidebar showing the new vault folder structure

- If **Graph View** is not already open in a tab, open it with **Cmd+G** (macOS) or **Ctrl+G** (Windows). If it is already open, click its tab to bring it to focus.

The graph will be sparse for now, but it will grow as you add content in the next steps.

![Obsidian Graph View showing initial vault nodes](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-graph-view-showing-initial-vault-nodes1775852785869.webp)

Obsidian Graph View showing initial vault nodes

> 🙋♀️ Folders not appearing in Obsidian?
> 
> Obsidian only shows folders that contain at least one file. Check that Claude Code created
> 
> README.md
> 
> files inside each folder. If they are missing, run the prompt again or ask our AI for help.

#### 📸 Take a screenshot of your Obsidian Graph View showing the initial vault structure.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_v2d1s6t4?t=1791555846456)

graphViex.png

100% uploaded

Edit answer

> 💡 What makes a good wiki page?
> 
> Good pages are **atomic** (one idea each), **densely linked** with
> 
> \[\[wiki-links\]\]
> 
> , **cited** back to files in
> 
> raw/
> 
> , **synthesized** instead of copy-pasted, and **reachable from
> 
> index.md
> 
> **. When sources disagree, good pages name the disagreement instead of picking a winner. You will encode all of this into your
> 
> CLAUDE.md
> 
> schema in Step 3, so Claude applies these rules automatically to every page it writes.

Your vault architecture is in place. Next up, you will create the

CLAUDE.md

file that tells Claude how to behave inside this vault. This is the schema that makes your second brain truly intelligent.

✨ Step #3

### Define Your Schema and Slash Commands

Your vault has a clear folder structure, but

Claude Code

doesn't know any of the rules yet. Every time you start a new session, Claude would be starting from scratch with zero understanding of how your wiki works or what the page conventions are.

You'll fix that with two things:

- A
	CLAUDE.md
	file at your vault root that describes the rules of the system. Claude Code auto-reads this file every session, so it becomes your system's constitution.
- A
	.claude/commands/
	folder with one file per workflow (
	ingest.md
	,
	query.md
	,
	lint.md
	,
	log.md
	). Each file becomes a real
	Claude Code slash command
	: type
	/ingest
	and it runs, tab-complete and all.

Together, CLAUDE.md is *what your vault is*, and the slash commands are *how you operate on it*.

**In this step, get ready to:**

#### ✍️ What are we doing in this step?

Edit answer

**Ask Claude to Create the Schema**

Your

Claude Code

session from Step 2 should still be running inside your vault root, which is exactly where it needs to be so Claude writes

CLAUDE.md

in the right place.

You're good to go. Skip straight to the prompt below.

No worries, let's reopen it.

- Open your terminal.
- Navigate to your vault folder.

```bash
cd ~/Documents/second-brain
```

- Start a new
	Claude Code
	session.

```bash
claude
```

![Claude Code launched from the second-brain vault root, ready for the CLAUDE.md prompt](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-launched-from-the-second-brain-vault-root-ready-for-the-claudemd-prompt1776281688743.webp)

Claude Code launched from the second-brain vault root, ready for the CLAUDE.md prompt

> 🙋♀️ Not sure you're in the right folder?
> 
> Run
> 
> pwd
> 
> in your terminal before
> 
> claude
> 
> . It should print the full path to your vault, for example
> 
> /Users/yourname/Documents/second-brain
> 
> . If it prints anything else,
> 
> cd
> 
> into the vault first.

- Paste the prompt below into
	Claude Code
	and press **Enter**.

```js
Create a CLAUDE.md file for my second brain vault with these four sections:

1. Project Structure
   Document the raw/ vs wiki/ folder separation, every subfolder,
   and the purpose of index.md and log.md.

2. Page Conventions
   Every wiki page must have YAML frontmatter with these fields:
   title, type (one of: concept, entity, source-summary, comparison,
   project, person), sources, related, created, last-updated.
   Pages should use [[wiki-links]], be atomic (one idea per page),
   and use a consistent heading structure.

3. Style Guide
   Use clear, concise prose. Prefer bullet points. Attribute every claim
   to its source. Note contradictions explicitly.

4. Domain Context
   IMPORTANT: Do NOT write this section yet. First, pause and ask me
   2-3 short questions, one at a time, to learn what I actually work
   on day to day. Suggested questions:
   - What topics or subjects come up most often in your conversations and notes?
   - Who are the main people, projects, or systems you think about?
   - What are you trying to remember or get smarter about over time?
   Wait for my answers, then use them to write the Domain Context
   section in 4-6 sentences using my own language. Do not invent
   details I did not give you.
```

> 💡 Why does Claude ask questions first?
> 
> The Domain Context section needs to reflect what YOU actually work on, not a template guess. Instead of asking you to articulate your domain cold, Claude pauses and asks about your topics, decisions, and what you want to remember. Answer each in a sentence or two and Claude writes the section in your own words.

- Answer Claude's questions as they come up.
- Once you have finished answering, Claude will write
	CLAUDE.md
	to your vault root. You will see "Created CLAUDE.md" (or similar) in the terminal.

![Claude Code confirming CLAUDE.md was created at the vault root](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-confirming-claudemd-was-created-at-the-vault-root1775853524969.webp)

Claude Code confirming CLAUDE.md was created at the vault root

> 💡 What did Claude just write?
> 
> One file at the vault root called
> 
> CLAUDE.md
> 
> , with four sections that together teach Claude the rules of your vault. **Project Structure** locks in the
> 
> raw/
> 
> vs
> 
> wiki/
> 
> ownership so Claude never writes into your source folders. **Page Conventions** sets frontmatter and linking rules. **Style Guide** sets the voice, including how contradictions get flagged. **Domain Context** names the subject matter of your work. In Karpathy's LLM Wiki pattern, this file is the spec Claude writes against. Edit it and every future page Claude writes will follow the new rules.
> 
> 💡 **How does Claude Code find**
> 
> **CLAUDE.md**
> 
> **?**
> 
> When you run
> 
> claude
> 
> from a folder, that folder is your "current working directory." Claude Code checks it for
> 
> CLAUDE.md
> 
> , then the parent folder, then its parent, all the way up to your home folder. Every file it finds gets stitched into one set of instructions for the session. That is why
> 
> CLAUDE.md
> 
> needs to be in the vault root. It is the folder you will launch Claude from every time.

**Review the Generated CLAUDE.md**

Claude's first draft is not always complete. Do a fast scan for each required piece.

- In
	Obsidian
	, click
	CLAUDE.md
	in the left sidebar to open it.

![The CLAUDE.md file open in Obsidian showing the schema sections](https://nextwork.ai/projects/static/ai-second-brain-claude-code/the-claudemd-file-open-in-obsidian-showing-the-schema-sections1775853558199.webp)

The CLAUDE.md file open in Obsidian showing the schema sections

#### 📸 Take a screenshot of your CLAUDE.md open in Obsidian.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_v3n8q1w6?t=1791555846502)

claudeMD.png

100% uploaded

Edit answer

#### ✍️ What are the four sections in your CLAUDE.md, and what does each one teach Claude about your vault?

Edit answer

1/2

**Create Your Slash Commands**

CLAUDE.md teaches Claude the rules of your vault. Now you need the verbs, the things you'll actually type to operate on the vault. In

Claude Code

, a slash command is just a Markdown file at

.claude/commands/\<name>.md

: its contents become the prompt when you type

/\<name>

.

- Confirm your Claude Code session is running from your vault root (the same folder that holds
	CLAUDE.md
	,
	raw/
	, and
	wiki/
	). If you're not sure, type
	/exit
	,
	cd
	into the vault, and run
	claude
	again.
- Paste this prompt into your Claude Code session:

```js
Create a .claude/commands/ folder inside my current working directory (this vault root, next to CLAUDE.md, raw/, and wiki/). Do NOT create it anywhere else. Add four slash-command files inside that folder. Each file should start with a short frontmatter block (description, argument-hint) and then the prompt body.

1. .claude/commands/ingest.md
   Description: Ingest new files from raw/ into wiki/.
   Prompt body should instruct Claude to:
   - For each unread file in raw/ (skip anything already summarised):
     read it, write a source-summary page in wiki/, create or update
     concept/project/person pages as needed, cross-link with [[wiki-links]],
     update wiki/index.md, and append a timestamped entry to wiki/log.md.
   - Process 5-10 sources thoroughly per run. If $ARGUMENTS is provided,
     limit to that many sources.

2. .claude/commands/query.md
   Description: Synthesise an answer from the wiki.
   Argument-hint: the question to answer
   Prompt body should instruct Claude to:
   - Read wiki/index.md and the pages most relevant to $ARGUMENTS.
   - Synthesise an answer grounded in the wiki, cite every claim by
     wiki page name, and flag if sources disagree.
   - If the synthesis reveals a new connection, propose a wiki update
     but do not write it without confirmation.

3. .claude/commands/lint.md
   Description: Run a health check on the wiki.
   Prompt body should instruct Claude to:
   - Scan wiki/ for broken [[wiki-links]], orphan pages, pages missing
     required frontmatter, stale pages (30+ days untouched), and
     contradictions between pages.
   - Report findings as a structured list. Do not fix anything yet,
     ask for permission first.

4. .claude/commands/log.md
   Description: Append a timestamped note to wiki/log.md.
   Argument-hint: the thought or note to capture
   Prompt body should instruct Claude to:
   - Append a timestamped entry containing $ARGUMENTS to wiki/log.md.
   - If the note mentions a project, person, or concept that has a
     wiki page, update that page too. Otherwise do not create new pages.

Create all four files now.
```

- Approve each file creation when Claude Code asks.

![Claude Code creating the four slash-command files inside .claude/commands/](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-creating-the-four-slash-command-files-inside-claudecommands1776199970899.webp)

Claude Code creating the four slash-command files inside.claude/commands/

> 💡 Why.claude/commands/ instead of putting this in CLAUDE.md?
> 
> CLAUDE.md
> 
> is context that Claude reads passively every session. Files under
> 
> .claude/commands/
> 
> are real Claude Code slash commands: typing
> 
> /ingest
> 
> at the start of a message runs the file as a prompt, with
> 
> $ARGUMENTS
> 
> filled in from anything you type after the command. They tab-complete, they're shareable via Git, and they don't conflict with Claude Code's parser.

#### 📸 Take a screenshot of your.claude/commands/ folder showing the four slash-command files.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_p6x2m9k4?t=1791555846512)

claudeMD.png

100% uploaded

Edit answer

#### ✍️ What does Claude Code do with each file inside \`.claude/commands/\`?

Edit answer

1/2

**Restart Your Claude Code Session**

Claude Code only scans

.claude/commands/

when it starts. To make your new slash commands available, you need to restart the session.

- In your
	Claude Code
	session, type:

```js
/exit
```

- Then start a fresh session from the same vault folder:

```bash
claude
```

> 💡 Why restart?
> 
> New slash commands are not hot-reloaded. Without a restart, typing
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
> , or
> 
> /log
> 
> will fail because the session still has the old (empty) command list.

**Test That Everything Works**

- Confirm your setup in a single message. Paste this into Claude Code:

```js
List the slash commands available in this vault and tell me the rules from CLAUDE.md in one paragraph each.
```

Claude should list

/ingest

,

/query

,

/lint

, and

/log

with their descriptions, and summarise the Project Structure, Page Conventions, Style Guide, and Domain Context from your schema.

![Claude Code summarising the vault rules and listing the four slash commands](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-responding-with-the-project-rules-from-claudemd1775853870327.webp)

Claude Code summarising the vault rules and listing the four slash commands

> 🙋♀️ Claude doesn't list the commands?
> 
> Check that
> 
> .claude/commands/
> 
> sits at the vault root, next to
> 
> CLAUDE.md
> 
> ,
> 
> raw/
> 
> , and
> 
> wiki/
> 
> . If the folder is there but the commands aren't picked up, restart Claude Code (
> 
> /exit
> 
> , then
> 
> claude
> 
> again) so it re-scans the commands directory. Still stuck?

#### 📸 Take a screenshot of Claude Code listing your slash commands and summarising the rules from CLAUDE.md.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_a9c4e7g1?t=1791555846491)

rules.png

100% uploaded

Edit answer

> 💡 Your schema and commands are meant to evolve
> 
> CLAUDE.md
> 
> and your
> 
> .claude/commands/
> 
> files are yours to edit freely. As you use the system, you'll discover better page conventions and new workflows worth turning into commands. This co-evolution between you and the LLM is what makes the system get smarter over time.

Your schema is locked in and your slash commands are live. Next up, you'll feed the vault real source material and put

/ingest

to work.

📝 Step #4

### Export and Import Your Existing Data

Your vault has a solid structure, your

CLAUDE.md

schema is in place, and your slash commands are ready. But the vault is still empty.

The whole point of an AI second brain is to avoid starting from a blank canvas. You already have valuable knowledge scattered across

Claude

conversations,

ChatGPT

chats, Granola meeting notes, and

Notion

pages. In this step, you will export that knowledge and feed it into your vault so

Claude Code

has real material to work with.

**In this step, get ready to:**

#### ✍️ What are we doing in this step?

Edit answer

**Export Your Conversations**

You do not need all of these sources. Even 5-10 items from a single tool is enough to get started. Pick the tool you use most and come back for the others later.

- Open [claude.ai](https://claude.ai/) in your browser.
- Click your initials in the lower-left corner.
- Select **Settings**.

![Selecting Settings from the account menu](https://nextwork.ai/projects/static/ai-second-brain-claude-code/selecting-settings-from-the-account-menu1775854919268.webp)

Selecting Settings from the account menu

- Navigate to **Privacy**.
- Click **Export data**.

![The Claude Export Data dialog showing options to export all conversations](https://nextwork.ai/projects/static/ai-second-brain-claude-code/the-claude-export-data-dialog-showing-options-to-export-all-conversations1775855110410.webp)

The Claude Export Data dialog showing options to export all conversations

- Leave the default settings (export **All** conversations) and click **Export**.

![The Claude Export Data confirmation showing the export request was submitted successfully](https://nextwork.ai/projects/static/ai-second-brain-claude-code/image1775855233241.webp)

The Claude Export Data confirmation showing the export request was submitted successfully

You will receive a download link via email within a few minutes. The link expires in 24 hours.

- Open the email and download the ZIP file.

![Email from Claude containing the download link for your conversation export ZIP file](https://nextwork.ai/projects/static/ai-second-brain-claude-code/image1775855312449.webp)

Email from Claude containing the download link for your conversation export ZIP file

- Unzip the file.

![The unzipped Claude export folder showing the JSON conversation files inside](https://nextwork.ai/projects/static/ai-second-brain-claude-code/image1775855319714.webp)

The unzipped Claude export folder showing the JSON conversation files inside

> 💡 What is in the export?
> 
> The Claude export contains
> 
> JSON
> 
> files with your conversation history. Each file holds the messages from a conversation, including both your prompts and Claude's responses.

- Drag the unzipped export folder from your Downloads into the Claude Code terminal. This pastes the folder path.
- After the path, type
	move all these files into raw/claude-exports/
	and press **Enter**.

Claude Code terminal showing the export folder path pasted with the move command appended

- Claude Code will ask for permission to access the folder. Select **Yes** to proceed.

![Claude Code asking for permission to access the Downloads folder to move export files](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-downloads-permission.webp)

Claude Code asking for permission to access the Downloads folder to move export files

Your Claude export files are now in

raw/claude-exports/

. You won't see them in Obsidian's sidebar yet because Obsidian hides JSON files by default. You'll convert them to readable Markdown in the next section.

> 🙋♀️ Export option not showing up?
> 
> The export feature is only available from the Claude web app. It is not available on mobile. Make sure you are signed in at [claude.ai](https://claude.ai/) in a desktop browser. Still stuck?

↑ Back to the top of Step 4

- Open [chat.openai.com](https://chat.openai.com/) in your browser.
- Click your profile icon.
- Select **Settings**.
- Navigate to **Data Controls**.
- Click **Export Data**.
- Confirm via email.

You will receive a ZIP file via email. The link expires in 24 hours.

- Download the ZIP file from the email.
- Unzip the file.

> 💡 What is in the export?
> 
> The ChatGPT export contains a
> 
> conversations.json
> 
> file with your full chat history. Each conversation includes metadata like the title and timestamps alongside the messages.

- Drag the unzipped export folder from your Downloads into the Claude Code terminal.
- After the path, type
	move all these files into raw/chatgpt-exports/
	and press **Enter**.

Your ChatGPT export files are now in

raw/chatgpt-exports/

. You won't see them in Obsidian's sidebar yet because Obsidian hides JSON files by default. You'll convert them to readable Markdown in the next section.

> 🙋♀️ Email not arriving?
> 
> Check your spam folder. The export email can take up to 10 minutes to arrive. Still waiting?

↑ Back to the top of Step 4

Granola doesn't have a built-in "export everything" button, so you have two options. Pick whichever fits.

Granola caches your signed-in credentials locally, so

Claude Code

can script a bulk export of every meeting straight into your vault. No clicking through the app.

- In your
	Claude Code
	session (running from your vault root), paste:

```js
I want to bulk export every meeting note from Granola into raw/granola-exports/ as individual Markdown files.

Please:
1. Check that Granola is signed in on this machine by looking for ~/Library/Application Support/Granola/supabase.json (macOS) or the equivalent on Windows/Linux. Tell me what you find.
2. Use the credentials from that file to call Granola's get-documents API and fetch every meeting I have access to.
3. For each meeting, write a Markdown file into raw/granola-exports/ containing the AI-generated notes, attendees, date, and transcript if available. Name the file using the meeting date and title.
4. Add YAML frontmatter with: source: granola, date, attendees, and topic.
5. Before running anything, summarise the plan and ask me to confirm. After running, tell me how many meetings were exported and flag any that failed.
```

- Claude Code will ask for permission to read the credentials file and make network requests. Select **Yes** when it does.

> 💡 Why this works
> 
> Granola stores an authenticated session token on disk when you sign in. Claude Code reads that token, calls Granola's API the same way the desktop app does, and writes every meeting as Markdown. Your credentials never leave your machine.
> 
> 🙋♀️ **Claude Code says it can't find the credentials file?**
> 
> Make sure you're signed into the Granola desktop app at least once. Ask Claude Code to troubleshoot if the file really isn't there.

If you only want the meetings that actually mattered, export them one at a time from the app.

- Open the Granola desktop app.
- Find a meeting note you want to export in the left sidebar.
- Right-click the note (or click the **...** menu at the top of the note).
- Select **Export as Markdown**.
- Choose where to save the file.

Repeat this for each meeting you want in your second brain. Start with the last 10-20 meetings that actually mattered.

- Drag the folder with your exported files into the Claude Code terminal.
- After the path, type
	move all these files into raw/granola-exports/
	and press **Enter**.

> 🙋♀️ Can't find the export option?
> 
> Granola's menus move around between versions. Ask Claude Code for help.

> 💡 What is in the export?
> 
> Either path gives you Granola's AI-generated meeting notes as
> 
> Markdown
> 
> files, including the summary, decisions, and action items. They are already in a readable format, so no JSON conversion is needed later.

↑ Back to the top of Step 4

- Open [Notion](https://notion.so/) in your browser.
- Click **Settings & Members** in the left sidebar.
- Select **Settings**.
- Scroll down and click **Export all workspace content**.
- Choose **Markdown & CSV** as the export format.
- Click **Export**.

You will receive a download link via email.

- Download the ZIP file from the email.
- Unzip the file.

> 💡 What format does Notion export?
> 
> Notion exports pages as
> 
> Markdown
> 
> files. Unlike Claude and ChatGPT exports, these are already in a readable format, so no conversion is needed later.

- Drag the unzipped export folder from your Downloads into the Claude Code terminal.
- After the path, type
	move all these files into raw/notion-exports/
	and press **Enter**.

> 💡 Pro tip
> 
> Exporting individual pages
> 
> You can also export specific pages instead of your entire workspace. Open a page, click the **...** menu in the top right, then select **Export** and choose **Markdown & CSV**.

↑ Back to the top of Step 4

Don't see your tool in the tabs above? No problem. Almost every knowledge app has some way to export your data, but the exact steps change every few months. Instead of hunting through menus, let

Claude Code

do the detective work for you.

- Create a new folder inside
	raw/
	for your tool. For example, if you use Apple Notes, create
	raw/apple-notes-exports/
	.
- Open
	Claude Code
	in your terminal from your vault root.
- Paste this prompt and replace enter your tool name with the tool you want to export from:

```js
I want to pull my data out of enter your tool name
 and save it into raw/enter your tool name
-exports/ inside my Obsidian vault so I can feed it into my AI second brain.

Please help me by:
1. Looking up the current, official export instructions for enter your tool name
 and summarising the exact steps I need to click through.
2. Telling me what format the export will come in (JSON, HTML, CSV, Markdown, PDF, etc.) so I know what I'm working with.
3. If enter your tool name
 has an API, CLI, or scriptable export, offer to write a small script that downloads my data directly into raw/enter your tool name
-exports/ for me.
4. Once I've got the files, telling me whether I need a conversion step to turn them into clean Markdown for the ingest process.

Start by telling me what you found about enter your tool name
's export options before writing any code.
```

- Follow the steps Claude Code gives you and drop the exported files into the folder it suggests.

> 💡 Tools that work well as sources
> 
> Apple Notes, Google Docs, Obsidian (another vault), Bear, Roam Research, Logseq, Readwise highlights, Todoist, Linear, and even voice memo transcripts all make great raw material for a second brain. If a tool stores your thinking, it's fair game.
> 
> 🙋♀️ **Claude Code can't find export instructions?**
> 
> Some smaller tools do not document their export flow clearly. Ask Claude Code to inspect the app's local storage as a fallback.

↑ Back to the top of Step 4

Add as many sources as you'd like until you're done. You only need one source to get started, but the more you import, the richer your second brain will be. Scroll back up and click through the other tabs to export from each tool you use.

![Obsidian sidebar showing raw/ subfolders filling up with exported files from Claude, ChatGPT, Granola, and Notion](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-sidebar-showing-raw-subfolders-filling-up-with-exported-files-from-claude-chatgpt-granola-and-notion1776194586552.webp)

Obsidian sidebar showing raw/ subfolders filling up with exported files from Claude, ChatGPT, Granola, and Notion

**Convert Exports to Clean Markdown**

Some exports arrive in JSON (Claude, ChatGPT, Perplexity, Raycast AI, Cursor, Copilot, Readwise, and many meeting tools like Fathom, Otter, or Fireflies), which is not human-readable. Others arrive already in

Markdown

(Notion, Granola, Apple Notes) and don't need conversion.

The prompt below lets Claude Code scan every

raw/

subfolder, find whatever JSON you imported, and convert only those files. If none of your sources are JSON, Claude will tell you there's nothing to convert and you can skip ahead.

> 🙋♀️ Closed your Claude Code session?
> 
> If you closed Claude Code after Step 3, reopen it with
> 
> claude
> 
> from your vault root before continuing.

- Paste this prompt into your
	Claude Code
	session:

```js
Scan every subfolder inside raw/ for JSON files. For each JSON file you find:
1. Parse the conversations, messages, highlights, or records inside
2. Convert each item to clean markdown
3. Name each file based on the conversation topic, title, or first message
4. Save the converted files back in the same raw/ subfolder alongside the original JSON
5. Add YAML frontmatter to each file with: source (the subfolder name), date, and topic

If you find a JSON structure you don't recognise, tell me what you see before writing the script so we can decide the best conversion together. If there are no JSON files in raw/, tell me which subfolders you checked and stop - no conversion needed.

Then run the script.
```

- Press **Enter** and let Claude Code generate and execute the script.

![Claude Code generating and running the conversion script in the terminal](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-generating-and-running-the-conversion-script-in-the-terminal1776195903162.webp)

Claude Code generating and running the conversion script in the terminal

> 💡 What does this script do?
> 
> The script reads raw JSON conversation files, extracts the messages, and writes each conversation as a clean Markdown file with
> 
> YAML frontmatter
> 
> at the top. The frontmatter tags each file with its source (Claude or ChatGPT), the date, and the topic, which makes it easier for the ingest process to organize later.

You should see new

.md

files appearing in your

raw/

subfolders. Each one is a converted conversation.

That's okay! Let's troubleshoot:

- Tell Claude Code exactly what went wrong. Paste the error message back into the chat:

```js
The script failed - here's the error: [paste your error here]. Can you fix it and try again?
```

- The JSON format for these exports can change over time. If the script cannot parse your files, ask Claude Code to inspect the raw file first:

```js
Can you look at the first 50 lines of raw/claude-exports/[filename].json and figure out the structure, then rewrite the conversion script?
```

> 🙋♀️ Still stuck?
> 
> Get help with your error or share your error with [the NextWork community!](https://discord.gg/gexhP97ySu)

#### 📸 Take a screenshot of your raw/ folder in Obsidian showing your converted markdown files.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_k8n4y1q3?t=1791555846472)

exportJsontoMd.png

100% uploaded

Edit answer

#### ✍️ How many markdown files did Claude Code create from your exports?

Edit answer

1/2

**Verify Your Files in Obsidian**

- Switch to
	Obsidian
	and open the file explorer in the left sidebar.
- Expand the
	raw/
	folder and its subfolders.
- Confirm that you can see
	.md
	files in the export subfolders.

![Obsidian file explorer showing markdown files in the raw subfolders](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-file-explorer-showing-markdown-files-in-the-raw-subfolders1776195976853.webp)

Obsidian file explorer showing markdown files in the raw subfolders

- Open a few of the converted files.
- Check that they have readable content and YAML frontmatter at the top. In Obsidian, frontmatter is auto-rendered as a **Properties** panel right under the file title, with one row per field (e.g.
	source
	,
	date
	,
	topic
	). If you see that Properties panel, the YAML is there.

![Obsidian showing the Properties panel with source, date, and topic fields for a converted Claude conversation file](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-showing-the-properties-panel-with-source-date-and-topic-fields-for-a-converted-claude-conversation-file1776198650803.webp)

Obsidian showing the Properties panel with source, date, and topic fields for a converted Claude conversation file

> 💡 Want to see the raw YAML?
> 
> Obsidian hides the
> 
> \---
> 
> block and shows it as the Properties pane by default. To see the underlying YAML, press **Cmd+E** (macOS) or **Ctrl+E** (Windows) to toggle Source mode. You'll see something like this at the very top of the file:
> 
> ```markdown
> ---
> source: claude-exports
> date: 2026-03-26
> topic: Building muscle while cutting fat and improving mobility
> ---
> ```

Do not worry about perfect formatting at this stage. The ingest process in the next step handles synthesis and cross-linking.

> 💡 Large exports? Start small
> 
> Claude Code has
> 
> context window
> 
> limits. If you exported hundreds of conversations, start with 10-20 of your most relevant ones. You can always add more later by running the conversion script again on the remaining files.

#### ✍️ What did you notice when opening one of the converted files in Obsidian?

Edit answer

Your vault now has real content to work with. Next up, you will run the

/ingest

command and watch Claude Code compile your raw notes into a cross-linked wiki.

🚀 Step #5

### Run Your First Ingest Cycle

Your

raw/

folder is loaded with real content, your

CLAUDE.md

defines the rules, and your

.claude/commands/ingest.md

is waiting to be invoked. Now it is time to run the core operation that makes the entire system work: the ingest.

/ingest

is the heart of Karpathy's pattern. Instead of searching through scattered raw notes every time you need something, Claude pre-compiles your knowledge into structured

wiki

pages with cross-links. Think of it like a compiler turning source code into an executable. Your messy notes go in, and a navigable knowledge base comes out.

**In this step, get ready to:**

#### ✍️ What are we doing in this step and why is the ingest cycle important?

Edit answer

**Start the Ingest**

> 🙋♀️ Closed your Claude Code session?
> 
> If you closed Claude Code after Step 4, reopen it with
> 
> claude
> 
> from your vault root before continuing.
> 
> 🚨 **Heads up:**
> 
> **/ingest**
> 
> **eats
> 
> tokens
> 
> **
> 
> A full ingest reads every file in
> 
> raw/
> 
> and writes new pages into
> 
> wiki/
> 
> , which burns through a lot of tokens and can take 10+ minutes on a large batch. On a
> 
> Claude
> 
> Pro plan, big ingests can push you into the 5-hour usage limit. On the API, a heavy run can cost a few dollars.
> 
> The fix is simple: start with a tiny demo ingest, then run the full ingest in small batches.
> 
> /log
> 
> and
> 
> /query
> 
> are cheap by comparison, so lean on those day-to-day and reserve
> 
> /ingest
> 
> for when you have new source material.

Start with a tiny demo ingest so you can see the workflow in action before committing to a long run.

- In Claude Code, type:

```js
/ingest 2
```

The

2

is passed in as

$ARGUMENTS

to your ingest command, telling Claude to only process 2 sources. A minute or two later you'll see source-summary pages, concept pages, cross-links, and updated

index.md

/

log.md

appear in Obsidian. That's a working slice of the whole system on a small sample.

> 💡 What /ingest is actually doing
> 
> For each file in
> 
> raw/
> 
> , Claude:
> 
> • Writes a summary of it in
> 
> wiki/
> 
> • Pulls out the concepts, people, and projects inside into their own pages
> 
> • Links everything together with
> 
> \[\[wiki-links\]\]
> 
> • Updates
> 
> index.md
> 
> (your table of contents) and
> 
> log.md
> 
> (your activity log)
> 
> The full recipe lives in
> 
> .claude/commands/ingest.md
> 
> . Edit that file any time you want to change how
> 
> /ingest
> 
> behaves.

```js
BEFORE                                                  AFTER
────────────────────────                                ────────────────────────
raw/                                                    wiki/
└── claude-exports/                                     ├── index.md         (catalog)
    ├── chat-on-pricing.md     ──┐                      ├── log.md           (activity)
    ├── chat-on-hiring.md      ──┤                      ├── concepts/
    └── chat-on-launch.md      ──┤    ──/ingest──►      │     ├── pricing.md
└── granola-notes/               │                      │     └── hiring.md
    ├── standup-tues.md        ──┤                      ├── people/
    └── 1-1-with-alex.md       ──┘                      │     └── alex.md
                                                        └── projects/
                                                              └── launch.md

one file per conversation,                              one page per idea,
one file per meeting                                    all cross-linked with [[wiki-links]]
```

![Claude Code running the /ingest slash command and processing raw sources](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-running-the-ingest-command-and-processing-raw-sources1776196498151.webp)

Claude Code running the /ingest slash command and processing raw sources

Once the demo looks right, run

/ingest

without arguments to process the rest of your sources in batches.

- When you're ready to compile the rest, type:

```js
/ingest
```

This runs the command with no argument, so it uses the default "5-10 sources thoroughly" rule from your

ingest.md

file. Re-run it as many times as you need to work through

raw/

.

> 💡 Pro tip
> 
> Watch your graph grow in real time
> 
> Open
> 
> Obsidian
> 
> 's Graph View by pressing **Cmd+G** (macOS) or **Ctrl+G** (Windows) while the ingest runs. You will see new nodes and connections appear as Claude creates each wiki page.

Claude will work through your raw sources one by one. For each file, it reads the content, creates structured wiki pages, and cross-links everything using

\[\[wiki-links\]\]

. This process may take a few minutes depending on how many sources you have.

![Claude Code output showing completed ingest with pages created](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-output-showing-completed-ingest-with-pages-created1776196470922.webp)

Claude Code output showing completed ingest with pages created

#### 📸 Take a screenshot of Claude Code's output after the ingest command finishes.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_p3r8w5n1?t=1791555846463)

{0E07A1F7-861E-451C-B621-EA636BC93CBB}.png

100% uploaded

Edit answer

#### ✍️ How many pages does wiki/index.md list after the ingest?

Edit answer

1/2

**Explore the Results**

- Open
	wiki/index.md
	in
	Obsidian
	. This is the master catalog of every page Claude created.

![The wiki index.md page listing all created wiki pages](https://nextwork.ai/projects/static/ai-second-brain-claude-code/the-wiki-indexmd-page-listing-all-created-wiki-pages1776196718053.webp)

The wiki index.md page listing all created wiki pages

- Open
	wiki/log.md
	to see a timestamped record of everything Claude did during the ingest.

![The wiki log.md showing timestamped ingest activity](https://nextwork.ai/projects/static/ai-second-brain-claude-code/the-wiki-logmd-showing-timestamped-ingest-activity1776196886672.webp)

The wiki log.md showing timestamped ingest activity

- Browse through the wiki subfolders to explore what Claude compiled.

The

wiki/concepts/

folder holds the key ideas and frameworks Claude pulled from your sources. The

wiki/people/

folder contains dossiers for anyone mentioned in your notes. The

wiki/projects/

folder holds the projects and initiatives that came up across your sources.

- Click any
	\[\[wiki-link\]\]
	inside a page to navigate between connected pages.

![A wiki page showing cross-linked content with clickable wiki-links](https://nextwork.ai/projects/static/ai-second-brain-claude-code/a-wiki-page-showing-cross-linked-content-with-clickable-wiki-links1776196937005.webp)

A wiki page showing cross-linked content with clickable wiki-links

> 💡 What are wiki-links?
> 
> Wiki-links
> 
> use the
> 
> \[\[page-name\]\]
> 
> syntax to create connections between pages. When you click a wiki-link in
> 
> Obsidian
> 
> , it jumps straight to the linked page. These links are what turn a folder of isolated notes into a connected knowledge graph.

#### ✍️ Pick one wiki page Claude created. What is the page about and what other pages does it link to?

**Explore Graph View**

- Switch to your **Graph View** tab in Obsidian. If it is not open, press **Cmd+G** (macOS) or **Ctrl+G** (Windows).

You should now see a web of interconnected nodes. Each node represents a wiki page and each line represents a

\[\[wiki-link\]\]

between pages. Clusters of tightly connected nodes indicate related topics.

![Obsidian Graph View showing interconnected wiki pages after ingest](https://nextwork.ai/projects/static/ai-second-brain-claude-code/obsidian-graph-view-showing-interconnected-wiki-pages-after-ingest1776196981324.webp)

Obsidian Graph View showing interconnected wiki pages after ingest

> 💡 What am I looking at?
> 
> The graph is the visual payoff of the ingest cycle. As Andrej Karpathy puts it, "Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase." The dense clusters you see are topics where your notes had the most overlap. Sparse nodes may need more source material.
> 
> 🙋♀️ **Only seeing a few pages or links?**
> 
> Check that your
> 
> raw/
> 
> subfolders actually contain markdown files. If you imported a large number of sources, try running the ingest in batches by subfolder. Even 5-10 conversations is enough to see meaningful connections. How can I check my raw folder contents?

#### 📸 Take a screenshot of your Obsidian Graph View showing the interconnected wiki pages.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

![](https://nextwork.ai/uploads/ai-second-brain-claude-code_k9g4z6c2?t=1791555846485)

{600E855F-AC0D-47D1-A3EC-CFF9A10DF35D}.png

100% uploaded

Edit answer

Your second brain has real compiled knowledge. That's a complete system you can start using today. If you want to push further and put your other three slash commands to work, the Secret Mission below walks through

/query

,

/lint

, and

/log

on your freshly ingested wiki.

💎 SECRET MISSION

### Put Your Four Verbs to Work

You've got

/ingest

running. In this secret mission, you will put the other three slash commands through their paces:

/query

to pull synthesised answers out of your wiki,

/lint

to health-check it, and

/log

to capture ideas on the fly.

**In this secret mission, get ready to:**

```js
THE FOUR VERBS OF A SECOND BRAIN
────────────────────────────────

   /ingest   raw/   ──► wiki/         compile sources into pages
   /query    wiki/  ──► answer        ask questions, get cited answers
   /lint     wiki/  ──► report        find broken links & orphan pages
   /log      note   ──► log.md        capture an idea in one line

These four are the only things you ever do inside your second brain.
```

#### 🤫 What are we doing in this secret mission?

**Use /query**

/query

reads your wiki and writes a cited, synthesised answer to whatever you ask. It's most useful for "what do I already know about X?" style questions.

- In
	Claude Code
	, type:

```js
/query What are the main themes or recurring ideas across my sources?
```

Anything you type after

/query

is passed in as

$ARGUMENTS

and becomes the question. Claude will pull from relevant wiki pages, cite each one by name, and flag if sources disagree.

![Claude Code responding to a /query command with cited wiki sources](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-responding-to-a-query-command-with-cited-wiki-sources1776197099850.webp)

Claude Code responding to a /query command with cited wiki sources

> 💡 What makes a good /query result?
> 
> A strong result cites specific wiki pages by name, synthesises across multiple sources instead of quoting one, and flags contradictions where they exist. If the answer feels thin, you probably need to
> 
> /ingest
> 
> more sources first.

**Use /lint**

/lint

is your wiki's health check. It scans every page and reports broken

\[\[wiki-links\]\]

, orphan pages, missing frontmatter, and contradictions.

- In Claude Code, type:

```js
/lint
```

Claude Code will usually pause partway through and ask **"Continue scanning the remaining pages?"** before finishing the report. Reply

yes

(or press **Enter**) to let it complete.

![Claude Code running /lint and displaying a health report for the wiki](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-running-lint-and-displaying-a-health-report-for-the-wiki1776197134877.webp)

Claude Code running /lint and displaying a health report for the wiki

- Review the report, then ask Claude to fix what it found:

```js
Fix these issues.
```

> 💡 Pro tip
> 
> Run /lint after every big ingest
> 
> New ingests often introduce broken links or orphan pages before things settle. A weekly
> 
> /lint
> 
> keeps the vault healthy.

#### 🤫 Take a screenshot of the /lint health report in Claude Code.

Hover to paste, click to upload or drag and drop

PNG or JPG (max. 10MB)

#### 🤫 What issues did /lint find, and how did Claude fix them?

1/2

**Use /log**

log.md

is mostly an audit trail that

/ingest

,

/query

, and

/lint

append to automatically.

/log

is the human-facing version: drop in a thought that isn't worth saving as a formal source in

raw/

, but shouldn't be lost.

- In Claude Code, type:

```js
/log Had a useful chat about prioritisation today. Key takeaway: ask "what actually breaks if this slips by a week?" before promoting anything.
```

![Claude Code appending a timestamped entry to log.md](https://nextwork.ai/projects/static/ai-second-brain-claude-code/claude-code-appending-a-timestamped-entry-to-logmd1776199864215.webp)

Claude Code appending a timestamped entry to log.md

- Open
	wiki/log.md
	in
	Obsidian
	and confirm the timestamped entry appears. If your note mentioned an existing project, person, or concept that has a wiki page, check that page too — Claude may have updated it.

> 💡 The four verbs of a second brain
> 
> Karpathy's pattern treats
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
> as the only four things you ever need to do inside a second brain. Everything else is a combination of these four verbs. You stop thinking in terms of "open this file, edit that, cross-reference this" and start thinking "ingest this source" or "query this question." The primitives raise your level of abstraction, which is the move that turns a pile of notes into a system you actually use.

![keyhole](https://nextwork.ai/static/keyhole-black.svg)

## 🤫 Secret Mission

Ready for a challenge? Secret Missions are for learners looking to showcase more advanced skills.

🗑 Before you go

### Clean Up Your Resources

Decide whether to keep your resources running, pause them to come back later, or delete them entirely. This project runs entirely locally, so there are no ongoing costs.

**Resources you used:**

No action needed. Choose this if you're still actively building or want to keep testing right away.

Your vault and all its files are stored locally with no ongoing costs. The

CLAUDE.md

file,

raw/

exports, and

wiki/

notes will stay exactly where they are.

> 💡 Back up your CLAUDE.md
> 
> CLAUDE.md
> 
> is the brain of your second brain. Copy it to cloud storage (iCloud, Google Drive, Dropbox) or a private
> 
> GitHub
> 
> repo so you never lose your custom instructions.

Shut down running processes to free up memory, but keep all your files and data so you can pick up where you left off.

- Type
	/exit
	in your
	Claude Code
	session to close it cleanly. This ensures any in-progress file writes complete and
	log.md
	is flushed.

Your vault files,

CLAUDE.md

, and all exports in

raw/

will remain on your machine. To pick up later, open

Obsidian

, navigate to your vault, and start a new

Claude Code

session.

> 💡 Back up your CLAUDE.md
> 
> Before stepping away, copy
> 
> CLAUDE.md
> 
> to cloud storage or a private
> 
> Git
> 
> repository. Your vault is plain
> 
> Markdown
> 
> , so it works perfectly with Git. Run
> 
> git init
> 
> inside your vault folder and commit regularly for version history, backup, and rollback capability.

Remove all project resources and start fresh if you ever want to rebuild.

- Type
	/exit
	in your
	Claude Code
	session if it is still running.
- Delete the entire vault directory:

```bash
rm -rf ~/second-brain
```

- If you installed
	Obsidian
	only for this project and no longer need it, uninstall it through your system's application manager.

> 💡 The raw/ folder is immutable
> 
> If you only want to redo your wiki pages, you do not need to delete everything. Update
> 
> CLAUDE.md
> 
> with new instructions and re-run the
> 
> /ingest
> 
> command. Never delete files from
> 
> raw/
> 
> directly.

🎉 Mission Accomplished

### That's a Wrap!

Nice work! 🚀 You've just built an AI-maintained knowledge base that turns scattered notes into a structured, cross-linked wiki using

Claude Code

and

Obsidian

. This is Part 1 of a 3-part AI Second Brain series.

**You've learned how to:**

- 🏗️ Set up a structured
	Obsidian
	vault using Karpathy's raw/ and wiki/ architecture.
- 📥 Import your existing knowledge from your everyday tools (Claude, ChatGPT, Granola, Notion, or whatever you use) into raw/ as
	Markdown
	files.
- 📝 Write a
	CLAUDE.md
	schema and author four real Claude Code
	slash commands
	(
	/ingest
	,
	/query
	,
	/lint
	,
	/log
	) under
	.claude/commands/
	.
- 🔄 Compile a wiki with cross-linked concept pages, people dossiers, and project pages using
	/ingest
	.
- 🌐 Explore your knowledge as an interconnected web using
	Obsidian
	's Graph View.
- 💎 Put
	/query
	,
	/lint
	, and
	/log
	to work in the Secret Mission to turn your vault into a system you use daily.

#### ✅ What were the key tools and concepts you learnt in this project?

#### ✅ How long did it take you to complete this project?

#### ❤️ Thanks for doing this project!

1/3

Ready to quiz yourself? 💪

## AI Second Brain Fundamentals

5/6

Answers correct

April 30, 2026

Test your understanding of Obsidian, Claude Code, vault architecture, and the ingest process.

> 💡 p.s. Does it say "Still tasks to complete!" at the bottom of the screen?
> 
> This means you still have screenshots left to upload, or questions left to answer!
> 
> 1. Press Ctrl+F (Windows) or Command+F (Mac) on your keyboard.
> 2. Search for the text **Return to later**.
> 3. Jump straight to your incomplete tasks!
> 4. 🙋♀️ Still stuck? [Ask the community!](https://discord.gg/gexhP97ySu)