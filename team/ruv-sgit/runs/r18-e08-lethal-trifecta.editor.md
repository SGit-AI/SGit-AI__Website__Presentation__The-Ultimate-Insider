# Editor check: r18-e08-lethal-trifecta

**Verdict: pass with 0 must fix, 3 should fix.** Checked at t=4, 12, 20, 28, 36, 45 and ?static, dark and light, 1280x720. The three ingredients match the programme and source, Willison is named on screen, no quotation, no numbers, no em-dashes. Every text is 20px or larger; the headline, the strapline and the foot clear the ID and each other; the end state does not overlap. The agent red is used only for the agent and what it sends. "Closed" and the final line say "that path", never "safe". The switches behave as the explainer says: the times in RUV_STEPS and the render code match (stages 0, 7, 16, 24, 32, 41; off at +0.6 s, wall at +0.6 to +1.1 s, back on at +6 s, path whole again at +7.6 s).

## Must fix

None.

## Should fix

1. `src/static/studio/lab/e08/v1/index.html`, the `w.tag` text 'turn off: closed' stays under every switch, in teal, while the switch is still on (the end still, and the stages for the other two switches). Teal plus "closed" under an on switch reads as the switch's state, and the end still shows three on switches and three "closed" tags. Fix: change the text to 'off closes this path' (still 20px) and let it fade out when that switch is back on, or keep it only on the switch being turned off: `w.tag.style.opacity = k(s.a + 1) * (1 - S.ease(S.seg(t, s.a + 6, s.a + 6.5)))`. Then update the explainer's sentence "Under the switch, 'turn off: closed' appears and stays" and the 41 s row ("under each switch 'turn off: closed'") to match.
2. `src/pages/ruv-sgit/lethal-trifecta/explainer.html`, Technique: "E10's wall is the stop" cites a piece not yet shipped (E10 is still "asked" in the programme). Fix: "E04 v2's language: a path draws itself, changes colour where it crosses the agent, and stops at a wall." (drop E10).
3. `src/pages/ruv-sgit/lethal-trifecta/explainer.html`, What was left out: "EchoLeak ... had all three present (email as untrusted content, internal data, a path out)" claims more than the data says. injection-sources.json records a crafted email, internal data included in a response that sent it out, and the label "vendor-confirmed vulnerability", not three named ingredients. Fix: "EchoLeak, in the studio's injection-sources data (a crafted email, internal data sent out in a response; labelled there a vendor-confirmed vulnerability), was left out to keep the slide to one idea; E03 already shows it."
