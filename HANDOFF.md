> Publication update: the project owner has approved uploading this handoff to GitHub ndthanh/sentimeter on main. Earlier review gates below describe the package review stage. Hosted-site deployment is unchanged.

# Sentimeter — tài liệu bàn giao cho đội phát triển

**Bản review ngày 28/10/2026 · Chưa phê duyệt push GitHub**

Gói này là source frontend có thể chạy độc lập, gồm hai bộ audio tiếng Việt và interface nối backend. UI dùng tiếng Anh. Mọi hồ sơ khách hàng, giao dịch, lịch sử cuộc gọi và quy tắc nghiệp vụ trong demo đều là dữ liệu giả lập.

Bản review bổ sung tra cứu độc lập sau khi chọn phân loại; không cần phát cuộc gọi. Thay đổi này có trong gói local, chưa được publish/push. Trang hosted trước đó không phải nguồn chuẩn của bản review này.

## 1. Khởi chạy trong 5 phút

Yêu cầu: Python 3 để phục vụ static files; Node.js 18+ và npm để chạy kiểm tra. Không có bước build hoặc dependency runtime cần cài đặt. Cần phục vụ qua HTTP, không mở index.html bằng file://.

```sh
# Chạy từ thư mục gốc sau khi giải nén
python3 -m http.server 4173 --directory dist
# Mở http://localhost:4173

# Ở terminal khác
npm test
```

`npm start` là lệnh tương đương để chạy server. Google Fonts được tải từ mạng; khi offline dùng Arial fallback. Audio và ứng dụng nằm trong gói, không cần API key ElevenLabs hay đăng nhập dịch vụ để phát demo. Chỉ expose thư mục `dist`, không expose toàn bộ source bằng web server production.

## 2. Hai cách dùng demo

### Tra cứu độc lập

Không bấm logo S. Chọn đủ bốn cấp trong breadcrumb. Sau khoảng 1,1 giây loading, frontend chạy các check mẫu theo thứ tự. Card hoàn tất có thể bấm để mở record, bảng và kết luận. Đổi phân loại sẽ huỷ các callback cũ và xoá kết quả cũ. Đồng hồ cuộc gọi giữ 00:00; không có xác thực danh tính thật hay hành động ghi vào hệ thống ngân hàng.

Có 5 workflow mẫu: thiếu điểm Rewards; khoá thẻ vĩnh viễn; tra soát chuyển tiền; hỗ trợ đăng nhập/thiết bị; kiểm tra tính điểm sai. Các workflow ngoài case chính có record minh hoạ, không có hội thoại audio riêng. Chỉ case thiếu điểm có recommended response đầy đủ. Nút follow-up vẫn cần consent; việc tra cứu độc lập không tự tạo case.

### Cuộc gọi có audio và cursor

Bấm logo S để start/pause/resume/replay. Avatar LA mở Settings (chọn voice pair, guided cursor, reset). Mặc định Quynh / Chi. Luồng:

1. Ringing → Accept call.
2. Audio xác nhận ngày sinh/CCCD → indicator verified.
3. Khách nêu yêu cầu → cursor chọn bốn cấp phân loại → loading workflow.
4. Khách đồng ý hold → Hold call → các agent kiểm tra tuần tự.
5. Kết quả đầy đủ → recommended response → Resume call.
6. Khách đồng ý lập yêu cầu → Register follow-up → audio xác nhận, kết thúc.

Accept/Hold/Resume/End call nằm bên trái Avaya Voice. End call dừng audio và các tác vụ demo đang chờ. Start audio từ màn hình tra cứu độc lập sẽ huỷ run mẫu và bắt đầu kịch bản mới. Các tab Customer profile/Call history và Call insights/Live transcript không làm mất dữ liệu. Guided cursor có thể tự mở lại profile để hiển thị thao tác xác thực.

## 3. Kết luận nghiệp vụ cần giữ đúng

