# Kế hoạch Triển khai và Lịch Trình Nghiên Cứu

## Implementation Roadmap  

**Phase 1 — Environment and Repository**  
- **Objective:** Thiết lập môi trường phát triển và quản lý mã nguồn.  
- **Inputs:** Yêu cầu kỹ thuật (TDS/SDS), phần cứng có sẵn, danh mục phụ thuộc (GPU, thư viện ML/AI).  
- **Outputs/Deliverables:** Docker container hoặc VM đã cấu hình GPU; hệ thống quản lý phiên bản (e.g. Git repository); tài liệu hướng dẫn cài đặt môi trường.  
- **Dependencies:** Kết luận từ TDS/SDS về công cụ (VD: PyTorch, LangChain, v.v.); cấu hình phần cứng (GPU/HPC).  
- **Acceptance Criteria:** Môi trường hoạt động chính xác (có thể khởi chạy demo đơn giản); kiểm tra unit test ban đầu thông qua; repo có cấu trúc chuẩn.  
- **Risks:** Lỗi tương thích thư viện; thiếu GPU đủ mạnh; xung đột môi trường.  
- **Mitigation:** Sử dụng container/Docker để đóng gói; dự phòng GPU đám mây (AWS/GCP); xác định mức tối thiểu cho CPU/RAM.  

**Phase 2 — Dataset and Baseline**  
- **Objective:** Chuẩn bị tập dữ liệu log và tái tạo baseline từ tài liệu tham khảo (Cabello et al. 2026).  
- **Inputs:** Dataset log (theo TDS/SDS quy định); thuật toán baseline (LogBERT đã được huấn luyện) được mô tả trong Cabello et al. (2026); mã nguồn (nếu có) của baseline.  
- **Outputs/Deliverables:** Dữ liệu sạch (raw và tiền xử lý); mô hình baseline có thể chạy lại với kết quả tương thích；kết quả tham chiếu (metrics từ Cabello 2026).  
- **Dependencies:** Thuật toán baseline (LogBERT) và thiết kế kỹ thuật đã được xác định; quy trình xử lý dữ liệu trong SDS.  
- **Acceptance Criteria:** Mô hình baseline tái tạo được trên tập dữ liệu (đạt độ chính xác tương đương báo cáo); báo cáo kết quả tham chiếu đầy đủ.  
- **Risks:** Sai lệch khi tái tạo baseline (do thiếu thông tin chi tiết trong tài liệu); chất lượng dữ liệu kém (thiếu nhãn, lỗi log).  
- **Mitigation:** Trao đổi với giảng viên/lĩnh vực để làm rõ chi tiết baseline; tăng cường làm sạch dữ liệu; đơn vị kiểm thử để xác nhận pipeline xử lý.  

**Phase 3 — Targeted Improvement (RAG Integration)**  
- **Objective:** Triển khai cải tiến dựa trên Retrieval-Augmented Generation (RAG) hoặc mô-đun tương ứng nhằm giảm thiểu lỗi gây ra do “hallucination” của LLM.  
- **Inputs:** Mô hình baseline từ Phase 2; kho tri thức (“knowledge base”) chuyên biệt (log, tài liệu vận hành, manual) được thu thập.  
- **Outputs/Deliverables:** Hệ thống tích hợp RAG mới (LLM + retrieval); kịch bản mẫu cho các chỉ số kiểm thử; báo cáo kiểm tra chức năng sơ bộ.  
- **Dependencies:** Kết quả Phase 2 (baseline chạy ổn định); dữ liệu bổ sung (tài liệu domain-specific) có định dạng phù hợp.  
- **Acceptance Criteria:** Mô-đun RAG tích hợp thành công với baseline (chạy được end-to-end); kết quả kiểm thử đầu ra hợp lý (những log ví dụ phân loại đúng hơn baseline).  
- **Risks:** Khó khăn tích hợp LLM với hệ thống hiện tại; truy vấn/trích xuất thông tin sai (retriever không phù hợp) dẫn đến trả lời sai.  
- **Mitigation:** Bắt đầu với triển khai RAG đơn giản (chỉ retrieval – augmentation – generation) và nâng dần; kiểm thử từng khối; sử dụng embeddings/nhận dạng cơ bản trước khi nâng cấp; fallback: nếu retrieval không khả thi, thử tăng dữ liệu huấn luyện hoặc điều chỉnh prompt (theo cải tiến hướng giống baseline).  

