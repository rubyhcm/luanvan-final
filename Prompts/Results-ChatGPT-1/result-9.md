# Lộ trình Triển khai (Implementation Roadmap)

Dựa trên thiết kế thực nghiệm cuối cùng (result-8.md) đã xác định, chúng ta chia lộ trình triển khai thành các giai đoạn chính theo dependency thực tế. Mỗi giai đoạn nêu rõ mục tiêu, đầu vào, đầu ra, kết quả bàn giao (deliverables), các phụ thuộc, tiêu chí thành công và rủi ro chính.

### Giai đoạn 1 – Môi trường và kho mã nguồn  
- **Mục tiêu:** Thiết lập môi trường lập trình và quản lý phiên bản phù hợp cho nghiên cứu.  
- **Đầu vào:** Kết quả thiết kế kỹ thuật (Technical Design) và thiết kế phần mềm (Software Design) từ result-6.md và result-7.md; thông tin về công nghệ cần sử dụng.  
- **Đầu ra:** Môi trường lập trình sẵn sàng (Python, thư viện AI), kho mã nguồn (Git) với cấu trúc ban đầu cho từng module (baseline, improvement).  
- **Deliverables:** Cấu hình môi trường (gói cài, Dockerfile nếu cần), repository git mẫu với các thư mục cơ bản và tệp README khởi tạo.  
- **Phụ thuộc:** Không phụ thuộc giai đoạn trước; đảm bảo có truy cập phần cứng (GPU/CPU) cần thiết.  
- **Tiêu chí thành công:** Có thể chạy thử một script mẫu (ví dụ: kiểm tra import thư viện, kết nối API) thành công. Repository có đầy đủ các nhánh/kho lưu trữ cần thiết.  
- **Rủi ro:** Vấn đề tương thích thư viện, thiếu giấy phép cho API (OpenAI), lỗi thiết lập đường dẫn, chi phí GPU cao. Mitigation: Sử dụng container (Docker), tài liệu hướng dẫn thiết lập rõ ràng.

### Giai đoạn 2 – Chuẩn bị dữ liệu và Baseline  
- **Mục tiêu:** Chuẩn bị bộ dữ liệu log và thực hiện tái tạo (reproduce) mô hình baseline theo kết quả tham chiếu (baseline 2025–2026).  
- **Đầu vào:** Thiết kế thực nghiệm (result-8.md) xác định bộ dữ liệu và phương pháp baseline, hướng dẫn trong SDS (result-7.md).  
- **Đầu ra:** Dữ liệu đã làm sạch và tiền xử lý (log cleaned/split labels), mã nguồn triển khai baseline, kết quả đầu tiên của baseline (metrics, báo cáo).  
- **Deliverables:** Tập dữ liệu sẵn sàng (đã phân chia train/validation/test); mã và hướng dẫn chạy baseline; báo cáo kết quả đầu tiên (ví dụ: độ chính xác, F1, thời gian phát hiện).  
- **Phụ thuộc:** Môi trường từ Gđ1 phải hoạt động ổn định; cần có dữ liệu gốc hoặc hướng dẫn tải dữ liệu.  
- **Tiêu chí thành công:** Chạy được baseline với kết quả hợp lý, so sánh được với kết quả tham chiếu (cần chênh lệch nhỏ nếu có).  
- **Rủi ro:** Dữ liệu không đúng định dạng, thiếu nhãn (class imbalance), baseline không chạy được (cài đặt sai). Mitigation: Chuẩn bị script kiểm tra dữ liệu, sử dụng thuật toán baseline đơn giản làm bước khởi động, theo dõi logs để sửa lỗi kịp thời.

### Giai đoạn 3 – Triển khai cải tiến (Targeted Improvement)  
- **Mục tiêu:** Phát triển và tích hợp giải pháp cải tiến đã xác định (ví dụ: LLM tăng cường bộ nhớ/tri thức) vào pipeline baseline.  
- **Đầu vào:** Kết quả baseline (mã và dữ liệu), thiết kế kỹ thuật mô tả cải tiến (result-6.md, result-7.md).  
- **Đầu ra:** Mô hình cải tiến tích hợp với pipeline baseline, mã nguồn chạy thử nghiệm.  
- **Deliverables:** Mã nguồn cải tiến (ví dụ mô-đun RAG hoặc Memory-LLM), hướng dẫn cấu hình, kết quả test khởi tạo cho cải tiến.  
- **Phụ thuộc:** Hoàn thành Gđ2 (baseline chạy ổn định); cần thư viện bổ sung (retrieval, memory).  
- **Tiêu chí thành công:** Cải tiến chạy mà không lỗi, kết quả mô hình ổn định trên tập nhỏ (dữ liệu kiểm tra).  
- **Rủi ro:** Phức tạp trong tích hợp (dependency xung đột), hiệu năng kém (model quá nặng), thiếu kinh nghiệm với RAG/LLM. Mitigation: Phát triển từng phần riêng biệt, sử dụng thư viện được hỗ trợ (vd. Haystack, LangChain), thử trên subset nhỏ trước.

### Giai đoạn 4 – Thí nghiệm có kiểm soát (Controlled Experiments)  
- **Mục tiêu:** Tiến hành thí nghiệm so sánh trực tiếp giữa baseline và mô hình cải tiến, thu thập số liệu.  
- **Đầu vào:** Mã và dữ liệu từ Gđ2 (baseline) và Gđ3 (improvement).  
- **Đầu ra:** Kết quả thí nghiệm (bảng so sánh, đồ thị) thể hiện hiệu suất baseline vs cải tiến theo các metric chính.  
- **Deliverables:** Báo cáo kết quả thô (log), biểu đồ so sánh metric (độ chính xác, F1, khoảng thời gian phát hiện sớm), kịch bản chạy thí nghiệm nhiều lần (toàn bộ công cụ).  
- **Phụ thuộc:** Gđ2 và Gđ3 phải hoàn thành (cả hai mô hình sẵn sàng so sánh).  
- **Tiêu chí thành công:** Thí nghiệm chính (theo Kịch bản từ result-8) được lặp đủ lần, thu đủ số liệu, ghi nhận được sự khác biệt (dương hoặc âm) giữa baseline và cải tiến.  
- **Rủi ro:** Kết quả bị nhiễu do biến thiên ngẫu nhiên, không đủ dữ liệu thực nghiệm (chạy không hoàn thành trong thời gian), tiêu chí so sánh chưa phù hợp. Mitigation: Định nghĩa seed cố định, chạy nhiều lần, sử dụng phân tích thống kê, ghi lại log chi tiết.

