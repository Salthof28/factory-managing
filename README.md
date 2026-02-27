<!-- create venv for isntall framework or library like node_module in javascript, not global install -->
python -m venv venv

<!-- pointer installer to venv/Scripts/activate -->
source venv/Scripts/activate

<!-- refresh to venv -->
Ctrl + Shift + P
<!-- write this -->
Python: Select Interpreter


<!-- create requirements.txt like package.json in node.js. (but you need call this in terminal, each you install new library) -->
pip freeze > requirements.txt
<!-- if you want to use my project or clone my project and want to install framework and library, follow this step -->
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

<!-- alternative use pyproject.toml (this is modern package.json python) -->
<!-- if you use this methode you don't need to setting "source venv/Scripts/activate", because uv automatic install in local -->
pip install uv
uv init <!-- this automatic (You don't need call this in terminal each you install new library. You need call first time  when you create the project) -->
uv sync <!-- for install framework or library -->




<!-- running project fast api -->
python -m uvicorn main:app --reload


<!-- run project in mode dev -->
fastapi dev app/