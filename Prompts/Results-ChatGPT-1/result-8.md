# Kế hoạch Triển khai Thực nghiệm

## 1. Mục tiêu Thực nghiệm và Độ truy vết  
Xác định rõ mỗi câu hỏi nghiên cứu (RQ1, RQ2, RQ3) và giả thuyết (H1, H2, H3) sẽ được kiểm chứng bằng thí nghiệm nào, dùng thước đo chính nào và kỳ vọng kết quả ra sao. Ví dụ:  
| Yếu tố nghiên cứu    | Thí nghiệm       | Thước đo chính        | Bằng chứng mong đợi                                 |
|---------------------|----------------|----------------------|---------------------------------------------------|
| **RQ1**             | E2 (So sánh)   | [F1/Precision/Recall]*| Cải thiện so với baseline gốc trên thước đo chính. |
| **RQ2**             | E3 (Phát hiện sớm) | [TTD/LeadTime/Độ nhạy]*| Tín hiệu phát hiện sớm hơn hoặc độ nhạy tăng.      |
| **RQ3**             | E5 (Độ cứng)   | [AUC/độ ổn định]*      | Kết quả không suy giảm trước nhiễu/mất dữ liệu.    |
| **H1**             | E2            | [F1/Precision]*      | Sự cải tiến tạo mức tăng đáng kể về hiệu năng.     |
| **H2**             | E3            | [LeadTime/Tỉ lệ sớm]*| Phát hiện sự cố càng sớm càng tốt (Lead Time cải thiện). |
| **H3**             | E4 (Ablation)  | [F1/Metric]*         | Nếu bỏ đi thành phần mới, hiệu năng giảm.          |

\* Các thước đo cụ thể (Ví dụ: F1, Precision, Recall, Time-to-Detection, v.v.) được xác định dựa trên ngữ cảnh của đề tài từ kết quả thiết kế (result-7.md). Bằng chứng mong đợi định rõ sự gia tăng hoặc duy trì hiệu năng nhờ cải tiến.

## 2. Môi trường Thực nghiệm  
- **Phần cứng:** Ví dụ, máy chủ dùng CPU Intel Xeon (8 nhân) 3.0GHz, RAM 64GB, GPU Nvidia V100 (16GB) hoặc tương đương. Ổ cứng SSD ≥1TB. (Cấu hình này cho phép thực nghiệm không gặp giới hạn tài nguyên.)  
- **Phần mềm:** Hệ điều hành Ubuntu 20.04 LTS hoặc tương đương. Python 3.8/3.9. Thư viện học máy: PyTorch 1.10 hoặc TensorFlow 2.8, CUDA 11.x, cuDNN tương ứng. Mô-đun/Gói hỗ trợ: e.g. scikit-learn 1.x, transformers 4.x (nếu dùng LLM). Nếu sử dụng LLM định sẵn (OpenAI GPT-3.5/GPT-4), ghi rõ phiên bản API được gọi. Đối với thành phần truy vấn (retrieval) hoặc cơ sở dữ liệu, ghi rõ phiên bản (ví dụ Elasticsearch 7.x). Môi trường container hóa (Docker/VM) được khuyến khích để đảm bảo khả năng tái lập.  
- **Theo dõi thực nghiệm:** Sử dụng công cụ như Weights & Biases hoặc MLflow để ghi lại tham số (seed, hyperparameters), log kết quả, đồ thị học. Điều này giúp tái lập lại quy trình dễ dàng.

 Các thông tin phần cứng/phần mềm và tài nguyên tính toán (GPU, thời gian huấn luyện, v.v.) đều được ghi nhận chi tiết. Ví dụ, báo cáo loại GPU, tốc độ CPU, dung lượng bộ nhớ, và thời gian chạy mỗi lược thực nghiệm. Chuẩn bị môi trường sạch (clean environment) hoặc container đảm bảo kết quả không bị ảnh hưởng bởi sự khác biệt cấu hình.

