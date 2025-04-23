# Dynamic[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#dynamic "Permanent link")

Until now, all allocation and optimization functions were based strictly on external information such as pricing data and had no control over the actual execution. But what if we want to rebalance based on some conditions within the current trading environment? For instance, to perform a threshold rebalancing, we need to know the current portfolio value. This scenario introduces a path-dependent problem, which can only be addressed using a custom order function.

Let's backtest threshold rebalancing, which is a portfolio management strategy used to maintain a set of desired allocations, without allowing the asset weightings from deviating excessively. We'll create a template pipeline that takes any user-defined, Numba-compiled allocation function. When one of the individual constituents of the portfolio crosses outside the bounds of their desired allocations, the entire portfolio is rebalanced to realign with the target allocations.

Here's a general template:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-1)>>> GroupMemory = namedtuple("GroupMemory", [ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-2)... "target_alloc", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-3)... "size_type",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-4)... "direction",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-5)... "order_value_out"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-6)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-8)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-9)... def pre_group_func_nb(c): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-10)... group_memory = GroupMemory(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-11)... target_alloc=np.full(c.group_len, np.nan), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-12)... size_type=np.full(c.group_len, vbt.pf_enums.SizeType.TargetPercent), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-13)... direction=np.full(c.group_len, vbt.pf_enums.Direction.Both),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-14)... order_value_out=np.full(c.group_len, np.nan) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-16)... return group_memory,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-18)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-19)... def pre_segment_func_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-20)... c, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-21)... group_memory, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-22)... min_history, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-23)... threshold, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-24)... allocate_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-25)... *args
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-26)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-27)... should_rebalance = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-28)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-29)... if c.i >= min_history:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-30)... in_position = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-31)... for col in range(c.from_col, c.to_col):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-32)... if c.last_position[col] != 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-33)... in_position = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-34)... break
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-35)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-36)... if not in_position:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-37)... should_rebalance = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-38)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-39)... curr_value = c.last_value[c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-40)... for group_col in range(c.group_len):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-41)... col = c.from_col + group_col
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-42)... curr_position = c.last_position[col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-43)... curr_price = c.last_val_price[col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-44)... curr_alloc = curr_position * curr_price / curr_value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-45)... curr_threshold = vbt.pf_nb.select_from_col_nb(c, col, threshold) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-46)... alloc_diff = curr_alloc - group_memory.target_alloc[group_col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-47)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-48)... if abs(alloc_diff) >= curr_threshold:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-49)... should_rebalance = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-50)... break
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-51)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-52)... if should_rebalance:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-53)... allocate_func_nb(c, group_memory, *args) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-54)... vbt.pf_nb.sort_call_seq_1d_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-55)... c, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-56)... group_memory.target_alloc, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-57)... group_memory.size_type, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-58)... group_memory.direction, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-59)... group_memory.order_value_out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-60)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-61)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-62)... return group_memory, should_rebalance
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-63)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-64)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-65)... def order_func_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-66)... c, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-67)... group_memory, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-68)... should_rebalance, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-69)... price,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-70)... fees
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-71)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-72)... if not should_rebalance:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-73)... return vbt.pf_nb.order_nothing_nb()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-74)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-75)... group_col = c.col - c.from_col 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-76)... return vbt.pf_nb.order_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-77)... size=group_memory.target_alloc[group_col], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-78)... price=vbt.pf_nb.select_nb(c, price),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-79)... size_type=group_memory.size_type[group_col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-80)... direction=group_memory.direction[group_col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-81)... fees=vbt.pf_nb.select_nb(c, fees)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-0-82)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 

Let's create an allocation function for an equally-weighted portfolio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-1-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-1-2)... def uniform_allocate_func_nb(c, group_memory):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-1-3)... for group_col in range(c.group_len):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-1-4)... group_memory.target_alloc[group_col] = 1 / c.group_len 
 
[/code]

 1. 

Hint

Sometimes, we may want to rebalance dynamically based on a function that uses a third-party library, such as SciPy or scikit-learn, and cannot be compiled with Numba. In such cases, we can disable jitting of the main simulator function by passing `jitted=False`.

Now it's time to run the simulation!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-1)>>> def simulate_threshold_rebalancing(threshold, allocate_func_nb, *args, **kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-2)... return vbt.Portfolio.from_order_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-3)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-4)... open=data.get("Open"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-5)... pre_group_func_nb=pre_group_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-6)... pre_group_args=(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-7)... pre_segment_func_nb=pre_segment_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-8)... pre_segment_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-9)... 0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-10)... vbt.Rep("threshold"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-11)... allocate_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-12)... *args
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-13)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-14)... order_func_nb=order_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-15)... order_args=(vbt.Rep('price'), vbt.Rep('fees')), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-16)... broadcast_named_args=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-17)... price=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-18)... fees=0.005,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-19)... threshold=threshold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-20)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-21)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-22)... group_by=vbt.ExceptLevel("symbol"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-23)... freq='1h', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-24)... **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-27)>>> pf = simulate_threshold_rebalancing(0.05, uniform_allocate_func_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-2-28)>>> pf.plot_allocations().show()
 
