# 1. Bản đồ tài liệu (Q1/Q2, 2023–2026)

Chúng tôi khảo sát các công trình liên quan tới **phát hiện bất thường từ log** được công bố 2023–2026 trên các tạp chí **Q1/Q2** có peer-review (không tính preprint). Kết quả sơ bộ:

- **Transformer/NLP-based**: Ví dụ _CoLog_ (Nasirzadeh et al. 2025, Sci. Rep. Q1) dùng **collaborative transformer** để phát hiện _điểm bất thường_ lẫn _tập hợp bất thường_. _LogEDL_ (Duan et al. 2024, Appl. Sci. Q2) tích hợp **evidential deep learning** vào mô hình BERT để xử lý bất định và các _anomaly mới_. _Sentiment-Aware BERT_ (Catalán et al. 2026, Sci. Rep. Q1) dùng **BERT + phân tích cảm tính** để phân loại bất thường trong từng dòng log riêng lẻ. _LogSentry_ (Li et al. 2025, Sci. Rep. Q1) kết hợp **contrastive learning** và **RAG (KNN retrieval)** với mô hình BERT để tăng độ chính xác. _TM LogMTC_ (He et al. 2025, IEEE Trans. Sust. Comput. Q1/Q2) đề xuất **chuyển giao học và học đối chiếu** cho phát hiện bất thường đa hệ thống khác dịch vụ.

- **Contrastive Learning**: Phương pháp như _LogContrast_, _AugLog_, _CLDTLog_ (các nguồn trước 2023) và _LogSentry_ (2025) dùng supervised contrastive để cân bằng dữ liệu (LogSentry đạt hiệu quả cao nhờ RAG như trên).

- **Trí tuệ hướng agent/memory**: Các hướng rất mới như _LogRESP-Agent_ (trên MDPI preprint) đề xuất khung AI tác nhân tự hướng (SAS, 2024, chưa peer-review Q1/Q2) tuy chưa chính thức. Dữ liệu cũng chưa thấy bài Q1/Q2 áp dụng LLM hay Agent chi tiết cho anomaly logs, ngoại trừ _Cabello et al._ (2026, Systems Soft. Comput.) dùng tự mã hóa LogBERT cho AIOps thực tế.

- **Hybrid và ML truyền thống**: _Aziz & Munir_ (IEEE Access 2024, Q2) dùng hybrid kết hợp SOM, Autoencoder và BERT để cải thiện độ chính xác chung. Tuy nhiên, đa số kỹ thuật mới ưu tiên **deep learning/transformer** do khả năng xử lý ngôn ngữ log linh hoạt.

- **Xu hướng nổi bật (2023–2026)**: Sự thống trị của các mô hình transformer tiền huấn luyện (BERT, LogBERT) và phương pháp tăng cường (contrastive, evidential learning) ghi nhận trong các bài nêu trên. Đồng thời, sự quan tâm tăng về việc tích hợp **retrieval-augmented (RAG)** đã thể hiện qua _LogSentry (2025)_. Ngoài ra, các phương pháp tăng khả giải thích (như SHAP kết hợp BERT) được đề xuất. Các nghiên cứu về **annot có giá trị dài hạn** (log theo thời gian, bộ nhớ) hay **kiến thức chuyên ngành** chưa thấy xuất hiện trong Q1/Q2 recent, chủ yếu là xu hướng mới đầy hứa hẹn.

# 2. Xu hướng nghiên cứu

Các phương pháp **độ trễ thấp/hệ thời gian thực** vẫn là thách thức lớn. Các tác giả như Nasirzadeh et al. nêu rõ _CoLog_ mới được đánh giá trong chế độ “batch”, cần tối ưu cho latency khi triển khai thực nghiệm. Đồng thời, tăng cường **khả năng thích ứng** (log thay đổi cấu trúc theo thời gian) được các tác giả thừa nhận là hạn chế cần khắc phục. Những hướng nghiên cứu “N+1D” (nhanh, hiệu quả, dễ giải thích) đang nổi lên, ví dụ phân tích cảm tính nội dung log và RAG để tăng cường ngữ cảnh. Ngoài ra, _sentinel AI_ (triển khai agent tự động hóa phân tích log) và **kiến thức ngoài (knowledge base)** tuy được nhắc đến, nhưng chưa nhiều paper chính thống Q1/Q2. Có thể thấy bức tranh nghiên cứu đang di chuyển từ các mô hình deep learning cơ bản lên tích hợp **bộ nhớ dài hạn, retrieval, tri thức chuyên ngành** để giải quyết dữ liệu log đa dạng và biến động.

