---
layout: page
title: "Bài 1 - Từ Bản Vẽ Tên Lửa Đến Phép Toán Tập Hợp - Bình Minh Của Dữ Liệu"
date: 2026-06-24
excerpt: "Ngày 25 tháng 5 năm 1961, JFK đưa ra thử thách cho toàn nước Mỹ đưa người lên mặt trăng và trở lại trái đất an toàn."
toc: true
---

# 1. Làm sao lắp tàu mặt trăng?

Ngày 25 tháng 5 năm 1961, JFK đưa ra thử thách cho toàn nước Mỹ đưa người lên mặt trăng và trở lại trái đất an toàn. Kỳ tích này phải hoàn thành trước khi thập kỷ kết thúc. Đây là một phần của Nhiệm vụ Apollo. 

American Rockwell là thầu chính chịu trách nhiệm thiết kế và chế tạo tên lửa đẩy Saturn V có nhiệm vụ mang tàu thám hiểm Apollo bay vào không gian. Saturn V là một trong những kì quan công nghệ của toàn nhân loại. Tên lửa này được cấu tạo từ khoảng 2 triệu linh kiện khác nhau, và chỉ nội việc quản lý thông tin của các bộ phận này như: nguồn gốc, thông số kĩ thuật, thứ tự lắp ráp đã là một thử thách cực đại. 

![300]({{ '/assets/media/Pasted%20image%2020260623160209.png' | relative_url }})

Ở thập niên 60, công nghệ lưu trữ dữ liệu lúc đó vẫn chủ yếu là trên băng từ hoặc thẻ đục lỗ. Chắc chắn Rockwell không thể quản lý 2 triệu mảnh tên lửa với những công nghệ đó, vì thế họ bắt tay với IBM. Năm 1966, một đội 12 người được thành lập với thành viên đến từ IBM, Rockwell, Caterpillar Tractor với nhiệm vụ xây một hệ thống quản lý danh mục vật tư cho việc chế tạo tàu vũ trụ. Hệ thống đó được đặt tên *Information Control System and Data Language/Interface (ICS)*, phiên bản đầu tiên ra lò năm 1967, cài đặt lần đầu tại Rockwell Space Division năm 1968. 

Một năm sau thành công đó đó, IBM mở một nhánh kinh doanh mới, đem ICS đổi tên thành IMS (Information Management System/360) và mở bán với toàn thị trường.

<div class="obs-callout obs-callout-info" markdown="1">
<div class="obs-callout-title">Info</div>

