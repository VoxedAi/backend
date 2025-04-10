"""
Schema definitions for agent operations.
"""
from typing import Dict, Any, Optional, Union, List
from pydantic import BaseModel, Field, validator


class QueryResult(BaseModel):
    """Schema for a single query result/source."""
    id: str = Field(..., description="Unique identifier for the source")
    content: str = Field(..., description="Content of the source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata about the source")


class ThinkingStep(BaseModel):
    """Schema for a thinking/reasoning step."""
    step: int = Field(..., description="Step number in the reasoning process")
    thinking: str = Field(..., description="The reasoning/thinking content")


class AgentEvent(BaseModel):
    """Schema for agent workflow events."""
    type: str = Field("agent_event", description="The type of event (usually 'agent_event')")
    event_type: str = Field(..., description="The specific event type (decision, file_edit_start, etc.)")
    decision: Optional[str] = Field(None, description="Decision made by the agent")
    file_id: Optional[str] = Field(None, description="ID of a file being edited")
    tool: Optional[str] = Field(None, description="Tool being used by the agent")
    message: Optional[str] = Field(None, description="Event message")
    data: Optional[str] = Field(None, description="Additional event data")


class AgentRequest(BaseModel):
    """Schema for agent request."""
    space_id: str = Field(..., description="ID of the space the query pertains to")
    active_file_id: Optional[str] = Field(None, description="ID of the active file the user is working with")
    query: str = Field(..., description="The user's question or command")
    stream: bool = Field(False, description="Whether to stream the response")
    model_name: Optional[str] = Field(None, description="Optional model name to use for the response")
    top_k: Optional[int] = Field(None, description="Optional number of top results to consider")
    user_id: Optional[str] = Field(None, description="Optional user ID for tracking or personalization")
    chat_session_id: Optional[str] = Field(None, description="ID of the chat session this request belongs to")
    save_to_db: bool = Field(True, description="Whether to save the request and response to the database")


class AgentResponse(BaseModel):
    """Schema for agent response."""
    success: bool = Field(..., description="Whether the agent execution was successful")
    response: str = Field(..., description="The response text (answer)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional information about the response")
    chat_session_id: Optional[str] = Field(None, description="ID of the chat session this response belongs to")
    workflow: Optional[List[AgentEvent]] = Field(None, description="Workflow events from the agent process")
    
    @property
    def sources(self) -> List[QueryResult]:
        """Get the sources used for this response."""
        return self.metadata.get("sources", [])
    
    @property
    def thinking(self) -> List[ThinkingStep]:
        """Get the thinking steps for this response."""
        return self.metadata.get("thinking", [])
    
    @property
    def reasoning(self) -> str:
        """Get the reasoning content."""
        return self.metadata.get("reasoning", "")
    
    @property
    def query_time_ms(self) -> int:
        """Get the query execution time in milliseconds."""
        return self.metadata.get("query_time_ms", 0)
                         
