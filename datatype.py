class JobProfile:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.description = data.get("description")
        
        self.other_names = data.get("other_name", [])
        self.essential_skills = data.get("essential_skill", [])
        self.optional_skills = data.get("optional_skill", [])
        self.essential_knowledge = data.get("essential_knowledge", [])
        self.optional_knowledge = data.get("optional_knowledge", [])

    def __repr__(self):
        # A helpful representation for printing the object
        return f"JobProfile(name='{self.name}', description='{self.description[:30]}...')"