### Giai đoạn 5 – Ablation / Độ bền / Hiệu quả (nếu có yêu cầu)  
- **Mục tiêu:** Thực hiện các thí nghiệm bổ sung (nếu được yêu cầu trong result-8) để kiểm chứng độ đóng góp của thành phần cụ thể hoặc đánh giá hiệu suất.  
- **Đầu vào:** Mã và kết quả từ Gđ4, chi tiết thử nghiệm bổ sung (result-8.md).  
- **Đầu ra:** Kết quả ablation hoặc thử nghiệm hiệu năng (bảng, đồ thị).  
- **Deliverables:** Báo cáo thí nghiệm bổ trợ (như thay đổi tham số, loại bỏ module, đánh giá tốc độ), số liệu liên quan.  
- **Phụ thuộc:** Gđ4 hoàn thành (có thể thực hiện trên hệ thống có sẵn).  
- **Tiêu chí thành công:** Các thử nghiệm bổ sung cung cấp thông tin về đóng góp của từng thành phần hoặc hiệu quả bổ sung.  
- **Rủi ro:** Thời gian hạn chế không đủ thực hiện thêm, phạm vi thí nghiệm phụ không rõ ràng. Mitigation: Ưu tiên những thử nghiệm quan trọng nhất, nếu cần lược bỏ các biến thể ít quan trọng.

### Giai đoạn 6 – Phân tích cuối cùng (Final Analysis)  
- **Mục tiêu:** Phân tích chi tiết kết quả thí nghiệm, thực hiện so sánh thống kê, kiểm tra sớm phát hiện, đánh giá lỗi và hạn chế.  
- **Đầu vào:** Dữ liệu và kết quả từ Gđ4 (và Gđ5 nếu có).  
- **Đầu ra:** Báo cáo phân tích (thống kê kiểm định, biểu đồ, phân tích lỗi), nhận xét so sánh hiệu quả phát hiện sớm giữa baseline và cải tiến.  
- **Deliverables:** Bảng kết quả thống kê (độ tin cậy, p-value), đồ thị error analysis, báo cáo chi tiết (có thể kèm hình minh họa).  
- **Phụ thuộc:** Gđ4 (và Gđ5) hoàn thành đầy đủ kết quả thô.  
- **Tiêu chí thành công:** Tất cả metric chính đều được phân tích (bao gồm sớm phát hiện), xác định được hạn chế của mô hình, thu được bằng chứng thỏa đáng cho/nổi bật hạn chế đã xác định trước và sự cải thiện (nếu có).  
- **Rủi ro:** Không tìm thấy sự khác biệt có ý nghĩa, số liệu không đồng nhất, thiếu bằng chứng cho các giả thuyết. Mitigation: Đảm bảo chạy đủ lần để thống kê, kiểm tra các giả thuyết thay thế, minh bạch báo cáo cả kết quả âm.

### Giai đoạn 7 – Hoàn tất artifact (Artifact Freeze)  
- **Mục tiêu:** Đóng băng mọi cấu hình, mã nguồn, kết quả và tài liệu để đảm bảo tính tái lập, sẵn sàng bàn giao toàn bộ artifact.  
- **Đầu vào:** Mã và kết quả cuối từ các giai đoạn trước (Gđ1–6).  
- **Đầu ra:** Gói artifact hoàn chỉnh (code, dữ liệu mẫu/đường dẫn, kết quả đã xử lý, tài liệu hướng dẫn reproducibility).  
- **Deliverables:** Thư mục artifact đúng cấu trúc, bao gồm toàn bộ thành phần (code, config, dữ liệu mẫu hoặc hướng dẫn download, scripts chạy, logs, figures/tables, reproducibility.md).  
- **Phụ thuộc:** Tất cả giai đoạn trước đã hoàn thành (gói artifact chỉ freeze khi kết quả ổn định).  
- **Tiêu chí thành công:** Mọi tài nguyên cần thiết đã được lưu trữ và ghi chú phiên bản; tài liệu hướng dẫn đầy đủ để người khác tái lập kết quả.  
- **Rủi ro:** Thiếu mục trong artifact (code, file config, dữ liệu), thông tin về môi trường không rõ ràng, sai lệch phiên bản; Mitigation: Kiểm tra checklist artifact một lần cuối, sử dụng hệ thống CI để xác minh, lưu notebook và logs chạy.

## 2. Lịch trình Phát triển (Development Timeline)

