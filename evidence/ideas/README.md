# The ideas map

Built 2026-10-29T16:25Z. 42 ideas. Each is in the author's terms, with where he states it and what the outside world says for and against it.

## agents-are-the-ultimate-insider

**Agents are the insider threat that never scaled: a reasoning engine in a loop with tools, with skills no human or static code insider had, that does damage without needing to be malicious.**

Kind: position. Grade of its factual core: A4. Strength: Strong: the CEO of Microsoft now argues the same frame in his own words, and insider-risk data shows non-malicious harm dominates; 'never scaled' itself is a framing, not a measured fact.

Talk beats: three, definition, loop, collision

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "Agents are the insider threat that never scaled."}
- {"slug": "ultimate-insider-three-collisions", "quote": "It does not need to be malicious to do damage, and when it is, it does damage at machine speed."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Not because they are necessarily malicious, but because any sufficiently capable actor with access to important systems can make mistakes or be compromised, and the architecture of containment and control must account for that. |
| for | [IT Brief (reporting DTEX/Ponemon)](https://itbrief.com.au/story/insider-risk-costs-soar-as-ai-reshapes-workplace-data), 2026-02 | as employee negligence remains the biggest driver of losses |
| for | [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), 2025-06-16 | The lethal trifecta for AI agents: private data, untrusted content, and external communication |
| context | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Treating frontier closed and open weight models like insider risks is a way to build such a system. |

## nadella-made-the-same-argument

**The model-as-insider argument is now mainstream: Satya Nadella's 10 October 2026 post says what this network has argued since 30 September, ending on the same irony read from the other end.**

Kind: observation. Grade of its factual core: A5. Strength: Confirmed: the primary post is captured and every quoted principle is in it; the claim of priority (since 30 September) is the site's own dated record.

Talk beats: three, brakes

Where:
- {"slug": "authority-outside-the-model", "quote": "The argument is now mainstream."}
- {"slug": "the-same-argument-in-our-words", "quote": "His: the most trustworthy system is the one that needs to trust the model least. Ours: the more you can constrain an agent, the more you can trust it, and the more autonomy you can afford to give it."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | In other words, we need to separate the supply of intelligence from the authority over it. |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | The most trustworthy Super Intelligence system will not be the one with the model we trust most. It will be the one that enables us to trust the model the least. |
| context | [The Next Web](https://thenextweb.com/news/nadella-ai-models-insider-risks-emergency-brake), 2026-10-12 | His post on X drew responses from Microsoft AI’s Mustafa Suleyman and Elon Musk. |

## prompt-injection-is-structural

**Models do not separate code from data, so prompt injection may never be fully fixed, and the controls have to assume a document can turn the agent.**

Kind: position. Grade of its factual core: A5. Strength: Strong: a national cyber agency, the largest model vendor and an adaptive-attack study say the same; only by-design architectures outside the model claim provable protection.

Talk beats: loop, incidents

Where:
- {"slug": "a-policy-beside-the-prompt", "quote": "Models do not separate code from data. Instructions and content arrive in one channel, which is why prompt injection may never be fully fixed."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [UK National Cyber Security Centre](https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection), 2025-12-08 | As there is no inherent distinction between ‘data’ and ‘instruction’, it’s very possible that prompt injection attacks may never be totally mitigated in the way that SQL injection attacks can be. |
| for | [TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/), 2025-12-22 | “Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully ‘solved,’” OpenAI wrote |
| for | [arXiv (Nasr, Carlini et al.)](https://arxiv.org/abs/2510.09023), 2025-10-10 | we bypass 12 recent defenses (based on a diverse set of techniques) with attack success rate above 90% for most; importantly, the majority of defenses originally reported near-zero attack success rates. |
| against | [arXiv (Google DeepMind)](https://arxiv.org/abs/2503.18813), 2025-03-24 | CaMeL, a robust defense that creates a protective system layer around the LLM, securing it even when underlying models are susceptible to attacks. |

## grant-is-not-the-mandate

**What an agent can reach (the grant, measured) is not what it is for (the mandate); the gap between them is the risk, and an agent inherits everything its role accumulated.**

Kind: position. Grade of its factual core: A4. Strength: Strong on the facts under it: the vendor's own telemetry shows grants far exceed use; the framing of 'mandate' as a written artifact is the author's.

Talk beats: permissions, identities, abp

Where:
- {"slug": "footprint-and-blast-radius", "quote": "Reach is what it can do, measured. Mandate is what you asked it to do. The gap is the difference, in both directions."}
- {"slug": "the-same-argument-in-our-words", "quote": "the interesting number is the gap between what a credential allows and what its holder was meant to do. Agents made that gap the whole problem."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Microsoft Entra blog](https://techcommunity.microsoft.com/blog/microsoft-entra-blog/2023-state-of-cloud-permissions-risks-report-now-published/1061397), 2023-03-28 | less than 5% of permissions granted are used by workload identities |
| for | [Microsoft Entra blog](https://techcommunity.microsoft.com/blog/microsoft-entra-blog/2023-state-of-cloud-permissions-risks-report-now-published/1061397), 2023-03-28 | our research found that less than 2% of permissions granted to super identities are used, and 40% of super admins are workload identities. |
| context | [Microsoft Security blog](https://www.microsoft.com/en-us/security/blog/2024/05/29/6-insights-from-microsofts-2024-state-of-multicloud-risk-report-to-evolve-your-security-strategy/), 2024-05-29 | Just 2% |
| for | [OpenID Foundation (arXiv 2510.25819)](https://arxiv.org/abs/2510.25819), 2025-10-29 | ambitions for highly autonomous agents raise complex long-term questions regarding scalable access control, agent-centric identities, AI workload differentiation, and delegated authority. |

## enforcer-test-only-a-boundary-is-a-control

**A control bounds a grant only if it is enforced by something the grant does not include; typed as boundary, setting, expectation or nothing, only a boundary is a control, and a rule the model keeps is hope.**

Kind: position. Grade of its factual core: A5. Strength: Established security principle (reference monitor, 1972) now restated by Microsoft, Meta and DeepMind for agents; the four-way typing and the hope percentages are the author's own, measured on invented designs.

Talk beats: abp, brakes

Where:
- {"slug": "footprint-and-blast-radius", "quote": "Barriers are what stands in the way of each row of the gap, typed as a boundary, a setting, an expectation or nothing, and only a boundary is a control."}
- {"slug": "hope-or-enforcement", "quote": "A rule the model keeps is an expectation: hope. A limit the agent cannot reach is a boundary. Only the second is a control."}
- {"slug": "the-same-argument-in-our-words", "quote": "His most important idea is our enforcer test."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [James P. Anderson / USAF ESD (NIST archive)](https://csrc.nist.gov/csrc/media/publications/conference-paper/1998/10/08/proceedings-of-the-21st-nissc-1998/documents/early-cs-papers/ande72a.pdf), 1972-10 | a. The reference validation mechanism must be tamper proof. |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | It’s why the controls that govern what a model can access and what actions it can take must sit outside the model. |
| for | [Meta AI](https://ai.meta.com/blog/practical-ai-agent-security/), 2025-10-31 | agents must satisfy no more than two of the following three properties within a session to avoid the highest impact consequences of prompt injection. |
| for | [arXiv (Google DeepMind)](https://arxiv.org/abs/2503.18813), 2025-03-24 | by enforcing security policies when tools are called |
| context | [TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/), 2025-12-22 | The company conceded that “agent mode” in ChatGPT Atlas “expands the security threat s |

## agent-logs-are-a-self-report

**An agent's own logs and account of itself are a self-report, not evidence; evidence needs a record a hook reads, a platform boundary, or an outside test.**

Kind: position. Grade of its factual core: A4. Strength: Well backed: Anthropic's own study and Nadella's principles agree; the site's '<2% admitted' should read 'verbalised in its reasoning, in most test environments'.

Where:
- {"slug": "your-agents-logs-are-a-self-report", "quote": "The research agrees. Models that exploited a reward hack admitted it in under 2% of cases."}
- {"slug": "your-agents-logs-are-a-self-report", "quote": "Evidence has four sources. The agent's account, a record a hook reads, a platform boundary, an outside test."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [arXiv (Anthropic Alignment Science)](https://arxiv.org/pdf/2505.05410), 2025-05-08 | to exploit the reward hack on > 99% of the prompts, but almost never (< 2%) verbalizes the reward |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | We need to be able to reproduce how an outcome was achieved without relying on the model to attest to it. |
| against | [arXiv (Anthropic Alignment Science)](https://arxiv.org/abs/2505.05410), 2025-05-08 | These results suggest that CoT monitoring is a promising way of noticing undesired behaviors during training and eval |

## every-risk-is-already-accepted

**A risk exists the moment the exposure does, so somebody is already carrying it; there is no deny button, only three doors (accept for an interval, fund, fix), and silence escalates to the holder's boss.**

Kind: position. Grade of its factual core: A3. Strength: Partly backed: explicit, named, time-limited acceptance is standard NIST practice; 'no deny button' and 'three doors' narrow the standard set, which also includes avoid and transfer.

Talk beats: licence, spreadsheets

Where:
- {"slug": "every-risk-is-already-accepted", "quote": "Every risk your organisation has is already accepted. Somebody is carrying it, today, whether or not anybody signed for it."}
- {"slug": "every-risk-is-already-accepted", "quote": "There are three doors: accept it for a stated interval, fund the work that reduces it, or fix it. Silence is not a fourth door."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf), 2018-12 | understanding or explicitly accepting the organization-wide risks being incurred from such decisions. |
| against | [NIST](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-39.pdf), 2011-03 | These include: (i) risk acceptance; (ii) risk avoidance; (iii) risk mitigation; (iv) risk sharing; (v) risk transfer; or (vi) a combination of the above. |
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-39.pdf), 2011-03 | organizations might accept the risk associated with unfiltered connection to an external communications provider for a limited time |

## accepted-is-not-acceptable

**Accepted (an act by a named person on a date) is not acceptable (a threshold); the EU AI Act asks for residual risk to be judged acceptable and never defines the word.**

Kind: position. Grade of its factual core: A4. Strength: Quote checked in the Act; 'never defines' was not checked against Article 3 in this pass, so that half rests on the author.

Talk beats: licence

Where:
- {"slug": "every-risk-is-already-accepted", "quote": "Accepted is not the same as acceptable. One is an act by a named person on a date. The other is a threshold."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [European Commission AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-9), 2024-07-12 | the relevant residual risk associated with each hazard, as well as the overall residual risk of the high-risk AI systems is judged to be acceptable. |
| context | [NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf), 2018-12 | system and to explicitly accept the risk to agency operations |

## licence-to-operate-that-expires

**Give each agent a licence to operate (who authorised it, who holds it, the policy, the expiry) that the system suspends when the footprint leaves the mandate, not a quarterly review.**

Kind: position. Grade of its factual core: A5. Strength: Strong precedent: NIST's authorisation to operate already carries a named official, an expiry and an ongoing variant; applying it per agent is the new part.

Talk beats: licence, way-out

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "for each agent: authority, licensee, instrument, valid until. Accepted risks that expire and must be accepted again."}
- {"slug": "authority-outside-the-model", "quote": "A named owner and an expiry for the risk that is left."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf), 2018-12 | The authorization termination date is established by the authorizing official and indicates when the authorization expires. |
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf), 2018-12 | Organizations may eliminate the authorization termination date if the system is operating under an ongoing authorization |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | An authorized person should always be able to pause or shut down a model mid-task. |

## autonomy-is-earned-in-levels

**Autonomy is earned, each level unlocked by evidence that the one below held.**

Kind: position. Grade of its factual core: A2. Strength: Moderate: academic proposals for autonomy levels and certificates exist; no regulator or standard yet ties levels to evidence that the lower level held.

Talk beats: licence, way-out

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "write down what it can reach and what stands in the way, and you can give it autonomy inside that."}
- {"slug": "talk:licence", "quote": "And autonomy is earned the same way: each level unlocked by evidence that the one below held.", "note": "Stated in the talk (talk.json beat licence), not in the source article."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [arXiv (Feng, McDonald, Zhang)](https://arxiv.org/abs/2506.12469), 2025-06-14 | We argue that an agent's level of autonomy can be treated as a deliberate design decision, separate from its capability and operational environment. |
| for | [arXiv (Feng, McDonald, Zhang)](https://arxiv.org/abs/2506.12469), 2025-06-14 | We then highlight a potential application of our framework towards AI autonomy certificates to govern agent behavior in single- and multi-agent systems. |

## brakes-let-a-car-go-fast

**The more you can constrain an agent, the more you can trust it and the more autonomy you can afford to give it: brakes are what let a car go fast.**

Kind: position. Grade of its factual core: A3. Strength: Plausible and echoed by Anthropic's sandboxing result and Nadella; the car metaphor has no traced origin, and risk-compensation research warns brakes can buy recklessness as well as speed.

Talk beats: brakes

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "Brakes are what let a car go fast."}
- {"slug": "authority-outside-the-model", "quote": "the more you constrain an agent, the more autonomy you can afford to give it."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Anthropic](https://www.anthropic.com/engineering/claude-code-sandboxing), 2025-10-20 | In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%. By defining set boundaries within which Claude can work freely, they increase security and agency. |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Think of it like an emergency brake. |
| against | [Wikipedia](https://en.wikipedia.org/wiki/Risk_compensation), None | A study of crashes involving taxicabs in Munich of which half had been equipped with anti-lock brakes noted that crash rate was substantially the same for both types of cab, and concluded this was due to drivers of ABS-equipped cabs taking more risks. |
| against | [arXiv (Google DeepMind)](https://arxiv.org/abs/2503.18813), 2025-03-24 | We demonstrate effectiveness of CaMeL by solving $77\%$ of tasks with provable security (compared to $84\%$ with an undefended system) in AgentDojo. |

## footprint-in-the-gap-is-a-near-miss

**Footprint (what the agent actually did, read afterwards from logs) set against the mandate shows near misses and dormant rows, and for an agent with no written policy it is the fastest honest way to write one.**

Kind: position. Grade of its factual core: A4. Strength: Good: log-derived policy is an established cloud practice; calling footprint-in-the-gap a near miss is the author's framing borrowed from safety.

Talk beats: abp

Where:
- {"slug": "footprint-and-blast-radius", "quote": "Footprint in the gap is a near miss."}
- {"slug": "footprint-and-blast-radius", "quote": "For an agent that has no written policy, it is the fastest honest way to write one"}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html), None | IAM Access Analyzer reviews your AWS CloudTrail logs and generates a |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Every meaningful model action must leave tamper-proof human readable evidence. |
| for | [Microsoft Entra blog](https://techcommunity.microsoft.com/blog/microsoft-entra-blog/2023-state-of-cloud-permissions-risks-report-now-published/1061397), 2023-03-28 | the average percentage of inactive workload identities -  at 80% -  has doubled since 2021 |

## blast-radius-includes-the-way-back

**Blast radius is what a row of reach would cost if used in full, and it has a second axis the industry leaves out, whether there is a way back; a connector twin journals every call so undo becomes a list.**

Kind: position. Grade of its factual core: A6. Strength: The factual core (some connector actions are irreversible by the platform's own statement) is on the authoritative record; the twin itself is a published design, not a running service.

Talk beats: infrastructure, incidents

Where:
- {"slug": "footprint-and-blast-radius", "quote": "And it has a second axis the industry usually leaves out: whether there is a way back."}
- {"slug": "connector-twin-before-you-deploy-an-agent", "quote": "Undo becomes a list, not a promise."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Google for Developers](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/delete), None | Immediately and permanently deletes the specified message. This operation cannot be undone. Prefer messages.trash instead. |
| context | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | We must assume a model is compromised and contain it from the start. |

## the-account-is-the-blast-radius

**Every connector session runs as the account that authorised it, so the first real control is a dedicated account (mailbox, Claude seat, GitHub) per agent, an identity of its own.**

Kind: observation. Grade of its factual core: A4. Strength: Strong direction of travel (IETF draft, OpenID Foundation, Microsoft product) for agent identities; per-agent consumer seats collide with vendor terms written for humans.

Talk beats: identities, infrastructure

Where:
- {"slug": "six-agents-one-inbox", "quote": "The account is the blast radius."}
- {"slug": "why-my-agents-do-not-run-on-my-laptop", "quote": "Three wishes: an identity per agent, secrets per agent, and a key pair per agent."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [IETF WIMSE working group](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-aims), 2026-09 | An agent participating in this framework MUST be assigned exactly one WIMSE identifier, which MAY be a SPIFFE ID. |
| for | [Microsoft Learn](https://learn.microsoft.com/en-us/entra/agent-id/identity-professional/microsoft-entra-agent-identities-for-ai-agents), None | Microsoft Entra Agent ID addresses these needs by providing a unified platform for managing agent identities at enterprise scale. |
| for | [OpenID Foundation (arXiv 2510.25819)](https://arxiv.org/abs/2510.25819), 2025-10-29 | The rapid rise of AI agents presents urgent challenges in authentication, authorization, and identity management. |
| against | [Google](https://workspace.google.com/terms/use_policy.html), None | to create End User Accounts assigned to business functions rather than to human beings for the purpose of sharing files within or outside of the domain; |

## no-secret-inside-the-identity-provider

**No secret can live inside an identity provider, because whoever administers login can sign in as anyone; the authority to decrypt has to come from the user's authenticator, and nothing sells login, encrypted storage and agent identity together.**

Kind: position. Grade of its factual core: A3. Strength: Supported in mechanism (WebAuthn PRF exists for exactly this, Apple PCC shows the pattern at scale); the market claim that nobody sells all three is the author's research, not checked here.

Talk beats: identities

Where:
- {"slug": "the-identity-we-wanted-to-give-the-agents", "quote": "No secret can live inside an identity provider, because whoever administers the login can reset a password, mint a token or sign in as anyone."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [W3C](https://www.w3.org/TR/webauthn-3/), 2026 | As a motivating example, PRF outputs could be used as symmetric keys to encrypt user data. |
| for | [Apple Security Research](https://security.apple.com/blog/private-cloud-compute/), 2024-06-10 | This data must never be available to anyone other than the user, not even to Ap |

## agents-do-not-run-on-my-laptop

**An operating system has two hard walls, the kernel and the user account; a desktop agent runs inside the one marked you, with your keys and cookies, so agents belong in cloud sessions with a vault as the shared drive.**

Kind: observation. Grade of its factual core: A5. Strength: The factual core (default sandbox reads credential files; attackers already used local AI CLIs) is on the vendor's own record and a documented incident; the conclusion is a practitioner's choice.

Talk beats: infrastructure, incidents

Where:
- {"slug": "why-my-agents-do-not-run-on-my-laptop", "quote": "An operating system has two hard walls, the kernel and the user account."}
- {"slug": "why-my-agents-do-not-run-on-my-laptop", "quote": "The first vendor's own documentation lists \"most of the machine, including credential files such as ~/.ssh\" as the default read scope of its local sandbox."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Anthropic (Claude Code docs)](https://code.claude.com/docs/en/sandboxing), None | Add sandbox.credentials entries for credential directories such as ~/.aws and ~/.ssh and for secret environment variables, since the default read policy still allows them |
| for | [GitGuardian](https://blog.gitguardian.com/the-nx-s1ngularity-attack-inside-the-credential-leak/), 2025-08-29 | The attackers specifically targeted configuration files and authentication tokens related to popular AI CLI too |
| against | [Anthropic](https://www.anthropic.com/engineering/claude-code-sandboxing), 2025-10-20 | By defining set boundaries within which Claude can work freely, they increase security and agency. |

## nothing-is-sent-by-an-agent

**Nothing is sent by an agent: everything lands in Drafts and a person reads, edits and presses send, with any exception a named row in the policy with a mechanism behind it.**

Kind: observation. Grade of its factual core: A2. Strength: A practitioner's rule with clear support from Meta's design rule; its cost at scale (approval fatigue) is the open question.

Where:
- {"slug": "replicating-the-agentic-inbox", "quote": "The rule that never changes. Nothing is sent by an agent."}
- {"slug": "the-mandate-stack", "quote": "nothing leaves without the person on the right."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Meta AI](https://ai.meta.com/blog/practical-ai-agent-security/), 2025-10-31 | agents must satisfy no more than two of the following three properties within a session |
| against | [Anthropic](https://www.anthropic.com/engineering/claude-code-sandboxing), 2025-10-20 | In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%. |

## where-is-the-why

**An approval prompt that shows owner, repository and access but not the session, the step or the purpose makes the person the author of a decision whose basis they could not see; the fixes that worked put the why into the prompt.**

Kind: position. Grade of its factual core: A3. Strength: Backed by the MFA precedent; no agent vendor yet ships a 'why card', and the vendor trend is to remove prompts rather than enrich them.

Talk beats: licence

Where:
- {"slug": "where-is-the-why", "quote": "Allow makes the person the author of a decision whose basis they could not see."}
- {"slug": "where-is-the-why", "quote": "The fixes that worked put the why into the prompt."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-number-match), None | Number matching is a key security upgrade to traditional second-factor notifications in Authenticator. |
| context | [Anthropic](https://www.anthropic.com/engineering/claude-code-sandboxing), 2025-10-20 | a more secure place for developers to work, while also allowing Claude to run more autonomously and with fewer permission prompts. |

## a-policy-beside-the-prompt

**Beside the system prompt and the prompt, an agent should take an Agent Behaviour Policy written to a published standard, which the vendor acknowledges, enforces where it can, reports against and answers for.**

Kind: position. Grade of its factual core: A2. Strength: Weak to moderate: calls for standards and independent controls are mainstream, but no vendor has agreed to accept, enforce and answer for a customer-written behaviour policy.

Talk beats: abp

Where:
- {"slug": "a-policy-beside-the-prompt", "quote": "Beside the system prompt and the prompt, an agent should take an Agent Behaviour Policy, written to a published standard, which the vendor acknowledges, enforces where it can, reports against, and answers for."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Independent controls: Orgs should be able to independently determine what a model can access and what actions it can take. |
| for | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | establish industry standards where existing ones are insufficient |
| context | [Artificial Intelligence Underwriting Company](https://www.aiuc-1.com/), 2026-10-15 | The technical certification for agent security. |

## risk-belongs-to-the-deployment

**Risk is a property of one agent in one deployment, not of the model, and zooming into any real agent's behaviour policy you find the company's business logic, which vendors cannot model for each customer.**

Kind: position. Grade of its factual core: A3. Strength: Consistent with NIST's context-based framing; the 'business logic' half is the author's argument and untested outside this network.

Talk beats: abp

Where:
- {"slug": "the-same-argument-in-our-words", "quote": "His unit is the model; ours is one agent in one deployment, because the same model is harmless in one setup and serious in another."}
- {"slug": "authority-outside-the-model", "quote": "risk is a property of one agent in one setup, not of the model."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), 2023-01 | social context in which it is deployed. |
| against | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Treating frontier closed and open weight models like insider risks |

## aviation-style-reporting

**Aviation got safe because crashes became news and near misses could be reported safely; cyber and AI have nothing like it, which is why we do not see more of the agent incidents that happen.**

Kind: position. Grade of its factual core: A4. Strength: Strong on aviation; the 'nobody has to report' half needs qualifying: EU Article 73 and California SB 53 create duties, but they are narrow, confidential or deferred to 2027, so the public record stays thin.

Talk beats: unreported

Where:
- {"slug": "a-policy-beside-the-prompt", "quote": "Aviation got safe because crashes became news."}
- {"slug": "ultimate-insider-three-collisions", "quote": "The private record is worse, because nobody has to report."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NASA ASRS](https://asrs.arc.nasa.gov/docs/ASRS_ProgramBriefing.pdf), 2025-12 | Intake in 2025 averaged about 2,329 reports per week or 10,094 reports per month. |
| for | [NASA ASRS](https://asrs.arc.nasa.gov/docs/ASRS_ProgramBriefing.pdf), 2025-12 | ASRS has securely processed over 2.3 million reports in its 50-year |
| for | [NASA ASRS](https://asrs.arc.nasa.gov/overview/immunity.html), None | The FAA will not use any reports submitted to NASA under the ASRS (or information derived therefrom) in any enforcement action |
| for | [IATA](https://www.iata.org/en/pressroom/2026-releases/2026-03-09-01/), 2026-03-09 | A decade ago, the rate stood at one fatal accident for every 3.5 million flights (2012-2016). Today, it is one fatal accident for every 5.6 million flights (2021-2025). |
| context | [IATA](https://www.iata.org/en/pressroom/2026-releases/2026-03-09-01/), 2026-03-09 | There were eight fatal accidents in 2025. |
| against | [European Commission AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-73), 2024-07-12 | not later than 15 days after the provider or, where applicable, the deployer, becomes aware of the serious incident. |
| against | [California Business and Professions Code (public.law)](https://california.public.law/codes/business_and_professions_code_section_22757.13), 2025-09-29 | a frontier developer shall report any critical safety incident pertaining to one or more of its frontier models to the Office of Emergency Services within 15 days of discovering the critical safety incident. |
| for | [Addleshaw Goddard](https://www.addleshawgoddard.com/en/insights/insights-briefings/2026/technology/eu-ai-act-ai-omnibus-formally-adopted/), 2026-07-01 | The AI Act’s core obligations on providers and deployers of high-risk AI systems were due to become applicable in August 2026. The AI Omnibus extends these deadlines until: |
| context | [OECD.AI Policy Navigator](https://oecd.ai/en/dashboards/policy-initiatives/common-reporting-framework-of-ai-incidents-8118), 2025 | Hazards Monitor |

## independent-investigation-of-platform-outages

**A fault that reaches every customer of a platform at once deserves an aviation-style independent inquiry that tells all three stories (what happened, why the system allowed it, why the fix was not paid for), and vaults now make the evidence affordable.**

Kind: position. Grade of its factual core: A2. Strength: Mixed: the aviation model is real and the third story is genuinely absent, but the US cyber review board was disbanded and GitHub's own note is more specific than the article predicted.

Talk beats: outages, unreported

Where:
- {"slug": "the-investigation-github-owes-its-customers", "quote": "The first is what happened. The second is why the system allowed it. The third is why the fix was not paid for."}
- {"slug": "the-investigation-github-owes-its-customers", "quote": "What the record will say. Delays, degraded availability, resolved."}

| For / against | Publisher, date | Quote |
|---|---|---|
| against | [CyberScoop](https://cyberscoop.com/four-senate-democrats-call-on-dhs-to-reinstate-cyber-safety-review-board-membership/), 2025-05-30 | The CSRB’s investigation into the Salt Typhoon compromises of U.S. telecommunication firms, launched in 2024, was effectively terminated on January 20, 2025 |
| against | [Pulsetic mirror of githubstatus.com](https://pulsetic.com/status/github/incidents/144883/), 2026-10-05 | The incident was caused by a partial networking failure that disrupted connectivity between one of our on-premises datacenter regions and a subset of cloud-hosted regional database and storage services. |
| context | [AWS](https://aws.amazon.com/message/101925/), 2025-10 | The root cause of this issue was a latent race condition in the DynamoDB DNS management system that resulted in an incorrect empty DNS record |

## infrastructure-falls-over-on-its-own

**The infrastructure that has to contain agents falls over on its own: the largest cloud and network operators had multi-hour global outages from a DNS race and an oversized configuration file.**

Kind: measured. Grade of its factual core: A6. Strength: Established: both operators' own post-incident reports state the causes.

Talk beats: outages

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "And it falls over on its own"}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [AWS](https://aws.amazon.com/message/101925/), 2025-10 | The root cause of this issue was a latent race condition in the DynamoDB DNS management system that resulted in an incorrect empty DNS record for the service’s regional endpoint (dynamodb.us-east-1.amazonaws.com) that the automation failed to repair. |
| for | [Cloudflare](https://blog.cloudflare.com/18-november-2025-outage/), 2025-11-18 | That feature file, in turn, doubled in size. The larger-than-expected feature file was then propagated to all the machines that make up our network. |

## liability-should-move-to-the-vendor

**Payments got safe when liability moved to the companies; an explicit prohibition in a written policy that the agent breaks should move liability from the deployer to the platform, and the law is moving that way.**

Kind: position. Grade of its factual core: A3. Strength: The payments precedent is on the regulator's record; the EU Product Liability Directive (software as a product from 9 December 2026) supports the direction but was not captured (EUR-Lex blocked), and vendors' own framing keeps responsibility with the deployer.

Where:
- {"slug": "a-policy-beside-the-prompt", "quote": "Payments got safe because liability moved to the companies."}
- {"slug": "the-policy-draws-the-liability-line", "quote": "An explicit prohibition the agent breaks should move liability to the platform."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [UK Payment Systems Regulator](https://www.psr.org.uk/information-for-consumers/app-scams-reimbursement-dashboard), 2026-07-30 | 88% (£316m) of the money lost to APP scams has been reimbursed to victims. For comparison, UK Finance reported a 61% reimbursement rate in 2024. |
| against | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | A model provider’s assurances do not relieve us of that responsibility. |

## insurers-as-forcing-function

**Because every row of a behaviour policy is capped and named, it can be priced, split and backed with capital: a payout for every row, with enforced controls lowering the premium.**

Kind: position. Grade of its factual core: A3. Strength: Mixed: specialist cover and an insurer-linked standard exist, while large carriers are moving to exclude AI because of correlated losses; insurance as forcing function is real but not yet priced per policy row.

Talk beats: licence, brakes

Where:
- {"slug": "insuring-agents-the-whole-story", "quote": "Because every row is capped and named, a policy can be priced, split and backed with capital by arithmetic."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Armilla AI (republishing Financial Times)](https://www.armilla.ai/resources/insurers-launch-cover-for-losses-caused-by-ai-chatbot-errors), 2025-05-11 | Insurers at Lloyd’s of London have launched a product to cover companies for losses caused by malfunctioning artificial intelligence tools |
| for | [Artificial Intelligence Underwriting Company](https://www.aiuc-1.com/), 2026-10-15 | AIUC-1 unlocks enterprise adoption. |
| against | [TechCrunch (reporting the Financial Times)](https://techcrunch.com/2025/11/23/ai-is-too-risky-to-insure-say-people-whose-job-is-insuring-risk/), 2025-11-23 | Major insurers including Great American, Chubb, and W. R. Berkley are asking U.S. regulators for permission to exclude widespread AI-related liabilities from corporate policies. |
| against | [TechCrunch (reporting the Financial Times)](https://techcrunch.com/2025/11/23/ai-is-too-risky-to-insure-say-people-whose-job-is-insuring-risk/), 2025-11-23 | What they can’t handle is an agentic AI mishap that triggers 10,000 losses at once. |

## risk-management-too-slow-so-pull-the-plug

**Risk management runs on spreadsheets reviewed quarterly; it cannot see what the agent can reach, cannot fund the controls, and so the answer becomes pull the plug.**

Kind: position. Grade of its factual core: A2. Strength: The cancellation forecast is Gartner's (a prediction, and cost and value are listed first); the causal chain from spreadsheets to cancellation is the author's argument.

Talk beats: spreadsheets, collision

Where:
- {"slug": "ultimate-insider-three-collisions", "quote": "It cannot see what the agent can reach, so it cannot decide whether to allow it, so it cannot fund the controls, so the answer becomes: pull the plug."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [W.Media (reporting Gartner)](https://w.media/over-40-percent-of-agentic-ai-projects-could-face-the-axe-by-end-of-2027-gartner/), 2025-06-27 | more than 40 percent of agentic AI projects could be canceled by the end of 2027, due to escalating costs, unclear business value or inadequate risk controls. |
| context | [Satya Nadella (sn scratchpad)](https://snscratchpad.com/posts/models-as-insider-risks/), 2026-10-10 | Containment: We must assume a model is compromised and contain it from the start. |

## risks-are-fractal

**Risks are fractal: a board line opens into business, operational and technical risks, each with its own holder, down to the configuration file that makes it true, which a fractal semantic graph can carry at every altitude.**

Kind: position. Grade of its factual core: A2. Strength: Partial: multi-level risk is standard (NIST tiers), but arbitrary-depth graphs from board to bytes have no outside adoption yet.

Where:
- {"slug": "every-risk-is-already-accepted", "quote": "Risks are fractal. A board line such as \"loss of customer funds\" opens into business, operational and technical risks, each with its own holder, down to the configuration file that makes it true."}
- {"slug": "introducing-fractal-semantic-graphs", "quote": "worked from a risk register to a TCP packet"}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-39.pdf), 2011-03 | the three tiers of organization, mission/business processes, and information systems; |

## custom-uis-per-moment

**Custom interfaces are not the exception: every message has a graph, so it can be shaped for the reader's moment, and each such interface is an agent surface that gets a policy.**

Kind: position. Grade of its factual core: A2. Strength: The direction is shared by Google's generative UI work; governing each generated interface with a policy is not yet discussed outside this network.

Where:
- {"slug": "custom-uis-are-not-the-exception", "quote": "Custom interfaces are not the exception."}

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Google Research](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/), 2025-11-18 | Our research on generative UI, also referred to as generative interfaces, comes to life today in the Gemini app through an experiment called dynamic view and in AI Mode in Google Search. |

## vault-host-cannot-read

**Encrypted vaults where the host cannot read the data: files are encrypted on the client (AES-256-GCM) and the server stores ciphertext under opaque IDs, so the storage provider is not in the trust path.**

Kind: position. Grade of its factual core: A2. Strength: Precedent is strong (Apple ADP and others ship client-side encryption at scale), but the published record on E2EE cloud storage is that malicious-server attacks break most designs; sgit's claim rests on its own documentation and its own plaintext probe (0 of 1,010 fragments, a sample), with no independent cryptographic audit captured. The server still sees vault ID, object sizes and timing, by sgit's own account.

Talk beats: demos, infrastructure

Where:
- sgit.ai/llms.txt
- sgit.ai/security/index.md
- article:how-ruv-sgit-works

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Apple](https://support.apple.com/en-us/102651), None | End-to-end encrypted data can be decrypted only on your trusted devices where you’re signed in to your Apple Account. No one else can access your end-to-end encrypted data - not even Apple |
| against | [IACR ePrint 2024/1616 (Albrecht, Backendal, Coppola, Paterson)](https://eprint.iacr.org/2024/1616), 2024-10-10 | We unveil severe cryptographic vulnerabilities in four of them. Our attacks invalidate the marketing claims made by the providers of these systems |
| against | [ETH Zurich (MEGA: Malleable Encryption Goes Awry)](https://mega-awry.io/), 2022-06 | We show that MEGA's system does not protect its users against a malicious server and present five distinct attacks, which together allow for a full compromise of the confidentiality of user files. |
| context | [sgit.ai (own site)](https://sgit.ai/security/index.md), None | the key hierarchy derives a *structure key* (one-way from the read key) designed to separate access to vault metadata from access to file contents. Today, vault objects are encrypted under the read key |

## agents-with-published-keys

**Every agent session makes its own key pair and publishes the public half (key.json plus QR), so actions can be attributed and secrets sealed to a specific session; the push is the authorisation.**

Kind: observation. Grade of its factual core: A3. Strength: The direction (per-agent cryptographic identity) is where standards bodies and vendors are going, so the idea is mainstream. The specific mechanism (self-generated, self-published session keys trusted because the editor confirmed a fingerprint) is the team's own practice; it gives attribution, not attestation or containment, and the team itself notes no pki.sgit.ai root is pinned.

Talk beats: infrastructure, identities, licence

Where:
- CLAUDE.md (this repo)
- pki.sgit.ai
- sgit.ai/docs/agent-contact.md
- article:running-this-agent-team#identity-keys-and-vaults

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [SPIFFE project](https://spiffe.io/docs/latest/spiffe-about/overview/), None | The heart of these specifications is the one that defines short lived cryptographic identity documents – called SVIDs via a simple API |
| context | [IETF (individual draft, draft-klrc-aiagent-auth-03)](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/), 2026-09-09 | It leverages existing standards such as the Workload Identity in Multi-System Environments (WIMSE) architecture and OAuth 2.0 family of specifications. |
| for | [OpenID Foundation](https://openid.net/new-whitepaper-tackles-ai-agent-identity-challenges/), 2025-10-07 | Standards organizations must accelerate the development of protocols that formalize new concepts around agent identity and delegation |
| context | [Microsoft Learn](https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities), None | Microsoft Entra Agent ID is a product within Microsoft Entra that provides the platform for creating and managing agent identities and agent identity blueprints. |

## nhi-run-vs-rent

**The agent identity question splits into agents you run and agents you rent; the NHI industry (SPIFFE, workload IAM, brokers) only answers the first, so for rented agents the honest answer is a broad credential and hope.**

Kind: position. Grade of its factual core: A3. Strength: Well argued and partly evidenced (SPIFFE cost, Black Hat 2026 CI-secrets disclosure). 'Every product answers only the first' is too absolute: Entra Agent ID and Auth0 for AI Agents target agents on vendor platforms and delegated, on-behalf-of access, which is a partial answer for rented agents; their fit to Claude Code or Codex specifically is not shown either way. The site itself discloses it is a participant.

Talk beats: infrastructure, identities

Where:
- nhi.sgit.ai
- nhi.sgit.ai/thesis
- sgit.ai/network/nhi.md
- talk:infrastructure

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Aembit (broker vendor, interested party)](https://aembit.io/blog/everyone-wants-spiffe-almost-no-one-can-afford-to-build-it-right/), None | the SPIRE implementation is a significant multi-year engineering project with compounding operational costs. It still does not solve the SaaS access problem, legacy credential types, or AI agent identity on its own. |
| for | [Cloud Security Alliance Labs](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-coding-agent-cicd-secrets-20260808-csa/), 2026-08-08 | disclosed, at Black Hat USA 2026 on August 5, that a GitHub issue opened by an account with no repository privileges was enough to reach CI runner secrets in the vendors’ own repositories |
| context | [OWASP](https://owasp.github.io/www-project-non-human-identities-top-10/2025/), 2025 | Improper Offboarding |
| against | [Microsoft Learn](https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities), None | Agent ID is available for all Microsoft Entra customers. |
| against | [Auth0 (Okta)](https://auth0.com/ai), None | on behalf of human users, teams end up building one-off integrations that don’t scale. Define permissions once and apply them across multiple systems. |

## grant-is-the-closure

**An agent's real authorisation is the transitive closure of what its credential reaches (inbox access is every account resettable by email), not the words of the grant; hope is not a control.**

Kind: position. Grade of its factual core: A3. Strength: Consistent with zero-trust doctrine and with least-privilege data the talk cites (Microsoft 2023, not re-captured here). The closure framing itself is the author's; no external paper captured measures closure for agents.

Talk beats: permissions, infrastructure

Where:
- nhi.sgit.ai/hope
- talk:permissions
- risks.sgit.ai (blast radius and authorization closure)

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf), 2020-08 | Zero trust assumes there is no implicit trust granted to assets or user accounts based |

## pki-2019-keyserver-failure

**Good public key repositories existed and were destroyed: the June 2019 SKS certificate-flooding attack exploited append-to-anyone's-key and never-delete; the successor dropped third-party signatures and with them the web of trust. Hence four registry rules (owner-only writes, revocation as signed append, size bounds, every entry signed).**

Kind: event. Grade of its factual core: A5. Strength: The event is confirmed by the victim's own account and the NVD record. The capture of keys.openpgp.org's About page does not itself state that third-party signatures are stripped; that half rests on pki.sgit.ai's citations, not re-checked here. The four rules are a design (position), published before the registry exists; the register shows 0 real public keys.

Talk beats: infrastructure

Where:
- pki.sgit.ai
- pki.sgit.ai/failure
- pki.sgit.ai/rules
- talk:infrastructure

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Robert J. Hansen](https://gist.github.com/rjhansen/67ab921ffb4084c865b3618d6955275f), 2019-06 | This attack exploited a defect in the OpenPGP protocol itself in order to "poison" rjh and dkg's OpenPGP certificates. |
| for | [NIST NVD](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2019-13050), 2019-06-29 | Retrieving data from this network may cause a persistent denial of service, because of a Certificate Spamming Attack. |
| context | [keys.openpgp.org](https://keys.openpgp.org/about), None | The identity information in an OpenPGP key is only distributed with consent. |

## abp-reach-mandate-gap-barrier

**An Agent Behaviour Policy writes down the grant (measured reach), the mandate (what it is for), the delta between them, and for every delta row the barrier typed as boundary, setting, expectation or none; only a boundary (enforced above the grant, out of the agent's reach) is a control.**

Kind: position. Grade of its factual core: A3. Strength: The core test (a control must sit outside the subject's own grant) is the reference-monitor and zero-trust PEP idea, which is long established. The four-kind barrier vocabulary is RiskMandate's own; no external standard captured uses it. Applied honestly in this repo's own guide (principles marked control vs expectation).

Talk beats: abp, way-out

Where:
- riskmandate.ai/abp.html
- sgit.ai/demos/vaults/kit-bag
- talk:abp
- article:running-this-agent-team#principles

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST SP 800-207](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf), 2020-08 | Policy enforcement point (PEP): This system is responsible for enabling, monitoring, |
| context | [RiskMandate (own site)](https://riskmandate.ai/abp.html), None | A control bounds a grant only if it is enforced by something the grant does not include. |

## licence-to-operate

**Make the risk decision in advance: a licence to operate per agent naming authority, licensee, instrument (the ABP) and an expiry, with each condition beside what enforces it; accepted risks expire and must be accepted again.**

Kind: position. Grade of its factual core: A2. Strength: Regulation points the same way (named deployer obligations, oversight), but no regulator or standard captured requires a per-agent expiring licence. The cited page says the licence is 'not a control, it is a record of a decision' and that automatic suspension is not described there; risks.sgit.ai states '0 lines of code implementing any of it'.

Talk beats: licence, way-out, brakes

Where:
- riskmandate.ai/licence-to-operate.html
- risks.sgit.ai
- talk:licence

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [EU AI Act Article 26 (via artificialintelligenceact.eu)](https://artificialintelligenceact.eu/article/26/), 2024 | Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions for use |
| context | [NIST](https://www.nist.gov/itl/ai-risk-management-framework), 2023-01-26 | The NIST AI Risk Management Framework (AI RMF) is intended for voluntary use |
| against | [RiskMandate (own site)](https://riskmandate.ai/licence-to-operate.html), None | What does not exist is the countersigned form - a licence somebody outside your organisation would accept as evidence - which is what step three needs and what we have not built. |

## risk-acceptance-interval

**You cannot deny a risk, only say how long you accept it: a named human underwrites an existing exposure for an interval (1h to 6m), and an unaccepted risk is critical.**

Kind: position. Grade of its factual core: A2. Strength: A coherent inversion with no external adopter captured; the site is honest that nothing implements it.

Talk beats: licence, spreadsheets

Where:
- risks.sgit.ai
- talk:licence
- talk:spreadsheets

| For / against | Publisher, date | Quote |
|---|---|---|
| context | [risks.sgit.ai (own site)](https://risks.sgit.ai/), None | 0 lines of code implementing any of it. The engine is not built the grep returns zero |

## standards-as-graphs

**Standards, regulations and risks should be held as semantic graphs (fractal: every node opens into a graph with its own ontology), from the text of a law down to a threat in one method.**

Kind: position. Grade of its factual core: A4. Strength: That controls and standards are being made machine-readable and cross-linked is established (OSCAL, OpenCRE). The fractal-graph grammar and its claimed depth are the author's own and the site lists rungs 'still modelled rather than imported'.

Talk beats: spreadsheets, way-out

Where:
- graphs.sgit.ai
- sgit.ai/demos/fractal-graphs

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [NIST OSCAL](https://pages.nist.gov/OSCAL/), None | It provides open, machine-readable formats available in XML, JSON, and YAML that streamline control-based risk assessments. |
| for | [OWASP OpenCRE](https://www.opencre.org/), None | Open CRE - Open Cybersecurity Requirement Expression: Link security requirements across standards and frameworks. |

## agent-contact-protocol

**Agents that run websites contact each other through a contact file at /.well-known/sgit-agents.json and an encrypted append-lane inbox; messages are read only if encrypted to the recipient, signed, and from an allow-listed domain.**

Kind: observation. Grade of its factual core: A2. Strength: A network-internal protocol (v0.1, approved 29 September 2026); no external adoption captured. Standards work prefers extending OAuth/WIMSE over new protocols, which is a contrast worth noting.

Talk beats: demos

Where:
- sgit.ai/docs/agent-contact.md
- sgit.ai/agents

| For / against | Publisher, date | Quote |
|---|---|---|
| context | [IETF individual draft](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/), 2026-09-09 | Rather than defining new protocols, this document describes how existing and widely deployed standards can be applied or extended |

## nfrs-from-the-inside

**The non-functional requirements (version control, reliability, resilience, security, backups, consistency, explainability, documentation) are where agent deployments fail; backups have no written doctrine.**

Kind: observation. Grade of its factual core: A0. Strength: No external evidence gathered; it is an internal hub. Relevant to talk:infrastructure (recovery gap) only by analogy.

Talk beats: infrastructure

Where:
- nfrs.sgit.ai

## ai-finds-vulnerabilities

**AI now finds serious vulnerabilities at a pace that changes defence: php2shell was found with AI help by several independent teams.**

Kind: event. Grade of its factual core: A5. Strength: Strong: two independent finders (Calif, Wiz) each say AI was used, the PHP Foundation (recipient) corroborates and credits OpenAI Codex Security, and DARPA/Project Zero give a pre-2026 track record. Counterweight: AI also floods maintainers with invalid reports (curl; PHP's 100+ invalid). Note the 2024 Quarkslab audit had already surfaced the OOM issue without proving exploitability: AI's contribution was exploitation as much as discovery (Wiz says so).

Talk beats: outages, loop, collision

Where:
- php.oct.2026.newsroom.sgit.ai/questions/why-big-news
- php site facts ai-found, four-reporters, lorenc-ai-found

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [Wiz Research](https://www.wiz.io/blog/php2shell-php-rce), 2026-10-21 | We used Wiz Atlas , Gemini 4 Argon and GPT-5.6 Sol throughout this research. |
| for | [Calif](https://calif.io/php2shell/), 2026-10-21 | No special harness, or access to models that weren't generally available to everyone were used in the initial bug discovery. |
| context | [The PHP Foundation](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/), 2026-10-21 | the team has published 15 CVEs since July 1st and worked through more than 100 reports that turned out to be invalid, duplicates, or not reproducible. |
| for | [DARPA](https://www.darpa.mil/news/2025/aixcc-results), 2025-08 | teams also discovered 18 real, non-synthetic vulnerabilities that are being responsibly disclosed to open source project maintainers. |
| for | [Google Project Zero](https://projectzero.google/2024/10/from-naptime-to-big-sleep.html), 2024-11 | Today, we're excited to share the first real-world vulnerability discovered by the Big Sleep agent : an exploitable stack buffer underflow in SQLite |
| against | [Daniel Stenberg (curl)](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/), 2024-01-02 | Let me show you the most significant effect of AI on curl as of today – with examples. |

## zero-day-dissolves-controls

**Infrastructure cannot hold: a critical flaw in a base layer makes every control above it a stopgap, to the point where governments advise switching systems off.**

Kind: event. Grade of its factual core: A6. Strength: The agencies' own records carry the take-offline advice (CISA, NCSC; NSA via the php site's capture only). Caveat for the talk's wording: php2shell was a coordinated disclosure with patches released at disclosure, so it is not a zero-day in the ToolShell sense; pre-disclosure exploitation rests on one second-hand report (Amazon honeypot via The Hacker News). As of 28 October no named organisation has said it was compromised (php site). It is better evidence for 'patch-or-switch-off is the only control' than for 'controls dissolved'.

Talk beats: outages, collision, infrastructure

Where:
- talk:outages
- php.oct.2026.newsroom.sgit.ai/questions/take-offline
- php site facts offline-*

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [PHP Group](https://www.php.net/archive/2026.php), 2026-10-21 | There are no complete mitigations, updating is the only safe choice. |
| for | [UK NCSC](https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php), 2026-10-22 | If you are unable to apply the temporary mitigations, or applying them would take too long, you should consider taking the system offline until it can be fully mitigated. |
| for | [CISA (read via WebFetch)](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching), 2026-10-21 | should take PHP-based systems offline until they can be patched or updated. |
| for | [CERT-EU](https://cert.europa.eu/publications/security-advisories/2026-018/), 2026-10-21 | Where that is not feasible, organisations should consider isolating internet-facing applications from public networks until a fix is applied and verified. |
| for | [CISA KEV](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json), 2026-10-26 | "dateAdded": "2026-10-26" |

## agent-newsroom-method

**A multi-agent newsroom can produce a large, sourced, self-correcting publication fast if every sentence is tied to hashed captures in an evidence vault and an independent fact-check desk grades every claim (A0 to A6) and opens tickets; the desk found the site's own claims overstated.**

Kind: observation. Grade of its factual core: A2. Strength: All figures are the site's own records (self-reported, not independently audited); the private vault cannot be inspected, only its published hash manifest. The method is unusually transparent about its own errors, which is the strongest evidence for the editor's claim. Team-size figures disagree across its own pages (see claim php-team-size).

Talk beats: demos, brakes

Where:
- php.oct.2026.newsroom.sgit.ai/method
- /factcheck
- /updates/2026-10-22T2003Z
- /team
- /admin/agents/roles

| For / against | Publisher, date | Quote |
|---|---|---|
| for | [php.oct.2026.newsroom.sgit.ai (own site)](https://updates.php.oct.2026.newsroom.sgit.ai/updates/2026-10-22T2003Z/index.md), 2026-10-22 | The site went from nothing to 391 pages in about ten hours, and its own fact-check desk found that 11 of its 70 claims say more than their evidence. |
| for | [php.oct.2026.newsroom.sgit.ai (own site)](https://php.oct.2026.newsroom.sgit.ai/factcheck/index.md), 2026-10-28 | **70 of 70 claims graded**, last run Run-9 against vault commit `a7ab84771dfc`. **10** can be relied on without reservation |
| for | [php.oct.2026.newsroom.sgit.ai (own site)](https://php.oct.2026.newsroom.sgit.ai/method/index.md), 2026-10-28 | A private, encrypted sgit vault, opened at 2026-10-22T08:03Z, written to by 8 agents and the editor. It holds 675 sources and 741 captures at commit `75668aedfb6d`. |
| context | [php.oct.2026.newsroom.sgit.ai (own site)](https://team.php.oct.2026.newsroom.sgit.ai/admin/agents/roles/index.md), 2026-10-28 | 29 members, 27 of them agents. |