[/code]

 1. 2. 3. 4. 5. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic.dark.svg#only-dark)

We see that threshold rebalancing makes asset allocations to repeatedly jump to their target levels. 

Info

In cases where your kernel dies, or you want to validate the pipeline you created with Numba, it's advisable to either enable bound checks, or disable Numba entirely and then run your pipeline on sample data. This will effectively expose your hidden indexing bugs.

For this, run the following in the first cell before anything else:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-3-1)>>> import os
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-3-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-3-3)>>> os.environ["NUMBA_BOUNDSCHECK"] = "1"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-3-4)>>> os.environ["NUMBA_DISABLE_JIT"] = "1"
 
[/code]

We can also test multiple thresholds by simply making it an index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-1)>>> pf = simulate_threshold_rebalancing(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-2)... vbt.Param(np.arange(1, 16) / 100, name="threshold"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-3)... uniform_allocate_func_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-6)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-7)threshold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-8)0.01 1.939551
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-9)0.02 1.964451
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-10)0.03 1.985215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-11)0.04 1.984484
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-12)0.05 1.993381
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-13)0.06 2.019594
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-14)0.07 1.983087
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-15)0.08 2.047598
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-16)0.09 2.087186
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-17)0.10 1.939077
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-18)0.11 1.962485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-19)0.12 1.978320
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-20)0.13 1.963077
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-21)0.14 1.969721
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-22)0.15 1.983179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-4-23)Name: sharpe_ratio, dtype: float64
 
[/code]

 1. 


# Post-analysis[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#post-analysis "Permanent link")

But can we somehow get the rebalancing timestamps? Of course!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-2)... def track_uniform_allocate_func_nb(c, group_memory, index_points, alloc_counter):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-3)... for group_col in range(c.group_len):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-4)... group_memory.target_alloc[group_col] = 1 / c.group_len
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-5)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-6)... index_points[alloc_counter[0]] = c.i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-7)... alloc_counter[0] += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-9)>>> index_points = np.empty(data.wrapper.shape[0], dtype=int_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-10)>>> alloc_counter = np.full(1, 0) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-11)>>> pf = simulate_threshold_rebalancing(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-12)... 0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-13)... track_uniform_allocate_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-14)... index_points, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-15)... alloc_counter
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-17)>>> index_points = index_points[:alloc_counter[0]] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-19)>>> data.wrapper.index[index_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-20)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-02-02 04:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-21) '2020-03-07 15:00:00+00:00', '2020-05-28 18:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-22) '2020-06-03 16:00:00+00:00', '2020-07-07 13:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-23) '2020-08-14 17:00:00+00:00', '2020-09-09 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-24) '2020-11-05 13:00:00+00:00', '2020-11-21 14:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-25) '2020-11-24 00:00:00+00:00', '2020-12-22 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-26) '2020-12-23 11:00:00+00:00', '2020-12-28 23:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-27) '2020-12-29 16:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-5-28) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 3. 

What if we want to post-analyze both, index points and target allocations? And how should we treat cases when there are multiple parameter combinations? 

Allocations can be saved to an array in the same way as index points. But as soon as there are multiple groups, we have two options: either run the entire pipeline in a loop (remember that vectorbt sometimes even encourages you to do that because you can use chunking), or simply concatenate index points and target allocations of all groups into a single array and track the group of each entry in that array. We can then construct an instance of [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) to conveniently post-analyze the entire target allocation data!