| Thời gian | Nhiệm vụ chính | Deliverables | Phụ thuộc | Tiêu chí hoàn thành |
|---|---|---|---|---|
| **Tháng 1 (M1)** | Thiết lập môi trường, repo; thu thập xử lý dữ liệu ban đầu | Môi trường Python chuẩn, repo Git với cấu trúc mẫu | – | Environment thiết lập hoàn tất, repo sẵn sàng dùng |
| **Tháng 2 (M2)** | Triển khai và chạy thử baseline; hoàn thiện preprocessing data | Kết quả benchmark cơ sở (sơ bộ), mã baseline | M1 | Baseline chạy được, đạt kết quả tham chiếu ban đầu |
| **Tháng 3 (M3)** | Phát triển mô hình cải tiến và tích hợp với baseline | Prototype improvement, test tích hợp | M2 | Cải tiến tích hợp thành công (đạt tính ổn định trên subset) |
| **Tháng 4 (M4)** | Thực hiện thí nghiệm chính (baseline vs cải tiến), nhiều lần chạy | Dữ liệu kết quả chính (bảng, đồ thị so sánh) | M3 | Thí nghiệm hoàn thành đủ lần, thu thập số liệu đúng yêu cầu |
| **Tháng 5 (M5)** | Thực hiện thí nghiệm bổ sung (ablation, robustness) | Số liệu bổ sung (bảng, biểu đồ) | M4 | Thí nghiệm hỗ trợ hoàn thành (nếu thuộc yêu cầu) |
| **Tháng 6 (M6)** | Phân tích kết quả: kiểm định thống kê, phân tích lỗi, sớm phát hiện | Báo cáo phân tích, figures/thống kê | M4, M5 | Kết quả được phân tích đầy đủ, có nhận xét, biểu đồ, kiểm định |
| **Tháng 7 (M7)** | Viết luận văn các chương 1–3; hoàn thiện artifact | Bản thảo chương 1–3, sơ đồ kiến trúc, docs artifact | M6 | Hoàn tất bản nháp chương 1–3, artifact cơ bản đã có tài liệu |
| **Tháng 8 (M8)** | Viết luận văn chương 4–5, chỉnh sửa toàn bộ; chuẩn bị công bố | Bản thảo hoàn chỉnh các chương, tài liệu reproducibility | M7 | Bản nháp chương 1–5 hoàn thiện, kiểm tra phản hồi, artifact ổn định |
| **Tháng 9 (M9)** | Hoàn thiện luận văn và bài báo, đóng gói nộp | Luận văn cuối cùng, artifact freeze, nháp bài báo | M8 | Luận văn + artifact + nháp báo cáo sẵn sàng nộp |

## 3. Kế hoạch Nguồn lực (Resource Planning)

- **Phần cứng:** Cần một hệ thống hoặc máy chủ với GPU (tối thiểu 1 GPU NVidia tương đương 12-16GB VRAM hoặc truy cập dịch vụ đám mây GPU) để xử lý LLM. CPU ≥ 8 lõi, RAM ≥ 32GB, dung lượng lưu trữ ~100GB cho dataset và kết quả. Dự kiến sử dụng GPU để tính toán mô hình (nghiên cứu với LLM thường tốn tài nguyên), dự trữ RAM cho xử lý dữ liệu lớn và lưu trữ logs. Nên chuẩn bị dự phòng cho tính toán đám mây (AWS/GCP credit) nếu máy cục bộ không đủ.  
- **Phần mềm:** Sử dụng ngôn ngữ Python (phiên bản mới nhất) và các thư viện như PyTorch, Hugging Face Transformers, scikit-learn, Pandas. Nếu dùng các foundation model: OpenAI API (GPT-4) hoặc mô hình offline (LLaMA/Mistral) với các thư viện hỗ trợ. Nếu áp dụng RAG/Memory: thư viện LangChain hoặc haystack để tích hợp retrieval. Công cụ quản lý mã: Git/GitHub. Quản lý môi trường: Docker/Conda. Nếu có GUI thì Jupyter Notebook hoặc Colab cho phát triển. Các công cụ hỗ trợ khác: Matplotlib/Seaborn cho vẽ biểu đồ; pandas/numpy cho xử lý dữ liệu; có thể dùng TensorBoard để theo dõi. Chỉ liệt kê các công cụ được đề cập trong SDS: ví dụ nếu SDS đề cập đến OpenAI API, LangChain, FAISS/Pinecone, thì ghi chính xác.  
- **Nhân sự:** Nghiên cứu sinh chính (phát triển mã, thực nghiệm), giáo sư hướng dẫn (hỗ trợ chuyên môn, đánh giá), có thể có chuyên gia dữ liệu/log (để đánh giá tính khả dụng của tập log) hoặc chuyên gia LLM (nếu cải tiến phức tạp). Cần cân nhắc thời gian và kinh nghiệm: nếu việc tích hợp LLM/RAG phức tạp, có thể xin hỗ trợ thêm từ cộng tác viên hoặc tìm tư vấn kỹ thuật.  

_Đặc biệt đánh giá:_ Thiết lập compute bottleneck (thời gian tính toán cho mỗi lần chạy LLM, chi phí API), chi phí gọi API (nếu dùng), dung lượng và chi phí lưu trữ (log có thể lớn), thời gian chạy mỗi thử nghiệm (nếu phải chạy nhiều lần). Giải pháp: sử dụng sample ban đầu để kiểm tra, lên kế hoạch chi phí và hạn mức API, parallel hóa pipeline nếu có thể, ưu tiên phiên bản tối ưu.  

## 4. Quản lý Rủi ro (Risk Management)

