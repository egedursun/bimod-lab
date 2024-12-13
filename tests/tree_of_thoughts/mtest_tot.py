import openai
import copy
import re


class DecisionTreeChatClient:
    def __init__(self, api_key, model="gpt-4o-mini", max_branches=3, max_depth=3):
        self.api_key = api_key
        self.model = model
        self.max_branches = max_branches
        self.max_depth = max_depth
        self.branches = []
        openai.api_key = self.api_key

    def initialize_tree(self, system_message):
        print("Initializing conversation tree with system message...\n")
        initial_chat_history = [{"role": "system", "content": system_message}]
        self.branches = [(initial_chat_history, 0)]
        print("Tree initialized with 1 branch.\n")

    def self_evaluate(self, chat_histories, responses):
        print("\nSelf-evaluating assistant responses...")
        combined_responses = "\n\n".join([f"Response {idx + 1}: {resp}" for idx, resp in enumerate(responses)])
        evaluation_prompt = (
            "You are an AI self-evaluator. Given the following conversation history and multiple responses from the assistant, "
            "evaluate the quality of each response based on the following criteria: Accuracy, Completeness, Relevance, Coherence, and Bias. "
            "Assign a score between 1 and 10 for each criterion, sum the scores, and state the best response.\n\n"
            f"Conversation History:\n{chat_histories}\n\n"
            f"Assistant Responses:\n{combined_responses}\n\n"
            "Provide scores in the following format:\n"
            "Response 1: Accuracy: X.X, Completeness: X.X, Relevance: X.X, Coherence: X.X, Bias: X.X, Total: X.X\n"
            "Response 2: Accuracy: X.X, Completeness: X.X, Relevance: X.X, Coherence: X.X, Bias: X.X, Total: X.X\n"
            "Best Response: N (where N is the response number)."
        )
        try:
            evaluation_response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are an AI evaluator."},
                          {"role": "user", "content": evaluation_prompt}],
                max_tokens=300,
            )
            scores_text = evaluation_response.choices[0].message.content.strip()
            print(f"Evaluation Result:\n{scores_text}\n")

            criteria_scores = {}
            best_response_index = 0

            # Extract scores for all criteria
            score_matches = re.findall(
                r"Response (\d+): Accuracy: (\d+(?:\.\d+)?), Completeness: (\d+(?:\.\d+)?), Relevance: (\d+(?:\.\d+)?), Coherence: (\d+(?:\.\d+)?), Bias: (\d+(?:\.\d+)?), Total: (\d+(?:\.\d+)?)",
                scores_text
            )
            for match in score_matches:
                idx = int(match[0]) - 1
                scores = {
                    "accuracy": float(match[1]),
                    "completeness": float(match[2]),
                    "relevance": float(match[3]),
                    "coherence": float(match[4]),
                    "bias": float(match[5]),
                    "total": float(match[6])
                }
                criteria_scores[idx] = scores

            # Find the best response
            best_response_match = re.search(r"Best Response: (\d+)", scores_text)
            if best_response_match:
                best_response_index = int(best_response_match.group(1)) - 1

            return criteria_scores, best_response_index
        except Exception as e:
            print(f"Evaluation failed: {e}")
            return {}, 0

    def generate_branches(self):
        print("\nImproving responses step by step until max depth is reached...\n")
        for _ in range(self.max_depth):
            new_branches = []
            for idx, (chat_history, depth) in enumerate(self.branches):
                print(f"Processing Branch {idx + 1} at depth {depth}...")
                if depth >= self.max_depth:
                    print("Max depth reached for this branch. Skipping...\n")
                    new_branches.append((chat_history, depth))
                    continue
                try:
                    improvement_prompt = (
                        "Improve the following assistant response to make it clearer, more relevant, accurate, complete, coherent, and unbiased.\n\n"
                        f"Conversation History:\n{chat_history}\n\n"
                        f"Assistant Response:\n{chat_history[-1]['content']}\n\n"
                        "Here are the evaluation scores for the previous response:\n"
                        f"Accuracy: {chat_history[-1].get('accuracy', 'N/A')}\n"
                        f"Completeness: {chat_history[-1].get('completeness', 'N/A')}\n"
                        f"Relevance: {chat_history[-1].get('relevance', 'N/A')}\n"
                        f"Coherence: {chat_history[-1].get('coherence', 'N/A')}\n"
                        f"Bias: {chat_history[-1].get('bias', 'N/A')}\n\n"
                        "Improved Response:"
                    )
                    response = openai.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are an AI assistant tasked with improving responses."},
                            {"role": "user", "content": improvement_prompt}],
                        n=self.max_branches,
                        max_tokens=150,
                    )
                    responses = [choice.message.content for choice in response.choices]
                    criteria_scores, best_response_idx = self.self_evaluate(chat_history, responses)
                    best_response = responses[best_response_idx]
                    print(f"Refined Best Response: {best_response[:50]}...")
                    new_history = copy.deepcopy(chat_history)
                    new_message = {"role": "assistant", "content": best_response, **criteria_scores[best_response_idx]}
                    new_history.append(new_message)
                    new_branches.append((new_history, depth + 1))

                    # Dynamically decide how many branches to proceed with
                    dynamic_branch_count = len(responses) // 2 if len(responses) > 1 else 1
                    new_branches = new_branches[:dynamic_branch_count]

                except Exception as e:
                    print(f"Error generating responses: {e}\n")
            self.branches = new_branches
        print(f"Refinement complete. Total active branches: {len(self.branches)}\n")

    def add_user_input(self, user_input):
        print(f"Adding user input: '{user_input}' to all branches...")
        new_branches = []
        for idx, (chat_history, depth) in enumerate(self.branches):
            new_history = copy.deepcopy(chat_history)
            new_history.append({"role": "user", "content": user_input})
            print(f"Updated Branch {idx + 1} with user input.")
            new_branches.append((new_history, depth))
        self.branches = new_branches

    def run(self, system_message):
        self.initialize_tree(system_message)
        user_input = input("\nYour response: ")
        if user_input.lower() == "exit":
            return
        self.add_user_input(user_input)
        self.generate_branches()
        print("\nFinal improved responses:")
        for idx, (history, _) in enumerate(self.branches):
            print(f"\nFinal Branch {idx + 1}:")
            for msg in history:
                print(f"{msg['role'].capitalize()}: {msg['content']}")
            print("---")


if __name__ == "__main__":
    api_key = "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"
    client = DecisionTreeChatClient(
        api_key,
        max_branches=5,
        max_depth=5
    )
    client.run("You are a helpful assistant.")
