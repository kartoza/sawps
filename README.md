# SANBI WPS


## 🏃‍♂️ How To Run Project with Visual Studio Code

- Copy and customize environtnment file :

    Create a copy of the .template.env file and name it .env. Update the .env file with your project-specific settings.

- Ensure you have Dev Containers extension is installed

- Build and open project in devcontainer :

    Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux) to open the Command Palette. 
Type "Dev Containers: Rebuild and Reopen in Container" and select it to reopen the folder inside the devcontainer.

- Install dependencies inside the container:

    Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux), type "Tasks: Run Tasks" and select it.
    Choose "React: Install dependencies" to install the necessary dependencies.

- Run the project inside the container:

    Press Cmd+Shift+D (macOS) or Ctrl+Shift+D (Windows/Linux), choose "Django+React" in RUN AND DEBUG dropdown.
    
- Open your web browser and go to localhost:8000 to view the running application.