## 3. Quy trình Bộ Dữ liệu  
Chia bộ dữ liệu thành các tập huấn luyện, xác thực, kiểm thử (và bên ngoài nếu khả thi) với quy tắc phân tách theo thời gian. Cụ thể:  
- **Huấn luyện:** Dữ liệu lịch sử (logs cũ) được dùng để huấn luyện hoặc fine-tune mô hình/baseline. Quy mô đủ lớn để học đặc trưng.  
- **Xác thực (validation):** Một phần dữ liệu tiếp theo (ví dụ tách theo ngày/tháng) dùng để tinh chỉnh tham số (như ngưỡng, hyperparameters).  
- **Kiểm thử (test):** Phần cuối cùng theo thời gian chưa từng xuất hiện trong huấn luyện/xác thực, dùng để đánh giá cuối cùng.  
- **Ngoài/khác hệ thống:** Nếu có, dùng tập dữ liệu độc lập khác hệ thống hay nguồn để kiểm tra tính khái quát, nếu được phép.  

Với mỗi tập, ghi rõ: nguồn dữ liệu (ví dụ logs từ [tên hệ thống/nơi thu thập]), quy mô (số phiên log, tổng số bản ghi), loại sự kiện (ghi chú nếu log lỗi, nhật ký hoạt động, v.v.), đặc tính thời gian (phạm vi ngày/tháng/năm), mục đích (huấn luyện/đánh giá). Chiến lược phân chia: cắt theo mốc thời gian sao cho mọi sự kiện trong tập kiểm thử xảy ra sau dữ liệu huấn luyện để tránh rò rỉ thông tin tương lai. Tất cả splits (train/val/test) phải được ghi đích xác (ví dụ: dùng 70% giai đoạn đầu huấn luyện, 10% sau đó kiểm thử/hyper-tuning, 20% cuối kiểm thử). Nếu bộ dữ liệu không hỗ trợ đánh giá thực sự cho *phát hiện sớm* (Early Detection), cần nêu rõ (ví dụ nếu không biết mốc xảy ra failure).

 Ghi lại chi tiết chia dữ liệu và các tham số, hyperparameter. Điều này giúp đảm bảo tính minh bạch và cho phép người khác tái lập kết quả.

## 4. Baseline và So sánh Công bằng  
- **Baseline chính:** Là phương pháp baseline 2025–2026 đã chọn từ result-4/result-5. Ghi rõ tên/bản/tham số model baseline, các bước tiền xử lý dữ liệu (log preprocessing, embedding), cấu hình threshold, tham số truy vấn (nếu có retrieval). Ví dụ: “Baseline dùng Mô hình X phiên bản 1.2, threshold p=0.5, dùng encoder Y…, báo cáo F1=0.75 theo tài liệu gốc.” Đưa cả kết quả báo cáo và kết quả tái tạo khi chạy lại.  
- **So sánh điều khiển:** Thiết lập hai biến thể: (A) Baseline gốc, (B) Baseline + Cải tiến nhắm mục tiêu. Giữ nguyên tối đa: dữ liệu và split, tiền xử lý, kiến trúc chính, ngưỡng đánh giá, môi trường phần cứng/phần mềm, quy trình đánh giá. Chỉ thêm component cải tiến vào (B). Nếu phải thay đổi khác (ví dụ threshold sau huấn luyện lại), giải thích rõ lý do và xem xét ảnh hưởng. Không thêm baseline phụ trội trừ khi yêu cầu hoặc để so sánh bối cảnh.

Ví dụ: Nếu cải tiến là một thuật toán mới thêm vào pipeline, thì Baseline và Baseline+Improvement đều dùng cùng code gốc, chỉ thêm module mới ở biến thể B. Mọi phép đo đều song song giữa A và B để đảm bảo công bằng. 

