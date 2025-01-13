from couchbase.cluster import Cluster, ClusterOptions
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
collection = bucket.default_collection()

def get_db_collection() -> CBCollection:
    return collection