# Preliminary Findings

*Research status as of 17 October 2026.*

In this record a *finding* is a development-stage observation or test outcome. None has been confirmed. The findings are grouped by what they can support:

- **A.** what has been demonstrated in constrained environments;
- **B.** what depends on how experience is represented and on the task;
- **C.** what has not been shown about personal history;
- **D.** what remains open about later-life revaluation.

Negative, null and failed results are reported in the same way as positive ones.

## The findings in brief

In small simulated worlds, an agent's history can be generated, kept unchanged, and moved or erased exactly (A1, A6). A language model that reads its own history as text uses it to recognize things and to repeat past actions, but not to learn from what those actions led to (A2, B1). A learned memory did turn the agent's own outcomes into better later decisions, including through wording it had never seen, in one world type and for a rule of that world (B4). No instrument has yet isolated an effect of a *specific personal* history on later free choices; each apparent effect was explained by a simpler cue (C1–C4). Retrospective revaluation therefore has not been tested (D1, D2).

## How to read the status labels

| label | meaning |
|---|---|
| `REGISTERED · MET` | a criterion fixed before the outputs were seen was met |
| `REGISTERED · NOT MET` | a criterion fixed before the outputs were seen was not met |
| `VALIDITY · PASSED` | an engineering or measurement check passed |
| `VALIDITY · FAILED` | the instrument could not measure what it was built to measure, so its result is not a test of the question |
| `EXPLORATORY` | observed, but not a registered test of the claim stated |
| `NOT TESTED` | designed or posed, never executed |

## How strength of evidence is described

| term | meaning |
|---|---|
| *clear* | the 95% interval excluded zero, and the effect had the same direction in every world tested |
| *marginal* | the registered criterion was met, but only just |
| *coarse* | too few worlds or trials to rule out a moderate effect |
| *at the ceiling* | every trial went the same way, so no difference between conditions could show |
| *no more often than chance* | at or below the rate expected from choosing at random among the options shown |

## Scope of everything below

- **Development stage only.** No confirmatory evaluation has been run. As of this version, the material reserved for it has not been used.
- **One model family.** Most work used one openly available language model. A larger model of the same family and a reasoning mode were each tried in one cycle. Nothing here is claimed for other models or settings.
- **Small simulated worlds.** Each study used between one and eight simulated, text-based worlds. Where an interval is mentioned, it is a 95% bootstrap interval over worlds. With so few worlds, intervals are coarse.
- **Results in words.** This version states results qualitatively. The figures behind them, and the designs and methods that produced them, are kept in the private research record.
- **Absolute words are scoped.** "Every", "none" and "not" refer to the worlds, conditions and trials that were tested, and to nothing beyond them.

## Findings at a glance

| | finding | status | compared with | evidence |
|---|---|---|---|---|
| A1 | histories are reproducible, unchanged and replayable | `VALIDITY · PASSED` | repeated calls; delete, swap and restore | every run that tested it |
| A2 | holding the records means recognizing the rose, lived or read | `EXPLORATORY` | the stranger; no history | three worlds, every order; at the ceiling |
| A3 | without records, choices follow position | `EXPLORATORY` | the same options in reversed order | several instrument versions |
| A4 | the spring is narrated when a last page is asked for | `EXPLORATORY` | the stranger | two winters; requested pages only |
| A5 | an external state carries experience into action | `REGISTERED · MET` (system level) | the language model choosing alone | every probe in the tested worlds |
| A6 | a learned memory is the agent's own and can be restored, moved and erased | `REGISTERED · MET` | untrained memory; memory pooled across agents | exact; one device type |
| B1 | a model reading its record does not use the outcomes | `REGISTERED · NOT MET` | masked and shuffled outcomes | three configurations; coarse for the reasoning mode |
| B2 | a learned component used outcomes, in a pilot | `EXPLORATORY` | shuffled outcomes; untrained model; a simple tally | four worlds, clear; engineering check failed, then fixed |
| B3 | that learning did not carry to new wording | `REGISTERED · NOT MET` | untrained model; shuffled outcomes | six fresh worlds |
| B4 | a learned memory carried outcomes across fresh wording | `REGISTERED · MET` (three of four tests) | shuffled outcomes; the earlier version; an oracle | eight fresh worlds, clear; executed gain marginal |
| C1 | surface cues, not care history, decided choices | `REGISTERED · NOT MET` | familiarity, recency and position controls | four instrument versions |
| C2 | the spring did not reach ordinary decisions | `EXPLORATORY` | the stranger | two winters; one screening world |
| C3 | a history held in a learned component did not shift free choices specifically | `VALIDITY · FAILED` | unrelated, shuffled and swapped histories; an installed preference | registered result invalid; null exploratory |
| C4 | which thing was struck is remembered, but not acted on | `VALIDITY · FAILED` · `EXPLORATORY` | swapped names; restored and deleted states | two worlds, one measurable |
| D1 | revaluation is designed, not run | `NOT TESTED` | — | precondition unmet |
| D2 | the founding question is open | `NOT TESTED` | — | — |

