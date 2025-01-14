# Bookstore API

Đây là một project API đơn giản sử dụng FastAPI và Couchbase để quản lý sách.

## Mô tả

Project này cung cấp các API cơ bản để:

* Đăng ký và đăng nhập người dùng.
* Thêm, sửa, xóa và xem thông tin sách.
* Hiển thị danh sách sách dưới dạng bảng, có phân trang, tìm kiếm (sử dụng DataTables).
* Frontend đơn giản sử dụng Bootstrap 5.

## Yêu cầu

* Python 3.11+
* Couchbase Server 7.0+
* Đã cài đặt các thư viện trong file `requirements.txt`

## Cài đặt

1. **Cài đặt Couchbase Server:**
    * Tạo container Couchbase Server

    ```bash
        docker network create --driver bridge couchbase-network
        docker run --name couchbase-node1 --network couchbase-network --hostname couchbase-node1.local -p 8091-8096:8091-8096 -p 11210:11210 couchbase/server:community
        docker run --name couchbase-node2 --network couchbase-network --hostname couchbase-node2.local -p 8097-8102:8091-8096 -p 11211:11210 couchbase/server:community
        docker run -it -p 8000:8000 --name ubuntu-app --network couchbase-network ubuntu:22.04
    ```

    * Sau khi cài đặt, tạo một bucket tên là `bookstore`.
2. **Clone repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

3. **Cài đặt các thư viện cần thiết:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Cấu hình file `.env`:**

    * Tạo file `.env` trong thư mục gốc của project.
    * Thêm các thông tin sau vào file `.env` (thay đổi giá trị cho phù hợp):

        ```
        PROJECT_NAME="Bookstore API"
        API_V1_STR="/api/v1"
        COUCHBASE_USER=giangpt
        COUCHBASE_PASSWORD=123456
        COUCHBASE_CONNECTION_STRING=couchbase://172.19.0.2
        COUCHBASE_BUCKET=bookstore
        SECRET_KEY=your-secret-key # Thay bằng secret key của bạn
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30
        ```

5. **Tạo index trong Couchbase:**

    ```bash
    python app/db/init_db.py
    ```

## Chạy ứng dụng

```bash
uvicorn app.main:app --reload --host 0.0.0.0
