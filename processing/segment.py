from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from typing import Union


def window(iterable, size: int, overlap=32):
    """
    Generator for getting sliding windows from iterable
    """
    start = 0
    end = size
    step = size - overlap

    length = len(iterable)

    while start < length:
        yield iterable[start:end]
        start += step
        end += step


def segment(
    text: str,
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
    max_tokens=200,
    overlap=32,
) -> list[str]:
    """
    Segment text into overlapping segments for embedding.
    """
    tokens = tokenizer(text)
    input_ids = tokens["input_ids"]

    if len(input_ids) < max_tokens:  # type: ignore
        return [text]

    segments = []

    for i in window(input_ids, max_tokens, overlap):
        # FIXME: encoding is a desctructive process and decoding does not result in the original text
        # There are added symbols like <s>
        segment = tokenizer.decode(i)
        segments.append(segment)

    return segments