We need to make a few adaptations though. First, [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) requires index points to be of type [AllocPoints](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/records/#vectorbtpro.portfolio.pfopt.records.AllocPoints), which, in turn, requires the underlying data to be a structured array of a complex data type [alloc_point_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.alloc_point_dt). Second, our counter will track count per group rather than globally. By taking the sum of it, we can still derive the global count. For a better illustration, we'll also implement a new allocation function that generates weights randomly. Finally, if you aren't scared of complexity and want the most flexible thing possible, see the "Flexible" tab for the same pipeline but with templates and in-outputs ![😏](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f60f.svg)

PresetFlexible
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-2)... def random_allocate_func_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-3)... c, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-4)... group_memory, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-5)... alloc_points, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-6)... alloc_weights, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-7)... alloc_counter
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-8)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-9)... weights = np.random.uniform(0, 1, c.group_len)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-10)... group_memory.target_alloc[:] = weights / weights.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-11)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-12)... group_count = alloc_counter[c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-13)... count = alloc_counter.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-14)... alloc_points["id"][count] = group_count 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-15)... alloc_points["col"][count] = c.group 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-16)... alloc_points["alloc_idx"][count] = c.i 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-17)... alloc_weights[count] = group_memory.target_alloc 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-18)... alloc_counter[c.group] += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-20)>>> thresholds = pd.Index(np.arange(1, 16) / 100, name="threshold")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-21)>>> max_entries = data.wrapper.shape[0] * len(thresholds) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-22)>>> alloc_points = np.empty(max_entries, dtype=vbt.pf_enums.alloc_point_dt) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-23)>>> alloc_weights = np.empty((max_entries, len(data.symbols)), dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-24)>>> alloc_counter = np.full(len(thresholds), 0) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-25)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-26)>>> pf = simulate_threshold_rebalancing(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-27)... vbt.Param(thresholds),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-28)... random_allocate_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-29)... alloc_points, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-30)... alloc_weights,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-31)... alloc_counter,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-32)... seed=42 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-33)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-34)>>> alloc_points = alloc_points[:alloc_counter.sum()] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-6-35)>>> alloc_weights = alloc_weights[:alloc_counter.sum()]
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-2)... def random_allocate_func_nb(c, group_memory): 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-3)... weights = np.random.uniform(0, 1, c.group_len)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-4)... group_memory.target_alloc[:] = weights / weights.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-5)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-6)... group_count = c.in_outputs.alloc_counter[c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-7)... count = c.in_outputs.alloc_counter.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-8)... c.in_outputs.alloc_points["id"][count] = group_count
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-9)... c.in_outputs.alloc_points["col"][count] = c.group
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-10)... c.in_outputs.alloc_points["alloc_idx"][count] = c.i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-11)... c.in_outputs.alloc_weights[count] = group_memory.target_alloc
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-12)... c.in_outputs.alloc_counter[c.group] += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-14)>>> alloc_points = vbt.RepEval("""
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-15)... max_entries = target_shape[0] * len(group_lens)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-16)... np.empty(max_entries, dtype=alloc_point_dt)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-17)... """, context=dict(alloc_point_dt=vbt.pf_enums.alloc_point_dt)) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-18)>>> alloc_weights = vbt.RepEval("""
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-19)... max_entries = target_shape[0] * len(group_lens)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-20)... np.empty((max_entries, n_cols), dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-21)... """, context=dict(n_cols=len(data.symbols)))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-22)>>> alloc_counter = vbt.RepEval("np.full(len(group_lens), 0)")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-24)>>> InOutputs = namedtuple("InOutputs", [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-25)... "alloc_points",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-26)... "alloc_weights", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-27)... "alloc_counter"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-28)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-29)>>> in_outputs = InOutputs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-30)... alloc_points=alloc_points, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-31)... alloc_weights=alloc_weights,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-32)... alloc_counter=alloc_counter,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-33)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-34)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-35)>>> pf = simulate_threshold_rebalancing(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-36)... vbt.Param(np.arange(1, 16) / 100, name="threshold"), 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-37)... random_allocate_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-38)... in_outputs=in_outputs, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-39)... seed=42
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-40)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-41)>>> alloc_points = pf.in_outputs.alloc_points[:pf.in_outputs.alloc_counter.sum()]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-7-42)>>> alloc_weights = pf.in_outputs.alloc_weights[:pf.in_outputs.alloc_counter.sum()]
 
[/code]

 1. The function is the same as in the "Preset" example, but the arrays are now provided via the in-outputs tuple rather than via arguments
 2. The same logic as in the "Preset" example, but we use templates to postpone the creation of all arrays to the point where all other arrays are broadcast and the final shape and the number of groups are available
 3. Don't name the field `allocations`, it's a reserved word!
 4. Notice how array creation isn't tied to the threshold array anymore!
 5. Since we now use templates, we don't have references to the created arrays anymore. But luckily, we can use in-outputs, which store the references to all arrays for us.

Hint

If you perform portfolio optimization on some history of data (for example, by searching for the maximum Sharpe ratio), make sure to use [alloc_range_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.alloc_range_dt) and [AllocRanges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/records/#vectorbtpro.portfolio.pfopt.records.AllocRanges) \- this would open another dimension in data analysis.

What's left is the creation of a [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) instance using the target allocation data that we just filled:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-1)>>> pfo = vbt.PortfolioOptimizer( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-2)... wrapper=pf.wrapper, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-3)... alloc_records=vbt.AllocPoints(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-4)... pf.wrapper.resolve(), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-5)... alloc_points
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-6)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-7)... allocations=alloc_weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-8-8)... )
 
