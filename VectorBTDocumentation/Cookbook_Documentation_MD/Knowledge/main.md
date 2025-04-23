# Knowledge [¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#knowledge "Permanent link")


# Assets[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#assets "Permanent link")

Knowledge assets are instances of [KnowledgeAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset) that hold a list of Python objects (most often dicts) and expose various methods to manipulate them. For usage examples, see the API documentation of the particular method.


# VBT assets[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#vbt-assets "Permanent link")

There are two knowledge assets in VBT: 1) website pages, and 2) Discord messages. The former asset consists of pages and headings that you can find on the (mainly private) website. Each data item represents a page or a heading of a page. Pages usually just point to one or more other pages and/or headings, while headings themselves hold text content - it all reflects the structure of Markdown files. The latter asset consists of the message history of the "vectorbt.pro" Discord server. Here, each data item represents a Discord message that may reference other Discord message(s) through replies. 

The assets are attached to each [release](https://github.com/polakowo/vectorbt.pro/releases) as `pages.json.zip` and `messages.json.zip` respectively, which is a ZIP-compressed JSON file. This file is managed by the class [PagesAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.PagesAsset) and [MessagesAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.MessagesAsset) respectively. It can be either loaded automatically or manually. When loading automatically, GitHub token must be provided.

Hint

The first pull will download the assets, while subsequent pulls will use the cached versions. Once VBT is upgraded, new assets will be downloaded automatically.

How to load an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-1)env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>" 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-2)pages_asset = vbt.PagesAsset.pull()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-3)messages_asset = vbt.MessagesAsset.pull()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-5)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-7)vbt.settings.set("knowledge.assets.vbt.token", "YOUR_GITHUB_TOKEN") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-8)pages_asset = vbt.PagesAsset.pull()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-9)messages_asset = vbt.MessagesAsset.pull()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-11)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-13)pages_asset = vbt.PagesAsset(/MessagesAsset).pull(release_name="v2024.8.20") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-14)pages_asset = vbt.PagesAsset(/MessagesAsset).pull(cache_dir="my_cache_dir") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-15)pages_asset = vbt.PagesAsset(/MessagesAsset).pull(clear_cache=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-16)pages_asset = vbt.PagesAsset(/MessagesAsset).pull(cache=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-18)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-20)pages_asset = vbt.PagesAsset.from_json_file("pages.json.zip") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-0-21)messages_asset = vbt.MessagesAsset.from_json_file("messages.json.zip")
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


# Generic assets[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#generic-assets "Permanent link")

Knowledge assets are not limited to VBT assets - you can construct an asset out of any list!

How to load an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-1-1)asset = vbt.KnowledgeAsset(my_list) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-1-2)asset = vbt.KnowledgeAsset.from_json_file("my_list.json") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-1-3)asset = vbt.KnowledgeAsset.from_json_bytes(vbt.load_bytes("my_list.json")) 
 
[/code]

 1. 2. 3. 


# Describing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#describing "Permanent link")

Knowledge assets behave like regular lists, thus, to describe an asset, you should describe it as a list. This gives us many analysis options like assessing the length, printing out a random data item, but also more sophisticated options like printing out the field schema - most data items of an asset are dicts, so you can describe them by their fields.

How to describe an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-1)print(len(asset)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-3)asset.sample().print() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-4)asset.print_sample()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-6)asset.print_schema() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-8)vbt.pprint(messages_asset.describe()) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-2-10)pages_asset.print_site_schema() 
 
[/code]

 1. 2. 3. 4. 5. 


# Manipulating[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#manipulating "Permanent link")

A knowledge asset is just a sophisticated list: it looks like a VBT object but behaves like a list. For manipulation, it offers a collection of methods that end with `item` or `items` to get, set, or remove data items, either by returning a new asset instance (default) or modifying the asset instance in place.

How to manipulate an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-1)d = asset.get_items(0) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-2)d = asset[0]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-3)data = asset[0:100] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-4)data = asset[mask] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-5)data = asset[indices] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-7)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-9)new_asset = asset.set_items(0, new_d) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-10)asset.set_items(0, new_d, inplace=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-11)asset[0] = new_d 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-12)asset[0:100] = new_data
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-13)asset[mask] = new_data
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-14)asset[indices] = new_data
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-16)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-18)new_asset = asset.delete_items(0) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-19)asset.delete_items(0, inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-20)asset.remove(0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-21)del asset[0]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-22)del asset[0:100]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-23)del asset[mask]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-24)del asset[indices]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-26)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-28)new_asset = asset.append_item(new_d) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-29)asset.append_item(new_d, inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-30)asset.append(new_d)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-31)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-32)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-33)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-34)new_asset = asset.extend_items([new_d1, new_d2]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-35)asset.extend_items([new_d1, new_d2], inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-36)asset.extend([new_d1, new_d2])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-37)asset += [new_d1, new_d2]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-38)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-39)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-40)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-41)print(d in asset) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-42)print(asset.index(d)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-43)print(asset.count(d)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-44)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-45)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-46)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-47)for d in asset: 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-3-48) ...
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 


# Querying[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#querying "Permanent link")

There is a zoo of methods to query an asset: [get](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.get) / [select](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.select), [query](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.query) / [filter](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.filter), and [find](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.find). The first pair is used to get and process one to multiple fields from each data item. The `get` method returns the raw output while the `select` method returns a new asset instance. The second pair is used to run queries against the asset using various engines such as JMESPath. And again, the `query` method returns the raw output while the `filter` method returns a new asset instance. Finally, the `find` method is specialized at finding information across one to multiple fields. By default, it returns a new asset instance.

