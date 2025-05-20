import pandas as pd
import re

def extract_contents(cell: str) -> list[str]:
    """
    Given a string like:
      "[{'role': 'left', 'content': 'Hello ...', 'timestamp': 123}, {...}]"
    return a list of the content strings, e.g.
      ["Hello ...", "..."]
    """
    # 1) strip off the wrapping double-quotes, if any
    s = cell.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    # 2) remove the outer [ ]
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1]
    # 3) split into each dict-like chunk
    items = re.split(r"\},\s*\{", s)
    contents = []
    for item in items:
        # look for the content field up to the next ', 'timestamp'
        m = re.search(r"'content':\s*'(.*?)(?=',\s*'timestamp')", item, flags=re.DOTALL)
        if m:
            contents.append(m.group(1))
    return contents

# ———————
# 1) Load your file (adjust path as needed)
df = pd.read_csv('huge1.csv', dtype=str)

# 2) Extract the content-only lists
df['contents'] = df['transcript'].apply(extract_contents)

# 3) Keep only the new column plus labels
out = df[['contents', 'labels']]

# 4) Save to a new CSV
out.to_csv('huge1_final.csv', index=False)
