# Boot sequence and security

## Theme and splash

`select_theme()` runs before splash. `display_splash()`:

- Initializes `pygame.mixer` and plays `system_sounds/opsiieboot.mp3` relative to the repository root. Failure prints an error and continues.
- Prints the ASCII OPSIIE logo with a **24-bit ANSI pastel gradient** (`print_opsiie_logo_gradient`).
- Sleeps two seconds.

## Facial and emotional authentication (`facial_recognition_auth`)

1. **Load enrollments** — For each `known_user_names` entry with non-empty `picture`, load the still image, compute the first `face_recognition` encoding. Missing face in still image prints an error and **`sys.exit()`**.
2. **Open camera** index `0`. Failure exits.
3. **Loop**
   - Read frame; run **DeepFace** emotion (`angry` or `fear` → deny and exit).
   - Match encodings against the live frame; on success bind `current_user` to **`full_name`**, `call_name`, `db_params`, `public0x`, `arpa_id`, then return.
4. **Timeouts** — No face encoding for 9 seconds: warning. 18 seconds: fail closed.
5. **Master greeting** — If `arpa_id` starts with `R`, a random `master_user_greetings` line may be sent to ElevenLabs TTS in a **background thread**.

## `boot_up_sequence` stages (ordered)

| Step | Action |
|------|--------|
| 1 | Facial authentication |
| 2 | Hydrate `system_prompt` with `call_name`, emotional text, ARPA tier text; assign `convo[0]` |
| 3 | `connect_db()` using authenticated `db_params` |
| 4 | `preload_conversations(convo)` |
| 5 | Append `soul_sig` lines into `system_prompt` |
| 6 | `ensure_vector_db_exists()` for global `conversations` collection |
| 7 | `fetch_conversations()` sanity |
| 8 | Ollama configured chat model probe |
| 9 | Camera and microphone ambient calibration |
| 10 | Construct `Web3Handler` if Web3 env is complete and Base RPC responds; otherwise defer Web3 |
| 11 | Mail credentials banner |
| 12 | Dream engine CUDA or CPU banner |
| 13 | DNA smoke, `yfinance` SPY probe, TAF-3000 banner |
| 14 | Agentic API key validation and agent list |
| 15 | Play `system_sounds/gb.mp3`; ready prompt; `listen_for_voice_command(5)` |

Failures frequently call `sys.exit()` — there is no degraded interactive shell in the stock build.

## `/status` command

`display_status()` speaks a short preamble, prints a reboot line including **`call_name`**, sleeps, then calls **`boot_up_sequence()` again** (full re-authentication including camera). Use with care on unattended machines.

## Threat and safety notes

- **Photo-based auth** is replayable with a photograph unless liveness is added.
- **Emotion gate** is a demonstration policy layer, not clinical instrumentation.
- **Soul signature wipe** requires typing `confirm` after `/soulsig wipe`.

See [SECURITY.md](../SECURITY.md). For composable biometric and emotion policy outside this process, compare **[Gatekeeper](https://github.com/arpahls/gatekeeper)** in the ARPAHLS organization.
