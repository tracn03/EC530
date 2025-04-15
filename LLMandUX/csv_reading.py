import pandas as pd
import sqlite3
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='error_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def inspect_csv_structure(csv_path):
    """Inspect CSV file structure and return column information"""
    df = pd.read_csv(csv_path)
    
    # Get column information
    column_info = []
    for column in df.columns:
        dtype = df[column].dtype
        # Map pandas dtypes to SQLite types
        if pd.api.types.is_integer_dtype(dtype):
            sql_type = 'INTEGER'
        elif pd.api.types.is_float_dtype(dtype):
            sql_type = 'REAL'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            sql_type = 'TIMESTAMP'
        else:
            sql_type = 'TEXT'
            
        column_info.append({
            'name': column,
            'pandas_dtype': str(dtype),
            'sql_type': sql_type
        })
    
    return column_info

def generate_create_table_sql(table_name, column_info):
    """Generate CREATE TABLE SQL statement based on column information"""
    column_definitions = []
    for col in column_info:
        # Replace spaces and special characters in column names
        safe_column_name = f'"{col["name"]}"'
        column_definitions.append(f'{safe_column_name} {col["sql_type"]}')
    
    sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {',\n        '.join(column_definitions)}
    )
    '''
    return sql

def get_existing_schema(cursor, table_name):
    """Get existing table schema using PRAGMA table_info"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    if not columns:
        return None
    
    schema_info = {}
    for col in columns:
        # PRAGMA table_info returns: (id, name, type, notnull, default_value, pk)
        schema_info[col[1]] = col[2]  # col[1] is name, col[2] is type
    return schema_info

def handle_schema_conflict(existing_schema, new_column_info, table_name):
    """Handle schema conflicts with user interaction"""
    print("\nSchema conflict detected!")
    print("\nExisting schema:")
    for col_name, col_type in existing_schema.items():
        print(f"  {col_name}: {col_type}")
    
    print("\nNew schema:")
    for col in new_column_info:
        print(f"  {col['name']}: {col['sql_type']}")
    
    while True:
        choice = input("\nHow would you like to proceed?\n"
                      "1. Overwrite existing table\n"
                      "2. Create new table with timestamp\n"
                      "3. Skip import\n"
                      "Enter choice (1-3): ")
        
        if choice == '1':
            return table_name, True
        elif choice == '2':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_table_name = f"{table_name}_{timestamp}"
            return new_table_name, True
        elif choice == '3':
            return table_name, False
        else:
            print("Invalid choice. Please try again.")

def create_database_dynamic(csv_path, table_name='sheet_data'):
    """Create database with dynamic schema based on CSV structure"""
    try:
        # Inspect CSV structure
        column_info = inspect_csv_structure(csv_path)
        
        # Connect to database
        conn = sqlite3.connect('spreadsheet.db')
        cursor = conn.cursor()
        
        # Check existing schema
        existing_schema = get_existing_schema(cursor, table_name)
        
        if existing_schema:
            # Handle schema conflict
            table_name, should_proceed = handle_schema_conflict(
                existing_schema, column_info, table_name
            )
            if not should_proceed:
                logging.info(f"Import skipped for {csv_path} due to user choice")
                return None
        
        # Generate and execute CREATE TABLE statement
        create_table_sql = generate_create_table_sql(table_name, column_info)
        logging.info(f"Creating table {table_name} with schema:\n{create_table_sql}")
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        return table_name
    
    except Exception as e:
        logging.error(f"Error in create_database_dynamic: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def load_csv_to_sqlite(csv_path, table_name='sheet_data'):
    try:
        # Read CSV file using pandas
        df = pd.read_csv(csv_path)
        
        # Connect to the database
        conn = sqlite3.connect('spreadsheet.db')
        
        # Write the dataframe to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Successfully loaded {len(df)} rows into {table_name}")
        
    except Exception as e:
        logging.error(f"Error in load_csv_to_sqlite: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def run_sample_queries(table_name='sheet_data'):
    conn = sqlite3.connect('spreadsheet.db')
    cursor = conn.cursor()
    
    # Get table info
    print("Table Structure:")
    cursor.execute(f"PRAGMA table_info({table_name})")
    print(cursor.fetchall())
    
    # Sample query 1: Select all records
    print("\nFirst 5 records:")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    print(cursor.fetchall())
    
    # Sample query 2: Count total records
    print("\nTotal number of records:")
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    print(cursor.fetchone()[0])
    
    conn.close()

def list_tables():
    """List all tables in the database"""
    try:
        conn = sqlite3.connect('spreadsheet.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name;
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in the database.")
            return
        
        print("\nAvailable tables:")
        for table_name, create_sql in tables:
            print(f"\n{table_name}:")
            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
    
    except Exception as e:
        logging.error(f"Error listing tables: {str(e)}")
        print("Error listing tables. Check error_log.txt for details.")
    finally:
        if 'conn' in locals():
            conn.close()

def execute_custom_query(query):
    """Execute a custom SQL query and display results"""
    try:
        conn = sqlite3.connect('spreadsheet.db')
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # If the query returns results, fetch and display them
        if cursor.description is not None:
            # Get column names
            columns = [description[0] for description in cursor.description]
            print("\nColumns:", columns)
            
            # Fetch and print results
            results = cursor.fetchall()
            print("\nResults:")
            for row in results:
                print(row)
            print(f"\nTotal rows: {len(results)}")
        else:
            print("Query executed successfully (no results to display)")
        
        conn.commit()
    
    except Exception as e:
        logging.error(f"Query execution error: {str(e)}")
        print(f"Error executing query: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

def chat_interface():
    """Interactive chat-like interface for database operations"""
    print("\nWelcome to the CSV-SQL Chat Interface!")
    
    while True:
        print("\nAvailable commands:")
        print("1. Load a CSV file")
        print("2. List all tables")
        print("3. Run a custom SQL query")
        print("4. Exit")
        
        choice = input("\nWhat would you like to do? (Enter 1-4): ").strip()
        
        if choice == '1':
            # Load CSV file
            csv_path = input("\nEnter the path to your CSV file: ").strip()
            csv_file = Path(csv_path)
            
            if csv_file.exists():
                table_name = create_database_dynamic(csv_file)
                if table_name:
                    load_csv_to_sqlite(csv_file, table_name)
                    print(f"\nSuccessfully loaded {csv_path} into table '{table_name}'")
            else:
                print(f"File not found: {csv_path}")
        
        elif choice == '2':
            # List tables
            list_tables()
        
        elif choice == '3':
            # Run custom query
            print("\nEnter your SQL query (press Enter twice to execute):")
            query_lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                query_lines.append(line)
            
            query = " ".join(query_lines)
            if query.strip():
                execute_custom_query(query)
            else:
                print("Empty query. Please try again.")
        
        elif choice == '4':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        chat_interface()
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        print(f"An error occurred. Check error_log.txt for details.")

