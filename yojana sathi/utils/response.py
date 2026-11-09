def generate_response(user_query, schemes):

    if not schemes:
        return (
            "माफ़ कीजिए, मुझे आपकी बात से संबंधित "
            "कोई योजना अपने डेटाबेस में नहीं मिली। "
            "आप सरकारी सहायता के लिए संबंधित सरकारी "
            "विभाग या आधिकारिक पोर्टल से संपर्क करें।"
        )

    scheme = schemes[0]

    response = f"""
आपकी जानकारी के अनुसार, आपके लिए यह योजना उपयोगी हो सकती है:

योजना का नाम: {scheme['name']}

योजना की जानकारी:
{scheme['description']}

मुख्य लाभ:
"""

    for benefit in scheme["benefits"]:
        response += f"\n- {benefit}"

    response += "\n\nपात्रता की मुख्य शर्तें:\n"

    for condition in scheme["eligibility"]:
        response += f"\n- {condition}"

    response += (
        f"\n\nअधिक जानकारी के लिए आधिकारिक वेबसाइट देखें: "
        f"{scheme['official_website']}"
    )

    response += (
        "\n\nध्यान दें: यह शुरुआती जानकारी है। "
        "आपकी वास्तविक पात्रता की पुष्टि संबंधित "
        "सरकारी विभाग से करें।"
    )

    return response