from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class File(BaseModel):
    path: str = Field(description="The path to the folder where the file needs to be created or modified")
    purpose: str = Field(description="The purpose of the file")


class Plan(BaseModel):
    name: str = Field(description="The name of the app to be built")
    description: str = Field(description="A short description of the app to be built, eg: A workout buddy")
    techstack: str = Field(description="The tech stack app to be built")
    features: str = Field(description="A list of features app to be built")
    files: str = Field(description="A list of files to be created for the application")


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path of the file to be built")
    task_description: str = Field(description="A detailed description of the task to be implemented")


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description="A list of steps to be taken to implement a task")
    model_config = ConfigDict(extra="allow")

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None,
                                                description="The content of the file currently being edited or created")

