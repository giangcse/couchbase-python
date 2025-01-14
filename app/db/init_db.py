from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.management.queries import QueryIndexManager
from app.core.config import settings
from couchbase.management.buckets import BucketManager
# from couchbase.exceptions import ScopeExistsException, CollectionExistsException
from couchbase.options import CreateScopeOptions, CreateCollectionOptions


def create_indexes():
    cluster = Cluster(
        f"couchbase://{settings.COUCHBASE_CONNECTION_STRING}",
        ClusterOptions(
            PasswordAuthenticator(
                settings.COUCHBASE_USER, settings.COUCHBASE_PASSWORD
            )
        ),
    )
    bucket = cluster.bucket(settings.COUCHBASE_BUCKET)

    bucket_manager: BucketManager = cluster.buckets()
    # Create scope
    bucket_manager.create_scope("bookscope", CreateScopeOptions())
    print("Scope 'bookscope' already exists.")
    bucket_manager.create_scope("userscope", CreateScopeOptions())
    print("Scope 'userscope' already exists.")

# Create collection
    bookscope = bucket.scope("bookscope")
    bookscope.create_collection("books", CreateCollectionOptions())
    print("Collection 'books' already exists in 'bookscope'.")

    userscope = bucket.scope("userscope")
    userscope.create_collection("users", CreateCollectionOptions())
    print("Collection 'users' already exists in 'userscope'.")

    query_manager: QueryIndexManager = cluster.query_indexes()

    # Create primary index
    query_manager.create_primary_index(
        settings.COUCHBASE_BUCKET, "books", "bookscope", ignore_if_exists=True
    )
    query_manager.create_primary_index(
        settings.COUCHBASE_BUCKET, "users", "userscope", ignore_if_exists=True
    )

    # Create index on type field
    query_manager.create_index(
        settings.COUCHBASE_BUCKET,
        "idx_type",
        ["type"],
        ignore_if_exists=True,
        scope_name="bookscope",
        collection_name="books",
    )
    query_manager.create_index(
        settings.COUCHBASE_BUCKET,
        "idx_type",
        ["type"],
        ignore_if_exists=True,
        scope_name="userscope",
        collection_name="users",
    )

    query_manager.create_fts_index(
        settings.COUCHBASE_BUCKET,
        'idx_fts_books', ['description', 'summary', 'title', 'author'], 
        ignore_if_exists=True
    )
    print("Indexes created successfully")

if __name__ == "__main__":
    create_indexes()