# Các loại logs:

## 1. Application Logs

- Ghi lại mọi hoạt động, luồng xử lý hoặc lỗi (errors, warnings) phát sinh từ chính mã nguồn của ứng dụng.
- Giúp lập trình viên và người giám sát theo dõi luồng người dùng và tìm nguyên nhân gây ra các lỗi logic hoặc sự cố ứng dụng.

## 2. System Logs / Infrastructure Logs

- Chứa các thông tin liên quan đến hệ điều hành, máy chủ (Linux Syslog (syslog/rsyslog), Windows Event Logs, Linux Audit Daemon (auditd))
- Giám sát tình trạng phần cứng, tài nguyên hệ thống (CPU, RAM) và các tiến trình nền.
- Nội dung log:
  - Quá trình xác thực và phân quyền (auth logs).
  - Lịch sử chạy các câu lệnh hệ thống (`secure` hoặc `audit.log`).
  - Trạng thái tài nguyên (CPU, RAM, Disk I/O exhaustion events).

## 3. Access Logs / Audit Logs

- Ghi lại toàn bộ lịch sử ai đã truy cập, truy cập khi nào, từ địa chỉ IP nào và thao tác những gì.
- Kiểm toán hệ thống, theo dõi hành vi người dùng và phục vụ cho việc giải quyết tranh chấp.

## 4. Security Logs

- Theo dõi các sự kiện liên quan đến an toàn thông tin.
- Phát hiện sớm các cuộc tấn công mạng, lỗ hổng bảo mật hoặc các truy cập trái phép.

## 5. Network Logs

- Ghi lại các thông tin về lưu lượng truy cập đi qua các thiết bị mạng (Router, Switch, Firewall, Access Points).
- Khắc phục sự cố mạng, phân tích băng thông và kiểm tra các kết nối bị chặn.
- Nội dung log:
  - Trạng thái cổng kết nối (Interface Up/Down).
  - Các sự kiện định tuyến (OSPF neighbor change, BGP flap).
  - Lưu lượng bị chặn bởi tường lửa (ACL denies).
  - Các nỗ lực truy cập bất hợp pháp (SSH/Telnet login failures).

# NOTE

- Mình sẽ chọn loại log nào cho đề tài? hay kết hợp nhiều loại? => chọn dataset cho phù hợp

# Các sự cố bất thường hệ thống liên quan đến trí tuệ nhân tạo

## 1. Poisoning Attacks

- Tiêm các dữ liệu nhật ký độc hại được ngụy trang khéo léo vào hệ thống lưu trữ log trong thời gian dài.
- Khi hệ thống phát hiện bất thường bằng AI tiến hành tự động huấn luyện lại (re-training) trên tập dữ liệu này, mô hình sẽ coi hành vi tấn công này là bình thường => cho phép tin tặc xâm nhập mà không bị phát hiện.

## 2. Evasion Attacks

- Tạo ra các payload tấn công được tùy chỉnh nhẹ (ví dụ: chèn thêm các ký tự nhiễu hoặc thay đổi cấu trúc dòng log nhưng vẫn giữ nguyên tác vụ phá hoại).
- Làm lệch semantic vector khi qua các bộ mã hóa, khiến mô hình phát hiện bất thường phân loại sai từ "Mối đe dọa" thành "Bình thường".

## 3. Brute-force

- AI được dùng để tự động quét lỗ hổng mạng, thực hiện các cuộc tấn công DDoS thích ứng cao (adaptive DDoS), hoặc gửi các truy vấn thăm dò mạng tốc độ cực nhanh.

## 4. Bẻ khoá mật khẩu bằng Deep Learning

- Sử dụng các phương pháp học sâu (PassGAN) để nâng cao khả năng đoán và bẻ khóa mật khẩu một cách hiệu quả hơn nhiều so với các công cụ truyền thống

# NOTE

- Mình sẽ tập trung vào những sự cố bất thường nào?

