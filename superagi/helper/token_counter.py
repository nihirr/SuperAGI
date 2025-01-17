from typing import List

import tiktoken

from superagi.types.common import BaseMessage

class TokenCounter:
    @staticmethod
    def token_limit(model: str = "gpt-3.5-turbo-0301") -> int:
        try:
            model_token_limit_dict = {"gpt-3.5-turbo-0301": 4032, "gpt-4-0314": 8092, "gpt-3.5-turbo": 4032, "gpt-4": 8092}
            return model_token_limit_dict[model]
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            return 8092

    @staticmethod
    def count_message_tokens(messages: List[BaseMessage], model: str = "gpt-3.5-turbo-0301") -> int:
        try:
            model_token_per_message_dict = {"gpt-3.5-turbo-0301": 4, "gpt-4-0314": 3, "gpt-3.5-turbo": 4, "gpt-4": 3}
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = model_token_per_message_dict[model]
        if tokens_per_message is None:
            raise NotImplementedError(
                f"num_tokens_from_messages() is not implemented for model {model}.\n"
                " See https://github.com/openai/openai-python/blob/main/chatml.md for"
                " information on how messages are converted to tokens."
            )

        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            num_tokens += len(encoding.encode(message['content']))

        num_tokens += 3
        return num_tokens
