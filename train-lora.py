#!/bin/env python3
import unsloth # seems like it needs to load before anyone
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset, concatenate_datasets
from unsloth import is_bfloat16_supported
import numpy as np

# check CUDA support
print(torch.cuda.get_device_name(0))
print(torch.cuda.is_available())

model_name = "Qwen/Qwen3-8b"
json_dataset_path = "raw_data/training-prompts.json"
text_dataset_path = "raw_data/zig-0.14.0-docs.md"
text2_dataset_path = "raw_data/zig-0.14.0-release-notes.md"
text3_dataset_path = "raw_data/zig_docs_with_filenames.txt"
text4_dataset_path = "raw_data/zig_cookbook_chat.txt"
text5_dataset_path = "raw_data/zig_stdlib_concat.txt"

# Load base model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name,
    use_fast=False,
    trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16, # Can try float16 if you face issues
    #device_map="auto", 
    trust_remote_code=True
)
model = model.to("cuda")

# Setup LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Common for Qwen/Llama/transformers
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Prepare HuggingFace dataset for text
text5_dataset = load_dataset("text", data_files={"train": text5_dataset_path})['train']
text4_dataset = load_dataset("text", data_files={"train": text4_dataset_path})['train']
text3_dataset = load_dataset("text", data_files={"train": text3_dataset_path})['train']
text2_dataset = load_dataset("text", data_files={"train": text2_dataset_path})['train']
text_dataset = load_dataset("text", data_files={"train": text_dataset_path})['train']
json_dataset = load_dataset("text", data_files={"train": json_dataset_path})['train']

# oversample the prompts to try to influence the bias towards this new documentation
N = 100  # Oversampled target size
indices = np.random.choice(len(json_dataset), size=N, replace=True)
oversampled_ds = json_dataset.select(indices)
# text5 (std) won't fit in the 4090 so removed from combined
combined_dataset = concatenate_datasets([text_dataset, text2_dataset, text3_dataset, text4_dataset, oversampled_ds])

# Tokenize your dataset FIRST:
def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, padding=True)

tokenized_dataset = combined_dataset.map(tokenize_function, batched=True)

# Training hyperparameters
training_args = SFTConfig(
    output_dir = "qwen3-zig-lora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps = 5,
    num_train_epochs = 5, # Set this for 1 full training run.
    #max_steps = 60,
    learning_rate = 2e-4,
    fp16 = not is_bfloat16_supported(),
    bf16 = is_bfloat16_supported(),
    optim = "adamw_8bit",
    weight_decay = 0.01,
    lr_scheduler_type = "linear",
    seed = 3407,
    report_to = "none",
    max_seq_length = 2048,
    dataset_num_proc = 4,
    packing = False, # Can make training 5x faster for short sequences.
)

# Trainer for unsupervised SFT
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    processing_class=tokenizer,
)
trainer.train()
model.save_pretrained("qwen3-zig-lora")
tokenizer.save_pretrained("qwen3-zig-lora")