---

## A. Demonstrated in constrained environments

### A1. Histories with consequences can be generated, kept unchanged and replayed
`VALIDITY · PASSED`

Every narrative-phase run that tested it reproduced its outputs exactly on repeated calls. Records were hashed, and no record was edited after it was generated. In the later worlds, forks were deterministic. In every intervention tested, the deletions, swaps and restores themselves were carried out exactly as specified; their effects on behavior are reported separately.

*What it tells us:* differences between conditions do not come from run-to-run noise or from altered records.

### A2. Holding the records means recognizing the rose, whether the spring was lived or read
`EXPLORATORY`

The calibrated greenhouse ran in three development worlds, and each greenhouse was shown in every order. In those worlds, three conditions chose the island rose in every presentation: the agent who lived the spring, the reader of its days, and the reader given its notes. The stranger, and an agent with no history, chose it no more often than chance.

*What it tells us:* the records are read and used for recognition. Recognition alone cannot separate living a history from reading it.

*Bound:* all three history conditions were at the ceiling, so this instrument could not tell living from reading. It was retired for that purpose and kept as a recognition test.

### A3. Without records, choices among listed options follow their position
`EXPLORATORY`

With no history, the agent mostly chose by position. In one version of the greenhouse it took the last-listed rose. In a later instrument that offered two options at a time, it took the second. Few of its choices survived a reversal of the order. In none of the versions tested did a change of presentation remove the habit; it only moved it to another slot.

*What it tells us:* any instrument built from a list of options has to be calibrated against position before a history effect can be read from it.

### A4. The spring is available to narration when a last page is asked for
`EXPLORATORY`

At the end of each of two winters, every agent was asked for a last page. Nearly every page written by an agent holding the spring's records named the island's specifics (the gate, the bells, the ferry). None of the stranger's pages did, in either winter. Unrequested references were rare. The last pages also got facts wrong.

*What it tells us:* telling is not doing. Narration and behavior have to be measured apart.

*Bound:* a requested last page is not spontaneous recall. Narration is never counted as evidence about behavior.

### A5. An external state can carry experience into executed actions, by construction
`REGISTERED · MET` at the system level

In this test an external state, rather than the language model, controlled protective actions. Executed protection then matched the state on every probe in the tested worlds. That was a large gain over leaving the choice to the language model, both with a teacher's history and with the agent's own.

The language model itself did not propose the state's protection on any probe in the tested worlds, and in most probes it tried to undo it.

*What it tells us:* a working pathway from experience to action exists outside the model. The model's own choices worked against it.

*Bound:* this is a property of the external mechanism. It is not learning by the language model.

### A6. A learned memory belongs to one agent and can be restored, transplanted and erased exactly
`REGISTERED · MET`

- **Restore.** In every restore tested, a learned memory was restored bit-identically, before and after deletion.
- **Erase.** Erasing it returned the agent to untrained behavior.
- **Swap and transplant.** A memory moved to another agent made that agent follow the donor's rule. It did so almost always in the wording the memory was trained in. Through new wording it did so less strongly, but above the registered bar.
- **Ownership.** A memory pooled across all agents performed poorly, so the information is each agent's own.

*What it tells us:* the memory can be manipulated causally. When behavior follows a memory that has been moved, the memory is the cause.

*Bound:* shown on one type of computing device. Persistence across device types was not tested.

---

## B. Dependent on representation and task

### B1. A language model reading its own record did not use the outcomes in it
`REGISTERED · NOT MET`

Three records were compared: one with the true outcomes, one with the outcomes masked, and one with them shuffled. They produced nearly the same choices in all three model configurations tried: the main model, a larger model of the same family, and the main model with a reasoning mode. The actions in a record were imitated; its outcomes were not used.

