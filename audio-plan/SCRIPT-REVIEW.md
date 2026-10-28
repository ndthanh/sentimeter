# Kịch bản thoại tiếng Việt — bản chờ duyệt

Hai giọng nữ. Tất cả thông tin khách hàng là giả lập. UI vẫn bằng tiếng Anh.

## 1. Chào và xác thực — sau khi bấm Accept call

**Tổng đài viên:** Em chào chị Hà, em là Linh Anh, tổng đài viên Techcombank. Để hỗ trợ chị, em xin phép xác nhận một số thông tin. Chị cho em biết ngày, tháng, năm sinh của chị được không ạ?

**Khách hàng:** Chị sinh ngày mười hai tháng ba năm một nghìn chín trăm chín mươi.

**Tổng đài viên:** Dạ, ngày sinh của chị đã khớp với thông tin trên hệ thống. Chị vui lòng đọc giúp em số căn cước công dân ạ.

*UI cue: verify_dob*

**Khách hàng:** Số căn cước của chị là không không một, không chín không, không không chín, hai tám một.

**Tổng đài viên:** Em đã đối chiếu, thông tin căn cước của chị trùng khớp. Cảm ơn chị. Hôm nay em có thể hỗ trợ chị vấn đề gì ạ?

*UI cue: verify_national_id, identity_verified*

## 2. Tiếp nhận yêu cầu — chờ bấm Hold ở cuối đoạn

**Khách hàng:** Ngày mười lăm tháng mười, chị có chi tiêu mười hai triệu đồng bằng thẻ tín dụng trên Trip chấm com, mà đến giờ chị vẫn chưa thấy được cộng điểm thưởng. Em kiểm tra giúp chị với.

*UI cue: request_captured, classify_case*

**Tổng đài viên:** Dạ, em ghi nhận chị muốn kiểm tra điểm thưởng cho giao dịch mười hai triệu đồng tại Trip chấm com, ngày mười lăm tháng mười. Đúng giao dịch này phải không chị?

**Khách hàng:** Đúng rồi em. Chị thấy giao dịch trực tuyến được tích điểm nên muốn biết vì sao giao dịch này lại chưa có.

**Tổng đài viên:** Dạ, chị cho em xin phép giữ máy trong giây lát để kiểm tra thông tin giao dịch và lịch sử tích điểm cho chị nhé.

**Khách hàng:** Ừ, em kiểm tra giúp chị nhé.

*UI cue: hold_enabled*

## 3. Trả lời — sau khi bấm Resume call

**Tổng đài viên:** Cảm ơn chị Hà đã chờ. Em đã kiểm tra và thấy giao dịch mười hai triệu đồng tại Trip chấm com đang ở trạng thái thất bại trên hệ thống điểm thưởng. Đây là lý do giao dịch chưa được cộng điểm cho chị.

**Khách hàng:** Vậy có phải chị đã tích đủ hạn mức điểm trong tháng rồi không em?

**Tổng đài viên:** Dạ không chị. Các giao dịch tích điểm thành công trong tháng của chị hiện là một trăm tám mươi nghìn điểm, còn hạn mức là năm trăm nghìn điểm. Em cũng đã đối chiếu điều kiện của thẻ và mã ngành của đơn vị chấp nhận thẻ; giao dịch đáp ứng điều kiện chương trình. Trường hợp này chưa được cộng điểm vì giao dịch trên hệ thống điểm thưởng báo thất bại.

**Khách hàng:** Vậy bây giờ chị cần làm gì để được kiểm tra lại?

**Tổng đài viên:** Em đề xuất lập yêu cầu kiểm tra giao dịch thất bại và chuyển bộ phận phụ trách đối soát quyền lợi điểm thưởng cho chị. Chị đồng ý để em ghi nhận yêu cầu này chứ ạ?

**Khách hàng:** Chị đồng ý. Em giúp chị ghi nhận nhé.

*UI cue: followup_enabled*

**Tổng đài viên:** Dạ, em đã ghi nhận nội dung chị yêu cầu. Ngân hàng sẽ liên hệ lại với chị qua số điện thoại đã đăng ký khi có kết quả xử lý. Chị còn cần em hỗ trợ thêm thông tin nào không ạ?

**Khách hàng:** Không, chị cảm ơn em.

**Tổng đài viên:** Em cảm ơn chị Hà đã liên hệ Techcombank. Em chào chị ạ.

*UI cue: call_complete*
