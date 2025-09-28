if [[ $# -eq 0 ]] ; then
    echo 'error: please enter a commit comment'
    exit 1
fi

# Cleanup junk files
find . -type f -name "*.DS_Store*" -exec rm -f {} \;
find . -type f -name "*.eggs*" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;

# Run project scripts
cd film_packaging || exit 1
python3 make_lowres.py
python3 update_page.py
python3 update_stats.py

# Git workflow
current_branch=$(git rev-parse --abbrev-ref HEAD)

git add --all
git commit -m "$@"

# Ask whether to push
read -r -p "Do you want to push to remote (y/n)? " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    git push origin "$current_branch"
else
    echo "Commit saved locally on branch '$current_branch'."
fi
