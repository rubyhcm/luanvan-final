# Kế hoạch Triển khai và Xuất bản cho Luận văn

## 1. Implementation Roadmap

### Pha 1 — Thiết lập Môi trường và Kho mã  
- **Mục tiêu:** Xây dựng môi trường phát triển và kho mã nguồn có kiểm soát phiên bản. Thiết lập hệ điều hành, ngôn ngữ lập trình (Python 3.x), công cụ quản lý gói (pip/conda), thư viện học máy (PyTorch/HuggingFace), và hệ thống kiểm soát phiên bản (Git/GitHub).  
- **Đầu vào:** Tài liệu Technical/Software Design (result-6, result-7), công cụ phát triển (IDE, CLI).  
- **Kết quả:** Hệ thống môi trường hoạt động, kho mã khởi tạo với cấu trúc thư mục (theo tiêu chuẩn artifact).  
- **Sản phẩm bàn giao:** Tập tin cấu hình môi trường (requirements.txt hoặc environment.yml), README khởi tạo, khung sườn repository trên GitHub.  
- **Phụ thuộc:** Phần cứng (máy chủ/PC phát triển) sẵn sàng, kết nối Internet để cài đặt gói.  
- **Tiêu chí chấp nhận:** Có thể chạy thành công môi trường mẫu (ví dụ `python --version`, cài thành công gói), cấu trúc repository đúng như “artifact/” hướng dẫn. Kiểm thử cấu hình với script đơn giản.  
- **Rủi ro:** Vấn đề tương thích thư viện, sai lệch phiên bản, giải pháp: khóa phiên bản ổn định; fallback: sử dụng docker nếu cần thiết.

### Pha 2 — Chuẩn bị Dữ liệu và Tái sinh Baseline  
- **Mục tiêu:** Thu thập và xử lý dữ liệu log, triển khai và tái hiện hệ thống baseline từ **Cabello et al. (2026)**. Baseline sử dụng mô hình tự giám sát LogBERT cho phát hiện bất thường log.  
- **Đầu vào:** Bộ dữ liệu log (ví dụ: log hệ thống Linux, theo đề xuất baseline), mô tả baseline (TDS result-6), mã hóa sơ khởi nếu có.  
- **Kết quả:** Dữ liệu đã tiền xử lý (đã tách sequence log, chuẩn hoá định dạng), và mô hình baseline có thể huấn luyện/đánh giá.  
- **Sản phẩm bàn giao:** Script tiền xử lý dữ liệu, mã nguồn baseline (theo mô tả LogBERT), kết quả ban đầu như báo cáo lỗi giả định (anomaly scores) mẫu.  
- **Phụ thuộc:** Môi trường đã thiết lập (Pha 1), truy cập bộ dữ liệu (nếu yêu cầu giải thích cách lấy dữ liệu).  
- **Tiêu chí chấp nhận:** Mô hình baseline chạy không lỗi, tạo kết quả khớp trong biên độ với kết quả báo cáo trong Cabello et al. (2026). Nếu khác biệt đáng kể, đánh giá nguyên nhân.  
- **Rủi ro:** Dữ liệu không đầy đủ hoặc sai lệch (giải pháp: thu thập thêm hoặc xin phép người giữ dữ liệu; fallback: dùng dataset thay thế khác nhưng tương đồng). Mô tả thuật toán không rõ (mitigation: tham khảo code công khai của tác giả hoặc liên hệ tác giả).

### Pha 3 — Triển khai Cải tiến Hướng mục tiêu  
- **Mục tiêu:** Xây dựng và tích hợp phương pháp cải tiến đã xác định, ví dụ **LLM bổ sung bộ nhớ** hoặc RAG/GraphRAG cho log (theo Design result-6/result-7). Phát triển mã cho cải tiến và kết hợp vào hệ thống baseline.  
- **Đầu vào:** Mã baseline đã chạy, tài liệu thiết kế cải tiến (TDS/SDS), dữ liệu log tiền xử lý.  
- **Kết quả:** Mô hình cải tiến sẵn sàng huấn luyện/đánh giá, được tích hợp vào quy trình baseline.  
- **Sản phẩm bàn giao:** Mã nguồn cải tiến (folder `improvement/`), script so sánh đơn giản giữa baseline và cải tiến trên mẫu dữ liệu nhỏ.  
- **Phụ thuộc:** Baseline ổn định (Pha 2), thiết kế chi tiết cải tiến.  
- **Tiêu chí chấp nhận:** Mô hình cải tiến chạy thành công với dữ liệu thử, cho kết quả hợp lý (đối chiếu sanity check). Cấu trúc mã có thể kết hợp được với baseline.  
- **Rủi ro:** Tương thích mã (dependency) phức tạp (mitigation: refactor mã, isolation module; fallback: nếu không tích hợp được, thực hiện phương án cải tiến đơn giản hơn trong phạm vi cải tiến hiện tại).