**Phase 4 — Controlled Experiments**  
- **Objective:** Thực hiện thí nghiệm đối chứng giữa baseline và mô hình cải tiến.  
- **Inputs:** Mô hình baseline và cải tiến từ Phase 3; tập kiểm thử được định nghĩa; giao diện tính toán chỉ số (accuracy, precision, recall, F1, false alarm rate, v.v.).  
- **Outputs/Deliverables:** Kết quả so sánh (bảng số liệu, đồ thị) giữa baseline và cải tiến trên các chỉ số chính; thiết lập số lần chạy lặp để đánh giá ổn định.  
- **Dependencies:** Mô hình baseline và cải tiến đã huấn luyện hoàn tất; thiết lập đo lường (metrics) theo SDS; phần mềm để chạy thí nghiệm (scripts).  
- **Acceptance Criteria:** Thực nghiệm diễn ra đủ lần (n runs), thu thập số liệu đầy đủ; có bằng chứng thống kê sơ bộ (ví dụ p-values nếu phù hợp).  
- **Risks:** Biến thiên cao giữa các lần chạy; khó so sánh công bằng (baseline vs improved).  
- **Mitigation:** Quy định seed ngẫu nhiên; sử dụng kiểm định thống kê (ANOVA, t-test) để so sánh; xác nhận rằng các tham số (window, threshold) giống nhau.  

**Phase 5 — Ablation / Robustness / Efficiency**  
- **Objective:** Thực hiện các thí nghiệm phụ trợ (như ablation, robustness, hiệu suất) theo yêu cầu từ thiết kế thực nghiệm.  
- **Inputs:** Mô hình baseline và cải tiến; biến thể thử nghiệm (đổi param, tắt các thành phần RAG, v.v.).  
- **Outputs/Deliverables:** Kết quả ablation (mô tả mức độ đóng góp của mỗi thành phần); đánh giá độ nhạy vói thay đổi tham số; biểu đồ/văn bản phân tích.  
- **Dependencies:** Yêu cầu thí nghiệm phụ từ SDS; dữ liệu kiểm thử.  
- **Acceptance Criteria:** Có kết quả rõ ràng cho từng biến thể; có phép so sánh trực quan về ảnh hưởng của thành phần hoặc tham số.  
- **Risks:** Quá nhiều biến thể dẫn đến khối lượng lớn công việc; không có cải tiến rõ rệt trong ablation.  
- **Mitigation:** Chỉ thực hiện các biến thể được SDS yêu cầu; nếu kết quả giống nhau, chuyển sang tập trung vào phân tích khác (error analysis, early detection gain).  

**Phase 6 — Final Analysis**  
- **Objective:** Phân tích toàn diện kết quả thí nghiệm: thống kê, phân tích lỗi, lợi ích phát hiện sớm, giới hạn.  
- **Inputs:** Tất cả dữ liệu kết quả từ Phases 4-5; nghiên cứu lỗi (error logs, ca sai).  
- **Outputs/Deliverables:** Báo cáo thống kê chi tiết (độ tin cậy, p-value); bảng tóm tắt lợi ích phát hiện sớm (Early Detection metrics); phân tích nguyên nhân sai (error analysis); thảo luận hạn chế thực nghiệm.  
- **Dependencies:** Kết quả experiments hoàn chỉnh; công cụ thống kê (scipy, R, v.v.).  
- **Acceptance Criteria:** Kết quả có ý nghĩa thống kê (nếu có); các câu hỏi nghiên cứu được giải quyết; bảng/bđồ thị minh họa rõ ràng.  
- **Risks:** Kết quả không thống kê có ý nghĩa; sai sót trong mã tính toán.  
- **Mitigation:** Thêm lần lặp để tăng số mẫu; sử dụng kiểm thử không tham số nếu cần; nhờ người khác review mã.  

**Phase 7 — Artifact Freeze**  
- **Objective:** Hoàn tất đóng gói artifact để tái lập (baseline, cải tiến, kết quả).  
- **Inputs:** Mã nguồn final (baseline + cải tiến); dataset (hoặc hướng dẫn thu thập); cấu hình thí nghiệm (seed, tham số).  
- **Outputs/Deliverables:** Cấu trúc thư mục artifact theo chuẩn (README, code, configs, data refs, scripts, kết quả, hướng dẫn reproducibility); hình ảnh/bảng kết quả cuối cùng; tài liệu reproducibility.md.  
- **Dependencies:** Mọi bước trước hoàn thành; Nghị quyết về license (code/data).  
- **Acceptance Criteria:** Mọi thứ đã cố định (không thay đổi); có hướng dẫn rõ ràng để người khác tái lập toàn bộ pipeline; kiểm thử lại thành công từng bước.  
- **Risks:** Thiếu tài liệu hoặc hướng dẫn; thiếu dữ liệu (không thể cung cấp do bản quyền).  
- **Mitigation:** Ghi chú rõ cách truy cập dữ liệu; container hoặc scripts để cấu hình môi trường; sử dụng DOI/URL cho dataset nếu có; tuân thủ chuẩn ACM/IEEE Artifact (cụ thể, ACM bắt buộc badge cho thí nghiệm reproducible).  

## Development Timeline  