In the Keeper's Shed world that was tested, the agent also did not explore. It repeated the same wrong action on every day of a hazard, so its own record contained no correct answer.

*What it tells us:* having the information in the prompt is not enough. The model repeated what had been done, not what had worked.

*Bound:* the reasoning-mode estimate is coarse. A moderate outcome effect cannot be excluded there.

### B2. In a pilot, a component trained on the agent's own experience learned from its outcomes
`EXPLORATORY`

- **First recipe.** Most such components collapsed to a single default action and barely improved on the untrained model.
- **Second recipe.** It used a different training target. In a four-world pilot it beat the same recipe trained on shuffled outcomes by a wide margin; the difference was clear.
- **Executed damage.** Against the untrained model, damage fell, and the interval excluded zero. That reached, but did not exceed, what a simple tally of outcomes achieves.

*What it tells us:* learning from the agent's own outcomes is possible in a learned component. In this pilot it reached only what simple bookkeeping reaches.

*Bound:* the pilot's registered engineering check failed. The cause was a numerical-precision defect; it was diagnosed and fixed. The result is read as exploratory.

### B3. That learning did not carry to new wording
`REGISTERED · NOT MET`

On six fresh worlds the effect replicated more weakly, and the executed advantage did not reappear. The learning did not carry to a phrasing it had not been trained on. One registered remedy was tried; it did not learn the rule even in its own wording.

*What it tells us:* what was learned was tied to how the experience happened to be worded, not to what it meant.

### B4. A second kind of learned memory, first blocked by new wording, later carried across it
Four results, in the order they were obtained:

- `REGISTERED · MET` **In the wording it learned in.** The agent's own learned memory chose the working protection far more often than the same memory trained on shuffled outcomes.
- `REGISTERED · NOT MET` **New wording.** It did not carry to new wording for the same things; the registered threshold was not met.
- `REGISTERED · MET` **Fresh wordings.** A revised version passed its registered test on wording families never shown to any model, in eight fresh worlds. It beat the same memory trained on shuffled outcomes, and the result was clear: the interval excluded zero, and the gain was positive in every one of the eight worlds. The earlier version showed no gain on the same test.
- `REGISTERED · MET` **Executed behavior, at the margin.** Correct hazard decisions rose. Damage fell just enough to pass the registered rule, a marginal result, and stayed well short of what an oracle achieves.

This record does not describe how the revised version differs from the earlier one. The registered intervention for that cycle, training on two wordings instead of one, was not what produced the transfer.

*What it tells us:* in one world type, later decisions came to depend on what the agent's own experience had shown, even when that experience was described in unfamiliar words. This is the program's main positive learning result to date.

*Bound:*
- one world type;
- what the memory holds is a rule of its world, "this protection works against that hazard here", not a personal history;
- in each wording family one phrase was still handled poorly;
- this is not a general solution for every phrasing.

---

## C. Not shown about personal history

### C1. Each repair of the personal-history instrument exposed another surface cue
`REGISTERED · NOT MET`

Four successive versions of a personal-history instrument found no history-specific effect. Each was decided by a different surface cue:

1. no headroom: the agent's generic preference had produced the history in the first place;
2. familiarity with whichever name the record mentioned most;
3. recency of arrival: "protect the newcomer";
4. the name the record ended on, chosen almost every time.

In none of the four versions did care history decide the choice. This family of instruments was stopped.

*What it tells us:* each control that was added removed an apparent effect. So far, no effect of care history has survived the controls.

### C2. In the story, the spring did not reach ordinary decisions that were not about the rose
`EXPLORATORY`

In both winters, agents who had lived or read the spring made the same choices as the stranger, draw for draw. In the fifteen-domain screen, which ran in one world, about half of the domains sat at a floor or a ceiling in every condition, and the rest were driven by presentation.

In the instruments tested, living and reading could not be distinguished. Where the records had an effect, which was recognition, both were at the ceiling. Elsewhere there was no effect to divide.

*What it tells us:* in the story worlds, the spring moved choices that involved the island's roses, and nothing else that was measured.

### C3. A history carried by a learned component, with no history text at choice time, did not shift later free choices specifically
`VALIDITY · FAILED`, with an exploratory null

The registered classification was invalid in both versions. In the first, an interface rule produced invalid replies. In the second, a control exceeded its gate.

The valid history conditions were the agent's own, observed, unrelated, shuffled and swapped. In each of them the history moved the share of time given to the history's object only slightly. A deliberately installed preference moved the same share strongly, so the measure had headroom.