| Rủi ro | Xác suất | Tác động | Giảm thiểu | Dự phòng |
|---|---:|---:|---|---|
| **(Nghiên cứu)** Cải tiến không tạo ra hiệu quả rõ rệt | Cao | Cao | Xem lại thiết kế, tối ưu tham số, cân nhắc giảm độ phức tạp | Nếu thất bại: hạn chế giải pháp cải tiến (ví dụ bỏ module nhớ phức tạp), tập trung cải thiện phần đơn giản hơn trong cùng hướng |
| **(Nghiên cứu)** Không tái tạo được baseline như tham chiếu | Trung bình | Cao | Kiểm tra kỹ thuật, tinh chỉnh mã, chạy thử các bộ dữ liệu nhỏ | Chỉ giữ phần baseline đơn giản hơn (giảm quy mô đầu vào) để vẫn có thể tiến hành so sánh |
| **(Nghiên cứu)** Giả thuyết nghiên cứu không được hỗ trợ | Trung bình | Trung bình | Đánh giá lại kết quả, kiểm tra số liệu, thử nghiệm thay đổi | Giảm tập trung sang các kết quả có ý nghĩa, nhưng vẫn trong hướng cải tiến (ví dụ: đánh giá cải tiến trên metric phụ) |
| **(Dữ liệu)** Rò rỉ thông tin trong dữ liệu (data leakage) | Trung bình | Cao | Kiểm tra quy trình chia train/test, xáo trộn dữ liệu, xác thực chéo | Sử dụng tập dữ liệu thay thế hoặc giới hạn phân tích trên subset an toàn |
| **(Dữ liệu)** Thiếu nhãn hoặc nhãn mất cân bằng | Cao | Trung bình | Tăng cường dữ liệu (synthetic), kêu gọi thêm ghi nhãn, dùng kỹ thuật oversampling | Đổi metric không cần nhãn (score anomaly) hoặc phối hợp chuyên gia để hỗ trợ nhãn thủ công |
| **(Engineering)** Phức tạp khi tích hợp các module (dependency/version conflict) | Trung bình | Trung bình | Dùng container (Docker), quản lý dependency bằng Pipenv/Conda, test tích hợp sớm | Nếu gặp vấn đề lớn, chia nhỏ dự án: tập trung phát triển từng phần riêng lẻ, lùi phiên bản thư viện|
| **(Engineering)** Tài nguyên tính toán không đủ (GPU/CPU) | Cao | Cao | Lập kế hoạch sử dụng GPU (đám mây nếu cần), tối ưu mã, giảm độ lớn batch | Giảm quy mô thử nghiệm (dùng ít mẫu/trong thời gian ngắn hơn), chuyển sang dùng API cloud (OpenAI) nếu khả thi |
| **(Foundation Model)** Mô hình LLM không ổn định (phiên bản thay đổi) | Trung bình | Cao | Khóa phiên bản cụ thể, lưu local model nếu có, kiểm tra thường xuyên cập nhật | Giảm reliance vào model phức tạp (chuyển sang model nhỏ hơn/cũ hơn), thay thế bằng kỹ thuật khác phù hợp |
| **(Foundation Model)** Độ nhạy lệnh điều khiển (prompt sensitivity), hallucination | Cao | Trung bình | Thiết kế prompt cẩn thận, thêm bước kiểm tra đầu ra (post-processing), giới hạn phạm vi lệnh | Chuyển hướng tập trung vào metric khác (ví dụ hiệu suất chung thay vì dependent phản hồi), bỏ phần không đáng tin cậy của đầu ra |
| **(Foundation Model)** Chất lượng truy hồi thấp (retrieval poor) | Trung bình | Trung bình | Đánh giá chất lượng cơ sở dữ liệu tri thức, tối ưu tham số truy vấn | Sử dụng embedding thay thế hoặc rút gọn phạm vi kiến thức, chuyển sang nguồn tri thức khác |
| **(Foundation Model)** Latency/cost khi gọi API | Cao | Cao | Điều chỉnh tần suất gọi API, cache kết quả, theo dõi chi phí | Giảm độ lớn thử nghiệm, dùng token nhỏ hơn hoặc mô hình miễn phí tương đương |

## 5. Kế hoạch Viết luận văn (Thesis Writing Plan)

Kế hoạch viết luận văn theo bố cục chương đã nêu, đảm bảo lồng ghép kết quả nghiên cứu từ các kết quả đã có (mapping, phân tích, thiết kế, kết quả thí nghiệm). Mỗi chương gồm các mục tiêu cụ thể, dẫn nguồn (từ result-1..result-8), nội dung mong đợi, hình/bảng cần có và tiêu chí hoàn thành.

### Chương 1 — Giới thiệu  
- **Mục tiêu:** Giới thiệu vấn đề phát hiện sớm bất thường từ log, bối cảnh và động lực nghiên cứu; xác định câu hỏi nghiên cứu, mục tiêu, giả thuyết và đóng góp.  
- **Nguồn:** Sử dụng đề cương/đề xuất nghiên cứu (result-4.md) làm nền; kết hợp bối cảnh từ tổng quan các kết quả trước.  
- **Nội dung:** Trình bày tổng quan lĩnh vực, vấn đề cụ thể đã chọn, mục tiêu và câu hỏi nghiên cứu, phạm vi nghiên cứu (bao gồm các công nghệ Scope đã nêu). Đưa ra đóng góp chính (baseline đã chọn, limitation cần khắc phục, cải tiến đề xuất).  
- **Hình/bảng:** Có thể bao gồm sơ đồ tổng quan kiến trúc hệ thống đề xuất hoặc khung nghiên cứu. Bảng/tóm tắt các mục tiêu và đóng góp của luận văn.  
- **Tiêu chí hoàn thành:** Bao gồm đủ các phần (vấn đề, động lực, mục tiêu, RQ, đóng góp), làm rõ điểm mới, rõ ràng phạm vi nghiên cứu.

### Chương 2 — Tổng quan tài liệu (Literature Review)  
- **Mục tiêu:** Phân tích nền tảng nghiên cứu hiện có; xác định baseline 2025–2026 và xác nhận limitation.  
- **Nguồn:** Kết quả Systematic Mapping (result-1.md), Critical Analysis (result-2.md) và phần Research Opportunity (result-3.md) để trình bày tổng quan và chỉ ra khoảng trống. Kết hợp với proposal (result-4) để nhấn mạnh baseline và hạn chế.  
- **Nội dung:** Tóm tắt kết quả tổng quan hệ thống (mapping) và phân tích phê phán các nghiên cứu liên quan (cụ thể lĩnh vực LLM/log anomaly). Nêu rõ baseline đã chọn (công nghệ 2025–2026) và limitation đã xác nhận. So sánh các giải pháp liên quan và chỉ ra gap không mở rộng thêm.  
- **Hình/bảng:** Bảng tổng hợp các nghiên cứu chính, sơ đồ phân loại phương pháp log anomaly (theo result-1/result-2). Có thể có đồ thị tóm tắt số liệu mapping (năm, số công trình).  
- **Tiêu chí hoàn thành:** Bao gồm mapping, phân tích phê phán, nêu rõ baseline và hạn chế xác nhận; tổng kết rõ gap đã tìm ra (không thêm gap mới).