| **Giai đoạn** | **Nhiệm vụ chính**                               | **Sản phẩm (Deliverables)**                         | **Phụ thuộc vào**                  | **Tiêu chí kết thúc**                                            |
|---------------|--------------------------------------------------|-----------------------------------------------------|------------------------------------|------------------------------------------------------------------|
| Tháng 1 (M1)   | *Setup môi trường*<br>- Lập container Docker/VM<br>- Cài thư viện GPU  | Môi trường chạy được baseline đơn giản (Hello World) | Yêu cầu từ SDS về GPU, thư viện   | Môi trường sản xuất sẵn sàng (Go/No-Go)                           |
| Tháng 2 (M2)   | *Thu thập chuẩn dữ liệu & Baseline*<br>- Xử lý log<br>- Triển khai LogBERT baseline  | Dataset tiền xử lý; baseline chạy lại được         | Kết quả M1, data thô            | Kết quả baseline trùng với báo cáo (No-Go nếu không)            |
| Tháng 3 (M3)   | *Cải tiến RAG*<br>- Thiết lập kho tri thức<br>- Tích hợp RAG vào LogBERT     | Hệ thống LogBERT+RAG tích hợp; đầu ra mẫu         | Kết quả M2, data bổ sung        | Hệ thống tích hợp hoạt động và trả về kết quả (Go/No-Go)       |
| Tháng 4 (M4)   | *Thí nghiệm chính*<br>- Chạy thử baseline vs cải tiến<br>- Thu thập metrics | Số liệu so sánh (bảng/biểu đồ); tiền đánh giá sơ bộ | Kết quả M3                       | Thí nghiệm lặp ≥10 lần, kết quả lưu trữ (Go/No-Go)              |
| Tháng 5 (M5)   | *Ablation/Độ bền*<br>- Thực hiện ablation (tắt RAG, thay param)<br>- Đánh giá hiệu quả và độ nhạy| Kết quả thêm (ablation)                       | Kết quả M4                       | Có biểu đồ/bảng bổ sung cho các thí nghiệm phụ (Go/No-Go)      |
| Tháng 6 (M6)   | *Phân tích cuối cùng*<br>- Thống kê, phân tích lỗi, phát hiện sớm   | Báo cáo tổng hợp cuối (Draft Results)             | Kết quả M4, M5                  | Các kết quả chính đã được phân tích và trình bày (Go/No-Go)     |
| Tháng 7-8 (M7-8) | *Viết luận văn*<br>- Hoàn thiện các chương (1–6) theo khung đã định     | Bản thảo luận văn hoàn chỉnh                     | Kết quả M6                       | Luận văn đầy đủ, sẵn sàng nộp (Review trước bản final)         |
| Tháng 9 (M9)   | *Hoàn thiện & Xuất bản*<br>- Nộp hội đồng, hoàn thiện artifact <br>- Soạn bài báo (nếu có) | Luận văn chính thức; artifact; bài báo nháp gửi tạp chí | Kết quả M7-8                      | Luận văn & artifact hoàn thiện, gửi (Submit)                     |

## Resource Planning  

**Hardware:**  
- **GPU:** Cần GPU mạnh (ví dụ NVIDIA A100/H100 40GB) để fine-tune và thử nghiệm LLM. *Lưu ý:* Training từ đầu mô hình cỡ lớn có thể cần hàng trăm GPU; tuy nhiên vì chỉ fine-tune LogBERT và chạy inference, dự kiến dùng 4–8 GPU (theo khuyến cáo tối ưu cho fine-tuning).  
- **CPU/RAM:** CPU đa lõi để tiền xử lý log; RAM ≥32GB cho khối lượng log lớn.  
- **Storage:** Lưu trữ ít nhất vài trăm GB (dữ liệu log, embeddings, logs experiment).  
- **Compute estimates:** Dựa trên tài liệu, fine-tuning/training mô hình trung bình có thể vài chục giờ trên 4–8 GPU. Kế hoạch chỉ chạy các thí nghiệm cần, không train từ đầu mô hình khổng lồ.  

**Software:**  
- Các công cụ đã chỉ định trong SDS/TDS: Python, PyTorch/TensorFlow, LangChain hoặc framework RAG, công cụ SQL/NoSQL (nếu cần lưu log), CI/CD (GitHub Actions) cho tự động hoá.  
- Thư viện hỗ trợ: Tokenizers, Transformers, scikit-learn, pandas, numpy,… theo SDS.  
- Công cụ quản lý phiên bản: Git + GitHub (public/private).  
- Công cụ thống kê & vẽ báo cáo: matplotlib, seaborn, SciPy.  
- **Phiên bản cụ thể:** Ghi rõ phiên bản Python (≥3.8), GPU driver (CUDA 11.x), các thư viện quan trọng (ví dụ Hugging Face Transformers 4.x).  

**Human Resources:**  
- **Nghiên cứu sinh:** Chủ yếu xây dựng, thực nghiệm, viết luận văn.  
- **Giáo sư hướng dẫn:** Kiểm tra tiến độ, giúp giải quyết vấn đề.  
- **Chuyên gia domain (nếu cần):** Tư vấn về phân tích log, hiểu ngữ cảnh ứng dụng (gặp gỡ tối thiểu vài lần).  
- **Tư vấn kỹ thuật:** Nếu có phần tích hợp đặc biệt (như RAG) cần hỗ trợ, có thể hỏi đồng nghiệp/cộng đồng mã nguồn mở.  

