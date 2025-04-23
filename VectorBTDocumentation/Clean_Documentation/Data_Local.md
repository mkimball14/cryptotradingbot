Skip to content 

_What's new_ : SearchVBT, ChatVBT, and [**more**](https://vectorbt.pro/pvt_7a467f6b/features)

[ ![logo](../../../assets/logo/logo.svg) ](../../.. "VectorBT® PRO")

VectorBT® PRO  v2025.3.1 

Local 

[ ](javascript:void\(0\) "Share")

Initializing search 




[ vectorbt.pro  ](https://github.com/polakowo/vectorbt.pro "Go to repository")

  * [ Getting started ](../../..)
  * [ Features ](../../../features/overview/)
  * [ Tutorials ](../../../tutorials/overview/)
  * [ Documentation ](../../overview/)
  * [ API ](../../../api/)
  * [ Cookbook ](../../../cookbook/overview/)
  * [ Terms ](../../../terms/terms-of-use/)



[ ![logo](../../../assets/logo/logo.svg) ](../../.. "VectorBT® PRO") VectorBT® PRO 

[ vectorbt.pro  ](https://github.com/polakowo/vectorbt.pro "Go to repository")

  * [ Getting started  ](../../..)
  * [ Features  ](../../../features/overview/)
  * [ Tutorials  ](../../../tutorials/overview/)
  * Documentation  Documentation 
    * [ Overview  ](../../overview/)
    * [ Fundamentals  ](../../fundamentals/)
    * [ Building blocks  ](../../building-blocks/)
    * Data  Data 
      * [ Data  ](../)
      * Local  [ Local  ](./) Table of contents 
        * Pickling 
        * Saving 
          * CSV 
          * HDF 
          * Feather & Parquet 
          * SQL 
          * DuckDB 
        * Loading 
          * CSV 
            * Chunking 
          * HDF 
            * Chunking 
          * Feather & Parquet 
          * SQL 
            * Chunking 
          * DuckDB 
        * Updating 
          * CSV & HDF 
          * Feather & Parquet 
          * SQL 
          * DuckDB 
      * [ Remote  ](../remote/)
      * [ Synthetic  ](../synthetic/)
      * [ Scheduling  ](../scheduling/)
    * Indicators  Indicators 
      * [ Indicators  ](../../indicators/)
      * [ Development  ](../../indicators/development/)
      * [ Analysis  ](../../indicators/analysis/)
      * [ Parsers  ](../../indicators/parsers/)
    * Portfolio  Portfolio 
      * [ Portfolio  ](../../portfolio/)
      * [ From orders  ](../../portfolio/from-orders/)
      * [ From signals  ](../../portfolio/from-signals/)
    * [ To be continued...  ](../../to-be-continued/)
  * [ API  ](../../../api/)
  * [ Cookbook  ](../../../cookbook/overview/)
  * [ Terms  ](../../../terms/terms-of-use/)



  1. [ Documentation  ](../../overview/)
  2. [ Data  ](../)



#  Local¶

Repeatedly hitting remote API endpoints is costly, thus it's very important to cache data locally. Luckily, vectorbt implements a range of ways for managing local data.

## Pickling¶

Like any other class subclassing [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable), we can save any [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) instance to the disk using [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save) and load it back using [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load). This will pickle the entire Python object including the stored Pandas objects, symbol dictionaries, and settings:
    
    
    >>> from vectorbtpro import *
    
    >>> yf_data = vbt.YFData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     start="2020-01-01", 
    ...     end="2020-01-05"
    ... )
    

Symbol 2/2
    
    
    >>> yf_data.save("yf_data")  # (1)!
    
    >>> yf_data = vbt.YFData.load("yf_data")  # (2)!
    >>> yf_data = yf_data.update(end="2020-01-06")
    >>> yf_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    2020-01-05 00:00:00+00:00  7411.317383  136.276779
    

  1. Automatically adds the extension `.pickle` to the file name
  2. The object can be loaded back in a new runtime or even on another machine, just make sure to use a compatible vectorbt version



Important

The class definition won't be saved. If a new version of vectorbt introduces a breaking change to the [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) constructor, the object may not load. In such a case, you can manually create a new instance: 
    
    
    >>> yf_data = vbt.YFData(**vbt.Configured.load("yf_data").config)
    

## Saving¶

While pickling is a pretty fast and convenient solution to storing Python objects of any size, the pickled file is effectively a black box that requires a Python interpreter to be unboxed, which makes it unusable for many tasks since it cannot be imported by most other data-driven tools. To lift this limitation, the [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) class allows us for saving exclusively the stored Pandas objects into one to multiple files of a tabular format.

### CSV¶

The first supported file format is the [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format, which is implemented by the instance method [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv). This method takes a path to the directory where the data should be stored (`path_or_buf`), and saves each symbol in a separate file using [DataFrame.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html).

By default, it appends the extension `.csv` to each symbol, and saves the files into the current directory:
    
    
    >>> yf_data.to_csv()
    

Info

Multiple symbols cannot be stored inside a single CSV file.

We can list all CSV files in the current directory using [list_files](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_files):
    
    
    >>> vbt.list_files("*.csv")
    [PosixPath('ETH-USD.csv'), PosixPath('BTC-USD.csv')]
    

A cleaner approach is to save all the data in a separate directory:
    
    
    >>> vbt.remove_file("BTC-USD.csv")  # (1)!
    >>> vbt.remove_file("ETH-USD.csv")
    
    >>> yf_data.to_csv("data", mkdir_kwargs=dict(mkdir=True))  # (2)!
    

  1. Delete the CSV files created previously from the current directory
  2. Save the files to the directory with the name `data`. If the directory doesn't exist, create a new one by passing keyword arguments `mkdir_kwargs` down to [check_mkdir](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.check_mkdir).



To save the data as tab-separated values (TSV):
    
    
    >>> yf_data.to_csv("data", ext="tsv")
    
    >>> vbt.list_files("data/*.tsv")
    [PosixPath('data/BTC-USD.tsv'), PosixPath('data/ETH-USD.tsv')]
    

Hint

You don't have to pass `sep`: vectorbt will recognize the extension and pass the correct delimiter. But you can still override this argument if you need to split the data by a special character.

Similarly to [Data.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.pull), we can provide any argument as a feature/symbol dictionary of type [key_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.key_dict) to define different rules for different symbols. Let's store the symbols from our example in separate directories:
    
    
    >>> yf_data.to_csv(
    ...     vbt.key_dict({
    ...         "BTC-USD": "btc_data",
    ...         "ETH-USD": "eth_data"
    ...     }), 
    ...     mkdir_kwargs=dict(mkdir=True)
    ... )
    

We can also specify the path to each file by using `path_or_buf` (first argument):
    
    
    >>> yf_data.to_csv(
    ...     vbt.key_dict({
    ...         "BTC-USD": "data/btc_usd.csv",
    ...         "ETH-USD": "data/eth_usd.csv"
    ...     }), 
    ...     mkdir_kwargs=dict(mkdir=True)
    ... )
    

To delete the entire directory (as part of a clean-up, for example):
    
    
    >>> vbt.remove_dir("btc_data", with_contents=True)
    >>> vbt.remove_dir("eth_data", with_contents=True)
    >>> vbt.remove_dir("data", with_contents=True)
    

### HDF¶

The second supported file format is the [HDF](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) format, which is implemented by the instance method [Data.to_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_hdf). In contrast to [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv), this method can store multiple symbols inside a single file, where symbols are distributed as HDF keys.

By default, it creates a new file with the same name as the name of the data class and an extension `.h5`, and saves each symbol under a separate key in that file using [DataFrame.to_hdf](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_hdf.html):
    
    
    >>> yf_data.to_hdf()
    
    >>> vbt.list_files("*.h5")
    [PosixPath('YFData.h5')]
    

To see the list of all the groups and keys contained in an HDF file:
    
    
    >>> with pd.HDFStore("YFData.h5") as store:
    ...     print(store.keys())
    ['/BTC-USD', '/ETH-USD']
    

Use the `key` argument to manually specify the key of a particular symbol:
    
    
    >>> yf_data.to_hdf(
    ...     key=vbt.key_dict({
    ...         "BTC-USD": "btc_usd",
    ...         "ETH-USD": "eth_usd"
    ...     })
    ... )
    

Hint

If there is only one symbol, you don't need to use [key_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.key_dict), just pass `key="btc_usd"`.

We can also specify the path to each file by using `path_or_buf` (first argument):
    
    
    >>> yf_data.to_hdf(
    ...     vbt.key_dict({
    ...         "BTC-USD": "btc_usd.h5",
    ...         "ETH-USD": "eth_usd.h5"
    ...     })
    ... )
    

The arguments `path_or_buf` and `key` can be combined.

Any other argument behaves the same as for [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv).

### Feather & Parquet¶

The third supported option is saving to a Feather/Parquet file, which is implemented by the instance method [Data.to_feather](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_feather) and [Data.to_parquet](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_parquet) respectively. Feather is an unmodified raw columnar Arrow memory and is designed for short-term storage, while Parquet is often more expensive to write but features more layers of encoding and compression, making Parquet files often much smaller than Feather files. Another major difference between both is that we cannot partition data with Feather, neither we can natively store the index - it must be stored as a separate column, which is done automatically by vectorbt. We'll show to how to save to a Parquet memory.

By default, it appends the extension `.parquet` to each symbol, and saves the files into the current directory:
    
    
    >>> yf_data.to_parquet()
    

Info

Multiple symbols cannot be stored inside a single Parquet file.

Other saving options are very similar to CSV saving options.

Apart from storing each DataFrame to a separate Parquet file, we can partition the DataFrame either by columns or rows. Partitioning by columns is controlled by the argument `partition_cols`, which takes a list of column names. Columns must be present in the data and are partitioned in the order they are given. Partitioning by rows is controlled by the argument `partition_by`, which takes a grouping instruction such as a frequency, an index (also multi-index), a Pandas grouper or resampler, or a vectorbt's own [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper) instance, and together with `groupby_kwargs` creates a new `Grouper` instance to be used in partitioning. Then, it attaches the groups as columns to each DataFrame, and provides the name of these columns as `partition_cols`. By default, if there's only one column, it will be named "group", and if there are more columns, they will be named after "group_{index}". To use own names, enable `keep_groupby_names`.

Info

When `partition_cols` or `partition_by` is provided, each symbol will be stored to a separate directory.

Let's partition our data by two days and save each DataFrame to its own Parquet directory:
    
    
    >>> yf_data.to_parquet(partition_by="2 days")
    

Let's visualize the directory tree for the `BTC-USD` symbol:
    
    
    >>> vbt.print_dir_tree("BTC-USD")
    BTC-USD
    ├── group=2020-01-01%2000%3A00%3A00.000000000
    │   └── 190335d948d04504b42a8d35ffb08f47-0.parquet
    └── group=2020-01-03%2000%3A00%3A00.000000000
        └── 190335d948d04504b42a8d35ffb08f47-0.parquet
    
    2 directories, 2 files
    

### SQL¶

The fourth supported option is saving to a SQL database, which is implemented by the instance method [Data.to_sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_sql). It requires [SQLAlchemy](https://www.sqlalchemy.org/) to be installed. This method takes the engine (object, name, or URL) and saves each symbol as a separate table to the database managed by the engine using [`pd.to_sql`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html). The engine can be created either manually using SQLAlchemy's `create_engine` functon, or we can pass an URL and it will be created for us; in this case, it will be disposed at the end of the call.

Let's create a SQL database file in our working directory and store the data there:
    
    
    >>> SQLITE_URL = "sqlite:///yf_data.db"
    
    >>> yf_data.to_sql(SQLITE_URL)
    

If we want to continue working with the same engine and don't want to create another engine object, we can pass `return_engine=True` to return the engine object.
    
    
    >>> engine = yf_data.to_sql(SQLITE_URL, if_exists="replace", return_engine=True)
    

We can also specify the schema by using the `schema` argument. Note, however, that some databases, such as SQLite, do not support the concept of a schema. If the schema doesn't exist, it will be created automatically.
    
    
    >>> POSTGRESQL_URL = "postgresql://postgres:postgres@localhost:5432"
    
    >>> yf_data.to_sql(POSTGRESQL_URL, schema="yf_data")
    

Use the `table` argument to manually specify the table name of a particular symbol:
    
    
    >>> yf_data.to_sql(
    ...     POSTGRESQL_URL,
    ...     table=vbt.key_dict({
    ...         "BTC-USD": "BTC_USD",
    ...         "ETH-USD": "ETH_USD"
    ...     })
    ... )
    

Info

If the index is datetime-like and/or there are datetime-like columns, the method will localize/convert them to UTC first. To change this behavior, set the argument `to_utc` to False to deactivate, to "index" to apply it to the index only, and to "columns" to apply it to the columns only. In addition, the UTC timezone will be removed if `remove_utc_tz` is True (default) since some databases do not support timezone-aware timestamps; other timezones are not touched.

### DuckDB¶

Hint

Previous method (using SQLAlchemy) can be used to write to a DuckDB database as well. For this, you have to install the [duckdb-engine](https://pypi.org/project/duckdb-engine/) extension.

The fifth supported option is very similar to the previous one and allows to save data to a DuckDB database or CSV/Parquet/JSON file(s). It's implemented by the instance method [Data.to_duckdb](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_duckdb). It requires [DuckDB](https://duckdb.org/) to be installed. This method takes the connection (object or URL) and saves each symbol as a separate table to the database managed by the connection or to file(s) using a SQL query. The connection can be created either manually using DuckDB's `connect` functon, or we can pass an URL and it will be created for us. If neither connection or connection-related keyword arguments are passed, the default in-memory connection is used.

Let's create a DuckDB database file in our working directory and store the data there:
    
    
    >>> DUCKDB_URL = "database.duckdb"
    
    >>> yf_data.to_duckdb(DUCKDB_URL)
    

We can also specify the catalog and schema by using the `catalog` and `schema` argument respectively. If the schema doesn't exist, it will be created automatically.
    
    
    >>> yf_data.to_duckdb(DUCKDB_URL, schema="yf_data")
    

Use the `table` argument to manually specify the table name of a particular symbol:
    
    
    >>> yf_data.to_duckdb(
    ...     DUCKDB_URL,
    ...     table=vbt.key_dict({
    ...         "BTC-USD": "BTC_USD",
    ...         "ETH-USD": "ETH_USD"
    ...     })
    ... )
    

There's also an option to save each DataFrame to a CSV, Parquet, or JSON file, rather than to the database itself. For this, we can use `write_format`, `write_path`, and `write_options`. The operation is performed using [`COPY TO`](https://duckdb.org/docs/sql/statements/copy.html). If `write_path` is a directory (which is the working directory by default), then each DataFrame will be saved to a file based on the specified format. Format is not needed if `write_path` points to a file with a recognizable extension. The options argument can be used to specify the options for writing; it can be either a string as in the DuckDB's documentation, such as `HEADER 1, DELIMITER ','`, or as a dictionary that will be translated into such a string by vectorbt, such as `dict(header=1, delimiter=',')`.

Let's save all data to Parquet files:
    
    
    >>> yf_data.to_duckdb(
    ...     DUCKDB_URL,
    ...     write_path="data",
    ...     write_format="parquet",
    ...     mkdir_kwargs=dict(mkdir=True)
    ... )
    

Info

See the notes in the SQL section.

## Loading¶

To import any previously stored data in a tabular format, we can either use Pandas or vectorbt's preset data classes specifically crafted for this job.

### CSV¶

Each CSV dataset can be manually imported using [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html):
    
    
    >>> yf_data.to_csv()
    
    >>> pd.read_csv("BTC-USD.csv", index_col=0, parse_dates=True)
                                      Open         High          Low        Close  \
    Date                                                                            
    2020-01-01 00:00:00+00:00  7194.892090  7254.330566  7174.944336  7200.174316   
    2020-01-02 00:00:00+00:00  7202.551270  7212.155273  6935.270020  6985.470215   
    2020-01-03 00:00:00+00:00  6984.428711  7413.715332  6914.996094  7344.884277   
    2020-01-04 00:00:00+00:00  7345.375488  7427.385742  7309.514160  7410.656738   
    
                                    Volume  Dividends  Stock Splits  
    Date                                                             
    2020-01-01 00:00:00+00:00  18565664997        0.0           0.0  
    2020-01-02 00:00:00+00:00  20802083465        0.0           0.0  
    2020-01-03 00:00:00+00:00  28111481032        0.0           0.0  
    2020-01-04 00:00:00+00:00  18444271275        0.0           0.0 
    

To join the imported datasets and wrap them with [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data), we can use [Data.from_data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.from_data):
    
    
    >>> btc_usd = pd.read_csv("BTC-USD.csv", index_col=0, parse_dates=True)
    >>> eth_usd = pd.read_csv("ETH-USD.csv", index_col=0, parse_dates=True)
    
    >>> data = vbt.Data.from_data({"BTC-USD": btc_usd, "ETH-USD": eth_usd})
    >>> data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

To relieve the user of the burden of manually searching, fetching, and merging CSV data, vectorbt implements the class [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData), which can recursively explore directories for CSV files, resolve path expressions using [glob](https://docs.python.org/3/library/glob.html), translate the found paths into symbols, and import and join tabular data - all automatically via a single command. It subclasses another class - [FileData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData), which takes the whole credit for making all the above possible. 

At the heart of the path matching functionality is the class method [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull), which iterates over the specified paths, and for each one, finds the matching absolute paths using another class method [FileData.match_path](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.match_path), and calls the abstract class method [FileData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.fetch_key) to pull the data from the file located under that path.

Let's explore how [FileData.match_path](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.match_path) works by creating a directory with the name `data` and storing various empty files inside:
    
    
    >>> vbt.make_dir("data", exist_ok=True)
    >>> vbt.make_file("data/file1.csv")
    >>> vbt.make_file("data/file2.tsv")
    >>> vbt.make_file("data/file3")
    
    >>> vbt.make_dir("data/sub-data", exist_ok=True)
    >>> vbt.make_file("data/sub-data/file1.csv")
    >>> vbt.make_file("data/sub-data/file2.tsv")
    >>> vbt.make_file("data/sub-data/file3")
    

To get a better visual representation of the created contents:
    
    
    >>> vbt.print_dir_tree("data")
    data
    ├── file1.csv
    ├── file2.tsv
    ├── file3
    └── sub-data
        ├── file1.csv
        ├── file2.tsv
        └── file3
    
    1 directories, 6 files
    

Match all files in a directory:
    
    
    >>> vbt.FileData.match_path("data")
    [PosixPath("data/file1.csv"),
     PosixPath("data/file2.tsv"),
     PosixPath("data/file3")]
    

Match all CSV files in a directory:
    
    
    >>> vbt.FileData.match_path("data/*.csv")
    [PosixPath("data/file1.csv")]
    

Match all CSV files in a directory recursively:
    
    
    >>> vbt.FileData.match_path("data/**/*.csv")
    [PosixPath("data/file1.csv"), PosixPath("data/sub-data/file1.csv")]
    

For more details, see the documentation of [glob](https://docs.python.org/3/library/glob.html).

Going back to [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull): it can match one or multiple path expressions like above, provided either as `symbols` (if `paths` is None) or `paths`. Whenever we provide paths as symbols, the method calls [FileData.path_to_symbol](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.path_to_symbol) on each matched path to parse the name of the symbol (by default, it's the stem of the path):
    
    
    >>> vbt.CSVData.pull("BTC-USD.csv").symbols
    ["BTC-USD"]
    
    >>> vbt.CSVData.pull(["BTC-USD.csv", "ETH-USD.csv"]).symbols
    ["BTC-USD", "ETH-USD"]
    
    >>> vbt.CSVData.pull("*.csv").symbols
    ["BTC-USD", "ETH-USD"]
    
    >>> vbt.CSVData.pull(["BTC/USD", "ETH/USD"], paths="*.csv").symbols  # (1)!
    ["BTC/USD", "ETH/USD"]
    
    >>> vbt.CSVData.pull(  # (2)!
    ...     ["BTC/USD", "ETH/USD"], 
    ...     paths=["BTC-USD.csv", "ETH-USD.csv"]
    ... ).symbols
    ["BTC/USD", "ETH/USD"]
    

  1. Specify the symbols explicitly
  2. Specify the symbols and the paths explicitly



Note

Don't forget to filter by the `.csv`, `.tsv`, or any other extension in the expression.

Whenever we use a wildcard such as `*.csv`, vectorbt will sort the matched paths (per each path expression). To disable sorting, set `sort_paths` to False. We can also disable the path matching mechanism entirely by setting `match_paths` to False, which will forward all arguments directly to [CSVData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData.fetch_key):
    
    
    >>> vbt.CSVData.pull(
    ...     ["BTC/USD", "ETH/USD"], 
    ...     paths=vbt.key_dict({
    ...         "BTC/USD": "BTC-USD.csv",
    ...         "ETH/USD": "ETH-USD.csv"
    ...     }),
    ...     match_paths=False
    ... ).symbols
    ["BTC/USD", "ETH/USD"]
    

Hint

Instead of paths, you can pass objects of any type supported by the `filepath_or_buffer` argument in [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).

To sum up the techniques discussed above, let's create an empty directory with the name `data` (again), write the `BTC-USD` symbol to a CSV file and the `ETH-USD` symbol to a TSV file, and load both datasets with a single `fetch` call:
    
    
    >>> vbt.remove_dir("data", with_contents=True)
    
    >>> yf_data.to_csv(
    ...     "data",
    ...     ext=vbt.key_dict({
    ...         "BTC-USD": "csv",
    ...         "ETH-USD": "tsv"
    ...     }), 
    ...     mkdir_kwargs=dict(mkdir=True)
    ... )
    
    >>> csv_data = vbt.CSVData.pull(["data/*.csv", "data/*.tsv"])  # (1)!
    

  1. The delimiter is recognized automatically based on the file's extension



Symbol 2/2
    
    
    >>> csv_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

Note

Providing two paths with wildcards (`*`) doesn't mean we will get exactly two symbols: there may be more than one path matching each wildcard. You should imagine the two expressions above as being combined using the OR rule into a single expression `data/*.{csv,tsv}` (which isn't supported by [glob](https://docs.python.org/3/library/glob.html), unfortunately).

The last but not the least is regex matching with `match_regex`, which instructs vectorbt to iterate over all matched paths and additionally validate them against a regular expression:
    
    
    >>> vbt.CSVData.pull(
    ...     "data/**/*",  # (1)!
    ...     match_regex=r"^.*\.(csv|tsv)$"  # (2)!
    ... ).close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

  1. Recursively get the paths of all files in all subdirectories in `data`
  2. Filter out any paths that do not end with `csv` or `tsv`



Any other argument is being passed directly to [CSVData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData.fetch_key) and then to [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).

#### Chunking¶

As an alternative to reading everything into memory, Pandas allows us to read data in chunks. In the case of CSV, we can load only a subset of lines into memory at any given time. Even though this is a very useful concept for processing big data, chunking doesn't provide many benefits when the only goal is to load the entire data into memory anyway.

Where chunking becomes really useful though is data filtering! The class [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) as well as the function [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) it's based on don't have arguments for skipping rows based on their content, only based on their row index. For example, to skip all the data that comes before `2020-01-03`, we would need to load the entire data into memory first. But once data becomes too large, we may run out of RAM. To account for this, we can split data into chunks and check the condition on each chunk at a time.

We have two options from here:

  1. Use `chunksize` to split data into chunks of a fixed length
  2. Use `iterator` to return an iterator that can be used to read chunks of a variable length



Both options make [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) return an iterator of type `TextFileReader`. To make use of this iterator, [CSVData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData.fetch_key) accepts a user-defined function `chunk_func` that should 1) accept the iterator, 2) select, process, and concatenate chunks, and 3) return a Series or a DataFrame. 

Let's fetch only those rows that have the date ending with an even day:
    
    
    >>> csv_data = vbt.CSVData.pull(
    ...     ["data/*.csv", "data/*.tsv"],
    ...     chunksize=1,  # (1)!
    ...     chunk_func=lambda iterator: pd.concat([
    ...         df 
    ...         for df in iterator
    ...         if (df.index.day % 2 == 0).all()
    ...     ], axis=0)
    ... )
    

  1. Each chunk will be a DataFrame with one row



Symbol 2/2
    
    
    >>> csv_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

Note

Chunking should mainly be used when memory considerations are more important than speed considerations.

### HDF¶

Each HDF dataset can be manually imported using [pandas.read_hdf](https://pandas.pydata.org/docs/reference/api/pandas.read_hdf.html):
    
    
    >>> yf_data.to_hdf()
    
    >>> pd.read_hdf("YFData.h5", key="BTC-USD")
                                      Open         High          Low        Close  \
    Date                                                                            
    2020-01-01 00:00:00+00:00  7194.892090  7254.330566  7174.944336  7200.174316   
    2020-01-02 00:00:00+00:00  7202.551270  7212.155273  6935.270020  6985.470215   
    2020-01-03 00:00:00+00:00  6984.428711  7413.715332  6914.996094  7344.884277   
    2020-01-04 00:00:00+00:00  7345.375488  7427.385742  7309.514160  7410.656738   
    
                                    Volume  Dividends  Stock Splits  
    Date                                                             
    2020-01-01 00:00:00+00:00  18565664997        0.0           0.0  
    2020-01-02 00:00:00+00:00  20802083465        0.0           0.0  
    2020-01-03 00:00:00+00:00  28111481032        0.0           0.0  
    2020-01-04 00:00:00+00:00  18444271275        0.0           0.0  
    

Similarly to [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) for CSV data, vectorbt implements a preset class [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) tailored for reading HDF files. It shares the same parent class [FileData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData) and its fetcher [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull). But in contrast to CSV datasets, which are stored one per file, HDF datasets are stored one per key in an HDF file. Since groups and keys follow the [POSIX](https://en.wikipedia.org/wiki/POSIX)-style hierarchy with `/`-separators, we can query them in the same way as we query directories and files in a regular file system.

Let's illustrate this by using [HDFData.match_path](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData.match_path), which upgrades [FileData.match_path](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.match_path) with a proper discovery and handling of HDF groups and keys:
    
    
    >>> vbt.HDFData.match_path("YFData.h5")
    [PosixPath("YFData.h5/BTC-USD"), PosixPath("YFData.h5/ETH-USD")]
    

As we can see, the HDF file above is now being treated as a directory while groups and keys are being treated as subdirectories and files respectively. This makes importing HDF datasets as easy as CSV datasets:
    
    
    >>> vbt.HDFData.pull("YFData.h5/BTC-USD").symbols  # (1)!
    ["BTC-USD"]
    
    >>> vbt.HDFData.pull("YFData.h5").symbols  # (2)!
    ["BTC-USD", "ETH-USD"]
    
    >>> vbt.HDFData.pull("YFData.h5/BTC*").symbols  # (3)!
    ["BTC-USD"]
    
    >>> vbt.HDFData.pull("*.h5/BTC-*").symbols  # (4)!
    ["BTC-USD"]
    

  1. Matches the key `BTC-USD` in `YFData.h5`
  2. Matches all keys in `YFData.h5`
  3. Matches all keys starting with `BTC` in `YFData.h5`
  4. Matches all keys starting with `BTC` in all HDF files



Any other argument behaves the same as for [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData), but now it's being passed directly to [HDFData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData.fetch_key) and then to [pandas.read_hdf](https://pandas.pydata.org/docs/reference/api/pandas.read_hdf.html).

#### Chunking¶

Chunking for HDF files is identical to that for CSV files, but with two exceptions: the data must be saved as a [PyTables](https://www.pytables.org/) Table structure by using `format="table"`, and the iterator is now of type `TableIterator` instead of `TextFileReader`.
    
    
    >>> yf_data.to_hdf(format="table")
    
    >>> hdf_data = vbt.HDFData.pull(
    ...     "YFData.h5",
    ...     chunksize=1,
    ...     chunk_func=lambda iterator: pd.concat([
    ...         df 
    ...         for df in iterator
    ...         if (df.index.day % 2 == 0).all()
    ...     ], axis=0)
    ... )
    

Symbol 2/2
    
    
    >>> hdf_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

### Feather & Parquet¶

Each Parquet dataset can be manually imported using [pandas.read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html):
    
    
    >>> yf_data.to_parquet()
    
    >>> pd.read_parquet("BTC-USD.parquet")
                                      Open         High          Low        Close  \
    Date                                                                            
    2020-01-01 00:00:00+00:00  7194.892090  7254.330566  7174.944336  7200.174316   
    2020-01-02 00:00:00+00:00  7202.551270  7212.155273  6935.270020  6985.470215   
    2020-01-03 00:00:00+00:00  6984.428711  7413.715332  6914.996094  7344.884277   
    2020-01-04 00:00:00+00:00  7345.375488  7427.385742  7309.514160  7410.656738   
    
                                    Volume  Dividends  Stock Splits  
    Date                                                             
    2020-01-01 00:00:00+00:00  18565664997        0.0           0.0  
    2020-01-02 00:00:00+00:00  20802083465        0.0           0.0  
    2020-01-03 00:00:00+00:00  28111481032        0.0           0.0  
    2020-01-04 00:00:00+00:00  18444271275        0.0           0.0  
    

Same goes for partitioned datasets:
    
    
    >>> yf_data2 = vbt.YFData.pull(
    ...     ["BNB-USD", "XRP-USD"], 
    ...     start="2020-01-01", 
    ...     end="2020-01-05"
    ... )
    >>> yf_data2.to_parquet(partition_by="2D")
    
    >>> pd.read_parquet("BNB-USD")  # (1)!
                                    Open       High        Low      Close  \
    Date                                                                    
    2020-01-01 00:00:00+00:00  13.730962  13.873946  13.654942  13.689083   
    2020-01-02 00:00:00+00:00  13.698126  13.715548  12.989974  13.027011   
    2020-01-03 00:00:00+00:00  13.035329  13.763709  13.012638  13.660452   
    2020-01-04 00:00:00+00:00  13.667442  13.921914  13.560008  13.891512   
    
                                  Volume  Dividends  Stock Splits  \
    Date                                                            
    2020-01-01 00:00:00+00:00  172980718        0.0           0.0   
    2020-01-02 00:00:00+00:00  156376427        0.0           0.0   
    2020-01-03 00:00:00+00:00  173683857        0.0           0.0   
    2020-01-04 00:00:00+00:00  182230374        0.0           0.0   
    
                                                       group  
    Date                                                      
    2020-01-01 00:00:00+00:00  2020-01-01 00:00:00.000000000  
    2020-01-02 00:00:00+00:00  2020-01-01 00:00:00.000000000  
    2020-01-03 00:00:00+00:00  2020-01-03 00:00:00.000000000  
    2020-01-04 00:00:00+00:00  2020-01-03 00:00:00.000000000  
    

  1. The path is pointing at a directory



Similarly to other classes for pulling data from local files, vectorbt implements preset classes [FeatherData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/feather/#vectorbtpro.data.custom.feather.FeatherData) and [ParquetData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/parquet/#vectorbtpro.data.custom.parquet.ParquetData) tailored for reading Feather and Parquet files respectively. They share the same parent class [FileData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData) and its fetcher [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull).

But first, let's discover any Parquet files or directories stored in the current working directory using [ParquetData.list_paths](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/parquet/#vectorbtpro.data.custom.parquet.ParquetData.list_paths). What it does is searching for any files that have a ".parquet" extension as well as any directories with partitioned datasets that follow the [Hive partitioning scheme](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.HivePartitioning.html).
    
    
    >>> vbt.ParquetData.list_paths()
    [PosixPath('BNB-USD'),
     PosixPath('BTC-USD.parquet'),
     PosixPath('ETH-USD.parquet'),
     PosixPath('XRP-USD')]
    
    >>> vbt.ParquetData.is_parquet_file("BTC-USD.parquet")
    True
    
    >>> vbt.ParquetData.is_parquet_dir("BNB-USD")
    True
    

This makes importing Parquet datasets as easy as any other file datasets:
    
    
    >>> vbt.ParquetData.pull("BTC-USD.parquet").symbols  # (1)!
    ['BTC-USD']
    
    >>> vbt.ParquetData.pull(["BTC-USD.parquet", "ETH-USD.parquet"]).symbols
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.ParquetData.pull("*.parquet").symbols  # (2)!
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.ParquetData.pull("BNB-USD").symbols  # (3)!
    ['BNB-USD']
    
    >>> vbt.ParquetData.pull(["BNB-USD", "XRP-USD"]).symbols
    ['BNB-USD', 'XRP-USD']
    
    >>> vbt.ParquetData.pull().symbols  # (4)!
    ['BNB-USD', 'BTC-USD', 'ETH-USD', 'XRP-USD']
    

  1. Pull a single-file dataset
  2. Pull all single-file datasets
  3. Pull a partitioned dataset
  4. Pull all single-file and partitioned datasets



But maybe you're wondering: what happens to that "group" column in partitioned datasets? Whenever a partitioned dataset is pulled and vectorbt sees one or more partition groups that are named "group" or "group_{index}", they are ignored automatically since they were most likely generated by using a user-defined row partitioning with `partition_by`. Such groups are also called default groups.
    
    
    >>> vbt.ParquetData.list_partition_cols("BNB-USD")
    ['group']
    
    >>> vbt.ParquetData.is_default_partition_col("group")
    True
    
    >>> vbt.ParquetData.pull("BNB-USD").features
    ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    

We can disable this behavior by setting `keep_partition_cols` to False:
    
    
    >>> vbt.ParquetData.pull("BNB-USD", keep_partition_cols=True).features
    ['Open',
     'High',
     'Low',
     'Close',
     'Volume',
     'Dividends',
     'Stock Splits',
     'group']
    

### SQL¶

Each SQL table can be manually imported using [pandas.read_sql_table](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_table.html):
    
    
    >>> pd.read_sql_table(
    ...     "BTC-USD", 
    ...     POSTGRESQL_URL, 
    ...     schema="yf_data",
    ...     index_col="Date", 
    ...     parse_dates={"Date": dict(utc=True)}
    ... )
                                      Open         High          Low        Close  \
    Date                                                                            
    2020-01-01 00:00:00+00:00  7194.892090  7254.330566  7174.944336  7200.174316   
    2020-01-02 00:00:00+00:00  7202.551270  7212.155273  6935.270020  6985.470215   
    2020-01-03 00:00:00+00:00  6984.428711  7413.715332  6914.996094  7344.884277   
    2020-01-04 00:00:00+00:00  7345.375488  7427.385742  7309.514160  7410.656738   
    
                                    Volume  Dividends  Stock Splits  
    Date                                                             
    2020-01-01 00:00:00+00:00  18565664997        0.0           0.0  
    2020-01-02 00:00:00+00:00  20802083465        0.0           0.0  
    2020-01-03 00:00:00+00:00  28111481032        0.0           0.0  
    2020-01-04 00:00:00+00:00  18444271275        0.0           0.0 
    

We can also execute any query using [pandas.read_sql_query](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html):
    
    
    >>> pd.read_sql_query(
    ...     'SELECT * FROM yf_data."BTC-USD"', 
    ...     POSTGRESQL_URL, 
    ...     index_col="Date", 
    ...     parse_dates={"Date": dict(utc=True)}
    ... )
                                      Open         High          Low        Close  \
    Date                                                                            
    2020-01-01 00:00:00+00:00  7194.892090  7254.330566  7174.944336  7200.174316   
    2020-01-02 00:00:00+00:00  7202.551270  7212.155273  6935.270020  6985.470215   
    2020-01-03 00:00:00+00:00  6984.428711  7413.715332  6914.996094  7344.884277   
    2020-01-04 00:00:00+00:00  7345.375488  7427.385742  7309.514160  7410.656738   
    
                                    Volume  Dividends  Stock Splits  
    Date                                                             
    2020-01-01 00:00:00+00:00  18565664997        0.0           0.0  
    2020-01-02 00:00:00+00:00  20802083465        0.0           0.0  
    2020-01-03 00:00:00+00:00  28111481032        0.0           0.0  
    2020-01-04 00:00:00+00:00  18444271275        0.0           0.0 
    

But first, how do we know what kind of schemas and tables are stored in our database? We can call [SQLData.list_schemas](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.list_schemas) and [SQLData.list_tables](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.list_tables) respectively. Most methods of [SQLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData), including these two, require the engine to be provided.
    
    
    >>> vbt.SQLData.list_schemas(engine=POSTGRESQL_URL)
    ['information_schema', 'public', 'yf_data']
    
    >>> vbt.SQLData.list_tables(engine=POSTGRESQL_URL)
    ['information_schema:_pg_foreign_data_wrappers',
     'information_schema:_pg_foreign_servers',
     ...
     'yf_data:BTC-USD',
     'yf_data:ETH-USD']
    
    >>> vbt.SQLData.list_tables(engine=POSTGRESQL_URL, schema="yf_data")
    ['BTC-USD', 'ETH-USD']
    

To fetch the actual data, we have [SQLData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.fetch_key) at our disposal, which calls `pd.read_sql_query` and does many pre-processings and post-processings under the hood. For instance, it can "inspect" the database and map columns indices to names, which aren't natively supported by the Pandas method. This is useful when specifying any information per column while relying solely on column positions, such as when providing `index_col` (which, by the way, defaults to 0 - the first column). It also does some heavy lifting on datetime index and columns, and can automatically retrieve all tables stored under a schema or even entire database.

Let's pull all the tables we stored previously, implicitly and explicitly:
    
    
    >>> vbt.SQLData.pull(engine=SQLITE_URL).symbols   # (1)!
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.SQLData.pull(["BTC-USD", "ETH-USD"], engine=SQLITE_URL).symbols  # (2)!
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.SQLData.pull(engine=POSTGRESQL_URL, schema="yf_data").symbols  # (3)!
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.SQLData.pull(["yf_data:BTC-USD", "yf_data:ETH-USD"], engine=POSTGRESQL_URL).symbols  # (4)!
    ['yf_data:BTC-USD', 'yf_data:ETH-USD']
    

  1. Pull all tables from the database
  2. Pull specific tables from the database
  3. Pull all tables under a schema from the database
  4. Pull tables from the database by also specifying the schema for each



We can also specialize any information per feature/symbol by providing it as an instance of [key_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.key_dict):
    
    
    >>> vbt.SQLData.pull(
    ...     ["BTCUSD", "ETHUSD"], 
    ...     schema="yf_data",
    ...     table=vbt.key_dict({
    ...         "BTCUSD": "BTC-USD",
    ...         "ETHUSD": "ETH-USD",
    ...     }),
    ...     engine=POSTGRESQL_URL
    ... ).symbols
    ['BTCUSD', 'ETHUSD']
    

This is especially useful to execute custom queries:
    
    
    >>> vbt.SQLData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     query=vbt.key_dict({
    ...         "BTC-USD": 'SELECT * FROM yf_data."BTC-USD"',
    ...         "ETH-USD": 'SELECT * FROM yf_data."ETH-USD"',
    ...     }), 
    ...     index_col="Date",
    ...     engine=POSTGRESQL_URL
    ... ).symbols
    ['BTC-USD', 'ETH-USD']
    

Note

When executing a custom query, most of the preprocessings won't be available because the query isn't easily introspectable. For example, we have to provide a column name under `index_col` (or False to not use any column as an index).

Since different engines have different configurations and we don't want to repeatedly pass them during pulling, we can save the respective configuration to the global settings. For this, we need to create an engine name first and then save all the keyword arguments that we normally pass to [SQLData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.fetch_key) under this engine name in `vbt.settings.data.engines`. This can be easily accomplished with [SQLData.set_engine_settings](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.set_engine_settings), which takes an engine name and keyword arguments that should be saved. If the engine name is new, make sure to set `populate_` to True.
    
    
    >>> vbt.SQLData.set_engine_settings(
    ...     engine_name="sqlite",
    ...     populate_=True,
    ...     engine=SQLITE_URL
    ... )
    
    >>> vbt.SQLData.set_engine_settings(
    ...     engine_name="postgresql",
    ...     populate_=True,
    ...     engine=POSTGRESQL_URL,
    ...     schema="yf_data"
    ... )
    

If any argument during fetching is None, it will be looked under these settings first. All we have to do is to provide an engine name as `engine` or `engine_name`:
    
    
    >>> vbt.SQLData.pull(engine_name="sqlite").symbols
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.SQLData.pull(engine_name="postgresql").symbols
    ['BTC-USD', 'ETH-USD']
    

We can also save arguments that we want to use under each engine name. For example, let's define the default engine name:
    
    
    >>> vbt.SQLData.set_custom_settings(engine_name="postgresql")
    
    >>> vbt.SQLData.pull().symbols
    ['BTC-USD', 'ETH-USD']
    

To fetch some specific columns, we can use the `columns` argument:
    
    
    >>> vbt.SQLData.pull(columns=["High", "Low"]).features
    ['High', 'Low']
    

Hint

If you want to pull just one column and keep it as a DataFrame, set `squeeze` to False.

In contrast to the Pandas method, we can also filter by any start and end condition. When `align_dates` is True (default) and `start` and/or `end` is provided, [SQLData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData.fetch_key) will fetch just one row of data first. It will then check whether the index of this row is datetime-like, and if so, will treat the provided `start` and/or `end` argument as a datetime-like object; this means converting it to a `datetime` object and localizing/converting it into the timezone of the index.

Note

If you used [Data.to_sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_sql) to save the data, make sure to use the same `to_utc` option during pulling as during saving.
    
    
    >>> vbt.SQLData.pull(start="2020-01-03").close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

Most databases either don't support timezones, or data is stored in UTC, thus the default behavior is to localize any timezone-naive datetime to UTC; the user is then responsible to provide the correct timezone. If a timezone is provided via `tz` and the provided datetime has no timezone, it will be localized to `tz` and then converted to the timezone of the index. If `to_utc` is True, it will be converted to UTC. If the index has no timezone, the provided datetime will be either converted to `tz` or UTC (if `to_utc` is True) first and then the timezone will be removed.

Let's demonstrate using a custom timezone by saving and then pulling the price of AAPL:
    
    
    >>> aapl_data = vbt.YFData.fetch("AAPL", start="2022", end="2023")
    >>> aapl_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190979
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171844
                                        ...
    2022-12-28 00:00:00-05:00    125.504539
    2022-12-29 00:00:00-05:00    129.059372
    2022-12-30 00:00:00-05:00    129.378006
    Name: Close, Length: 251, dtype: float64
    
    >>> aapl_data.to_sql("sqlite")  # (1)!
    >>> aapl_data.to_sql("postgresql")  # (2)!
    
    >>> vbt.SQLData.pull(
    ...     "AAPL", 
    ...     engine_name="sqlite", 
    ...     start="2022-12-23",
    ...     end="2022-12-30",
    ...     tz="America/New_York"
    ... ).close
    Date
    2022-12-23 00:00:00-05:00    131.299820
    2022-12-27 00:00:00-05:00    129.477585
    2022-12-28 00:00:00-05:00    125.504539
    2022-12-29 00:00:00-05:00    129.059372
    Name: Close, dtype: float64
    
    >>> vbt.SQLData.pull(
    ...     "AAPL", 
    ...     engine_name="postgresql", 
    ...     start="2022-12-23",
    ...     end="2022-12-30",
    ...     tz="America/New_York"
    ... ).close
    Date
    2022-12-23 00:00:00-05:00    131.299820
    2022-12-27 00:00:00-05:00    129.477585
    2022-12-28 00:00:00-05:00    125.504539
    2022-12-29 00:00:00-05:00    129.059372
    Name: Close, dtype: float64
    

  1. The first argument can also be an engine name from the global settings
  2. Schema defined in the global settings will be used by default



All datetime pre-processings can be disabled by turning off `align_dates`: 
    
    
    >>> vbt.SQLData.pull(
    ...     "AAPL", 
    ...     start="2022-12-23",
    ...     end="2022-12-30",
    ...     tz="America/New_York",
    ...     align_dates=False
    ... ).close
    Date
    2022-12-23 00:00:00-05:00    131.299820
    2022-12-27 00:00:00-05:00    129.477585
    2022-12-28 00:00:00-05:00    125.504539
    2022-12-29 00:00:00-05:00    129.059372
    Name: Close, dtype: float64
    

When a custom query should be executed, the filtering must be done within the query:
    
    
    >>> vbt.SQLData.pull(
    ...     "AAPL", 
    ...     query="""
    ...         SELECT *
    ...         FROM yf_data."AAPL" 
    ...         WHERE yf_data."AAPL"."Date" >= :start AND yf_data."AAPL"."Date" < :end
    ...     """,
    ...     tz="America/New_York",
    ...     index_col="Date",
    ...     params={
    ...         "start": vbt.datetime("2022-12-23", tz="America/New_York"),
    ...         "end": vbt.datetime("2022-12-30", tz="America/New_York")
    ...     }
    ... ).close
    Date
    2022-12-23 00:00:00-05:00    131.299820
    2022-12-27 00:00:00-05:00    129.477585
    2022-12-28 00:00:00-05:00    125.504539
    2022-12-29 00:00:00-05:00    129.059372
    Name: Close, dtype: float64
    

To filter by row number, we have to put a column with row numbers first. This can be done automatically by using [Data.to_sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_sql) and setting `attach_row_number` to True.
    
    
    >>> aapl_data.to_sql("sqlite", attach_row_number=True, if_exists="replace")
    

Then, when pulling, we can directly use `start_row` and `end_row`:
    
    
    >>> vbt.SQLData.pull(
    ...     "AAPL", 
    ...     start_row=5,
    ...     end_row=10,
    ...     tz="America/New_York"
    ... ).close
    Date
    2022-01-10 00:00:00-05:00    170.469116
    2022-01-11 00:00:00-05:00    173.330231
    2022-01-12 00:00:00-05:00    173.775711
    2022-01-13 00:00:00-05:00    170.469116
    2022-01-14 00:00:00-05:00    171.340347
    Freq: D, Name: Close, dtype: float64
    

#### Chunking¶

Chunking for SQL databases is identical to that for CSV files:
    
    
    >>> vbt.SQLData.pull(
    ...     "AAPL",
    ...     chunksize=1,
    ...     chunk_func=lambda iterator: pd.concat([
    ...         df 
    ...         for df in iterator
    ...         if df.index.is_month_start.all()
    ...     ], axis=0),
    ...     tz="America/New_York"
    ... ).close
    Date
    2022-02-01 00:00:00-05:00    172.864914
    2022-03-01 00:00:00-05:00    161.774826
    2022-04-01 00:00:00-04:00    172.787796
    2022-06-01 00:00:00-04:00    147.627930
    2022-07-01 00:00:00-04:00    137.919113
    2022-08-01 00:00:00-04:00    160.334793
    2022-09-01 00:00:00-04:00    157.028458
    2022-11-01 00:00:00-04:00    149.761551
    2022-12-01 00:00:00-05:00    147.679932
    Name: Close, dtype: float64
    

### DuckDB¶

Hint

Previous method (using SQLAlchemy) can be used to read from a DuckDB database as well. For this, you have to install the [duckdb-engine](https://pypi.org/project/duckdb-engine/) extension.

To fetch data using DuckDB, we can use the convenient class [DuckDBData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/duckdb/#vectorbtpro.data.custom.duckdb.DuckDBData). It contains methods for discovering catalogs, schemas, and tables, as well as methods for fetching the actual data, such as [DuckDBData.fetch_key](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/duckdb/#vectorbtpro.data.custom.duckdb.DuckDBData.fetch_key). Let's delete the previous DuckDB database, create a new database by setting its URL globally, put some data inside, and take a look at the stored objects:
    
    
    >>> vbt.remove_file(DUCKDB_URL)
    
    >>> vbt.DuckDBData.set_custom_settings(
    ...     connection=DUCKDB_URL
    ... )
    
    >>> yf_data.to_duckdb(schema="yf_data")
    
    >>> vbt.DuckDBData.list_catalogs()
    ['database']
    
    >>> vbt.DuckDBData.list_schemas()
    ['main', 'yf_data']
    
    >>> vbt.DuckDBData.list_tables()
    ['yf_data:BTC-USD', 'yf_data:ETH-USD']
    

To fetch the data, we can use [DuckDBData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/duckdb/#vectorbtpro.data.custom.duckdb.DuckDBData.pull). Whenever we provide one or more keys, they are automatically used as table names. Without any arguments, the method first determines the tables stored in the database and then pulls them.
    
    
    >>> vbt.DuckDBData.pull("yf_data:BTC-USD").symbols
    ['yf_data:BTC-USD']
    
    >>> vbt.DuckDBData.pull("BTC-USD", schema="yf_data").symbols
    ['BTC-USD']
    
    >>> vbt.DuckDBData.pull(["BTC-USD", "ETH-USD"], schema="yf_data").symbols
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.DuckDBData.pull().symbols
    ['yf_data:BTC-USD', 'yf_data:ETH-USD']
    

For cases where symbol names and table names should be kept separate, we can provide each table explicitly using a dictionary of type [key_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.key_dict):
    
    
    >>> vbt.DuckDBData.pull(
    ...     ["BTC", "ETH"], 
    ...     table=vbt.key_dict(BTC="BTC-USD", ETH="ETH-USD"),
    ...     schema="yf_data"
    ... ).symbols
    ['BTC', 'ETH']
    

The same approach can be used to execute custom queries:
    
    
    >>> vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     query=vbt.key_dict({
    ...         "BTC-USD": 'SELECT * FROM yf_data."BTC-USD"', 
    ...         "ETH-USD": 'SELECT * FROM yf_data."ETH-USD"'
    ...     })
    ... ).symbols
    ['BTC-USD', 'ETH-USD']
    

Apart from querying tables, we can also read CSV, Parquet, and JSON files. The reading behavior here is very similar to the writing behavior in [Data.to_duckdb](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_duckdb) in that there are three arguments: `read_format`, `read_path`, and `read_options`. The first argument controls the format of the file(s). The second argument controls the path of the file(s). The third argument controls the options for reading the file(s). When `read_format` is not provided, it gets parsed from the extension of the file. It's then used to call the `read_{format}` function from within the SQL query; for example, [`read_parquet`](https://duckdb.org/docs/data/parquet/overview) for Parquet.
    
    
    >>> vbt.DuckDBData.pull(read_path="data").symbols
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"],
    ...     read_path=vbt.key_dict({
    ...          "BTC-USD": "data/BTC-USD.parquet",
    ...          "ETH-USD": "data/ETH-USD.parquet"
    ...     })
    ... ).symbols
    ['BTC-USD', 'ETH-USD']
    
    >>> vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"],
    ...     query=vbt.key_dict({
    ...          "BTC-USD": "SELECT * FROM read_parquet('data/BTC-USD.parquet')",
    ...          "ETH-USD": "SELECT * FROM read_parquet('data/ETH-USD.parquet')"
    ...     })
    ... ).symbols
    ['BTC-USD', 'ETH-USD']
    

## Updating¶

### CSV & HDF¶

Tabular data such as CSV and HDF data can be read line by line, which makes possible listening for data updates. The classes [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) and [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) can be updated like every preset data class by keeping track of the last row index in [Data.returned_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.returned_kwargs). Whenever an update is triggered, this index is being used as the start row from which the dataset should be read. After the update, the end row is being used as the new last row index.

Let's separately download the data for `BTC-USD` and `ETH-USD`, save them to one HDF file, and read the entire file using [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData):
    
    
    >>> yf_data_btc = vbt.YFData.pull(
    ...     "BTC-USD", 
    ...     start="2020-01-01", 
    ...     end="2020-01-03"
    ... )
    >>> yf_data_eth = vbt.YFData.pull(
    ...     "ETH-USD", 
    ...     start="2020-01-03", 
    ...     end="2020-01-05"
    ... )
    
    >>> yf_data_btc.to_hdf("data.h5", key="yf_data_btc")
    >>> yf_data_eth.to_hdf("data.h5", key="yf_data_eth")
    
    >>> hdf_data = vbt.HDFData.pull(["BTC-USD", "ETH-USD"], paths="data.h5")
    

Symbol 2/2
    
    
    >>> hdf_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316         NaN
    2020-01-02 00:00:00+00:00  6985.470215         NaN
    2020-01-03 00:00:00+00:00          NaN  134.171707
    2020-01-04 00:00:00+00:00          NaN  135.069366
    

Let's look at the last row index in each dataset:
    
    
    >>> hdf_data.returned_kwargs
    key_dict({'BTC-USD': {'last_row': 1}, 'ETH-USD': {'last_row': 1}})
    

We see that the third row in each dataset is the new start row (1 row holding the header and 1 row holding the data). Let's append new data to the `BTC-USD` dataset and then update our [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) instance:
    
    
    >>> yf_data_btc = yf_data_btc.update(end="2020-01-06")
    >>> yf_data_btc.to_hdf("data.h5", key="yf_data_btc")
    
    >>> hdf_data = hdf_data.update()
    >>> hdf_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316         NaN
    2020-01-02 00:00:00+00:00  6985.470215         NaN
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    2020-01-05 00:00:00+00:00  7411.317383         NaN
    

The `BTC-USD` dataset has been updated with 3 new data points while the `ETH-USD` dataset hasn't been updated. This is reflected in the last row index:
    
    
    >>> hdf_data.returned_kwargs
    key_dict({
        'BTC-USD': {'last_row': 4, 'tz_convert': datetime.timezone.utc}, 
        'ETH-USD': {'last_row': 1, 'tz_convert': datetime.timezone.utc}
    })
    

This workflow can be repeated endlessly.

### Feather & Parquet¶

While Feather and Parquet classes don't have any `start` or `end` arguments to select a date range to pull, we can still load the entire data and append the difference to the currently stored data. This operation isn't too costly because reading such data format is very efficient. But starting from newer versions of Pandas, we can also filter partitions using the `filters` argument (only Parquet format supports this feature):
    
    
    >>> parquet_data = vbt.ParquetData.pull(
    ...     "BNB-USD", 
    ...     filters=[("group", "<", "2020-01-03")]
    ... )
    >>> parquet_data.close
    Date
    2020-01-01 00:00:00+00:00    13.689083
    2020-01-02 00:00:00+00:00    13.027011
    Name: Close, dtype: float64
    
    >>> parquet_data = parquet_data.update(
    ...     filters=[("group", ">=", "2020-01-03")]
    ... )
    >>> parquet_data.close
    Date
    2020-01-01 00:00:00+00:00    13.689083
    2020-01-02 00:00:00+00:00    13.027011
    2020-01-03 00:00:00+00:00    13.660452
    2020-01-04 00:00:00+00:00    13.891512
    Freq: D, Name: Close, dtype: float64
    

Also, in newer versions of PyArrow, we can use the same argument to select rows:
    
    
    >>> parquet_data = vbt.ParquetData.pull(
    ...     "BNB-USD", 
    ...     filters=[("Date", "<", vbt.timestamp("2020-01-03", tz="UTC"))]
    ... )
    >>> parquet_data.close
    Date
    2020-01-01 00:00:00+00:00    13.689083
    2020-01-02 00:00:00+00:00    13.027011
    Name: Close, dtype: float64
    
    >>> parquet_data = parquet_data.update(
    ...     filters=[("Date", ">=", vbt.timestamp("2020-01-03", tz="UTC"))]
    ... )
    >>> parquet_data.close
    Date
    2020-01-01 00:00:00+00:00    13.689083
    2020-01-02 00:00:00+00:00    13.027011
    2020-01-03 00:00:00+00:00    13.660452
    2020-01-04 00:00:00+00:00    13.891512
    Freq: D, Name: Close, dtype: float64
    

Important

There's an issue with PyArrow starting from the version 12.0.0 that makes it impossible to filter by timezone-aware timestamps - <https://github.com/apache/arrow/issues/37355>. This issue is said to be resolved by the version 14.0.0.

### SQL¶

The class [SQLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData) can be updated in two different ways: using the last row number and using the last index. The first approach works only if we have attached a column with row numbers, the name of this column is known and stored in [Data.returned_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.returned_kwargs) (which happens automatically), and index-based filtering (`start` and/or `end`) isn't used. If these conditions are true, this approach will be used by default; it will extract the last row number from the DataFrame and pass it as `start_row`.
    
    
    >>> aapl_data.to_sql("postgresql", attach_row_number=True, if_exists="replace")
    
    >>> sql_data = vbt.SQLData.pull(
    ...     "AAPL", 
    ...     end_row=5,
    ...     tz="America/New_York"
    ... )
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190964
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171814
    2022-01-06 00:00:00-05:00    170.281021
    2022-01-07 00:00:00-05:00    170.449341
    Freq: D, Name: Close, dtype: float64
    
    >>> sql_data = sql_data.update(end_row=10)
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190964
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171814
    2022-01-06 00:00:00-05:00    170.281021
    2022-01-07 00:00:00-05:00    170.449341
    2022-01-10 00:00:00-05:00    170.469131
    2022-01-11 00:00:00-05:00    173.330261
    2022-01-12 00:00:00-05:00    173.775726
    2022-01-13 00:00:00-05:00    170.469131
    2022-01-14 00:00:00-05:00    171.340317
    Freq: B, Name: Close, dtype: float64
    

The second approach is enabled if the first approach is disabled and row-based filtering (`start_row` and/or `end_row`) isn't used; it will extract the last index from [Data.last_index](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.last_index) and pass it as `start`, regardless of the index data type.
    
    
    >>> aapl_data.to_sql("postgresql", attach_row_number=False, if_exists="replace")
    
    >>> sql_data = vbt.SQLData.pull(
    ...     "AAPL", 
    ...     end="2022-01-08",
    ...     tz="America/New_York"
    ... )
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190964
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171814
    2022-01-06 00:00:00-05:00    170.281021
    2022-01-07 00:00:00-05:00    170.449341
    Freq: D, Name: Close, dtype: float64
    
    >>> sql_data = sql_data.update(end="2022-01-15")
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190964
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171814
    2022-01-06 00:00:00-05:00    170.281021
    2022-01-07 00:00:00-05:00    170.449341
    2022-01-10 00:00:00-05:00    170.469131
    2022-01-11 00:00:00-05:00    173.330261
    2022-01-12 00:00:00-05:00    173.775726
    2022-01-13 00:00:00-05:00    170.469131
    2022-01-14 00:00:00-05:00    171.340317
    Freq: B, Name: Close, dtype: float64
    

If the data was originally pulled using a custom query, both approaches will be disabled and we will have to implement either of the approaches manually.
    
    
    >>> sql_data = vbt.SQLData.pull(
    ...     "AAPL", 
    ...     query="""
    ...         SELECT *
    ...         FROM yf_data."AAPL" 
    ...         WHERE yf_data."AAPL"."Date" >= :start AND yf_data."AAPL"."Date" < :end
    ...     """,
    ...     tz="America/New_York",
    ...     index_col="Date",
    ...     params={
    ...         "start": vbt.datetime("2022-01-01", tz="America/New_York"),
    ...         "end": vbt.datetime("2022-01-08", tz="America/New_York")
    ...     }
    ... )
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190964
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171814
    2022-01-06 00:00:00-05:00    170.281021
    2022-01-07 00:00:00-05:00    170.449341
    Freq: D, Name: Close, dtype: float64
    
    >>> sql_data = sql_data.update(
    ...     params={
    ...         "start": vbt.datetime("2022-01-08", tz="America/New_York"),
    ...         "end": vbt.datetime("2022-01-18", tz="America/New_York")
    ...     }
    ... )
    >>> sql_data.close
    Date
    2022-01-03 00:00:00-05:00    180.190948
    2022-01-04 00:00:00-05:00    177.904068
    2022-01-05 00:00:00-05:00    173.171844
    2022-01-06 00:00:00-05:00    170.281006
    2022-01-07 00:00:00-05:00    170.449326
    2022-01-10 00:00:00-05:00    170.469116
    2022-01-11 00:00:00-05:00    173.330231
    2022-01-12 00:00:00-05:00    173.775742
    2022-01-13 00:00:00-05:00    170.469116
    2022-01-14 00:00:00-05:00    171.340332
    Freq: B, Name: Close, dtype: float64
    

### DuckDB¶

Hint

Previous method (using SQLAlchemy) can be used to update from a DuckDB database as well. For this, you have to install the [duckdb-engine](https://pypi.org/project/duckdb-engine/) extension.

To update an existing [DuckDBData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/duckdb/#vectorbtpro.data.custom.duckdb.DuckDBData) using new data, we can either use the arguments `start` and `end`, or construct a SQL query that returns the desired data range.
    
    
    >>> duckdb_data = vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     end="2020-01-03",
    ...     schema="yf_data"
    ... )
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    
    >>> duckdb_data = duckdb_data.update(end=None)
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

Or manually using a custom SQL query:
    
    
    >>> duckdb_data = vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     query=vbt.key_dict({
    ...         "BTC-USD": """
    ...             SELECT * FROM yf_data."BTC-USD" 
    ...             WHERE "Date" < TIMESTAMP '2020-01-03 00:00:00.000000'
    ...         """, 
    ...         "ETH-USD": """
    ...             SELECT * FROM yf_data."ETH-USD" 
    ...             WHERE "Date" < TIMESTAMP '2020-01-03 00:00:00.000000'
    ...         """
    ...     })
    ... )
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    
    >>> duckdb_data = duckdb_data.update(
    ...     query=vbt.key_dict({
    ...         "BTC-USD": """
    ...             SELECT * FROM yf_data."BTC-USD" 
    ...             WHERE "Date" >= TIMESTAMP '2020-01-03 00:00:00.000000'
    ...         """, 
    ...         "ETH-USD": """
    ...             SELECT * FROM yf_data."ETH-USD" 
    ...             WHERE "Date" >= TIMESTAMP '2020-01-03 00:00:00.000000'
    ...         """
    ...     })
    ... )
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

The same but using prepared statements:
    
    
    >>> duckdb_data = vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     query=vbt.key_dict({
    ...         "BTC-USD": """
    ...             SELECT * FROM yf_data."BTC-USD" 
    ...             WHERE "Date" >= $start AND "Date" < $end
    ...         """, 
    ...         "ETH-USD": """
    ...             SELECT * FROM yf_data."ETH-USD" 
    ...             WHERE "Date" >= $start AND "Date" < $end
    ...         """
    ...     }),
    ...     params=dict(
    ...         start=vbt.datetime("2020-01-01"),
    ...         end=vbt.datetime("2020-01-03")
    ...     )
    ... )
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    
    >>> duckdb_data = duckdb_data.update(
    ...     params=dict(
    ...         start=vbt.datetime("2020-01-03"),
    ...         end=vbt.datetime("2020-01-05")
    ...     )
    ... )
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

Similar to above but now filter based on the (dynamically generated) row number:
    
    
    >>> duckdb_data = vbt.DuckDBData.pull(
    ...     ["BTC-USD", "ETH-USD"], 
    ...     query=vbt.key_dict({
    ...         "BTC-USD": """
    ...             SELECT * EXCLUDE (Row) FROM (
    ...                 SELECT row_number() OVER () AS "Row", * FROM yf_data."BTC-USD"
    ...             )
    ...             WHERE Row >= $start_row AND Row < $end_row
    ...         """, 
    ...         "ETH-USD": """
    ...             SELECT * EXCLUDE (Row) FROM (
    ...                 SELECT row_number() OVER () AS "Row", * FROM yf_data."ETH-USD"
    ...             )
    ...             WHERE Row >= $start_row AND Row < $end_row
    ...         """
    ...     }),
    ...     params=dict(start_row=1, end_row=3)
    ... )
    >>> duckdb_data.close
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    
    >>> duckdb_data = duckdb_data.update(params=dict(start_row=3, end_row=5))
    symbol                         BTC-USD     ETH-USD
    Date                                              
    2020-01-01 00:00:00+00:00  7200.174316  130.802002
    2020-01-02 00:00:00+00:00  6985.470215  127.410179
    2020-01-03 00:00:00+00:00  7344.884277  134.171707
    2020-01-04 00:00:00+00:00  7410.656738  135.069366
    

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/documentation/data/local.py.txt)

Back to top  [ Previous  Data  ](../) [ Next  Remote  ](../remote/)

Copyright (C) 2021-2025 Oleg Polakow. All rights reserved. 

[ ](https://www.linkedin.com/in/polakowo "www.linkedin.com") [ ](https://github.com/polakowo "github.com")

#### Cookie consent

We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. With your consent, you're helping us to make our documentation better.

  * Google Analytics 
  * GitHub 



Accept Manage settings
