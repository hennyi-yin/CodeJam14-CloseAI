import os
import logging
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Config:
    """Configuration settings for the car sales assistant"""
    OPENAI_MODEL: str = "gpt-4o-mini"
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"  # sentence-transformers model
    MAX_TOKENS: int = 300
    TEMPERATURE: float = 0.7
    TOP_K_RESULTS: int = 3
    MAX_HISTORY_TURNS: int = 10

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class CarSalesAssistant:
    def __init__(self, config: Optional[Config] = None, api_key=None):
        """Initialize the car sales assistant"""
        self.config = config or Config()
        self.api_key = api_key
        self._validate_config()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Initialize sentence transformer
        self.model = SentenceTransformer(self.config.MODEL_NAME)
        
        # Initialize storage
        self.embeddings = None
        self.documents = None
        self.conversation_history = []
        self.last_recommendations = []  # Cache for recommendations
    
    def _validate_config(self) -> None:
        """Validate configuration settings"""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def format_car_document(self, car_data: Dict[str, Any]) -> str:
        """Format car data into a readable string"""
        try:
            return (
                f"Type: {car_data['Type']}, "
                f"Stock: {car_data['Stock']}, "
                f"VIN: {car_data['VIN']}, "
                f"Year: {car_data['Year']}, "
                f"Make: {car_data['Make']}, "
                f"Model: {car_data['Model']}, "
                f"ModelNumber: {car_data['ModelNumber']}, "
                f"Exterior Color: {car_data['ExteriorColor']}, "
                f"Interior Color: {car_data['InteriorColor']}, "
                f"Transmission: {car_data['Transmission']}, "
                f"Mileage: {car_data['Miles']:,}mi, "
                f"Selling Price: ${car_data['SellingPrice']}, "
                f"Options: {car_data['Options']}, "
                f"Style Description: {car_data['Style_Description']}, "
                f"Engine Block Type: {car_data['Engine_Block_Type']}, "
                f"Engine Aspiration Type: {car_data['Engine_Aspiration_Type']}, "
                f"Engine Description: {car_data['Engine_Description']}, "
                f"Transmission Description: {car_data['Transmission_Description']}, "
                f"Drivetrain: {car_data['Drivetrain']}, "
                f"Fuel Type: {car_data['Fuel_Type']}, "
                f"City MPG: {car_data['CityMPG']}mpg, "
                f"Highway MPG: {car_data['HighwayMPG']}mpg, "
                f"EPA Classification: {car_data['EPAClassification']}, "
                f"Wheelbase Code: {car_data['Wheelbase_Code']}, "
                f"Market Class: {car_data['MarketClass']}, "
                f"Passenger Capacity: {car_data['PassengerCapacity']}, "
                f"Engine Displacement: {car_data['EngineDisplacementCubicInches']}"
            )
        except KeyError as e:
            logger.error(f"Missing required field in car data: {e}")
            return ""
    
    def load_car_data(self, csv_path: str) -> None:
        """Load and embed car data from CSV file"""
        try:
            logger.info(f"Loading car data from {csv_path}")
            df = pd.read_csv(csv_path)
            
            self.documents = []
            for _, row in df.iterrows():
                doc = self.format_car_document(row)
                if doc:
                    self.documents.append(doc)
            
            if not self.documents:
                logger.warning("No valid car documents to load")
                return
            
            logger.info("Creating embeddings for car documents")
            self.embeddings = self.model.encode(self.documents)
            
            logger.info(f"Successfully loaded {len(self.documents)} cars")
            
        except Exception as e:
            logger.error(f"Error loading car data: {str(e)}")
            raise
    
    def is_reference_query(self, query: str) -> Tuple[bool, int]:
        """Check if query is referencing a previous recommendation"""
        reference_mapping = {
            'first': 0, 'first one': 0, '1': 0,
            'second': 1, 'second one': 1, '2': 1,
            'third': 2, 'third one': 2, '3': 2
        }
        
        query_lower = query.lower()
        for ref, idx in reference_mapping.items():
            if ref in query_lower:
                logger.info(f"Detected reference query: {ref} -> index {idx}")
                return True, idx
        return False, -1
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding using sentence transformer"""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            raise
    
    def get_relevant_cars(self, query: str, threshold: float = 0.2) -> str:
        """Get relevant cars based on query"""
        if self.embeddings is None or not self.documents:
            logger.warning("No car data available")
            return "No car data available"
        
        # Check if query references previous recommendations
        is_ref, ref_idx = self.is_reference_query(query)
        if is_ref and self.last_recommendations:
            if ref_idx < len(self.last_recommendations):
                logger.info(f"Using cached recommendation at index {ref_idx}")
                return self.last_recommendations[ref_idx]
        
        try:
            logger.info(f"Creating embedding for query: {query}")
            query_embedding = self.get_embedding(query)
            
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            
            sorted_indices = np.argsort(similarities)[::-1]
            scores = similarities[sorted_indices]
            
            relevant_indices = []
            for i, score in enumerate(scores):
                if score >= threshold or len(relevant_indices) < self.config.TOP_K_RESULTS:
                    relevant_indices.append(sorted_indices[i])
                    logger.debug(f"Selected document {i} with score {score:.3f}")
                if len(relevant_indices) >= self.config.TOP_K_RESULTS:
                    break
            
            self.last_recommendations = [self.documents[i] for i in relevant_indices]
            recommendations = "\n".join(self.last_recommendations)
            
            logger.info(f"Found {len(relevant_indices)} relevant cars")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in get_relevant_cars: {str(e)}")
            return "Error retrieving car information"
    
    def create_system_prompt(self, relevant_cars: str) -> str:
        """Create general system prompt"""
        base_prompt = """You are Hennyi, an experienced car salesperson who is professional, adaptive, and focused on closing deals. Your responses should be brief but impactful, always aiming to move the conversation towards a sale while maintaining authenticity.

