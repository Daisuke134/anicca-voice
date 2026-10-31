# Anicca Pause

A phone call that guides one honest pause (一呼吸, *hitoiki*) when you are anxious or spiraling. You get a call, breathe 4-in / 6-out with a calm voice, name the loudest thought once, hear it reflected back without judgment, and pick one small next step. About two minutes.

Built on [Bolna](https://www.bolna.ai) for the Bolna Buildathon. It grew out of the Twilio morning-call flow behind the [Anicca](https://aniccaai.com) app.

## Architecture
```
pause.py ──POST /v2/agent──▶ Bolna agent (agent.json + prompt.md)
         ──POST /call─────▶ Bolna ──Plivo (default)──▶ caller's phone
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
Only the Python standard library is used. You need a Bolna account with a telephony number (Twilio or Bolna's default).

Not a medical device or a substitute for professional care.