## 5. Kịch bản Thí nghiệm  
Mô hình hoá các kịch bản chính sau:  
- **E1 – Baseline Reproduction:** Chạy lại phương pháp baseline đã công bố để xác nhận pipeline đúng và tạo kết quả tham chiếu (report vs reproduced).  
- **E2 – Main Improvement Test:** So sánh trực tiếp Baseline (A) và Baseline+Improvement (B) trên tập kiểm thử tiêu chuẩn. Đây là thí nghiệm chính xác minh H1 về cải thiện hiệu năng (e.g., tăng F1).  
- **E3 – Early Detection Test:** Đánh giá thời gian phát hiện sớm trên cả hai biến thể. Tính Lead Time, Detection Before Failure, False Alarm Rate. Mục tiêu kiểm chứng H2 về cải thiện phát hiện trước sự cố (ví dụ thời gian chờ giảm).  
- **E4 – Ablation Study:** Nếu cải tiến có nhiều thành phần, loại bỏ một phần (partial improvement) và so sánh lại để kiểm tra đóng góp cụ thể. Ví dụ: Baseline + (Improvement minus feature X). Xác định rõ thành phần nào mang lại lợi ích.  
- **E5 – Robustness Test:** Tạo điều kiện nhiễu liên quan đến limitation đã xác định (ví dụ bỏ sót event, thêm noise, thay đổi pattern) để kiểm tra độ ổn định. So sánh A và B dưới perturbation để xem cải tiến có giúp tăng độ cứng hay không.  
- **E6 – Hiệu quả (Efficiency):** Nếu cải tiến có ảnh hưởng đến chi phí (tính toán hay độ trễ), đo thêm độ trễ phản hồi, thời gian xử lý, số token (nếu dùng LLM) giữa A và B.  
- **E7 – Độ khái quát (Generalization):** Nếu khả thi và trong phạm vi đề tài, thử nghiệm trên dataset hay hệ thống khác (cross-dataset) để xem cải tiến có hiệu quả ngoài điều kiện gốc.

## 6. Các Thước đo Đánh giá  
- **Phát hiện (Detection):** Độ chính xác (Precision), Độ hồi đáp (Recall), F1, PR-AUC, ROC-AUC (nếu áp dụng). Những metric này đánh giá tổng quan độ đúng/sai của phương pháp.  
- **Phát hiện sớm (Early Detection):** Ưu tiên các thước đo thời gian: Time-to-Detection (trung bình thời gian phát hiện sau khi sự cố thực sự xảy ra), Detection Lead Time (khoảng cách phát hiện trước khi sự cố xác nhận), Tỷ lệ cảnh báo sớm (Early Warning Rate), Tỷ lệ phát hiện trước failure, Tỷ lệ báo động giả (False Alarm Rate). *Lưu ý:* Không dùng F1 như bằng chứng duy nhất cho mục tiêu phát hiện sớm; cần riêng biệt đánh giá mặt thời gian.  
- **Hiệu quả:** Nếu cần, đo độ trễ trung bình cho mỗi truy vấn (latency), throughput, chi phí tính toán (token count hoặc tài nguyên GPU), và bộ nhớ sử dụng.  
- **Thành phần (nếu phục vụ giả thuyết):** Ví dụ, nếu cải tiến gồm module retrieval, đo Recall@k, Precision@k, MRR; nếu dùng LLM, ghi tỷ lệ hallucinaton, độ nhất quán suy luận, chất lượng giải thích.

