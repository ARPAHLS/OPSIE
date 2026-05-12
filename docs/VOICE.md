# Voice stack

## Modes (user-facing)

| Mode | Flags | Input | Output |
|------|-------|-------|--------|
| `/voice` | `voice_mode_active=True`, `agent_voice_active=True` | Mic loop | Text plus ElevenLabs speech |
| `/voice1` | `agent_voice_active=True` | Keyboard | ElevenLabs on assistant lines |
| `/voice2` | `voice_mode_active=True`, `agent_voice_active=False` | Mic loop | Text only from assistant |
| `/voiceoff` | both False | — | Console confirmation |

## Text-to-speech (ElevenLabs)

- `speak_response` streams TTS from ElevenLabs using `VOICE_ID` and `ELEVENLABS_API_KEY`.
- `speak_agent_response` swaps to `NYX_VOICE_ID` or `G1_VOICE_ID` for agent-colored room lines.

## Speech-to-text

- `speech_recognition.Recognizer` with the default microphone.
- **`recognize_google`** path (networked).

## Boot-time voice latch

`listen_for_voice_command(timeout=5)` listens for the word **`voice`** to auto-start `/voice` mode; otherwise it prompts the operator to type `/voice` later.

## Custom vocal shortcuts (MFCC)

`custom_words` maps spoken phrases to local audio files for similarity-triggered actions. **Default paths are developer-specific** (`E:\Agents\Test 1\...`); replace with your own media or remove unused entries.

## Help bell

`display_help()` in `help.py` loads `system_sounds/helpbell.mp3` relative to `help.py`.

## Configuration checklist

Set in `.env`:

- `ELEVENLABS_API_KEY`
- `VOICE_ID`, `NYX_VOICE_ID`, `G1_VOICE_ID`
- `G1_VOICE_LIVE` for `/ask g1 live`

Ensure the default Windows recording device matches expectations.
