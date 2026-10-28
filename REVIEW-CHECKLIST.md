> Publication update: the project owner has approved uploading this handoff to GitHub ndthanh/sentimeter on main. Earlier review gates below describe the package review stage. Hosted-site deployment is unchanged.

# Review checklist — 28/10/2026

## Đã kiểm tra trong bản đóng gói

- [x] JavaScript syntax checks cho app, workflows, bridge, details và adapter example.
- [x] Unit checks: transcript partial/final/correction, duplicate revisions, invalid state/patch atomic rejection, SSE frame chunking, Unicode text.
- [x] Hai bộ audio: đủ 19 lượt thoại/bộ, cue nằm trong turn tương ứng, runtime MP3 tồn tại.
- [x] 5 workflow: bốn cấp taxonomy, card IDs không trùng trong route, evidence schema hợp lệ.
- [x] Browser: chọn Rewards khi chưa Start demo → loading → 6/6 completed; clock 00:00, không xác thực danh tính giả thành thật.
- [x] Browser: Rewards Portal mở được record/bảng, trạng thái FAILED, 0 điểm, cap không phải nguyên nhân.
- [x] Browser: nhánh khoá thẻ 3/3 checks, mở Card Management; đổi sang topic khác khi run đang chờ không làm kết quả cũ xuất hiện trở lại.
- [x] ZIP giải nén: npm test, syntax checks và HTTP 200 cho HTML, modules, MP3, manifests.
- [x] Exact-key scan source/archives/textual Git history: 0 matches. Key đã xoá khỏi local config. ZIP allowlist + high-confidence secret pattern scan: 0 matches; từng file khớp manifest SHA-256.

## Kiểm chứng ở các bản trước

Đã chạy đầy đủ call audio + guided cursor, xác thực, breadcrumb, hold, recommendation, consent/follow-up, replay. Đã kiểm tra tabs, avatar settings, breadcrumb ellipsis, call controls và End call. Bản đóng gói này chưa chạy lại toàn bộ 2–3 phút audio end-to-end sau khi thêm standalone runner; cần review regression trước khi gắn gateway.

## Team dev cần nghiệm thu cùng backend

- [ ] Session/customer ID động, bootstrap/history/catalog.
- [ ] STT partial/final/revision trùng và out-of-order từ nhà cung cấp thật.
- [ ] SSE qua proxy thực tế: flush, buffering, Unicode bytes, network drop, timeout.
- [ ] Hai run cạnh tranh; reset/call transfer/disconnect không nhận event cũ.
- [ ] Avaya Accept/Hold/Resume/End ACK và hold budget authoritative.
- [ ] Identity verification do operator được server xác nhận.
- [ ] Follow-up idempotent, pending/error/success, reference thật.
- [ ] Các lỗi từng system: timeout/not found/ambiguous/retry/manual fallback.
- [ ] Notes persistence và audit actions.
- [ ] Chính sách PII, retention, quyền truy cập, authentication và authorization.
- [ ] Thuật ngữ L3/L4, terms/MCC/cap/SLA được nghiệp vụ duyệt.
- [ ] Nghe audio và đo sync trên máy trình bày, foreground/background, pause/resume.
- [ ] Accessibility keyboard/focus và responsive trên thiết bị mục tiêu.

## Gate xuất bản

Chủ dự án review gói trước. Không push GitHub hoặc publish thay đổi review khi chưa có xác nhận. Chưa có repository/branch GitHub được chỉ định cho lần bàn giao này.