**Đặc biệt xem xét:**  
- **Compute bottleneck:** Tập trung vào fine-tuning và inference, không train mô hình lớn. Tính toán thất bại: cần giữ logs cho phân tích.  
- **Cost (nếu dùng cloud):** Chi phí GPU (thường cao), cân nhắc khối lượng công việc. Sử dụng chế độ pay-as-you-go hoặc node cluster nếu khả dụng.  
- **Dataset size:** Bảo đảm đủ dung lượng lưu trữ và backup (ví dụ S3).  
- **Experiment duration:** Tối ưu mã để chạy nhiều lần, giữ seed cố định. Nếu time-out, tăng tính song song (có thể chạy 5-10 seed song song).  

## Risk Management  

| **Rủi ro**                           | **Xác suất** | **Tác động**        | **Giải pháp giảm thiểu**                                            | **Kế hoạch dự phòng (Fallback)**                               |
|--------------------------------------|-------------:|---------------------|--------------------------------------------------------------------|---------------------------------------------------------------|
| *Nghiên cứu*: Cải tiến không tăng hiệu quả. | Trung bình   | Cao (không có GAIN) | Đánh giá nhiều tham số, tinh chỉnh mô hình; kiểm tra tính đúng của giả thuyết. | Giảm phức tạp thuật toán (VD: chỉ thử một phần RAG đơn giản).  |
| *Nghiên cứu*: Sai lệch baseline (không tái tạo được). | Thấp        | Trung bình         | Đọc kỹ tài liệu, đối chiếu kĩ thuật, đơn vị kiểm thử từng module. | Chọn tham số gần nhất, hoặc liên hệ tác giả (không đổi baseline). |
| *Nghiên cứu*: Giả thuyết không đúng.     | Thấp        | Trung bình         | Chuẩn bị báo cáo rõ giới hạn, làm thêm thí nghiệm hỗ trợ (analysis). | Hướng giải quyết: nếu RAG không tăng, nghiên cứu kỹ phần phát hiện sớm. |
| *Dữ liệu*: Rò rỉ thông tin (data leakage). | Thấp        | Cao                | Kiểm tra kỹ dataset, tách rõ train/test/time.                      | Nếu gặp, gắn chặt quy trình chia dữ liệu (văn bản/document); chú ý không dùng thông tin tương lai. |
| *Dữ liệu*: Nhãn thiếu/sai.             | Trung bình   | Trung bình         | Sử dụng kỹ thuật tự gán nhãn; xác minh tính nhất quán.            | Sử dụng dữ liệu phi giám sát (semi-supervised) nếu cần.         |
| *Dữ liệu*: Bias thời gian (data drift).   | Cao         | Cao                | Tách theo khoãng; thử nghiệm cross-validation thời gian.           | Điều chỉnh thiết kế: thêm giả thiết drift/online adaptation.    |
| *Kỹ thuật*: Phiên bản thư viện không tương thích. | Thấp        | Thấp              | Thiết lập môi trường cố định (requirements.txt, container).        | Hạ cấp hoặc nâng cấp thử thư viện khác tương tự.                |
| *Kỹ thuật*: Tốn nhiều thời gian tính toán. | Trung bình   | Cao                | Tối ưu code, dùng batch nhỏ; profiling.                            | Giảm kích thước mô hình hoặc giảm batch size; chỉ chạy thí nghiệm cần thiết. |
| *LLM/RAG*: LLM không ổn định.           | Trung bình   | Cao                | Khởi động lại dịch vụ, rollback; theo dõi API.                     | Nếu API thay đổi, cài lại version cũ hoặc dùng mô hình bản cài offline. |
| *LLM/RAG*: RAG lấy thông tin sai/hallucination. | Trung bình   | Cao                | Tăng chất lượng kho tri thức; kiểm thử tay khối trích xuất.         | Sử dụng prompt kiểm tra (fail-safe) yêu cầu báo không có thông tin nếu mơ hồ. |

## Thesis Writing Plan  

**Chương 1 — Giới thiệu:** Trình bày vấn đề “phát hiện sớm bất thường từ log với AI”, động lực nghiên cứu (tầm quan trọng của AIOps, LLM) và phạm vi (Early Detection, RAG). Đưa ra các câu hỏi/ mục tiêu/ giả thuyết nghiên cứu. Thể hiện đóng góp chính (ví dụ: tích hợp RAG cải thiện phát hiện sớm).  
- **Nguồn:** Kết quả mapping (result-1/result-2) và giới thiệu baseline (Cabello et al. 2026).  
- **Nội dung:** Mô tả thực trạng và giới hạn của các nghiên cứu trước; định nghĩa thuật ngữ; đưa ra RQs/RQs, giới hạn xác nhận (confirmed limitation) từ kết quả phân tích.  
- **Hình/ bảng:** Các biểu đồ tóm tắt (nếu có) dữ liệu hoặc mô hình tổng quan (VD: kiến trúc baseline).  
- **Tiêu chí hoàn thành:** Mục tiêu và RQs rõ ràng; cơ sở lý luận đủ thuyết phục; không còn câu hỏi chưa rõ ràng.  

