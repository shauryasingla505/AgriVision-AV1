import pandas as pd
import json
import os

def generate_all_data():
    # 1. processed_nutrients.csv (Full list of Indian States)
    nutrients_data = {
        'State': [
            'ANDHRA PRADESH', 'ARUNACHAL PRADESH', 'ASSAM', 'BIHAR', 'CHHATTISGARH', 
            'GOA', 'GUJARAT', 'HARYANA', 'HIMACHAL PRADESH', 'JHARKHAND', 
            'KARNATAKA', 'KERALA', 'MADHYA PRADESH', 'MAHARASHTRA', 'MANIPUR', 
            'MEGHALAYA', 'MIZORAM', 'NAGALAND', 'ODISHA', 'PUNJAB', 'RAJASTHAN', 
            'SIKKIM', 'TAMIL NADU', 'TELANGANA', 'TRIPURA', 'UTTAR PRADESH', 
            'UTTARAKHAND', 'WEST BENGAL'
        ],
        'Nitrogen': [80, 70, 75, 90, 85, 60, 95, 120, 65, 80, 75, 65, 100, 85, 60, 65, 55, 60, 80, 130, 110, 50, 85, 80, 70, 115, 65, 95],
        'Phosphorus': [40, 35, 40, 50, 45, 30, 55, 60, 35, 45, 40, 35, 50, 45, 35, 35, 30, 35, 40, 65, 55, 30, 45, 45, 40, 60, 35, 50],
        'Potassium': [40, 35, 40, 50, 40, 35, 50, 60, 40, 45, 50, 60, 45, 45, 35, 40, 30, 35, 45, 65, 55, 35, 50, 45, 40, 55, 40, 50]
    }
    pd.DataFrame(nutrients_data).to_csv('processed_nutrients.csv', index=False)
    print("✅ Created processed_nutrients.csv")

    # 2. forecasting_data.csv (Weather data matching States)
    weather_data = {
        'State': nutrients_data['State'],
        'Jan': [20]*28, 'Feb': [22]*28, 'Mar': [25]*28, 'Apr': [28]*28, 
        'May': [30]*28, 'June': [32]*28, 'July': [28]*28, 'Aug': [27]*28, 
        'Sep': [27]*28, 'Oct': [25]*28, 'Nov': [22]*28, 'Dec': [20]*28,
        'Average annual rainfall (mm)': [1100, 2500, 2800, 1200, 1300, 3000, 800, 600, 1200, 1300, 1200, 3000, 1000, 1000, 1800, 2800, 2500, 2000, 1400, 600, 500, 2700, 900, 950, 2200, 1000, 1500, 1600]
    }
    pd.DataFrame(weather_data).to_csv('forecasting_data.csv', index=False)
    print("✅ Created forecasting_data.csv")

    # 3. crop_requirements.json
    crop_reqs = {
        "Rice": {"n": 80, "p": 40, "k": 40, "t_min": 20, "t_max": 35, "r_min": 1000, "months": "June-July-Aug-Sep-Oct"},
        "Wheat": {"n": 100, "p": 50, "k": 40, "t_min": 15, "t_max": 25, "r_min": 500, "months": "Nov-Dec-Jan-Feb-Mar"},
        "Maize": {"n": 120, "p": 60, "k": 40, "t_min": 18, "t_max": 32, "r_min": 600, "months": "June-July-Aug-Sep"},
        "Cotton": {"n": 100, "p": 50, "k": 50, "t_min": 25, "t_max": 35, "r_min": 500, "months": "May-June-July-Aug"},
        "Sugarcane": {"n": 150, "p": 80, "k": 80, "t_min": 20, "t_max": 32, "r_min": 1500, "months": "Jan-Feb-Mar-Apr-May"}
    }
    with open('crop_requirements.json', 'w') as f:
        json.dump(crop_reqs, f, indent=4)
    print("✅ Created crop_requirements.json")

    # 4. cultivation_details.json
    cult_details = {
        "Rice": "Nursery preparation starts in June. Maintain 2-5cm standing water. Use Nitrogen in three split doses: at transplanting, tillering, and panicle initiation.",
        "Wheat": "Sow in lines with 22.5cm spacing. Ensure first irrigation at Crown Root Initiation (21 days after sowing). Apply remaining Nitrogen after first irrigation.",
        "Maize": "Requires well-drained loamy soil. Thinning should be done 10-15 days after emergence. Control weeds during the first 45 days.",
        "Cotton": "Maintain plant population of 50k-80k per hectare. Monitor for Pink Bollworm. Harvest only when bolls are fully dry.",
        "Sugarcane": "Plant sets in deep furrows. Requires earthing up at 90-120 days to prevent lodging. Harvest when lower leaves start drying."
    }
    with open('cultivation_details.json', 'w') as f:
        json.dump(cult_details, f, indent=4)
    print("✅ Created cultivation_details.json")

    # 5. lang_pack.json (Pre-translated UI dictionary)
    lang_pack = {
        "hi": {
            "Select State": "राज्य चुनें", "Select Crop": "फसल चुनें", "AgriVision-AV": "एग्रीविज़न-AV",
            "Nitrogen": "नाइट्रोजन", "Phosphorus": "फास्फोरस", "Potassium": "पोटेशियम",
            "Avg Temp": "औसत तापमान", "Rainfall": "वर्षा", "Predict & Show Advice": "पूर्वानुमान और सलाह दिखाएं",
            "Suitability": "उपयुक्तता", "Yield Estimate": "उपज अनुमान", "Potential Earnings": "संभावित आय",
            "Action Plan": "कार्य योजना", "Soil Health": "मृदा स्वास्थ्य", "Audio": "ऑडियो", "Agency Directory": "एजेंसी निर्देशिका",
            "Detailed NPK Gap Analysis": "विस्तृत NPK अंतराल विश्लेषण", "Requirement for": "के लिए आवश्यकता", "gap": "अभाव"
        },
        "mr": {
            "Select State": "राज्य निवडा", "Select Crop": "पीक निवडा", "AgriVision-AV": "अ‍ॅग्रीव्हिजन-AV",
            "Nitrogen": "नत्र", "Phosphorus": "स्फुरद", "Potassium": "पालाश",
            "Avg Temp": "सरासरी तापमान", "Rainfall": "पाऊस", "Predict & Show Advice": "अंदाज आणि सल्ला पहा",
            "Suitability": "योग्यता", "Yield Estimate": "उत्पन्न अंदाज", "Potential Earnings": "संभावित उत्पन्न",
            "Action Plan": "कृती योजना", "Soil Health": "जमिनीचे आरोग्य", "Audio": "ऑडिओ", "Agency Directory": "एजेंसी मार्गदर्शिका",
            "Detailed NPK Gap Analysis": "तपशीलवार NPK विश्लेषण", "Requirement for": "साठी आवश्यक", "gap": "कमतरता"
        },
        "ta": {
            "Select State": "மாநிலத்தைத் தேர்ந்தெடுக்கவும்", "Select Crop": "பயிரைத் தேர்ந்தெடுக்கவும்", "AgriVision-AV": "அக்ரிவிஷன்-AV",
            "Nitrogen": "நைட்ரஜன்", "Phosphorus": "பாஸ்பரஸ்", "Potassium": "பொட்டாசியம்",
            "Avg Temp": "சராசரி வெப்பநிலை", "Rainfall": "மழைப்பொழிவு", "Predict & Show Advice": "கணிப்பு மற்றும் ஆலோசனையைக் காட்டு",
            "Suitability": "பொருத்தம்", "Yield Estimate": "மகசூல் மதிப்பீடு", "Potential Earnings": "சாத்தியமான வருவாய்",
            "Action Plan": "செயல் திட்டம்", "Soil Health": "மண் ஆரோக்கியம்", "Audio": "ஆடியோ", "Agency Directory": "முகமை அடைவு",
            "Detailed NPK Gap Analysis": "விரிவான NPK இடைவெளி பகுப்பாய்வு", "Requirement for": "தேவை", "gap": "இடைவெளி"
        },
        "te": {
            "Select State": "రాష్ట్రాన్ని ఎంచుకోండి", "Select Crop": "పంటను ఎంచుకోండి", "AgriVision-AV": "అగ్రివిజన్-AV",
            "Nitrogen": "నైట్రోజన్", "Phosphorus": "భాస్వరం", "Potassium": "పొటాషియం",
            "Avg Temp": "సగటు ఉష్ణోగ్రత", "Rainfall": "వర్షపాతం", "Predict & Show Advice": "అంచనా మరియు సలహా చూపించు",
            "Suitability": "అనుకూలత", "Yield Estimate": "దిగుబడి అంచనా", "Potential Earnings": "సంభావ్య ఆదాయం",
            "Action Plan": "కార్యాచరణ ప్రణాళిక", "Soil Health": "నేల ఆరోగ్యం", "Audio": "ఆడియో", "Agency Directory": "ఏజెన్సీ డైరెక్టరీ",
            "Detailed NPK Gap Analysis": "వివరణాత్మక NPK విశ్లేషణ", "Requirement for": "కోసం అవసరం", "gap": "తక్కువ"
        }
    }
    with open('lang_pack.json', 'w', encoding='utf-8') as f:
        json.dump(lang_pack, f, ensure_ascii=False, indent=4)
    print("✅ Created lang_pack.json")

if __name__ == "__main__":
    generate_all_data()