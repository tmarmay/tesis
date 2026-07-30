#!/bin/bash

PAIRS=("5 10" "20 10" "20 20" "15 30" "25 25" "30 30" "80 80" "65 65" "40 80" "80 40" "70 35" "30 60" "45 45" "40 40" "50 25")

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
      config.generator=random \
      "experiments.name=turing8_random_C${c}_V${v}"
done
