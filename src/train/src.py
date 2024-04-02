import pandas as pd
from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments, sample_dataset

data = pd.read_csv("../../data/output_extraction/labeled_training_data.csv")

dataset = Dataset.from_pandas(data)

# Simulate the few-shot regime by sampling 8 examples per class
train_dataset = sample_dataset(dataset, label_column="label", num_samples=8)

eval_size = min(100, len(dataset) // 2)
test_size = len(dataset) - eval_size

eval_dataset = dataset.select(range(eval_size))
test_dataset = dataset.select(range(eval_size, eval_size + test_size))

model = SetFitModel.from_pretrained(
    "sentence-transformers/paraphrase-mpnet-base-v2",
    labels=["0", "1"],
)

args = TrainingArguments(
    output_dir="output",
    report_to="none",
    batch_size=16,
    num_epochs=4,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    metric="accuracy",
    column_mapping={"text": "text", "label": "label"}
)

# Train and evaluate
trainer.train()
metrics = trainer.evaluate(test_dataset)
print(f"Evaluation metrics: {metrics}")