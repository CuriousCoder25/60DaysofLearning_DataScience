# Day 3: Data Collections - Mastering Python Lists

# 1. Creating a list of data metrics (Floats and Strings)
data_metrics = [1.5, 3.2, 4.8, 2.1, 5.0]
modules = ["Ingestion", "Cleaning", "Modeling"]

print("Initial Data Metrics:", data_metrics)

# 2. Accessing data using Indexing and Slicing
first_metric = data_metrics[0]
subset_metrics = data_metrics[1:4] # Grabs index 1, 2, and 3

print(f"First Metric: {first_metric}")
print(f"Slicing Example (Index 1 to 3): {subset_metrics}")

# 3. Modifying the list (Mutability)
data_metrics.append(6.4) # Adding new data to the end
modules[1] = "Data_Wrangling" # Updating an existing element

print("Updated Metrics (After Append):", data_metrics)
print("Updated Modules (After Modification):", modules)