How to query an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-1)messages = messages_asset.get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-2)total_reactions = sum(messages_asset.get("reactions")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-3)first_attachments = messages_asset.get("attachments[0]['content']", skip_missing=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-4)first_attachments = messages_asset.get("attachments.0.content", skip_missing=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-5)stripped_contents = pages_asset.get("content", source="x.strip() if x else ''") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-6)stripped_contents = pages_asset.get("content", source=lambda x: x.strip() if x else '') 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-7)stripped_contents = pages_asset.get(source="content.strip() if content else ''") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-11)all_contents = pages_asset.select("content").remove_empty().get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-12)all_attachments = messages_asset.select("attachments").merge().get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-13)combined_content = messages_asset.select(source=vbt.Sub('[$author] $content')).join() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-17)user_questions = messages_asset.query("content if '@polakowo' in mentions else vbt.NoResult") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-18)is_user_question = messages_asset.query("'@polakowo' in mentions", return_type="bool") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-19)all_attachments = messages_asset.query("[].attachments | []", query_engine="jmespath") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-20)all_classes = pages_asset.query("name[obj_type == 'class'].sort_values()", query_engine="pandas") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-21)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-22)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-24)support messages = messages_asset.filter("channel == 'support'") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-26)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-28)new_messages_asset = messages_asset.find("@polakowo") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-29)new_messages_asset = messages_asset.find("@polakowo", path="author") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-30)new_messages_asset = messages_asset.find(vbt.Not("@polakowo"), path="author") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-31)new_messages_asset = messages_asset.find( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-32) ["@polakowo", "from_signals"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-33) path=["author", "content"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-34) find_all=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-35))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-36)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-37)found_fields = messages_asset.find( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-38) ["vbt.Portfolio", "vbt.PF"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-39) return_type="field"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-40)).get()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-41)found_code_matches = messages_asset.find( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-42) r"(?<!`)`([^`]*)`(?!`)", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-43) mode="regex", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-44) return_type="match",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-4-45)).sort().get()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20. 21. 22. 23. 

Tip

To make chained calls more readable, use one of the following two styles:

How to find admonition types
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-1)admonition_types = (
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-2) pages_asset.find(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-3) r"!!!\s+(\w+)", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-4) mode="regex", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-5) return_type="match"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-6) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-7) .sort()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-8) .get()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-10)admonition_types = pages_asset.chain([
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-11) ("find", (r"!!!\s+(\w+)",), dict(mode="regex", return_type="match")),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-12) "sort",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-13) "get"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-5-14)])
 
[/code]


# Code[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#code "Permanent link")

There is a specialized method for finding code, either in single backticks or blocks.

How to find code
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-1)found_code_blocks = messages_asset.find_code().get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-2)found_code_blocks = messages_asset.find_code(language="python").get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-3)found_code_blocks = messages_asset.find_code(language=True).get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-4)found_code_blocks = messages_asset.find_code("from_signals").get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-5)found_code_blocks = messages_asset.find_code("from_signals", in_blocks=False).get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-6-6)found_code_blocks = messages_asset.find_code("from_signals", path="attachments").get() 
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Links[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#links "Permanent link")

Custom knowledge assets like pages and messages also have specialized methods for finding data items by their link. The default behavior is to match the target against the end of each link, such that searching for both "<https://vectorbt.pro/become-a-member/>" and "become-a-member/" will reliably return "<https://vectorbt.pro/become-a-member/>". Also, it automatically adds a variant with the slash or without if either "exact" or "end" mode is used, such that searching for "become-a-member" (without slash) will still return "<https://vectorbt.pro/become-a-member/>". This will also disregard another matched link "<https://vectorbt.pro/become-a-member/#become-a-member>" as it belongs to the same page.

How to find links
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-1)new_messages_asset = messages_asset.find_link( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-2) "https://discord.com/channels/918629562441695344/919715148896301067/923327319882485851"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-3))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-4)new_messages_asset = messages_asset.find_link("919715148896301067/923327319882485851") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-6)new_pages_asset = pages_asset.find_page( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-7) "https://vectorbt.pro/pvt_xxxxxxxx/getting-started/installation/"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-8))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-9)new_pages_asset = pages_asset.find_page("https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-10)new_pages_asset = pages_asset.find_page("installation/")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-11)new_pages_asset = pages_asset.find_page("installation") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-7-12)new_pages_asset = pages_asset.find_page("installation", aggregate=True) 
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Objects[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#objects "Permanent link")

You can also find headings that correspond to VBT objects.

How to find an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-8-1)new_pages_asset = pages_asset.find_obj(vbt.Portfolio) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-8-2)new_pages_asset = pages_asset.find_obj(vbt.Portfolio, aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-8-3)new_pages_asset = pages_asset.find_obj(vbt.PF.from_signals, aggregate=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-8-4)new_pages_asset = pages_asset.find_obj(vbt.pf_nb, aggregate=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-8-5)new_pages_asset = pages_asset.find_obj("SignalContext", aggregate=True)
 
[/code]

 1. 2. 


# Nodes[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#nodes "Permanent link")

You can also traverse pages and messages similarly to nodes in a graph.

How to traverse an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-1)new_vbt_asset = vbt_asset.select_previous(link) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-2)new_vbt_asset = vbt_asset.select_next(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-4)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-6)new_pages_asset = pages_asset.select_parent(link) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-7)new_pages_asset = pages_asset.select_children(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-8)new_pages_asset = pages_asset.select_siblings(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-9)new_pages_asset = pages_asset.select_descendants(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-10)new_pages_asset = pages_asset.select_branch(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-11)new_pages_asset = pages_asset.select_ancestors(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-12)new_pages_asset = pages_asset.select_parent_page(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-13)new_pages_asset = pages_asset.select_descendant_headings(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-17)new_messages_asset = messages_asset.select_reference(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-18)new_messages_asset = messages_asset.select_replies(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-19)new_messages_asset = messages_asset.select_block(link) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-20)new_messages_asset = messages_asset.select_thread(link)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-9-21)new_messages_asset = messages_asset.select_channel(link)
 
[/code]

 1. 2. 3. 

Note

Each operation requires at least one full data pass; use sparingly.


# Applying[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#applying "Permanent link")

"Find" and many other methods rely upon [KnowledgeAsset.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.apply), which executes a function on each data item. They are so-called asset functions, which consist of two parts: argument preparation and function calling. The main benefit is that arguments are prepared only once and then passed to each function call. The execution is done via the mighty [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) function, which is capable of parallelization.

