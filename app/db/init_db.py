from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.management.queries import QueryIndexManager
from app.core.config import settings

def create_indexes():
    cluster = Cluster(
        f"couchbase://{settings.COUCHBASE_SERVER}",
        ClusterOptions(
            PasswordAuthenticator(
                settings.COUCHBASE_USER, settings.COUCHBASE_PASSWORD
            )
        ),
    )
    bucket = cluster.bucket(settings.COUCHBASE_BUCKET)

    # Lấy QueryIndexManager từ cluster thay vì bucket
    query_manager: QueryIndexManager = cluster.query_indexes()

    # Create primary index
    query_manager.create_primary_index(
        settings.COUCHBASE_BUCKET,
        ignore_if_exists=True
    )

    # Create index on type field
    query_manager.create_index(
        settings.COUCHBASE_BUCKET,
        "idx_type", ["type"], ignore_if_exists=True
    )

    print("Indexes created successfully")

if __name__ == "__main__":
    create_indexes()