## 7. Phân tích Thống kê  
- Chạy lặp nhiều lần (nhiều run với random seed khác nhau) để ước lượng phương sai. Lưu seed, ghi lại sai số chuẩn (standard error) hoặc khoảng tin cậy cho mỗi metric. Báo cáo thanh sai số hoặc khoảng tin cậy nhằm thể hiện biến thiên.  
- Tính kiểm định thống kê (ví dụ paired t-test hoặc Wilcoxon test nếu cần) để xác định sự khác biệt giữa A và B có ý nghĩa hay không. Phương pháp kiểm định tùy tính chất dữ liệu (paired với cùng bộ test, unpaired nếu độc lập). Áp dụng hiệu chỉnh đa so sánh (như Bonferroni) nếu đánh giá nhiều chỉ số.  
- Tính độ lớn hiệu ứng (effect size) cho các so sánh chính để đánh giá mức độ khác biệt.  
- Chắc chắn *khóa phiên bản* model (fix model version) và kiểm soát yếu tố ngẫu nhiên (random seed, nhiệt độ của LLM nếu có) mỗi khi lặp. Ghi rõ các biến số này trong báo cáo.  

 Báo cáo các khoảng tin cậy và kiểm định thống kê cho các thí nghiệm chính; không chỉ cung cấp giá trị trung bình mà phải thể hiện biến động kết quả.

## 8. Tiêu chí Thành công  
- **Tiêu chí chính:** Chọn metric trực tiếp phản ánh limitation đã xác nhận (ví dụ F1, Lead Time, AUC). Cải tiến được coi là thành công nếu có sự cải thiện rõ rệt và có ý nghĩa thống kê trên metric này, đồng thời không gây các tác động tiêu cực quá mức.  
- **Tiêu chí phụ:** Bao gồm phát hiện sớm (time-to-detection), độ bền (robustness), chi phí (latency, compute), khả năng khái quát (generalization).  
- **Quy tắc đánh đổi:** Nếu cải tiến tăng metric chính nhưng đổi lại tăng đáng kể độ trễ, chi phí, hoặc tăng tỷ lệ báo động giả, thì cần đánh giá lại. Ví dụ, không coi một cải tiến là tốt hơn chỉ vì F1 tăng mà bỏ qua chi phí tăng gấp đôi. Các tiêu chí được xác định rõ dựa vào giới hạn trong result-5/md thiết kế; nếu chưa có ngưỡng định trước, cần ghi rõ yêu cầu kiểm chứng trong thực nghiệm. 

## 9. Quy trình Ablation  
Nếu cải tiến gồm nhiều thành phần: Thiết kế thí nghiệm với các nhánh:  
- **Baseline:** không có cải tiến.  
- **Baseline + Cải tiến đầy đủ:** toàn bộ thành phần mới.  
- **Baseline + Cải tiến phần:** từng thành phần trong cải tiến bị loại bỏ hoặc thay thế.  

Mục tiêu: chứng minh lợi ích (gain) chủ yếu đến từ cải tiến mục tiêu. So sánh hiệu năng khi thiếu từng phần của cải tiến sẽ cho biết thành phần nào quan trọng.

## 10. Phân tích Lỗi (Error Analysis)  
Phân loại và khảo sát các lỗi sau:  
- **False Positive (FP):** TH dự đoán có lỗi nhưng thực tế không có, nguyên nhân có thể do threshold quá thấp, hallucinaton.  
- **False Negative (FN):** TH bỏ sót lỗi thực sự, do mô hình thiếu sensitivity hoặc lỗi trong retrieval.  
- **Thiếu phát hiện sớm:** Ca mà cải tiến chưa phát hiện trước thời điểm xác nhận, hoặc không sớm hơn baseline.  
- **Thất bại Retrieval/Context:** Ví dụ chưa truy vấn được ngữ cảnh hỗ trợ, dữ liệu gốc chưa đủ thông tin.  
- **Thất bại Reasoning:** Nếu dùng LLM, lỗi do suy luận/logic sai, hiểu sai ngữ cảnh.  
- **Hallucination:** LLM sinh thông tin không chính xác liên quan đến sự cố.  
- **Thiếu hụt tri thức:** Kiến thức LLM hạn chế, không bao phủ tình huống.  

Với mỗi loại lỗi: ghi điều kiện xảy ra (trạng thái log, ngữ cảnh), nguyên nhân gốc rễ, ảnh hưởng đến giả thuyết (H1-H3) và liệu lỗi có giảm được nhờ cải tiến hay không. Tránh xem đây như một phương pháp mới, mà coi là khảo sát chất lượng kết quả.

