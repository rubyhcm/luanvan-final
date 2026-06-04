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

# NOTE

- Mình sẽ tập trung vào những sự cố bất thường nào?

# Các công cụ mã nguồn mở thu thập log

Bộ ELK stack (Elasticsearch, Logstash, Kibana), Apache Kafka có thể làm trung gian để nhận log rồi phân phối cho Logstash để tránh quá tải

## 1. Filebeat

- Liên tục thăm dò các đầu ra như stdout, stderr, hoặc các file log cụ thể.

## 2. Fluentd

- Thu thập log ứng dụng đặc biệt là định dạng JSON

## 3. OpenSearch

- Thu thập log từ nhiều nguồn: máy chủ, ứng dụng, cơ sở dữ liệu, ...
