import yaml

with open("prompts/v001.yaml", "r") as v:
    data = yaml.safe_load(v)

version= data['version']
date = data['created_at']
prompt = data['system_prompt']

print(f"Version : {version}")
print(f"\nDate : {date}")
print(f"\nSystem Propmt : {prompt}")