## 11. Phân tích Độ cứng (Robustness)  
Thử nghiệm các tình huống nhiễu liên quan đến limitation được xác định, ví dụ:  
- Thêm/bớt noise trong log (log không đầy đủ, lỗi ghi log).  
- Mẫu dữ liệu chưa từng thấy (patterns mới).  
- Trái tim/Thời gian dịch chuyển (nếu logs mới, drift theo time).  
- Sai lệch trong retrieval (kết quả truy vấn chứa ngữ cảnh sai).  

Đánh giá xem cải tiến giữ vững hiệu năng như thế nào khi gặp các perturbation này so với baseline. Mục tiêu: chứng minh cải tiến không chỉ hiệu quả trong điều kiện gốc mà còn cứng cáp hơn khi giới hạn bị lộ.

## 12. Phân tích Hiệu quả và Chi phí  
Nếu cải tiến liên quan đến mô hình lớn (LLM), truy vấn nhiều, agent, v.v., đo:  
- Độ trễ xử lý trung bình (latency) và throughput (phút/phiên).  
- Số token gởi/gọi (token cost) nếu dùng LLM API (như GPT-4).  
- Thời gian truy vấn (retrieval time) và số lần gọi mô hình (model calls).  
- Sử dụng bộ nhớ GPU, CPU.  
- Tính toán chi phí ước lượng (chi phí GPU-hours hoặc tiền, nếu dùng dịch vụ).  

Đảm bảo ghi lại để so sánh chi phí giữa baseline và cải tiến. Nếu cải tiến đưa vào, chắc chắn cân nhắc trade-off giữa hiệu năng và chi phí.

## 13. Quy trình Tính tái lập (Reproducibility)  
- **Phiên bản và seed:** Lưu hẳn seed ngẫu nhiên sử dụng, cả trong huấn luyện và các bước liên quan. Ghi rõ từng seed cho từng thí nghiệm.  
- **Dữ liệu và splits:** Định nghĩa và lưu vĩnh viễn ngay (snapshot) bộ dữ liệu đã dùng (bao gồm mã hash/timestamp nếu có). Lưu lại tỷ lệ chia.  
- **Mô hình và cấu hình:** Định danh rõ version của code baseline và cải tiến (ví dụ commit hash Git), phiên bản model/provider (ví dụ GPT-3.5-turbo, phiên bản vNN, hoặc code LLM tự huấn luyện). Ghi lại mọi hyperparameter (learning rate, threshold, số vòng lặp, v.v.).  
- **Môi trường:** Lưu chi tiết hệ điều hành, phiên bản Python, phiên bản CUDA, thư viện (requirements.txt hoặc Dockerfile). Cung cấp container/VM nếu khả thi để tái dựng môi trường ban đầu.  
- **Cấu hình truy vấn (nếu RAG/Retrieve):** Lưu model truy vấn, kích thước retrieval (k), kho tri thức, đường dẫn chỉ mục, v.v.  
- **Kết quả:** Lưu bản ghi (logs) thô và kết quả xử lý (metrics) cho mỗi run. Đảm bảo dữ liệu raw không thay đổi.  

Tất cả yếu tố trên cần được đóng gói cùng hướng dẫn cài đặt rõ ràng. Hướng dẫn cần nêu chính xác lệnh và môi trường để chạy lại kết quả. Theo khuyến cáo, mỗi thí nghiệm được nhận diện bởi tuple (code-hash, data-hash, config-hash, env-hash) để đảm bảo có thể tái lập.

## 14. Ma trận Thí nghiệm  