[CRITICAL RULES: 
1. Only recommend vehicles that exist in the provided csv file.
2. When encountering a vehicle with price showing as $0:
   - Do not mention the actual $0 price
   - Instead say "Price: Contact for special pricing"
   - If customer asks specifically about that vehicle's price, respond with "This vehicle has special pricing. I'd be happy to discuss the details in person or over the phone."
   - Focus on the vehicle's features and benefits
   - Encourage direct contact for pricing discussion
3. For all vehicles with regular pricing:
   - Always show the actual price
   - Be transparent about all costs
4. Never make up or guess prices]

[Vehicle Classification Rules]
    
Electric Vehicles (EV):
Pure electric vehicle
Examples: Tesla, Nissan Leaf
Hybrid Vehicles:
Combines gas engine and electric motor
Examples: Toyota Prius, Ford Fusion Hybrid
Traditional Vehicles:
Gas or diesel engines only

THINKING FRAMEWORK:

1. Customer Understanding Phase
- Interpret customer's explicit and implicit needs
- Analyze customer's communication style and mood
- Identify key buying signals or objections
- Consider customer's price sensitivity
- Map customer requests to available inventory

2. Vehicle Matching Process
- Compare customer needs with available inventory
- Consider multiple vehicle options
- Evaluate price alignment
- Assess feature relevance
- Prepare alternative suggestions

3. Response Strategy Development
- Choose appropriate communication style
- Structure information hierarchy
- Plan closing technique
- Prepare for potential objections
- Design next steps

Core Response Behaviors:

1. Response Style
- Keep all responses under 3 sentences unless specifically asked for details
- Always shows three possible options
- Lead with the most relevant information first
- Use natural, conversational language
- Maintain professionalism even when faced with casual or rude behavior

2. Sales Strategy
- Always include price ranges when mentioning specific models
- When introducing specific models, always bring proper length of details
- Respond to budget-related keywords (like "broke", "expensive", "cheap") with appropriate options
- When lacking inventory information, focus on general recommendations and invite store visits
- Look for opportunities to suggest viewing available vehicles in person

3. Customer Interaction
- Match the customer's communication style while staying professional
- Handle non-serious queries (like jokes) with brief, friendly responses before steering back to sales
- For unclear requests, provide one quick clarification question followed by a suggestion
- When faced with rudeness, respond once professionally then wait for serious queries
- When customer shows interest in test drives, guide them to click Appointment link: 

4. Information Hierarchy
- Price -> Features -> Technical details
- Always mention price ranges with vehicle suggestions
- 
- Keep technical explanations simple unless specifically asked for details
- Focus on practical benefits over technical specifications

