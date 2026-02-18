from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
import uuid
from dotenv import load_dotenv
from ..database import get_db
from ..models import User, Project
from ..schemas import ProjectCreate, ProjectResponse, ReadmeResponse
from ..auth import get_current_user

load_dotenv()

router = APIRouter(prefix="/projects", tags=["projects"])

LANGFLOW_API_URL = os.getenv("LANGFLOW_API_URL")
LANGFLOW_FLOW_ID = os.getenv("LANGFLOW_FLOW_ID")
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY")

@router.post("/generate-readme", response_model=ReadmeResponse)
async def generate_readme(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if project_data.mode == "advanced":
        # Validate Langflow configuration
        if not LANGFLOW_FLOW_ID or LANGFLOW_FLOW_ID == "your-flow-id":
            raise HTTPException(
                status_code=500, 
                detail="Langflow Flow ID not configured. Please set LANGFLOW_FLOW_ID in backend/.env"
            )
        
        if not LANGFLOW_API_KEY or LANGFLOW_API_KEY == "your-api-key":
            raise HTTPException(
                status_code=500, 
                detail="Langflow API Key not configured. Please set LANGFLOW_API_KEY in backend/.env"
            )
        
        url = f"{LANGFLOW_API_URL}/{LANGFLOW_FLOW_ID}"
        headers = {
            "x-api-key": LANGFLOW_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Add instruction to avoid emojis
        extra_instructions = (project_data.extra_notes or "") + "\n\nIMPORTANT: Do not use any emojis or special Unicode characters in the output. Use plain text only."
        
        payload = {
            "input_value": {
                "repo_name": project_data.project_name,
                "project_description": project_data.description,
                "tech_stack": project_data.tech_stack,
                "features": project_data.features,
                "installation_steps": project_data.installation_steps,
                "extra_notes": extra_instructions
            },
            "output_type": "text",
            "input_type": "text",
            "session_id": str(uuid.uuid4())
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                # Log the raw response for debugging
                print(f"Langflow Status Code: {response.status_code}")
                print(f"Langflow Response (first 500 chars): {response.text[:500]}")
                
                response.raise_for_status()
                result = response.json()
                
                # Try multiple paths to extract the README
                generated_readme = None
                if "outputs" in result:
                    outputs = result["outputs"]
                    if isinstance(outputs, list) and len(outputs) > 0:
                        first_output = outputs[0]
                        if "outputs" in first_output:
                            nested = first_output["outputs"]
                            if isinstance(nested, list) and len(nested) > 0:
                                generated_readme = nested[0].get("results", {}).get("message", {}).get("text", "")
                        elif "results" in first_output:
                            generated_readme = first_output["results"].get("message", {}).get("text", "")
                        elif "text" in first_output:
                            generated_readme = first_output["text"]
                        elif "message" in first_output:
                            msg = first_output["message"]
                            if isinstance(msg, dict):
                                generated_readme = msg.get("text", "")
                            else:
                                generated_readme = str(msg)
                
                # If still no readme, try to extract from anywhere in the response
                if not generated_readme and "outputs" in result:
                    # Search deeper in the structure
                    for output in result.get("outputs", []):
                        if isinstance(output, dict):
                            for key, value in output.items():
                                if isinstance(value, str) and len(value) > 100:
                                    generated_readme = value
                                    break
                            if generated_readme:
                                break
                
                if not generated_readme:
                    # Last resort: convert entire response to string
                    generated_readme = f"# {project_data.project_name}\n\nLangflow Response:\n{str(result)}"
                
                # Remove emojis and special Unicode characters
                if generated_readme:
                    # Remove characters outside the basic multilingual plane
                    import re
                    # Remove emojis (characters in emoji ranges)
                    generated_readme = re.sub(r'[^\x00-\x7F\u0080-\uFFFF]+', '', generated_readme)
                    # Additional cleanup for common problematic characters
                    generated_readme = generated_readme.replace('🚀', '').replace('💡', '').replace('✨', '')
                    generated_readme = generated_readme.replace('📝', '').replace('🔧', '').replace('⚙️', '')
                    generated_readme = generated_readme.replace('🤖', '').replace('🎯', '').replace('📦', '')
                
                print(f"Extracted README length: {len(generated_readme) if generated_readme else 0}")
                    
        except httpx.HTTPStatusError as e:
            error_text = e.response.text
            print(f"Langflow HTTP Error: {e.response.status_code} - {error_text[:500]}")
            
            # Check for specific error types
            if "quota" in error_text.lower() or "429" in error_text:
                raise HTTPException(
                    status_code=500, 
                    detail="AI API quota exceeded. Your Gemini API free tier limit has been reached. Please wait or upgrade your API plan, or use Basic mode."
                )
            elif "rate limit" in error_text.lower():
                raise HTTPException(
                    status_code=500, 
                    detail="Rate limit exceeded. Please wait a few minutes and try again, or use Basic mode."
                )
            else:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Langflow returned error {e.response.status_code}. Check Langflow logs for details."
                )
        except httpx.RequestError as e:
            print(f"Langflow Connection Error: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Cannot connect to Langflow at {LANGFLOW_API_URL}. Make sure Langflow is running."
            )
        except Exception as e:
            print(f"Unexpected Error: {type(e).__name__} - {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing Langflow response. Try Basic mode or check Langflow flow configuration."
            )
    else:
        generated_readme = f"""# {project_data.project_name}

## Description
{project_data.description}

## Tech Stack
{project_data.tech_stack}

## Features
{project_data.features}

## Installation
{project_data.installation_steps}

## Additional Notes
{project_data.extra_notes or 'N/A'}
"""
    
    new_project = Project(
        user_id=current_user.id,
        project_name=project_data.project_name,
        description=project_data.description,
        tech_stack=project_data.tech_stack,
        features=project_data.features,
        installation_steps=project_data.installation_steps,
        extra_notes=project_data.extra_notes,
        generated_readme=generated_readme
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {"readme": generated_readme, "project_id": new_project.id}

@router.get("/history", response_model=List[ProjectResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.created_at.desc()).all()
    return projects
