import socket
import pickle  # For deserializing the data from the client
import jwt
import threading
import json
import requests
from protobuf_decoder.protobuf_decoder import Parser
import time
import base64
from datetime import datetime
import re
from google.protobuf.timestamp_pb2 import Timestamp
from xxx import *
def process_client_data(client_socket):
    try:
        # Receive the serialized data from the client
        serialized_data = client_socket.recv(4096)
        print("Received data from client.")
    except Exception as e:
        print(f"Error receiving data: {e}")
        return

    try:
        # Deserialize the data
        data = pickle.loads(serialized_data)
        print("Data deserialized successfully.")
    except Exception as e:
        print(f"Error deserializing data: {e}")
        return

    try:
        token = data['token']
        key = data['key']
        iv = data['iv']
        timestamp = data['Timestamp']
        print(f"Extracted token, key, iv, and timestamp from data.")
    except KeyError as e:
        print(f"Missing expected key in data: {e}")
        return
    except Exception as e:
        print(f"Error extracting data: {e}")
        return

    try:
        # Decode and process the token
        decoded = jwt.decode(token, options={"verify_signature": False})
        account_id = decoded.get('account_id')
        encoded_acc = hex(account_id)[2:]
        hex_value = dec_to_hex(timestamp)
        time_hex = hex_value
        BASE64_TOKEN_ = token.encode().hex()
        print(f"Token decoded and processed. Account ID: {account_id}")
    except Exception as e:
        print(f"Error processing token: {e}")
        return

    try:
        head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]

        # Handle the encoded account ID length and add leading zeros as needed
        length = len(encoded_acc)
        zeros = '00000000'  # Default value

        if length == 9:
            zeros = '0000000'
        elif length == 8:
            zeros = '00000000'
        elif length == 10:
            zeros = '000000'
        elif length == 7:
            zeros = '000000000'
        else:
            print('Unexpected length encountered')
        
        # Construct the final token
        head = f'0115{zeros}{encoded_acc}{time_hex}00000{head}'
        final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
        print("Final token constructed successfully.")
    except Exception as e:
        print(f"Error constructing final token: {e}")
        return

    try:
        # Send the processed token back to the client
        client_socket.sendall(final_token.encode())
        print("Processed token sent to client.")
    except Exception as e:
        print(f"Error sending data to client: {e}")

# Example server setup
def start_server(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((ip, port))
            server_socket.listen()

            print(f'Server started on {ip}:{port}')
            
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f'Connected by {addr}')
                    with client_socket:
                        process_client_data(client_socket)
                except Exception as e:
                    print(f"Error handling client connection: {e}")
    except Exception as e:
        print(f"Error starting server: {e}")

# Start the server
start_server('0.0.0.0', 7300)