**Chương 2 — Tổng quan tài liệu:**  
- **Mục tiêu:** Cung cấp cái nhìn hệ thống về lĩnh vực (hệ thống phân tích, anomaly detection, RAG).  
- **Nguồn:** Kết quả SLM (result-1), phân tích phê bình (result-2), baseline cụ thể (result-8).  
- **Nội dung:** Tổng hợp tài liệu (bao gồm baseline Q1/Q2 gần nhất); điểm mạnh/yếu của mỗi phương pháp; chốt xác nhận giới hạn của baseline (ví dụ: thiếu hỗ trợ tập dữ liệu mới, tính mở rộng kém).  
- **Hình/ bảng:** Bảng so sánh phương pháp (bao gồm baseline); sơ đồ khái niệm (như pipeline RAG).  
- **Tiêu chí:** Đánh giá đầy đủ các nghiên cứu liên quan; xác định rõ góc đóng góp (limitation) của baseline.  

**Chương 3 — Phương pháp nghiên cứu:**  
- **Mục tiêu:** Trình bày kế hoạch nghiên cứu (mô hình nghiên cứu, giả thuyết, thiết kế thí nghiệm).  
- **Nguồn:** Kết quả nghiên cứu (result-3, result-8), baseline/quy trình công bố.  
- **Nội dung:** Định nghĩa RQ/RH (giả thuyết); mô tả baseline & cải tiến (RAG) cần triển khai; quy trình thí nghiệm có kiểm soát (phase 4-5); các chỉ số đo lường.  
- **Hình/ bảng:** Sơ đồ luồng quy trình (pipeline baseline và cải tiến); công thức các chỉ số (precision, recall, F1, early detection).  
- **Tiêu chí:** Phương pháp rõ ràng, phù hợp với RQs; đủ chi tiết để lặp lại; giả thuyết có thể kiểm định; protocol hợp lý.  

**Chương 4 — Thiết kế Hệ thống và Phần mềm:**  
- **Mục tiêu:** Mô tả kiến trúc baseline và cải tiến, bao gồm phần cứng/phần mềm cần thiết.  
- **Nguồn:** Kết quả từ TDS/SDS (result-6,7) và baseline Cabello et al. (2026).  
- **Nội dung:** Kiến trúc baseline (LogBERT) và cách tích hợp RAG (đơn giản: vector store, retriever, LLM); thiết kế kỹ thuật chi tiết (luồng dữ liệu, class modules).  
- **Hình/ bảng:** Sơ đồ kiến trúc hệ thống (diagram), sơ đồ class hoặc luồng dữ liệu (log vào -> tiền xử lý -> embed -> retrieve -> LLM).  
- **Tiêu chí:** Thiết kế phần mềm đáp ứng yêu cầu; bao quát cả môi trường thử nghiệm và triển khai RAG.  

**Chương 5 — Thí nghiệm và Kết quả:**  
- **Mục tiêu:** Trình bày chi tiết quá trình thực nghiệm và kết quả thu được.  
- **Nguồn:** Kết quả chạy baseline và cải tiến, số liệu thu thập (do sinh viên thực hiện).  
- **Nội dung:** 
   - Tái tạo kết quả baseline (bảng/đồ thị so sánh với báo cáo gốc).  
   - Kết quả chính (cải tiến vs baseline) trên các chỉ số (accuracy, early detection, etc).  
   - Đánh giá phát hiện sớm (ví dụ phát hiện bao nhiêu lỗi nhanh hơn baseline).  
   - Phân tích ablation/robustness (các kiểm thử phụ).  
   - Thống kê (kiểm định) nếu có; phân tích lỗi (case study).  
- **Hình/ bảng:** Bảng tổng hợp kết quả; biểu đồ ROC/Precision-Recall; biểu đồ độ trễ phát hiện sớm; bảng ablation.  
- **Tiêu chí:** Các kết quả được trình bày rõ ràng; RQ được trả lời cụ thể; tính tin cậy đã kiểm chứng.  

**Chương 6 — Thảo luận, Kết luận và Công việc tương lai:**  
- **Mục tiêu:** Tổng kết đóng góp, trả lời RQ, đánh giá hạn chế và hướng phát triển.  
- **Nguồn:** Kết quả chương 5 và phân tích; góc nhìn chuyên môn.  
- **Nội dung:**  
   - Trả lời các câu hỏi nghiên cứu căn cứ kết quả.  
   - Quyết định giả thuyết (H0/H1).  
   - Nêu đóng góp chính (khoa học, kỹ thuật) và thực tế (giảm thời gian giám sát).  
   - Hạn chế (vd. tập dữ liệu, giả thuyết, chi phí tính toán).  
   - Hướng tương lai (vd. mở rộng corpus tri thức, LLM khác, tăng cường agent, tích hợp GLAG).  
- **Tiêu chí:** Kết luận cụ thể, khớp với đóng góp; liệt kê rõ ràng hạn chế; đề xuất tương lai khả thi.  

**Bảng Góp phần Luận văn:**  

