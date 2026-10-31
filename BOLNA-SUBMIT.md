# Anicca Pause — Bolna提出作業

目的は既存の音声エージェントをTwilio経路で動かし、60秒以内のデモを用意すること。対象はagent設定、会話prompt、提出説明だけ。通話成功はBolna executionとTwilioの実測で判定する。

## 現在の根拠と実行順

- 元repo: `/Users/anicca/anicca-project/anicca-voice`
- Remote: https://github.com/Daisuke134/anicca-voice
- 開始commit: `a0286dc155ac101959b74e7f4a5db7ed5292f059`（remote mainと一致）
- 作業コピー: `/Users/anicca/anicca-project/output/life-manager/bolna-twilio-demo`
- Branch: `codex/bolna-twilio-demo`
- 開始時はPlivo入出力・最大180秒・約2分のprompt。今回Twilio入出力・最大60秒・50秒目標のpromptへ変更。Twilioデモは未実施。

TODO（この順序で実行）:

1. [x] Twilio入出力・最大60秒の設定と短い会話を用意し、ローカル検証する。
2. [ ] Bolna API keyと接続済みTwilio番号を既存実行環境で確認する。
3. [ ] 対象者の同意済み番号へ1回発信し、executionとTwilio call結果を確認する。
4. [ ] 55秒のデモを収録し、実ファイルのdurationが60秒以内と確認する。
5. [ ] デモURLと実測結果を本文へ反映して提出する。

現在cursor: 2。Credential SSOTを全件読み取ったが、`credentials[].service` にBolna/Twilio/voice該当名はない。秘密値は保存・転記しない。

## 実施した検証

- `python3 -m unittest -v test_demo_config.py`: 変更前は `plivo != twilio` で失敗。変更後は1件成功。入出力が両方Twilioで、通話timeoutが1〜60秒の範囲にあることを確認。
- `git diff --check`: 成功。
- remote mainのcommitを `git ls-remote` と `git fetch origin` で確認。
- ローカル`.env`なし。Bolna/Twilioの該当環境変数なし。ブラウザregistry・LaunchAgentsに現行の接続経路なし。
- CUA inventoryでは稼働中Chromiumを観測。ただし選択時に `Computer Use was not approved to use Chromium` と返り、Bolnaの既存sessionは未確認。
- `crwl`はローカルDBを開けず失敗。公式MarkdownとGitHub一次資料の別経路で設定仕様を確認。

## 提出用の説明

Anicca Pauseは、不安な時に一呼吸し、今いちばん強い考えを言葉にして、小さな次の一歩を選ぶための音声エージェント。BolnaがSTT・LLM・TTSをつなぎ、Twilioで電話を接続する。診断や治療効果を主張しない。

構成: `pause.py → Bolna → Twilio → 電話`。既存のDeepgram、OpenAI、ElevenLabs設定を使う。医療や緊急対応の代替ではない。

## 55秒デモ台本（収録前）

| 秒 | 映像・操作 |
|---|---|
| 0–5 | Anicca Pauseと「一呼吸から、小さな一歩へ」を表示 |
| 5–10 | BolnaのTwilio選択を表示。個人番号・鍵は映さない |
| 10–25 | 実通話で4秒吸う・6秒吐く一呼吸を聞かせる |
| 25–40 | 利用者が考えを一言伝え、エージェントが短く受け止める |
| 40–50 | 利用者が小さな次の行動を選び、通話を終える |
| 50–55 | 実際のexecution結果とrepoを表示 |

録画・音声ファイル: 未取得。デモURL: 未取得。通話duration: 未計測。台本の秒数は予定であり、実測ではない。

## 公式資料

