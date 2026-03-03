"""Project management core entities and operations."""

class ProjectService:
    def __init__(self) -> None:
        self.projects: dict[str, dict] = {}

    def create(self, project_id: str, name: str) -> dict:
        p={"project_id":project_id,"name":name,"status":"active","tasks":[]}
        self.projects[project_id]=p
        return p

    def add_task(self, project_id: str, task: str) -> dict:
        self.projects[project_id]["tasks"].append(task)
        return self.projects[project_id]
