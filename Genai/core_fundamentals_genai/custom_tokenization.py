import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

input_token = "Hey there, My name is Mohit Soni"

token_after_tokenization = enc.encode(input_token)

print(token_after_tokenization)

## decoding

output_token_after_detokenization = enc.decode([25216, 1354, 11, 3673, 1308, 382, 31564, 278, 336, 7415])

print(output_token_after_detokenization)