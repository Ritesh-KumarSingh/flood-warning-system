"""
Multi-Language Support System
Currently supports: English, Hindi
Easily extensible to other Indian languages
"""

class LanguageTranslator:
    """Handle translations for disaster warning messages"""
    
    def __init__(self):
        self.translations = {
            'en': {
                # UI Elements
                'app_title': 'AI Disaster Early Warning System',
                'select_disaster': 'Select Disaster Type',
                'enter_city': 'Enter City Name',
                'check_risk': 'Check Risk',
                'risk_assessment': 'Risk Assessment',
                'recommended_actions': 'Recommended Actions',
                'emergency_contacts': 'Emergency Contacts',
                'current_weather': 'Current Weather Conditions',
                
                # Risk Levels
                'safe': 'Safe',
                'warning': 'Warning',
                'high_risk': 'High Risk',
                'critical': 'Critical',
                
                # Disaster Types
                'flood': 'Flood',
                'earthquake': 'Earthquake',
                'cyclone': 'Cyclone',
                'landslide': 'Landslide',
                'heatwave': 'Heatwave',
                
                # Actions
                'evacuate': 'Evacuate immediately',
                'prepare': 'Prepare emergency supplies',
                'monitor': 'Monitor conditions',
                'stay_indoors': 'Stay indoors',
                'move_high_ground': 'Move to higher ground',
                'avoid_slopes': 'Avoid hilly areas',
                'stay_hydrated': 'Stay hydrated',
                
                # Emergency Services
                'ambulance': 'Ambulance',
                'police': 'Police',
                'fire': 'Fire Service',
                'disaster_mgmt': 'Disaster Management',
                
                # Weather
                'temperature': 'Temperature',
                'humidity': 'Humidity',
                'rainfall': 'Rainfall',
                'wind_speed': 'Wind Speed',
            },
            'hi': {
                # UI Elements
                'app_title': 'AI आपदा पूर्व चेतावनी प्रणाली',
                'select_disaster': 'आपदा प्रकार चुनें',
                'enter_city': 'शहर का नाम दर्ज करें',
                'check_risk': 'जोखिम जांचें',
                'risk_assessment': 'जोखिम मूल्यांकन',
                'recommended_actions': 'अनुशंसित कार्य',
                'emergency_contacts': 'आपातकालीन संपर्क',
                'current_weather': 'वर्तमान मौसम की स्थिति',
                
                # Risk Levels
                'safe': 'सुरक्षित',
                'warning': 'चेतावनी',
                'high_risk': 'उच्च जोखिम',
                'critical': 'गंभीर',
                
                # Disaster Types
                'flood': 'बाढ़',
                'earthquake': 'भूकंप',
                'cyclone': 'चक्रवात',
                'landslide': 'भूस्खलन',
                'heatwave': 'गर्मी की लहर',
                
                # Actions
                'evacuate': 'तुरंत निकल जाएं',
                'prepare': 'आपातकालीन सामान तैयार करें',
                'monitor': 'स्थिति पर नजर रखें',
                'stay_indoors': 'घर के अंदर रहें',
                'move_high_ground': 'ऊंची जगह पर जाएं',
                'avoid_slopes': 'पहाड़ी इलाकों से बचें',
                'stay_hydrated': 'पानी पीते रहें',
                
                # Emergency Services
                'ambulance': 'एम्बुलेंस',
                'police': 'पुलिस',
                'fire': 'फायर सर्विस',
                'disaster_mgmt': 'आपदा प्रबंधन',
                
                # Weather
                'temperature': 'तापमान',
                'humidity': 'नमी',
                'rainfall': 'बारिश',
                'wind_speed': 'हवा की गति',
            }
        }
        
        # Messages by disaster and risk level
        self.messages = {
            'en': {
                'flood': {
                    0: "Low flood risk. Weather conditions are normal.",
                    1: "Moderate flood risk. Monitor weather closely.",
                    2: "HIGH flood risk! Heavy rainfall expected. Prepare to evacuate.",
                    3: "CRITICAL FLOOD ALERT! Severe flooding imminent. Evacuate NOW!"
                },
                'earthquake': {
                    0: "Low seismic risk. Normal conditions.",
                    1: "Moderate seismic activity possible. Stay prepared.",
                    2: "HIGH earthquake risk! Ensure emergency preparedness.",
                    3: "CRITICAL seismic alert! Very high risk. Immediate safety measures required!"
                },
                'cyclone': {
                    0: "No cyclone threat. Weather stable.",
                    1: "Cyclone watch. Monitor weather updates.",
                    2: "CYCLONE WARNING! Strong winds expected. Prepare to evacuate.",
                    3: "CRITICAL CYCLONE! Severe storm approaching. Evacuate immediately!"
                },
                'landslide': {
                    0: "Low landslide risk. Slopes stable.",
                    1: "Landslide watch. Heavy rain may affect slopes.",
                    2: "HIGH landslide risk! Avoid hilly areas.",
                    3: "CRITICAL landslide danger! Evacuate slopes immediately!"
                },
                'heatwave': {
                    0: "Comfortable weather. Normal temperatures.",
                    1: "Hot conditions. Stay hydrated.",
                    2: "HEATWAVE WARNING! Extreme heat. Avoid outdoor activities.",
                    3: "CRITICAL HEAT! Dangerous conditions. Stay indoors with AC!"
                }
            },
            'hi': {
                'flood': {
                    0: "बाढ़ का कम जोखिम। मौसम सामान्य है।",
                    1: "मध्यम बाढ़ जोखिम। मौसम पर ध्यान दें।",
                    2: "उच्च बाढ़ जोखिम! भारी बारिश संभावित। निकलने की तैयारी करें।",
                    3: "गंभीर बाढ़ अलर्ट! भयंकर बाढ़ आ रही है। अभी निकल जाएं!"
                },
                'earthquake': {
                    0: "भूकंप का कम खतरा। सामान्य स्थिति।",
                    1: "मध्यम भूकंप संभव। तैयार रहें।",
                    2: "उच्च भूकंप जोखिम! आपातकालीन तैयारी सुनिश्चित करें।",
                    3: "गंभीर भूकंप अलर्ट! बहुत उच्च खतरा। तुरंत सुरक्षा उपाय करें!"
                },
                'cyclone': {
                    0: "चक्रवात का खतरा नहीं। मौसम स्थिर है।",
                    1: "चक्रवात चेतावनी। मौसम अपडेट देखें।",
                    2: "चक्रवात चेतावनी! तेज हवाएं आ रही हैं। निकलने की तैयारी करें।",
                    3: "गंभीर चक्रवात! भयंकर तूफान आ रहा है। तुरंत निकल जाएं!"
                },
                'landslide': {
                    0: "भूस्खलन का कम खतरा। ढलान सुरक्षित हैं।",
                    1: "भूस्खलन चेतावनी। भारी बारिश से ढलान प्रभावित हो सकती हैं।",
                    2: "उच्च भूस्खलन जोखिम! पहाड़ी इलाकों से बचें।",
                    3: "गंभीर भूस्खलन खतरा! पहाड़ों से तुरंत निकल जाएं!"
                },
                'heatwave': {
                    0: "आरामदायक मौसम। सामान्य तापमान।",
                    1: "गर्म मौसम। पानी पीते रहें।",
                    2: "गर्मी की लहर चेतावनी! अत्यधिक गर्मी। बाहर जाने से बचें।",
                    3: "गंभीर गर्मी! खतरनाक स्थिति। AC के साथ घर में रहें!"
                }
            }
        }
        
        # Action translations
        self.actions = {
            'en': {
                'flood': {
                    0: ["Monitor weather", "Review flood safety"],
                    1: ["Prepare emergency kit", "Avoid low areas", "Stock supplies"],
                    2: ["Move to higher ground", "Secure valuables", "Ready to evacuate"],
                    3: ["EVACUATE NOW", "Follow authorities", "Move to high ground"]
                },
                'earthquake': {
                    0: ["Review earthquake plan", "Secure furniture"],
                    1: ["Identify safe spots", "Prepare emergency kit", "Practice DROP-COVER-HOLD"],
                    2: ["Secure appliances", "Identify evacuation routes", "Stock supplies"],
                    3: ["Ensure kit ready", "Stay away from buildings", "Follow emergency services"]
                },
                'cyclone': {
                    0: ["Monitor weather", "Review cyclone plan"],
                    1: ["Secure outdoor items", "Stock supplies", "Charge devices"],
                    2: ["Board windows", "Move to shelter", "Avoid coast"],
                    3: ["EVACUATE to shelter", "Stay away from windows", "Listen to broadcasts"]
                },
                'landslide': {
                    0: ["Monitor weather", "Avoid steep slopes in rain"],
                    1: ["Watch slope stability", "Avoid hillside driving", "Plan escape route"],
                    2: ["EVACUATE slope areas", "Stay away from valleys", "Watch for debris"],
                    3: ["EVACUATE IMMEDIATELY", "Move to stable ground", "Call emergency"]
                },
                'heatwave': {
                    0: ["Stay hydrated", "Enjoy weather safely"],
                    1: ["Drink water frequently", "Avoid peak sun", "Wear light clothing"],
                    2: ["Stay indoors peak hours", "Use AC", "Check on elderly"],
                    3: ["STAY INDOORS with AC", "Seek cooling centers", "Medical help if needed"]
                }
            },
            'hi': {
                'flood': {
                    0: ["मौसम पर नज़र रखें", "बाढ़ सुरक्षा की समीक्षा करें"],
                    1: ["आपातकालीन किट तैयार करें", "निचले इलाकों से बचें", "सामान स्टॉक करें"],
                    2: ["ऊंची जगह पर जाएं", "कीमती सामान सुरक्षित करें", "निकलने के लिए तैयार रहें"],
                    3: ["अभी निकल जाएं", "अधिकारियों का पालन करें", "ऊंची जमीन पर जाएं"]
                },
                'earthquake': {
                    0: ["भूकंप योजना की समीक्षा करें", "फर्नीचर सुरक्षित करें"],
                    1: ["सुरक्षित स्थान पहचानें", "आपातकालीन किट तैयार करें", "झुको-ढको-पकड़ो का अभ्यास करें"],
                    2: ["उपकरण सुरक्षित करें", "निकासी मार्ग पहचानें", "सामान स्टॉक करें"],
                    3: ["किट तैयार रखें", "इमारतों से दूर रहें", "आपातकालीन सेवाओं का पालन करें"]
                },
                'cyclone': {
                    0: ["मौसम पर नज़र रखें", "चक्रवात योजना की समीक्षा करें"],
                    1: ["बाहरी वस्तुएं सुरक्षित करें", "सामान स्टॉक करें", "डिवाइस चार्ज करें"],
                    2: ["खिड़कियां बंद करें", "शेल्टर में जाएं", "तट से बचें"],
                    3: ["शेल्टर में निकल जाएं", "खिड़कियों से दूर रहें", "प्रसारण सुनें"]
                },
                'landslide': {
                    0: ["मौसम पर नज़र रखें", "बारिश में खड़ी ढलानों से बचें"],
                    1: ["ढलान की स्थिरता देखें", "पहाड़ी ड्राइविंग से बचें", "बचाव मार्ग योजना बनाएं"],
                    2: ["ढलान क्षेत्रों से निकल जाएं", "घाटियों से दूर रहें", "मलबे के लिए देखें"],
                    3: ["तुरंत निकल जाएं", "स्थिर जमीन पर जाएं", "आपातकालीन कॉल करें"]
                },
                'heatwave': {
                    0: ["पानी पीते रहें", "सुरक्षित रूप से मौसम का आनंद लें"],
                    1: ["बार-बार पानी पिएं", "चरम धूप से बचें", "हल्के कपड़े पहनें"],
                    2: ["चरम घंटों में घर के अंदर रहें", "AC का उपयोग करें", "बुजुर्गों की जांच करें"],
                    3: ["AC के साथ घर में रहें", "कूलिंग सेंटर की तलाश करें", "जरूरत पर चिकित्सा सहायता लें"]
                }
            }
        }
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text for a key"""
        return self.translations.get(language, {}).get(key, self.translations['en'].get(key, key))
    
    def get_message(self, disaster_type: str, risk_level: int, language: str = 'en') -> str:
        """Get disaster message in specified language"""
        return self.messages.get(language, {}).get(disaster_type, {}).get(risk_level, "Unknown")
    
    def get_actions(self, disaster_type: str, risk_level: int, language: str = 'en') -> list:
        """Get action items in specified language"""
        return self.actions.get(language, {}).get(disaster_type, {}).get(risk_level, [])
    
    def get_available_languages(self) -> dict:
        """Get list of available languages"""
        return {
            'en': '🇬🇧 English',
            'hi': '🇮🇳 हिंदी (Hindi)'
        }


# Quick test
def test_translator():
    """Test the translator"""
    translator = LanguageTranslator()
    
    print("Testing Language Translator...")
    print("="*70)
    
    print("\n1. Available Languages:")
    for code, name in translator.get_available_languages().items():
        print(f"   {code}: {name}")
    
    print("\n2. UI Elements:")
    print(f"   EN: {translator.get_text('app_title', 'en')}")
    print(f"   HI: {translator.get_text('app_title', 'hi')}")
    
    print("\n3. Flood Messages:")
    for level in range(4):
        print(f"   Level {level} EN: {translator.get_message('flood', level, 'en')}")
        print(f"   Level {level} HI: {translator.get_message('flood', level, 'hi')}")
        print()
    
    print("="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_translator()

