# Obsidian Company Memory

## What it is, in plain English

If you've ever asked your AI for help with your company and watched it produce the same wrong assumption it produced last week — this is the fix.

This skill sets up a folder on your machine called an **Obsidian vault**. Inside the vault, a small set of files tells every future AI session: *read this first*. From then on, your AI shows up to every conversation with the right context already loaded. The vault grows as a by-product of using it — you don't have to maintain it on the side.

You stay in control of everything: the data lives on your disk, in plain text files. You can read it, edit it, delete it, back it up like any other folder. Nothing goes to us, ever.

---

## What you'll need

- A laptop — Mac, Windows, or a recent Linux distro.
- **Obsidian** installed — free from [obsidian.md](https://obsidian.md/download), no account, no sign-up. (You don't have to already know Obsidian; the skill walks you through opening it.)
- An **AI tool** — most people use [Cowork](https://claude.com/cowork) (browser-based, easiest). [Claude Code](https://claude.com/claude-code) also works, as do Codex, opencode, and anything else that reads an `AGENTS.md` file.
- An **empty folder** where you want your company memory to live. Inside Dropbox / iCloud / OneDrive / Google Drive, or just on your laptop — your choice.
- **About 25 minutes**, most of which is you reading what the skill puts in front of you.

---

## Install

### If you're using Cowork (recommended)

1. Go to the [latest release](https://github.com/absolutionlabs/obsidian-company-memory/releases/latest) and download all three files (small — ~30 KB total).
2. In Cowork: open **Skills → Upload skill** and drag each file in. Three uploads, takes about 30 seconds.
3. In a new conversation, say: *"Set up my Obsidian company memory."* Follow the prompts.

That's it.

### If you're using Claude Code or another tool

The install path is slightly different (you clone the repo and copy three folders rather than uploading zips). Full instructions in the [install walkthrough](docs/install-walkthrough.md).

---

## What happens during install

The skill walks you through five short steps, in order:

1. **A safety check.** It asks you to confirm the folder is yours to use, and that your cloud sync provider (if any) is one you're allowed to put your company info into. It won't touch anything until you confirm.
2. **Two questions.** Your company name, and which cloud sync you're using (or "local-only" if none).
3. **About 20 files appear in your folder.** All plain text — Markdown, JSON, YAML. The skill names each one as it lands.
4. **A quick test.** The skill creates a single welcome page and asks you to confirm it shows up in Obsidian. This proves the whole system works.
5. **A short pointer to a guide.** A file called `HOW-TO-USE-THIS.md` lands in your folder. ~10 minutes to read; it covers everything about ongoing use.

If you'd rather read what the skill does before running it, see the [install walkthrough](docs/install-walkthrough.md) — it mirrors the same five steps in detail.

---

## A reasonable amount of caution

This is provided **AS-IS** under the [MIT License](LICENSE). It's free, open source, and we use it ourselves. We've built it carefully and tested it across the situations we could think of — but it's free software you got off GitHub, and the responsibility for what happens on your machine sits with you.

**Please read [DISCLAIMERS.md](DISCLAIMERS.md) before you install.** It covers the limits of our responsibility, what to do if something goes wrong, and the legal terms of using a free tool you got from us. If you're in a regulated sector (drinks, healthcare, finance, professional services), it's especially worth a read.

**Will this touch anything else on my computer?** No. The skill writes files only to the folder you pick. It doesn't install other software. It doesn't run in the background. It doesn't send any data to us — no install ping, no telemetry, no usage data, no error reports. We don't even know you installed it.

**How do I uninstall?** Delete the folder. The skill itself can be removed from your AI tool's skills list the same way you installed it.

**Never installed something from GitHub before?** That's fine. Email `info@absolutionlabs.com` first and we'll happily talk you through it.

---

## If you want to know more before installing

- **[How it compares to other Obsidian setups](docs/standard-vs-ours.md)** — if you've used Obsidian before and want to know what's different here.
- **[Step-by-step install walkthrough](docs/install-walkthrough.md)** — the same five install steps in detail. ~5 minutes to read.
- **[Frequently asked questions](docs/faq.md)** — "can I", "what if", "why does it" answers.
- **[Compatibility matrix](COMPATIBILITY.md)** — operating systems, AI tools, cloud sync providers we've tested.

## If you hit a problem

- **[Troubleshooting](docs/troubleshooting.md)** — common issues with what to do.
- **Email us:** `info@absolutionlabs.com` — a human at Absolution Labs replies within one business day.
- **Security issues:** `security@absolutionlabs.com` — please don't open a public issue for these.

## If you want to fork or customise it

- **[Customisation guide](docs/customisation.md)** — what's editable, what to leave alone, how to re-package.
- **[Upgrading](docs/upgrading.md)** — version pinning, rollback, manual refresh of an existing vault.
- **MIT licensed.** You can take it, modify it, sell it, build on top of it. The only requirement is that the copyright and license text travel with the copy. If you build a commercial variant, please rename it so it isn't confused with the official Absolution Labs release.

---

## About

[**Absolution Labs**](https://absolutionlabs.com) builds AI-augmented operations tools for small companies, mostly in drinks and FMCG. We use this exact memory architecture inside our own operation, and to run [**Asterley Bros**](https://asterleybros.com) — the small-batch drinks company we founded and operate.

If you install this, see it work, and want help applying the same shape to a bigger problem in your business — you know where to find us.

---

*© 2026 Absolution Labs LTD. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL. Full disclaimers: [DISCLAIMERS.md](DISCLAIMERS.md).*