Giao dịch Trip.com 12.000.000 VNĐ ngày 15/10/2026 có trạng thái **FAILED trong Rewards Portal**, vì vậy không được ghi điểm. Không suy diễn rằng khoản thanh toán thẻ đã thất bại ở FIMI hoặc rằng chưa bị ghi nợ. Điều kiện chương trình/MCC trong fixtures đạt; điểm tháng thành công 180.000 trên cap 500.000 nên cap không phải nguyên nhân.

Solution: ghi nhận yêu cầu kiểm tra giao dịch thất bại và chuyển bộ phận phụ trách. Không tự cộng điểm, không hứa thời hạn xử lý chưa được nghiệp vụ duyệt. FCR trong demo là hỗ trợ xác định nguyên nhân và thống nhất bước tiếp theo; không có bằng chứng quyền lợi đã được xử lý xong ngay trong cuộc gọi.

Breadcrumb vẫn giữ nhánh nghiệp vụ người dùng cung cấp. L3 reversal/cancellation chưa khớp hoàn toàn với kết luận FAILED, L4 là `Item not supplied`; UI có ghi chú review. Đây là dữ liệu chờ nghiệp vụ xác nhận, không phải taxonomy production. Tỷ lệ, MCC loại trừ, cách tính điểm, chu kỳ cap và SLA cũng cần xác nhận từ nguồn chính thức.

## 4. Cấu trúc source và trách nhiệm

| File/thư mục | Nội dung |
|---|---|
| `dist/index.html` | Shell ba cột, tabs, dialogs, toolbar và customer fixtures |
| `dist/style.css` | Giao diện light/red, responsive, cursor, loading; hiện có CSS override tích luỹ |
| `dist/app.js` | Controller DOM, audio state machine, manual runner, transport và public API |
| `dist/workflows.js` | 5 workflow, taxonomy và evidence cho các case mẫu phụ |
| `dist/model.js` | Fixtures case Rewards, câu trả lời; còn reducer/timeline cũ không dùng bởi controller mới |
| `dist/bridge.js` | Validate state, apply top-level patches, transcript store, SSE decoder |
| `dist/details.js` | Render chi tiết evidence; xử lý đặc biệt ledger/cap cho Portal |
| `dist/audio/*` | MP3 và playback-manifest.json của từng voice pair |
| `integration/contracts.ts` | TypeScript contracts để tham khảo khi tích hợp SDK |
| `integration/README.md` | API wire/profile chi tiết |
| `integration/examples/` | Snapshot, SSE fixture và adapter client minh hoạ |
| `integration/tests.mjs` | Tests reducer, transcript, SSE, audio manifest và 5 workflows |
| `audio-plan/` | Script thoại, code generate, alignment gốc và tài liệu audio |
| `REVIEW-CHECKLIST.md` | Checklist nghiệm thu và phần chưa kiểm chứng |
| `PACKAGE-MANIFEST.json` | Hash SHA-256 từng file trong gói, trừ chính manifest |

Đây là vanilla ES modules, không React/Vue. Không cần framework để nối thử backend. Nên tách app.js thành call controller / workflow controller / transport / renderer trước khi mở rộng nhiều case; xoá reducer cũ sau khi bảo đảm không còn consumer. Đưa CSS overrides về tokens/components ở bước refactor riêng.

## 5. Ranh giới frontend và backend

Frontend nhận transcript, trạng thái call và structured evidence; backend chịu trách nhiệm session, quyền truy cập, điều phối agent, adapter hệ thống và xác nhận hành động. UI đang dùng template tin cậy để render dữ liệu; không cho model sinh rồi thực thi HTML/JavaScript tuỳ ý. Đây là adaptive UI dựa trên AG-UI events, không phải triển khai đầy đủ mọi khả năng generative UI của AG-UI.

Luồng tích hợp đề xuất:

```text
Avaya / STT → Backend gateway → transcript + call state → frontend
                                  ↓ final context + operator action
                              Agent orchestrator
                                  ↓ tool adapters
                T24 → FIMI → Terms → MCC → IDO → Portal
                                  ↓ AG-UI SSE
                     validated state → cards / recommendation
```

