
echo "Cleaning top level directories"
rm -rf logs .pytest_cache __pycache__ 

echo "Cleaning Pycache"
pyclean -v .