How to apply a function to an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-1)links = messages_asset.apply("get", "link") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-3)from vectorbtpro.utils.knowledge.base_asset_funcs import GetAssetFunc 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-4)args, kwargs = GetAssetFunc.prepare("link")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-5)links = [GetAssetFunc.call(d, *args, **kwargs) for d in messages_asset]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-7)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-9)links_asset = messages_asset.apply(lambda d: d["link"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-10)links = messages_asset.apply(lambda d: d["link"], wrap=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-11)json_asset = messages_asset.apply(vbt.dump, dump_engine="json") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-15)new_asset = asset.apply( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-16) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-17) execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-18) n_chunks="auto", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-19) distribute="chunks", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-20) engine="processpool"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-21) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-10-22))
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Pipelines[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#pipelines "Permanent link")

Most examples show how to execute a chain of standalone operations, but each operation passes through data at least once. To pass through data exactly once regardless of the number of operations, use asset pipelines. There are two kinds of asset pipelines: basic and complex. Basic ones take a list of tasks (i.e., functions and their arguments) and compose them into a single operation that takes a single data item. This composed operation is then applied to all data items. Complex ones take a Python expression in a functional programming style where one function receives a data item and returns a result that becomes argument of another function.

How to apply a pipeline to an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-1)tasks = [("find", ("@polakowo",), dict(return_type="match")), len, "get"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-2)tasks = [vbt.Task("find", "@polakowo", return_type="match"), vbt.Task(len), vbt.Task("get")] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-3)mention_count = messages_asset.apply(tasks) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-5)asset_pipeline = vbt.BasicAssetPipeline(tasks) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-6)mention_count = [asset_pipeline(d) for d in messages_asset]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-8)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-10)expression = "get(len(find(d, '@polakowo', return_type='match')))"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-11)mention_count = messages_asset.apply(expression) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-13)asset_pipeline = vbt.ComplexAssetPipeline(expression) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-11-14)mention_count = [asset_pipeline(d) for d in messages_asset]
 
[/code]

 1. 2. 3. 4. 5. 6. 

Info

In both pipelines, arguments are prepared only once during initialization.


# Reducing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#reducing "Permanent link")

[Reducing](https://realpython.com/python-reduce-function/) means merging all data items into one. This requires a function that takes two data items. At first, these two data items are the initializer (such as empty dict) and the first data item. If the initializer is unknown, the first two data items are used. The result of this first iteration is then passed as the first data item to the next iteration. The execution is done by [KnowledgeAsset.reduce](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.reduce) and cannot be parallelized since each iteration depends on the previous one.

How to reduce an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-1)all_attachments = messages_asset.select("attachments").reduce("merge_lists") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-3)from vectorbtpro.utils.knowledge.base_asset_funcs import MergeListsAssetFunc 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-4)args, kwargs = MergeListsAssetFunc.prepare()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-5)d1 = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-6)for d2 in messages_asset.select("attachments"):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-7) d1 = MergeListsAssetFunc.call(d1, d2, *args, **kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-8)all_attachments = d1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-10)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-12-12)total_reactions = messages_asset.select("reactions").reduce(lambda d1, d2: d1 + d2) 
 
[/code]

 1. 2. 3. 


* * *

+


* * *

In addition, you can split a knowledge asset into groups and reduce the groups. The iteration over groups is done by the [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) function, which is capable of parallelization.

How to reduce groups of an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-1)reactions_by_channel = messages_asset.groupby_reduce( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-2) lambda d1, d2: d1 + d2["reactions"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-3) by="channel", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-4) initializer=0,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-5) return_group_keys=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-6))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-8)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-10)result = asset.groupby_reduce( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-11) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-12) execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-13) n_chunks="auto", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-14) distribute="chunks", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-15) engine="processpool"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-16) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-13-17))
 
[/code]

 1. 2. 


# Aggregating[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#aggregating "Permanent link")

Since headings are represented as individual data items, they can be aggregated back into their parent page. This is useful in order to [format](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#formatting) or [display](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#browsing) the page. Note that only headings can be aggregated - pages cannot be aggregated into other pages. 

How to aggregate pages
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-14-1)new_pages_asset = pages_asset.aggregate() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-14-2)new_pages_asset = pages_asset.aggregate(append_obj_type=False, append_github_link=False) 
 
[/code]

 1. 2. 


* * *

+


* * *

Messages, on the other hand, can be aggregated across multiple levels: _"message"_ , _"block"_ , _"thread"_ , and _"channel"_. Aggregation here simply means taking messages that belong to the specified level, and dumping and putting them into the content of a single, bigger message. 

 * The level _"message"_ means that attachments are included in the content of the message. 
 * The level _"block"_ puts together messages of the same author that reference the same block or don't reference anything at all. The link of the block is the link of the first message in the block. 
 * The level _"thread"_ puts together messages that belong to the same channel and are connected through a chain of replies. The link of the thread is the link of the first message in the thread. 
 * The level _"channel"_ puts together messages that belong to the same channel.

How to aggregate messages
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-1)new_messages_asset = messages_asset.aggregate() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-2)new_messages_asset = messages_asset.aggregate(by="message") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-3)new_messages_asset = messages_asset.aggregate(by="block") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-4)new_messages_asset = messages_asset.aggregate(by="thread") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-5)new_messages_asset = messages_asset.aggregate(by="channel") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-6)new_messages_asset = messages_asset.aggregate(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-7) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-8) minimize_metadata=True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-10)new_messages_asset = messages_asset.aggregate(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-11) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-12) dump_metadata_kwargs=dict(dump_engine="nestedtext") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-15-13))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


# Formatting[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#formatting "Permanent link")

Most Python objects can be dumped (i.e., serialized) into strings.

How to dump an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-1)new_asset = asset.dump() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-2)new_asset = asset.dump(dump_engine="nestedtext", indent=4) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-4)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-6)print(asset.dump().join()) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-7)print(asset.dump().join(separator="\n\n---------------------\n\n")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-16-8)print(asset.dump_all()) 
 
[/code]

 1. 2. 3. 4. 5. 


* * *

+


* * *

Custom knowledge assets like pages and messages can be converted and optionally saved in Markdown or HTML format. Only the field "content" will be converted while other fields will build the metadata block displayed at the beginning of each file.