Giữ thứ tự nghiệp vụ đã duyệt; chỉ song song hoá khi xác định được dependency. Agent activity là trạng thái task/tool công khai, không phải chain-of-thought nội bộ. Sentiment hiện là minh hoạ, không phải suy luận tâm lý được kiểm chứng.

## 6. Public API hiện có

Truy cập qua `window.sentimeter` sau khi `app.js` đã load. Mặc định `mode='demo'`. Gọi `setMode('live')` trước khi nối backend; thao tác này huỷ audio, guided actions và manual mock jobs. Không có UI form nhập endpoint hoặc key.

| Method | Vai trò |
|---|---|
| `setMode('live'|'demo')` | Chuyển backend hoặc reset về demo |
| `ingestTranscript(segment)` | Nhận partial/final/correction |
| `getRunInput()` | Tạo RunAgentInput với final transcript, state và context |
| `connectAgent({url,input,headers})` | POST JSON, đọc SSE; endpoint do backend cung cấp |
| `receiveEvent(event, scope)` | Nhận event từ transport/SDK của team |
| `setCallState(state)` | Phản ánh call state và kết quả xác nhận từ server |
| `getState()/getTranscript()/getEvents()` | Đọc state/transcript/event log hiện tại |
| `disconnect()` | Huỷ fetch SSE và đánh dấu run inactive |

`callId` hiện cố định `SM-1027-084`. Chưa có session bootstrap/reset sang customer khác. Team cần refactor callId, customer data, workflow catalog và history thành dữ liệu server trước khi dùng nhiều cuộc gọi. API hiện không phải một security boundary.

### Transcript

```js
window.sentimeter.setMode('live');
window.sentimeter.ingestTranscript({
  id: 'seg-001', callId: window.sentimeter.callId,
  speaker: 'customer', text: 'Chị chưa được cộng điểm.',
  revision: 0, isFinal: false, startMs: 38000, endMs: 41000
});
// Final dùng cùng id và revision lớn hơn
window.sentimeter.ingestTranscript({
  id: 'seg-001', callId: window.sentimeter.callId,
  speaker: 'customer', text: 'Chị chưa được cộng điểm cho giao dịch Trip.com.',
  revision: 1, isFinal: true, startMs: 38000, endMs: 44000
});
```

Timestamp là millisecond từ đầu cuộc gọi, không phải Unix time. Chỉ nhận speaker customer/operator. Revision phải tăng; duplicate/older ignored. Final không quay lại partial; final correction revision cao hơn thay thế nội dung trước. Chỉ finals vào model context. Lời operator là quan sát bên ngoài với role user và nhãn speaker, không giả thành lời assistant của model.

`sentimeter:context-ready` phát khi final/corrected final được nhận. Gateway phải debounce/coalesce và quyết định khi đủ dữ kiện; không tạo run trên mỗi partial. Không nhét toàn bộ định danh nhạy cảm vào prompt production; xử lý tại gateway trước model.

### Call state và operator actions

```js
window.sentimeter.setCallState({
  callId: window.sentimeter.callId,
  eligible: {dob:true, id:true},
  verified: {dob:true, id:true},
  elapsedSeconds: 75,
  phase: 'awaiting-hold'
});
window.addEventListener('sentimeter:action', ({detail}) => {
  // Gửi detail về backend action endpoint; detail.id là idempotency key.
  // Không đưa vendor key vào frontend.
});
```

Actions: `accept_call`, `confirm_identity_field`, `select_classification`, `hold_call`, `resume_call`, `end_call`, `create_followup_case`, `call_complete`. Payload xác thực chứa field; phân loại chứa level, label, path; follow-up chứa evidence IDs. Envelope còn có id, callId, mode, timestamp (Unix milliseconds).

Live mode gửi intent; backend phải xác thực/authorize rồi gọi `setCallState` để phản ánh kết quả. Phases hỗ trợ: live, ringing, awaiting-hold, answer-ready, followup, complete. Sau consent dùng `followupAllowed:true`; sau tạo case thành công dùng `followupConfirmed:true`.

