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