### Pha 4 — Thực nghiệm có Kiểm soát  
- **Mục tiêu:** Thực hiện thí nghiệm so sánh giữa baseline và mô hình cải tiến. Đánh giá các chỉ số chính (độ chính xác, F1, thời gian phát hiện). Lặp lại nhiều lần để kiểm định thống kê.  
- **Đầu vào:** Mã baseline và cải tiến hoàn thiện, bộ dữ liệu test/validation.  
- **Kết quả:** Tập kết quả thô (metrics, log) của cả hai hệ thống.  
- **Sản phẩm bàn giao:** Báo cáo kết quả thí nghiệm (bảng số liệu so sánh baseline vs cải tiến), log chạy, script chạy thí nghiệm.  
- **Phụ thuộc:** Mô hình cải tiến hoàn chỉnh (Pha 3), tài nguyên tính toán.  
- **Tiêu chí chấp nhận:** Số liệu thí nghiệm đã thu thập đầy đủ, đủ để phân tích. Độ lặp (variability) được ghi nhận, chuẩn bị cho phân tích thống kê.  
- **Rủi ro:** Thí nghiệm thất bại hoặc kết quả không ổn định (mitigation: kiểm thử nhỏ từng phần, backup script; fallback: đơn giản hóa thiết lập thí nghiệm).

### Pha 5 — Phân tích Ablation/Độ bền/Hiệu suất  
- **Mục tiêu:** Thực hiện các khảo sát phụ theo yêu cầu trong result-8: ví dụ kiểm tra ảnh hưởng của các thành phần cải tiến (ablation), đo độ bền với dữ liệu nhiễu, đo lường hiệu suất (thời gian, tài nguyên).  
- **Đầu vào:** Kết quả thí nghiệm chính (Pha 4), mã nguồn hệ thống.  
- **Kết quả:** Tập kết quả bổ sung (bảng ablation, đồ thị độ bền, log hiệu suất).  
- **Sản phẩm bàn giao:** Báo cáo ablation và robustness (bảng phân tích, biểu đồ), scripts thực hiện các điều kiện thử nghiệm bổ sung.  
- **Phụ thuộc:** Thí nghiệm chính (Pha 4) đã thành công.  
- **Tiêu chí chấp nhận:** Đã hoàn thành tất cả thí nghiệm phụ theo thiết kế. Dữ liệu đủ để chứng minh tác động của từng thành phần cải tiến.  
- **Rủi ro:** Kết quả ablation mơ hồ (mitigation: thử nghiệm thêm khác biệt; fallback: ghi nhận như hạn chế, chuyển sang tập trung vào phân tích khác).

### Pha 6 — Phân tích Cuối cùng  
- **Mục tiêu:** Phân tích toàn diện kết quả thí nghiệm: kiểm định thống kê, phân tích lỗi, đánh giá khả năng phát hiện sớm (nếu áp dụng). Xác định hạn chế cuối cùng của nghiên cứu.  
- **Đầu vào:** Toàn bộ kết quả thí nghiệm (Pha 4,5), RQs và giả thuyết gốc.  
- **Kết quả:** Kết quả phân tích định tính và định lượng, câu trả lời cho RQs, các biểu đồ/bảng thống kê.  
- **Sản phẩm bàn giao:** Báo cáo phân tích (thống kê, error analysis), đồ thị so sánh, bảng tóm tắt kết quả.  
- **Phụ thuộc:** Kết quả thí nghiệm đầy đủ.  
- **Tiêu chí chấp nhận:** Kết quả có ý nghĩa thống kê (p-value), lỗi chính được phân tích, RQs đã có câu trả lời rõ. Các kết quả sẵn sàng trình bày trong luận văn.  
- **Rủi ro:** Phân tích không rõ ràng (mitigation: tham vấn chuyên gia thống kê; fallback: nhấn mạnh hạn chế).

### Pha 7 — Hoàn thiện Artifact và Đóng băng Kết quả  
- **Mục tiêu:** Chuẩn bị gói artifact đầy đủ phục vụ tái lập: mã nguồn, cấu hình, hướng dẫn, dữ liệu tham khảo. Tổng hợp kết quả cuối cùng, đồ thị/bảng sẵn sàng xuất bản.  
- **Đầu vào:** Mã hoàn chỉnh, kết quả tối ưu, tài liệu hiện có (README, reproducibility.md).  
- **Kết quả:** Gói artifact hoàn chỉnh, tài liệu tái lập chi tiết.  
- **Sản phẩm bàn giao:** Kho artifact trên GitHub: bao gồm `baseline/`, `improvement/`, `experiments/`, `results/`, `figures/`, `reproducibility.md`, v.v. Báo cáo kiểm tra tính tái lập (reproducibility checklist).  
- **Phụ thuộc:** Mã và kết quả ổn định (các pha trước).  
- **Tiêu chí chấp nhận:** Toàn bộ kết quả (số liệu, hình vẽ) đã được cập nhật vào artifact. Artifact được đóng băng (khóa phiên bản). Các hướng dẫn chạy lại thí nghiệm rõ ràng.  
- **Rủi ro:** Thiếu tài liệu hoặc file (mitigation: kiểm tra đối chiếu checklist sau đây; fallback: gán người chịu trách nhiệm thêm ghi chú).

## 2. Development Timeline

