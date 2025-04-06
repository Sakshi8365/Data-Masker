import os
import pandas as pd
from masker import mask_text

def process_txt(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    redacted = mask_text(content)
    print(f"\n🔐 Redacted Text from {file_path}:\n")
    print(redacted)

def process_csv(file_path):
    df = pd.read_csv(file_path)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(lambda x: mask_text(x) if isinstance(x, str) else x)
    print(f"\n🔐 Redacted CSV from {file_path}:\n")
    print(df.to_string(index=False))


file_list = ["test_text.txt", "sample_data.csv"] #for both files


for file_path in file_list:
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue

    ext = os.path.splitext(file_path)[1]

    if ext == ".txt":
        process_txt(file_path)
    elif ext == ".csv":
        process_csv(file_path)
    else:
        print(f"❌ Unsupported file type: {file_path}")
# import os
# import pandas as pd
# from masker import mask_text

# def process_txt(file_path):
#     with open(file_path, "r") as f:
#         content = f.read()
#     return mask_text(content)

# def process_csv(file_path):
#     df = pd.read_csv(file_path)
#     for col in df.columns:
#         if df[col].dtype == "object":
#             df[col] = df[col].apply(lambda x: mask_text(x) if isinstance(x, str) else x)
#     return df

# #  CHANGE The file
# file_path = "test_text.txt"  # OR "sample_data.csv"
# 

# ext = os.path.splitext(file_path)[1]

# if ext == ".txt":
#     result = process_txt(file_path)
#     print("🔐 Redacted Text:\n")
#     print(result)

# elif ext == ".csv":
#     result = process_csv(file_path)
#     print("🔐 Redacted CSV:\n")
#     print(result.to_string(index=False))

# else:
#     print("❌ Unsupported file type. Use .txt or .csv")