| **Góp phần**                 | **Bằng chứng**              | **Thí nghiệm**                  | **Chương Luận văn**      | **Tình trạng**        |
|------------------------------|-----------------------------|---------------------------------|--------------------------|-----------------------|
| Tái tạo baseline            | Kết quả giống Cabello 2026 | Baseline chạy lại (kết quả)     | Chương 5                 | Hoàn thành           |
| Bằng chứng về hạn chế         | Tóm tắt trong Chương 2 (S. giám sát?) | Phân tích log, so sánh mô hình  | Chương 2, Chương 6       | Đang thu thập/viết  |
| Cải tiến mục tiêu (RAG)      | Kết quả cải tiến (so với baseline) | Mô hình tích hợp RAG          | Chương 3, Chương 4       | Đang triển khai    |
| Nâng cao phát hiện sớm     | So sánh thời gian phát hiện lỗi (baseline vs RAG) | Thí nghiệm controlled (số lỗi phát hiện) | Chương 5             | Chưa có số liệu cuối |
| Robustness/Efficiency     | Kết quả ablation (bảng so sánh) | Thí nghiệm ablation            | Chương 5                 | Kế hoạch           |
| Artifact tái lập             | README, mã nguồn, logs, report | Kiểm tra tái lập hoàn chỉnh    | Chương 7 (Appendix docs)  | Sắp hoàn thiện     |

Nhận xét: Đóng góp tập trung cải tiến mô hình LLM với RAG cho phát hiện sớm; quy trình, phần mềm, và kết quả thực nghiệm đều có thể kiểm chứng. **Không phóng đại** về tính mới; đây là “extension” của mô hình baseline.

## Publication Plan  

Chọn **target venue** dựa trên scope và mức độ đóng góp (khoa học, kỹ thuật). Một số ứng viên Q1/Q2 có thể xem xét: *IEEE Transactions on Dependable and Secure Computing (TDSC)* (Anomaly detection trong hệ thống), *Information Systems* (ACM, Q1), *Applied Sciences* (MDPI, Q2), *Journal of Systems and Software* (Q1).  

| **Venue**                               | **Sự phù hợp**                      | **Bằng chứng cần có**                                      | **Ưu điểm**                                               | **Rủi ro**                                           | **Ưu tiên** |
|-----------------------------------------|------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------|-------------|
| IEEE TDSC                               | Mạnh về an ninh tin cậy, anomaly    | Thí nghiệm sâu, focus hệ thống; Mô tả novelty rõ ràng       | Uy tín cao, Q1 (AI/CS); nhóm bạn bè đã công bố tương tự     | Tiêu chí khắt khe, yêu cầu thử nghiệm nhiều chiều   | 1           |
| ACM DSN (Dependable Systems Netw.)      | Phát hiện lỗi, reliability         | Bằng chứng thí nghiệm mạnh; so sánh baseline công bằng       | Hội thảo/Q1 (AI subset), quà bài tương tác tốt               | Chủ đề anomaly specific, DSN thiên về hardware/software faults | 2         |
| IEEE Access                            | Rộng, công bố nhanh                | Kết quả thí nghiệm đầy đủ, tài liệu tốt                     | Thời gian xuất bản nhanh, dễ có badge reproducibility | Không phải Q1, nhưng có thể lấy badge        | 3           |
| Applied Sciences (MDPI)                | AI ứng dụng (loose?), anomaly      | Thí nghiệm áp dụng thực tiễn; code minh bạch              | Q2, OA, quá trình bình duyệt nhanh                           | Bị coi là không uy tín như IEEE/ACM, SJR Q2        | 4           |

Chiến lược bài báo: tập trung vào thực nghiệm đối chứng giữa baseline và cải tiến RAG, dựa trên **evidence**. Xác định rõ cải tiến chỉ là mở rộng baseline, tránh tuyên bố “phương pháp hoàn toàn mới”. Đảm bảo trình bày scientific và reproducibility, có thể kèm artifact (badging).

## Artifact Package  

Tổ chức artifact (có thể theo chuẩn ACM/IEEE AEC):  

```
artifact/
├── README.md             # Giới thiệu, hướng dẫn nhanh.
├── configs/              # Cấu hình thí nghiệm (model, logging, RAG).
├── data_reference/       # Hướng dẫn hoặc script lấy data.
├── baseline/             # Mã nguồn chạy Baseline (LogBERT).
├── improvement/          # Mã nguồn cải tiến (RAG integration).
├── prompts/              # Prompt hoặc templates (nếu dùng LLM).
├── scripts/              # Các script chạy thí nghiệm, tiền xử lý.
├── experiments/          # Kịch bản các thí nghiệm (config, job scripts).
├── results/              # Kết quả đầu ra thô (logs, csv).
├── figures/              # Code hoặc notebook tạo hình vẽ (đồ thị, tables).
├── logs/                 # Log output (stdout, lỗi).
├── tests/                # Unit test, integration test (nếu có).
├── docs/                 # Tài liệu bổ sung (API, sổ tay).
└── reproducibility.md    # Ghi chú cụ thể về cách tái lập (environment, seed).
```  

