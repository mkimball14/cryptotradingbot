# Signals[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#signals "Permanent link")

Question

Learn more in [Signal development tutorial](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/).


# Cleaning[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#cleaning "Permanent link")

Only two arrays can be cleaned at a time, for more arrays write a custom Numba function that does the job.

Clean 4 arrays
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-2)def custom_clean_nb(long_en, long_ex, short_en, short_ex):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-3) new_long_en = np.full_like(long_en, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-4) new_long_ex = np.full_like(long_ex, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-5) new_short_en = np.full_like(short_en, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-6) new_short_ex = np.full_like(short_ex, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-8) for col in range(long_en.shape[1]): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-9) position = 0 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-10) for i in range(long_en.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-11) if long_en[i, col] and position != 1:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-12) new_long_en[i, col] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-13) position = 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-14) elif short_en[i, col] and position != -1:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-15) new_short_en[i, col] = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-16) position = -1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-17) elif long_ex[i, col] and position == 1:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-18) new_long_ex[i, col] = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-19) position = 0
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-20) elif short_ex[i, col] and position == -1:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-21) new_short_ex[i, col] = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-22) position = 0
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/signals/#__codelineno-0-24) return new_long_en, new_long_ex, new_short_en, new_short_ex
 
[/code]

 1. 2. 3. 4. 

Tip

Convert each input array to NumPy with `arr = vbt.to_2d_array(df)` and then each output array back to Pandas with `new_df = df.vbt.wrapper.wrap(arr)`.