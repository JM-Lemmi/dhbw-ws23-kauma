#! /bin/bash

# testcases from https://datatracker.ietf.org/doc/html/rfc6229
# only the first 32 bits of the resulting keystream are used, since the format is weird af

for i in ./testcases/*.in; do
    n=${i#./testcases/}; n=${n%.in}

    if diff -q <(./rc4.py $(cat ${i})) <(cat ${i%.in}.out) > /dev/null; then
        echo "[✔] Test ${n} passed"
    else
        echo "[✘] Test ${n} failed"
    fi
done