[/code]

 1. 2. 3. 

Having such an instance allows us to post-analyze the target allocation data. Even though we used random weights in rebalancing, let's describe the allocations generated for the threshold of 10% just for the sake of example:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-1)>>> pfo[0.1].allocations.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-2)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-3)count 6.000000 6.000000 6.000000 6.000000 6.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-4)mean 0.159883 0.149608 0.156493 0.292615 0.241400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-5)std 0.092490 0.079783 0.043584 0.098891 0.083152
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-6)min 0.076678 0.056292 0.094375 0.200873 0.098709
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-7)25% 0.091023 0.082134 0.149385 0.220957 0.223424
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-8)50% 0.123982 0.157974 0.153985 0.252078 0.243109
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-9)75% 0.230589 0.204527 0.156810 0.375171 0.293097
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-10)max 0.288493 0.248507 0.231013 0.423879 0.336853
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-9-12)>>> pfo.plot(column=0.1).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_01.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_01.dark.svg#only-dark)

Here's how the target allocation picture changes with a lower threshold:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-10-1)>>> pfo.plot(column=0.03).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_003.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_003.dark.svg#only-dark)

And here's what actually happened:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-11-1)>>> pf[0.03].plot_allocations().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_003_sim.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/dynamic_003_sim.dark.svg#only-dark)

Want the cool part? If we feed our manually-constructed optimizer instance to [Portfolio.from_optimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_optimizer), we'll get the exact same results ![🤯](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f92f.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-1)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-2)threshold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-3)0.01 1.098642
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-4)0.02 1.707515
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-5)0.03 1.775001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-6)0.04 2.077479
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-7)0.05 2.082900
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-8)0.06 1.964474
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-9)0.07 2.106367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-10)0.08 2.121511
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-11)0.09 1.838164
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-12)0.10 2.072388
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-13)0.11 2.229001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-14)0.12 1.766305
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-15)0.13 1.859604
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-16)0.14 2.209144
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-17)0.15 2.124474
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-18)Name: sharpe_ratio, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-20)>>> pf_new = vbt.Portfolio.from_optimizer(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-21)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-22)... pfo, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-23)... val_price=data.get("Open"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-24)... freq="1h", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-25)... fees=0.005
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-28)>>> pf_new.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-29)threshold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-30)0.01 1.098642
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-31)0.02 1.707515
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-32)0.03 1.775001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-33)0.04 2.077479
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-34)0.05 2.082900
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-35)0.06 1.964474
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-36)0.07 2.106367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-37)0.08 2.121511
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-38)0.09 1.838164
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-39)0.10 2.072388
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-40)0.11 2.229001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-41)0.12 1.766305
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-42)0.13 1.859604
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-43)0.14 2.209144
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-44)0.15 2.124474
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-12-45)Name: sharpe_ratio, dtype: float64
 
[/code]

This proves once again how powerful vectorbt is: we just performed dynamic threshold rebalancing, extracted the target allocation data from within the simulation, analyzed that data after the simulation, and fed it to another, totally-different simulation method to make sure that we did no mistakes related to order generation.


# Bonus 1: Own optimizer[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#bonus-1-own-optimizer "Permanent link")

As a bonus, let's do a periodic mean-variance optimization using our own simulator! We'll generate the rebalancing dates in advance, and for each of them, we'll generate a bunch of Sharpe ratios for that period and use the Efficient Frontier to select the best one. The pipeline below is the most lightweight pipeline we can get: it processes only one parameter combination at a time using the vectorbt's low-level order execution API, and consumes only the information it really needs.

