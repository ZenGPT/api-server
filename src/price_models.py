openAIModels = {
    'gpt-3.5-turbo': {
        'oneDollarToken': 1 / 0.002 * 1000,
        'name': 'gpt-3.5-turbo-0301',
        'max_tokens': 4096,
        'tokens_per_message': 4,  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        'tokens_per_name': -1,  # if there's a name, the role is omitted
    },
    'gpt-4': {
        'promptTokenPerDollar': 1 / 0.43 * 1000,
        'completionTokenPerDollar': 1 / 0.86 * 1000,
        'name': 'gpt-4-0314',
        'max_tokens': 8000,
        'tokens_per_message': 3,
        'tokens_per_name': 1,
    },
}