### Chương 3 — Phương pháp nghiên cứu (Research Methodology)  
- **Mục tiêu:** Mô tả chi tiết thiết kế nghiên cứu, bao gồm phương pháp, giả thuyết, baseline và cải tiến, giao thức thí nghiệm.  
- **Nguồn:** Nghiên cứu thiết kế (result-5.md), đề xuất (result-4.md).  
- **Nội dung:** Giải thích cách nghiên cứu được tiến hành: mô hình baseline (mô hình LLM cơ sở) và cải tiến (như RAG/memory-augmented), các giả thuyết cụ thể, phương pháp thực nghiệm so sánh. Mô tả quy trình thu thập và xử lý dữ liệu, đánh giá metric (bao gồm metric sớm phát hiện). Liệt kê giả thuyết và cách kiểm định chúng.  
- **Hình/bảng:** Sơ đồ luồng công việc nghiên cứu (flowchart), biểu đồ khối giải pháp. Bảng liệt kê giả thuyết và tương ứng mô hình kiểm định.  
- **Tiêu chí hoàn thành:** Phương pháp đầy đủ và rõ ràng; giải thích rõ baseline vs improvement; xác định được các giả thuyết và thiết kế thí nghiệm.

### Chương 4 — Thiết kế hệ thống và phần mềm (System and Software Design)  
- **Mục tiêu:** Trình bày kiến trúc hệ thống baseline và phần mở rộng cải tiến; chi tiết thiết kế kỹ thuật và thiết kế phần mềm.  
- **Nguồn:** Thiết kế kỹ thuật (result-6.md) và Thiết kế phần mềm (result-7.md).  
- **Nội dung:** Mô tả kiến trúc tổng thể của hệ thống phát hiện bất thường (bao gồm thu thập log, tiền xử lý, mô hình baseline, giao thức cải tiến). Trình bày chi tiết thành phần cải tiến (ví dụ module truy xuất tri thức, bộ nhớ ngoài). Giải thích luồng dữ liệu và tương tác giữa các module.  
- **Hình/bảng:** Sơ đồ kiến trúc (block diagram) của baseline và cải tiến; lưu đồ luồng xử lý; bảng thông số kỹ thuật (cấu hình mạng, tham số).  
- **Tiêu chí hoàn thành:** Cung cấp đủ chi tiết về thiết kế phần cứng/lập trình, minh họa rõ ràng quá trình baseline và cải tiến, dễ hiểu và logic.

### Chương 5 — Thí nghiệm và kết quả (Experiments and Results)  
- **Mục tiêu:** Trình bày kết quả thu được từ thí nghiệm, so sánh baseline và cải tiến, đánh giá sớm phát hiện, thực hiện ablation/robustness (nếu có) cùng phân tích thống kê và lỗi.  
- **Nguồn:** Giao thức thí nghiệm (result-8.md) và dữ liệu thí nghiệm từ các giai đoạn trước.  
- **Nội dung:** Báo cáo kết quả mô hình baseline (tái tạo kết quả tham chiếu), so sánh với cải tiến theo các metric định trước (độ chính xác, recall, F1, thời gian/phát hiện sớm). Phân tích tình huống phát hiện bất thường sớm hơn. Trình bày kết quả ablation hoặc robustness (nếu có). Thêm phần phân tích thống kê (test t hoặc ANOVA) và phân tích lỗi (ví dụ trường hợp sai phân loại).  
- **Hình/bảng:** Đồ thị so sánh hiệu suất (bar chart hoặc line chart), ROC/AUC nếu phù hợp, biểu đồ thời gian phát hiện; bảng thống kê kết quả; ví dụ log phân tích lỗi (nếu cần).  
- **Tiêu chí hoàn thành:** Thí nghiệm chính (baseline vs improved) được trình bày rõ ràng với số liệu đầy đủ, kèm phân tích ý nghĩa; trả lời được RQ liên quan đến hiệu quả cải tiến và sớm phát hiện.

### Chương 6 — Thảo luận, Kết luận và Hướng phát triển (Discussion, Conclusion and Future Work)  
- **Mục tiêu:** Đánh giá kết quả, trả lời các câu hỏi nghiên cứu, xác nhận hay bác bỏ giả thuyết, trình bày đóng góp, hạn chế và hướng nghiên cứu tiếp theo.  
- **Nguồn:** Tổng hợp mọi kết quả, kết luận từ các chương trước.  
- **Nội dung:** Tóm tắt lại kết quả đạt được đối với từng RQ và giả thuyết. Nêu rõ đóng góp khoa học (performance improvement), đóng góp phương pháp (tiếp cận kết hợp LLM+memory), đóng góp kỹ thuật (artifact tái lập) và đóng góp thực tiễn (ứng dụng cho hệ thống log). Thảo luận các hạn chế (ví dụ: dữ liệu, mô hình) và đề xuất hướng mở rộng trong tương lai (dựa trên limitations đã báo cáo).  
- **Hình/bảng:** Bảng tóm tắt đóng góp vs bằng chứng; bảng hạn chế và biện pháp giải quyết; bảng kế hoạch nghiên cứu tiếp theo.  
- **Tiêu chí hoàn thành:** Trả lời thỏa đáng mọi RQ/Giả thuyết; đóng góp rõ ràng, phù hợp; liệt kê giới hạn và gợi ý công việc tương lai cụ thể.  

_Bảng đóng góp và bằng chứng (Thesis Contribution Mapping):_

