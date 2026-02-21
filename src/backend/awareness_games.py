"""
Disaster Awareness Games & Quizzes
Educational mini-games to train users about disaster preparedness
— 40+ questions, 5 scenarios, randomized on each play
"""

import streamlit as st
import random
from datetime import datetime


class DisasterGames:
    """Interactive games and quizzes for disaster awareness"""
    
    def __init__(self):
        # ── Large question bank ─────────────────────────────────────────
        self.quizzes = {
            'flood': [
                {"question": "What should you do FIRST when a flood warning is issued?",
                 "options": ["Take photos", "Move to higher ground", "Call friends", "Pack everything"],
                 "correct": 1, "explanation": "Moving to higher ground immediately is the top priority."},
                {"question": "Can you drive through flood water?",
                 "options": ["Yes, always", "No, never", "Only if shallow", "Only in 4WD"],
                 "correct": 1, "explanation": "Never drive through flood water — just 6 inches can sweep away a car!"},
                {"question": "How much water per person per day do you need in an emergency?",
                 "options": ["1 cup", "1 liter", "1 gallon (4L)", "5 gallons"],
                 "correct": 2, "explanation": "You need 1 gallon (4 liters) of water per person per day."},
                {"question": "What should you do with electricity during a flood?",
                 "options": ["Leave it on", "Turn off at mains", "Only turn off lights", "Use normally"],
                 "correct": 1, "explanation": "Turn off electricity at the main switch to prevent electrocution."},
                {"question": "After a flood, is the tap water safe to drink?",
                 "options": ["Yes, always", "No, boil it first", "Only if clear", "Yes, if cold"],
                 "correct": 1, "explanation": "Flood water contaminates supply — always boil water or use purification."},
                {"question": "What is the safest place during a flood inside a building?",
                 "options": ["Basement", "Ground floor", "Top floor / roof", "Bathroom"],
                 "correct": 2, "explanation": "The highest floor or roof is safest as water rises from below."},
                {"question": "Which of these should be in a waterproof bag during floods?",
                 "options": ["Clothes", "Food", "Important documents", "Toys"],
                 "correct": 2, "explanation": "Important documents like IDs, insurance papers should be waterproofed."},
                {"question": "How deep must flood water be to knock a person off their feet?",
                 "options": ["6 inches", "2 feet", "4 feet", "1 foot"],
                 "correct": 0, "explanation": "Just 6 inches (15 cm) of fast-moving water can knock you down!"},
            ],
            'earthquake': [
                {"question": "During an earthquake, what should you do?",
                 "options": ["Run outside", "Stand in doorway", "DROP-COVER-HOLD", "Hide under bed"],
                 "correct": 2, "explanation": "DROP under sturdy furniture, COVER your head, HOLD ON until shaking stops."},
                {"question": "Is it safe to use elevators during an earthquake?",
                 "options": ["Yes", "No", "Only in emergency", "Depends on building"],
                 "correct": 1, "explanation": "NEVER use elevators during earthquake — always use stairs!"},
                {"question": "What causes most earthquake injuries?",
                 "options": ["Ground shaking", "Falling objects", "Running outside", "Aftershocks"],
                 "correct": 1, "explanation": "Most injuries come from falling objects — that's why you COVER your head!"},
                {"question": "What is an aftershock?",
                 "options": ["A bigger earthquake", "Electric shock", "Smaller quake after main one", "Warning before earthquake"],
                 "correct": 2, "explanation": "Aftershocks are smaller earthquakes that follow the main one, sometimes for weeks."},
                {"question": "Where is the safest place during an earthquake indoors?",
                 "options": ["Near windows", "Under a sturdy table", "In a hallway", "Against outer wall"],
                 "correct": 1, "explanation": "Under a sturdy table protects you from falling debris."},
                {"question": "What should you keep near your bed for earthquake preparedness?",
                 "options": ["Television", "Shoes and flashlight", "Heavy bookshelf", "Nothing"],
                 "correct": 1, "explanation": "Shoes protect from broken glass, flashlight helps if power is out."},
                {"question": "If you're outdoors during an earthquake, you should…",
                 "options": ["Run into nearest building", "Move to open area", "Stand under a tree", "Lie flat anywhere"],
                 "correct": 1, "explanation": "Move to an open area away from buildings, power lines, and trees."},
                {"question": "Which magnitude earthquake can cause structural damage?",
                 "options": ["2.0", "3.5", "5.0+", "Only 8.0+"],
                 "correct": 2, "explanation": "Magnitude 5.0 and above can cause moderate to severe structural damage."},
            ],
            'cyclone': [
                {"question": "What does the 'EYE' of a cyclone mean?",
                 "options": ["Most dangerous part", "Calm center", "Where it starts", "Where it ends"],
                 "correct": 1, "explanation": "The eye is the calm center — but don't go outside! Dangerous winds return."},
                {"question": "What should you do with windows during a cyclone?",
                 "options": ["Open them wide", "Board them up", "Leave them cracked", "Break them"],
                 "correct": 1, "explanation": "Board up windows to prevent shattering from flying debris."},
                {"question": "What is the India Meteorological Department's helpline?",
                 "options": ["100", "112", "1800-180-1717", "108"],
                 "correct": 2, "explanation": "IMD's helpline 1800-180-1717 provides weather and cyclone warnings."},
                {"question": "Which room is safest during a cyclone?",
                 "options": ["Room with large windows", "Interior room without windows", "Garage", "Attic"],
                 "correct": 1, "explanation": "An interior room without windows minimizes risk from flying glass and debris."},
                {"question": "After a cyclone passes, what should you NOT do?",
                 "options": ["Check for injuries", "Touch fallen power lines", "Listen to radio", "Help neighbors"],
                 "correct": 1, "explanation": "NEVER touch fallen power lines — they may still be live and deadly."},
                {"question": "A cyclone with winds above 120 knots is called?",
                 "options": ["Severe cyclone", "Very severe cyclone", "Super cyclonic storm", "Hurricane"],
                 "correct": 2, "explanation": "Above 120 knots is classified as a Super Cyclonic Storm in the Indian Ocean."},
                {"question": "What colour warning means cyclone expected in 12 hours?",
                 "options": ["Green", "Yellow", "Orange", "Red"],
                 "correct": 3, "explanation": "Red warning means the cyclone is expected to hit within 12 hours."},
                {"question": "Which coast of India faces more cyclones?",
                 "options": ["West coast", "East coast", "Both equally", "Neither"],
                 "correct": 1, "explanation": "India's east coast (Bay of Bengal) faces significantly more cyclones."},
            ],
            'landslide': [
                {"question": "What is the most common trigger for landslides?",
                 "options": ["Wind", "Heavy rainfall", "Sunlight", "Cold weather"],
                 "correct": 1, "explanation": "Heavy or prolonged rainfall saturates soil, making slopes unstable."},
                {"question": "Which is a warning sign of an impending landslide?",
                 "options": ["Clear skies", "New cracks in ground/walls", "Birds singing", "Temperature drop"],
                 "correct": 1, "explanation": "New cracks in ground, walls, or pavement indicate the slope is moving."},
                {"question": "If you hear a rumbling sound from a hillside, you should…",
                 "options": ["Investigate", "Run perpendicular to the slope", "Stay still", "Run towards it"],
                 "correct": 1, "explanation": "Move laterally (perpendicular) away from the landslide path."},
                {"question": "Which human activity increases landslide risk?",
                 "options": ["Planting trees", "Deforestation", "Farming on flat land", "Swimming"],
                 "correct": 1, "explanation": "Deforestation removes root systems that hold soil in place on slopes."},
                {"question": "After a landslide, what is the biggest secondary risk?",
                 "options": ["Sunburn", "More landslides", "Wind", "Cold"],
                 "correct": 1, "explanation": "After one landslide, the area is weakened and more slides are likely."},
                {"question": "What should you do if trapped by landslide debris?",
                 "options": ["Scream loudly", "Tap on hard surfaces to signal rescuers", "Try to dig out alone", "Sleep"],
                 "correct": 1, "explanation": "Tapping on pipes/walls uses less energy and sound travels through structures."},
            ],
            'heatwave': [
                {"question": "At what body temperature is heat stroke dangerous?",
                 "options": ["37°C", "38°C", "40°C (104°F)+", "42°C only"],
                 "correct": 2, "explanation": "Body temp above 40°C (104°F) is a medical emergency — call 108 immediately!"},
                {"question": "What is the best drink during a heatwave?",
                 "options": ["Alcohol", "Coffee", "Water with ORS", "Soda"],
                 "correct": 2, "explanation": "Water and ORS (oral rehydration salts) replace lost electrolytes."},
                {"question": "Peak heat hours to avoid going outdoors are…",
                 "options": ["6-9 AM", "12-3 PM", "5-8 PM", "9-11 PM"],
                 "correct": 1, "explanation": "12 PM to 3 PM has the most intense heat — stay indoors if possible."},
                {"question": "A person with heat stroke has hot, red skin and NO sweating. What should you do?",
                 "options": ["Give hot tea", "Cool them with cold water & call 108", "Let them walk", "Wait"],
                 "correct": 1, "explanation": "Cool the person immediately and call 108 — heat stroke is life-threatening."},
                {"question": "How often should you drink water during extreme heat?",
                 "options": ["Once a day", "Only when thirsty", "Every 20 minutes", "Every 2 hours"],
                 "correct": 2, "explanation": "Drink water every 20 minutes during extreme heat, even if not thirsty."},
                {"question": "Which clothing is best in a heatwave?",
                 "options": ["Dark, tight clothes", "Light, loose cotton", "Synthetic fabric", "Wool"],
                 "correct": 1, "explanation": "Light-coloured, loose cotton clothing allows air circulation and sweat evaporation."},
                {"question": "What is the difference between heat exhaustion and heat stroke?",
                 "options": ["Same thing", "Heat stroke is more severe", "Heat exhaustion is worse", "No difference"],
                 "correct": 1, "explanation": "Heat stroke is a life-threatening emergency; heat exhaustion is serious but less severe."},
            ],
            'general': [
                {"question": "What is India's national emergency number?",
                 "options": ["100", "101", "112", "108"],
                 "correct": 2, "explanation": "112 is the national emergency number for all emergencies in India!"},
                {"question": "How many days of supplies should an emergency kit have?",
                 "options": ["1 day", "3 days", "1 week", "1 month"],
                 "correct": 1, "explanation": "Minimum 3 days of water, food, and supplies for each person."},
                {"question": "What does NDMA stand for?",
                 "options": ["National Defense Military Agency", "National Disaster Management Authority", "New Delhi Metro Authority", "National Data Monitor Agency"],
                 "correct": 1, "explanation": "National Disaster Management Authority handles disaster preparedness in India."},
                {"question": "In CPR, how many chest compressions before 2 rescue breaths?",
                 "options": ["10", "15", "30", "50"],
                 "correct": 2, "explanation": "The standard is 30 compressions followed by 2 rescue breaths."},
                {"question": "What is the easiest way to purify water in an emergency?",
                 "options": ["Freeze it", "Boil for 1 minute", "Leave in sunlight forever", "Shake it"],
                 "correct": 1, "explanation": "Boiling water for 1 minute kills most pathogens — simplest purification."},
                {"question": "Which of these should NOT be in an emergency kit?",
                 "options": ["Flashlight", "First aid kit", "Heavy furniture", "Phone charger"],
                 "correct": 2, "explanation": "Emergency kits must be portable — heavy furniture can't be carried!"},
                {"question": "What is the NDMA helpline number?",
                 "options": ["100", "1098", "1078", "112"],
                 "correct": 2, "explanation": "1078 is the NDMA (National Disaster Management Authority) helpline."},
                {"question": "Emergency supplies should be stored in…",
                 "options": ["A locked safe", "An easily accessible location", "The car trunk only", "The basement"],
                 "correct": 1, "explanation": "Store emergency supplies where they're easily accessible during a crisis."},
            ]
        }
        
        # ── Scenarios (one per disaster type) ───────────────────────────
        self.scenarios = [
            {
                'title': "🌊 Flood Escape Challenge",
                'description': "You're at home and water is rising rapidly. What's your plan?",
                'steps': [
                    {'action': "Turn off electricity at mains", 'correct': True, 'points': 10},
                    {'action': "Pack all your belongings", 'correct': False, 'points': 0},
                    {'action': "Move to highest floor / roof", 'correct': True, 'points': 20},
                    {'action': "Call emergency services (112)", 'correct': True, 'points': 15},
                    {'action': "Walk through the flood water to neighbors", 'correct': False, 'points': 0},
                    {'action': "Signal for help with flashlight / whistle", 'correct': True, 'points': 15},
                    {'action': "Wait on roof if rescue needed", 'correct': True, 'points': 10},
                ]
            },
            {
                'title': "🔥 Earthquake Survival",
                'description': "You're in a 5-story office building when shaking starts. What do you do?",
                'steps': [
                    {'action': "DROP to the ground immediately", 'correct': True, 'points': 15},
                    {'action': "Run to the elevator", 'correct': False, 'points': 0},
                    {'action': "Take COVER under a sturdy desk", 'correct': True, 'points': 20},
                    {'action': "HOLD ON until shaking stops", 'correct': True, 'points': 15},
                    {'action': "Jump out of a window", 'correct': False, 'points': 0},
                    {'action': "After shaking, use stairs to exit", 'correct': True, 'points': 10},
                    {'action': "Check for gas leaks before leaving", 'correct': True, 'points': 10},
                ]
            },
            {
                'title': "🌪️ Cyclone Response",
                'description': "A severe cyclone warning has been issued for your coastal city. You have 6 hours. What do you do?",
                'steps': [
                    {'action': "Board up windows and secure doors", 'correct': True, 'points': 15},
                    {'action': "Go to the beach to watch the waves", 'correct': False, 'points': 0},
                    {'action': "Fill containers with drinking water", 'correct': True, 'points': 15},
                    {'action': "Charge all phones and power banks", 'correct': True, 'points': 10},
                    {'action': "Move to designated cyclone shelter", 'correct': True, 'points': 20},
                    {'action': "Leave your car parked under trees", 'correct': False, 'points': 0},
                    {'action': "Secure loose outdoor objects", 'correct': True, 'points': 10},
                ]
            },
            {
                'title': "⛰️ Landslide Alert",
                'description': "You notice cracks in the road near your hillside home and hear rumbling. Rain has been heavy for 3 days. What do you do?",
                'steps': [
                    {'action': "Evacuate immediately away from hillside", 'correct': True, 'points': 25},
                    {'action': "Stay home and wait to see what happens", 'correct': False, 'points': 0},
                    {'action': "Alert neighbors of danger", 'correct': True, 'points': 15},
                    {'action': "Call disaster management (1078)", 'correct': True, 'points': 15},
                    {'action': "Go investigate the cracks alone", 'correct': False, 'points': 0},
                    {'action': "Move to a flat, open area", 'correct': True, 'points': 10},
                    {'action': "Take important documents with you", 'correct': True, 'points': 5},
                ]
            },
            {
                'title': "🌡️ Heatwave Emergency",
                'description': "It's 47°C outside and your elderly neighbor has collapsed. Their skin is hot, red, and they're confused. What do you do?",
                'steps': [
                    {'action': "Call ambulance (108) immediately", 'correct': True, 'points': 25},
                    {'action': "Move person to cool shade", 'correct': True, 'points': 15},
                    {'action': "Give them hot tea", 'correct': False, 'points': 0},
                    {'action': "Cool body with cold water/wet cloth", 'correct': True, 'points': 15},
                    {'action': "Fan them aggressively", 'correct': True, 'points': 10},
                    {'action': "Force them to walk around", 'correct': False, 'points': 0},
                    {'action': "Place ice packs on neck, armpits, groin", 'correct': True, 'points': 10},
                ]
            },
        ]
    
    def _get_random_questions(self, disaster_type='general', count=8):
        """Get a random subset of questions for a quiz session."""
        pool = list(self.quizzes.get(disaster_type, self.quizzes['general']))
        # Add some general questions too
        if disaster_type != 'general':
            pool += list(self.quizzes['general'])
        random.shuffle(pool)
        return pool[:count]

    def display_quiz_game(self, disaster_type='general'):
        """Display interactive quiz game with random questions."""
        
        st.markdown("### 🎯 Disaster Knowledge Quiz")
        
        # Initialize game state — generate new questions when starting fresh
        if 'quiz_state' not in st.session_state or st.session_state.quiz_state.get('_dtype') != disaster_type:
            questions = self._get_random_questions(disaster_type, count=8)
            st.session_state.quiz_state = {
                'current_q': 0,
                'score': 0,
                'answered': [],
                'questions': questions,
                '_dtype': disaster_type,
            }
        
        state = st.session_state.quiz_state
        questions = state['questions']
        
        if state['current_q'] < len(questions):
            q = questions[state['current_q']]
            
            # Progress
            st.progress((state['current_q'] + 1) / len(questions))
            st.markdown(f"**Question {state['current_q'] + 1} of {len(questions)}**")
            
            col1, col2 = st.columns([3, 1])
            with col2:
                st.metric("Score", f"{state['score']}/{state['current_q']*10}")
            
            # Question
            st.markdown(f"#### {q['question']}")
            
            selected = st.radio(
                "Select your answer:",
                options=range(len(q['options'])),
                format_func=lambda x: q['options'][x],
                key=f"q_{state['current_q']}_{disaster_type}"
            )
            
            if st.button("Submit Answer", type="primary"):
                if selected == q['correct']:
                    st.success("✅ Correct! +10 points")
                    st.info(f"💡 {q['explanation']}")
                    state['score'] += 10
                else:
                    st.error(f"❌ Wrong! Correct answer: {q['options'][q['correct']]}")
                    st.info(f"💡 {q['explanation']}")
                
                state['answered'].append(selected == q['correct'])
                state['current_q'] += 1
                
                if state['current_q'] < len(questions):
                    st.button("Next Question →")
                
                st.rerun()
        
        else:
            # Quiz complete
            st.balloons()
            
            total_questions = len(questions)
            percentage = (state['score'] / (total_questions * 10)) * 100
            
            st.markdown("## 🎉 Quiz Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Final Score", f"{state['score']}/{total_questions*10}")
            with col2:
                st.metric("Percentage", f"{percentage:.0f}%")
            with col3:
                correct = sum(state['answered'])
                st.metric("Correct Answers", f"{correct}/{total_questions}")
            
            if percentage >= 80:
                st.success("🌟 Excellent! You're well-prepared for disasters!")
            elif percentage >= 60:
                st.info("👍 Good job! Review the wrong answers to improve.")
            else:
                st.warning("📚 Keep learning! Practice makes perfect.")
            
            # Restart / Refresh
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Play Again (New Questions)", type="primary"):
                    del st.session_state.quiz_state
                    st.rerun()
            with c2:
                if st.button("🔁 Retry Same Questions"):
                    st.session_state.quiz_state = {
                        'current_q': 0,
                        'score': 0,
                        'answered': [],
                        'questions': questions,
                        '_dtype': disaster_type,
                    }
                    st.rerun()
    
    def display_scenario_challenge(self):
        """Display scenario-based challenge game."""
        
        st.markdown("### 🎮 Disaster Scenario Challenge")
        
        # Let user pick scenario
        if 'scenario_idx' not in st.session_state:
            st.session_state.scenario_idx = 0
        
        scenario_titles = [s['title'] for s in self.scenarios]
        selected_idx = st.selectbox("Choose a scenario:", range(len(scenario_titles)),
                                     format_func=lambda i: scenario_titles[i],
                                     key='scenario_picker')
        
        scenario = self.scenarios[selected_idx]
        
        st.markdown(f"#### {scenario['title']}")
        st.info(scenario['description'])
        
        st.markdown("**Select the RIGHT actions (you can choose multiple):**")
        
        # Track selections with unique keys per scenario
        selections = []
        for idx, step in enumerate(scenario['steps']):
            checked = st.checkbox(step['action'], key=f"scenario_{selected_idx}_step_{idx}")
            if checked:
                selections.append(idx)
        
        max_score = sum(s['points'] for s in scenario['steps'] if s['correct'])
        
        if st.button("Check My Plan", type="primary"):
            score = 0
            feedback = []
            
            for idx in selections:
                step = scenario['steps'][idx]
                if step['correct']:
                    score += step['points']
                    feedback.append(f"✅ {step['action']} — Correct! (+{step['points']} pts)")
                else:
                    feedback.append(f"❌ {step['action']} — Not recommended!")
            
            for idx, step in enumerate(scenario['steps']):
                if step['correct'] and idx not in selections:
                    feedback.append(f"⚠️ Missed: {step['action']} (+{step['points']} pts)")
            
            st.markdown("---")
            st.markdown("### 📊 Results")
            
            for fb in feedback:
                if "✅" in fb:
                    st.success(fb)
                elif "❌" in fb:
                    st.error(fb)
                else:
                    st.warning(fb)
            
            st.metric("Total Score", f"{score}/{max_score} points")
            
            pct = (score / max_score * 100) if max_score else 0
            if pct >= 80:
                st.success("🌟 Excellent survival plan!")
            elif pct >= 50:
                st.info("👍 Good, but review the warnings above!")
            else:
                st.warning("⚠️ Practice more to improve your response!")
    
    def display_memory_game(self):
        """Display disaster safety memory card game."""
        
        st.markdown("### 🃏 Emergency Numbers Memory Game")
        st.info("Match the emergency service with its number!")
        
        pairs = [
            ("National Emergency", "112"),
            ("Ambulance", "108"),
            ("Police", "100"),
            ("Fire", "101"),
            ("Disaster Mgmt (NDMA)", "1078"),
            ("Women Helpline", "1091"),
            ("Child Helpline", "1098"),
            ("Railway Emergency", "139"),
        ]
        
        if 'memory_seed' not in st.session_state:
            st.session_state.memory_seed = random.randint(0, 99999)
        
        rng = random.Random(st.session_state.memory_seed)
        
        services = [p[0] for p in pairs]
        numbers = [p[1] for p in pairs]
        shuffled_services = list(services)
        shuffled_numbers = list(numbers)
        rng.shuffle(shuffled_services)
        rng.shuffle(shuffled_numbers)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Services**")
            for i, service in enumerate(shuffled_services):
                st.markdown(f"**{i+1}.** {service}")
        
        with col2:
            st.markdown("**Numbers**")
            for i, number in enumerate(shuffled_numbers):
                st.markdown(f"**{chr(65+i)}.** {number}")
        
        st.markdown("---")
        
        # Let user match via dropdowns
        st.markdown("**Match each service to its number:**")
        
        user_matches = {}
        for i, service in enumerate(shuffled_services):
            choice = st.selectbox(
                f"{i+1}. {service}",
                options=["-- Select --"] + [f"{chr(65+j)}. {n}" for j, n in enumerate(shuffled_numbers)],
                key=f"match_{i}_{st.session_state.memory_seed}"
            )
            if choice != "-- Select --":
                user_matches[service] = choice.split(". ", 1)[1]
        
        if st.button("Check Answers", type="primary"):
            correct_map = dict(pairs)
            score = 0
            total = len(pairs)
            for service, user_num in user_matches.items():
                if correct_map.get(service) == user_num:
                    score += 1
                    st.success(f"✅ {service} → {user_num}")
                else:
                    st.error(f"❌ {service} → {user_num} (correct: {correct_map.get(service, '?')})")
            
            unmatched = total - len(user_matches)
            if unmatched > 0:
                st.warning(f"⚠️ {unmatched} services not matched.")
            
            st.metric("Score", f"{score}/{total}")
            
            if score == total:
                st.balloons()
                st.success("🌟 Perfect! You know all the numbers!")
        
        if st.button("🔄 Shuffle & Try Again"):
            st.session_state.memory_seed = random.randint(0, 99999)
            st.rerun()


def test_games():
    """Test disaster games"""
    games = DisasterGames()
    
    print("Testing Disaster Games...")
    print("="*70)
    
    for dtype, qs in games.quizzes.items():
        print(f"\n{dtype}: {len(qs)} questions")
    
    print(f"\nScenarios: {len(games.scenarios)}")
    
    sample = games._get_random_questions('flood', 5)
    print(f"\nRandom 5 flood questions:")
    for q in sample:
        print(f"  - {q['question'][:60]}...")
    
    print("\n" + "="*70)
    print("✅ Test complete!")


if __name__ == "__main__":
    test_games()