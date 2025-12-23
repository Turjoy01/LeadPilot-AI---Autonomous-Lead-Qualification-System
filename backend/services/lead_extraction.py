from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from backend.config import settings
from backend.models.lead import LeadFields
import json

client = AsyncOpenAI(api_key=settings.openai_api_key)


class LeadExtractionService:
    """Service for extracting lead information using OpenAI function calling"""
    
    def __init__(self):
        self.extraction_tools = [
            {
                "type": "function",
                "function": {
                    "name": "update_lead_information",
                    "description": "Update lead information with extracted details from the conversation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Full name of the lead"
                            },
                            "email": {
                                "type": "string",
                                "description": "Email address of the lead"
                            },
                            "phone": {
                                "type": "string",
                                "description": "Phone number of the lead"
                            },
                            "service_interest": {
                                "type": "string",
                                "description": "Service or product the lead is interested in"
                            },
                            "budget": {
                                "type": "string",
                                "description": "Budget range or budget indication"
                            },
                            "timeline": {
                                "type": "string",
                                "description": "When they want to start or purchase"
                            },
                            "location": {
                                "type": "string",
                                "description": "Location or city of the lead"
                            },
                            "company": {
                                "type": "string",
                                "description": "Company name if mentioned"
                            }
                        }
                    }
                }
            }
        ]
    
    async def extract_from_conversation(
        self,
        messages: List[Dict[str, str]],
        current_fields: LeadFields
    ) -> Optional[LeadFields]:
        """
        Extract lead information from conversation using OpenAI function calling
        
        Args:
            messages: Conversation history
            current_fields: Current lead fields
        
        Returns:
            Updated LeadFields if new information extracted, None otherwise
        """
        try:
            # Create system message for extraction
            system_message = """You are a lead information extraction assistant. 
Your job is to extract contact and qualification information from conversations.
Only extract information that is explicitly mentioned by the user.
Call the update_lead_information function whenever you find new information."""
            
            # Prepare messages for OpenAI
            openai_messages = [
                {"role": "system", "content": system_message}
            ]
            openai_messages.extend(messages[-10:])  # Last 10 messages for context
            
            # Call OpenAI with function calling
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=openai_messages,
                tools=self.extraction_tools,
                tool_choice="auto",
                temperature=0.3  # Lower temperature for more consistent extraction
            )
            
            # Check if function was called
            message = response.choices[0].message
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "update_lead_information":
                        # Parse extracted data
                        extracted_data = json.loads(tool_call.function.arguments)
                        
                        # Merge with current fields (only update if new value provided)
                        updated_fields = current_fields.model_copy()
                        
                        for field, value in extracted_data.items():
                            if value and value.strip():  # Only update if non-empty
                                setattr(updated_fields, field, value)
                        
                        return updated_fields
            
            return None
            
        except Exception as e:
            print(f"Error extracting lead information: {e}")
            return None
    
    def get_missing_fields(self, fields: LeadFields) -> List[str]:
        """Get list of missing important fields"""
        missing = []
        
        if not fields.name:
            missing.append("name")
        if not fields.email and not fields.phone:
            missing.append("contact (email or phone)")
        if not fields.service_interest:
            missing.append("service interest")
        if not fields.budget:
            missing.append("budget")
        if not fields.timeline:
            missing.append("timeline")
        
        return missing
    
    def generate_next_question(self, missing_fields: List[str], tenant_questions: List[str]) -> Optional[str]:
        """Generate next qualification question based on missing fields"""
        if not missing_fields:
            return None
        
        # Map fields to questions
        field_questions = {
            "name": "May I have your name?",
            "contact (email or phone)": "What's the best way to reach you? Could you share your email or phone number?",
            "service interest": "What service or solution are you interested in?",
            "budget": "Do you have a budget range in mind for this project?",
            "timeline": "When are you looking to get started?"
        }
        
        # Return question for first missing field
        first_missing = missing_fields[0]
        return field_questions.get(first_missing, f"Could you tell me about your {first_missing}?")
