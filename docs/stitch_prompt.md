# Frontend UI Prompt for Google Stitch

**Role:** You are an expert UX/UI designer and Next.js frontend developer. 

**Task:** Generate modern, premium frontend UI mockups and Next.js components for an "AI Restaurant Recommendation Engine".

**Framework:** Next.js (React).

## Design & Aesthetic Guidelines
- **Visual Excellence:** The design must be visually stunning, premium, and dynamic. Avoid generic or flat designs.
- **Theme:** Implement a sleek, modern dark mode by default with vibrant, harmonious accent colors (e.g., deep purples, neon blues, or warm food-inspired gradients).
- **Styling:** Utilize glassmorphism effects (frosted glass, subtle blurs) for cards and modals.
- **Typography:** Use modern, clean fonts like *Inter*, *Outfit*, or *Plus Jakarta Sans*.
- **Micro-interactions:** Include subtle hover effects, smooth transitions, and loading micro-animations to make the interface feel alive and highly responsive.

## Core Screens & Components to Generate

### 1. The Input Interface (Hero Section)
This is where the user provides their context. It should look like a premium search engine or AI chat interface rather than a boring corporate form.
- **Header:** Clean branding for "Zomato AI" with a short, catchy subtitle.
- **Static Context Inputs:**
  - Location (Text Input: e.g., "Koramangala, Bangalore")
  - Budget for Two (Dropdown/Pills: "Under ₹500", "₹500 - ₹1500", "Above ₹1500")
  - Cuisine Preference (Optional Text Input or selectable chips: e.g., "Italian, Sushi")
- **The "Nuance" Input (The Star Feature):** A prominent, inviting textarea asking "What's the vibe?" (e.g., "A quiet romantic place for an anniversary dinner").
- **Call to Action:** A prominent, glowing "Find Recommendations" button.

### 2. Loading / Processing State
- When the user clicks submit, show a beautiful loading state that indicates the AI is "Analyzing preferences...", "Filtering locations...", and "Consulting the LLM...". Use skeleton loaders or dynamic pulsing orbs.

### 3. The Results Interface (Recommendation Cards)
- Display the Top 3 to 5 restaurant recommendations seamlessly.
- **Card Layout:** Each recommendation should be a beautifully styled card.
- **Content:**
  - Restaurant Name (prominent)
  - **AI Rationale:** A distinct, highlighted section within the card where the AI explains *why* it chose this restaurant based on the user's "vibe" input.
  - Basic details (Location, Rating, Cost) formatted elegantly as metadata tags.
