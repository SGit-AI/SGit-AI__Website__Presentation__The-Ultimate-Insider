---
title: A site for one talk, built the way the talk says to build things
kicker: This site
date: 2026-10-29
author: Dinis Cruz
minutes: 7
description: What is on this site for The ultimate insider at hack::soho, why one talk gets a whole site, how the slides and the releases work, and the team of agents that comes next.
abstract: Tonight at hack::soho, at IOActive in London, I give a talk called The ultimate insider. This is its site: the slides as live infographics, the script beat by beat, every source, and the articles written for it. It exists because a deck that travels without its sources is a claim nobody can check, and because a talk about writing down what agents may do should be built by agents working under rules that are written down. This article says what is here, how it is built, what comes next, and what it does not claim.
---

## In short

- **This is the companion site for The ultimate insider,** my talk at hack::soho on 29 October 2026, hosted by IOActive in London and livestreamed from about 7pm.
- **The slides are web pages that animate.** Each one is an infographic built from the numbers in the article the talk comes from, and the [player](../talk/player.html) steps through them, with a presenter view that keeps the notes and the timings in step.
- **The talk is data.** One file, [talk.json](../talk/talk.json), holds every beat: the slide, what I say, the cue and the sources. The player, [the script](../talk/script.html) and [the slide list](../talk/index.html) all read it, so none of them can drift from the others.
- **Every number is sourced.** [The sources page](../sources/index.html) lists each one by act, and says which are predictions, surveys or preliminary.
- **CI owns the version.** Nobody, person or agent, types a version number here. The release job picks it, tags it and deploys it.
- **A team of agents comes next,** each with a written mandate, in the shape of the SGit Newsroom. Its design will be published here before it runs.

## What the talk is about

Three known problems are arriving at the same time, and nobody is presenting them as one story. AI agents are the insider threat that never scaled before: a reasoning engine in a loop with tools, with skills no human insider ever had, where the distance between benign and malicious is a prompt. The infrastructure that has to contain them was built for static code, and struggles to stay up on its own. And the risk management that has to decide what to do about both still runs on spreadsheets, at the speed of quarters.

The talk puts the three side by side, using the public incidents of the last eighteen months, most of which were not attacks, just agents being agents. Then it turns to the way out: measure what the agent can actually reach, write down what stands in the way, give it a licence to operate that can be suspended, and let it earn its autonomy.

The full argument, with every figure linked, is the newsroom article I wrote a month ago: [The ultimate insider: agents, the infrastructure that cannot hold them, and risk management that cannot keep up](https://newsroom.sgit.ai/articles/ultimate-insider-three-collisions.html). The talk is that article cut to forty minutes, with the evidence on screen.

## Why one talk gets a whole site

A slide deck is usually a file that travels on its own. It gets shared as a PDF, the speaker notes are lost, the sources are a line of small text on the last slide, and a month later nobody can check a number on slide twelve. For a talk whose first half is a list of incidents and statistics, that is the wrong shape. If I tell a room that there are 82 machine identities for every human, the room should be able to find where that comes from, and find that it is a survey of security leaders, not a census.

So the deck and its sources live together. sgit.ai already does this for talks given as vaults, where the slides and the papers they cite never separate. [ruv.sgit.ai](https://ruv.sgit.ai/) did it on 15 October for the talk at Agentic Engineering Live, with every number on screen read from recorded runs. This site follows the second pattern: the slides are pages, the talk is a data file, and the site is the thing you bookmark.

There is a second reason, and it is the argument of the talk itself. The way out I describe is to write down what an agent may do, measure what it can do, and let it earn autonomy inside that. A site about that, built by agents, should be built under rules that are written down, released by a pipeline that does not trust anyone's arithmetic, and checked by a gate before anything goes live. Otherwise it is advice I do not take.

## How the slides work

Each slide is a page of its own, a 1280 by 720 canvas that scales to any screen. It animates on a clock of its own: elements fade in on cue, numbers count up to their value, bars grow to their share, and paths draw themselves. The player can pause that clock, replay it from the start, or jump to the end, which is what the presenter view and the thumbnails use. If your system asks for reduced motion, every slide shows its final frame instead.

The [player](../talk/player.html) is keyboard-first: the arrow keys and the space bar move between beats, **R** replays the current animation, **B** blanks the screen, **F** goes full screen, and **P** opens the presenter view in a second window. The two windows stay in step through the browser, with no server in between: the presenter view shows the current slide, the next one, what I planned to say, the cue, the clock, and whether I am ahead of or behind the plan. Everything runs from static files, so it works from the live site, from a laptop with no network, or from a copy of the repository.

## How it is built and released

The site follows the guidance every repository on the sgit.ai network follows, [Every sgit repository](https://sgit.ai/docs/guidance/repositories.html):

- **The brief is published in full.** What I asked for, the event text and the abstract are on [the brief](../brief/index.html), as given. Where the brief turns out to be wrong, the finding goes in a corrections file, not into the brief.
- **One script builds everything.** Pages are written as fragments; the build adds the navigation and the footer, renders the articles, generates the script and the slide list from `talk.json`, and writes a markdown twin next to every page and an [llms.txt](../llms.txt) at the root, so an agent can read the site as easily as a person.
- **A gate fails the build.** Links resolve, every page has its twin, no placeholder survives, nothing loads from another host, every script parses, every beat has a slide, no em-dashes, and a leak tripwire for keys and tokens. The list is on [the about page](../about/index.html).
- **CI owns the version.** This is the scheme I wrote for OSBot-Utils in 2023, which the newsroom adopted on 27 October after two version races and a refused release in one day; the story is in [CI owns the version](https://newsroom.sgit.ai/articles/ci-owns-the-version.html). Here, the committer's commit carries no number at all. On a push to `dev` or `main`, one release job at a time reads the newest tag, picks the next number, writes it, commits and tags as GitHub Actions, then builds and deploys that exact commit. The footer of every page says which release you are reading, and [the releases page](../admin/versions.html) is read from git, not typed.

## What comes next: a team

This first pass was built in one session by one agent. The next step is a team, in the shape of the ones running the [SGit Newsroom](https://newsroom.sgit.ai/) and the [PHP October 2026 newsroom](https://php.oct.2026.newsroom.sgit.ai/): roles as files, each with a written mandate, the work as a board of files, briefs and debriefs in the open, and every release going through the same gate and the same pipeline. The details of that team are still to come, and when they do, its design goes on this site before any of it runs. That is the order the talk argues for: write down what each agent is for and what stands in its way, then let it work.

## What this does not claim

- **The script is a draft,** written from the article before rehearsal. The talk on the night will differ from it, and the script will be updated afterwards.
- **The demos slide lists candidates.** The running order is confirmed on the night.
- **Two things on the licence slide are examples,** the licence itself and the ladder of autonomy levels; neither is a published scale.
- **The figures are the sources' figures,** as of the article, 30 September 2026. None was re-measured for this site, and one, the date of the US incident reporting rule, is flagged to be checked on the day.
- **One release has not happened yet.** This article is written before the first push to `dev`; the version in the footer is whatever CI numbers it.

*Written up by dev@the-ultimate-insider, this site's developer agent, in a Claude Code session, from the brief and from my article; the argument and the editorial responsibility are mine. Text CC BY 4.0.*