Note

Without [aggregation](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#aggregating), each page heading will become a separate file.

How to format an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-1)new_pages_asset = pages_asset.to_markdown() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-2)new_pages_asset = pages_asset.to_markdown(root_metadata_key="pages") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-3)new_pages_asset = pages_asset.to_markdown(clear_metadata=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-4)new_pages_asset = pages_asset.to_markdown(remove_code_title=False, even_indentation=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-6)dir_path = pages_asset.save_to_markdown() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-7)dir_path = pages_asset.save_to_markdown(cache_dir="markdown") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-8)dir_path = pages_asset.save_to_markdown(clear_cache=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-9)dir_path = pages_asset.save_to_markdown(cache=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-15)new_pages_asset = pages_asset.to_html() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-16)new_pages_asset = pages_asset.to_html(to_markdown_kwargs=dict(root_metadata_key="pages")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-17)new_pages_asset = pages_asset.to_html(make_links=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-18)new_pages_asset = pages_asset.to_html(extensions=[], use_pygments=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-20)extensions = vbt.settings.get("knowledge.formatting.markdown_kwargs.extensions")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-21)new_pages_asset = pages_asset.to_html(extensions=extensions + ["pymdownx.smartsymbols"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-22)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-23)extensions = vbt.settings.get("knowledge.formatting.markdown_kwargs.extensions")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-24)extensions.append("pymdownx.smartsymbols") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-26)extension_configs = vbt.settings.get("knowledge.formatting.markdown_kwargs.extension_configs")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-27)extension_configs["pymdownx.superfences"]["preserve_tabs"] = False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-28)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-29)new_pages_asset = pages_asset.to_html(format_html_kwargs=dict(pygments_kwargs=dict(style="dracula"))) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-30)vbt.settings.set("knowledge.formatting.pygments_kwargs.style", "dracula") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-31)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-32)style_extras = vbt.settings.get("knowledge.formatting.style_extras")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-33)style_extras.append("""
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-34).admonition.success {
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-35) background-color: #00c8531a;
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-36) border-left-color: #00c853;
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-37)}
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-38)""") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-39)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-40)head_extras = vbt.settings.get("knowledge.formatting.head_extras")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-41)head_extras.append('<link ...>') 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-42)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-43)body_extras = vbt.settings.get("knowledge.formatting.body_extras")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-44)body_extras.append('<script>...</script>') 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-45)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-46)vbt.settings.get("knowledge.formatting").reset() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-47)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-48)dir_path = pages_asset.save_to_html() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-49)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-17-50)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20. 21. 22. 23. 24. 


# Browsing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#browsing "Permanent link")

Pages and messages can be displayed and browsed through via static HTML files. When a single item should be displayed, VBT creates a temporary HTML file and opens it in the default browser. All links in this file remain **external**. When multiple items should be displayed, VBT creates a single HTML file where items are displayed as iframes that can be iterated over using pagination.

How to display an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-1)file_path = pages_asset.display() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-2)file_path = pages_asset.display(link="documentation/fundamentals") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-3)file_path = pages_asset.display(link="documentation/fundamentals", aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-5)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-7)file_path = messages_asset.display() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-8)file_path = messages_asset.display(link="919715148896301067/923327319882485851") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-18-9)file_path = messages_asset.filter("channel == 'announcements'").display() 
 
[/code]

 1. 2. 3. 4. 5. 6. 


* * *

+


* * *

When one or more pages (and/or headings) should be browsed like a website, VBT can convert all data items to HTML and replace all external links to **internal** ones such that you can jump from one page to another locally. But which page is displayed first? Pages and headings build a directed graph. If there's one page from which all other pages are accessible, it's displayed first. If there are multiple pages, VBT creates an index page with metadata blocks from which you can access other pages (unless you specify `entry_link`).

How to browse an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-1)dir_path = pages_asset.browse() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-2)dir_path = pages_asset.browse(aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-3)dir_path = pages_asset.browse(entry_link="documentation/fundamentals", aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-4)dir_path = pages_asset.browse(entry_link="documentation", descendants_only=True, aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-5)dir_path = pages_asset.browse(cache_dir="website") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-6)dir_path = pages_asset.browse(clear_cache=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-7)dir_path = pages_asset.browse(cache=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-9)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-11)dir_path = messages_asset.browse() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-12)dir_path = messages_asset.browse(entry_link="919715148896301067/923327319882485851") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-19-14)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 


# Combining[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#combining "Permanent link")

Assets can be easily combined. When the target class is not specified, their common superclass is used. For example, combining [PagesAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.PagesAsset) and [MessagesAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.MessagesAsset) will yield an instance of [VBTAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.VBTAsset), which is based on overlapping features of both assets, such as "link" and "content" fields.

How to combine multiple assets
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-20-1)vbt_asset = pages_asset + messages_asset 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-20-2)vbt_asset = pages_asset.combine(messages_asset) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-20-3)vbt_asset = vbt.VBTAsset.combine(pages_asset, messages_asset) 
 
[/code]

 1. 2. 3. 


* * *

+


* * *

If both assets have the same number of data items, you can also merge them on the data item level. This works even for complex containers like nested dictionaries and lists by flattening their nested structures into flat dicts, merging them, and then unflattening them back into the original container type.

How to merge multiple assets
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-21-1)new_asset = asset1.merge(asset2) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-21-2)new_asset = vbt.KnowledgeAsset.merge(asset1, asset2) 
 
[/code]

 1. 2. 


* * *

+


* * *

You can also merge data items of a single asset into a single data item.

How to merge one asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-22-1)new_asset = asset.merge() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-22-2)new_asset = asset.merge_dicts() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-22-3)new_asset = asset.merge_lists() 
 
[/code]

 1. 2. 3. 


# Searching[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#searching "Permanent link")


# For objects[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#for-objects "Permanent link")

There are 4 methods to search for an arbitrary VBT object in pages and messages. The first method searches for the API documentation of the object, the second method searches for object mentions in the non-API (human-readable) documentation, the third method searches for object mentions in Discord messages, and the last method searches for object mentions in the code of both pages and messages.

