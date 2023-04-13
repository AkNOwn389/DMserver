#/bin/bash

echo "BUILD START BOSS DARIUS"
python3.9 -m pipenv shell
python3.9 -m pip install -r requirements.txt
echo "BUILD END"
echo "Collect Static..."