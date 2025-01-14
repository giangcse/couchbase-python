Tôi hiểu rằng bạn muốn thao tác tạo scope, collection, và index trực tiếp trên giao diện web của Couchbase, thay vì phải viết code. Điều này hoàn toàn có thể thực hiện được thông qua **Couchbase Web Console**.

**Couchbase Web Console**

Couchbase Web Console là một giao diện web cung cấp đầy đủ các công cụ để quản lý và thao tác trên Couchbase Server. Bạn có thể sử dụng giao diện này để:

* **Tạo Bucket:** Bạn đã tạo bucket "bookstore" trong các bước trước.
* **Tạo Scope:** Bạn có thể tạo các scope như "bookscope" và "userscope".
* **Tạo Collection:** Bạn có thể tạo các collection như "books" và "users" trong các scope tương ứng.
* **Tạo Index:** Bạn có thể tạo primary index, index trên type field và FTS index.

**Cách sử dụng Couchbase Web Console:**

1. **Truy cập Web Console:** Mở trình duyệt web và truy cập vào Couchbase Web Console theo địa chỉ: `http://<couchbase-server-ip>:8091` (thay `<couchbase-server-ip>` bằng địa chỉ IP của server Couchbase của bạn, nếu bạn cài đặt trên máy của bạn thì dùng địa chỉ `127.0.0.1`).
2. **Đăng nhập:** Đăng nhập vào Couchbase Web Console bằng thông tin tài khoản admin bạn đã thiết lập khi cài đặt Couchbase Server.
3. **Chọn Bucket:** Chọn bucket `bookstore` từ danh sách bucket.
4. **Tạo Scope:**
    * Click vào tab **Scopes**.
    * Click vào **Add Scope**.
    * Nhập tên scope (ví dụ: `bookscope`), chọn **Add Scope**.
    * Thực hiện tương tự để tạo scope `userscope`.
5. **Tạo Collection:**
    * Chọn scope `bookscope` vừa tạo.
    * Click vào tab **Collections**.
    * Click vào **Add Collection**.
    * Nhập tên collection (ví dụ: `books`) và chọn **Add Collection**.
    * Chọn scope `userscope` và thực hiện tương tự để tạo collection `users`.
6. **Tạo Index:**
    * Click vào tab **Query** để mở Query Editor.
    * **Tạo Primary Index:** Gõ các lệnh sau và nhấn **Execute**.
        * `CREATE PRIMARY INDEX ON`bookstore`.bookscope.books`
        * `CREATE PRIMARY INDEX ON`bookstore`.userscope.users`
    * **Tạo Index Trên Type Field:** Gõ các lệnh sau và nhấn **Execute**.
         * `CREATE INDEX idx_type ON`bookstore`.bookscope.books(type)`
         * `CREATE INDEX idx_type ON`bookstore`.userscope.users(type)`
    * **Tạo FTS Index:**

        * Chọn menu **Search**.
        * Chọn **Indexes**.
        * Chọn **Add Index**.
        * Chọn bucket `bookstore`.
        * Nhập tên index: `idx_fts_books`.
        * Ở phần Mapping, chọn scope: `bookscope` và Collection `books`
         * Ở phần Mapping, chọn các trường `description`, `summary`, `title`, `author`
         * Chọn **Add Index**
         * Chờ đợi Couchbase tạo index

**Lợi ích:**

* **Giao diện trực quan:** Dễ dàng thao tác và xem các cấu hình.
* **Không cần code:** Bạn không cần viết code Python để tạo các cấu trúc cơ bản.
* **Dễ quản lý:** Bạn có thể quản lý scope, collection và index tập trung tại một nơi.

**Lưu ý:**

* **Tài khoản Admin:** Bạn cần đăng nhập bằng tài khoản admin để có quyền thực hiện các thao tác này.
* **Tạo index FTS:** Việc tạo FTS index có thể mất chút thời gian để Couchbase xây dựng index. Bạn nên làm việc này khi khởi tạo database, không nên tạo index thường xuyên.

**Thay đổi code:**

Bạn có thể bỏ phần code tạo scope, collection, index trong `init_db.py`. Thay vào đó, bạn chỉ cần code tạo connection, có thể sửa lại `app/db/session.py` như sau:

```python
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import CBCollection
from app.core.config import settings

# Tạo đối tượng Authenticator trước
authenticator = PasswordAuthenticator(
    settings.COUCHBASE_USER,
    settings.COUCHBASE_PASSWORD
)

# Sau đó, sử dụng authenticator để tạo ClusterOptions
cluster_options = ClusterOptions(authenticator)

# Cuối cùng, sử dụng cluster_options khi khởi tạo Cluster
cluster = Cluster(
    f"couchbase://{settings.COUCHBASE_CONNECTION_STRING}",
    cluster_options,
)
bucket = cluster.bucket(settings.COUCHBASE_BUCKET)

# Lấy scope
bookscope = bucket.scope('bookscope')
userscope = bucket.scope('userscope')

# Lấy collection
bookcollection = bookscope.collection('books')
usercollection = userscope.collection('users')

def get_book_collection() -> CBCollection:
    # Trả về collection books đã được khởi tạo
    return bookcollection
def get_user_collection() -> CBCollection:
    # Trả về collection users đã được khởi tạo
    return usercollection
```

**Tóm lại:**

Bạn có thể quản lý các cấu trúc cơ bản trên Couchbase (bucket, scope, collection, index) thông qua Couchbase Web Console. Cách này trực quan và dễ dàng hơn là viết code, đặc biệt khi bạn chỉ cần thiết lập một lần.

Tôi hy vọng rằng điều này sẽ giúp ích cho bạn. Nếu bạn có bất kỳ câu hỏi nào khác, đừng ngần ngại cho tôi biết.