How to find API-related knowledge about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-1)api_asset = vbt.find_api(vbt.PFO) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-2)api_asset = vbt.find_api(vbt.PFO, incl_bases=False, incl_ancestors=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-3)api_asset = vbt.find_api(vbt.PFO, use_parent=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-4)api_asset = vbt.find_api(vbt.PFO, use_refs=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-5)api_asset = vbt.find_api(vbt.PFO.row_stack) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-6)api_asset = vbt.find_api(vbt.PFO.from_uniform, incl_refs=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-7)api_asset = vbt.find_api([vbt.PFO.from_allocate_func, vbt.PFO.from_optimize_func]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-9)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-11)api_asset = vbt.PFO.find_api() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-23-12)api_asset = vbt.PFO.find_api(attr="from_optimize_func")
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 

How to find documentation-related knowledge about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-1)docs_asset = vbt.find_docs(vbt.PFO) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-2)docs_asset = vbt.find_docs(vbt.PFO, incl_shortcuts=False, incl_instances=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-3)docs_asset = vbt.find_docs(vbt.PFO, incl_custom=["pf_opt"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-4)docs_asset = vbt.find_docs(vbt.PFO, incl_custom=[r"pf_opt\s*=\s*.+"], is_custom_regex=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-5)docs_asset = vbt.find_docs(vbt.PFO, as_code=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-6)docs_asset = vbt.find_docs([vbt.PFO.from_allocate_func, vbt.PFO.from_optimize_func]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-8)docs_asset = vbt.find_docs(vbt.PFO, up_aggregate_th=0) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-9)docs_asset = vbt.find_docs(vbt.PFO, up_aggregate_pages=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-10)docs_asset = vbt.find_docs(vbt.PFO, incl_pages=["documentation", "tutorials"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-11)docs_asset = vbt.find_docs(vbt.PFO, incl_pages=[r"(features|cookbook)"], page_find_mode="regex") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-12)docs_asset = vbt.find_docs(vbt.PFO, excl_pages=["release-notes"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-14)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-16)docs_asset = vbt.PFO.find_docs() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-24-17)docs_asset = vbt.PFO.find_docs(attr="from_optimize_func")
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 

How to find Discord-related knowledge about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-1)messages_asset = vbt.find_messages(vbt.PFO) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-5)messages_asset = vbt.PFO.find_messages() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-25-6)messages_asset = vbt.PFO.find_messages(attr="from_optimize_func")
 
[/code]

 1. 2. 

How to find code examples of an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-1)examples_asset = vbt.find_examples(vbt.PFO) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-5)examples_asset = vbt.PFO.find_examples() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-26-6)examples_asset = vbt.PFO.find_examples(attr="from_optimize_func")
 
[/code]

 1. 2. 


* * *

+


* * *

The first three methods are guaranteed to be non-overlapping, while the last method can return examples that can be returned by the first three methods as well. Thus, there is another method that calls the first three methods by default and combines them into a single asset. This way, we can gather all relevant knowledge about a VBT object.

How to combine knowledge about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-1)combined_asset = vbt.find_assets(vbt.Trades) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-2)combined_asset = vbt.find_assets(vbt.Trades, asset_names=["api", "docs"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-3)combined_asset = vbt.find_assets(vbt.Trades, asset_names=["messages", ...]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-4)combined_asset = vbt.find_assets(vbt.Trades, asset_names="all") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-5)combined_asset = vbt.find_assets( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-6) vbt.Trades, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-7) api_kwargs=dict(incl_ancestors=False),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-8) docs_kwargs=dict(as_code=True),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-9) messages_kwargs=dict(as_code=True),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-10))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-11)combined_asset = vbt.find_assets(vbt.Trades, minimize=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-12)asset_list = vbt.find_assets(vbt.Trades, combine=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-13)combined_asset = vbt.find_assets([vbt.EntryTrades, vbt.ExitTrades]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-17)combined_asset = vbt.find_assets("SQL", resolve=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-18)combined_asset = vbt.find_assets(["SQL", "database"], resolve=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-20)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-21)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-22)messages_asset = vbt.Trades.find_assets() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-23)messages_asset = vbt.Trades.find_assets(attr="plot")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-27-24)messages_asset = pf.trades.find_assets(attr="expectancy")
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 

How to browse combined knowledge about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-1)vbt.Trades.find_assets().select("link").print() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-3)file_path = vbt.Trades.find_assets( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-4) asset_names="docs", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-5) docs_kwargs=dict(excl_pages="release-notes")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-6)).display()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-8)dir_path = vbt.Trades.find_assets( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-9) asset_names="docs", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-10) docs_kwargs=dict(excl_pages="release-notes")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-28-11)).browse(cache=False)
 
[/code]

 1. 2. 3. 


# Globally[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#globally "Permanent link")

Not only we can search for knowledge related to an individual VBT object, but we can also search for any VBT items that match a query in natural language. This works by embedding the query and the data items, computing their pairwise similarity scores, and sorting the data items by their mean score in descending order. Since the result contains all the data items from the original set just in a different order, it's advised to select top-k results before displaying.

All the methods discussed in [objects](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#for-objects) work on queries too!

How to search for knowledge using natural language
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-29-1)api_asset = vbt.find_api("How to rebalance weekly?", top_k=20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-29-2)docs_asset = vbt.find_docs("How to hedge a position?", top_k=20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-29-3)messages_asset = vbt.find_messages("How to trade live?", top_k=20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-29-4)combined_asset = vbt.find_assets("How to create a custom data class?", top_k=20)
 
[/code]


* * *

+


* * *

There also exists a specialized [search](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.search) function that calls [find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_assets), caches the documents (such that the next search call becomes a magnitude faster), and displays the top results as a static HTML page.

Info

The first time you run this command, it may take up to 15 minutes to prepare and embed documents. However, most of the preparation steps are cached and stored, so future searches will be significantly faster without needing to repeat the process.

