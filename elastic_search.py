import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from elasticsearch import Elasticsearch, exceptions
import pandas as pd
import numpy as np

# Function to execute when the Submit button is clicked
def submit():
    es_host = host_entry.get()
    es_port = port_entry.get()
    index_name = index_entry.get()
    column_name = column_entry.get()

    # Input validation
    if not es_host or not es_port or not index_name or not column_name:
        messagebox.showerror("Error", "Please fill in all input fields.")
        return

    try:
        port = int(es_port)
    except ValueError:
        messagebox.showerror("Error", "Invalid port number. Please enter a valid integer.")
        return

    try:
        # Set up Elasticsearch connection
        es = Elasticsearch([f'http://{es_host}:{es_port}'])

        # Test connection
        if not es.ping():
            messagebox.showerror("Error", "Cannot connect to Elasticsearch. Please check the host and port.")
            return

        # Create an Elasticsearch query
        query = {
            "size": 1000,  # Maximum number of results to fetch
            "query": {
                "match_all": {}  # Match all documents, replace this with your specific query
            }
        }

        # Fetch data from Elasticsearch
        response = es.search(index=index_name, body=query)

        # Extract the data from the response
        data = [hit['_source'] for hit in response['hits']['hits']]

        # Analyze data using Python
        df = pd.DataFrame(data)

        # Perform some basic analysis, such as finding the mean of a specific column
        if column_name not in df.columns:
            messagebox.showerror("Error", f"Column '{column_name}' not found in the index.")
            return

        mean_value = df[column_name].mean()

        messagebox.showinfo("Result", f"The mean value of the column '{column_name}' is: {mean_value}")
    except exceptions.NotFoundError:
        messagebox.showerror("Error", f"Index '{index_name}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Elasticsearch Data Analyzer")

# Create and place input fields and labels
host_label = ttk.Label(root, text="Elasticsearch Host:")
host_label.grid(row=0, column=0)
host_entry = ttk.Entry(root)
host_entry.grid(row=0, column=1)

port_label = ttk.Label(root, text="Elasticsearch Port:")
port_label.grid(row=1, column=0)
port_entry = ttk.Entry(root)
port_entry.grid(row=1, column=1)

index_label = ttk.Label(root, text="Index Name:")
index_label.grid(row=2, column=0)
index_entry = ttk.Entry(root)
index_entry.grid(row=2, column=1)

column_label = ttk.Label(root, text="Column Name:")
column_label.grid(row=3, column=0)
column_entry = ttk.Entry(root)
column_entry.grid(row=3, column=1)

# Create and place the Submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=4, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
