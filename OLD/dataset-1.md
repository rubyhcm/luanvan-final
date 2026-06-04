# 📊 Danh sách & Đánh giá các Tập dữ liệu (Datasets) cho Đề tài

Tài liệu này tổng hợp, phân tích và đề xuất các tập dữ liệu nhật ký (log datasets) phù hợp để giải quyết 3 Câu hỏi Nghiên cứu (RQs) của đề tài.

---

## 🎯 Bảng tổng quan các tập dữ liệu

| #     | Tập dữ liệu           | Phân loại / Vai trò                      | Mức độ khuyến nghị        | Đặc trưng kỹ thuật chính                                                     |
| :---- | :-------------------- | :--------------------------------------- | :------------------------ | :--------------------------------------------------------------------------- |
| **1** | **BGL (Blue Gene/L)** | Tập dữ liệu chính (so sánh AI/LLM - RQ2) | 🌟 **Khuyên dùng tối đa** | 4.7 triệu dòng, 348k nhãn bất thường thủ công, >1.800 mẫu sự kiện.           |
| **2** | **Thunderbird**       | Đánh giá hiệu năng quy mô lớn (RQ1)      | 🚀 **Khuyên dùng**        | ~211 triệu dòng log, quy mô dữ liệu khổng lồ, phù hợp test khả năng mở rộng. |
| **3** | **Network Logs**      | Kiểm chứng thực tế môi trường mạng (RQ3) | 🌐 **Cần thiết**          | OpenStack (228k dòng log failure), log Switch/Router thực tế.                |
| **4** | **HDFS**              | Đối chứng / Baseline ban đầu             | ⚠️ **Hạn chế**            | Đơn giản, độ chính xác dễ bão hòa (F1 ~1.0). Chỉ dùng để Sanity Check.       |

---

## 🔍 Chi tiết các tập dữ liệu

### 1. BGL (Blue Gene/L)

> **🌟 Khuyên dùng làm tập dữ liệu thực nghiệm chính**

- **Mô tả:** Nhật ký thu thập từ hệ thống siêu máy tính Blue Gene/L tại LLNL. Chứa **4.7 triệu dòng log**, trong đó có **348,460 dòng** được gán nhãn bất thường thủ công (manual anomaly labels).
- **Lý do lựa chọn:**
  - **Độ phức tạp cực cao:** Chứa hơn **1,800 mẫu sự kiện (event templates)**. Sự đa dạng và tính chất phi cấu trúc này phản ánh đúng thực tế của một hệ thống quy mô lớn.
  - **Thử thách thực tế cho LLM:** Khác với các tập dữ liệu đơn giản, BGL yêu cầu mô hình phải hiểu ngữ nghĩa ngữ cảnh sâu sắc (semantic-aware). Đây là môi trường lý tưởng để đánh giá khả năng suy luận logic và phân tích của LLM.
  - **Không có Session ID:** Dữ liệu là một dòng chảy liên tục (continuous log stream). Điều này buộc nghiên cứu phải xây dựng các phương pháp phân đoạn (sliding window hoặc chronological chunking) tiệm cận với giám sát thời gian thực.

---

### 2. Thunderbird

> **🚀 Dùng để đánh giá hiệu năng xử lý quy mô lớn (Scalability)**

- **Mô tả:** Nhật ký thu thập từ siêu máy tính Thunderbird với kích thước khổng lồ, lên tới **~211 triệu dòng log**.
- **Lý do lựa chọn:**
  - **Giải quyết Câu hỏi nghiên cứu 1:** Cung cấp nguồn dữ liệu đủ lớn để thử nghiệm kiến trúc xử lý, lọc dữ liệu và tối ưu hiệu suất trích xuất đặc trưng.
  - **Thiết lập linh hoạt:** Có thể cắt một phân đoạn thời gian (chronological subset) để huấn luyện/kiểm thử (ví dụ: phân tách theo tỉ lệ `6,000 / 2,000 / 2,000` mẫu như nghiên cứu _AdaptiveLog_) nhằm chứng minh giải pháp AI hoạt động ổn định khi dữ liệu phình to.

---

### 3. Network Device Logs (Cisco/Huawei/OpenStack)

> **🌐 Cần thiết để bám sát thực tế "Hệ thống mạng lớn"**

- **Mô tả:** Nhật ký từ hệ thống mạng ảo hóa (OpenStack - chứa **228k dòng log** từ các kịch bản lỗi/failure tests) hoặc log thực tế từ thiết bị chuyển mạch/định tuyến (Switches/Routers).
- **Lý do lựa chọn:**
  - **Phù hợp với tiêu đề đề tài:** Đề tài hướng đến "hệ thống mạng lớn". Các tập dữ liệu như BGL hay HDFS thực chất là log hệ điều hành hoặc hệ thống phân tán. Tích hợp log mạng sẽ giúp đề tài mang tính thực tiễn cao hơn.
  - **Giải quyết triệt để Câu hỏi nghiên cứu 3:** Tích hợp syslog từ thiết bị mạng (chứa trạng thái cổng Up/Down, giao thức định tuyến OSPF/BGP, hiện tượng link flap hoặc dấu vết tấn công mạng) giúp hoàn thiện quy trình giám sát mạng thực tế.

---

### 4. HDFS (Hadoop Distributed File System)

> **⚠️ Chỉ dùng làm Baseline (Đối chứng / Sanity Check)**

- **Mô tả:** Nhật ký từ hệ thống file phân tán Hadoop chạy trên môi trường Amazon EC2.
- **Lý do nên hạn chế sử dụng:**
  - **Quá đơn giản:** Các mô hình học máy truyền thống (LogBERT, DeepLog) và cả LLM đều dễ dàng đạt độ chính xác gần như tuyệt đối (F1-score từ `0.99` đến `1.0`) do các mẫu bất thường rất dễ nhận biết.
  - **Hiện tượng bão hòa độ chính xác:** Các nghiên cứu mới nhất năm 2025 chỉ ra HDFS không còn đủ độ khó để đánh giá các kỹ thuật AI/LLM nâng cao. Chỉ nên dùng tập dữ liệu này để chạy thử nghiệm nghiệm thu ban đầu (sanity check) để kiểm tra luồng xử lý của code.

---

## 📌 Gợi ý thiết lập thực nghiệm cho đề tài

Để giải quyết trọn vẹn 3 Câu hỏi Nghiên cứu (RQs) đã đề ra, cấu hình thực nghiệm được đề xuất như sau:

| Câu hỏi Nghiên cứu (Research Questions) | Tập dữ liệu áp dụng                             | Phương pháp / Mục tiêu kiểm thử                                                                      |
| :-------------------------------------- | :---------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **RQ1 (Kiến trúc & Xử lý log lớn)**     | 📂 **Thunderbird** (sub-sample)                 | Đánh giá tốc độ xử lý, khả năng lọc và trích xuất đặc trưng khi tăng quy mô dữ liệu.                 |
| **RQ2 (So sánh kỹ thuật AI/LLM)**       | 📂 **BGL**                                      | Đánh giá độ chính xác (Precision, Recall, F1-score) và khả năng hiểu ngữ cảnh phức tạp của các LLMs. |
| **RQ3 (Giám sát thực tế & Phòng thủ)**  | 📂 **OpenStack** hoặc **Router/Switch Syslogs** | Thử nghiệm quy trình giám sát end-to-end, phát hiện sớm sự cố và các dấu hiệu tấn công mạng thực tế. |