# 3. Phân loại phương pháp

Chúng tôi đề xuất phân nhóm như sau (theo hướng công nghệ):

- **Transformer/NLP**: Các phương pháp dựa trên BERT/BERT cải tiến, LogBERT, hoặc các biến thể transformer (CoLog, LogEDL, Sentiment-BERT, BiLSTM+CNN hybrid).
- **Contrastive Learning**: Áp dụng supervised contrastive để cải thiện phân bố embedding (LogSentry, CLDTLog, AugLog).
- **Knowledge-Augmented (RAG)**: Phương pháp có truy vấn tri thức bên ngoài, bộ nhớ (LogSentry tích hợp retrieval, chuẩn bị vector logs).
- **Agent/Multi-Agent AI**: Các kiến trúc sử dụng tác nhân tự động (ví dụ kiến trúc trong LogRESP-Agent) – còn rất ít tài liệu Q1/Q2.
- **Memory-Enhanced**: Mô hình có thành phần bộ nhớ dài (hiện vẫn lỏng lẻo ở giai đoạn này).
- **Truyền thống/Machine Learning**: Hybrid SOM/Autoencoder (Aziz & Munir 2024), LightGBM (Djukanovic et al. 2026 dùng TF-IDF/BERT+LightGBM tối ưu PSO).

# 4. Bức tranh các phương pháp Q1/Q2 (2023–2026)

| Phương pháp                               | Năm  | Tạp chí                     | Kiến trúc chính                               | Công khai mã nguồn | Datasets chính                 | Hiệu năng (đặc điểm)                                         |
| ----------------------------------------- | :--: | --------------------------- | --------------------------------------------- | ------------------ | ------------------------------ | ------------------------------------------------------------ |
| **CoLog** (Nasirzadeh et al. 2025)        | 2025 | _Scientific Reports_ (Q1)   | Collaborative Transformer 2-modality          | **Có** (GitHub)    | HDFS, BGL, WID                 | Precision≈99.6%, Recall≈99.6%, F1≈99.6% trên 7 tập log       |
| **LogSentry** (Li et al. 2025)            | 2025 | _Scientific Reports_ (Q1)   | BERT + Contrastive + KNN-RAG                  | Không rõ           | HDFS, BGL, Thunderbird         | Đạt “hiệu năng cao hơn baseline” (tăng F1) với RAG           |
| **LogEDL** (Duan et al. 2024)             | 2024 | _Applied Sciences_ (Q2)     | BERT + Evidential Deep Learning               | Không công bố      | HDFS, BGL, Thunderbird         | Khẳng định đạt SOTA trên HDFS, BGL, Thunderbird              |
| **Aziz & Munir** 2024                     | 2024 | _IEEE Access_ (Q2)          | SOM + BERT + Autoencoder (Hybrid)             | Không công bố      | (log, traffic, transaction)    | Tăng độ chính xác so với mô hình trước (DeepLog, LogAnomaly) |
| **Sentiment-BERT** (Catalán et al. 2026)  | 2026 | _Scientific Reports_ (Q1)   | BERT + Sentiment Analysis + SHAP              | Không rõ           | Casper, Windows, Zookeeper,…   | F1≈99.96% (in-domain), 96.97% (out-of-domain)                |
| **NLP+LightGBM** (Djukanovic et al. 2026) | 2026 | _Scientific Reports_ (Q1)   | TF-IDF/BERT/Word2Vec + PSO-optimized LightGBM | Không rõ           | Cloud logs (tùy tập)           | “Accuracy up to 100%” (có vẻ dễ dataset)                     |
| **LogMTC** (He et al. 2025)               | 2025 | _IEEE Trans. Sust. Comput._ | Transfer Learning + Contrastive               | Không công bố      | Chuyển giao logs (hai dịch vụ) | Hơn LogTAD ~1–8% F1 trên nhiều target                        |

# 5. Ứng viên baseline tiềm năng

Theo tiêu chí nghiêm ngặt (Q1/Q2, năm 2023–2026, bài đăng chính thức, code reproducible), các ứng viên baseline có thể cân nhắc:

