from utils.retriever import find_schemes
from utils.response import generate_response

query = "मुझे खेती के लिए सरकारी सहायता चाहिए"

schemes = find_schemes(query)

answer = generate_response(query, schemes)

print(answer)