How to search for knowledge on VBT using natural language and display top results
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-30-1)file_path = vbt.search("How to turn df into data?") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-30-2)found_asset = vbt.search("How to turn df into data?", display=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-30-3)file_path = vbt.search("How to turn df into data?", display_kwargs=dict(open_browser=False)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-30-4)file_path = vbt.search("How to fix 'Symbols have mismatching columns'?", asset_names="messages") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-30-5)file_path = vbt.search("How to use templates in signal_func_nb?", asset_names="examples", display=100) 
 
[/code]

 1. 2. 3. 4. 5. 


# Chatting[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#chatting "Permanent link")

Knowledge assets can be used as a context in chatting with LLMs. The method responsible for chatting is [Contextable.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Contextable.chat), which [dumps](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#formatting) the asset instance, packs it together with your question and chat history into messages, sends them to the LLM service, and displays and persists the response. The response can be displayed in a variety of formats, including raw text, Markdown, and HTML. All three formats support streaming. This method also supports multiple LLM APIs, including OpenAI, LiteLLM, and LLamaIndex.

How to chat about an asset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-1)env["OPENAI_API_KEY"] = "<OPENAI_API_KEY>" 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-5)patterns_tutorial = pages_asset.find_page( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-6) "https://vectorbt.pro/pvt_xxxxxxxx/tutorials/patterns-and-projections/patterns/", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-7) aggregate=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-8))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-9)patterns_tutorial.chat("How to detect a pattern?")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-11)data_documentation = pages_asset.select_branch("documentation/data").aggregate() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-12)data_documentation.chat("How to convert DataFrame into vbt.Data?")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-14)pfo_api = pages_asset.find_obj(vbt.PFO, aggregate=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-15)pfo_api.chat("How to rebalance weekly?")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-17)combined_asset = pages_asset + messages_asset
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-18)signal_func_nb_code = combined_asset.find_code("signal_func_nb") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-19)signal_func_nb_code.chat("How to pass an array to signal_func_nb?")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-21)polakowo_messages = messages_asset.filter("author == '@polakowo'").minimize().shuffle()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-22)polakowo_messages.chat("Describe the author of these messages", max_tokens=10_000) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-24)mention_fields = combined_asset.find(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-25) "parameterize", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-26) mode="substring", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-27) return_type="field", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-28) merge_fields=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-29))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-30)mention_counts = combined_asset.find(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-31) "parameterize", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-32) mode="substring", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-33) return_type="match", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-34) merge_matches=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-35)).apply(len)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-36)sorted_fields = mention_fields.sort(keys=mention_counts, reverse=True).merge()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-37)sorted_fields.chat("How to parameterize a function?") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-38)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-39)vbt.settings.set("knowledge.chat.max_tokens", None) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-40)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-41)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-42)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-43)chat_history = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-44)signal_func_nb_code.chat("How to check if we're in a long position?", chat_history) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-45)signal_func_nb_code.chat("How about short one?", chat_history) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-46)chat_history.clear() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-47)signal_func_nb_code.chat("How to access close price?", chat_history)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-48)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-49)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-50)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-51)asset.chat(..., completions="openai", model="o1-mini", system_as_user=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-52)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-53)# vbt.settings.set("knowledge.chat.completions_configs.openai.model", "o1-mini")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-54)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-55)# vbt.OpenAICompletions.set_settings({"model": "o1-mini"})
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-56)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-57)env["OPENAI_API_KEY"] = "<YOUR_OPENROUTER_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-58)asset.chat(..., completions="openai", base_url="https://openrouter.ai/api/v1", model="openai/gpt-4o") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-59)# vbt.settings.set("knowledge.chat.completions_configs.openai.base_url", "https://openrouter.ai/api/v1")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-60)# vbt.settings.set("knowledge.chat.completions_configs.openai.model", "openai/gpt-4o")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-61)# vbt.OpenAICompletions.set_settings({
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-62)# "base_url": "https://openrouter.ai/api/v1", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-63)# "model": "openai/gpt-4o"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-64)# })
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-65)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-66)env["DEEPSEEK_API_KEY"] = "<YOUR_DEEPSEEK_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-67)asset.chat(..., completions="litellm", model="deepseek/deepseek-coder")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-68)# vbt.settings.set("knowledge.chat.completions_configs.litellm.model", "deepseek/deepseek-coder")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-69)# vbt.LiteLLMCompletions.set_settings({"model": "deepseek/deepseek-coder"})
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-70)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-71)asset.chat(..., completions="llama_index", llm="perplexity", model="claude-3-5-sonnet-20240620") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-72)# vbt.settings.set("knowledge.chat.completions_configs.llama_index.llm", "anthropic")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-73)# anthropic_config = {"model": "claude-3-5-sonnet-20240620"}
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-74)# vbt.settings.set("knowledge.chat.completions_configs.llama_index.anthropic", anthropic_config)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-75)# vbt.LlamaIndexCompletions.set_settings({"llm": "anthropic", "anthropic": anthropic_config})
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-76)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-77)vbt.settings.set("knowledge.chat.completions", "litellm") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-78)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-79)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-80)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-81)asset.chat(..., stream=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-82)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-83)asset.chat(..., formatter="plain") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-84)asset.chat(..., formatter="ipython_markdown") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-85)asset.chat(..., formatter="ipython_html") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-86)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-87)file_path = asset.chat(..., formatter="html") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-88)file_path = asset.chat(..., formatter="html", formatter_kwargs=dict(cache_dir="chat")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-89)file_path = asset.chat(..., formatter="html", formatter_kwargs=dict(clear_cache=True)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-90)file_path = asset.chat(..., formatter="html", formatter_kwargs=dict(cache=False)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-91)file_path = asset.chat( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-92) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-93) formatter="html", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-94) formatter_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-95) to_markdown_kwargs=dict(...),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-96) to_html_kwargs=dict(...),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-97) format_html_kwargs=dict(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-98) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-99))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-100)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-101)asset.chat(..., formatter_kwargs=dict(update_interval=1.0)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-102)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-103)asset.chat(..., formatter_kwargs=dict(output_to="response.txt")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-104)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-105)asset.chat( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-106) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-107) system_prompt="You are a helpful assistant",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-108) context_prompt="Here's what you need to know: $context"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-31-109))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20. 21. 22. 23. 24. 25. 26. 27. 28. 


# About objects[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#about-objects "Permanent link")

