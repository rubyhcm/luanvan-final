# Các bộ dữ liệu (Datasets) Security Logs cho Phân tích AI/LLM

Để phục vụ cho đề tài "Phát hiện sự cố bất thường trong hệ thống mạng lớn sử dụng phân tích dữ liệu nhật kí dựa trên trí tuệ nhân tạo (đặc biệt là LLMs)", việc chọn bộ dữ liệu đóng vai trò quyết định. 

Do mô hình ngôn ngữ lớn (LLM) vượt trội ở khả năng đọc hiểu ngữ nghĩa văn bản (text semantics), ta **KHÔNG NÊN** chọn các dataset đã được trích xuất thành các đặc trưng số học (như CIC-IDS2017 dạng CSV). Thay vào đó, ta **PHẢI** chọn các dataset chứa **chuỗi log nguyên bản (raw text logs)** liên quan đến an ninh mạng.

Dưới đây là các dataset phù hợp nhất cho định hướng này:

## 1. AIT Log Dataset (Đề xuất cao nhất 🌟)
* **Nguồn:** Austrian Institute of Technology (Viện Công nghệ Áo).
* **Thành phần:** Hệ thống log đa dạng từ mạng doanh nghiệp mô phỏng, bao gồm **Apache Access Logs**, **Suricata IDS alerts**, **Syslog**, và **Auditd**.
* **Dấu hiệu tấn công (Labels):** Chứa dữ liệu của các nhóm tấn công phổ biến, đặc biệt là các cuộc tấn công web thực tế như SQL Injection (SQLi), Cross-Site Scripting (XSS), Brute Force, Directory Traversal, Web Shell.
* **Đánh giá mức độ phù hợp với LLM:** Rất cao. Dữ liệu chứa rất nhiều payload tấn công nằm ẩn bên trong các dòng log. LLM có khả năng suy luận (reasoning) để "hiểu" mã độc ẩn trong log Apache mà không cần quá trình feature engineering rườm rà như ML truyền thống.

## 2. LANL (Los Alamos National Laboratory) Cybersecurity Dataset
* **Nguồn:** Phòng thí nghiệm quốc gia Los Alamos (Mỹ).
* **Thành phần:** Bộ dữ liệu đồ sộ bậc nhất thế giới về Enterprise Security. Bao gồm chủ yếu là **Windows Event Logs (Authentication)**, **DNS logs**, **Process logs**.
* **Dấu hiệu tấn công (Labels):** Dữ liệu thu thập trong 58 ngày, chứa các cuộc tấn công có chủ đích từ đội **Red Team** ẩn mình trong hệ thống.
* **Đánh giá mức độ phù hợp với LLM:** Rất cao. Cho phép LLM theo dõi chuỗi hành vi của một user/tiến trình theo thời gian để phát hiện leo thang đặc quyền (Privilege Escalation) hoặc di chuyển ngang (Lateral Movement) trong mạng lưới.

## 3. BETH Dataset (Host-based Security Logs)
* **Nguồn:** Được thu thập từ mạng lưới Honeypot trên môi trường cloud AWS.
* **Thành phần:** Chủ yếu là **Linux Syslog** và **Auditd** (nhật ký giám sát kernel của Linux).
* **Dấu hiệu tấn công (Labels):** Chứa các hành vi khai thác vào máy chủ Linux và các lệnh (commands) trái phép được thực thi bởi kẻ tấn công.
* **Đánh giá mức độ phù hợp với LLM:** Tốt. LLM rất giỏi trong việc phân tích các bash command độc hại hoặc những chuỗi lệnh bất thường được ghi nhận trong Auditd.

## 4. Các tập con Security của Loghub (Logpai)
* **Nguồn:** Bộ sưu tập Loghub (https://github.com/logpai/loghub).
* **Thành phần:** Nếu muốn sử dụng lại các công cụ tiền xử lý truyền thống (như Drain) kết hợp với LLM, ta có thể dùng các tập con chuyên về bảo mật:
    * **Linux / Mac logs:** Phân tích các lỗi hệ thống và tấn công dò mật khẩu.
    * **OpenSSH:** Phân tích các cuộc tấn công SSH Brute Force.
    * **Apache:** Phân tích request độc hại.
* **Đánh giá mức độ phù hợp với LLM:** Khá. Bộ dữ liệu đơn giản, dễ tiếp cận để xây dựng các baseline model đầu tiên trước khi thử nghiệm dữ liệu phức tạp hơn.

---

**Khuyến nghị:** Nên ưu tiên sử dụng **AIT Log Dataset** vì nó đáp ứng đầy đủ yêu cầu về tính đa dạng của hệ thống mạng (Web, OS, IDS) và tính chân thực của các cuộc tấn công mạng thực tế, cực kỳ phù hợp để LLM phát huy thế mạnh phân tích ngữ nghĩa văn bản.
