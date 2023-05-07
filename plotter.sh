#!/bin/sh

TEMP_DAT=$(mktemp --suffix .dat)
TEMP_PNG=$(mktemp --suffix .png)

cat > $TEMP_DAT && \
gnuplot <<EOF
set terminal png
set output '$TEMP_PNG'
plot '$TEMP_DAT' with lines
EOF

eog $TEMP_PNG

rm -f $TEMP_DAT
rm -f $TEMP_PNG
