requests_

#  requests_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/requests_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#vectorbtpro.utils.requests_ "Permanent link")

Utilities for requests.

* * *

## requests_retry_session function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/requests_.py#L24-L42 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#vectorbtpro.utils.requests_.requests_retry_session "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-1)requests_retry_session(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-2)    retries=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-3)    backoff_factor=0.3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-4)    status_forcelist=(500, 502, 504),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-5)    session=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-0-6))
    

Retry `retries` times if unsuccessful.

* * *

## text_to_giphy_url function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/requests_.py#L45-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#vectorbtpro.utils.requests_.text_to_giphy_url "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-1-1)text_to_giphy_url(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-1-2)    text,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-1-3)    api_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-1-4)    weirdness=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/requests_/#__codelineno-1-5))
    

Translate text to GIF.

See <https://engineering.giphy.com/contextually-aware-search-giphy-gets-work-specific/>
