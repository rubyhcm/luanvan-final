Dataset gần thực tế - **OpenStack**: trích dẫn từ [DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning](https://acmccs.github.io/papers/p1285-duA.pdf) và [Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics](https://arxiv.org/abs/2008.06448). Dataset có 2.000 dòng logs, follow https://github.com/logpai/loghub/tree/master/OpenStack.

- **structured sample CSV** dùng các field: `LineId`, `Logrecord`, `Date`, `Time`, `Pid`, `Level`, `Component`, `ADDR`, `Content`, `EventId`, `EventTemplate`; field `ADDR` đặc biệt hữu ích vì thường chứa request/context identifiers để correlation theo request hoặc transaction.

- Tiền xử lý cho OpenStack là: parse raw log thành template bằng **logparser/Drain**, correlation theo `ADDR` hoặc theo service log (`nova`, `neutron`, `keystone`, nếu có), sau đó tạo **request windows** hoặc **fixed windows** để huấn luyện baseline; deep baselines lấy từ deep-loglizer, còn parser/feature baselines dùng từ logparser/loglizer.

Dataset đơn giản dễ thực hiện train baseline ban đầu để test (được sử dụng trong nhiều papers): **HDFS_v1** trích dẫn từ [Detecting Large-Scale System Problems by Mining Console Logs](https://people.eecs.berkeley.edu/~jordan/papers/xu-etal-sosp09.pdf) và [Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics](https://arxiv.org/abs/2008.06448). Dataset có 2.000 dòng logs, follow https://github.com/logpai/loghub/tree/master/HDFS

- **structured CSV sample** của HDFS dùng các field: `LineId`, `Date`, `Time`, `Pid`, `Level`, `Component`, `Content`, `EventId`, `EventTemplate`. Trong bản demo của loglizer, HDFS được dùng trực tiếp cho API `load_HDFS(...)`, và benchmark HDFS trong loglizer công bố nhiều baseline cổ điển như LR, Decision Tree, SVM, Isolation Forest, PCA, Invariants Mining và Clustering => HDFS_v1 lý tưởng để dựng pipeline đầu tiên, vì cả **schema**, **trace unit** lẫn **baseline literature** đều rất rõ.

Dataset lớn test performance: **Thunderbird** và **BlueGene/L** lấy từ https://www.usenix.org/cfdr-data#hpc4, số dòng log lớn nhưng được thu thập trong giai đoạn 2003 đến 2007 (hơi cũ), follow chi tiết ở https://github.com/logpai/loghub/tree/master/Thunderbird và https://github.com/logpai/loghub/tree/master/BGL

## NOTE

Dự tính dùng HDFS_v1 hoặc OpenStack để train, dùng Thunderbird hoặc BlueGene_L để test thử nghiệm