| Đóng góp | Bằng chứng | Thí nghiệm | Chương luận văn | Trạng thái |
|---|---|---|---|---|
| Tái tạo baseline | Kết quả experiment baseline | Thí nghiệm giai đoạn 2 | Chương 5 | Đang thực hiện |
| Bằng chứng về hạn chế | Phân tích hiệu suất baseline, phát hiện limitation | Thí nghiệm giai đoạn 2/3 | Chương 2 & 5 | Đang thực hiện |
| Cải tiến đề xuất | Kết quả so sánh baseline vs improvement | Thí nghiệm giai đoạn 4 | Chương 5 | Chưa thực hiện |
| Cải thiện phát hiện sớm | Metric phát hiện sớm (delay detection) | Thí nghiệm giai đoạn 4 | Chương 5 | Chưa thực hiện |
| Robustness/Hiệu năng | Phân tích ablation hoặc benchmark thời gian | Thí nghiệm giai đoạn 5 | Chương 5 | Tùy yêu cầu |
| Artifact tái lập | Bên lề: cấu trúc mã, docs hoàn chỉnh | Giai đoạn 7 (Artifact Freeze) | Chương 6 & Phụ lục | Đang thực hiện |

Các đóng góp đã xác định mang tính **khoa học** (đo lường cải thiện hiệu suất, phát hiện sớm hơn), **phương pháp** (kết hợp LLM + memory/retrieval), **kỹ thuật** (artifact có thể tái lập) và nếu có thể **thực tiễn** (áp dụng cho hệ thống log thực tế). Đóng góp tập trung vào cải tiến đã xác nhận, không phóng đại tính mới.

## 7. Kế hoạch Công bố (Publication Plan)

Lựa chọn hội nghị/tạp chí dựa trên quy mô đóng góp và phạm vi chuyên ngành. Hướng chiến lược:  trình bày rõ baseline hiện tại, hạn chế, cải tiến đề xuất và bằng chứng thực nghiệm.

| Venue (Hội nghị/Tạp chí) | Phù hợp (Fit) | Cần bằng chứng | Điểm mạnh | Rủi ro | Ưu tiên |
|---|---:|---|---|---|---|
| **KDD/ICDM 2026** (Hội thảo khai thác dữ liệu) | Rất cao (dữ liệu/log anomaly) | Kết quả thực nghiệm mạnh, phân tích sớm phát hiện | Cộng đồng data mining quan tâm anomaly detection, đánh giá cao số liệu | Cạnh tranh cao, cần làm nổi bật sự khác biệt | Cao |
| **AAAI 2026** (Hội nghị AI hàng đầu) | Cao (sử dụng LLM/AI) | Bằng chứng cải thiện rõ, giải thích kỹ thuật mới kết hợp | Uy tín quốc tế, cộng đồng AI lớn | Yêu cầu cao về tính mới, mô hình là cải tiến (not novel method) | Trung bình |
| **TKDE (IEEE)** (Data engineering) | Trung bình cao (xử lý log và dữ liệu lớn) | Số liệu chi tiết, mở rộng ứng dụng | Tạp chí uy tín, review kỹ lưỡng | Chu kỳ bài báo lâu, đòi hỏi rigor cao | Trung bình |
| **TNNLS (IEEE)** (Neural Networks & Learning Sys) | Cao (hướng LLM) | Cần phân tích học sâu và so sánh | Xu hướng LLM, cơ hội được chú ý | Đòi hỏi thực nghiệm sâu, cải tiến phải rõ nét | Cao |
| **ICLR/NeurIPS Workshop** (AI conferences) | Trung bình (learning) | Thử nghiệm sơ bộ để lấy phản hồi | Cộng đồng ML cập nhật, workshop dễ chấp nhận | Các hội thảo workshop chỉ nhìn feedback, không main track | Thấp |

_Chú ý:_ Chiến lược bài báo dựa trên bằng chứng thực nghiệm: mô tả baseline và limitation đã được chứng minh, sau đó trình bày cải tiến và so sánh đối chứng. Không tự nhận “phương pháp hoàn toàn mới” nếu chỉ là mở rộng/cải tiến trên cơ sở đã tồn tại.

## 8. Gói Artifact (Artifact Package)

Thiết kế gói artifact tối thiểu như sau (cây thư mục ví dụ):

```
artifact/
├── README.md
├── configs/
├── data_reference/
├── baseline/
├── improvement/
├── prompts/         
├── scripts/
├── experiments/
├── results/
├── figures/
├── logs/
├── tests/
├── docs/
└── reproducibility.md
```