- [The Most Important Database You've Never Heard of](https://twobithistory.org/2017/10/07/the-most-important-database.html)
- [History of IMS: Beginnings at NASA - IBM Documentation](https://www.ibm.com/docs/en/zos-basic-skills?topic=now-history-ims-beginnings-nasa)
</div>


![Pasted image 20260623121400]({{ '/assets/media/Pasted%20image%2020260623121400.png' | relative_url }})

## 1.1. Dữ liệu hình cây

> Tên đúng là *mô hình dữ liệu phân cấp (hierarchical data model)* nhưng tôi thích gọi là dữ liệu hình cây. 

Dữ liệu trong IMS được tổ chức theo dạng cây, từ nút tổng nối tới các nút nhỏ hơn. Ví dụ: 

```
Saturn V
├── Khoang 1
│ ├── Động cơ A
│ │ ├── LK-100
│ │ ├── LK-123
│ │ └── LK-200
│ └── Động cơ B
└── Khoang 2
```

Mỗi nút trên cây được nối với nhau bằng các pointer vật lý trỏ trực tiếp tới vị trí dữ liệu trên ổ đĩa:
- nút cha trỏ tới nút con
- các nút anh em lần lượt nối với nhau (thứ tự quan trọng)
- database lần theo các pointer (con trỏ) để truy cập dữ liệu.

Một tương tác điển hình với IMS sẽ trông như thế này:

- Kỹ sư đang lắp ráp hệ thống nhiên liệu của động cơ A. 
- Lần theo đường dẫn `Saturn V/Khoang 1/Động cơ A`, anh tra cứu được thông tin rằng linh kiện `LK-123` đang ở trạng thái `sẵn sàng lắp đặt`. 
- Sau khi lắp đặt xong, anh chuyển trạng thái của nó sang `đã lắp đặt`. 

Hệ thống này rất nhanh và hiệu quả; theo IBM, nó có thể xử lý tới 100.000 giao dịch/giây. Đây cũng là lý do nhiều ngân hàng lớn vẫn còn sử dụng IMS cho tới ngày nay. Tuy nhiên IMS rất thiếu linh hoạt, ta chỉ có thể truy vấn dữ liệu hiệu quả nếu xuôi theo sơ đồ cây đã định sẵn (cha -> con), truy vấn ngược (con -> cha) sẽ là một thảm họa. 

Ví dụ: 
1. Cha -> con : Kiểm tra số dư của tài khoản ID 103 thuộc chi nhánh Kì Đồng của Vietcombank
2. Con -> cha: Tìm xem số điện thoại 0987123456 là của chủ tài khoản nào? 

Nếu muốn truy xuất dữ liệu không theo quy tắc leo các nhánh cây đã được định sẵn như trên ta sẽ gặp khó khăn. Đó là chưa kể đến các truy vấn tùy biến, đa điều kiện của các bài toán hiện đại như: 
- Giám đốc ngân hàng hỏi: Liệt kê tất cả các khách hàng mở tài khoản trong năm 2025, có số dư trên 1 tỷ đồng. 

Các truy vấn ad-hoc kiểu này sẽ cực kì hóc búa và khó nhằn với kĩ sư dữ liệu của hệ thống IMS. 
## 1.2. Thành công của IMS

Mặc dù sở hữu những điểm yếu cố hữu ở tầng thiết kế nhưng IMS vẫn nhanh chóng trở thành lựa chọn hàng đầu trong nhiều ngành công nghiệp ở thời điểm nó ra mắt. Đầu những năm 1970s, IBM đã thành công bán nó cho nhiều nhà máy, nhà bán lẻ, ngân hàng trên khắp nước Mỹ. 

Mặc dù đối đầu với sự cạnh tranh của mô hình cơ sở dữ liệu quan hệ (relational database) ra đời sau đó, nhưng IMS vẫn được duy trì và sử dụng rộng rãi cho đến ngày nay nhờ vào tốc độ và sự ổn định của nó. Đặc biệt các khách hàng đủ tiền mua IMS của IBM từ những năm 70s hầu hết đều thuộc hàng khủng long. 

- Sách [An Introduction to IMS (IBM 2004)](https://public.dhe.ibm.com/software/data/ims/shelf/v9pdf/DFSINTG0.pdf) viết rằng: Hơn 95% công ty Fortune 1000 đang xài IMS ở các mức độ khác nhau.
- Được vận hành bởi toàn bộ top 5 ngân hàng hàng đầu Hoa Kỳ, các công ty bảo hiểm, bệnh viện và cơ quan chính phủ.
- Hầu hết các giao dịch rút tiền tại máy ATM đều tương tác với hệ thống này.

> Xem thêm: [Information Management Systems \| IBM](https://www.ibm.com/history/information-management-system)

# 2. Mang lý thuyết tập hợp vào ổ đĩa

## 2.1. Edgar Codd - Nhà toán học đốn cây

Nhà toán học Edgar F. Codd sinh ra trên hòn đảo nhỏ Portland thuộc vùng biển phía nam nước Anh. Ông từng học ngành hóa tại Oxford đầu những năm 40s rồi xung phong đi phi công cho Không quân Hoàng gia Anh trong Thế chiến 2. Sau chiến tranh ông về Oxford chuyển ngành sang toán và học nốt đại học. 

> Xem [Edgar F. Codd - A.M. Turing Award Laureate](https://amturing.acm.org/award_winners/codd_1000892.cfm)

Tháng 6/1970, Codd, khi đó đang làm việc cho IBM tại chi nhánh San Jose, công bố bài báo [A Relational Model of Data for Large Shared Data Banks](https://www.cis.upenn.edu/~zives/03f/cis550/codd.pdf). Lúc này mô hình dữ liệu hình cây của IMS mới chỉ gần 3 tuổi, và cấu trúc dữ liệu hình cây có những điểm yếu cố hữu ở tầng thiết kế làm Codd không hài lòng. 

Trước Codd, database được xem như một cấu trúc vật lý, mỗi nút được lưu ở một điểm trên ổ đĩa, nút cha được nối với nút con, truy vấn lần theo các đường nối này. Lập trình viên phải suy nghĩ như đang đi trong bộ nhớ máy tính. Các ý tưởng đột phá của Codd có thể được tóm tắt như sau: 
1. Dữ liệu chỉ là các tập hợp toán học
2. Các tập hợp được nối với nhau bởi những giá trị key (giá trị chung để tham chiếu giữa 2 tập, hãy tưởng tượng đến phép VLOOKUP trong Excel)

Chi tiết mời bạn đọc paper gốc, dưới đây là phiên bản đơn giản hóa. 

### 2.1.1. Dữ liệu là tập hợp 

Linh kiện là một tập hợp: 

```
parts = {LK-100, LK-123, LK-200,...}
```

Muốn tìm linh kiện ở trạng thái `sẵn sàng lắp đặt` chỉ cần áp dụng 1 phép toán lên nó: 

```
σ(status = 'sẵn sàng lắp đặt')(parts)
```

Người dùng lúc này chỉ cần mô tả dữ liệu cần lấy, database sẽ tự tìm dữ liệu đó cho họ. 

### 2.1.2. Nối với nhau bởi giá trị key

Tập linh kiện (`parts`) có thể nối với tập động cơ (`engine`) bởi giá trị chung là `engine_id`.

```
ENGINES

engine_id | name
----------+----------
1         | Engine A
2         | Engine B
```

```
PARTS

part_id | name   | engine_id
--------+--------+----------
123     | Valve  | 1
124     | Pump   | 1
125     | Sensor | 2
```

Nếu bạn không phải dân tech, một lần nữa, hãy tưởng tượng lại phép `VLOOKUP` trong Excel. 

### 2.1.3. Kết quả

Từ 2 ý tưởng trên, hàng loạt khái niệm quen thuộc của ngành dữ liệu xuất hiện: 
#### Độc lập dữ liệu

Đây có lẽ là mục tiêu lớn nhất của Codd với relational database. 

Trước Codd, cấu trúc logic và cấu trúc vật lý trên ổ đĩa gần như là một. Nếu database thay đổi cách lưu dữ liệu, ứng dụng cũng phải thay đổi theo. 

Ví dụ, hôm nay:

```text
Saturn V
 └─ Khoang 1
     └─ Động cơ A
         └─ LK-123
```

Ngày mai hệ thống thêm một lớp trung gian:

```text
Saturn V
 └─ Khoang 1
	 └─ Hệ thống nhiên liệu 
	     └─ Động cơ A
	         └─ LK-123
```

Mọi chương trình đang truy cập `LK-123` có thể phải sửa lại vì đường dẫn đã đổi.

Trong mô hình quan hệ, ứng dụng không cần biết dữ liệu được tổ chức ra sao trên ổ đĩa. Chúng chỉ làm việc với các bảng và các quan hệ logic. Điều này tạo ra một lớp ngăn cách giữa người dùng và cách lưu trữ vật lý của dữ liệu. Database có thể thay đổi cấu trúc bên trong để tối ưu hiệu năng mà không làm ảnh hưởng đến ứng dụng phía trên.

Ngày nay chúng ta xem đây là điều hiển nhiên. Năm 1970, nó là một ý tưởng mang tính cách mạng.

#### Bảng dữ liệu

Ở phía trên, tôi đã nói dữ liệu chỉ là các tập hợp. Đây là thứ máy tính thấy: 

```
{
  (123, Valve),
  (456, Pump),
  (789, Turbine)
}
```

Đây là thứ bạn thấy: 

```
PARTS

part_id | name
--------+-------
123     | Valve
456     | Pump
789     | Turbine
```

Dữ liệu bố trí dạng bảng là một lớp trừu tượng được xây nên từ ý tưởng của Codd. Ngày nay chúng ta đã quen với nó đến mức coi như đây là cách mặc định. Đối với dân IT, đây là giao diện ta nhìn thấy hàng ngày trong các phần mềm quản lý database. Đối với một nhân viên văn phòng bình thường, bảng Excel và database là gần như đồng nghĩa. 

#### Ngôn ngữ truy vấn khai báo

Người dùng không còn phải mô tả cách đi đến dữ liệu như với IMS, họ chỉ cần mô tả kết quả mong muốn. Đây là tiền đề cho sự phát triển của ngôn ngữ truy vấn SQL hiện đại: 

```sql
SELECT * 
FROM parts 
WHERE part_id = 123
```

#### Chuẩn hóa & Phi chuẩn hóa (Normalization & Denormalization):

Khi dữ liệu được mô hình hóa thành các tập hợp liên kết với nhau bằng key, một câu hỏi mới xuất hiện: *Nên chia dữ liệu thành bao nhiêu tập khác nhau?* (1) Lưu tất cả vào một bảng lớn hay (2) chia dữ liệu thành các tập nhỏ để giảm duplication, tối ưu lưu trữ? 

Nói cách đơn giản, hướng (1) là phi chuẩn hóa, (2) là chuẩn hóa. 

Câu trả lời của thập niên 70s là (2). Chi phí lưu trữ dữ liệu của thời đó rất đắt đỏ do giới hạn phần cứng, và các bài toán phân tích dữ liệu hiện đại chưa xuất hiện. Chúng ta sẽ trở lại với vấn đề này trong những thập niên tiếp theo của lịch sử. 

## 2.2. IBM kháng cự: Lời nguyền của kẻ dẫn đầu

Nếu bạn là ban lãnh đạo IBM lúc đó, nắm trong tay một phát minh thay đổi nhân loại, bạn sẽ làm gì? Thưởng lớn cho Codd và tất tay vào relational database à?

Không. IBM đã chọn cách dập tắt nó.

Lý do đằng sau thì rất đời thường. Lúc bấy giờ, con gà đẻ trứng vàng của IBM vẫn là IMS. Nó đang bán rất chạy và tạo ra lợi nhuận khổng lồ. Giới chóp bu của IBM nhìn bài báo của Codd như một thứ dị giáo rủi ro đập vỡ nồi cơm hiện tại của công ty.

Codd không chịu ngồi yên, vượt rào sự ngăn cản của IBM để present ý tưởng relational database với khách hàng. Mãi đến khi khách hàng bắt đầu rục rịch đòi hỏi, IBM mới chậm chạp đẻ ra dự án System R (nơi thai nghén ngôn ngữ SQL). Nhưng vì còn mải mê đánh nhau trong cuộc chiến máy tính cá nhân và vẫn rón rén bảo vệ doanh số IMS, phải đến tận năm 1983 IBM mới tung ra sản phẩm relational database thương mại DB2.

Và lúc đó thì miếng bánh đã bị kẻ khác cuỗm mất từ lâu.

## 2.3. Larry Ellison - Người tàn ác sống thảnh thơi

<div class="yt-embed">
  <iframe src="https://www.youtube.com/embed/nG5hYn93GQ8" title="The Database Wars: How Oracle Ruthlessly crushed iBM & took over MySQL" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  <p class="yt-embed-caption"><a href="https://www.youtube.com/watch?v=nG5hYn93GQ8" target="_blank" rel="noopener">The Database Wars: How Oracle Ruthlessly crushed iBM & took over MySQL</a></p>
</div>

Năm 1945, Florence Spellman - một mẹ đơn thân 19 tuổi - ngậm ngùi gửi đứa con trai 9 tháng vừa qua cơn bạo bệnh cho người dì tại Chicago của mình nhận nuôi. Đứa bé đó chính là Larry Ellison. Lớn lên, Larry rất gắn bó với người mẹ nuôi nhưng lại xa cách với người bố - người luôn cay nghiệt nói rằng ông sẽ chẳng bao giờ làm nên trò trống gì. Những tác lực đặc biệt thời thơ ấu này đã nhào nặn nên một Larry Ellison gai góc, ngạo nghễ và có phần tàn nhẫn trên thương trường sau này.

Larry bỏ đại học tới hai lần, rồi tự học lập trình rồi mưu sinh bằng nghề viết code. Sau vài năm lăn lộn tại nhiều công ty khác nhau, Larry đọc được bài báo của Codd, ông cùng các đồng sự thành lập Software Development Laboratories năm 1977 (sau đổi tên thành Oracle). Năm 1979, Oracle tung ra bản thương mại Relational Database đầu tiên. Một fact thú vị: Bản phát hành đầu tiên mang tên **Oracle V2** (bỏ qua bản V1 vì Larry nắm thóp tâm lý khách hàng: _"Chẳng ai lại bỏ tiền đi mua phiên bản số 1 để làm chuột bạch cả"_).

> [Britanica - Larry Ellison](https://www.britannica.com/money/Larry-Ellison)

Larry Ellison không phải một nhà khoa học máy tính lỗi lạc, nhưng ông là một người bán hàng thiên tài. Nếu xét thuần túy về công nghệ thời điểm đó, Oracle V2 rất nhiều lỗi và thua xa dự án mã nguồn mở Ingress (do Michael Stonebraker tại UC Berkeley phát triển). Nhưng trên thương trường, có một sự thật phũ phàng: **Sản phẩm xịn nhất chưa chắc đã là sản phẩm chiến thắng.**

Ellison đã đè bẹp các đối thủ bằng những chiến thuật cực kì khát máu như sau:

1. **Bán Vaporware:** Đội ngũ sale của Oracle sẵn sàng hứa hẹn với khách hàng những tính năng... chưa hề tồn tại trong code base, cốt chỉ để chốt đơn và khóa khách hàng vào hệ sinh thái.
2. **Phá giá cực đoan:** Sẵn sàng cắt giảm lợi nhuận, bán rẻ mạt để đè bẹp các đối thủ kỹ thuật tốt hơn như Ingres ra khỏi các gói thầu lớn.
3. **Đứng trên vai người khổng lồ:** Cú hích lớn nhất của Ellison là giành được hợp đồng xây dựng cơ sở dữ liệu cho CIA. Hiệu ứng bầy đàn lập tức kích hoạt: Khi CIA đã tin dùng hệ thống của bạn, toàn bộ khối chính phủ và doanh nghiệp sẽ tự động xuống tiền mà không mảy may nghi ngờ.

Các đối thủ ngây thơ cứ thế rụng dần. Ingress lụi tàn vì kĩ sư không biết làm business. Sybase từng gầm gừ thách thức bằng kiến trúc client-server, nhưng lại chọn nước cờ sai khi bắt tay với Microsoft làm SQL Server - tự tay nuôi lớn một con quái vật sau này nuốt chửng luôn thị phần của mình.

## 2.4. Oracle - Dọn dẹp chiến trường

Nhiều năm sau, khi Internet bùng nổ, MySQL nổi lên như một thách thức khổng lồ mang ngọn cờ "Mã nguồn mở".

Bản năng sinh tồn tàn nhẫn của Oracle trỗi dậy. Khác với IBM rụt rè năm xưa, Larry Ellison hiểu rõ mối đe dọa. Năm 2010, Oracle gây sốc khi chi 7,4 tỷ USD mua đứt Sun Microsystems - công ty mẹ đang nắm giữ MySQL. Mua lại không phải để phát triển, mà mua lại để kiểm soát hệ sinh thái và triệt tiêu rủi ro.

Sẽ có người đọc đến đây và bĩu môi nói Larry Ellison là kẻ cơ hội, chơi bẩn, còn IBM thì quá bảo thủ. Technically thì đúng là vậy. Nhưng nhìn rộng ra lớp cơ chế hệ thống, câu chuyện này phơi bày một góc khuất nghiệt ngã của thế giới công nghệ: Dữ liệu, thuật toán hay một cái paper đột phá như của Codd thực chất mới chỉ là hạt giống. Cách bạn phân phối nó, chiến lược định giá, và khả năng chốt sale mới là mảnh đất để hạt giống đó bùng nổ thành một đế chế.

## 2.5. PostgreSQL - Di sản cộng đồng

Nếu dừng ở đây thì có lẽ nhìn thị trường database có vẻ hơi đen tối, bạo chúa Oracle thống trị và làm tiền khắp thị trường. Tuy nhiên, một cái tên khác đã dần vươn lên hàng ghế đầu và làm bức tranh trở nên sáng sủa hơn. Đó chính là database mã nguồn mở Postgres. 

Postgres không xuất hiện từ hư không. Nó được phát triển bởi giáo sư Michael Stonebraker tại UC Berkeley năm 1986, cha đẻ dự án Ingres (đối thủ đã thất bại trước Oracle trên thương trường ta nhắc phía trên). Không bán license cho doanh nghiệp như Oracle, Postgres phát triển trong môi trường đại học, mã nguồn được công khai, bất kỳ ai cũng có thể tải về, sử dụng và chỉnh sửa. Sau nhiều năm phát triển, nó được đổi tên thành PostgreSQL.

Postgres không thằng bởi đội sale hùng hậu, không ký những hợp đồng trăm triệu đô, không có một Larry Ellison cáo già đứng sau điều khiển. Postgres lớn lên từng chút một nhờ cộng đồng kỹ sư trên khắp thế giới. Khi Internet bùng nổ, hàng nghìn startup bắt đầu đặt câu hỏi: "Không đủ tiền mua Oracle thì sao?"

Câu trả lời thường là PostgreSQL.

Rồi startup lớn dần. Dữ liệu tăng dần. Lượng truy cập cũng tăng theo. Postgres dần len lỏi vào mọi ngõ ngách trong ngành công nghệ. Nửa thế kỷ sau bài báo của Codd, có lẽ PostgreSQL mới là hiện thân gần nhất của giấc mơ ban đầu mà ông theo đuổi. Ngày nay có lẽ giới kỹ sư đều đồng ý với nhau rằng Oracle là database của doanh nghiệp còn PostgreSQL là database cho kỹ sư. 

> [PostgreSQL - Wikipedia](https://en.wikipedia.org/wiki/PostgreSQL#Notable_users)

# 3. Kết

Cuộc cách mạng của Codd đã thành công ngoài sức tưởng tượng. Các cơ sở dữ liệu quan hệ đã phủ bóng toàn ngành công nghệ. Oracle biến nó thành một đế chế thương mại. PostgreSQL đưa nó thành tài sản chung của cộng đồng. Hàng triệu ứng dụng trên thế giới vận hành mỗi ngày dựa trên những ý tưởng được viết ra từ năm 1970.

Nhưng chiến thắng mới lại sinh ra một vấn đề mới.

Các cơ sở dữ liệu quan hệ được thiết kế để ghi nhận giao dịch. Chúng rất giỏi trả lời những câu hỏi vận hành như:
- Tài khoản A còn bao nhiêu tiền?
- Đơn hàng B đang ở trạng thái nào?
- Linh kiện C hiện nằm ở đâu?

Nhưng doanh nghiệp lại cần hỏi cả những câu mang tính chiến lược hơn:
- Doanh thu tháng này tăng hay giảm?
- Khách hàng nào mang lại nhiều lợi nhuận nhất?
- Xu hướng tiêu dùng đang thay đổi ra sao?

Database lúc này giống như một cỗ máy ghi chép khổng lồ. Nó nhớ mọi giao dịch, nhưng bất lực trong việc xâu chuỗi chúng thành một câu chuyện kinh doanh. Khi data bùng nổ, doanh nghiệp nhận ra họ ngập trong dữ liệu giao dịch nhưng lại đói tri thức để ra quyết định.

Ma sát của thực tại kinh doanh này tạo ra một lực đẩy độc nhất kéo hai cái tên Bill Inmon và Ralph Kimball bước lên sàn đấu và khai sinh ra Data Warehouse. Xin mời độc giả cùng đón đọc bài viết tiếp theo trong chuỗi bài về lịch sử Data Engineer:

> Bài 2: Khủng hoảng báo cáo: Khi cái máy ghi không biết đọc