Here's our raw Numba-compiled pipeline (optimization function agnostic):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-2)... def optimize_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-3)... close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-4)... val_price,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-5)... range_starts,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-6)... range_ends,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-7)... optimize_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-8)... optimize_args=(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-9)... price=np.inf,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-10)... fees=0.,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-11)... init_cash=100.,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-12)... group=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-13)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-14)... val_price_ = vbt.to_2d_array_nb(np.asarray(val_price)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-15)... price_ = vbt.to_2d_array_nb(np.asarray(price))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-16)... fees_ = vbt.to_2d_array_nb(np.asarray(fees))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-17)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-18)... order_records = np.empty(close.shape, dtype=vbt.pf_enums.order_dt) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-19)... order_counts = np.full(close.shape[1], 0, dtype=int_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-20)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-21)... order_value = np.empty(close.shape[1], dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-22)... call_seq = np.empty(close.shape[1], dtype=int_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-23)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-24)... last_position = np.full(close.shape[1], 0.0, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-25)... last_debt = np.full(close.shape[1], 0.0, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-26)... last_locked_cash = np.full(close.shape[1], 0.0, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-27)... cash_now = float(init_cash) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-28)... free_cash_now = float(init_cash)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-29)... value_now = float(init_cash)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-30)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-31)... for k in range(len(range_starts)): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-32)... i = range_ends[k] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-33)... size = optimize_func_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-34)... range_starts[k], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-35)... range_ends[k], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-36)... *optimize_args
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-37)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-38)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-39)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-40)... value_now = cash_now
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-41)... for col in range(close.shape[1]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-42)... val_price_now = vbt.flex_select_nb(val_price_, i, col)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-43)... value_now += last_position[col] * val_price_now
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-44)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-45)... for col in range(close.shape[1]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-46)... val_price_now = vbt.flex_select_nb(val_price_, i, col)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-47)... exec_state = vbt.pf_enums.ExecState(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-48)... cash=cash_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-49)... position=last_position[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-50)... debt=last_debt[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-51)... locked_cash=last_locked_cash[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-52)... free_cash=free_cash_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-53)... val_price=val_price_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-54)... value=value_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-55)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-56)... order_value[col] = vbt.pf_nb.approx_order_value_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-57)... exec_state,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-58)... size[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-59)... vbt.pf_enums.SizeType.TargetPercent,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-60)... vbt.pf_enums.Direction.Both,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-61)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-62)... call_seq[col] = col 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-63)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-64)... vbt.pf_nb.insert_argsort_nb(order_value, call_seq) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-65)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-66)... for c in range(close.shape[1]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-67)... col = call_seq[c] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-68)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-69)... order = vbt.pf_nb.order_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-70)... size=size[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-71)... price=vbt.flex_select_nb(price_, i, col),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-72)... size_type=vbt.pf_enums.SizeType.TargetPercent,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-73)... direction=vbt.pf_enums.Direction.Both,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-74)... fees=vbt.flex_select_nb(fees_, i, col),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-75)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-76)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-77)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-78)... price_area = vbt.pf_enums.PriceArea(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-79)... open=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-80)... high=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-81)... low=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-82)... close=vbt.flex_select_nb(close, i, col),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-83)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-84)... val_price_now = vbt.flex_select_nb(val_price_, i, col)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-85)... exec_state = vbt.pf_enums.ExecState(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-86)... cash=cash_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-87)... position=last_position[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-88)... debt=last_debt[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-89)... locked_cash=last_locked_cash[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-90)... free_cash=free_cash_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-91)... val_price=val_price_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-92)... value=value_now,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-93)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-94)... _, new_exec_state = vbt.pf_nb.process_order_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-95)... group=group,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-96)... col=col,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-97)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-98)... exec_state=exec_state,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-99)... order=order,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-100)... price_area=price_area,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-101)... order_records=order_records,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-102)... order_counts=order_counts
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-103)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-104)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-105)... cash_now = new_exec_state.cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-106)... free_cash_now = new_exec_state.free_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-107)... value_now = new_exec_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-108)... last_position[col] = new_exec_state.position
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-109)... last_debt[col] = new_exec_state.debt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-110)... last_locked_cash[col] = new_exec_state.locked_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-111)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-112)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-13-113)... return vbt.nb.repartition_nb(order_records, order_counts)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 

And here's our Numba-compiled MVO function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-1)>>> @njit(nogil=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-2)... def sharpe_optimize_func_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-3)... start_idx, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-4)... end_idx, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-5)... close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-6)... num_tests, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-7)... ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-8)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-9)... close_period = close[start_idx:end_idx] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-10)... returns = (close_period[1:] - close_period[:-1]) / close_period[:-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-11)... mean = vbt.nb.nanmean_nb(returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-12)... cov = np.cov(returns, rowvar=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-13)... best_sharpe_ratio = -np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-14)... weights = np.full(close.shape[1], np.nan, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-15)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-16)... for i in range(num_tests): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-17)... w = np.random.random_sample(close.shape[1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-18)... w = w / np.sum(w)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-19)... p_return = np.sum(mean * w) * ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-20)... p_std = np.sqrt(np.dot(w.T, np.dot(cov, w))) * np.sqrt(ann_factor)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-21)... sharpe_ratio = p_return / p_std
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-22)... if sharpe_ratio > best_sharpe_ratio:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-23)... best_sharpe_ratio = sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-24)... weights = w
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-25)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-14-26)... return weights
 
[/code]

 1. 2. 3. 4. 

Let's run the MVO on a weekly basis:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-1)>>> range_starts, range_ends = data.wrapper.get_index_ranges(every="W")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-2)>>> ann_factor = vbt.timedelta("365d") / vbt.timedelta("1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-3)>>> init_cash = 100
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-4)>>> num_tests = 30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-5)>>> fees = 0.005
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-7)>>> order_records = optimize_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-8)... data.get("Close").values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-9)... data.get("Open").values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-10)... range_starts,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-11)... range_ends,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-12)... sharpe_optimize_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-13)... optimize_args=(data.get("Close").values, num_tests, ann_factor),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-14)... fees=fees,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-15)... init_cash=init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-15-16)... )
 