| **Thời gian** | **Công việc chính**                          | **Sản phẩm bàn giao**                               | **Phụ thuộc**             | **Tiêu chí kết thúc**                      |
|---------------|----------------------------------------------|----------------------------------------------------|---------------------------|-------------------------------------------|
| Tháng 1 (M1)  | Thiết lập môi trường & Kho mã                | Môi trường chạy được, repository khởi tạo           | Pha 0 (Thiết bị sẵn sàng)   | Môi trường mẫu hoạt động, repo tổ chức    |
| Tháng 2 (M2)  | Thu thập, tiền xử lý dữ liệu; Tái sinh Baseline| Dữ liệu xử lý xong, code baseline, kết quả tham khảo | Môi trường (M1)           | Baseline chạy ổn định, kết quả tương tự báo cáo|
| Tháng 3 (M3)  | Triển khai cải tiến                           | Mã cải tiến tích hợp, kiểm thử ban đầu               | Baseline (M2), bản thiết kế| Cải tiến chạy không lỗi, so khớp sơ bộ     |
| Tháng 4 (M4)  | Thực hiện thí nghiệm chính                    | Kết quả so sánh baseline vs cải tiến (metrics)       | Cải tiến (M3)             | Kết quả chính đã thu thập, sẵn sàng phân tích|
| Tháng 5 (M5)  | Thí nghiệm ablation và robustness             | Báo cáo bổ sung: ablation, robustness, hiệu suất     | Thí nghiệm chính (M4)     | Mọi thí nghiệm phụ hoàn thành             |
| Tháng 6 (M6)  | Phân tích kết quả cuối cùng                   | Đồ thị, bảng, phân tích thống kê, báo cáo lỗi         | Kết quả (M4,M5)           | Phân tích hoàn thành, RQ đã có câu trả lời |
| Tháng 7 (M7)  | Viết luận văn (phần khung chính)             | Bản nháp chương 1-4                                | Phân tích kết quả (M6)     | Cấu trúc hoàn chỉnh, xong 50% nội dung     |
| Tháng 8 (M8)  | Viết luận văn (phần thí nghiệm & thảo luận)  | Bản nháp chương 5-6, hoàn chỉnh luận văn             | Nghiên cứu xong (M6)      | Hoàn thành bản nháp đầy đủ, có phản hồi sơ bộ|
| Tháng 9 (M9)  | Finalize & Chuẩn bị nộp                      | Luận văn cuối, artifact, bài báo nháp                | Bản nháp hoàn chỉnh (M8)   | Đóng băng luận văn và artifact, nộp luận văn|

*Exit Criteria:* Mỗi giai đoạn kết thúc khi đã đạt tiêu chí (Go/No-Go). Ví dụ M2: baseline tái sinh thành công; M4: dữ liệu thí nghiệm thu thập xong; M7–M8: draft đạt yêu cầu phản hồi.

## 3. Resource Planning

- **Phần cứng:** Cần GPU mạnh (ví dụ NVIDIA A100/RTX 3090 trở lên) để huấn luyện mô hình LogBERT/LLM, dung lượng VRAM ≥ 24GB. CPU mạnh (Intel Xeon hoặc AMD Ryzen 9), RAM ≥ 32GB để xử lý dữ liệu. Ổ cứng SSD ≥ 1TB (lưu trữ dữ liệu log, kết quả). Dự trữ khả năng tính toán (GPU-hours ~ vài trăm giờ).  
- **Phần mềm:** Python 3.x, PyTorch (hoặc TensorFlow), thư viện HuggingFace Transformers, thư viện khai thác văn bản/logs (NLTK hoặc Elastic nếu cần). Công cụ thiết kế kiểm thử (PyTest), quản lý thí nghiệm (Hydra, MLFlow tùy nhu cầu). Git/GitHub để quản lý mã và artifact. Cuối cùng, LaTeX hoặc Word cho văn bản luận văn.  
- **Nhân sự:** Một nghiên cứu sinh/chuyên viên (thực hiện triển khai mã và thí nghiệm), một giáo sư hướng dẫn (theo dõi tiến độ và chuyên môn), có thể tham vấn chuyên gia dữ liệu log hoặc DevOps nếu cần.  
- **Đánh giá tài nguyên:** GPU và thời gian huấn luyện là nút thắt (tối ưu mô hình nhỏ gọn; sử dụng lập lịch công việc). Nếu dùng API LLM (GPT-4, ChatGPT), tính toán chi phí token; có thể chuyển sang LLM mã nguồn mở (LLaMA2, Mistral) nếu kinh phí hạn chế. Dung lượng lưu trữ chủ yếu cho dataset logs (một vài chục GB). Thời gian chạy các kịch bản thí nghiệm dài (hàng giờ) cần tính trước (theo kết quả baseline báo cáo).  

## 4. Risk Management