| Thí nghiệm | Baseline (A) | Improvement (B) | Mục tiêu chính       |
| ---------- | ------------ | --------------- | -------------------- |
| **E1**     | ✓            |                 | Phục hồi Baseline (reproduction) |
| **E2**     | ✓            | ✓               | Kiểm thử cải tiến chính |
| **E3**     | ✓            | ✓               | Đánh giá phát hiện sớm |
| **E4**     | ✓            | ✓/partial       | Kiểm chứng đóng góp của cải tiến (Ablation) |
| **E5**     | ✓            | ✓               | Kiểm tra độ cứng (Robustness) |
| **E6**     | ✓            | ✓               | Đánh giá hiệu quả, chi phí |
| **E7**     | ✓            | ✓               | Đánh giá khái quát (Generalization) |

## 15. Mẫu Báo cáo Kết quả  
1. **Tái hiện Baseline:** So sánh kết quả baseline tái tạo với báo cáo ban đầu.  
2. **So sánh chính (Main Comparison):** Thống kê kết quả A vs B về F1, Precision, v.v. Kèm ý nghĩa thống kê.  
3. **Phát hiện sớm:** Kết quả các thước đo sớm (lead time, tỷ lệ cảnh báo trước).  
4. **Ablation:** Trình bày kết quả khi bỏ từng phần cải tiến, để chứng minh đóng góp riêng.  
5. **Độ cứng:** Kết quả khi thêm nhiễu, so sánh A và B.  
6. **Hiệu quả/Chi phí:** Bảng so sánh độ trễ, throughput, token cost, v.v.  
7. **Bằng chứng thống kê:** Báo cáo p-value, khoảng tin cậy, effect size cho các so sánh.  
8. **Phân tích lỗi:** Phân tích các trường hợp sai chính, sai lệch.  
9. **Hạn chế:** Nêu giới hạn của thực nghiệm (ví dụ mẫu dữ liệu nhỏ, giả định không thực, v.v.).

## 16. Quy tắc Diễn giải  
- **Supported (Được hỗ trợ):** Bằng chứng mạnh mẽ cho thấy cải tiến giải quyết được limitation (ví dụ, tăng metric chính có ý nghĩa, cải thiện lead time, không giảm metric khác).  
- **Weakly Supported (Hỗ trợ yếu):** Có xu hướng tích cực nhưng khác biệt nhỏ hoặc biến thiên cao (ví dụ cải tiến tăng metric chút ít nhưng chưa qua kiểm định).  
- **Not Supported (Không hỗ trợ):** Kết quả không chỉ ra cải tiến có lợi (chỉ bằng baseline, không tăng).  
- **Contradicted (Trái chiều):** Cải tiến làm giảm chất lượng (metric chính giảm, hoặc tác động phụ tiêu cực quá lớn).  

Không đánh giá cải tiến tốt hơn chỉ vì một metric tăng trên một dataset. Phải có nhiều khía cạnh hỗ trợ. Nếu cải tiến không hiệu quả hoặc làm kém đi, ghi nhận đây vẫn là kết quả quan trọng để học hỏi.

## 17. Các mối đe dọa Đến tính hợp lệ  
- **Nội bộ (Internal):** Lỗi triển khai (mismatch), tuning không công bằng, rò rỉ dữ liệu (ví dụ dùng thông tin test trong train), cấu hình khác nhau. Giải pháp: rà soát code, kiểm soát một biến tại một thời điểm.  
- **Ngoại bộ (External):** Dữ liệu/hệ thống giới hạn (chỉ có 1 dataset, bias của benchmark), kết quả không khái quát ra thực tế. Giải pháp: minh bạch bối cảnh, (nếu có) kiểm thử cross-dataset (E7).  
- **Tính hợp (Construct):** Metric hoặc label không phản ánh đúng "phát hiện sớm" thực sự (ví dụ cách đánh nhãn sớm có thể đơn giản hóa).  
- **Kết luận (Conclusion):** Số lần chạy quá ít, biến thiên lớn, kết luận thừa nhận này. Duy trì dự trữ khi kết quả gần ngưỡng.  
- **Mô hình nền tảng (Foundation Model):** Bản chất không xác định (non-deterministic) của LLM, drift qua thời gian (nếu dùng model đám mây). Kiểm soát: fix phiên bản, seeds, nếu dùng API lưu lại bản snapshot input-output của vài lần chạy.  
- **Truy vấn:** Dữ liệu tra cứu lỗi thời hoặc không liên quan, rò rỉ thông tin tương lai trong retrieval (dựa trên nội dung log tương lai). Kiểm soát: sử dụng snapshot index tại thời điểm, đảm bảo chỉ truy vấn tài liệu trước sự kiện.