| Tên phương pháp             | Năm  | Tạp chí (Xếp loại)             | Công khai mã    | Chất lượng repo       | Phù hợp Early-AD          | Điểm mạnh                                  | Độ tân thời     | Kết quả                           | Hạn chế chính                                               | Bằng chứng hạn chế                                     |
| --------------------------- | :--: | ------------------------------ | --------------- | --------------------- | ------------------------- | ------------------------------------------ | --------------- | --------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------ |
| **CoLog** (Nasirzadeh+2025) | 2025 | Sci. Reports (Q1, JCR/Scimago) | Có (GitHub MIT) | Cao (162 commit, MIT) | Cao (điểm tập & đơn điểm) | Hiệu năng SOTA (F1≈99.6% trên 7 tập)       | Mới             | Rất tốt                           | _Batch mode; chủ yếu anomaly cuối chuỗi; cần adapt log mới_ | “Chỉ đánh giá batch, cần cải thiện cho thời gian thực” |
| **LogSentry** (Li+2025)     | 2025 | Sci. Reports (Q1)              | Không tìm thấy  | –                     | Trung bình (cả sequence)  | Kết hợp RAG, cải thiện imbalance           | Mới             | Cao                               | _Không có code; giá trị thực tiễn chưa rõ_                  | “RAG nâng cao độ chính xác”                            |
| **LogEDL** (Duan+2024)      | 2024 | Appl. Sciences (Q2)            | Không công bố   | –                     | Trung bình (sequence)     | Open-set recognition via uncertainty       | Mới             | SOTA                              | _Không code; chỉ tập trung classify cuối_                   | “Đạt SOTA phát hiện bất thường”                        |
| **Aziz & Munir** 2024       | 2024 | IEEE Access (Q2)               | Không công bố   | –                     | Trung bình                | Phương pháp lai (SOM + autoencoder + BERT) | Trung bình (Q2) | Cải thiện vs DeepLog & LogAnomaly | _Không code; kém current transformer_                       | “Chiến thắng các PP trước trên nhiều loại dữ liệu”     |

Trong số này, **CoLog** nổi bật là ứng viên baseline tốt nhất: công bố Sci. Rep Q1 (hạng cao), mã nguồn đầy đủ và được tác giả cung cấp, kết quả F1 rất cao. Các ứng viên khác dù có phương pháp mạnh (LogSentry kết hợp RAG, LogEDL mở rộng nhận dạng open-set) nhưng thiếu mã công khai hoặc chưa rõ reproducibility. Do đó, CoLog được chọn làm baseline chính, trong khi LogSentry có thể xem là đối thủ tham khảo để so sánh.

# 6. Phân tích so sánh baseline

**CoLog (Nasirzadeh+2025)** – _Ưu:_ hiệu năng cực cao (mean F1≈99.6% trên 7 bộ dữ liệu logs), thiết kế transformer lai 2-modality cho cả điểm và tập bất thường, mã nguồn mở (MIT), sử dụng kiến trúc rõ ràng và có báo cáo đầy đủ. _Nhược:_ chỉ đánh giá mô hình theo lô (batch), chưa kiểm tra thời gian thực; giả định logs cố định (templates) và dữ liệu có imbalance nhẹ, có thể giảm performance nếu anomaly hiếm (<1%) hoặc logs thay đổi nhanh. Không tích hợp cơ chế truy vấn bên ngoài (retrieval) hay lịch sử logs.

**LogSentry (Li+2025)** – _Ưu:_ Gợi ý hướng kết hợp retrieval với contrastive để cải thiện imbalance; thu được “hiệu năng cao” và cho thấy retrieval KNN rất hữu ích cho độ chính xác. _Nhược:_ Công bố SciRep Q1 nhưng không thấy mã nguồn; chi tiết hiệu năng chưa rõ số liệu cụ thể; chưa đạt độ nổi tiếng bằng CoLog. Tính phù hợp Early-AD ở mức trung bình do focus detection cuối sequence với threshold.

**LogEDL (Duan+2024)** – _Ưu:_ Kết hợp mô hình BERT với **Evidential Deep Learning**, giúp mô hình nhận diện _unknown anomalies_ (mở rộng khung đóng-phạm vi). _Nhược:_ Tạp chí Q2; không mã hóa nguồn; chưa rõ cấu trúc architecture (phụ thuộc BERT tiêu chuẩn); thiếu khai triển cho early detection, chỉ báo cáo phân loại nhị phân cuối sequence. Dù tác giả claim SOTA, nhưng không so sánh trực tiếp với các method transformer mới nhất.

