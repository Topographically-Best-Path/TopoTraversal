# Topo-Traversal
### Installation
1) Install Environments (only install ones you don't already have)
Install conda, instructions here https://conda.io/projects/conda/en/latest/user-guide/install/index.html
Install git, instructions here https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
2) Enter preferred directory and run these commands
git clone https://github.com/Topographically-Best-Path/TopoTraversal
conda config --prepend channels conda-forge
conda create --name pygmt python=3.6 pip numpy pandas xarray packaging gmt=6.1.1
conda activate pygmt
pip install pygmt
pip install opensimplex
Ivan put the stuff for pyinstaller and all that after this point
