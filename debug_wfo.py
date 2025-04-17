#!/usr/bin/env python
import traceback

try:
    import scripts.strategies.wfo_edge_strategy as wfo
    wfo.run_walk_forward_optimization()
except Exception as e:
    traceback.print_exc() 