
from openai import OpenAI

openai_api_key = 'sk-bloom-app-CAjHDM4W0FXLZlP5yVvgT3BlbkFJGeSaluzHcPr20animZV0'
client = OpenAI(
    api_key=openai_api_key,
)

training_file_jsonl = "sample_ft_data.jsonl"
model_to_train = "gpt-4o"

client.files.create(
  file=open(training_file_jsonl, "r"),
  purpose="fine-tune"
)

# Create a fine-tuning run
client.fine_tuning.jobs.create(
  training_file=training_file_jsonl,
  model=model_to_train,
)