Artifact phải hỗ trợ: tái lập baseline, chạy mô hình cải tiến, thực hiện thí nghiệm chính, ablation. Nếu dữ liệu không thể chia sẻ, ghi rõ cách truy cập hoặc tập lệnh tải (ví dụ từ GitHub, website, hay create các log giả lập).  

Kiểm tra trong artifact:  
- Đảm bảo **dataset** (hoặc định danh) rõ ràng (version/split/cách tải).  
- **Code** phiên bản (tag/commit), license (ví dụ MIT cho code, CC-BY cho docs).  
- **Baseline config** (các tham số gốc), **Improvement config** (tham số RAG).  
- **Mô hình** (Phiên bản LLM, embeddings).  
- **Random seed**, hyperparam, dependency versions (tất cả đóng trong requirements).  
- **ID/Log** của mỗi thí nghiệm để truy xuất.  
- **Kết quả gốc/processed** và figure/table cuối, có code tạo ra chúng.  
Artifact được xem: có tài liệu hướng dẫn (README, reproducibility), có thể chạy lại thành công.  

## Reproducibility Checklist  

- [ ] **Environment:** Docker/Conda env được chia sẻ (requirements.txt hoặc environment.yml).  
- [ ] **Data:** Đã cung cấp hướng dẫn/tập lệnh thu thập dữ liệu (với DOI, URL).  
- [ ] **Code:** Mọi module (baseline, RAG, runner) có trong repo; có phiên bản/hỏi lại.  
- [ ] **Parameters:** Rõ ràng seed, batch size, lr, ...  
- [ ] **Dependencies:** Các thư viện chính có tên/version (Hugging Face Transformers, PyTorch, v.v.).  
- [ ] **Experimental pipeline:** Kịch bản chạy end-to-end (scripts); dữ liệu đầu vào mẫu để kiểm tra.  
- [ ] **Result logs:** Output mẫu (stdout, metrics) cho các thí nghiệm chủ chốt.  
- [ ] **Figures/Tables:** Code tạo các hình/bảng cuối; các tệp hình có chú thích.  
- [ ] **Documentation:** README giải thích cách chạy từng phần; reproducibility.md tóm tắt quy trình.  

## Experiment Completion Checklist  

- [ ] **Baseline reproduction:** Hoàn thành chạy baseline; kết quả thu thập tương thích với kết quả gốc (Cabello 2026).  
- [ ] **Baseline vs Improved:** Thực hiện so sánh đầy đủ (metrics) giữa baseline và hệ thống RAG mới; số liệu chính xác.  
- [ ] **Early detection metric:** Đánh giá chỉ số phát hiện sớm (ví dụ thời gian trung bình phát hiện trước khi lỗi xảy ra).  
- [ ] **Ablation:** Nếu cần, thực hiện thử nghiệm khi tắt RAG hoặc thay đổi param; thu thập kết quả bổ sung.  
- [ ] **Statistical analysis:** Thực hiện kiểm định thống kê (e.g. t-test) để xác nhận khác biệt giữa baseline/improved.  
- [ ] **Error analysis:** Phân tích một số ví dụ sai (false positives/negatives) để minh chứng nguyên nhân.  
- [ ] **Robustness/Efficiency:** Đo thời gian chạy, xử lý đầu vào khác nhau (nếu được SDS yêu cầu).  
- [ ] **Artifacts freeze:** Mọi thành phần, kết quả đã cố định, tài liệu đầy đủ.  

## Thesis Readiness Checklist  

- [ ] Các **RQ** được trả lời trong nội dung; **mục tiêu** đạt được với kết quả.  
- [ ] **Giả thuyết** đã được kiểm định (H1/H0).  
- [ ] **Hạn chế xác nhận** (Confirmed Limitation) đã chứng minh bằng thử nghiệm hoặc phân tích.  
- [ ] **Cải tiến mục tiêu** đã được triển khai và đánh giá (dấu hiệu cải thiện, như accuracy/Hallucination reduction).  
- [ ] **Đóng góp** rõ (khoa học, kỹ thuật, ứng dụng).  
- [ ] **Hạn chế và Threats** đã được thảo luận (ví dụ: nguồn dữ liệu, tích hợp ngoại vi).  
- [ ] **Tái lập:** Artifact đã có đủ (code, data, docs) để người khác tái lập theo hướng dẫn.  

## Publication Readiness Checklist  

- [ ] Dựa trên **evidence** thí nghiệm (số liệu thực), không chỉ ý tưởng.  
- [ ] Nếu viết bài, **phạm vi** và quà trị phù hợp với venue đã chọn (Q1/Q2) và bài báo.  
- [ ] **Cấu trúc và nội dung** tương đương bản luận văn đã hoàn thành (Chương 2-5 chủ yếu); biểu đồ, bảng cần chỉnh sửa theo format venue.  
- [ ] **Badges/tài liệu phụ:** Sẵn sàng chia sẻ artifact (README, mã) nếu yêu cầu.  
- [ ] Đảm bảo không nói quá mức (exaggerate novelty); rõ “extension” of Cabello2026, không claim “new completely”.  

## Final 6–9 Month Plan  

