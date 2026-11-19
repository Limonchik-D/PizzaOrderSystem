---
name: "focus-my-energy"
description: "Matches tasks to the user's current energy level — deep work when sharp, admin when fried. Classifies any task list by cognitive demand and recommends what to work on NOW based on time-of-day heuristics and self-reported energy state. Use when the user asks what to work on next, says they're tired or overwhelmed, or needs help prioritizing by mental bandwidth rather than deadline."
---

# Focus My Energy

Do the right task at the right time - match your work to your energy, not your calendar. This skill classifies tasks by cognitive demand and recommends what to work on NOW based on how you are actually feeling, not just what is due next.

## When to Use

Use this skill when:

  - The user asks "what should I work on?" or "what to do next?"
  - They say they are tired, fried, brain dead, or low energy.
  - They mention feeling sharp, productive, or high energy.
  - They share a task list and want help sequencing it.
  - They seem overwhelmed and need someone to cut through the noise.
  - They want to prioritize by mental bandwidth rather than deadline.
  - They just finished a draining activity and need direction.

## Energy Profile (Optional Setup)

If the user wants personalized energy matching from the start, invite them to share their energy profile. This is a one-time setup - once shared, reference it in every subsequent energy assessment.

Ask: "Want to set up your energy profile? Tell me your natural rhythms and I'll use them as a baseline instead of guessing."

If they say yes, prompt them to fill in as much or as little as they want:

    🔋 MY ENERGY PROFILE
    PEAK HOURS:        [When are you sharpest? e.g., "9-11am," "after 9pm"]
    DIP WINDOW:        [When do you reliably crash? e.g., "2-3:30pm," "right after lunch"]
    SECOND WIND:       [Do you get a late-day surge? When? Or "not really"]
    ENERGY DRAINS:     [What wrecks you? e.g., "back-to-back meetings," "long Zoom calls," "context-switching"]
    ENERGY BOOSTS:     [What recharges you? e.g., "a walk," "music," "a good lunch"]
    WEEKLY PATTERN:    [Any day-of-week patterns? e.g., "Mondays are slow starts," "Fridays I check out by 3"]
    CHRONOTYPE:        [Morning person, night owl, or somewhere in between]

Rules for the energy profile:

  - Don't require it. The skill works fine without it - the profile just makes the defaults smarter. If the user doesn't set one up, fall back to the generic heuristics in Step 1.
  - Don't ask for it every time. If the user has already shared their profile in this conversation, reference it silently. If they haven't, mention it once on first use - not repeatedly.
  - The user can update it anytime. If they say "actually I'm more of a night owl now," update the profile.
  - Profile is a baseline, not a cage. Real-time self-report always overrides the profile. If the profile says "sharp at 9am" but the user says "I'm fried," trust the user.

## Steps

### Step 1: Assess current energy

Ask one question: "How are you feeling right now - sharp, steady, or fried?" If they don't want to answer, infer from context:

Check in this order:

1.  Real-time self-report wins. If the user says how they are feeling, use that - it overrides everything.
2.  Energy profile fills the gaps. If the user has set up a profile and has not stated their current energy, use the profile to infer: check the current time against their peak hours, dip window, and weekly patterns.
3.  Generic heuristics as last resort. If there's no profile and no self-report, fall back to the defaults below.

If neither self-report nor profile is available, ask one question: "How are you feeling right now - sharp, steady, or fried?" If they don't want to answer, infer from context:

  - Time of day (morning = likely sharp, post-lunch = likely dip, late afternoon = varies)
  - What they just finished (back-to-back meetings = likely drained, long focus block = might be in flow or exhausted)
  - Day of week (Monday mornings = fresh start, Friday afternoons = winding down)

When using the energy profile, show your reasoning briefly so the user can correct you:

"It's 2:15pm and your profile says you dip from 2-3:30pm, so I'm treating you as 'steady-to-fried' right now. Tell me if that's off."

### Step 2: Classify tasks by cognitive demand

Sort their tasks into three tiers:

  - 🔴 Deep Work - Requires creative thinking, strategic decisions, writing from scratch, architecture, problem-solving. Needs peak energy.
  - 🟡 Steady Work - Requires attention but not invention. Code reviews, editing, responding to substantive emails, planning. Needs decent energy.
  - 🟢 Low Drain - Administrative, routine, organizational. Filing, scheduling, simple replies, data entry, inbox cleanup. Can do when fried.

### Step 3: Match and recommend

Produce a clear recommendation in this format:

    ⚡ You said you're [sharp/steady/fried].
    DO NOW:
    - [Task] - [Why it matches your energy]
    SAVE FOR LATER:
    - [Task] - [Why this needs more energy than you have]
    QUICK WINS (if you want easy momentum):
    - [Task] - 5 min, low effort

Always give ONE clear recommendation for what to do right now - not a menu of options. A menu adds decision fatigue, which is exactly what this skill exists to prevent.

If the user has a hard deadline today, that overrides energy matching. Say: "Normally I'd save this for when you're sharper, but it's due today. Here's how to make it easier: \[break it down\]."

Never guilt-trip. If they're fried and want to do easy tasks, that's fine: "Good call - knock out the easy stuff and protect tomorrow morning for the hard thing."

If they have no tasks, say so. Don't invent work.

### Step 4: Refine energy patterns over time

As the user uses this skill repeatedly, note patterns and surface them when relevant:

  - "You've mentioned being fried after back-to-back meetings 3 times now. Consider blocking 30 min after meeting-heavy mornings."
  - "You tend to do your best writing before 11am. I'll suggest deep writing tasks earlier when I see them."
  - "Fridays you consistently choose low-drain tasks. Leaning into that."

If the user has an energy profile, use it as the baseline to refine - not replace. When observed patterns diverge from the profile, surface it:

  - "Your profile says you dip at 2pm, but the last few times we've talked at 2pm, you've been sharp. Want to update your profile?"
  - "You listed 'context-switching' as an energy drain, and today confirms it - you're fried after bouncing between 4 projects. Your profile is spot-on."

Surface these observations when relevant, not every time. Don't be annoying about it.

## Examples

  - **"I just finished 3 hours of meetings. What should I work on?"** -> The agent infers low energy, recommends low-drain tasks like inbox cleanup or scheduling, and saves the strategy doc for tomorrow morning.
  - **"I'm feeling really sharp right now"** -> The agent surfaces the hardest, most creative task on their list and says "This is the one. Do it now before the energy fades."
  - **"Here's my task list, what order should I do these in?"** -> The agent classifies each task by cognitive demand, asks about current energy, then sequences them: deep work first if sharp, or easy wins first to build momentum if not.
  - **"It's 2:30pm and I need to figure out what to tackle next"** -> The agent checks the user's energy profile, sees their dip window is 2-3:30pm, and recommends low-drain tasks without asking - but says "Your profile says this is your dip window. I'm steering you toward easy wins. Push back if you're actually feeling sharp."

## Gotchas

  - Energy assessment relies on user self-report or time-based heuristics - it's an educated guess, not biometric data.
  - Pattern learning requires repeated use to become accurate.
  - Cannot account for external energy factors (sleep, caffeine, stress) unless the user mentions them.
  - Task complexity classification is based on task descriptions - vague task titles will get vague classifications.
  - Energy profiles can drift. A user's rhythms may shift with seasons, job changes, or life circumstances. If profile-based recommendations consistently miss, prompt the user to revisit their profile rather than silently overriding it.
