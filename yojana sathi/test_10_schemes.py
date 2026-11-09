
from utils.retriever import find_schemes

queries = [
    "मुझे खेती के लिए सहायता चाहिए",
    "मेरे पिता को अस्पताल में इलाज चाहिए",
    "मुझे गैस कनेक्शन चाहिए",
    "मुझे बैंक में जीरो बैलेंस खाता खोलना है",
    "मुझे गांव में रोजगार चाहिए",
    "मुझे पक्का मकान बनवाना है",
    "मैं बढ़ई का काम करता हूं",
    "मैं ठेले पर सब्जी बेचता हूं",
    "मुझे अपना छोटा बिजनेस शुरू करना है",
    "मुझे कॉलेज की स्कॉलरशिप चाहिए"
]

for query in queries:
    results = find_schemes(query)

    print("\nUser:", query)

    if results:
        print("Matched:", results[0]["name"])
    else:
        print("No matching scheme")
