from utils.token_count import num_tokens_from_messages
import re
import os

REGEX_PATTERN = (r"(\*\*\S+\*\*)\n\n\n([\s\S]+?)\n------------------\n")
SYSTEM_PROMPT = {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture. Knowledge cutoff: 2021-09 Current date: 2023-04-27"}
COST_DICT = {
    "gpt-3.5-turbo": {
        "prompting": 0.002,
        "completion": 0.002,
    },
    "gpt-4": {
        "prompting": 0.03,
        "completion": 0.06,
    },
}

def get_messages_json(messages):
    messages = re.findall(REGEX_PATTERN, messages)
    message_json = []
    for role, message in messages:
        if "you" in role.lower():
            role = "user"
        else:
            role = "assistant"
        message_json.append({"role": role, "content": message})
    return message_json

def get_prompting_session(message_json):
    prompting_session = []
    for i in range(0,len(message_json),2):
        prompt_dict = {
            "prompt": [SYSTEM_PROMPT] + message_json[:i+1],
            "completion": message_json[i+1]
        }
        prompting_session.append(prompt_dict)
    return prompting_session

def evaluate_cost(prompting_session, model="gpt-4"):
    prompt_cost = COST_DICT[model]["prompting"]
    completion_cost = COST_DICT[model]["completion"]
    total_cost = 0
    for calls in prompting_session:
        prompt_tokens = num_tokens_from_messages(calls["prompt"], model=model)
        completion_tokens = num_tokens_from_messages([calls["completion"]], model=model)
        total_cost += prompt_cost * prompt_tokens / 1000 + completion_cost * completion_tokens / 1000
    return total_cost

if __name__ == "__main__":
    total_cost = 0

    data_path = "_posts/small-projects/chat-gpt-4-cost-analysis/"

    for filename in os.listdir(f"{data_path}/data"):
        if "gpt3" in filename:
            model = "gpt-3.5-turbo"
        else:
            model = "gpt-4"
        with open(f"{data_path}/data/{filename}", "r") as f:
            messages = f.read()
        messages = get_messages_json(messages)
        prompting_session = get_prompting_session(messages)
        cost = evaluate_cost(prompting_session, model=model)
        total_cost += cost

    print(f"Total cost of all sessions using API: ${total_cost:.2f}")
    if total_cost > 20:
        print("Since the cost is greater than $20, you should use ChatGPT instead of the API")
    else:
        print("Since the cost is less than $20, you should use the API instead of ChatGPT")