| **Rủi ro**                                             | **Xác suất** | **Tác động** | **Giải pháp giảm thiểu**                                     | **Giải pháp khắc phục (Fallback)**                                                   |
|--------------------------------------------------------|-------------:|------------:|-------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Cải tiến không cải thiện hiệu năng (không gain)        | Trung bình   | Cao         | Kiểm thử nhiều biến thể, đánh giá sớm, tham khảo ý kiến GV  | Giảm tính năng phức tạp, thử cải tiến đơn giản hơn (giảm quy mô bộ nhớ)             |
| Tái sinh baseline không khớp (mismatch)                | Trung bình   | Cao         | Đọc kỹ phương pháp, hỏi tác giả, tối ưu tham số             | Chọn baseline tương đương khác (vẫn hướng cải tiến về memory hoặc context)          |
| Giả thuyết nghiên cứu không được hỗ trợ                | Thấp         | Trung bình  | Kiểm thử lý thuyết, thêm thí nghiệm kiểm chứng             | Nếu thất bại, thừa nhận trong luận văn và giảm kỳ vọng (giảm scope)                |
| **Dữ liệu bị rò rỉ/không có giám sát đầy đủ**          | Thấp         | Trung bình  | Kiểm tra kỹ về phân chia (train/test), đảm bảo normal/anomaly rõ | Sử dụng kỹ thuật tự giám sát hoàn toàn (như baseline) và tái định nghĩa tác vụ nếu cần |
| **Thiếu nhãn (unsupervised)**                          | Trung bình   | Trung bình  | Dùng phương pháp tự giám sát, đánh giá dùng metric bất thường chuẩn | Sử dụng bán giám sát hoặc mô hình dự đoán sequence (như LogBERT)                    |
| **Độ lệch dữ liệu (bias)**                             | Trung bình   | Trung bình  | Kiểm tra thống kê dữ liệu, sử dụng kỹ thuật augmentation nếu cần | Hạn chế kết luận, bổ sung tập kiểm thử bổ sung                                  |
| **Tích hợp mã phức tạp/phiên bản phụ thuộc**           | Cao          | Trung bình  | Sử dụng môi trường cô lập (venv, docker), kiểm soát phiên bản rõ ràng | Tách rõ baseline và cải tiến, thử cài riêng từng phần                            |
| **Thiếu tài nguyên tính toán (GPU)**                  | Cao          | Cao         | Lên kế hoạch chạy trên GPU công ty/university, tối ưu mô hình | Sử dụng mô hình nhỏ hơn, huấn luyện trên GPU vừa (thời gian chậm hơn)               |
| **LLM/Stability issues**                              | Trung bình   | Cao         | Lựa chọn model tin cậy, kiểm thử lặp, giữ seed             | Nếu model LLM không ổn định, chuyển sang LLM khác hoặc tăng khối lượng training      |
| **Mẫn cảm với prompt (prompt sensitivity)**           | Trung bình   | Trung bình  | Thiết kế prompt rõ ràng, thử các biến thể                   | Đơn giản hoá prompt, sử dụng các kỹ thuật tinh chỉnh (fine-tuning)                 |
| **Hallucination của LLM/RAG không chính xác**        | Trung bình   | Cao         | Kiểm chứng thông tin, dùng RAG với nguồn đáng tin cậy        | Giới hạn phạm vi truy vấn, fallback sang mô hình truyền thống (vẫn hướng memory)   |
| **Chi phí hoặc độ trễ API (nếu dùng)**               | Thấp         | Trung bình  | Dự toán số token, so sánh giá cả, tối ưu prompt             | Chuyển sang LLM mã nguồn mở (không tốn chi phí API)                                |
| **Thay đổi model/API (update)**                      | Thấp         | Trung bình  | Khóa phiên bản model/API, kiểm thử lại khi cập nhật        | Duy trì bản sửa lỗi tạm thời, ghi lại thay đổi như hạn chế                           |

Mỗi rủi ro có giải pháp khắc phục giữ nguyên hướng cải tiến (thí dụ fallback vẫn dùng cải tiến bộ nhớ hoặc RAG, chỉ giảm độ phức tạp).

## 5. Kế hoạch Viết Luận văn

### Chương 1 — Giới thiệu  
- **Mục tiêu:** Trình bày vấn đề phát hiện bất thường sớm trong log với AI, động lực nghiên cứu, phạm vi (phát hiện sớm, Foundation Models, RAG/Memory-augmented LLM…), các câu hỏi nghiên cứu và đóng góp chính.  
- **Nguồn:** Đề cương final (result-4), định nghĩa mục tiêu Nghiên cứu (RQ, mục tiêu, giả thuyết đã xác định).  
- **Nội dung:** Mô tả bối cảnh AIOps/log anomaly detection, tầm quan trọng, khó khăn, giới hạn hiện tại. Nêu RQs, giả thuyết, cải tiến đề xuất.  
- **Hình/Bảng:** Sơ đồ khái niệm vấn đề (issue tree), bảng tóm tắt RQ và giả thuyết.  
- **Tiêu chí:** Đầy đủ các yếu tố (vấn đề, động lực, RQ, mục tiêu, đóng góp); rõ ràng, dẫn dắt mạch lạc.

