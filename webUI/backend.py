from flask import Flask, jsonify, request

from flask_cors import CORS
import argparse
import json
import os
import forecast2

app = Flask(__name__)

CORS(app)

# Simulated database
data_store = {}

@app.route('/greet', methods=['GET'])
def greet():
    # 

    name = request.args.get('name', 'World')
    print(name)
    reponditem = jsonify({"message": f"Hello, {name}!"})
    print("reponditem", reponditem, type(reponditem))

    
    try:
        parsedInput = json.loads(name)
        print(parsedInput)

        quoteVal = forecast2.getQuotes(parsedInput)
        print(quoteVal)

        return jsonify({"message": f"Given your input {parsedInput}, your excpected quote for regular policy={quoteVal}$, for high deductible the cost is {quoteVal*0.6}."})

    except Exception as e:

        print(f"Error: {e}")
        sampleText = '{"Name": "Bob", "Age": 2, "Smokes": "No", "Drinks" "Alcohol": "No", "Exercises Irregularly": "Yes",  "Sleeps Late": "Yes", Diet Irregularity: Yes,   Emotionally Unstable: No }'
        return jsonify({"message": f"Hello, please enter correct input format  for example{sampleText}!"})


    


@app.route('/get', methods=['GET'])
def get_value():
    # work
    key = request.args.get('key')
    value = data_store.get(key, "Not found")
    return jsonify({key: value})


@app.route('/insert', methods=['POST'])
def insert_value():
    # work
    key = request.json.get('key')
    value = request.json.get('value')
    data_store[key] = value
    return jsonify({"message": f"Inserted key: {key} with value: {value}"})


@app.route('/update', methods=['PUT'])
def update_value():
    key = request.json.get('key')
    value = request.json.get('value')
    if key in data_store:
        data_store[key] = value
        return jsonify({"message": f"Updated key: {key} with value: {value}"})
    else:
        return jsonify({"message": "Key not found"}), 404


# AWS S3 connection
def list_my_buckets(s3_resource):
    print("Buckets:\n\t", *[b.name for b in s3_resource.buckets.all()], sep="\n\t")


def create_and_delete_my_bucket(s3_resource, bucket_name, keep_bucket):
    list_my_buckets(s3_resource)

    try:
        print("\nCreating new bucket:", bucket_name)
        bucket = s3_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": s3_resource.meta.client.meta.region_name
            },
        )
    except ClientError as e:
        print(
            f"Couldn't create a bucket for the demo. Here's why: "
            f"{e.response['Error']['Message']}"
        )
        raise

    bucket.wait_until_exists()
    list_my_buckets(s3_resource)

    if not keep_bucket:
        print("\nDeleting bucket:", bucket.name)
        bucket.delete()

        bucket.wait_until_not_exists()
        list_my_buckets(s3_resource)
    else:
        print("\nKeeping bucket:", bucket.name)





if __name__ == '__main__':
    cursor, conn = False, False

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true')
    parser.add_argument("db_host", nargs=1, default=os.getcwd(), help="Database host name.")
    parser.add_argument("db_name", nargs=1, default=os.getcwd(), help="Database table name.")
    parser.add_argument("db_user", nargs=1, default=os.getcwd(), help="User name")
    parser.add_argument("db_password", nargs=1, default=os.getcwd(), help="aws password")

    # Establish a connection to the database
    try:




        # SQL query to fetch data
        sql_query = 'SELECT * FROM your_table_name'

        # Local file path to save the downloaded data
        local_file_path = 'local/path/to/save/data.csv'
        args = parser.parse_args()
        conn = psycopg2.connect(
            host=args.db_host,
            database=args.db_name,
            user=args.db_user,
            password=args.db_password
        )
        print("Connected to the database")

        # Create a cursor
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all the data
        data = cursor.fetchall()

        # Save the data to a local file (e.g., CSV)
        with open(local_file_path, 'w') as f:
            for row in data:
                f.write(','.join(map(str, row)) + '\n')

        print(f"Data downloaded successfully to {local_file_path}")

    except Exception as e:
        print("error while loading from aws")
        print(f"Error: {e}")

    finally:
            # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        else:
            print("\n Error ! cloud connection failed using local file \n")




        print("starting")
        
        # load data
        # connect to AWS remote db using try except
        # try load data from AWS
        # run ML model against AWS data

        # if except catch
        # loadCSV (previously learned result is stored in CSV)
        # put ML result in right variable for display


        app.run(host='0.0.0.0', port=80)