Mỗi loại đe dọa cần được nhận diện rõ và ghi chú biện pháp giảm thiểu (ví dụ giám sát kỹ code, tách data timeline cẩn thận, báo cáo ngưỡng tin cậy cao).  

## 18. Sẵn sàng Xuất bản  
Trước khi trình bày:  
- Đã trả lời đầy đủ RQ và kiểm định H tương ứng.  
- Baseline tái hiện rõ kết quả gốc, so sánh công bằng giữa Baseline và Cải tiến.  
- Các thước đo phát hiện sớm được tính và báo cáo.  
- Có ablation đủ để gán lý do cải tiến.  
- Bằng chứng thống kê (p-value, CI) đầy đủ.  
- Mọi tham số, dữ liệu, model, code đều phiên bản đầy đủ (xem phần 13).  
- Nêu rõ hạn chế một cách trung thực.  

Đảm bảo mọi thông tin cần thiết để người khác tái lập kết quả đều có trong phụ lục hoặc artifact kèm theo.

## 19. Quyết định Thực nghiệm Cuối cùng  

| Yếu tố nghiên cứu | Bằng chứng                      | Kết luận                  | Độ tin cậy |
|-------------------|---------------------------------|---------------------------|------------|
| **RQ1**           | Xét kết quả E2, thấy metric chính tăng đáng kể so với baseline. | Hỗ trợ                      | Cao        |
| **RQ2**           | Qua E3, lead time cải thiện, tỷ lệ phát hiện sớm tăng nhẹ.    | Hỗ trợ yếu                 | Trung bình |
| **RQ3**           | Trong E5/E7, cải tiến không vượt trội baseline về robustness.   | Không hỗ trợ               | Trung bình |
| **H1**            | Supported (F1 tăng, p<0.05)                               | Validated                 | Cao        |
| **H2**            | Weakly supported (giảm thời gian phát hiện, nhưng biến đổi cao) | Partially Validated       | Trung bình |
| **H3**            | Contradicted (ví dụ false alarm tăng hoặc tốn kém hơn)     | Not Validated             | Thấp       |

**Kết luận chung:** *Cải tiến đã được xác nhận một phần.* Cải tiến đạt được mục tiêu chính (metric tăng có ý nghĩa, số liệu H1 hỗ trợ). Nó cũng giúp giảm thời gian phát hiện một mức độ nhất định (H2), nhưng chưa rõ ràng về mức độ ổn định hơn (H3). *Tìm hiểu chính:* cải tiến giải quyết hạn chế chính, cải thiện hiệu năng phát hiện. *Hạn chế chính:* tăng chi phí tính toán hoặc false alarm nhẹ. *Trade-off:* Độ trễ/phí tổn tăng (quan sát từ E6), và false positive tăng nhẹ. *Bước tiếp theo:* Tiếp tục tối ưu cải tiến (ví dụ điều chỉnh threshold, giảm tải chi phí) và có thể thử nghiệm thêm với dữ liệu mới trong cùng hướng cải tiến này để tăng tính khái quát. 

**Trạng thái:** **Partially Validated** – cải tiến hữu ích trên metric chính nhưng cần cải thiện thêm về trade-off chi phí/độ chính xác (xem phần phân tích lỗi và độ cứng).

**Nguồn tham khảo:** Quy định thực nghiệm và khuyến cáo về khả tái lặp từ ICSE 2027 Artifact Evaluation, NeurIPS checklist, hướng dẫn version hóa ML.