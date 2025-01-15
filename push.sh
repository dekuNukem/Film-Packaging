if [[ $# -eq 0 ]] ; then
    echo 'error: please enter a commit comment'
    exit 1
fi

find . -type f -name "*.DS_Store*" -exec rm -f {} \;
find . -type f -name "*.eggs*" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;

bundle config set frozen false
cp README.md index.md

cd film_packaging
python3 update_stats.py

current_branch=$(git rev-parse --abbrev-ref HEAD)

git add --all
git commit -m "$@"
git push origin "$current_branch"