**Aziz & Munir 2024** – _Ưu:_ phương pháp lai (SOM + BERT + autoencoder) và báo cáo cải thiện so với DeepLog, LogAnomaly trên tập dữ liệu hỗn hợp (log, traffic, giao dịch). _Nhược:_ IEEE Access Q2; mã nguồn không công bố; phương pháp kém mới so với transformer; chỉ thử nghiệm đơn hệ thống, không tập trung early detection hay môi trường lớn. Do vậy tiềm lực baseline thấp hơn CoLog.

# 7. Phân tích thành phần

CoLog gồm các thành phần chính: (1) **Tiền xử lý và biểu diễn**: sử dụng tokenizer/BERT (tùy biến) tạo embedding từ logs; (2) **Collaborative Transformer**: hai thành phần (ví dụ transformer mạng đa-kênh) xử lý các modal log khác nhau (structure vs content) kết hợp qua attention đặc biệt; (3) **Cân bằng (balancing layer)**: thành phần điều chỉnh sự mất cân bằng (implícit sử dụng weighted loss hoặc focal loss); (4) **Bộ phân loại (anomaly scorer)**: đưa ra nhãn (bất thường/người) cho từng log entry; (5) **Hậu xử lý**: nhóm điểm bất thường để phát hiện tập bất thường lớn. CoLog chú trọng phát hiện cả **anomaly điểm lẻ (point)** lẫn **tập anomaly (collective)**.

CoLog làm tốt phần **rút trích ngữ nghĩa** (Transformer capture complex patterns) và **chuyển đổi thông báo đa-modal**. Yếu điểm: _không có cơ chế nhớ hay truy vấn_ – mọi dự đoán dựa trên mô hình huấn luyện. Hơn nữa, CoLog chưa nghiên cứu **khoảng cách thời gian** (detection lead time) mà chỉ tập trung classification. Các cải tiến tiềm năng được báo cáo bao gồm _continual learning_, _fine-tuning nhanh_ hoặc _resampling adaptive_ để đối phó imbalance nghiêm trọng. Ngoài ra, CoLog có thể cải thiện bằng cách kết hợp **thủ tục retrieval**: ví dụ LogSentry đã chứng minh việc lưu trữ embedding của logs huấn luyện và tra cứu KNN cải thiện recall khi dữ liệu bất cân bằng.

# 8. Bằng chứng hạn chế của baseline

Từ CoLog (bài gốc) và các nghiên cứu liên quan, hạn chế chính có bằng chứng gồm:

- **Khả năng thời gian thực thấp**: Tác giả CoLog thừa nhận mô hình mới chỉ đánh giá theo batch; đối với giám sát thực tế cần lo ngại độ trễ và tài nguyên.
- **Không bắt kịp logs biến đổi**: CoLog giả định định dạng logs tĩnh (template ổn định). Khi _template thay đổi nhanh_ hoặc anomaly tỷ lệ cực thấp (<1%), hiệu năng có thể giảm và cần “continual learning” hoặc _resampling adaptive_.
- **Chưa sử dụng thông tin lịch sử/ngữ cảnh bên ngoài**: CoLog không kết hợp cơ chế **retrieval/memory**, nên thiếu thông tin từ các logs tương tự hoặc sự kiện cũ. Trong khi đó, LogSentry chứng minh RAG (tra cứu KNN) rất cần thiết để khắc phục bias và cải thiện F1.
- **Chi phí tính toán**: Transformers cộng tác có kiến trúc phức tạp; chưa rõ điều này ảnh hưởng thế nào đến latency (chỉ đề cập cần tối ưu cho real-time).
- **Thiếu đánh giá về Early Detection**: Các báo cáo (CoLog, LogEDL…) chỉ cung cấp Precision/Recall/F1 cho nhãn anomalous, không đo “độ trễ phát hiện” (lead time). Do vậy chưa có bằng chứng họ thực sự làm “phát hiện sớm” log bất thường theo nghĩa đo thời gian trước lỗi. Theo hướng dẫn, nếu chỉ dùng F1 thì không chắc Early-AD đạt.

# 9. Cơ hội cải tiến (Improvement Mapping)