- [Twilio outbound](https://www.bolna.ai/docs/twilio/outbound-calls): 入出力providerを`twilio`に設定して`/call`を使う。原文: “Set your agent `input` and `output` tools as `twilio`”.
- [Twilio接続](https://www.bolna.ai/docs/twilio/connect-provider): Settings → Integrations → TelephonyでAccount SIDとAuth Tokenを接続する。自前番号の利用には接続が必要。
- [公式API実装例](https://github.com/bolna-ai/bolna/blob/master/API.md): Twilio入出力のJSON例を確認済み。
- [Agent API](https://www.bolna.ai/docs/api-reference/agent/create): `call_terminate` は指定秒数に到達すると切断する設定。ローカル設定値60を確認。providerでの適用は未確認。

## 不足と再開条件

Bolnaの利用可能な鍵、agent ID、Twilio接続・発信番号、同意済み受信番号は未確認。単なるconfig検証を発信・デモ完成・提出の成功として扱わない。既存の認可済み実行環境が見つかったら、そこで通常の認証と1回の発信を進める。提出先URL・締切・必須項目も未確認。

実行環境の読み取り専用調査は `bolna_runtime_probe` へ委譲済みで、利用可能な設定は確認できないとの結果を受領。次の担当は既存の認可済みBolnaセッションを持つowner。秘密値をチャットに出さず、同じMacのCredential SSOTを使う。実通話の成功条件はBolna executionの完了・録音またはtranscriptと、Twilio callの完了・duration。60秒以内の映像は別途実ファイルで計測する。


## Watchdog再開時の追加観測

- Credential SSOT全191件を再読し、Bolna/Twilio/voiceに該当するservice登録なし。ブラウザregistryにも該当経路なし。秘密値の転記なし。
- CUAでChromiumを選択すると `Computer Use was not approved to use Chromium`。UIの認可境界を迂回しない。
- remote mainは `a590511095e93b2e70184d934ad935ce20f5da06`。作業branchを同commitまでfast-forwardした。
- mainの `TRANSCRIPT.md` にはweb通話84.5秒という既存ownerの記録がある。execution ID・公式execution readback・Twilio Call SID・録画実ファイルは本作業では未取得。web通話をTwilio通話の成功として扱わない。既存ownerの外部effectを重複させないため新規発信なし。
- [Bolna Builders](https://www.bolna.ai/builders) のHTTP 200本文にDaisuke134 / Anicca Pause / repoリンクの掲載を確認した。掲載は確認済みだが、Buildathon応募受理の証拠とは区別する。
- [Builders提出フォーム](https://www.bolna.ai/builders/submit) はHTTP 200。項目はcategory・title・public link・description・handle。送信はpublic repoへのPRを開き、maintainerのmergeで掲載する方式。Buildathon締切・動画必須条件・コンテスト提出先は未確認。推測した `/buildathon` は404、DuckDuckGo検索はhuman challenge、crwlはローカルDBエラーだった。
- floor2の `fable-main` へagmsgで認可済みowner経路、既存execution・録音の非秘密パス、Twilioの有無を照会した。send成功を確認したが、team readbackはno_placement_record / delivery offであり、着手・受諾は未確認。
- 現在cursorは2を維持する。必要な外部依存は、認可済みBolna実行owner、接続済みTwilio経路と同意済み受信先、既存execution/録音の所在。通話・55秒動画・Buildathon提出は未完了。


## owner・録音所在の追加調査

目的は既存ownerのexecution、元録音、Twilio接続readbackの取得。新規発信は行わず、既存effectを照合する。

- `/private/tmp/anicca-pause-demo.mp4` を発見。ffprobe実測58.002993秒、1,024,626 bytes、H264映像とAAC音声あり。永続コピーは `/Users/anicca/anicca-project/output/life-manager/artifacts/bolna/anicca-pause-demo.mp4`。SHA256: `477674e1f7468ae9756caafe1a3f4ab5d04345cf6a6a57c12c8406d8eeb3e43b`。60秒以内の映像ファイルの存在は確認したが、55秒条件および元録音との対応は未確認。
- owner作業コピー `/Users/anicca/anicca-project/anicca-voice` を発見。main a590511、TRANSCRIPT.mdとwebcall driverはあるが、run_id.txt・call.webm・execution JSONは存在しない。元録音の所在とexecution IDは未取得。
- Credential SSOT全191件を再照合しBolna/Twilio serviceなし。browser registryも該当なし。Twilio接続済みとは判定できない。
- agmsg floor2のsol-codex受信箱に返信なし。fable-mainはno_placement_record、delivery offで稼働未確認。映像所在、execution/run_id、元録音、Twilio接続readbackとCall SIDの有無を短文照会済み。送信成功は受諾の証拠ではない。
- Desktop Commanderの端末一覧は同じMac Mini一台がOnline。別owner実行環境は見つからない。
- 現在cursorはexecution/元録音/Twilio公式readbackの取得を維持。必要な外部依存は認可済みBolna owner実行環境。次はowner返信の実行IDと保存先を照合し既存executionをGETする。Twilio call receiptなしに新規発信・再送しない。
