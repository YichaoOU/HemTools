msg=$1
b=$2
find . -size +90M | sed 's|^\./||g' | cat >> .gitignore; awk '!NF || !seen[$0]++' .gitignore
git add .
git commit -m $1
git push origin $2
