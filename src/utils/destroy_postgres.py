#!/usr/bin/env python3
"""
Script to destroy all tables in the public schema of the agri_kb PostgreSQL database.
This script will permanently delete all data and tables - use with caution!
"""

import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def get_connection_params():
    """Get database connection parameters from environment or use defaults"""
    import os

    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "database": os.getenv("POSTGRES_DATABASE", "agri_kb"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    }


def confirm_destruction():
    """Ask for confirmation before destroying the database"""
    print(
        "⚠️  WARNING: This script will permanently delete ALL tables in the public schema!"
    )
    print("📊 Database: agri_kb")
    print("🏗️  Schema: public")
    print()

    response = input(
        "Are you absolutely sure you want to continue? Type 'DESTROY' to confirm: "
    )
    if response != "DESTROY":
        print("❌ Operation cancelled.")
        sys.exit(0)

    print("✅ Confirmation received. Proceeding with destruction...")


def get_all_tables(conn):
    """Get all table names in the public schema"""
    cursor = conn.cursor()

    # Query to get all tables in public schema
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """

    cursor.execute(query)
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return tables


def destroy_tables(conn, tables):
    """Drop all tables in the database"""
    cursor = conn.cursor()

    print(f"🗑️  Found {len(tables)} tables to destroy:")
    for table in tables:
        print(f"   - {table}")

    print("\n🔥 Starting table destruction...")

    # Disable foreign key checks temporarily
    cursor.execute("SET session_replication_role = replica;")

    destroyed_count = 0
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"✅ Destroyed table: {table}")
            destroyed_count += 1
        except Exception as e:
            print(f"❌ Failed to destroy table {table}: {e}")

    # Re-enable foreign key checks
    cursor.execute("SET session_replication_role = DEFAULT;")

    cursor.close()
    return destroyed_count


def main():
    """Main function"""
    print("🗄️  PostgreSQL Database Destruction Script")
    print("=" * 50)

    # Get connection parameters
    params = get_connection_params()

    print(f"🔗 Connecting to database: {params['database']}")
    print(f"🏠 Host: {params['host']}:{params['port']}")
    print(f"👤 User: {params['user']}")
    print()

    # Confirm before proceeding
    confirm_destruction()

    try:
        # Connect to the database
        conn = psycopg2.connect(**params)  # type: ignore
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        print("✅ Connected to database successfully!")

        # Get all tables
        tables = get_all_tables(conn)

        if not tables:
            print("ℹ️  No tables found in public schema.")
            return

        # Destroy all tables
        destroyed_count = destroy_tables(conn, tables)

        print("\n🎉 Destruction completed!")
        print(f"📊 Total tables destroyed: {destroyed_count}/{len(tables)}")

        # Verify all tables are gone
        remaining_tables = get_all_tables(conn)
        if not remaining_tables:
            print("✅ All tables successfully removed from public schema!")
        else:
            print(f"⚠️  Warning: {len(remaining_tables)} tables still remain:")
            for table in remaining_tables:
                print(f"   - {table}")

        conn.close()

    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