### Chương 2 — Tổng quan Tài liệu liên quan  
- **Mục tiêu:** Tóm tắt kết quả Systematic Mapping và phân tích phê phán (result-1, result-2), giới thiệu baseline Q1/Q2 (2023–2026), xác định hạn chế đã xác nhận.  
- **Nguồn:** Kết quả định lượng/định tính mapping (result-1,2), danh sách baseline tiềm năng.  
- **Nội dung:** Phân loại và phân tích các phương pháp hiện có (đặc biệt trong log anomaly và AI); nêu một baseline đáp ứng (Cabello et al. 2026); thảo luận hạn chế (ví dụ: phụ thuộc sliding window, không có bối cảnh lịch sử).  
- **Hình/Bảng:** Sơ đồ bản đồ tri thức (từ result-1), bảng so sánh các phương pháp, bảng xác nhận hạn chế.  
- **Tiêu chí:** Tổng hợp rõ các nhóm phương pháp, chỉ rõ baseline đã chọn thuộc nhóm nào, liệt kê hạn chế dẫn tới cải tiến.

### Chương 3 — Phương pháp nghiên cứu  
- **Mục tiêu:** Mô tả thiết kế nghiên cứu (result-5), câu hỏi giả thuyết, kiến trúc baseline và ý tưởng cải tiến, quy trình thí nghiệm.  
- **Nguồn:** Research Design (result-5), Hypotheses, Protocol (result-8).  
- **Nội dung:** Chi tiết về mô hình baseline (LogBERT) và cải tiến (ví dụ LLM + memory), cách triển khai, số liệu đánh giá (metrics chính), cách thực hiện thí nghiệm có kiểm soát.  
- **Hình/Bảng:** Sơ đồ khối hệ thống baseline và cải tiến tích hợp; quy trình thí nghiệm.  
- **Tiêu chí:** Giải thích rõ ràng phương pháp baseline, cải tiến, biến thể thí nghiệm; so sánh baseline-improve trong khung nghiên cứu.

### Chương 4 — Thiết kế Hệ thống và Phần mềm  
- **Mục tiêu:** Trình bày thiết kế kỹ thuật và phần mềm chi tiết cho hệ baseline và cải tiến (từ result-6, result-7).  
- **Nguồn:** Technical Design (result-6), Software Design (result-7).  
- **Nội dung:** Mô tả kiến trúc phần mềm (module baseline, module cải tiến như thành phần memory), các chức năng chính, sơ đồ luồng dữ liệu, mô tả cụ thể các thuật toán.  
- **Hình/Bảng:** Sơ đồ lớp/module, sơ đồ dữ liệu. Bảng thông số kỹ thuật (kiến trúc model).  
- **Tiêu chí:** Đầy đủ chi tiết để đảm bảo người khác có thể xây dựng lại hệ thống; rõ ràng phần thay đổi khi tích hợp cải tiến.

### Chương 5 — Thí nghiệm và Kết quả  
- **Mục tiêu:** Báo cáo kết quả thực nghiệm: tái sinh baseline, so sánh chính với cải tiến, phân tích khả năng phát hiện sớm, ablation, thống kê và phân tích lỗi.  
- **Nguồn:** Protocol và kết quả thiết kế (result-8), dữ liệu thực nghiệm.  
- **Nội dung:** Mô tả quá trình tái tạo baseline và kết quả (so với công bố), thí nghiệm chính so sánh baseline/cải tiến (bảng metrics, biểu đồ ROC…), đánh giá phát hiện sớm (độ giảm thời gian/phát hiện ban đầu), thử nghiệm bổ trợ (độ bền, ablation), kết quả thống kê (p-value). Phân tích lỗi (log anomalies cụ thể).  
- **Hình/Bảng:** Bảng kết quả (precision, recall), đồ thị so sánh (curves, bar chart), hình minh hoạ phát hiện sớm. Bảng tóm tắt ablation.  
- **Tiêu chí:** Kết quả số liệu đầy đủ và rõ ràng; thông tin thống kê đủ để khẳng định đóng góp; trình bày đủ đồ thị/bảng minh hoạ quan trọng.

### Chương 6 — Thảo luận, Kết luận và Hướng phát triển  
- **Mục tiêu:** Tổng kết trả lời các câu hỏi nghiên cứu, đánh giá giả thuyết, nêu đóng góp, hạn chế và hướng tương lai.  
- **Nguồn:** Kết quả phân tích (Chương 5), các giả thuyết và mục tiêu ban đầu.  
- **Nội dung:** So sánh với công bố ban đầu, nêu rõ cải tiến đem lại hiệu quả nào. Khẳng định mức độ hỗ trợ/hoặc bác bỏ giả thuyết. Liệt kê đóng góp (khoa học, phương pháp, kỹ thuật). Thảo luận hạn chế (ví dụ mở rộng mô hình, dữ liệu). Đề xuất công việc tương lai.  
- **Hình/Bảng:** Bảng so sánh các đóng góp với kỳ vọng, tóm tắt đóng góp chính.  
- **Tiêu chí:** RQ được trả lời thỏa đáng, giả thuyết rõ ràng quyết định, đóng góp minh bạch, hạn chế đã nhắc đến, đề xuất phù hợp với kết quả.

## 6. Bảng Đóng góp Luận văn

