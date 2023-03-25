from schema import Schema, Optional, Or

open_ai_schema = Schema({
    'model': str,
    'prompt': Or(str, list),
    'user_token': str,
    Optional('temperature'): Or(float, int),
    Optional('max_tokens'): int,
    Optional('top_p'): Or(float, int),
    Optional('frequency_penalty'): Or(float, int),
    Optional('presence_penalty'): Or(float, int),
    Optional('stop'): [str],
    Optional('best_of'): int,
    Optional('stream'): bool,
    Optional('n'): int,
}, ignore_extra_keys=True)
