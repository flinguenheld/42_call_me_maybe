# 42_call_me_maybe
Does LLMs speak the language of computers? We’ll find out.

- Parameter: Variable in the prototype
- Argument: Value of a parameter

### Description

The purpose is to discover the [Function Calling System](https://developers.openai.com/api/docs/guides/function-calling).  

Given:
- A list of functions
- A plain text sentence

Ask a small LLM model to select the correct function and extract all arguments in JSON format.  

```json
User: "What is the sum of 40 and 2?"
Function Calling System:
{
"function": "add_numbers",
"arguments": {"a": 40, "b": 2}
}
```

### Example usage
<video controls align="center" src="https://github.com/user-attachments/assets/f753ad13-41d9-4391-80c5-b58739319632">
</video>

### Instructions
This project uses [UV](https://docs.astral.sh/uv/) for automatic virtual environment management.  
Once installed, you can use it with the Makefile with these commands:

```Bash
    make install
    make clean
    make lint
```
```Bash
  uv run python -m src [--functions_definition <function_definition_file>] \
                       [--input <input_file>] \
                       [--output <output_file>] \
                       [--model <[deepseek|lama|qwen]>]
```
Usage:
```Bash
    uv run python -m src --help
```
The project contains a folder named [data](https://github.com/flinguenheld/42_call_me_maybe/tree/master/data) with some examples:  
```Bash
    make examples
```

### Resources
[Function Calling System](https://developers.openai.com/api/docs/guides/function-calling)  
[Qwen/Qwen3-0.6B](https://github.com/QwenLM/Qwen3)  
[Hugging Face](https://huggingface.co/)  
[Argparse](https://www.geeksforgeeks.org/python/command-line-option-and-argument-parsing-using-argparse-in-python/)  
[Textual](https://textual.textualize.io/)  
[UV](https://docs.astral.sh/uv/)  

### Design decisions
I choose to split tasks to use several prompts and constraints.  

So for each prompt, the logic is:
- Find the [function's name](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/function/function.py)
- Find each [function's parameters](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_str.py) in a unique JSON:
    - Set the [prompt](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_float.py#L17) according to [the type](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/talker_manager.py#L89)
    - Set the list of [authorised tokens](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_int.py#L23)
    - Set the [start of the JSON](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_int.py#L23) answer
    - Get the tokens until the [end of the JSON](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_int.py#L23)
- [Merge the JSON](https://github.com/flinguenheld/42_call_me_maybe/blob/master/src/talker/parameter/parameter_int.py#L23) to update the ouput

### Algorithm explanation

<div align="center">
    <img src="./images/talkers.excalidraw.png">
</div>


### Performance analysis

To make the process faster, I choose to:
- Have very short prompts
- One prompt per type
- Fill the prompt with already known parts such as parameter names

Thanks to that, the generation is pretty fast for each prompt.

### Challenges faced

The main challenge was to understand the LLM vocabulary and how it works (e.g. with logits).  
(The way it sets them is still very obscure.)  
Due to that, writing prompts looks magic and it's complicated to find one which works for each cases.  
After having written long and detailed prompts, I finally opted for very short ones to reduce confusion.  

### Testing strategy

I wrote a visual representation to see what's happening.  
A serie of [pytests](https://docs.pytest.org/en/stable/) would be the best choice to update prompts.  