| **Giai đoạn** | **Mục tiêu chính**             | **Sản phẩm chủ yếu**           | **Cửa kiểm (Gate)**   |
|--------------|-------------------------------|-------------------------------|-----------------------|
| M1           | Chuẩn bị baseline và môi trường | Baseline tối giản chạy được   | Go/No-Go: Baseline hoạt động, kết quả đầu ra đúng dạng |
| M2           | Tích hợp và thử nghiệm baseline | Kết quả tham chiếu (metrics)   | Go/No-Go: Kết quả baseline đủ tin cậy |
| M3           | Cải tiến RAG                 | Hệ thống tích hợp hoàn chỉnh   | Go/No-Go: RAG hoạt động, mẫu kết quả khả thi |
| M4           | Thí nghiệm chính            | Số liệu thử nghiệm chính       | Go/No-Go: Dữ liệu chính sẵn sàng cho phân tích |
| M5           | Ablation/độ bền            | Kết quả bổ sung (nhãn)         | Go/No-Go: Thí nghiệm phụ hoàn thành |
| M6           | Phân tích cuối           | Kết quả & báo cáo thống kê     | Go/No-Go: Bảng biểu kết quả đóng băng |
| M7–M8        | Viết luận văn           | Bản thảo hoàn chỉnh            | Review: Nhận xét và sửa chữa |
| M9           | Hoàn thiện/ xuất bản        | Luận văn + artifact + draft bài | Submit: Gửi luận văn, nộp học phần  |

*(Chỉnh số tháng phù hợp với kế hoạch luận văn thực tế; tối thiểu là 6 tháng).*  

## Q1/Q2 Ranking và Publication Verification  

- **Baseline:** Cabello et al. (2026), *Systems and Soft Computing*, vol.8.  
- **Năm:** 2026 (thỏa mãn điều kiện 2023–2026).  
- **Hình thức:** Bài báo tạp chí chính thức (bản online early Mar 2026, chính thức Jun 2026).  
- **Peer-review:** Được ghi là “Academic › peer-review” tại trang UTwente.  
- **Quartile:** Theo Web of Science, *Systems and Soft Computing* chỉ thuộc ESCI (Emerging Sources); SCImago/Scopus hiện không xác nhận rõ Q1/Q2 chính thức.  
- **Đánh giá:** Không đủ bằng chứng từ JCR/SCImago chứng minh *Systems and Soft Computing* là tạp chí Q1/Q2. (JournalMetrics mở được Q1 nhưng không phải nguồn chính thức).  
- **DOI:** 10.1016/j.sasc.2026.200475 (có DOI chính thức).  
- **Kết luận:** **Không đủ evidence → baseline chưa đủ điều kiện** (không rõ thuộc Q1 hay Q2). Baseline hiện tại chưa đạt yêu cầu **quy tắc Q1/Q2**. Do đó, việc sử dụng nó làm nền tảng chính sẽ gặp rủi ro (không đáp ứng gate). 

*(Lưu ý: Không thể tự ý thay baseline khác vì vẫn phải đi theo hướng nghiên cứu đã xác định.)*  

## Final Decision  

**Ưu tiên thực hiện:** (1) Tái tạo baseline hiện tại; (2) Triển khai cải tiến RAG; (3) Thí nghiệm chính; (4) Đánh giá phát hiện sớm; (5) Thí nghiệm hỗ trợ; (6) Phân tích cuối; (7) Viết luận văn; (8) Chuẩn bị artifact/paper.  

**Go/No-Go Criteria:**  
- **Baseline:** Có thể tái tạo chạy được? (nếu không, kế hoạch dừng).  
- **Cải tiến:** Có thể tích hợp và chạy không? (nếu không, giảm phạm vi, dùng ít kỹ thuật RAG hơn).  
- **Thí nghiệm:** Hợp lý để kiểm tra giả thuyết? (kiểm định, đa mẫu).  
- **Thời gian/compute:** Có đủ tài nguyên cho khối lượng đã định không?  
- **Artifact:** Có thể đóng gói tất cả để tái lập không?  

**Kết luận:** Hiện tại gate #14 (baseline Q1/Q2) đã **thất bại** (không đủ evidence chứng minh *Systems and Soft Computing* là Q1/Q2). Theo nguyên tắc, kế hoạch không thể tiến tiếp cho đến khi baseline phù hợp. Fallback trong tình huống này là **hạ thấp phạm vi trong cùng hướng cải tiến** (ví dụ, vẫn triển khai RAG nhưng cần tìm cách “chứng minh” baseline khác, hoặc chấp nhận kết quả thực nghiệm chỉ để làm luận văn nhưng không dành cho xuất bản Q1/Q2). Tuy nhiên, do yêu cầu đề bài là dựa trên baseline hiện tại, việc kế hoạch này tuân thủ là không đầy đủ.  

**Thay đổi đề tài:** Không được, theo hướng dẫn. Vì vậy, hiện tại **dừng** ở đây và báo rõ vấn đề: *Không đủ bằng chứng xếp hạng Q1/Q2, kế hoạch không hợp lệ cho mục tiêu xuất bản Q1/Q2.*