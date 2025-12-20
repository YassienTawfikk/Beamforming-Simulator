import os
import shutil

class ProjectCleaner:
    @staticmethod
    def clean(logging_manager):
        project_root = os.getcwd()
        logging_manager.log("Starting project cleanup...")

        # 1. Remove .idea, __pycache__, .DS_Store
        for root, dirs, files in os.walk(project_root):
             if "__pycache__" in dirs:
                 shutil.rmtree(os.path.join(root, "__pycache__"))
             
             if ".DS_Store" in files:
                 os.remove(os.path.join(root, ".DS_Store"))

        idea_path = os.path.join(project_root, ".idea")
        if os.path.exists(idea_path):
             shutil.rmtree(idea_path)

        # 2. Generate .gitignore
        gitignore_path = os.path.join(project_root, ".gitignore")
        gitignore_content = ".idea/\n__pycache__/\n*.pyc\n*.DS_Store\n.venv/\n.env\nlogging/\n" 
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        
        logging_manager.log("Project cleanup complete and .gitignore generated.")