We can chat about a VBT object using [chat_about](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.chat_about). Under the hood, it calls the method above, but on code examples only. When passing arguments, they are automatically distributed between [find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_assets) and [KnowledgeAsset.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset.chat) (see [chatting](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#chatting) for recipes)

How to chat about an object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-1)vbt.chat_about(vbt.Portfolio, "How to get trading expectancy?") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-2)vbt.chat_about( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-3) vbt.Portfolio, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-4) "How to get returns accessor with log returns?", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-5) asset_names="api",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-6) api_kwargs=dict(incl_bases=False, incl_ancestors=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-7))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-8)vbt.chat_about( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-9) vbt.Portfolio, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-10) "How to backtest a basic strategy?", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-11) model="o1-mini",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-12) system_as_user=True,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-13) max_tokens=100_000,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-14) shuffle=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-15))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-17)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-19)vbt.Portfolio.chat("How to create portfolio from order records?") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-32-20)vbt.Portfolio.chat("How to get grouped stats?", attr="stats")
 
[/code]

 1. 2. 3. 4. 

You can also ask a question about objects that technically do not exist in VBT, or keywords in general, such as "quantstats", which will search for mentions of "quantstats" in pages and messages.

How to chat about keywords
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-1)vbt.chat_about(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-2) "sql", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-3) "How to import data from a SQL database?", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-4) resolve=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-5) find_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-6) ignore_case=True,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-7) allow_prefix=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-8) allow_suffix=True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-9) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-33-10))
 
[/code]

 1. 2. 3. 


# Globally[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#globally_1 "Permanent link")

Similarly to the global [search](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.search) function, there is also a global function for chatting - [chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.chat). It manipulates documents in the same way, but instead of displaying, it sends them to an LLM for completion.

Info

The first time you run this command, it may take up to 15 minutes to prepare and embed documents. However, most of the preparation steps are cached and stored, so future searches will be significantly faster without needing to repeat the process.

How to chat about VBT
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-1)vbt.chat("How to turn df into data?") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-2)file_path = vbt.chat("How to turn df into data?", formatter="html") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-3)vbt.chat("How to fix 'Symbols have mismatching columns'?", asset_names="messages") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-4)vbt.chat(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-5) "How to use templates in signal_func_nb?", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-6) asset_names="examples", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-7) top_k=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-8) cutoff=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-9) return_chunks=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-10)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-12)chat_history = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-13)vbt.chat("How to turn df into data?", chat_history) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-14)vbt.chat("What if I have symbols as columns?", chat_history) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-15)vbt.chat("How to replace index of data?", chat_history, incl_past_queries=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-17)_, chat = vbt.chat("How to turn df into data?", return_chat=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-34-18)chat.complete("What if I have symbols as columns?")
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 


# RAG[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#rag "Permanent link")

VBT deploys a collection of components for vanilla RAG. Most of them are orchestrated and deployed automatically whenever you globally [search](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#globally) for knowledge on VBT or [chat](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#globally_1) about VBT.


# Tokenizer[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#tokenizer "Permanent link")

The [Tokenizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Tokenizer) class and its subclasses offer an interface for converting text into tokens.

How to tokenize text
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-1)tokenizer = vbt.TikTokenizer() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-2)tokenizer = vbt.TikTokenizer(encoding="o200k_base")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-3)tokenizer = vbt.TikTokenizer(model="gpt-4o")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-5)vbt.TikTokenizer.set_settings(encoding="o200k_base") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-7)token_count = tokenizer.count_tokens(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-8)tokens = tokenizer.encode(text)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-9)text = tokenizer.decode(tokens)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-11)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-13)tokens = vbt.tokenize(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-14)text = vbt.detokenize(tokens)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-35-16)tokens = vbt.tokenize(text, tokenizer="tiktoken", model="gpt-4o") 
 
[/code]

 1. 2. 3. 4. 5. 


# Embeddings[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#embeddings "Permanent link")

The [Embeddings](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Embeddings) class and its subclasses offer an interface for generating vector representations of text.

How to embed text
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-1)embeddings = vbt.OpenAIEmbeddings() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-2)embeddings = vbt.OpenAIEmbeddings(batch_size=256) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-3)embeddings = vbt.OpenAIEmbeddings(model="text-embedding-3-large") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-4)embeddings = vbt.LiteLLMEmbeddings(model="openai/text-embedding-3-large") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-5)embeddings = vbt.LlamaIndexEmbeddings(embedding="openai", model="text-embedding-3-large") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-6)embeddings = vbt.LlamaIndexEmbeddings(embedding="huggingface", model_name="BAAI/bge-small-en-v1.5")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-8)vbt.OpenAIEmbeddings.set_settings(model="text-embedding-3-large") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-10)emb = embeddings.get_embedding(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-11)embs = embeddings.get_embeddings(texts)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-15)emb = vbt.embed(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-16)embs = vbt.embed(texts)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-36-18)emb = vbt.embed(text, embeddings="openai", model="text-embedding-3-large") 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 


# Completions[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#completions "Permanent link")

The [Completions](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Completions) class and its subclasses offer an interface for generating text completions based on user queries. For arguments such as `formatter`, see [chatting](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#chatting).

How to (auto-)complete a query
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-1)completions = vbt.OpenAICompletions() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-2)completions = vbt.OpenAICompletions(stream=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-3)completions = vbt.OpenAICompletions(max_tokens=100_000, tokenizer="tiktoken")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-4)completions = vbt.OpenAICompletions(model="o1-mini", system_as_user=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-5)completions = vbt.OpenAICompletions(formatter="html", formatter_kwargs=dict(cache=False))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-6)completions = vbt.LiteLLMCompletions(model="openai/o1-mini", system_as_user=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-7)completions = vbt.LlamaIndexCompletions(llm="openai", model="o1-mini", system_as_user=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-9)vbt.OpenAICompletions.set_settings(model="o1-mini", system_as_user=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-11)completions.get_completion(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-15)vbt.complete(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-37-17)vbt.complete(text, completions="openai", model="o1-mini", system_as_user=True) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


# Text splitter[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#text-splitter "Permanent link")

