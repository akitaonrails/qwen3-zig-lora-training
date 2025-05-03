## Qwen3 Zig LoRa (Attempt - for education purposes only)

The usual cut off for training materials for the main LLMs used today, end in 2023. Zig, being an experimental and quickly evolving new language, changes abruptly all the time. Everyone only knows until version 0.11 or 0.12 or as far back as 0.10. But Zig is currently in version 0.14, which means no LLM can spit out new Zig code.

Simple prompting or RAGs won't solve this. So the only other solution is to try to train a lora.

The material is limited yet (PRs are welcome) and I am no expert in LLM training, so even the available material may note be in optimal formatting and organization.

Check out the `raw_data` directory for the test train material I gathered so far.

You can regenerate the `zig_docs_with_filenames.txt` running `concat-zig-docs.py`. Same for `zig_cookbook_chat.txt` with `concat-zig-cookbook.py`, and `zig_stdlib_concat.txt` with `concat-zig-std.py`. Before running that you have to add these:

```
git clone https://github.com/zigcc/zig-cookbook.git raw_data/zig-cookbook
git clone https://github.com/ziglang/zig.git raw_data/zig
```

Unfortunatelly, I was only able to try training on top of the Qwen3-8b model. Even in an RTX 4090, there is not enough VRAM for that.

I also had to comment out adding the Zig STD source code to the training. That alone is 15MB and also won't fit in my 4090. I did not try renting an A40 on RunPod yet. Feel free to test larger base models and more training material, and let us know.

Finally, run:

```
./train-lora.py
```

The resulting `qwen3-zig-lora` is 3.7GB large.

I wasn't able to run this with Ollama, you have to serve the HTTP API with vLLM instead:

```
vllm serve Qwen/Qwen3-8B \
    --enable-lora \
    --lora-modules ziglora=./qwen3-zig-lora \
    --max-model-len 8192
```

If you want to try with Aider, you connect like this:

```
OPENAI_API_BASE=http://localhost:8000/v1 aider --watch-files \
    --model hosted_vllm/ziglora \
    --reasoning-effort none \
    --verbose
```

But Aider won't play nice: the system prompt is too large for a small model with only 8k tokens sized context window. You will have to rely on tools such as `curl` to test:

```
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ziglora",
        "messages": [{"role": "user", "content": "Hello, which most recent version of the Zig language are you familiar with?"}]
      }' | jq
```

This is still very experimental and a work in progress. Help from people more used to train models is appreciated.
