# Đề tài: Phát hiện sự cố bất thường trong hệ thống mạng lớn sử dụng phân tích dữ liệu nhật kí dựa trên trí tuệ nhân tạo

## Mục tiêu

Mục tiêu của đề tài là xây dựng giải pháp phát hiện sự cố bất thường trong hệ thống mạng lớn sử dụng kỹ thuật phân tích dựa trên trí tuệ nhân tạo đối với dữ liệu nhật kí hệ thống. Giải pháp là qui trình bao gồm thu thập, sàng lọc và đánh giá dữ liệu nhật kí hệ thống, sau đó áp dụng kỹ thuật phân tích dựa trên trí tuệ nhân tạo trên tập dữ liệu này, từ đó phát hiện các sự cố bất thường trên hệ thống.

## Câu hỏi nghiên cứu

Dựa trên các mục tiêu và vấn đề thực tiễn, đề tài tập trung giải quyết các câu hỏi nghiên cứu sau:

1. What architecture and methods are appropriate for efficiently processing, filtering, and extracting features from the massive and diverse volume of log data in large network systems? (Kiến trúc và phương pháp nào là phù hợp để xử lý, sàng lọc và trích xuất đặc trưng hiệu quả từ khối lượng dữ liệu nhật ký (log) khổng lồ, đa dạng trong các hệ thống mạng lớn?)
2. Which analysis technique combining Large Language Models (LLMs) yields optimal performance (in terms of accuracy, false positive rate, and response time) when analyzing system logs to detect anomalous incidents? (Kỹ thuật phân tích kết hợp Mô hình ngôn ngữ lớn (LLMs) nào mang lại hiệu quả tối ưu (về độ chính xác, tỷ lệ dương tính giả và tốc độ phản hồi) trong việc phân tích nhật ký hệ thống để phát hiện các sự cố bất thường?)
3. How can the proposed AI/LLM techniques be integrated into an end-to-end proactive monitoring process to automate the early detection of incidents and enhance defense capabilities against AI-powered cyberattacks? (Làm thế nào để tích hợp các kỹ thuật AI/LLMs đề xuất vào một quy trình giám sát chủ động (end-to-end) nhằm tự động hóa việc phát hiện sớm sự cố và gia tăng khả năng phòng thủ trước các cuộc tấn công mạng sử dụng AI?)

## Tính cần thiết và tính mới

Có 2 vấn đề chính trong phát hiện sự cố bất thường trên hệ thống mạng lớn:

- (1) các hệ thống mạng lớn khi vận hành thường tạo ra số lượng dữ liệu nhật kí rất lớn;
- (2) các kĩ thuật phân tích chưa đủ năng lực để phát hiện sự cố bất thường trên hệ thống mạng cho người quản trị hệ thống.

Tính cấp thiết của đề tài thể hiện:

- (1) cần giải pháp phát hiện hiệu quả sự cố bất thường trên hệ thống mạng lớn;
- (2) cần giải pháp bảo vệ hệ thống từ mối đe dọa ngày càng gia tăng của tấn công sử dụng trí tuệ nhân tạo.

## Tính mới của đề tài

(i) Phát hiện sự cố bất thường: Việc phụ thuộc hệ thống giám sát, kiến thức chuyên môn của người quản trị hệ thống, qui trình và công cụ để chuẩn đoán, phát hiện và giải quyết sự cố là phương pháp tiếp cận thụ động (avoidance hoặc detection) và không còn phù hợp với các hệ thống mạng qui mô lớn, phức tạp và quan trọng. Phương pháp tiếp cận chủ động (prevention) dựa trên các kĩ thuật trí tuệ nhân tạo tiên tiến phân tích số lượng lớn dữ liệu nhật kí hệ thống để phát hiện sự cố bất thường trên hệ thống.

(ii) Sự cố bất thường liên quan đến trí tuệ nhân tạo: Trí tuệ nhân tạo gia tăng phát hiện sự cố bất thường, ví dụ khai thác và phát hiện lỗ hổng bảo mật, đồng thời tạo áp lực rất lớn cho người quản trị hệ thống và hệ thống giám sát để đối phó với các cuộc tấn công ngày càng lớn về qui mô và cường độ do trí tuệ nhân tạo gây ra. Phương pháp tiếp cận tự động (automation) kết hợp kĩ thuật trí tuệ nhân tạo để phát hiện sớm và có biện pháp phòng thủ trước các cuộc tấn công.

## Phương pháp tiếp cận

- **Nội dung 1:** Tìm hiểu các loại dữ liệu nhật kí và sự cố bất thường hệ thống liên quan đến trí tuệ nhân tạo và công cụ giám sát mã nguồn mở thu thập dữ liệu này.
- **Nội dung 2:** Tìm hiểu các kỹ thuật phân tích dựa trên trí tuệ nhân tạo phù hợp kết hợp mô hình ngôn ngữ lớn cho dữ liệu nhật kí; đề xuất kỹ thuật phù hợp.
- **Nội dung 3:** Xây dựng giải pháp phát hiện sự cố bất thường trên hệ thống mạng lớn sử dụng kỹ thuật phân tích đề xuất, áp dụng thử nghiệm trên hệ thống mạng qui mô vừa và nhỏ.

## Sản phẩm

- Báo cáo kĩ thuật về phân tích dữ liệu nhật kí và sự cố bất thường hệ thống liên quan đến trí tuệ nhân tạo.
- Báo cáo kỹ thuật về kỹ thuật phù hợp phân tích dựa trên trí tuệ nhân tạo phù hợp kết hợp mô hình ngôn ngữ lớn cho dữ liệu nhật kí.
- Báo cáo tổng hợp giải pháp phát hiện sự cố bất thường trên hệ thống mạng lớn sử dụng kỹ thuật phân tích đề xuất và kết quả đánh giá thử nghiệm.