[/code]

The result of our optimization are order records, which can be used as an input to the [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) class:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-1)>>> pf = vbt.Portfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-2)... wrapper=symbol_wrapper.regroup(True), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-3)... close=data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-4)... order_records=order_records, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-5)... log_records=np.array([]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-6)... cash_sharing=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-7)... init_cash=init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-16-8)... )
 
[/code]

 1. 2. 

We can now analyze the portfolio as we usually do!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-17-1)>>> pf.plot_allocations().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/mvo.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/mvo.dark.svg#only-dark)


# Bonus 2: Parameterization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#bonus-2-parameterization "Permanent link")

In contrast to most of the examples above, our pipeline can process only one parameter combination at a time. This means that to be able to test multiple parameter combinations, we must do it in a loop, either manually, or by using a special [parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) decorator that magically transforms any Python function into a one that can accept arbitrary parameter grids! Under the hood, the decorator intercepts any argument passed to the original function, looks whether its value or any value nested inside is wrapped with the class [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param), broadcasts and builds the Cartesian product of all the found parameter sequences, prepares the arguments and keyword arguments that correspond to each parameter combination, and forwards those argument sets to the executor function [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute). This way, the decorator not only takes care of building the parameter grid, but also of distributing the execution, for example, with Dask.

Let's test the Cartesian product of different index ranges, number of tests, and fees. Since a distributed execution returns a list of outputs, the first step is writing a merging function that takes all the outputs and merges them. In our case, an output corresponding to a parameter combination is an array with order records, and since our target metric is the Sharpe ratio, we'll create a portfolio for each set of order records, extract the Sharpe ratios, and concatenate them:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-1)>>> def merge_func(order_records_list, param_index):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-2)... sharpe_ratios = pd.Series(index=param_index, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-3)... for i, order_records in enumerate(order_records_list):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-4)... pf = vbt.Portfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-5)... wrapper=symbol_wrapper.regroup(True), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-6)... close=data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-7)... order_records=order_records, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-8)... cash_sharing=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-9)... init_cash=init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-11)... sharpe_ratios.iloc[i] = pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-18-12)... return sharpe_ratios
 
[/code]

The first argument of `param_index` is a list of outputs of the original function (`optimize_portfolio_nb`), any other argument must be instructed to be passed. The parameter index (`param_index`) is a special argument that contains the multi-index built internally from all parameter combinations; it will become the index of the resulting Sharpe series.

The next step is decorating the original function with the decorator, which is relatively easy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-1)>>> param_optimize_portfolio_nb = vbt.parameterized(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-2)... optimize_portfolio_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-3)... merge_func=merge_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-4)... merge_kwargs=dict(param_index=vbt.Rep("param_index")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-5)... engine="dask", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-6)... chunk_len=4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-19-7)... )
 
[/code]

 1. 2. 

Next, we need to prepare our parameter grid. While passing multiple commission and `num_tests` combinations is easy, index ranges are more difficult to prepare: since index ranges cannot be built inside Numba ([ArrayWrapper.get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges) is not Numba-compiled), we need to iterate over each `every` instruction and extract the index ranges manually. Index ranges consist of two arrays - start and end indices - and are accepted by two different arguments in `optimize_portfolio_nb`, but they will appear as a single parameter in the final multi-index by having the same `level` in [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-1)>>> every_index = pd.Index(["D", "W", "M"], name="every") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-2)>>> num_tests_index = pd.Index([30, 50, 100], name="num_tests")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-3)>>> fees_index = pd.Index([0.0, 0.005, 0.01], name="fees")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-5)>>> range_starts = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-6)>>> range_ends = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-7)>>> for every in every_index:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-8)... index_ranges = symbol_wrapper.get_index_ranges(every=every)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-9)... range_starts.append(index_ranges[0])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-10)... range_ends.append(index_ranges[1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-11)>>> num_tests = num_tests_index.tolist()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-13)>>> range_starts = vbt.Param(range_starts, level=0, keys=every_index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-14)>>> range_ends = vbt.Param(range_ends, level=0, keys=every_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-15)>>> num_tests = vbt.Param(num_tests, level=1, keys=num_tests_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-20-16)>>> fees = vbt.Param(fees_index.values, level=2, keys=fees_index)
 
[/code]

 1. 2. 