Dựa trên hạn chế có chứng cứ, một hướng cải tiến mục tiêu là **bổ sung Retrieval/Memorie augmentation** cho CoLog:

| Baseline                  | Hạn chế xác nhận                             | Bằng chứng (paper)                             | Công trình liên quan                                                                                                        | Hướng cải tiến đề xuất                                                                                                                                                 | Kết quả kỳ vọng                                                                                                                                    | Rủi ro/Khó khăn                                                                                                                                                  |
| ------------------------- | -------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _CoLog_ (Nasirzadeh 2025) | Không tận dụng ngữ cảnh lịch sử/log tương tự | CoLog đánh giá batch, cần real-time; thiếu RAG | _LogSentry (2025)_: retrieval KNN giúp cải thiện độ chính xác; _ConceptDrift Work_ (thu hồi logs cũ khi templates thay đổi) | Thêm cơ chế **retrieval-augmented**: lưu embedding logs huấn luyện và khi suy đoán, kết hợp dự đoán của model CoLog và kết quả KNN tìm logs tương tự (RAG kiểu hybrid) | Cải thiện khả năng phát hiện **anomaly bất thường** mới hoặc hiếm bằng dữ liệu lịch sử; ổn định hơn với drift template; tăng recall trên anomalous | Tăng chi phí lưu/tra cứu (chi phí tính toán cao hơn); chọn trọng số α (kết hợp model + KNN) khó tuning; rủi ro “noisy retrieval” nếu logs nhị phân quá khác biệt |
| _CoLog_                   | Định dạng log thay đổi nhanh (drift)         | Mô tả tương tự như trên                        | _Continual Learning_ trên logs; _Adaptive Resampling_                                                                       | Kết hợp **fine-tuning online**: sử dụng lịch sử logs mới để tái huấn luyện nhẹ hoặc tiền huấn luyện thêm; sử dụng cơ chế _memory_ để nhận diện drift.                  | Nâng khả năng thích ứng với log mới; giảm hiệu năng suy giảm khi anomaly hiếm; duy trì độ chính xác qua thời gian                                  | Yêu cầu dữ liệu mới liên tục; rủi ro quá khớp với dữ liệu vừa thêm; phức tạp triển khai                                                                          |
| _CoLog_                   | Only batch inference                         | CoLog không hỗ trợ real-time (limit latency)   | –                                                                                                                           | **Giảm độ trễ**: tinh giản kiến trúc (như nén model), hoặc xử lý incremental (xử lý theo cửa sổ trượt nhỏ hơn)                                                         | Phù hợp triển khai thực tế trong AIOps; phát hiện sớm các anomaly (nếu giảm windows)                                                               | Giảm accuracy nếu windows quá nhỏ; cần thử nghiệm tính năng;                                                                                                     |

Bảng trên cho thấy _retrieval-augmented_ là cải tiến khả thi nhất nhắm trúng hạn chế có bằng chứng. LogSentry chứng tỏ RAG (KNN) “không thể thiếu” để tăng hiệu quả phân loại logs. Do vậy, chúng tôi đề xuất bổ sung RAG (có thể dùng kiến trúc vector database/FAISS) vào baseline CoLog. Kết quả mong đợi: tăng khả năng **nhận diện các bất thường chưa thấy**, đồng thời ổn định xử lý logs thay đổi.

# 10. Phân tích benchmark

Các công trình đều dùng các **tập dữ liệu công khai** truyền thống: _HDFS_, _BGL_, _Thunderbird_, _OpenStack_, _Spirit_, _Zookeeper_, _Windows_, v.v. (đặc biệt CoLog dùng 7 tập, Li+2025 dùng 3 tập). Đặc điểm chung: nhiều bộ có tính _mất cân đối_ (bình thường áp đảo bất thường), mẫu anomalies đa dạng (point và collective). Tuy nhiên, những tập này **ít tương tác thời gian thực** (gồm tập log đã có nhãn), nên không đo được lead-time phát hiện. Bản đồ sau tóm lược:

- **Tính quy mô**: HDFS, BGL là tập lớn (trên hàng chục nghìn đến hàng triệu sequence), các tập khác nhỏ hơn. CoLog và Li+2025 đều đạt F1 cao trên những tập này, tuy nhiên chưa đánh giá latency thực tế.
- **Loại anomaly**: Hầu hết đặt _nhiệm vụ nhị phân_ (bình thường/không) trên mỗi sequence log hoặc entry. CoLog còn phát hiện tập anomalies (collective) lồng nhau. Tuy nhiên, không rõ tập thử của CoLog có đo _early detection_ (trước failure) – mọi nhãn là hậu-facto anomalies.
- **Độ lệch**: Gần như không có sự đề cập về dữ liệu bên ngoài hay knowledge graph. Các phương pháp chủ yếu xử lý nội dung log bằng mạng neural tự thích ứng.
- **Thực dụng**: Các tập log benchmark (như HDFS, BGL) đã kinh điển nhưng có thể _không phản ánh đầy đủ_ phân bố logs phức tạp, đa dạng của hệ thống hiện đại. Chưa có benchmark nào tập trung đánh giá “cảnh báo sớm trước lỗi”.

Tóm lại, các tập benchmark hiện tại khó đánh giá khả năng _early anomaly detection_ (vì thiếu lead-time label). Chúng ta cần thận trọng không gán nhãn “early detection” cho kết quả chỉ có F1; phải đo các metrics như **Time-to-Detection** hoặc **early warning** nếu triển khai thật.

# 11. Phân tích đánh giá Early Detection

Trong số nghiên cứu, **không công bố metric nào đo trước khi lỗi xảy ra (lead time)**. Các công bố đều báo F1/Precision/Recall trên nhãn anomalies (đã biết). Không có báo cáo _Detection Lead Time_, _Time-to-Detection_ hoặc _Early Warning Horizon_. Vì thế, phạm trù **Early Log Anomaly Detection** (phát hiện thật sự trước sự cố) chưa được thực sự đánh giá; mọi phương pháp hiện nay chỉ là anomaly detection chung. Để xứng đáng tên gọi “sớm”, mô hình cần thử nghiệm trên tập có thời gian gắn cảnh báo trước sự cố, nhưng chưa có trong Q1/Q2.

# 12. Định vị nghiên cứu

Nghiên cứu dự kiến là **mở rộng và cải tiến** (incremental) của phương pháp CoLog (Q1 2025). Không hướng tới phát minh kiến trúc hoàn toàn mới: Chúng ta giữ khung CoLog (vì đã mạnh) và thêm thành phần targeted (retrieval). Điều này phù hợp nguyên tắc: “improvement/extension of existing method”, không công bố mô hình mới toanh. Tính đóng góp: đánh giá ưu thế của RAG khi bổ sung vào kiến trúc transformer hiện có, so sánh cụ thể với baseline (CoLog thuần) trên cùng benchmark. Do đó, nghiên cứu ở mức **Level 2 – Cải tiến mục tiêu**.

# 13. Đề xuất baseline và lý do

**Đề xuất baseline:** _CoLog (Nasirzadeh et al. 2025)_ – vì đáp ứng đầy đủ tiêu chí: đăng trên tạp chí Q1, năm 2025, đã peer-review; mã nguồn công khai và reproducible; kết quả hàng đầu (F1≈99.6%); kiến trúc rõ ràng và tác giả đánh giá ablation/anomalies. So với LogSentry hoặc LogEDL, CoLog có **chất lượng công bố cao hơn (Q1)** và có sẵn mã để tái tạo. CoLog _cũng phù hợp cho Anomaly Detection tổng quát_, mặc dù không đo lead time, nhưng thực tế cơ chế point/collective detection là nền tảng tốt. Nhược điểm (chưa có realtime, khôgn RAG) chính là cơ hội cải tiến hướng dẫn.

# 14. Cải tiến mục tiêu

**Hướng cải tiến:** Bổ sung **kiến trúc retrieval-augmentation (RAG)** vào CoLog. Cụ thể, duy trì CoLog như một encoder transformer, nhưng tạo thêm _“bộ nhớ log embedding”_ từ dữ liệu huấn luyện (như kho vector với nhãn anomaly). Khi dự đoán trên log mới, ta truy vấn N (Top-K) láng giềng gần nhất và kết hợp kết quả (theo trọng số) giữa CoLog và kết quả “bỏ phiếu” từ neighbors (như LogSentry). Điều này nhằm tận dụng thông tin lịch sử để **cải thiện độ nhạy** với trường hợp bất thường hiếm hoặc cú pháp log lạ, đồng thời giúp giảm thiểu bias do imbalance. Ta sẽ đánh giá CoLog gốc vs. CoLog+RAG trên bộ benchmark chuẩn (F1, Precision, Recall), và nếu có thể, đo thử thời gian trung bình phát hiện (nếu dự kiến thời gian thực).

