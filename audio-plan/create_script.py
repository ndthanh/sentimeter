import json
from pathlib import Path
blocks=[
('verification','accept_call',[
('operator','Em chào chị Hà, em là Linh Anh, tổng đài viên Techcombank. Để hỗ trợ chị, em xin phép xác nhận một số thông tin. Chị cho em biết ngày, tháng, năm sinh của chị được không ạ?',[]),
('customer','Chị sinh ngày mười hai tháng ba năm một nghìn chín trăm chín mươi.',[]),
('operator','Dạ, ngày sinh của chị đã khớp với thông tin trên hệ thống. Chị vui lòng đọc giúp em số căn cước công dân ạ.',['verify_dob']),
('customer','Số căn cước của chị là không không một, không chín không, không không chín, hai tám một.',[]),
('operator','Em đã đối chiếu, thông tin căn cước của chị trùng khớp. Cảm ơn chị. Hôm nay em có thể hỗ trợ chị vấn đề gì ạ?',['verify_national_id','identity_verified'])]),
('request','verification_ended',[
('customer','Ngày mười lăm tháng mười, chị có chi tiêu mười hai triệu đồng bằng thẻ tín dụng trên Trip chấm com, mà đến giờ chị vẫn chưa thấy được cộng điểm thưởng. Em kiểm tra giúp chị với.',['request_captured','classify_case']),
('operator','Dạ, em ghi nhận chị muốn kiểm tra điểm thưởng cho giao dịch mười hai triệu đồng tại Trip chấm com, ngày mười lăm tháng mười. Đúng giao dịch này phải không chị?',[]),
('customer','Đúng rồi em. Chị thấy giao dịch trực tuyến được tích điểm nên muốn biết vì sao giao dịch này lại chưa có.',[]),
('operator','Dạ, chị cho em xin phép giữ máy trong giây lát để kiểm tra thông tin giao dịch và lịch sử tích điểm cho chị nhé.',[]),
('customer','Ừ, em kiểm tra giúp chị nhé.',['hold_enabled'])]),
('resolution','resume_call',[
('operator','Cảm ơn chị Hà đã chờ. Em đã kiểm tra và thấy giao dịch mười hai triệu đồng tại Trip chấm com đang ở trạng thái thất bại trên hệ thống điểm thưởng. Đây là lý do giao dịch chưa được cộng điểm cho chị.',[]),
('customer','Vậy có phải chị đã tích đủ hạn mức điểm trong tháng rồi không em?',[]),
('operator','Dạ không chị. Các giao dịch tích điểm thành công trong tháng của chị hiện là một trăm tám mươi nghìn điểm, còn hạn mức là năm trăm nghìn điểm. Em cũng đã đối chiếu điều kiện của thẻ và mã ngành của đơn vị chấp nhận thẻ; giao dịch đáp ứng điều kiện chương trình. Trường hợp này chưa được cộng điểm vì giao dịch trên hệ thống điểm thưởng báo thất bại.',[]),
('customer','Vậy bây giờ chị cần làm gì để được kiểm tra lại?',[]),
('operator','Em đề xuất lập yêu cầu kiểm tra giao dịch thất bại và chuyển bộ phận phụ trách đối soát quyền lợi điểm thưởng cho chị. Chị đồng ý để em ghi nhận yêu cầu này chứ ạ?',[]),
('customer','Chị đồng ý. Em giúp chị ghi nhận nhé.',['followup_enabled']),
('operator','Dạ, em đã ghi nhận nội dung chị yêu cầu. Ngân hàng sẽ liên hệ lại với chị qua số điện thoại đã đăng ký khi có kết quả xử lý. Chị còn cần em hỗ trợ thêm thông tin nào không ạ?',[]),
('customer','Không, chị cảm ơn em.',[]),
('operator','Em cảm ơn chị Hà đã liên hệ Techcombank. Em chào chị ạ.',['call_complete'])])]
obj={'version':1,'status':'DRAFT_AWAITING_USER_APPROVAL','language':'vi','model_id':'eleven_v3','blocks':[]}
for bid,gate,turns in blocks:
 obj['blocks'].append({'id':bid,'start_gate':gate,'turns':[{'id':f'{bid}-{i+1:02}','speaker':r,'text':t,'on_end':ev} for i,(r,t,ev) in enumerate(turns)]})
Path(__file__).with_name('script.vi.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
