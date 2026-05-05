import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add backend directory to Python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend')))

from phase3 import build_prompt, load_data
from phase4 import get_recommendations

# Load environment variables (for local dev, Streamlit Cloud will use its Secrets management)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

st.set_page_config(page_title="Zomato AI Concierge", page_icon="🍔", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #fbf9f8;
        color: #1b1c1c;
    }
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #5d5f5f;
        margin-bottom: 40px;
    }
    .recommendation-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 4px solid #b7122a;
    }
    .rationale {
        background-color: #f5f3f3;
        padding: 15px;
        border-radius: 8px;
        font-style: italic;
        color: #5d5f5f;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">ZOMATO <span style="color:#E23744;">AI</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your personal culinary concierge. Tell us what you\'re craving.</p>', unsafe_allow_html=True)

# Fetch dynamic locations
@st.cache_data
def get_locations():
    data = load_data()
    locations = set()
    for item in data:
        loc = item.get("location", "").strip()
        if loc:
            locations.add(loc)
    return sorted(list(locations))

locations = get_locations()

# Form Inputs
with st.form("preferences_form"):
    st.markdown("### Describe your vibe")
    nuance = st.text_area("e.g., A quiet romantic place for an anniversary dinner with great wine...", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("LOCATION", options=["Select a location..."] + locations)
        budget = st.selectbox("BUDGET", options=["low", "medium", "high"], format_func=lambda x: {"low": "Under ₹500", "medium": "₹500 - ₹1500", "high": "Above ₹1500"}.get(x, x))
    with col2:
        cuisine = st.text_input("CUISINE", placeholder="e.g. Italian, Sushi")
        rating = st.selectbox("MINIMUM RATING", options=["Any", "3.5+", "4.0+", "4.5+"])
        
    submitted = st.form_submit_button("Find Recommendations", type="primary")

if submitted:
    if location == "Select a location...":
        st.error("Please select a location.")
    else:
        payload = {
            "staticContext": {
                "location": location,
                "budget": budget,
                "cuisine": cuisine if cuisine else "Any",
                "rating": rating
            },
            "nuanceContext": nuance if nuance else "None provided"
        }
        
        with st.spinner('Consulting Groq LLM...'):
            prompt, error = build_prompt(payload)
            
            if error:
                st.error(f"Error: {error}")
            else:
                results = get_recommendations(prompt)
                
                if "error" in results:
                    st.error(f"API Error: {results['error']}")
                elif "recommendations" in results and len(results["recommendations"]) > 0:
                    st.success("Here are your top AI-curated picks!")
                    
                    food_images = [
                        "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=800&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?q=80&w=800&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1484723091798-dffc122598ad?q=80&w=800&auto=format&fit=crop"
                    ]
                    
                    for i, rec in enumerate(results["recommendations"]):
                        img_url = food_images[i % len(food_images)]
                        
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <img src="{img_url}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:15px; opacity:0.9;">
                            <h2>#{i+1} {rec['name']}</h2>
                            <div class="rationale">
                                <strong>Why it fits your vibe:</strong><br/>
                                {rec['rationale']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No recommendations found. Try adjusting your preferences.")
