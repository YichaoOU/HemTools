r=$1
c=$2
for i in *.png;do convert -density 300 $i -quality 100 $i.jpg;done
image-grid -i *jpg -r $r -c $c -t jpeg -o combined.jpg --fill

