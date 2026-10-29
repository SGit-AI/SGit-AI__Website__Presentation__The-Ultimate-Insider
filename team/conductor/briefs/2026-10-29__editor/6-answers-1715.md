# The editor's answers (29 October 2026, about 17:15 London)

By conductor@the-ultimate-insider, from the editor's words in the conductor's session, before he got on the tube. They close six of the seven items in `pace.json` "waits_on_editor". Routed at 17:2x to dev, deck, ruv.sgit, the storyteller, the researcher and motion@.

## 1. Linux in the browser: yes, tonight

> "why can't we have Linux in the browser? Everything's already working, right? Even if you just show me what we have already ... in that same page on the website. Well, at least if you can do that, just put the link to the page that opens up. But it's actually a hell of a demo, and I think a lot of people will love it. So ... all you have to do is reuse what we already have on Harness. If you look at sharness.ai, he already has everything in it."

What this means, smallest first:

- **Nothing new is built.** The Linux already runs on sharness.ai: `https://sharness.ai/code/browser/demo/index.html` (the article: `https://sharness.ai/articles/linux-in-a-tab.html`). ruv.sgit's two pieces already tell it stage by stage: `/studio/lab/sharness/live-demo/v1/` (what to watch for) and `/studio/lab/sharness/kernel-in-a-tab/v1/` (the boot, recorded: this is the offline fallback the 16:3x pre-review asked for, already made).
- **dev**: in the SHarness part, a slide that opens the sharness.ai demo page **in a new tab** (a link and its QR, the showcase template is enough). No change to the player's engine and nothing embedded from another host: the editor clicks, the tab opens, he comes back to the player. This replaces dev 027's "after the talk" for tonight; the full in-player version stays after the talk.
- **deck**: places the three in a row in the SHarness section: live-demo (what to watch for), the link slide (the live tab), kernel-in-a-tab (the recorded boot, shown if the room's network fails, or after the live one as the recap).
- **The security pre-review's conditions (17:2x)**: a plain link, `target="_blank" rel="noopener noreferrer"`, no query string or fragment, the QR made from that same public URL only; no iframe, script or fetch from sharness.ai. If the SHarness section sits in part 1, the slide lands before the 18:30 lock or goes into v1.1 for part 2; a locked part is never changed.
- **The fallback rule holds**: if the network is down, the editor stays on kernel-in-a-tab. Nothing else to make.

## 2. Which blast radius

> "Use the one that we created here."

The blast-radius piece on this site, `/ruv-sgit/blast-radius/`, not ruv.sgit.ai's.

## 3. "Empower" and "the billing"

> "I have no idea what that is, so don't worry about it."

Dropped from the list of projects. Nobody chases them.

## 4. sharness.ai

> "Yeah, it's correct ... that's the website that we created ... it's not directly [SGit], but it's the website that we created in the last couple of days, using the same team, which has the whole thing."

The researcher's capture (`harness.json`) is confirmed. On the slides: sharness.ai is a sibling of the SGit family, made in the last few days by the same way of working, not an SGit product.

## 5. Attrition, on the Wardley maps

> "attrition in the Wardley maps is what prevents things from being commoditized ... why haven't we seen more AI exploits? Because there's a lot of attrition moving from a custom build to even a product and then a commodity ... Why have sometimes people not implement some of these workflows? Because there's attrition in changing how people's work. There's attrition in the technology. Why have companies not innovated? Because they don't have good CI pipelines or good innovation and flows like we have right here ... success breeds attrition."

Attrition is **not** commoditisation: it is the **friction that holds a component back** from moving right on the evolution axis. Three uses for the talk:

- the attackers: few AI exploits yet, because there is attrition from custom-built to product to commodity;
- the defenders: teams do not adopt these workflows, because there is attrition in changing how people work, and in the technology;
- this team: companies do not innovate because they lack good CI pipelines and flows; this team is what low attrition looks like.
- And Simon Wardley's line: success breeds attrition (inertia).

Storyteller: the maps use the word in this sense. motion@: where the Wardley piece shows a component stuck, label it attrition.

## 6. The editor lane

> "I haven't provided any feedback, so don't worry about it."

No longer a blocker. The conductor drains the lane when the editor sends the two sealed files.

## 7. The newsroom's API

Confirmed: **api.newsroom.sgit.ai**.

## Still open

D12, D02, item 4, the draft policy files and the handover zips: no word yet; nobody waits on them for part 1.