Giới hạn: UI follow-up vẫn có text/ID mock cứng, call/hold statistics chưa có schema live đầy đủ, classification trong UI thay đổi lạc quan trước server ACK. Team phải bổ sung acknowledgement/error state, server hold counters và case reference thật; không xem trạng thái UI là bằng chứng thao tác đã được thực thi.

### AG-UI run và shared state

```js
const input = window.sentimeter.getRunInput();
await window.sentimeter.connectAgent({url:'/api/agent', input});
```

`/api/agent` là endpoint đề xuất, chưa tồn tại trong static demo. Cấu trúc RunAgentInput có threadId, runId, state, messages, tools, context, forwardedProps. Backend phải echo đúng runId, threadId. Response `Content-Type: text/event-stream`, mỗi event kết thúc bằng dòng trống:

```text
data: {"type":"RUN_STARTED","threadId":"SM-1027-084","runId":"echo-input-runId"}

data: {"type":"STATE_SNAPSHOT","snapshot":{"cards":[],"agents":[],"recommendation":null,"signals":{"emotion":"Listening","confidence":"Insufficient evidence","guidance":"Review the case."}}}

data: {"type":"RUN_FINISHED","threadId":"SM-1027-084","runId":"echo-input-runId"}

```

State có cards, agents, recommendation, signals; xem contracts.ts và examples/rewards-state.json. Card cần id/source/title/status/body/evidence. Evidence chứa screen/reference/fields/columns/rows/conclusion; note và warn là optional. Dynamic strings được escape trước render.

STATE_SNAPSHOT thay state đầy đủ. STATE_DELTA **chỉ hỗ trợ add/replace ở cấp đầu** `/cards`, `/agents`, `/recommendation`, `/signals`. Không hỗ trợ nested JSON Patch/remove/move/test; patch không hợp lệ bị reject nguyên khối. Chọn snapshot/whole-field replacement hoặc thay reducer bằng SDK chuẩn khi mở rộng. STEP/TOOL events hiện ghi activity log, không tự tạo card; backend phải gửi state tương ứng.

ID card được allowlist: t24, fimi, policy, mcc, ido, portal và route-[1..4]-[0..3]. Renderer lấy danh sách systems từ workflow catalog. Muốn thêm nguồn mới phải cập nhật cả catalog, validation và types. `recommendation` chỉ hiện cho case Rewards chính; các case phụ cần mở rộng renderer nếu muốn có recommended response.

Backend cần cấp classification hợp lệ bằng `setCallState({callId, classification:[...fourLabels]})` để checklist hiện. Các nhãn phải khớp workflow catalog hiện tại; boolean legacy ánh xạ sang Rewards. Về production nên chuyển sang stable taxonomy IDs + display labels và workflow version.

### Transport, cancellation và lỗi

SSE parser xử lý UTF-8 ở transport, CRLF, nhiều dòng data và chunk boundaries. Có abort fetch, run matching, epoch và metadata.eventId dedup. Nếu dùng receiveEvent trực tiếp, truyền scope `{callId,runId}` từ lúc tạo run trong mọi callback; tránh callback cũ sau reset. Không có reconnect tự động, Last-Event-ID/resume, heartbeat timeout hoặc persistence. Sau lỗi nên mở run mới với snapshot đầy đủ.

Một callback RUN_STARTED cũ tự gửi lại vẫn có thể mở run mới nếu scope đúng với chính nó; gateway phải kiểm soát active request và không chuyển event từ request đã huỷ. `enterLive` không xoá mọi fixture/state đang có; gửi snapshot đầu run và authoritative call state để tránh kết quả cũ. Error UI hiện ở mức toast/status cơ bản. Không tự retry action có side effect.

## 7. Audio và cue synchronization

Giữ nguyên:

```text
dist/audio/quynh-chi/
  01-verification.mp3
  02-request.mp3
  03-resolution.mp3
  playback-manifest.json
dist/audio/oanh-thao-linh/  # cấu trúc tương tự
```

