# AI Pet Short Video Director

A director and producer skill for AI short videos that star a recurring pet. It takes a series about a cat, dog, or other companion animal from story idea to edit: visible story beats, animal blocking, shot planning, generation prompts, and footage review. Before you spend credits on a take, it pins down what that take must show and when to stop.

## What it does

The plugin adds one skill, `ai-pet-short-video-director`. Claude uses it when you ask for help with a pet video series: pitching a story, planning shots, writing a prompt for the video tool you name, or reviewing footage you have already generated. It works on the stage you ask for, replies in your language, and keeps your pet's species, markings, and temperament as you describe them. It is not meant for films led by people or for general commercial work.

## Install

In Claude Code:

```text
/plugin install ai-pet-short-video-director --marketplace Balance0014/ai-pet-short-video-director
```

Then start a new session.

## Data and permissions

The plugin is instructions only: Markdown files, a manifest, and an icon. It runs no code, has no hooks or MCP servers, connects to no service, and sends your data nowhere. It never generates video, spends credits, or publishes anything for you. You choose the generation tool, and that tool's own terms apply.

## Try it

> Pitch one 15-second AI video for my recurring orange cat. Give visible beats, the cat's decisive choice, an earned ending, and the main generation risk. Don't write a video prompt yet.

Once you approve the story, ask for a shot plan and one generation prompt for your tool.

## Source and license

The [source repository](https://github.com/Balance0014/ai-pet-short-video-director) also holds behavior test cases and an optional validator for paid-generation receipts, neither of which is part of this plugin. Released under the MIT License by [Balance Zhao](https://x.com/balance0014).
