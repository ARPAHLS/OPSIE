# System prompt and Soul Signature

## System prompt source

`utils.get_system_prompt()` returns a single large string that defines:

- **Identity:** OPSIE as an SCI agent for ARPA Corporation, personality blend (Ghost in the Shell, Urusei Yatsura, Sailor Moon tonal notes).
- **Behavior:** Memory-first reasoning, honesty about uncertainty, anti-template conversational style.
- **Capability catalog:** Narrative description of `/0x`, `/read`, `/imagine`, `/video`, `/music`, `/ask`, `/markets`, `/mail`, `/dna`, `/room` (see also [arpahls/rooms](https://github.com/arpahls/rooms) for standalone room tooling), voice modes, URL vision, and memory distinctions between OPSIE replies versus third-party command outputs.

At boot, `boot_up_sequence()`:

1. Optionally applies **`system_prompt.format(call_name=call_name)`** when the base string contains `{call_name}` placeholders (the stock `get_system_prompt()` body does not require this, but the call is harmless).
2. Appends user identity, emotional context from DeepFace, and **ARPA tier** language (`R` versus non-`R`).
3. Replaces `convo[0]['content']` with the hydrated prompt.
4. Appends **`Soul Signature:`** and each line from `known_user_names[current_user]['soul_sig']`.

## Soul Signature semantics

Soul Signature lines are **highest-priority user-specific instructions** in the system prompt. Operators manage them with `/soulsig`:

| Command | Effect |
|---------|--------|
| `/soulsig` | Print current lines |
| `/soulsig <text>` | Append a line (persisted through `save_known_user_names()`) |
| `/soulsig wipe` | Confirmed destructive clear with alert audio |
| `/soulsig heal` | Restore from `temporary_soul_sig` if a wipe just occurred |

The narrative in `utils.py` instructs OPSIE not to over-expose Soul Signature content unless relevant.

## Agent introductions

`get_agent_intro` supplies short spoken-style intros for OPSIE, Nyx, and G1 when a `/room` session begins.

## Dreaming phrases

`dreaming_expressions` and `get_random_expression()` support conversational filler before generative jobs (`/imagine`, `/music`, and related UX).