`audio-plan/generated*` chứa alignment/timing nguồn và manifest để tái tạo cue. Voice IDs là định danh công khai, không phải credential. API key đã bị xoá khỏi config local; gói không chứa config cá nhân. Không có API call ElevenLabs khi chạy frontend.

Mỗi variant có 19 lượt thoại trong 3 block. `cues` chứa turn_id, speaker, text, start/end; `ui_cues` chứa event và time_seconds. Clock chuẩn cho cue là HTMLAudioElement.currentTime + requestAnimationFrame; không dùng wall-clock setTimeout để thay thế audio alignment. Cursor prepositions trước cue xác thực 650ms; thao tác dropdown là sequence minh hoạ sau intent capture. Hold và consent là các gate; không ghép ba block thành một MP3 liên tục mà bỏ gate.

Loading workflow 1,1s và manual lookups dùng timer riêng, không phải audio cue. Hold checks demo khoảng 18s, auto Resume sau 2s nữa. Pause audio demo dừng các bước phụ thuộc demo clock; workflow loading timer ngắn không bị pause. Không cam kết frame-perfect ở tab nền; test khi tab foreground và trên thiết bị trình bày. Alignment đã kiểm tra cấu trúc, chưa được thẩm định phát âm/giọng bằng nghe chuyên biệt. Audio retry giữa block hiện có thể phát lại từ đầu trong khi cue ledger đã xử lý; cần thiết kế resume/retry rõ ràng cho production.

Nếu cần tạo lại audio: duyệt script mới, dùng script generate ở chế độ dry run trước. Chỉ truyền key mới qua biến môi trường/server-side config, không ghi vào dist. Việc xoá key local không phải revoke tại ElevenLabs. Không gọi API trả phí trong bước bàn giao này.

## 8. Kế hoạch nối backend đề xuất

| Bước | Đầu ra | Tiêu chí hoàn tất |
|---|---|---|
| 1. Bootstrap session | callId/customer/catalog/history từ backend | Không còn hardcode customer/callId trong UI |
| 2. Call + STT | Nhận lifecycle, hold state, partial/final/correction | Transcript không trùng; clock và hold khớp Avaya |
| 3. Agent gateway | POST/SSE, run correlation, snapshot/delta | Cancel/reset không nhận kết quả stale |
| 4. System adapters | Evidence từng hệ thống có reference và timestamp nguồn | Các bước đúng dependency; lỗi không giả thành kết quả đạt |
| 5. Operator actions | Idempotent endpoints và ACK/failed state | Không hiển thị follow-up thành công trước ACK |
| 6. Production hardening | Auth, audit, retention, notes persistence, reconnect | Kiểm tra role, PII, lỗi mạng, nhiều session |

Chưa có live Avaya/STT/LLM/T24/FIMI/IDO/Portal integration. Nghiệp vụ cần cung cấp API/data contracts, taxonomy IDs, terms version, MCC exclusion source, quy tắc cap/reversal/cutoff, consent policy và SLA. Hold policy demo: tối đa 2 lần, 60 giây/lần và 20% tổng thời lượng; production tính từ call events server.

## 9. Kiểm tra, gói bàn giao và GitHub

Xem REVIEW-CHECKLIST.md cho bằng chứng đã kiểm tra và phần chưa kiểm chứng. `npm test` không thay cho kiểm thử tích hợp với gateway thật, load test hay audit bảo mật.

ZIP bàn giao được tạo bằng allowlist; không có `.git`, `.openai`, site credentials, `.env`, config local hoặc archive lồng nhau. Audio MP3/alignment vẫn có. PACKAGE-MANIFEST.json lưu SHA-256 và kích thước từng file; CHECKSUMS.sha256 bên ngoài xác nhận ZIP và các tài liệu review.

**Chưa push GitHub, chưa publish các thay đổi từ lúc yêu cầu đóng gói.** Sau khi chủ dự án review và xác nhận mới chọn repository/branch, kiểm tra secret lần cuối, commit/push và mở PR nếu được yêu cầu. Không đưa lịch sử hosting hoặc thư mục credential cá nhân vào repository mới.
