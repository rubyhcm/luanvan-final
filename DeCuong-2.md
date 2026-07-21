# ĐỀ CƯƠNG ĐỀ TÀI LUẬN VĂN THẠC SĨ

**Tên đề tài:** Phát hiện sự cố bất thường trong hệ thống mạng lớn sử dụng phân tích dữ liệu nhật kí dựa trên trí tuệ nhân tạo

## 1. Nội dung

**Giới thiệu về đề tài:**
- **Bài toán/Vấn đề:** Các hệ thống mạng lớn sinh ra khối lượng dữ liệu nhật kí (log) khổng lồ từ nhiều nguồn thiết bị và dịch vụ. Điểm thách thức nhất hiện nay là cấu trúc log thay đổi liên tục (Unstable Logs) do các dịch vụ trong mạng thường xuyên được cập nhật và cấu hình lại. Các kỹ thuật giám sát bằng học máy truyền thống (đòi hỏi phân tích cú pháp tĩnh - parsing) thường xuyên bị vỡ cấu trúc và sinh ra vô số cảnh báo sai (False Positives) trước các thay đổi này.
- **Input:** Dữ liệu nhật kí (Network, System, Application, Security logs) thu thập từ hệ thống mạng lớn, ở dạng thô chưa qua phân tích cú pháp (raw logs).
- **Output:** Các cảnh báo sự cố bất thường, phân tích nguyên nhân gốc rễ và phân loại chính xác những bất thường do lỗi thực sự so với các thay đổi cấu trúc log do nâng cấp hệ thống.
- **Lí do chọn đề tài & Tính thời sự:** Đảm bảo an toàn, ổn định cho các hệ thống mạng lớn thông qua phân tích log bằng Trí tuệ nhân tạo (AI) là yêu cầu sống còn. Đề tài nắm bắt xu hướng bằng việc ứng dụng phương pháp đột phá: dùng Mô hình ngôn ngữ nhỏ (SLM) để xử lý log thô trực tiếp ở tốc độ cao (parsing-free), kết hợp sức mạnh phân tích ngữ cảnh của LLM và RAG để xử lý triệt để bài toán Log không ổn định. Kiến trúc này mang lại một hệ thống phát hiện chính xác, chủ động và tối ưu chi phí vận hành thông qua cơ chế Cache.
- **Khả năng ứng dụng:** Triển khai trên các hệ thống giám sát thực tế của doanh nghiệp, giúp tối ưu chi phí vận hành và tự động hóa quy trình phân tích của quản trị viên.

**Mục tiêu của đề tài:**
1. Xây dựng phương pháp trích xuất đặc trưng trực tiếp từ log thô (parsing-free) bằng Mô hình ngôn ngữ nhỏ (SLM) để thích ứng với dữ liệu log không ổn định.
2. Đề xuất kiến trúc cộng tác giữa SLM và LLM + RAG, trong đó LLM chỉ được kích hoạt chẩn đoán nguyên nhân khi độ bất định của SLM vượt ngưỡng, đồng thời tối ưu chi phí bằng cơ chế Cache.
3. Đánh giá tính hiệu quả của mô hình trên các tập dữ liệu Unstable Logs chuyên dụng, chứng minh sự ưu việt so với các phương pháp học máy truyền thống.

**Nội dung nghiên cứu của đề tài:**
1. **Nghiên cứu cơ sở lý thuyết:** Khảo sát các kỹ thuật phân tích log, bài toán Log không ổn định (Unstable Logs) trong kỷ nguyên cập nhật phần mềm liên tục, sự hạn chế của Log Parser và tiềm năng của các mô hình SLM, LLM.
2. **Nghiên cứu kiến trúc cộng tác SLM-LLM:** Xây dựng quy trình xử lý, trong đó SLM (như RoBERTa, LogFiT) làm bộ lọc đánh giá độ bất định trên log thô. Xây dựng hệ thống RAG và Cache để hỗ trợ LLM truy xuất các mẫu log lịch sử khi giải quyết các ca khó.
3. **Xây dựng giải pháp và thử nghiệm:** Lập trình giải pháp, chạy thử nghiệm trên các tập dữ liệu chuyên biệt về log không ổn định (ADFA-U, LOGEVOL-U, SynHDFS-U, SYNEVOL-U), so sánh với các baseline (FlexLog, LogBERT) và đánh giá tính thực tiễn.

**Phương pháp thực hiện:**
- **Thu thập và Tiền xử lý dữ liệu:** Sử dụng các tập dữ liệu Unstable Logs tiêu chuẩn. Áp dụng tiền xử lý trực tiếp (Parsing-Free) bằng các SLM (như RoBERTa/LogFiT) để hiểu ngữ nghĩa thẳng từ log thô.
- **Phát triển Mô hình và Thuật toán:** Sử dụng chiến lược cộng tác: SLM tính toán điểm bất định (Uncertainty Score) cho mỗi dòng log. Nếu điểm này vượt ngưỡng, kích hoạt LLM kết hợp RAG (truy vấn log lỗi trong quá khứ) để chẩn đoán. Kết quả được lưu vào Cache để giảm độ trễ cho các log tương tự sau này và tạo nhãn giả (pseudo-labels) huấn luyện lại SLM.
- **Đánh giá thực nghiệm:** Đánh giá trên hai khía cạnh: (1) Khả năng phát hiện (Accuracy, F1-score, False Positive Rate) và (2) Khả năng vận hành, tối ưu tài nguyên (Độ trễ/Latency, Throughput và Chi phí Token của LLM).

**Kết quả, sản phẩm dự kiến:**
1. Báo cáo kỹ thuật tổng quan về phân tích dữ liệu nhật kí và bất thường do hệ thống / do trí tuệ nhân tạo.
2. Báo cáo kỹ thuật về mô hình ngôn ngữ lớn và kỹ thuật AI lai (Hybrid) đề xuất để phân tích log.
3. Giải pháp/Sản phẩm phần mềm thực nghiệm và Báo cáo tổng hợp đánh giá kết quả chạy trên hệ thống mạng.

**Tài liệu tham khảo:**
[1] J. He et al., "Loghub: A large collection of system log datasets towards automated log analytics," *arXiv preprint arXiv:2008.06448*, 2020.
[2] M. Du, F. Li, G. Zheng, and V. Srikumar, "DeepLog: Anomaly detection and diagnosis from system logs through deep learning," in *Proc. of the 2017 ACM SIGSAC Conf. on Computer and Communications Security*, 2017, pp. 1285–1298.
[3] H. Guo, S. Yuan, and X. Wu, "LogBERT: Log Anomaly Detection via BERT," in *2021 International Joint Conference on Neural Networks (IJCNN)*, 2021, pp. 1–8.
[4] Y. Liu et al., "LogFiT: Log Anomaly Detection with Few-Shot Learning via Fine-Tuning," *IEEE Transactions on Network and Service Management*, 2022.
[5] X. Zhang et al., "AgentFM: Framework for Log Anomaly Detection Using Large Language Models," *IEEE Access*, 2023.

## 2. Kế hoạch

- **Thời gian thực hiện đề tài:** 6 tháng.
- **Lưu ý quy định:** Sau thời gian qui định nhưng chưa bảo vệ, học viên cần phải làm thủ tục gia hạn, nếu không đề tài sẽ bị huỷ và học viên phải làm lại đề tài.

**Kế hoạch thực hiện (Biểu đồ Gantt):**

![Biểu đồ Gantt Kế hoạch thực hiện đề tài trong 6 tháng](./gantt_chart.png)
