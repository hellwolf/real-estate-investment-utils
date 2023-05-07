mkdir -p test/IYC.d

for i in 2.0 2.5 3.0 3.5 4.0 4.5 5.0;do
for r in 400 425 450 475 500;do
    F=curve-$i-$r
    python utils.py IYC 93000 240 $i $r > test/IYC.d/$F.dat
    gnuplot <<EOF
set terminal png
set output 'test/IYC.d/$F.png'
plot 'test/IYC.d/$F.dat' with lines
EOF
done
done