Finally, pass the prepared arguments to the parameterized function, the same way as if we had passed them to `optimize_portfolio_nb`!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-1)>>> sharpe_ratios = param_optimize_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-2)... data.get("Close").values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-3)... data.get("Open").values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-4)... range_starts,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-5)... range_ends,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-6)... sharpe_optimize_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-7)... optimize_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-8)... data.get("Close").values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-9)... num_tests, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-10)... ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-11)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-12)... fees=fees,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-13)... init_cash=init_cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-14)... group=vbt.Rep("config_idx")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-21-15)... )
 
[/code]

Chunk 7/7

Using Dask, each function call executes in roughly 10 milliseconds! 

Let's take a look at the generated Sharpe ratios:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-1)>>> sharpe_ratios
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-2)every num_tests fees 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-3)D 30 0.000 2.208492
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-4) 0.005 0.412934
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-5) 0.010 -1.393060
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-6) 50 0.000 2.305169
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-7) 0.005 0.396711
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-8) 0.010 -1.444904
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-9) 100 0.000 2.202177
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-10) 0.005 0.380674
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-11) 0.010 -1.824848
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-12)W 30 0.000 2.507784
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-13) 0.005 2.297914
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-14) 0.010 1.962726
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-15) 50 0.000 2.358747
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-16) 0.005 1.940125
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-17) 0.010 1.736605
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-18) 100 0.000 2.563558
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-19) 0.005 2.365637
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-20) 0.010 1.877434
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-21)M 30 0.000 1.514242
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-22) 0.005 1.606507
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-23) 0.010 1.859369
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-24) 50 0.000 1.890288
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-25) 0.005 1.555012
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-26) 0.010 1.479636
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-27) 100 0.000 1.327935
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-28) 0.005 1.847109
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-29) 0.010 1.659961
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-22-30)dtype: float64
 
[/code]

We could have also stacked all the order records and analyzed them as part of a single portfolio, but this would require tiling the close price by the number of parameter combinations, which could become memory-expensive very quickly, thus basic looping is preferred here.


# Bonus 3: Hyperopt[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#bonus-3-hyperopt "Permanent link")

Instead of constructing and testing the full parameter grid, we can adopt a statistical approach. There are libraries, such as Hyperopt, that are tailored at minimizing objective functions.

> [Hyperopt](https://github.com/hyperopt/hyperopt) is a Python library for serial and parallel optimization over awkward search spaces, which may include real-valued, discrete, and conditional dimensions.

To use Hyperopt, we need to implement the objective function first. This is an easy task in our case:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-1)>>> def objective(kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-2)... close_values = data.get("Close").values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-3)... open_values = data.get("Open").values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-4)... index_ranges = symbol_wrapper.get_index_ranges(every=kwargs["every"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-5)... order_records = optimize_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-6)... close_values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-7)... open_values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-8)... index_ranges[0], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-9)... index_ranges[1], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-10)... sharpe_optimize_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-11)... optimize_args=(close_values, kwargs["num_tests"], ann_factor),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-12)... fees=vbt.to_2d_array(kwargs["fees"]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-13)... init_cash=init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-15)... pf = vbt.Portfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-16)... wrapper=symbol_wrapper.regroup(True), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-17)... close=data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-18)... order_records=order_records, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-19)... log_records=np.array([]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-20)... cash_sharing=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-21)... init_cash=init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-23-23)... return -pf.sharpe_ratio 
 
[/code]

 1. 2. 3. 

Then, we need to construct the grid:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-1)>>> from hyperopt import fmin, tpe, hp
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-3)>>> space = {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-4)... "every": hp.choice("every", ["%dD" % n for n in range(1, 100)]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-5)... "num_tests": hp.quniform("num_tests", 5, 100, 1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-6)... "fees": hp.uniform('fees', 0, 0.05)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-24-7)... }
 
[/code]

Finally, let's search for the best candidate:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-1)>>> best = fmin(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-2)... fn=objective,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-3)... space=space,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-4)... algo=tpe.suggest,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-5)... max_evals=30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-7)100%|██████| 30/30 [00:01<00:00, 24.11trial/s, best loss: -2.4913128485273424]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-9)>>> best
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-25-10){'every': 92, 'fees': 0.018781236093979012, 'num_tests': 46.0}
 
[/code]

Here's the [official tutorial](https://github.com/hyperopt/hyperopt/wiki/FMin) to help you get started.


# Bonus 4: Hybrid[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#bonus-4-hybrid "Permanent link")

We've covered generation of weights strictly prior and during the simulation, but what about use cases located somewhere in-between? For instance, how can we use external libraries (which usually cannot be Numba compiled) while still having access to the simulated state such as the current portfolio value? Disabling Numba completely and running the external optimization function as part of the simulation would be too slow and no better than doing the same with backtrader or any other conventional backtesting software. But here's a neat trick: simulate portfolio in chunks! For example, allocate weights, simulate a portfolio for a specific period of time, evaluate the portfolio, and repeat. If done correctly, the portfolios used for evaluation should closely match the performance of the post-generation portfolio.