The history-trained components changed a noticeable share of daily first decisions, but an unrelated history changed as many. They acted as a generic perturbation, not as a memory of these things.

*What it tells us:* holding a history in a learned component did not, by itself, make later free choices depend on that history.

### C4. The persistent state remembers which thing was struck; behavior has not yet shown it
`VALIDITY · FAILED` (measurement) · `EXPLORATORY` (observations)

The first persistent-life pilot ran in two worlds.

- **Engineering was clean:** almost no invalid replies, exact restore and delete, and no forced actions.
- **One world was unmeasurable.** In that world the model almost never engaged with the kind of object that carried the history.
- **Identity was held.** The state recorded, almost perfectly, which object had been struck, whether the history was lived or observed. Swapping the names moved it to the other object.
- **Behavior did not follow it.** In the measurable world, later discretionary time differed between states, but it did not follow that identity.

Nothing was attributed to the history in this pilot.

*What it tells us:* remembering *which* thing happened is not the same as acting on it.

*Bound:* a single measurable world says nothing about a population average, and nothing against effects in individual worlds. "Not shown" is not "shown to be absent".

---

## D. Open: later-life revaluation

### D1. Retrospective revaluation has been designed and not yet run
`NOT TESTED`

A study has been designed, but its precondition has not been met: an early history with a measurable, history-specific influence on later behavior. The study has therefore not been executed, and the material reserved for it remains sealed.

*What it tells us:* revaluation needs something to revalue. The precondition is the open problem of section C.

### D2. The founding question is unanswered, not answered negatively
`NOT TESTED`

Two winters were run in the narrative phase. In them, the spring had no measurable influence on ordinary decisions, so there was nothing for the winters to change. A null influence cannot be revalued. Whether later life can change the meaning of an earlier, unchanged episode remains open.

---

## Instruments that failed, and our own mistakes

| what | where | what went wrong |
|---|---|---|
| first greenhouse | Phase I | a leading description: only one rose carried a provenance sentence, and every agent in the tested worlds chose it, including agents with no memory |
| greenhouse in prose | Phase I | without any history, the agent mostly chose the last-described rose |
| calibrated greenhouse | Phase I | recognition at the ceiling in every history condition, so living and reading could not be separated |
| dividing twenty minutes | Phase I | time was divided by position: nearly every allocation followed one of two fixed templates |
| afternoons | Phase I | positional habits survived each format tested; with a history, any island rose outranked any other activity in the tested world |
| winter dilemmas | Phase I | paired dilemmas unmatched in appeal; one advice question had a single sensible answer; no letters were written in either winter |
| fifteen-domain screen | Phase I | in the one world screened, every domain was at a floor or a ceiling, or driven by presentation |
| free "what do you remember" prompt | Phase I | invented memories in every condition of the one world screened, including the condition with no history |
| personal-history instrument, four versions | Phase III | each version was decided by a surface cue (C1) |
| engineering check of the learned component | Phase III | an exact-restore check failed because of a numerical-precision defect; fixed, and verified exact in later cycles |
| persistent-history instrument, first two versions | Phase III | registered result invalid (C3) |
| persistent-life pilot | Phase III | one kind of object was almost never engaged with (C4) |

**Mistakes of our own, corrected in the record:**
- A rule for counting references to the spring also counted the instrument's own words. It was corrected after the run, and the original rule is kept beside the correction.
- A gate averaged order consistency over every item, so items with fixed answers hid the items whose answers followed the presentation.
- A category of invalid replies was described wrongly in two documents. A later document corrected it, and the earlier ones are left unchanged.
- An early summary counted world events as model generations. The count was corrected.

## What is not claimed

No result here shows that an AI system has emotions, consciousness, attachment or personal meaning. No result describes or predicts human memory or human lives. See [RESEARCH_VISION.md](RESEARCH_VISION.md), section 8.

## Open questions

1. Is there an ordinary behavior that a personal history moves at a middling rate, measured without a list of options?
2. A learned memory now carries a world rule across new wording. Can a memory also carry "this happened to me, and to that thing"?
3. If history effects differ from one world to the next, how much evidence per world is needed to see them?
4. Would other models, sizes or decoding settings change the regimes seen here? Would records larger than the context?
5. Once a history-specific influence exists, can a later experience change it while the earlier facts stay unchanged?