| **Đóng góp**                | **Bằng chứng**                       | **Thí nghiệm**                 | **Chương** | **Tình trạng**    |
|-----------------------------|--------------------------------------|--------------------------------|------------|------------------|
| Tái tạo baseline            | Kết quả baseline gốc   | Chạy mô hình baseline        | 5          | Đang thực hiện   |
| Bằng chứng hạn chế          | Phân tích kết quả baseline (sliding window)  | So sánh window dài/ngắn   | 5          | Đang thực hiện   |
| Cải tiến định hướng         | Đề xuất thêm memory/knowledge vào LLM    | Triển khai thêm bộ nhớ vào model | 4 & 5      | Đang thực hiện   |
| Lợi ích phát hiện sớm       | Giảm độ trễ phát hiện/metrics tăng       | So sánh thời gian phát hiện    | 5          | Đang thực hiện   |
| Độ bền/hiệu suất bổ trợ     | Kết quả ablation (task mutiplier)         | Thí nghiệm stress-test        | 5          | Đang thực hiện   |
| Artifact tái lập            | Kho mã, hướng dẫn reproducibility       | Đóng gói mã và dữ liệu tham khảo | 7          | Đang thực hiện   |

*Ghi chú:* Đóng góp khoa học chủ yếu ở phần phát hiện sớm cải tiến; phương pháp/mô hình mới; đóng góp kỹ thuật ở code, artifact tái lập; có thể có đóng góp công nghiệp nếu áp dụng tốt.

## 7. Kế hoạch Xuất bản

| **Đầu ra**           | **Độ phù hợp**                   | **Chứng cứ cần**              | **Ưu điểm**                      | **Rủi ro**                              | **Ưu tiên** |
|----------------------|----------------------------------|-------------------------------|----------------------------------|-----------------------------------------|-------------|
| *Expert Systems with Applications* (Elsevier, Q1) | Rộng về AI/logs           | Kết quả vượt baseline rõ rệt, phân tích sâu | Tạp chí Q1, tầm ảnh hưởng cao     | Cạnh tranh gay gắt, yêu cầu novelty cao   | Cao        |
| *Neurocomputing* (Elsevier, Q1)                    | ML cho anomaly detection | Kết quả cải tiến rõ, lập luận chặt   | Hội độc giả ML lớn, tạp chí Q1    | Yêu cầu kỹ thuật ML mạnh, đánh giá cao    | Trung bình |
| *Knowledge and Information Systems* (Springer, Q1) | Knowledge-augmented AI    | Sử dụng retrieval/knowledge rõ  | Tập trung kiến thức, phù hợp KAM  | Cần làm nổi bật hướng kiến thức          | Trung bình |
| *IEEE Access* (IEEE, Q2)                          | Journal phổ cập, open access | Kết quả đầy đủ, giải thích rõ  | Dễ tiếp cận, review nhanh         | Tạp chí Q2, cạnh tranh cao, chi phí APC    | Thấp       |

**Chiến lược:** Bài báo sẽ dựa trên bằng chứng thực nghiệm (baseline + cải tiến). Tập trung thuyết phục qua dữ liệu. Không tự xưng phương pháp hoàn toàn mới mà trình bày như extension/cải tiến của baseline. Nếu đóng góp không lớn, có thể chọn IEEE Access làm kênh xuất bản dễ hơn.

## 8. Artifact Package

```text
artifact/
├── README.md           # Hướng dẫn tổng quan
├── configs/            # Các file cấu hình (hóa học)
├── data_reference/     # Thông tin cách lấy bộ dữ liệu
├── baseline/           # Mã nguồn và script triển khai baseline
├── improvement/        # Mã nguồn và script cho phần cải tiến
├── prompts/           # (nếu dùng LLM/RAG) chứa prompt templates
├── scripts/           # Script chạy thí nghiệm tự động
├── experiments/       # Cài đặt và log của từng thí nghiệm
├── results/           # Kết quả thô và tiền xử lý (logs, metrics)
├── figures/           # Tập hình vẽ, biểu đồ cho luận văn
├── logs/              # Log hệ thống trong quá trình chạy
├── tests/             # Bộ kiểm thử code cơ bản
├── docs/              # Tài liệu phụ trợ, ví dụ mã mẫu
└── reproducibility.md # Hướng dẫn tái lập chi tiết
```

Artifact hỗ trợ:
- Tái lập baseline và mô hình cải tiến (mã `baseline/`, `improvement/`).  
- Chạy thí nghiệm chính và bổ trợ (`scripts/`, `experiments/`, `results/`).  
- Sinh đồ thị/bảng kết quả (`figures/`).  
- Tài liệu hướng dẫn (`README.md`, `reproducibility.md`) bao gồm cách cài đặt môi trường, cấu hình tham số (seed, hyperparameters, model version, prompt, retrieval settings).  

Kiểm tra đảm bảo:
- **Dữ liệu:** Phiên bản, nguồn, phân chia train/test rõ ràng. Nếu không chia, hướng dẫn tạo splits.  
- **Mã nguồn:** Phiên bản mã (commit Git), dependency versions (file lock).  
- **Cấu hình:** Cấu hình baseline và cải tiến (learning rate, batch size, seeds).  
- **Môi trường:** OS, Python version, library versions.  
- **Thông số mô hình:** kiến trúc, số tham số (nếu dùng LLM, tên model).  
- **Phân tích:** ID từng thí nghiệm, kết quả thô, tiền xử lý kết quả.  
- **Hình/bảng:** figure, bảng đầy đủ, có chú thích.  
- **Tài liệu:** README, reproducibility hướng dẫn rõ từng bước.  