# 15. Kết quả chính

1. **Hạ tầng tri thức**: Sự bùng nổ các mô hình transformer và RAG đã được áp dụng cho anomaly detection (CoLog, LogSentry). Các xu hướng AI cao cấp (LLM agent, knowledge graph) mới nổi nhưng chưa thấy trong Q1/Q2 2023-2026.
2. **Tổng quan các phương pháp**: Transformer/NLP chiếm ưu thế, tập trung vào cải thiện embedding (contrastive, evidential) và khả năng giải thích (SHAP). Retrieval (RAG) bắt đầu xuất hiện nhưng chủ yếu ở dạng KNN offline.
3. **Baseline mạnh**: CoLog (2025) là phương pháp dẫn đầu về hiệu năng và đã open-source, nên phù hợp làm baseline. Các hạn chế chính (thời gian thực, thích ứng log mới) đã được chính tác giả công nhận.
4. **Bằng chứng hạn chế**: CoLog được chứng minh SOTA trên F1, nhưng thiếu đánh giá realtime; các ablation cho thấy kỹ thuật của CoLog cần thử trong môi trường vận hành.
5. **Cơ hội cải tiến**: Kết quả của LogSentry cho thấy _retrieval-augmented_ giúp tăng performance rõ rệt. Đây là cơ sở kỹ thuật để gợi ý thêm thành phần RAG cho CoLog.
6. **Hướng nghiên cứu**: Mục tiêu cải tiến là **mở rộng CoLog** bằng thành phần truy vấn dữ liệu lịch sử. Đây là thay đổi có mục tiêu (targeted enhancement) thay vì đề xuất hoàn toàn mới. Dự kiến đánh giá: so sánh CoLog & CoLog+RAG theo các chỉ số chất lượng và tính chi phí.

# 16. Tài liệu tham khảo & Bằng chứng xếp hạng Q1/Q2

Dưới đây liệt kê tài liệu được trích dẫn trong báo cáo và căn cứ hạng Q1/Q2 (theo JCR/Scimago 2025 khi có):

- Nasirzadeh _et al._, **“A unified framework for detecting point and collective anomalies in operating system logs via collaborative transformers”**, _Sci. Reports_, 15:45698 (2025). (Q1; mã nguồn: MIT, link [GitHub].)
- Li _et al._, **“System log anomaly detection based on contrastive learning and retrieval augmented”**, _Sci. Reports_, 15:38370 (Nov 2025). (Q1.)
- Duan _et al._, **“LogEDL: Log Anomaly Detection via Evidential Deep Learning”**, _Applied Sci._ 14(16):7055 (Aug 2024). (Q2, _Applied Sciences_ là Q2 Kỹ thuật đa ngành.)
- Aziz & Munir, **“Anomaly Detection in Logs Using Deep Learning”**, _IEEE Access_ 12:176124 (2024). (Q2; mã nguồn không công bố.)
- Catalán _et al._, **“Interpretable sentiment-aware transformer-based model … log anomaly detection”**, _Sci. Reports_ 16:24270 (May 2026). (Q1.)
- Djukanovic _et al._, **“NLP + PSO-LightGBM for anomaly detection in cloud logs”**, _Sci. Reports_ 16:21936 (May 2026). (Q1.)
- He _et al._, **“Unsupervised Multi-Target Cross-Service Log Anomaly Detection”**, _IEEE Trans. Sust. Comput._ (Jan 2025). (Q1/Q2, rank SCimago cao; mã nguồn không rõ.)
- Zhang _et al._, **“LayerLog: Log sequence anomaly detection based on hierarchical semantics”**, _Applied Soft Comput._ 132:109860 (2023). (Q1.)
- Thông tin xếp hạng: _Applied Soft Computing_ (Elsevier) Q1 theo SCImago (CiteScore Q1, JCR Q1 Kỹ thuật máy tính). _Applied Sciences_ (MDPI) Q2 Kỹ thuật. _Sci. Reports_ (Nature) Q1 Đa ngành. _IEEE Access_ Q2 Kỹ thuật điện/điện tử. _IEEE Trans. Sust. Comput._ (nếu đánh giá, Q1 đa lĩnh vực tính toán).