The [TextSplitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.TextSplitter) class and its subclasses offer an interface for splitting text.

How to split text
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-1)text_splitter = vbt.TokenSplitter() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-2)text_splitter = vbt.TokenSplitter(chunk_size=1000, chunk_overlap=200)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-3)text_splitter = vbt.SegmentSplitter() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-4)text_splitter = vbt.SegmentSplitter(separators=r"\s+") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-5)text_splitter = vbt.SegmentSplitter(separators=[r"(?<=[.!?])\s+", r"\s+", None]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-6)text_splitter = vbt.SegmentSplitter(tokenizer="tiktoken", tokenizer_kwargs=dict(model="gpt-4o"))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-7)text_splitter = vbt.LlamaIndexSplitter(node_parser="SentenceSplitter") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-9)vbt.TokenSplitter.set_settings(chunk_size=1000, chunk_overlap=200) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-11)text_chunks = text_splitter.split_text(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-15)text_chunks = vbt.split_text(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-38-17)text_chunks = vbt.split_text(text, text_splitter="llamaindex", node_parser="SentenceSplitter") 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 


# Object store[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#object-store "Permanent link")

The [ObjectStore](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.ObjectStore) class and its subclasses offer an interface for efficiently storing and retrieving arbitrary Python objects, such as text documents and embeddings. Such objects must subclass [StoreObject](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.StoreObject).

How to store objects
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-1)obj_store = vbt.DictStore() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-2)obj_store = vbt.MemoryStore(store_id="abc") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-3)obj_store = vbt.MemoryStore(purge_on_open=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-4)obj_store = vbt.FileStore(dir_path="./file_store") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-5)obj_store = vbt.FileStore(consolidate=True, use_patching=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-6)obj_store = vbt.LMDBStore(dir_path="./lmdb_store") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-7)obj_store = vbt.CachedStore(obj_store=vbt.FileStore()) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-8)obj_store = vbt.CachedStore(obj_store=vbt.FileStore(), mirror=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-10)vbt.FileStore.set_settings(consolidate=True, use_patching=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-12)obj = vbt.TextDocument(id_, text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-13)obj = vbt.TextDocument.from_data(text) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-14)obj = vbt.TextDocument.from_data( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-15) {"timestamp": timestamp, "content": text}, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-16) text_path="content",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-17) excl_embed_metadata=["timestamp"],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-18) dump_kwargs=dict(dump_engine="nestedtext")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-19))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-20)obj1 = vbt.StoreEmbedding(id1, child_ids=[id2, id3]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-21)obj2 = vbt.StoreEmbedding(id2, parent_id=id1, embedding=embedding2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-22)obj3 = vbt.StoreEmbedding(id3, parent_id=id1, embedding=embedding3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-24)with obj_store: 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-25) obj = obj_store[obj.id_]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-26) obj_store[obj.id_] = obj
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-27) del obj_store[obj.id_]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-28) print(len(obj_store))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-29) for id_, obj in obj_store.items():
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-39-30) ...
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 


# Document ranker[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#document-ranker "Permanent link")

The [DocumentRanker](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.DocumentRanker) class offers an interface for embedding, scoring, and ranking documents.

How to rank documents
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-1)doc_ranker = vbt.DocumentRanker() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-2)doc_ranker = vbt.DocumentRanker(dataset_id="abc") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-3)doc_ranker = vbt.DocumentRanker( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-4) embeddings="litellm", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-5) embeddings_kwargs=dict(model="openai/text-embedding-3-large")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-6))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-7)doc_ranker = vbt.DocumentRanker( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-8) doc_store="file",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-9) doc_store_kwargs=dict(dir_path="./doc_file_store"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-10) emb_store="file",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-11) emb_store_kwargs=dict(dir_path="./emb_file_store"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-12))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-13)doc_ranker = vbt.DocumentRanker(score_func="dot", score_agg_func="max") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-15)vbt.DocumentRanker.set_settings(doc_store="memory", emb_store="memory") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-17)documents = [vbt.TextDocument("text1"), vbt.TextDocument("text2")] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-19)doc_ranker.embed_documents(documents) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-20)emb_documents = doc_ranker.embed_documents(documents, return_documents=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-21)embs = doc_ranker.embed_documents(documents, return_embeddings=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-22)doc_ranker.embed_documents(documents, refresh=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-24)doc_scores = doc_ranker.score_documents("How to use VBT?", documents) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-25)chunk_scores = doc_ranker.score_documents("How to use VBT?", documents, return_chunks=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-26)scored_documents = doc_ranker.score_documents("How to use VBT?", documents, return_documents=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-28)documents = doc_ranker.rank_documents("How to use VBT?", documents) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-29)scored_documents = doc_ranker.rank_documents("How to use VBT?", documents, return_scores=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-30)documents = doc_ranker.rank_documents("How to use VBT?", documents, top_k=50) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-31)documents = doc_ranker.rank_documents("How to use VBT?", documents, top_k=0.1) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-32)documents = doc_ranker.rank_documents("How to use VBT?", documents, top_k="elbow") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-33)documents = doc_ranker.rank_documents("How to use VBT?", documents, cutoff=0.5, min_top_k=20) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-34)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-35)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-36)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-37)vbt.embed_documents(documents) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-38)vbt.embed_documents(documents, embeddings="openai", model="text-embedding-3-large")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-40-39)documents = vbt.rank_documents("How to use VBT?", documents)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 


# Pipeline[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#pipeline "Permanent link")

The components mentioned above can enhance RAG pipelines, extending their utility beyond the VBT scope.

How to create a basic RAG pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-1)data = [
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-2) "The Eiffel Tower is not located in London.",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-3) "The Great Wall of China is not visible from Jupiter.",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-4) "HTML is not a programming language."
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-5)]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-6)query = "Where the Eiffel Tower is not located?"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-8)documents = map(vbt.TextDocument.from_data, data)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-9)retrieved_documents = vbt.rank_documents(query, documents, top_k=1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-10)context = "\n\n".join(map(str, retrieved_documents))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/knowledge/#__codelineno-41-11)vbt.complete(query, context=context)
 
[/code]