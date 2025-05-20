import pandas as pd

def parse_list(s: str) -> list[str]:
    s = s.strip().lstrip('"').rstrip('"').strip()
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1]
    parts = s.split("', '")
    return [p.lstrip("'").rstrip("'") for p in parts]

df = pd.read_csv('huge2.csv', dtype=str)

# parse the two dialogue columns
df['left_list']  = df['left'].apply(parse_list)
df['right_list'] = df['right'].apply(parse_list)

# merge them and preserve labels
df['merged'] = df['left_list'] + df['right_list']

# keep only merged + labels (drop the old columns and intermediates)
out = df[['merged', 'labels']]

out.to_csv('huge2_final.csv', index=False)
