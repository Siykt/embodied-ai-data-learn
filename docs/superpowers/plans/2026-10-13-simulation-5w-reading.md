# Simulation 5W Reading Implementation Plan

> **For agentic workers:** Use scoped parallel documentation tasks; review the resulting pages together before delivery.

**Goal:** Make the simulation section readable to beginners through familiar analogies and five explicit questions: Why, What, Who, Where, When.

**Architecture:** Rewrite the existing eleven simulation pages in place, keeping routes, evidence, concrete data, interactive components and useful deep links. Add the previously researched SoftVTBench / DiagGen report as one 5W case page. Introductions establish an everyday experience, map it to the subject, and state the analogy's limits; technical details follow the explanation rather than precede it.

**Tech Stack:** Astro 7, Starlight, Markdown/MDX, project-local SVG diagrams.

## Editorial contract

- Each page opens with a short concrete analogy before unfamiliar terms.
- Five main sections use `Why｜为什么…`, `What｜是什么…`, `Who｜谁…`, `Where｜在哪里…`, `When｜什么时候…` and answer distinct questions.
- Examples explain inputs, outputs and data use. Technical terms are explained at first use and in the glossary where needed.
- Preserve scientific caveats, published source links and observed/illustrative distinctions. Do not present either newly researched project as locally deployed.
- Retain multiple relevant local images distributed beside their explanations. Keep actual MuJoCo values and the explorer behavior intact.
- Technical appendices and reference sections may follow the five main sections; avoid merely wrapping unchanged dense text with five new headings.

## Work packages

- [x] Root: overview index, SoftVTBench / DiagGen case page, analogy diagrams, navigation and glossary.
- [x] Agent: scene/physics, sensors/timing, task generation, validation/transfer pages.
- [x] Agent: MuJoCo, Isaac Lab and learning repository pages.
- [x] Agent: history, simulator comparison and concrete MuJoCo walkthrough pages.
- [x] Root: read revised pages, verify claims against preserved evidence, repair internal anchors and confirm all local images exist.
- [x] Root: build the site, inspect generated headings and links, preview representative pages on desktop/mobile if browser tooling is available.

## Follow-up: original documentation as one learning route

The user clarified that the intended focus is the entire original eleven-page simulator documentation. The second pass makes those original pages the primary learning route; the project report remains a supplemental case. Simplify the visible reading path beyond changing headings: each chapter states a reader outcome, answers each W directly, and uses a concrete example before technical reference. Group the sidebar into foundations, the data pipeline, and tools/practice; align the homepage ordering and add chapter-to-chapter links. Open the original overview at delivery.

- [x] Revise the original overview and history, then regroup the sidebar and home index.
- [x] Simplify the original pipeline, tool and experiment chapters without altering recorded data or evidence.
- [x] Verify original-page links, examples, collapsed references, mobile layout and the saved experiment interaction.

## Verification commands

Run `npm run build`, check every simulation page for five question sections and multiple local diagrams, and validate internal documentation links and fragment targets against the generated HTML. Confirm the concrete experiment retains 401 states, 400 actions, six sensors and the source data values. Start a local preview only through `astro dev --background` and check its status. No dependency changes or new behavior tests are needed for this editorial task.

## Follow-up verification results

- `npm run build`: succeeded; 57 pages built. Existing sitemap warning remains because the project has no `site` value.
- All original 11 pages have the five ordered W sections and 2–4 local illustrations.
- 1,985 simulation-related internal links checked against generated files and anchors; no broken links or duplicate simulation-page IDs.
- Chrome at 1440px and 390px: all 11 original pages load, images render, no horizontal overflow or page errors. Sidebar and homepage follow the same learning route; supplementary case is last.
- Technical reference expands with its table rendered. Saved replay at 1.00s still maps video frame 25 to state 50 and displays angle 0.713747, velocity 0.627691 and next target 0.587785. Original 401 states, 400 actions, 6 sensors and 200 video frames are unchanged.