Trong đó:  
- **README.md:** Giải thích cấu trúc, cách cài đặt và sử dụng artifact.  
- **configs/**: Cấu hình thí nghiệm (hyperparameters, đường dẫn dữ liệu, tên mô hình) cho cả baseline và cải tiến.  
- **data_reference/**: Hướng dẫn thu thập hoặc đường dẫn đến dữ liệu (nếu không cho phép chia sẻ công khai, cung cấp script tải hoặc mô tả nguồn dữ liệu).  
- **baseline/** và **improvement/**: Mã nguồn thực thi cho mô hình baseline và cải tiến tương ứng.  
- **prompts/** (nếu có): Các prompt đã dùng cho LLM.  
- **scripts/**: Các script chạy thí nghiệm (chuẩn hóa đầu vào, thu thập kết quả).  
- **experiments/**: Giao diện thực thi từng thí nghiệm cụ thể (log chạy, file cấu hình).  
- **results/**: Kết quả đầu ra đã xử lý (CSV/JSON chứa metric), sẵn sàng tạo báo cáo.  
- **figures/**: Mã hoặc file gốc vẽ các biểu đồ/tables trình bày kết quả.  
- **logs/**: Tập tin ghi chép (log files) từ lần chạy thử nghiệm, để kiểm tra.  
- **tests/**: Các kiểm thử đơn vị (unit tests) hoặc kiểm thử tích hợp (nếu có) đảm bảo mã chạy đúng.  
- **docs/**: Tài liệu phụ trợ, ví dụ giải thích thuật toán, kiến trúc hệ thống.  
- **reproducibility.md:** Hướng dẫn chi tiết để tái lập toàn bộ kết quả (môi trường, bước chạy, data, seed).

Artifact phải hỗ trợ toàn bộ quy trình nghiên cứu: tái tạo baseline, chạy cải tiến, thực hiện so sánh chính, các ablation (nếu được yêu cầu), và sinh kết quả cuối (figures/tables). Nếu dữ liệu không cho phép chia sẻ thẳng, cần hướng dẫn rõ cách thu thập hoặc truy cập (ví dụ link tải).  

Kiểm tra nội dung artifact:  
- Xác định phiên bản và nguồn dữ liệu (file data_reference).  
- Mã nguồn có commit hash hoặc tag cụ thể.  
- Các cấu hình baseline/improvement, seed random, môi trường (có thể ở reproducibility.md).  
- Mỗi kết quả đã được lưu ở thư mục results, figures.  
- Xác minh rằng các bước thử nghiệm (scripts/experiments) chạy từ đầu đến cuối có thể sinh ra kết quả gốc.  

_Trạng thái:_  
- **Đã tái tạo baseline:** (Chưa) cần hoàn thành.  
- **So sánh baseline vs cải tiến:** (Chưa) sắp tới.  
- **Đánh giá sớm phát hiện:** (Chưa) cần triển khai.  
- **Thí nghiệm bổ trợ/ablation:** (Tùy thuộc vào thiết kế).  
- **Phân tích thống kê & lỗi:** (Chưa) thực hiện sau khi có dữ liệu.  
- **Artifact đóng băng:** (Chưa) sẽ thực hiện ở cuối; nếu thiếu mục, bổ sung.  

_Dự thảo checklist:_  
- Tất cả RQs được trả lời, mục tiêu đạt được.  
- Tất cả giả thuyết được kiểm định.  
- Hạn chế xác nhận đã được minh chứng trong kết quả.  
- Cải tiến đã được đánh giá đầy đủ.  
- Các đóng góp và hạn chế được mô tả rõ ràng.  
- Mọi phần mềm/dữ liệu/phiên bản được ghi nhận để tái lập hoàn toàn.  

**Quan trọng:** Đảm bảo bằng chứng giữa baseline gốc và cải tiến đủ mạnh để bảo vệ trước đánh giá. Phải có kết quả so sánh công bằng (giữ nguyên cài đặt baseline gốc, chỉ thay đổi phần cải tiến).  

## 9. Checklist Đảm bảo Tái lập (Reproducibility Checklist)

- **Môi trường chi tiết:** Ghi chép OS, ngôn ngữ, thư viện và phiên bản (hoặc Dockerfile). Đảm bảo mô tả cách cài đặt toàn bộ; chia sẻ kho mã nguồn công khai.  
- **Dữ liệu và phiên bản:** Cung cấp đường dẫn hoặc hướng dẫn tải dữ liệu (phiên bản cụ thể). Phân chia tập train/test rõ ràng. Nếu dữ liệu nhạy cảm, đưa code preprocessing.  
- **Cấu hình thí nghiệm:** Lưu trữ file config (học suất, epochs, batch, seed, các tham số quan trọng). Mỗi thí nghiệm gắn ID duy nhất.  
- **Mô hình và công cụ:** Định danh mô hình (phiên bản LLM, embedding, retrieval). Nếu dùng API, lưu log chi phí và phiên bản API.  
- **Scripts và tài liệu:** Cung cấp script chạy toàn bộ pipeline, bao gồm tiền xử lý, training, đánh giá. Viết hướng dẫn reproducibility.md bước 1–n.  
- **Kết quả thô và xử lý:** Cung cấp dữ liệu kết quả chưa xử lý và các tập dữ liệu đầu ra (metrics) dễ truy cập. Đảm bảo có đủ dữ liệu để tái tạo các bảng/biểu đồ trong luận văn.  
- **Lưu giữ ngẫu nhiên:** Đặt seed cố định ở những bước ngẫu nhiên; ghi seed trong config.  
- **Bằng chứng kèm theo:** Nếu có thuật toán tùy chỉnh (prompt, logic), để trong mục prompts/ và giải thích cách sử dụng.  
- **Đóng góp minh bạch:** Chú giải rõ ràng nguồn gốc và ý nghĩa của kết quả, theo hướng dẫn artifact evaluation (minh bạch provenance giúp tăng khả năng tái lập).  

## 10. Checklist Hoàn thành Thí nghiệm (Experiment Completion Checklist)

- **Baseline và cải tiến:** Đã chạy baseline lặp lại đủ lần, ghi nhận kết quả (metrics + logs). Đã chạy cải tiến lặp lại đủ lần.  
- **So sánh chính:** Đã tổng hợp và so sánh metric baseline vs improved (bảng, biểu đồ).  
- **Phát hiện sớm:** Tính toán và so sánh metric “delay to detect” hoặc tương đương (thời gian/mức độ sớm hơn phát hiện).  
- **Ablation/Robustness (nếu có):** Đã thực hiện các thí nghiệm bổ trợ định nghĩa trong result-8 (ví dụ: loại bỏ module, thay đổi tham số) và ghi nhận kết quả.  
- **Thống kê:** Thực hiện phân tích thống kê (p-value, CI) cho kết quả chính để đánh giá độ tin cậy.  
- **Phân tích lỗi:** Thực hiện phân tích ví dụ mẫu (nếu cần) để giải thích các trường hợp sai hoặc giới hạn.  
- **Tối ưu hóa:** Nếu cần đánh giá hiệu năng (latency, memory) của mô hình cải tiến, đã thu thập số liệu này.  
- **Ghi nhận:** Đảm bảo mọi kết quả trung gian và tập dữ liệu liên quan đã được lưu trữ trong artifact.

## 11. Checklist Sẵn sàng Luận văn (Thesis Readiness Checklist)

- **Trả lời RQs:** Tất cả các câu hỏi nghiên cứu (RQ) đã có câu trả lời rõ ràng dựa vào kết quả.  
- **Giả thuyết:** Mỗi giả thuyết đã được kiểm định và kết quả (chấp nhận/ bác bỏ) được trình bày.  
- **Mục tiêu đạt được:** Kiểm tra mục tiêu nghiên cứu, đảm bảo tất cả mục tiêu chính đã hoàn thành.  
- **Hạn chế:** Hạn chế được xác nhận đã được chứng minh trong các kết quả; các yếu tố ảnh hưởng đã thảo luận.  
- **Cải tiến:** Cải tiến đề xuất đã được đánh giá đầy đủ; hiệu quả so sánh rõ ràng.  
- **Đóng góp:** Đóng góp của luận văn đã được làm nổi bật, có bằng chứng (dựa trên bảng trên).  
- **Hạn chế và Validity:** Các hạn chế của nghiên cứu và nguy cơ (threats to validity) đã được liệt kê và bình luận.  
- **Artifact:** Artifact sẵn sàng chia sẻ (nếu công khai), hoặc đủ tài liệu hướng dẫn reproducible.  
- **Kết luận:** Luận văn có phần kết luận và hướng phát triển rõ ràng.

## 12. Checklist Sẵn sàng Công bố (Publication Readiness Checklist)

- **Bằng chứng thực nghiệm:** Bài báo cần tập trung vào bằng chứng từ thí nghiệm, đã chuẩn bị các bảng/số liệu chính minh hoạ kết quả.  
- **Tính mới phù hợp:** Không tuyên bố phương pháp hoàn toàn mới nếu chỉ là cải tiến, mà tập trung vào sự hiệu quả của cải tiến.  
- **Chất lượng thử nghiệm:** Đảm bảo thí nghiệm có tính lặp lại, đủ lượng mẫu, đầy đủ kiểm định thống kê.  
- **Viết bài:** Có bản thảo bài báo (hoặc outline) được chuẩn bị dựa trên luận văn (có thể tóm tắt chương 3–5).  
- **Artifact:** Chuẩn bị nội dung bổ sung cho bài báo (phụ lục artifact) nếu hội đồng yêu cầu; đảm bảo tham chiếu minh bạch.  
- **Địa điểm công bố:** Venue phù hợp đã chọn, nhấn mạnh đóng góp thực nghiệm; kiểm tra format và yêu cầu nộp bài.  

## 13. Kế hoạch Cuối (6–9 tháng)

| Kỳ (M) | Mục tiêu chính | Kết quả then chốt | Cổng quyết định |
|---|---|---|---|
| **M1** | Thiết lập baseline ban đầu | Baseline code chạy được | Baseline chạy (Go/No-Go) |
| **M2** | Xác thực baseline | Kết quả tham chiếu | Baseline khớp tham chiếu |
| **M3** | Triển khai cải tiến | Hệ thống tích hợp (baseline+improvement) | Cải tiến chạy ổn định |
| **M4** | Thí nghiệm chính | Bảng kết quả chính | Kết quả main experiments |
| **M5** | Ablation/Robustness | Bằng chứng hỗ trợ | Các thử nghiệm phụ hoàn thành |
| **M6** | Phân tích cuối cùng | Kết quả phân tích hoàn chỉnh | Dữ liệu và đồ thị ổn định |
| **M7–M8** | Viết luận văn | Bản nháp đầy đủ (chương 1–5) | Bản thảo sẵn sàng rà soát |
| **M9** | Hoàn thiện & công bố | Luận văn cuối, artifact, bản thảo báo | Sẵn sàng nộp (Submit) |

_Điều chỉnh thời gian nếu cần dựa theo thực tế luận văn (6–9 tháng)._ 

## 14. Quyết định Cuối cùng (Final Decision)

**Ưu tiên thực hiện luận văn:**  
1. Tái tạo baseline hiện tại.  
2. Triển khai và đánh giá cải tiến.  
3. Thí nghiệm chính (so sánh baseline vs cải tiến).  
4. Đánh giá “phát hiện sớm” (early detection).  
5. Thí nghiệm hỗ trợ (ablation/robustness, nếu có).  
6. Phân tích cuối cùng (thống kê, lỗi).  
7. Viết luận văn (chương 1–6).  
8. Chuẩn bị artifact và công bố.

**Tiêu chí Go/No-Go (cổng quyết định):**  
- *Baseline:* Đã tái tạo thành công kết quả baseline được tham chiếu. Nếu không, cần điều chỉnh lại baseline trong phạm vi bài (không đổi đề tài).  
- *Cải tiến:* Có thể cài đặt mô hình cải tiến đúng theo thiết kế. Nếu không, giảm quy mô cải tiến nhưng vẫn cùng hướng (ví dụ bỏ thành phần phức tạp).  
- *Thí nghiệm:* Thiết kế thí nghiệm phải có khả năng kiểm chứng giả thuyết; dữ liệu và công cụ đủ.  
- *Tài nguyên:* Computation và thời gian phải khả thi; nếu không, điều chỉnh quy mô (thí nghiệm ít mẫu hơn, hoặc dùng API thay vì đào tạo mới).  
- *Artifact:* Artifact phải tái lập được; nếu gặp vấn đề, tập trung sửa lỗi môi trường/phụ thuộc (không chuyển đề tài).  

Nếu một cổng (gate) bị đánh giá là không đạt, giải pháp dự phòng là **giảm bớt phạm vi trong cùng hướng cải tiến**, ví dụ đơn giản hóa thành phần hoặc giảm kích thước thử nghiệm, nhưng không thay đổi đề tài cơ bản.  

Tóm lại, việc thực hiện luận văn sẽ ưu tiên tập trung vào đóng góp rõ ràng, có thể kiểm chứng và tái lập, theo đúng lộ trình từ baseline → limitation đã xác nhận → cải tiến → kết quả thực nghiệm. Con đường nghiên cứu này bảo đảm luận văn và bài báo dựa trên bằng chứng vững chắc.  

**Nguồn tham khảo:** Việc ghi lại chi tiết môi trường và artifact giúp tăng khả năng tái lập kết quả.