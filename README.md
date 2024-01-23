# snowdas
A set of programs to acquire SNODAS data, extract it, and convert it to GeoTIFs.

## Process
```bash
python make_urls.py
python download.py
python extract.py
python to_gtiff.py
```

## Then, split the different model outputs
https://nsidc.org/sites/default/files/g02158-v001-userguide_2_1.pdf


```bash
mkdir ssmv01025SlL00T0024
mkdir ssmv01025SlL01T0024
mkdir ssmv11034tS__T0001
mkdir ssmv11036tS__T0001
mkdir ssmv11038wS__A0024
mkdir ssmv11039lL00T0024
mkdir ssmv11044bS__T0024
mkdir ssmv11050lL00T0024
```

```bash
mv *ssmv01025SlL00T0024*.tif ssmv01025SlL00T0024/
mv *ssmv01025SlL01T0024*.tif ssmv01025SlL01T0024/
mv *ssmv11034tS__T0001*.tif ssmv11034tS__T0001/
mv *ssmv11036tS__T0001*.tif ssmv11036tS__T0001/
mv *ssmv11038wS__A0024*.tif ssmv11038wS__A0024/
mv *ssmv11039lL00T0024*.tif ssmv11039lL00T0024/
mv *ssmv11044bS__T0024*.tif ssmv11044bS__T0024/
mv *ssmv11050lL00T0024*.tif ssmv11050lL00T0024/
```

## Visualize 
e.g. with `plot.ipynb`