Tất cả các bước kiểm thử (**experiment completion**) cần hoàn thành:
- Baseline tái tạo thành công.  
- So sánh baseline vs cải tiến thu thập xong.  
- Đánh giá metric Early Detection đã thực hiện (nếu áp dụng).  
- Ablation/robustness (nếu có yêu cầu trong result-8) hoàn thành.  
- Phân tích thống kê và lỗi hoàn thành.  
- Artifact được đóng băng (freeze) trước khi chấm.

## 9. Checklist Tái lập (Reproducibility)

- [ ] **Dữ liệu:** Mô tả nguồn, định dạng, phiên bản. Hướng dẫn lấy hoặc (nếu không share) mô tả cách thu thập.  
- [ ] **Phiên bản mã:** Tag/release trong Git, file lock (requirements.txt).  
- [ ] **Cấu hình thí nghiệm:** File config yaml hoặc ghi rõ hyperparameters, seed.  
- [ ] **Môi trường:** Document môi trường (OS, Python, GPU), có thể file `environment.yml`.  
- [ ] **Model/Prompt:** Ghi rõ model LLM (tên, phiên bản), prompt sử dụng nếu có.  
- [ ] **Script chạy:** Script cho từng thí nghiệm (baseline, cải tiến, ablation) có thể chạy lại được.  
- [ ] **Kết quả:** Cung cấp kết quả raw, mã code sinh đồ thị/bảng, các figures cuối cùng.  
- [ ] **Hướng dẫn:** README/Reproducibility có hướng dẫn từng bước tái lập.  

## 10. Checklist Hoàn thành Thí nghiệm

- [ ] Mô hình baseline đã tái tạo và đạt kết quả phù hợp.  
- [ ] Mô hình cải tiến đã tích hợp và chạy ổn định.  
- [ ] Kết quả so sánh baseline vs cải tiến thu thập xong (với thử nghiệm lặp).  
- [ ] Thí nghiệm Early Detection thực hiện (đo lường thời gian phát hiện hoặc lợi ích tương ứng).  
- [ ] Các thí nghiệm ablation/robustness (nếu có yêu cầu) đã hoàn thành.  
- [ ] Phân tích thống kê (độ tin cậy, p-value) đã sẵn sàng.  
- [ ] Phân tích lỗi (ví dụ các trường hợp phát hiện sai) hoàn tất.  
- [ ] Tất cả figures và tables cần thiết đã được tạo ra và kiểm chứng.

## 11. Checklist Sẵn sàng Luận văn

- [ ] **RQ trả lời:** Các câu hỏi nghiên cứu đã có câu trả lời dựa trên kết quả.  
- [ ] **Mục tiêu đạt:** Tất cả mục tiêu nghiên cứu đề ra (nâng cao độ chính xác, giảm thời gian) đã kiểm định.  
- [ ] **Giả thuyết:** Các giả thuyết ban đầu đã được xác nhận/hủy bỏ rõ ràng.  
- [ ] **Hạn chế:** Hạn chế ban đầu được chứng minh (ví dụ baseline không tối ưu trong khoảng thời gian ngắn).  
- [ ] **Cải tiến:** Cải tiến mục tiêu đã được triển khai và đánh giá.  
- [ ] **Đóng góp:** Đóng góp (cải thiện metric, mô hình mới) đã có bằng chứng.  
- [ ] **Giới hạn:** Đã nêu rõ giới hạn của nghiên cứu (dữ liệu, mô hình).  
- [ ] **Tính tái lập:** Tất cả các bước đã được ghi lại, artifact sẵn sàng.  

Đánh giá tổng thể:  
- Kết quả baseline vs cải tiến đủ mạnh để thuyết phục reviewer.  
- Kết quả ban đầu cho thấy tăng độ chính xác hoặc phát hiện sớm.  
- Thí nghiệm công bằng và đủ số lần lặp để đảm bảo tính khoa học, thống kê.  
- Artifact chất lượng (đầy đủ, có thể tái lập).  
- Viết luận văn rõ ràng, logic, không phóng đại đóng góp.  

## 12. Checklist Sẵn sàng Xuất bản

- [ ] **Kết quả thuyết phục:** Bằng chứng thực nghiệm đủ mạnh (statistically significant).  
- [ ] **Baseline cân bằng:** Mô hình baseline được re-implement tốt và so sánh công bằng.  
- [ ] **Đóng góp rõ:** Đóng góp (improvement) đã thể hiện rõ và có thể tách riêng (qua ablation).  
- [ ] **So sánh:** Đã so sánh với các phương pháp liên quan (nếu có dữ liệu).  
- [ ] **Viết bài:** Manuscript đầy đủ (structure, refer, English/Việt) sẵn sàng, không thiếu phần quan trọng.  
- [ ] **Hạn chế:** Nhận xét hợp lý về hạn chế, work future đã nêu.  
- [ ] **Phẩm chất kỹ thuật:** Mã sạch, được công bố cùng bài (artifact).  

