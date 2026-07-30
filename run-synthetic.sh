#!/bin/bash

PAIRS=("75 75" "70 70" "60 60" "55 55" "35 70" "50 50" "60 30" "25 50" "35 35" "20 40" "40 20" "30 15" "10 20" "15 15" "10 10")

for pair in "${PAIRS[@]}"; do
    read -r c v <<< "$pair"

    if   [ "$v" -eq "$c" ];             then rel="v=c"
    elif [ "$v" -eq $((c * 2)) ];       then rel="v>c"
    else                                     rel="v<c"
    fi

    echo "========================================="
    echo "  Customers=$c | Vehicles=$v | $rel"
    echo "========================================="

    python3 main.py \
      "experiments.num_customers=$c" \
      "experiments.num_vehicles=$v" \
      experiments.timeout=1200 \
      experiments.num_instances=1 \
      experiments.instance_reps=1 \
      generator=synthetic \
      "experiments.name=turing8_synthetic_C${c}_V${v}"
done