# Các dấu vết và biểu hiện của sự cốt bất thường trong log data

- Chuỗi sự kiện log bị ngắt quãng không liên tục như người lập trình mong muốn

- Phần trăm sử dụng CPU tăng, DISK I/O tăng => hết tài nguyên do nhiều threads hoạt động cùng lúc

# Các công cụ mã nguồn mở thu thập log

Bộ ELK stack (Elasticsearch, Logstash, Kibana), Apache Kafka có thể làm trung gian để nhận log rồi phân phối cho Logstash để tránh quá tải

## 1. Filebeat

- Liên tục thăm dò các đầu ra như stdout, stderr, hoặc các file log cụ thể.

## 2. Fluentd

- Thu thập log ứng dụng đặc biệt là định dạng JSON

## 3. OpenSearch

- Thu thập log từ nhiều nguồn: máy chủ, ứng dụng, cơ sở dữ liệu, ...

## 4.Prometheus

- Thu thập metrics từ nhiều nguồn

# Xử lý, sàn lọc và trích xuất đặc trưng

## 1. Xử lý

- Các công cụ truyền thống như Drain, Spell dễ gặp lỗi khi cấu trúc log phức tạp hoặc thay đổi
- LLM có thể xử dụng để trích xuất các mẫu nhật kí
- Áp dụng rule để chuẩn hoá các biến số như path, ip, ... về chung một định dạng chuản => giảm độ nhiễu
- Gom nhóm nhật kí

NOTE: Tìm hiểu thêm về **Few-shot learning**

## 2. Sàng lọc

Log rất nhiều bao gồm cả bình thường và bất thường nếu đưa hết vào LLM sẽ quá context nên phải sàng lọc.

- Gom cụm theo nội dung => chọn một đại diện cho từng cụm nọi dung => giảm context, giảm dư thừa
- Gán trọng số cho log: log xuất hiện phổ biến sẽ đánh trọng số thấp, log hiếm sẽ đánh trọng số cao (log hiếm thường là bất thường)

NOTE:

- Tìm hiểu thêm cách gom cụm nội dung (Jaccard, DBSCAN)
- Tìm hiểu thêm về các đánh trọng số log (TF-IDF)

## 3. Trích xuất đặc trưng

- Đếm số lần xuất hiện của các log đại diện nhân với trọng số => ma trận đặc trưng
- BERT, RoBERTa, DistilRoBERTa => chuyển đổi log thành ngữ nghĩa

# Kiến trúc, mã nguồn mở hiện tại

## 1. CoLA (Collaborative Log Anomaly Detection)

Cơ chế hoạt động: SDM đóng vai trò làm bộ lọc (xử lí nhanh và chọn ra log bất thường); LLM sẽ nhận log bất thường từ SDM rồi phân tích, chuẩn đoán và đưa rra giải thích chi tiết

## 2. FlexLog - phù hợp cho unstable log

Cơ chế hoạt động: kết hợp học máy truyền thống với LLM

## 3. Parsing-Free bằng LogFiT và NeuraLog

Các kiến trúc truyền thống thường cần công cụ phân tích cú pháp (như Drain) để chuyển log thô thành dạng có cấu trúc => dễ mất ngữ nghĩa. Kiến trúc này sẽ bỏ qua bước này

- LogFiT sử dụng RoBERTa hoặc Longformer, đọc trực tiếp log thô sau đó sử dụng khả năng dự đoán câu bị che để phát hiện xem log có lệch khỏi quy luật thông thường hay không
- NeuralLog: trích xuất ngữ nghĩa từ log

## 4. LogBERT

Cơ chế hoạt động: LogBERT học các ngữ cảnh bình thường của log qua: mô hình ngôn ngữ bị che và dự đoán câu tiếp theo. Bất thường xảy ra khi log mới không nằm trong các mẫu bình thường mà mô hình đã học

NOTE: xem xét không sử dụng LogBERT do log hiện đại thay đổi liên tục