**Các hạng mục chặn:** Môi trường chạy ổn định; baseline hoàn thiện; kết quả thí nghiệm chính đạt chuẩn; luận văn draft hoàn chỉnh.  
**Các hạng mục không chặn:** Tối ưu hóa tham số phụ, cải thiện đóng gói artifact thêm, tinh chỉnh ngôn ngữ văn bản.

## 13. Kế hoạch 6–9 Tháng cuối

| **Thời kỳ** | **Mục tiêu chính**       | **Kết quả chủ lực**        | **Decision Gate** |
|-------------|-------------------------|---------------------------|--------------------|
| M1          | Thiết lập baseline      | Baseline chạy được        | Go/No-Go: Môi trường và baseline ổn định |
| M2          | Xác thực baseline       | Kết quả tham chiếu        | Go/No-Go: Kết quả baseline đủ tốt để so sánh |
| M3          | Triển khai cải tiến      | Hệ thống tích hợp         | Go/No-Go: Cải tiến chạy và cho kết quả sơ bộ |
| M4          | Thí nghiệm chính       | Bằng chứng chính (metrics)| Go/No-Go: Đủ dữ liệu chứng minh cải tiến |
| M5          | Ablation/robustness    | Bằng chứng phụ trợ        | Go/No-Go: Hợp lệ các thử nghiệm bổ sung |
| M6          | Phân tích cuối cùng    | Kết quả hoàn thiện        | Go/No-Go: Các phân tích ổn định, kết luận rõ |
| M7–M8       | Viết luận văn         | Bản thảo đầy đủ            | Review: Có phản hồi/chỉnh sửa luận văn |
| M9          | Hoàn thiện & Xuất bản | Luận văn + artifact + bài | Submit: Nộp luận văn, bài báo draft |

Nếu thực tế luỹ tiến của luận văn khác (dài hơn), điều chỉnh số tháng tương ứng.

## 14. Xác minh Cuối cùng về Xếp hạng Q1/Q2 và Xuất bản Baseline

- **Bài báo baseline:** *Cabello et al. (2026). “Log anomaly detection in AIOps: A real-world implementation using Large Language Models.”* Tạp chí Systems and Soft Computing.  
- **Năm công bố:** 2026 (đạt điều kiện 2023–2026).  
- **Loại ấn phẩm:** Bài báo tạp chí chính thức, peer-reviewed (Academic Press/Elsevier).  
- **Tạp chí:** Systems and Soft Computing. Theo SCImago (SJR), năm 2024 xếp hạng Q2.  
- **Xác minh:** Có DOI 10.1016/j.sasc.2026.200475 và đã xuất bản chính thức tháng 6/2026.  
- **Khẳng định:** Baseline dùng xuyên suốt chính là bài trên; *không thay đổi baseline*. Hạn chế và cải tiến cũng giữ nguyên theo đề xuất ban đầu. Bằng chứng cho xếp hạng Q2 được trích dẫn từ SCImago.  

*Không cần suy diễn dữ liệu từ Google Scholar hay hàm ý khác.* Tóm tắt xác minh:

> **Systems and Soft Computing | 2026 | SCImago (SJR) | Q2 | Published (Elsevier) | 10.1016/j.sasc.2026.200475**

## 15. Quyết định Cuối cùng

**Ưu tiên thực hiện Luận văn:**  
1. Tái tạo baseline (với kết quả tham chiếu).  
2. Triển khai cải tiến được xác định.  
3. Thực hiện thí nghiệm chính (baseline vs cải tiến).  
4. Đánh giá khả năng phát hiện sớm (Early Detection).  
5. Thí nghiệm phụ trợ (ablation, robust, efficiency).  
6. Phân tích cuối cùng (thống kê, lỗi, RQ).  
7. Viết luận văn.  
8. Hoàn thiện artifact và chuẩn bị xuất bản.  

**Tiêu chí Go/No-Go:**  
- Baseline phải chạy được với kết quả hợp lý.  
- Cải tiến phải triển khai được (mã chạy không lỗi).  
- Thí nghiệm chính thiết kế tốt, khả năng kiểm chứng giả thuyết.  
- Tài nguyên (GPU, thời gian) khả thi cho các thí nghiệm.  
- Artifact đủ chi tiết để tái lập.  

Nếu một tiêu chí thất bại, phương án *fallback* là thu hẹp lại phạm vi ở hướng cải tiến đang có (ví dụ: giảm độ phức tạp của memory module thay vì phát triển thêm module mới). Không đổi sang đề tài khác.  

**Kết luận:** Luận văn tập trung vào cải tiến rõ ràng (Memory/RAG cho LLM log anomaly) dựa trên baseline Q2 năm 2026. Phương án nghiên cứu khả thi trong 6–9 tháng, đầy đủ bằng chứng thực nghiệm, có artifact reproducible. Nếu vượt qua các cổng kiểm tra trên, kế hoạch sẽ được tiếp tục tới giai đoạn viết báo và nộp luận văn.  

**References:** Các trích dẫn đã dùng: Cabello et al. (2026) cho baseline; SCImago (Systems and Soft Computing, 2024) cho xếp hạng Q2.