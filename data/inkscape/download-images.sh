# run this script to download all source images from kramerius

for UUID in $(ls | grep ".svg$" | cut -c -36)
do
    wget https://kramerius.mzk.cz/search/iiif/uuid:${UUID}/full/max/0/default.jpg \
        -O ./images/${UUID}.jpg
done
