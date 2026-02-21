"""
Disaster AI Chatbot & Voice Assistant
Provides instant answers to disaster-related questions in multiple languages
"""

import streamlit as st
from datetime import datetime
import random


class DisasterChatbot:
    """AI-powered chatbot for disaster preparedness and response"""
    
    def __init__(self):
        # Knowledge base - disaster FAQs
        self.knowledge_base = {
            'en': {
                'flood': {
                    'what to do during flood': "🌊 During a flood:\n1. Move to higher ground immediately\n2. Don't walk/drive through flood water\n3. Turn off electricity at the mains\n4. Keep emergency kit ready\n5. Listen to local authorities\n6. Call 112 or 1078 if in danger",
                    'flood preparation': "📦 Flood preparation:\n1. Store 3 days of water & food per person\n2. Keep documents in waterproof bags\n3. Know your evacuation route\n4. Charge phones & power banks\n5. Keep first aid kit ready\n6. Move valuables to upper floors",
                    'after flood': "After a flood:\n1. Don't return home until declared safe\n2. Avoid flood water (may be contaminated)\n3. Check for structural damage before entering\n4. Disinfect everything touched by flood water\n5. Watch for snakes & insects\n6. Document damage for insurance",
                    'flood warning signs': "⚠️ Flood warning signs:\n1. Heavy continuous rainfall for hours\n2. Rising river/stream levels\n3. Water appearing in unusual places\n4. Unusual sounds (rushing water, mudslides)\n5. Official flood warnings on news/alerts\n6. Waterlogged roads and drains overflowing",
                    'flood safety kit': "🎒 Flood emergency kit:\n1. Drinking water (4L per person/day)\n2. Non-perishable food (3 days)\n3. Flashlight + extra batteries\n4. First aid kit & medicines\n5. Important documents in waterproof bag\n6. Whistle for signaling help\n7. Phone charger / power bank\n8. Rope (30 feet)",
                    'driving in flood': "🚗 Driving in flood water:\n• NEVER drive through flooded roads\n• Just 6 inches of water can knock you down\n• 12 inches of water can sweep away a car\n• 2 feet can carry away SUVs/trucks\n• If car stalls in water, abandon it immediately\n• Turn around, don't drown!",
                    'sandbags': "🧱 Using sandbags:\n1. Fill bags 2/3 full with sand\n2. Stack in pyramid pattern\n3. Place against doors/openings\n4. Layer plastic sheeting behind them\n5. Remove after flood recedes\n6. Dispose contaminated bags safely",
                },
                'earthquake': {
                    'what to do during earthquake': "🔥 During an earthquake:\n1. DROP to the ground\n2. Take COVER under sturdy furniture\n3. HOLD ON until shaking stops\n4. Stay away from windows & heavy objects\n5. If outside, move to open area\n6. Never use elevators",
                    'earthquake preparation': "📦 Earthquake preparation:\n1. Secure heavy furniture to walls\n2. Know safe spots in each room\n3. Practice DROP-COVER-HOLD with family\n4. Keep emergency kit ready\n5. Know how to turn off gas/electricity\n6. Store shoes near bed (for broken glass)",
                    'after earthquake': "After an earthquake:\n1. Check for injuries, apply first aid\n2. Check for gas leaks & structural damage\n3. Expect aftershocks\n4. Stay out of damaged buildings\n5. Use phone only for emergencies\n6. Turn off gas if you smell a leak",
                    'earthquake safety outdoor': "🏃 If outdoors during earthquake:\n1. Move away from buildings & power lines\n2. Go to an open area\n3. Stay clear of bridges & overpasses\n4. Don't enter damaged buildings\n5. Watch for falling debris\n6. If in car, stop safely & stay inside",
                    'building earthquake safety': "🏢 Building safety:\n1. Avoid standing near windows\n2. Don't use elevators during shaking\n3. Use stairs to exit after shaking stops\n4. Check exits for damage first\n5. If trapped, tap on pipes/walls to signal\n6. Cover nose/mouth against dust",
                    'earthquake magnitude': "📊 Earthquake scale:\n• Below 2.0: Not felt\n• 2.0-3.9: Minor, rarely felt\n• 4.0-4.9: Light, noticeable shaking\n• 5.0-5.9: Moderate, can cause damage\n• 6.0-6.9: Strong, can be destructive\n• 7.0+: Major to Great, devastating",
                },
                'cyclone': {
                    'what to do during cyclone': "🌪️ During a cyclone:\n1. Stay indoors, away from windows\n2. Take shelter in strongest part of building\n3. Unplug all electrical equipment\n4. Fill bathtubs/containers with water\n5. Don't go outside during the eye\n6. Listen to official updates",
                    'cyclone preparation': "📦 Cyclone preparation:\n1. Board up windows\n2. Secure loose outdoor objects\n3. Store water & non-perishable food\n4. Charge all devices\n5. Keep important documents safe\n6. Know your nearest cyclone shelter",
                    'after cyclone': "After a cyclone:\n1. Wait for official all-clear\n2. Watch for fallen power lines\n3. Don't drink tap water until tested\n4. Check for structural damage\n5. Clean up debris carefully\n6. Help neighbors, especially elderly",
                    'cyclone warning signals': "🚩 Cyclone warning signals (India):\n• Green: Distant cyclone, no alarm\n• Yellow: Cyclone approaching, be alert\n• Orange: Cyclone expected in 24 hours\n• Red: Cyclone expected within 12 hours\n• Listen to IMD (India Meteorological Department)\n• National Emergency: 112",
                    'cyclone categories': "🌀 Cyclone categories:\n• Depression: <17 knots\n• Cyclonic Storm: 34-47 knots\n• Severe: 48-63 knots\n• Very Severe: 64-89 knots\n• Extremely Severe: 90-119 knots\n• Super Cyclonic Storm: 120+ knots",
                },
                'landslide': {
                    'what to do during landslide': "⛰️ During a landslide:\n1. Move away from the path of the slide\n2. Run to the nearest high ground\n3. If escape not possible, curl into a ball\n4. Protect your head\n5. Stay alert for additional slides\n6. Call emergency services: 112 / 1078",
                    'landslide warning signs': "⚠️ Landslide warning signs:\n1. New cracks in walls, ground, or pavement\n2. Tilting trees or utility poles\n3. Unusual sounds (rumbling, cracking)\n4. Springs appearing in new locations\n5. Sudden change in creek water (muddy)\n6. Bulging ground at base of slope",
                    'landslide preparation': "📦 Landslide preparation:\n1. Know your area's risk zones\n2. Plan evacuation route away from slopes\n3. Install drainage systems\n4. Don't build on steep slopes\n5. Maintain vegetation on slopes\n6. Learn to recognize warning signs",
                    'landslide causes': "🏔️ Common causes:\n1. Heavy or prolonged rainfall\n2. Earthquakes\n3. Deforestation / removing vegetation\n4. Mining and construction on slopes\n5. Rapid snowmelt\n6. Over-saturated soil\n7. River erosion at base of slopes",
                },
                'heatwave': {
                    'what to do during heatwave': "🌡️ During a heatwave:\n1. Stay indoors between 12-3 PM\n2. Drink water every 20 minutes\n3. Wear light, loose cotton clothes\n4. Avoid alcohol & caffeine\n5. Use ORS if dehydrated\n6. Keep curtains closed",
                    'heatwave preparation': "📦 Heatwave preparation:\n1. Stock up on water & ORS packets\n2. Check AC/cooler functionality\n3. Keep wet towels ready\n4. Plan outdoor activities for early morning\n5. Identify cool public spaces nearby\n6. Know heat stroke symptoms",
                    'heat stroke symptoms': "🚨 Heat stroke signs:\n1. Body temp above 104°F (40°C)\n2. Hot, red, dry skin (no sweating)\n3. Rapid strong pulse\n4. Throbbing headache\n5. Dizziness or confusion\n6. Nausea or vomiting\n\n⚡ ACT IMMEDIATELY: Call 108, cool the person with cold water",
                    'heat stroke first aid': "🏥 Heat stroke first aid:\n1. Call 108/112 immediately\n2. Move person to cool shade\n3. Cool body with cold water/ice packs\n4. Fan the person aggressively\n5. Do NOT give fluids if unconscious\n6. Place ice packs on neck, armpits, groin",
                    'outdoor workers heat': "👷 For outdoor workers:\n1. Take breaks every 30 minutes in shade\n2. Drink water constantly (not just when thirsty)\n3. Wear wide-brimmed hat\n4. Use sunscreen SPF 30+\n5. Know signs of heat exhaustion\n6. Buddy system: watch each other",
                },
                'general': {
                    'emergency kit': "🎒 Emergency kit essentials:\n1. Water (4L per person per day, 3 days)\n2. Non-perishable food (3 days)\n3. First aid kit & prescribed medicines\n4. Flashlight + batteries\n5. Phone charger + power bank\n6. Whistle\n7. Important documents (copies)\n8. Cash in small denominations\n9. Multi-tool / knife\n10. Blankets / warm clothing",
                    'first aid': "🏥 Basic first aid:\n1. Bleeding: Apply pressure with clean cloth\n2. Burns: Cool with water 10 min, cover loosely\n3. Fractures: Immobilize, don't move victim\n4. CPR: 30 compressions, 2 breaths (adults)\n5. Choking: 5 back blows, 5 Heimlich thrusts\n6. Shock: Lay down, elevate legs, keep warm",
                    'evacuation plan': "🏃 Evacuation plan:\n1. Know 2+ exit routes from home\n2. Pick a family meeting point\n3. Keep car fueled above half-tank\n4. Pack go-bag with 72-hour supplies\n5. Know your evacuation shelter\n6. Practice the plan with family twice a year",
                    'emergency numbers': "📞 Indian Emergency Numbers:\n• National Emergency: 112\n• Ambulance: 108 / 102\n• Police: 100\n• Fire: 101\n• Disaster Management (NDMA): 1078\n• Women Helpline: 1091\n• Child Helpline: 1098\n• Railway Emergency: 139",
                    'disaster insurance': "📋 Disaster insurance tips:\n1. Document all property & valuables (photos)\n2. Keep insurance papers in waterproof bag\n3. Review coverage annually\n4. Understand what's covered vs excluded\n5. File claims promptly with photos\n6. Keep receipts for emergency expenses",
                    'children safety': "👶 Keeping children safe:\n1. Teach them emergency numbers\n2. Practice drills at home\n3. Give them an ID card with contacts\n4. Have a comfort item in emergency kit\n5. Explain disasters calmly (no panic)\n6. Assign them age-appropriate tasks",
                    'pet safety': "🐾 Pet safety during disasters:\n1. Include pet food in emergency kit\n2. Keep vaccination records handy\n3. Have a leash/carrier ready\n4. Never leave pets tied up\n5. Many shelters don't allow pets — plan ahead\n6. Microchip your pets for identification",
                    'water purification': "💧 Emergency water purification:\n1. Boiling: Boil for 1 minute (best method)\n2. Chlorine: 8 drops bleach per gallon\n3. Iodine tablets: follow instructions\n4. Filter through clean cloth first\n5. Let particles settle before treating\n6. Store in clean containers",
                }
            },
            'hi': {
                'flood': {
                    'बाढ़ के दौरान क्या करें': "🌊 बाढ़ के दौरान:\n1. तुरंत ऊंचे स्थान पर जाएं\n2. बाढ़ के पानी में न चलें/न गाड़ी चलाएं\n3. बिजली का मेन स्विच बंद करें\n4. आपातकालीन किट तैयार रखें\n5. स्थानीय अधिकारियों की सुनें\n6. खतरे में हों तो 112 या 1078 पर कॉल करें",
                    'बाढ़ की तैयारी': "📦 बाढ़ की तैयारी:\n1. प्रति व्यक्ति 3 दिन का पानी और भोजन\n2. दस्तावेज़ वॉटरप्रूफ बैग में रखें\n3. निकासी मार्ग जानें\n4. फोन और पावर बैंक चार्ज रखें\n5. प्राथमिक चिकित्सा किट तैयार रखें",
                },
                'earthquake': {
                    'भूकंप के दौरान क्या करें': "🔥 भूकंप के दौरान:\n1. जमीन पर गिरें (DROP)\n2. मजबूत फर्नीचर के नीचे छिपें (COVER)\n3. हिलना बंद होने तक पकड़े रहें (HOLD)\n4. खिड़कियों से दूर रहें\n5. लिफ्ट का उपयोग न करें",
                },
                'general': {
                    'आपातकालीन नंबर': "📞 भारतीय आपातकालीन नंबर:\n• राष्ट्रीय आपातकाल: 112\n• एम्बुलेंस: 108/102\n• पुलिस: 100\n• फायर: 101\n• आपदा प्रबंधन: 1078\n• महिला हेल्पलाइन: 1091\n• बाल हेल्पलाइन: 1098",
                    'प्राथमिक चिकित्सा': "🏥 मूल प्राथमिक चिकित्सा:\n1. रक्तस्राव: साफ कपड़े से दबाएं\n2. जलना: 10 मिनट पानी से ठंडा करें\n3. फ्रैक्चर: हिलाएं नहीं\n4. सीपीआर: 30 दबाव, 2 सांस\n5. सदमा: लिटाएं, पैर ऊंचे करें",
                    'आपातकालीन किट': "🎒 आपातकालीन किट:\n1. पानी (प्रति व्यक्ति 4L/दिन, 3 दिन)\n2. सूखा भोजन (3 दिन)\n3. प्राथमिक चिकित्सा किट और दवाइयां\n4. टॉर्च + बैटरी\n5. फोन चार्जर + पावर बैंक\n6. सीटी\n7. महत्वपूर्ण दस्तावेज़\n8. नकदी",
                }
            }
        }
        
        # Intent patterns for matching
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good evening', 'नमस्ते', 'हैलो'],
            'thanks': ['thank', 'thanks', 'धन्यवाद', 'शुक्रिया', 'appreciate'],
            'emergency': ['emergency', 'help me', 'sos', 'urgent', 'danger', 'आपातकाल', 'मदद', 'बचाओ']
        }

    def get_response(self, user_message, disaster_type='general', language='en'):
        """Get chatbot response based on user message"""
        
        message_lower = user_message.lower()
        
        # Check for greetings
        if any(word in message_lower for word in self.intents['greeting']):
            responses = [
                "Hello! I'm your disaster safety assistant. How can I help you today?",
                "Hi! I'm here to help with disaster safety information. What would you like to know?"
            ] if language == 'en' else [
                "नमस्ते! मैं आपदा सुरक्षा सहायक हूं। मैं आपकी कैसे मदद कर सकता हूं?",
                "नमस्कार! मैं आपदा सुरक्षा जानकारी में मदद के लिए यहां हूं।"
            ]
            return random.choice(responses)
        
        # Check for thanks
        if any(word in message_lower for word in self.intents['thanks']):
            responses = [
                "You're welcome! Stay safe!",
                "Happy to help! Remember to stay prepared."
            ] if language == 'en' else [
                "आपका स्वागत है! सुरक्षित रहें!",
                "मदद करके खुशी हुई! तैयार रहना याद रखें।"
            ]
            return random.choice(responses)
        
        # Check for emergency
        if any(word in message_lower for word in self.intents['emergency']):
            if language == 'en':
                return """🚨 EMERGENCY NUMBERS:
• National Emergency: 112
• Ambulance: 108/102
• Police: 100
• Fire: 101
• Disaster Management: 1078

If you're in immediate danger, call 112 NOW!"""
            else:
                return """🚨 आपातकालीन नंबर:
• राष्ट्रीय आपातकाल: 112
• एम्बुलेंस: 108/102
• पुलिस: 100
• फायर: 101
• आपदा प्रबंधन: 1078

अगर आप तुरंत खतरे में हैं, तो अभी 112 पर कॉल करें!"""
        
        # Search knowledge base — fuzzy matching
        kb = self.knowledge_base.get(language, self.knowledge_base['en'])
        
        best_match = None
        best_score = 0
        
        # Search in disaster-specific and general knowledge
        search_categories = []
        if disaster_type in kb:
            search_categories.append(disaster_type)
        search_categories.append('general')
        # Also search all other categories
        for cat in kb:
            if cat not in search_categories:
                search_categories.append(cat)
        
        for category in search_categories:
            if category not in kb:
                continue
            for key, answer in kb[category].items():
                # Count how many words from the key appear in the user message
                key_words = key.lower().split()
                matching_words = sum(1 for w in key_words if w in message_lower)
                # Also check if any word from the message appears in the key
                msg_words = message_lower.split()
                reverse_match = sum(1 for w in msg_words if len(w) > 3 and w in key.lower())
                
                score = matching_words + reverse_match
                if score > best_score:
                    best_score = score
                    best_match = answer
        
        if best_match and best_score >= 1:
            return best_match
        
        # Default response
        if language == 'en':
            return """I can help with:
• What to do during disasters (flood, earthquake, cyclone, landslide, heatwave)
• Emergency preparation & safety kits
• First aid basics
• Emergency contact numbers
• Evacuation planning
• Heat stroke / water purification
• Children & pet safety

Try asking: "What to do during flood?" or "Emergency numbers" or "Heat stroke first aid" """
        else:
            return """मैं इसमें मदद कर सकता हूं:
• आपदा के दौरान क्या करें (बाढ़, भूकंप, चक्रवात, भूस्खलन, गर्मी)
• आपातकालीन तैयारी
• प्राथमिक चिकित्सा
• आपातकालीन संपर्क नंबर

पूछें: "बाढ़ के दौरान क्या करें?" या "आपातकालीन नंबर" """

    def display_chatbot(self, disaster_type='general', language='en'):
        """Display chatbot interface in Streamlit"""
        
        st.markdown("### 🤖 Disaster AI Assistant")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style='background: #1565c0; color: #ffffff; padding: 0.8rem; margin: 0.5rem 0; 
                                border-radius: 10px; text-align: right;'>
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: #263238; color: #e0e0e0; padding: 0.8rem; margin: 0.5rem 0; 
                                border-radius: 10px;'>
                        <strong>🤖 Assistant:</strong><br>{message['content'].replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me anything about disaster safety...",
                placeholder="e.g., What to do during earthquake?",
                key='chat_input',
                label_visibility='collapsed'
            )
        
        with col2:
            send_btn = st.button("Send", type="primary", use_container_width=True)
        
        if send_btn and user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get bot response
            response = self.get_response(user_input, disaster_type, language)
            
            # Add bot response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            # Clear input and rerun
            st.rerun()
        
        # Quick action buttons
        st.markdown("#### Quick Questions:")
        
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        
        questions = {
            'en': [
                "What to do during flood?",
                "Emergency numbers",
                "How to prepare?",
                "First aid basics"
            ],
            'hi': [
                "बाढ़ के दौरान क्या करें?",
                "आपातकालीन नंबर",
                "कैसे तैयार रहें?",
                "प्राथमिक चिकित्सा"
            ]
        }
        
        qs = questions.get(language, questions['en'])
        
        for col, q in zip([col_q1, col_q2, col_q3, col_q4], qs):
            with col:
                if st.button(q, use_container_width=True):
                    st.session_state.chat_history.append({'role': 'user', 'content': q})
                    response = self.get_response(q, disaster_type, language)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


# Test function
def test_chatbot():
    """Test disaster chatbot"""
    bot = DisasterChatbot()
    
    print("Testing Disaster Chatbot...")
    print("="*70)
    
    test_queries = [
        ("hello", "general"),
        ("what to do during flood", "flood"),
        ("earthquake preparation", "earthquake"),
        ("emergency numbers", "general"),
        ("heat stroke", "heatwave"),
        ("landslide warning", "landslide"),
        ("cyclone categories", "cyclone"),
        ("first aid", "general"),
        ("pet safety", "general"),
    ]
    
    for query, dtype in test_queries:
        response = bot.get_response(query, dtype)
        print(f"\nQ: {query} (type: {dtype})")
        print(f"A: {response[:80]}...")
    
    print("\n" + "="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_chatbot()