from utils.retriever import find_schemes

test_queries = [
    "मुझे खेती के लिए सरकारी सहायता चाहिए",
    "मेरे पिता को अस्पताल में इलाज करवाना है",
    "मुझे गैस सिलेंडर का कनेक्शन चाहिए",
    "मुझे सरकारी नौकरी चाहिए"
]

for query in test_queries:
    print("\nUser:", query)

    results = find_schemes(query)

    if results:
        for scheme in results:
            print("Matched Scheme:", scheme["name"])
    else:
        print("No matching scheme found.")