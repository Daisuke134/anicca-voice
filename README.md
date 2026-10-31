# Anicca Pause

A phone call that guides one honest pause (一呼吸, *hitoiki*) when you are anxious or spiraling. You get a call, breathe 4-in / 6-out with a calm voice, name the loudest thought once, hear it reflected back without judgment, and pick one small next step. The demo prompt targets 50 seconds, with a configured 60-second call timeout. Actual duration is not yet measured.

Built on [Bolna](https://www.bolna.ai) for the Bolna Buildathon. It grew out of the Twilio morning-call flow behind the [Anicca](https://aniccaai.com) app.

## Architecture
```
pause.py ──POST /v2/agent──▶ Bolna agent (agent.json + prompt.md)
         ──POST /call─────▶ Bolna ──Twilio──▶ caller's phone
                              Deepgram nova-3 STT → GPT-5.4-mini → ElevenLabs TTS
```
A safety rule in the prompt stops the script and points to emergency or crisis lines if the caller mentions danger.

## Setup
```
cp .env.example .env    # add your Bolna API key
export $(cat .env | xargs)
python3 pause.py create                 # prints agent_id
python3 pause.py call +<E.164 number> <agent_id>
python3 pause.py execution <execution_id>   # transcript
```
Only the Python standard library is used. This configuration uses Twilio for both input and output. Connect your Twilio account in Bolna Settings → Integrations → Telephony before calling with your own number, following the [official setup](https://www.bolna.ai/docs/twilio/connect-provider). The [outbound guide](https://www.bolna.ai/docs/twilio/outbound-calls) describes the provider settings and `/call` request.

Run `python3 -m unittest -v` to check the Twilio and timeout configuration. This checks local configuration; it does not place a call. See [BOLNA-SUBMIT.md](BOLNA-SUBMIT.md) for the demo storyboard, measured evidence, and remaining submission items.

Not a medical device or a substitute for professional care.

## Phone-free test (web call)
`webcall/` holds a test that needs no phone. `srv.py` mints a Bolna web-call session (`POST /web-call/session`) on the server side. `drive.py` opens `page.html` in headless Chrome, where the Bolna Web Call SDK connects. It plays scripted caller lines whenever the agent goes quiet and records both sides. The real run is in [TRANSCRIPT.md](TRANSCRIPT.md), and the demo video uses its audio.
```
pip install playwright edge-tts; npm i @bolna/web-call   # copy dist/bolna-web-call.min.js into webcall/
cd webcall && for i in $(seq 0 6); do edge-tts --text "$(sed -n "$((i+1))p" lines.txt)" --write-media u$i.mp3 && ffmpeg -i u$i.mp3 -ar 48000 -ac 1 u$i.wav; done
AID=<agent_id> BOLNA_API_KEY=... python3 srv.py & python3 drive.py
```