Let's create an optimization function that allocates equal weights, but only if the current allocation deviates from the target allocation by a certain percentage amount:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-1)>>> def optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-2)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-3)... index_slice, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-4)... temp_allocations, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-5)... temp_pfs, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-6)... threshold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-7)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-8)... sub_data = data.iloc[index_slice]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-9)... if len(temp_allocations) > 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-10)... prev_allocation = sub_data.symbol_wrapper.wrap( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-11)... [temp_allocations[-1]], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-12)... index=sub_data.wrapper.index[[0]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-14)... prev_pfo = vbt.PortfolioOptimizer.from_allocations( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-15)... sub_data.symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-16)... prev_allocation
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-18)... if len(temp_pfs) > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-19)... init_cash = temp_pfs[-1].cash.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-20)... init_position = temp_pfs[-1].assets.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-21)... init_price = temp_pfs[-1].close.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-22)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-23)... init_cash = 100.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-24)... init_position = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-25)... init_price = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-26)... prev_pf = prev_pfo.simulate( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-27)... sub_data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-28)... init_cash=init_cash, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-29)... init_position=init_position,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-30)... init_price=init_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-31)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-32)... temp_pfs.append(prev_pf)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-33)... should_rebalance = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-34)... curr_alloc = prev_pf.allocations.iloc[-1].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-35)... if (np.abs(curr_alloc - temp_allocations[-1]) >= threshold).any():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-36)... should_rebalance = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-37)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-38)... should_rebalance = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-39)... n_symbols = len(sub_data.symbols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-40)... if should_rebalance:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-41)... new_alloc = np.full(n_symbols, 1 / n_symbols) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-42)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-43)... new_alloc = np.full(n_symbols, np.nan) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-44)... temp_allocations.append(new_alloc)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-45)... return new_alloc
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-46)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-47)>>> pfs = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-48)>>> allocations = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-49)>>> pfopt = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-50)... data.symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-51)... optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-52)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-53)... vbt.Rep("index_slice"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-54)... allocations,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-55)... pfs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-56)... 0.03, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-57)... every="W"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-58)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-26-59)>>> pf = pfopt.simulate(data)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 

How do we make sure that all the used sub-portfolios closely resemble the reality? Let's compare the final value of each sub-portfolio to the corresponding value in the monolithic portfolio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-1)>>> final_values = pd.concat(map(lambda x: x.value[[-1]], pfs))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-2)>>> final_values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-4)2020-01-18 23:00:00+00:00 117.448601
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-5)2020-01-25 23:00:00+00:00 109.741201
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-6)2020-02-01 23:00:00+00:00 126.428241
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-7)2020-02-08 23:00:00+00:00 143.399207
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-8)2020-02-15 23:00:00+00:00 157.673925
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-9) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-10)2020-11-28 23:00:00+00:00 306.180144
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-11)2020-12-05 23:00:00+00:00 312.231039
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-12)2020-12-12 23:00:00+00:00 289.465806
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-13)2020-12-19 23:00:00+00:00 338.756466
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-14)2020-12-26 23:00:00+00:00 313.229099
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-15)Name: group, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-17)>>> pd.testing.assert_series_equal( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-18)... final_values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-19)... pf.value.loc[final_values.index],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#__codelineno-27-20)... )
 
[/code]

 1. 

Perfect match! ![⛳](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/26f3.svg)


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/dynamic/#summary "Permanent link")

With regular portfolio review, we can make adjustments and increase the likelihood we'll end up with comfortable returns while maintaining the amount of risk we're willing to carry. Diversification across asset classes is a risk-mitigation strategy, especially when spreading investments across a variety of asset classes. With vectorbt, we have powerful functionalities at our disposal to select optimal portfolios in a programmatic way. Not only there are tools that play well with third-party libraries, but there is an entire universe of options to easily implement and test any unique optimization strategy, especially when it takes advantage of acceleration, such as by compilation with Numba.

As we saw in this set of examples, vectorbt encourages us to adopt data science and to look at portfolio optimization from many angles to better understand how it affects the results. For instance, we can use the [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) class to quickly tune various parameters in weight generation and rebalancing timing, and upon a satisfactory pre-analysis, feed the optimizer into a simulator to post-analyze the chosen strategy. Or, we can decide to implement our own optimizer from the ground up to control the entire execution process. In this case, we can extract target allocations and other metadata from within the simulation and analyze them later. So many possibilities... ![💭](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4ad.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/portfolio-optimization/dynamic.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PortfolioOptimization.ipynb)