5. Closing Techniques
- End each response with a subtle call to action
- When suggesting test drives, specifically mention the "Appointment" link : "https://www.example.com" for easy scheduling
- Suggest store visits or test drives when interest is shown
- Provide clear next steps for interested customers
- Be direct about availability and options

INTERNAL DIALOGUE GUIDELINES:

Before each response, think through:
1. Customer Profile
- What is their apparent budget level?
- What style of communication are they using?
- What signals are they giving about their interests?
- What potential objections might they have?

2. Product Selection
- Which vehicles in our inventory match their needs?
- What are the key selling points for these options?
- What alternatives should we have ready?
- How do our options align with their budget?

3. Sales Approach
- What tone should I use in my response?
- How can I move this conversation toward a sale?
- What would be the most effective call to action?
- How can I overcome potential objections?

Response Templates:
- For jokes/non-serious queries: Brief acknowledgment + one vehicle suggestion
- For rude comments: Make a joke and then steer the conversation to sales
- For specific vehicle interests: Price range + key features + next step
- For general queries: 2-3 options with price ranges + simple comparison
- For test drive inquiries: Mention the "https://www.example.com" link convenience (e.g., "Feel free to click the Appointment website above to schedule your test drive!")

When suggesting vehicles, use this format:
Brand Model Name Price Range Key Benefit Available Action

[CRITICAL RULE: Only recommend vehicles that exist in the provided csv file.]

Please base your recommendations on the following vehicle data:
"""
        
        return base_prompt + relevant_cars
    
    def create_reference_prompt(self, car_info: str) -> str:
        """Create system prompt for reference queries"""
        return """You are Hennyi, an experienced car salesperson. When discussing a specific car that was previously mentioned:
        1. Be consistent with the details you provided before
        2. Focus on this specific car's features and benefits
        3. Encourage test drive scheduling with link : "https://www.example.com"
        4. Maintain continuous context
        5. If you realize any previous information was incorrect, acknowledge it professionally
        
        Current vehicle information:
        """ + car_info
    
    def get_completion(self, user_query: str) -> str:
        """Get AI response for user query"""
        try:
            relevant_cars = self.get_relevant_cars(user_query)
            
            is_ref, _ = self.is_reference_query(user_query)
            
            messages = [
                {
                    "role": "system",
                    "content": self.create_reference_prompt(relevant_cars) if is_ref 
                              else self.create_system_prompt(relevant_cars)
                }
            ]
            
            if self.conversation_history:
                history_start = max(0, len(self.conversation_history) - 
                                 (self.config.MAX_HISTORY_TURNS * 2))
                messages.extend(self.conversation_history[history_start:])
            
            messages.append({"role": "user", "content": user_query})
            
            completion = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=messages,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            ai_response = completion.choices[0].message.content
            self.conversation_history.append({"role": "user", "content": user_query})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error in get_completion: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again."
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

def setup_assistant():
    """Main execution function"""
    # Set your OpenAI API key here
    system_config = json.load(open("data/config.json", "r", encoding="utf-8"))
    api_key = system_config["api_key"]
    os.environ['OPENAI_API_KEY'] = api_key
    config = Config()
    assistant = CarSalesAssistant(config, api_key)
    
    csv_path = system_config["csv_path"]  # Replace with your CSV path
    assistant.load_car_data(csv_path)
    
    return assistant
    
    #try:
    #    config = Config()
    #    assistant = CarSalesAssistant(config)
    #    
    #    csv_path = system_config["csv_path"]  # Replace with your CSV path
    #    assistant.load_car_data(csv_path)
    #    
    #    print("\nCar Sales Assistant is ready!")
    #    print("You can ask about vehicle recommendations, specifications, pricing, and more.")
    #    print("Type 'exit' to end the conversation or 'clear' to clear chat history.")
    #    
    #    while True:
    #        user_input = input("\nYou: ").strip()
    #        
    #        if user_input.lower() in ['exit', 'quit']:
    #            print("\nThank you for your time. Goodbye!")
    #            break
    #        
    #        if user_input.lower() == 'clear':
    #            assistant.clear_conversation()
    #            print("Conversation history cleared.")
    #            continue
    #        
    #        response = assistant.get_completion(user_input)
    #        print(f"\nHennyi: {response}")
    #        
    #except Exception as e:
    #    logger.error(f"Application error: {str(e)}")
    #    print("An error occurred. Please check the logs for details.")