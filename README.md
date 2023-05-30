# 🦏 SANBI WPS

The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.


## 🧑🏽‍💻 Development

Please follow the Kartoza [coding standards](https://kartoza.github.io/TheKartozaHandbook/development/conventions/coding_standards/#compliance).


## 🏃‍♂️ How To Run Project with Visual Studio Code

Copy and customize environnment file: Create a copy of the ```deployment/.template.env``` file and name it ```deployment/.env```. Update the ```deployment/.env``` file with your project-specific settings.
![image](https://user-images.githubusercontent.com/178003/231014472-c77f7a00-1a1d-43d0-8c06-ef9634f2ccc7.png)


Ensure Dev Containers extension is installed
![image](https://user-images.githubusercontent.com/178003/231014270-65212ed8-6d78-4966-9c2b-f9ebe82f9025.png)

Build and open project in devcontainer: press ```Cmd+Shift+P``` (macOS) or ```Ctrl+Shift+P``` (Windows/Linux) to open the Command Palette. Type ```Dev Containers: Rebuild and Reopen in Container``` and select it to reopen the folder inside the devcontainer.
![image](https://user-images.githubusercontent.com/178003/231014643-3e4e9e56-1d03-4e15-9015-9f85a2a715a2.png)

Change the permissions of the django_project folder:

```
chmod -R a+rw django_project
```

Install dependencies inside the container: Press ```Cmd+Shift+P``` (macOS) or ```Ctrl+Shift+P``` (Windows/Linux), type ```Tasks: Run Tasks``` and select it. Choose ```React: Install dependencies``` to install the necessary dependencies.

![image](https://user-images.githubusercontent.com/178003/231015768-39803d00-95dc-42c7-a08f-ab58ac09fa58.png)

![image](https://user-images.githubusercontent.com/178003/231016195-5d78356b-e802-40f6-aa33-82404b65925d.png)

Run the project inside the container: Press ```Cmd+Shift+D``` (macOS) or ```Ctrl+Shift+D``` (Windows/Linux), choose ```Django+React``` in the RUN AND DEBUG dropdown.

![image](https://user-images.githubusercontent.com/178003/231016537-cda1d85f-5123-45ef-8f51-c12e90e1d0c9.png)


Open your web browser and go to localhost:8000 to view the running application.

## 💻 Resources

[Database ERD](https://drive.google.com/file/d/1O92w2zwbKm_SARXnXIljHbX-rQPmFiXM/view?usp=sharing)

[Figma Board](https://www.figma.com/file/T6JEAAXTWzA9OIfAQe3iW7/SANBI?node-id=6-2&t=4T7COmsnfif2Nwwn-0)
