# Productivity[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#productivity "Permanent link")


# ChatVBT [¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#chatvbt "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2025_3_1.svg)

 * Similar to SearchVBT, there's a feature called ChatVBT that takes search results and forwards them to an LLM for completion. This allows you to interact seamlessly with the entire VBT knowledge base, getting detailed and context-aware responses.

Info

The first time you run this command, it may take up to 15 minutes to prepare and embed documents. However, most of the preparation steps are cached and stored, so future searches will be significantly faster without needing to repeat the process.

ChatGPTHigh-reasoning ChatGPTDeepSeek R1 (OpenRouter)Claude 3.5 Sonnet (LiteLLM)DeepSeek R1 (LlamaIndex, locally)

Ask VBT a question using ChatGPT
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-0-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-0-2)>>> env["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-0-4)>>> vbt.chat("How to rebalance weekly?", formatter="html")
 
[/code]

Ask VBT a question using a high-reasoning ChatGPT
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-2)>>> env["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-4)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-5)... "knowledge.chat.completions_configs.openai.model", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-6)... "o3-mini" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-8)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-9)... "knowledge.chat.completions_configs.openai.reasoning_effort", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-10)... "high" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-12)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-13)... "knowledge.chat.completions_configs.openai.system_as_user", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-14)... True
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-1-17)>>> vbt.chat("How to rebalance weekly?", formatter="html")
 
[/code]

 1. Discover [more models](https://platform.openai.com/docs/models)
 2. Don't forget to update `openai` to the latest version

Ask VBT a question using DeepSeek R1
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-2)>>> env["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-3)>>> env["OPENROUTER_API_KEY"] = "<YOUR_OPENROUTER_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-5)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-6)... "knowledge.chat.completions_configs.openai.base_url", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-7)... "https://openrouter.ai/api/v1"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-9)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-10)... "knowledge.chat.completions_configs.openai.api_key", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-11)... env["OPENROUTER_API_KEY"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-13)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-14)... "knowledge.chat.completions_configs.openai.model", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-15)... "deepseek/deepseek-r1" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-2-18)>>> vbt.chat("How to rebalance weekly?", formatter="html")
 
[/code]

 1. Needed for embeddings
 2. Discover [more models](https://openrouter.ai/models)

Ask VBT a question using Claude 3.5 Sonnet
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-2)>>> env["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-3)>>> env["ANTHROPIC_API_KEY"] = "<YOUR_ANTHROPIC_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-5)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-6)... "knowledge.chat.completions", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-7)... "litellm"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-9)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-10)... "knowledge.chat.completions_configs.litellm.model", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-11)... "anthropic/claude-3-5-sonnet-20241022" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-3-14)>>> vbt.chat("How to rebalance weekly?", formatter="html")
 
[/code]

 1. Needed for embeddings
 2. Discover [more models](https://docs.litellm.ai/docs/providers)

Note

Make sure that you have the required hardware 

Requires the Hugging Face extension for LlamaIndex for [embeddings](https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/) and [LLMs](https://docs.llamaindex.ai/en/stable/examples/llm/huggingface/) to be installed.

Ask VBT a question using DeepSeek R1 (locally)
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-3)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-4)... "knowledge.chat.embeddings", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-5)... "llama_index"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-7)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-8)... "knowledge.chat.embeddings_configs.llama_index.embedding", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-9)... "huggingface"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-11)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-12)... "knowledge.chat.embeddings_configs.llama_index.model_name", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-13)... "BAAI/bge-small-en-v1.5" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-15)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-16)... "knowledge.chat.completions", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-17)... "llama_index"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-19)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-20)... "knowledge.chat.completions_configs.llama_index.llm", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-21)... "huggingface"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-23)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-24)... "knowledge.chat.completions_configs.llama_index.model_name", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-25)... "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" 

 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-27)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-28)... "knowledge.chat.completions_configs.llama_index.tokenizer_name", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-29)... "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-31)>>> vbt.settings.set(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-32)... "knowledge.chat.rank_kwargs.dataset_id", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-33)... "local"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-34)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-35)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-4-36)>>> vbt.chat("How to rebalance weekly?", formatter="html")
 
[/code]

 1. Discover [more embedding models](https://huggingface.co/spaces/mteb/leaderboard)
 2. Discover [more DeepSeek models](https://huggingface.co/deepseek-ai)

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/chatvbt.light.gif#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/chatvbt.dark.gif#only-dark)


# SearchVBT [¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#searchvbt "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2025_3_1.svg)

 * Want to find specific information using natural language on the website or Discord? VBT offers a powerful smart search feature called SearchVBT. Enter your query, and it will generate an HTML page with well-structured search results. Behind the scenes, SearchVBT leverages a [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) pipeline to embed, rank, and retrieve only the most relevant documents from VBT, ensuring precise and efficient search results.

Info

The first time you run this command, it may take up to 15 minutes to prepare and embed documents. However, most of the preparation steps are cached and stored, so future searches will be significantly faster without needing to repeat the process.

Search VBT knowledge for a warning
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-5-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-5-2)>>> env["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-5-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-5-4)>>> vbt.search("UserWarning: Symbols have mismatching index")
 
[/code]

Page 1Page 2Page 3

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt1.light.png#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt1.dark.png#only-dark)

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt2.light.png#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt2.dark.png#only-dark)

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt3.light.png#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/searchvbt3.dark.png#only-dark)


# Self-aware classes[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#self-aware-classes "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_12_15.svg)

 * Each VBT class provides methods to explore its features, including its API, associated documentation, Discord messages, and code examples. You can even interact with it directly via an LLM!

Ask portfolio optimizer a question
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-2)>>> env["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-4)>>> vbt.PortfolioOptimizer.find_assets().get("link")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-5)['https://vectorbt.pro/pvt_xxxxxxxx/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-6) 'https://vectorbt.pro/pvt_xxxxxxxx/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-7) 'https://vectorbt.pro/pvt_xxxxxxxx/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-9) 'https://vectorbt.pro/pvt_xxxxxxxx/features/optimization/#riskfolio-lib',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-10) 'https://vectorbt.pro/pvt_xxxxxxxx/features/optimization/#portfolio-optimization',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-11) 'https://vectorbt.pro/pvt_xxxxxxxx/features/optimization/#pyportfolioopt',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-12) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-13) 'https://discord.com/channels/x/918629995415502888/1064943203071045753',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-14) 'https://discord.com/channels/x/918629995415502888/1067718833646874634',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-15) 'https://discord.com/channels/x/918629995415502888/1067718855734075403',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-16) ...]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-6-18)>>> vbt.PortfolioOptimizer.chat("How to rebalance weekly?", formatter="html")
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/knowledge_assets.light.gif#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/knowledge_assets.dark.gif#only-dark)


# Knowledge assets[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#knowledge-assets "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_11_12.svg)

 * Each [release](https://github.com/polakowo/vectorbt.pro/releases) now includes valuable knowledge assets—JSON files containing the private website content and complete "vectorbt.pro" Discord history. These assets can be fed to LLMs and services like Cursor. Additionally, VBT provides a palette of classes for working with these assets, enabling functionalities such as converting to Markdown and HTML files, browsing the website offline, performing targeted searches, interacting with LLMs, and much more!

Gather all pages and messages that define signal_func_nb
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-1)>>> env["GITHUB_TOKEN"] = "<YOUR_GITHUB_TOKEN>"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-3)>>> pages_asset = vbt.PagesAsset.pull() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-4)>>> messages_asset = vbt.MessagesAsset.pull()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-5)>>> vbt_asset = pages_asset + messages_asset
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-6)>>> code = vbt_asset.find_code("def signal_func_nb", return_type="item")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-7-7)>>> code.print_sample() 
 
[/code]

 1. 2. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-1)link: https://discord.com/channels/x/918630948248125512/1251081573147742298
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-2)block: https://discord.com/channels/x/918630948248125512/1251081573147742298
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-3)thread: https://discord.com/channels/x/918630948248125512/1250844139952541837
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-4)reference: https://discord.com/channels/x/918630948248125512/1250844139952541837
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-5)replies:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-6)- https://discord.com/channels/x/918630948248125512/1251083513336299610
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-7)channel: support
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-8)timestamp: '2024-06-14 07:51:31'
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-9)author: '@polakowo'
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-10)content: Something like this
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-11)mentions:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-12)- '@fei'
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-13)attachments:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-14)- file_name: Screenshot_2024-06-13_at_20.29.45-B4517.png
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-15) content: |-
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-16) Here's the text extracted from the image:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-18) ```python
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-19) @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-20) def signal_func_nb(c, entries, exits, wait):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-21) is_entry = vbt.pf_nb.select_nb(c, entries)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-22) if is_entry:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-23) return True, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-24) is_exit = vbt.pf_nb.select_nb(c, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-25) if is_exit:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-26) if vbt.pf_nb.in_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-27) last_order = vbt.pf_nb.get_last_order_nb(c)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-28) if c.index[c.i] - c.index[last_order["idx"]] >= wait:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-29) return False, True, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-30) return False, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-31)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-32) pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-33) "BTC-USD",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-34) n=100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-35) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-36) signal_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-37) vbt.Rep("entries"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-38) vbt.Rep("exits"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-39) vbt.dt.to_ns(vbt.timedelta("1000 days"))
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-40) )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-41) )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-42) ```
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-8-43)reactions: 0
 
[/code]


# Iterated decorator[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#iterated-decorator "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_6_19.svg)

 * Considering parallelizing a for-loop? Think no more—VBT has a decorator just for that.

Emulate a parallelized nested loop to get Sharpe by year and month
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-1)>>> import calendar
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-3)>>> @vbt.iterated(over_arg="year", merge_func="column_stack", engine="pathos") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-4)... @vbt.iterated(over_arg="month", merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-5)... def get_year_month_sharpe(data, year, month): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-6)... mask = (data.index.year == year) & (data.index.month == month)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-7)... if not mask.any():
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-8)... return np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-9)... year_returns = data.loc[mask].returns
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-10)... return year_returns.vbt.returns.sharpe_ratio()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-11)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-12)>>> years = data.index.year.unique().sort_values().rename("year")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-13)>>> months = data.index.month.unique().sort_values().rename("month")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-14)>>> sharpe_matrix = get_year_month_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-15)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-16)... years,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-17)... {calendar.month_abbr[month]: month for month in months}, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-19)>>> sharpe_matrix.transpose().vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-20)... trace_kwargs=dict(colorscale="RdBu", zmid=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-21)... yaxis=dict(autorange="reversed")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-9-22)... ).show()
 
[/code]

 1. 2. 3. 4. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/iterated_decorator.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/iterated_decorator.dark.svg#only-dark)


# Tasks[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#tasks "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_6_19.svg)

 * Testing multiple parameter combinations typically involves using the `@vbt.parameterized` decorator. But what if we want to test entirely uncorrelated configurations or even different functions? The latest addition to VectorBT® PRO allows you to execute any sequence of unrelated tests in parallel by assigning each test to a task.

Simulate SL, TSL, and TP parameters in three separate processes and compare their expectancy
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-3)>>> task1 = vbt.Task( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-4)... vbt.PF.from_random_signals, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-5)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-6)... n=100, seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-7)... sl_stop=vbt.Param(np.arange(1, 51) / 100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-9)>>> task2 = vbt.Task(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-10)... vbt.PF.from_random_signals, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-11)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-12)... n=100, seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-13)... tsl_stop=vbt.Param(np.arange(1, 51) / 100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-15)>>> task3 = vbt.Task(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-16)... vbt.PF.from_random_signals, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-17)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-18)... n=100, seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-19)... tp_stop=vbt.Param(np.arange(1, 51) / 100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-21)>>> pf1, pf2, pf3 = vbt.execute([task1, task2, task3], engine="pathos") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-22)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-23)>>> fig = pf1.trades.expectancy.rename("SL").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-24)>>> pf2.trades.expectancy.rename("TSL").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-25)>>> pf3.trades.expectancy.rename("TP").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-10-26)>>> fig.show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/tasks.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/tasks.dark.svg#only-dark)


# Nested progress bars[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#nested-progress-bars "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_5_15.svg)

 * Progress bars are now aware of each other! When a new progress bar starts, it checks if another progress bar with the same identifier has completed its task. If it has, the new progress bar will close itself and delegate its progress to the other progress bar.

Display progress of three parameters using nested progress bars
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-1)>>> symbols = ["BTC-USD", "ETH-USD"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-2)>>> fast_windows = range(5, 105, 5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-3)>>> slow_windows = range(5, 105, 5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-4)>>> sharpe_ratios = dict()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-6)>>> with vbt.ProgressBar(total=len(symbols), bar_id="pbar1") as pbar1: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-7)... for symbol in symbols:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-8)... pbar1.set_description(dict(symbol=symbol), refresh=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-9)... data = vbt.YFData.pull(symbol)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-10)... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-11)... with vbt.ProgressBar(total=len(fast_windows), bar_id="pbar2") as pbar2: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-12)... for fast_window in fast_windows:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-13)... pbar2.set_description(dict(fast_window=fast_window), refresh=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-14)... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-15)... with vbt.ProgressBar(total=len(slow_windows), bar_id="pbar3") as pbar3: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-16)... for slow_window in slow_windows:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-17)... if fast_window < slow_window:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-18)... pbar3.set_description(dict(slow_window=slow_window), refresh=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-19)... fast_sma = data.run("talib_func:sma", fast_window)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-20)... slow_sma = data.run("talib_func:sma", slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-21)... entries = fast_sma.vbt.crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-22)... exits = fast_sma.vbt.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-23)... pf = vbt.PF.from_signals(data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-24)... sharpe_ratios[(symbol, fast_window, slow_window)] = pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-25)... pbar3.update()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-26)... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-27)... pbar2.update()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-28)... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-11-29)... pbar1.update()
 
[/code]

 1. 2. 3. 

Symbol 2/2

Fast window 20/20

Slow window 20/20
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-1)>>> sharpe_ratios = pd.Series(sharpe_ratios)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-2)>>> sharpe_ratios.index.names = ["symbol", "fast_window", "slow_window"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-3)>>> sharpe_ratios
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-4)symbol fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-5)BTC-USD 5 10 1.063616
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-6) 15 1.218345
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-7) 20 1.273154
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-8) 25 1.365664
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-9) 30 1.394469
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-10) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-11)ETH-USD 80 90 0.582995
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-12) 95 0.617568
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-13) 85 90 0.701215
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-14) 95 0.616037
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-15) 90 95 0.566650
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-12-16)Length: 342, dtype: float64
 
[/code]


# Annotations[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#annotations "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2023_12_23.svg)

 * Whenever you write a function, the meaning of each argument can be specified using an annotation next to the argument. VBT now offers a rich set of in-house annotations tailored to specific tasks. For example, whether an argument is a parameter can be specified directly in the function rather than in the [parameterized decorator](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameterized-decorator).

Test a cross-validation function with annotations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-1)>>> @vbt.cv_split(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-2)... splitter="from_rolling", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-3)... splitter_kwargs=dict(length=365, split=0.5, set_labels=["train", "test"]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-4)... parameterized_kwargs=dict(random_subset=100),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-6)... def sma_crossover_cv(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-7)... data: vbt.Takeable, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-8)... fast_period: vbt.Param(condition="x < slow_period"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-9)... slow_period: vbt.Param, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-10)... metric
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-11)... ) -> vbt.MergeFunc("concat"):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-12)... fast_sma = data.run("sma", fast_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-13)... slow_sma = data.run("sma", slow_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-14)... entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-15)... exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-16)... pf = vbt.PF.from_signals(data, entries, exits, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-17)... return pf.deep_getattr(metric)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-18)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-19)>>> sma_crossover_cv(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-20)... vbt.YFData.pull("BTC-USD", start="4 years ago"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-21)... np.arange(20, 50),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-22)... np.arange(20, 50),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-23)... "trades.expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-25)split set fast_period slow_period
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-26)0 train 22 33 26.351841
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-27) test 21 34 35.788733
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-28)1 train 21 46 24.114027
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-29) test 21 39 2.261432
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-30)2 train 30 44 29.635233
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-31) test 30 38 1.909916
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-32)3 train 20 49 -7.038924
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-33) test 20 44 -1.366734
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-34)4 train 28 44 2.144805
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-35) test 29 38 -4.945776
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-36)5 train 35 47 -8.877875
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-37) test 34 37 2.792217
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-38)6 train 29 41 8.816846
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-39) test 28 43 36.008302
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-13-40)dtype: float64
 
[/code]

 1. 2. 3. 


# DataFrame product[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#dataframe-product "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_13_0.svg)

 * Several parameterized indicators can produce DataFrames with different shapes and columns, which makes a Cartesian product of them tricky since they often share common column levels (such as "symbol") that shouldn't be combined with each other. There's now a method to cross-join multiple DataFrames block-wise.

Enter when SMA goes above WMA, exit when EMA goes below WMA
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-2)>>> sma = data.run("sma", timeperiod=[10, 20], unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-3)>>> ema = data.run("ema", timeperiod=[30, 40], unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-4)>>> wma = data.run("wma", timeperiod=[50, 60], unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-5)>>> sma, ema, wma = sma.vbt.x(ema, wma) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-6)>>> entries = sma.vbt.crossed_above(wma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-7)>>> exits = ema.vbt.crossed_below(wma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-9)>>> entries.columns
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-10)MultiIndex([(10, 30, 50, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-11) (10, 30, 50, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-12) (10, 30, 60, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-13) (10, 30, 60, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-14) (10, 40, 50, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-15) (10, 40, 50, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-16) (10, 40, 60, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-17) (10, 40, 60, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-18) (20, 30, 50, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-19) (20, 30, 50, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-20) (20, 30, 60, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-21) (20, 30, 60, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-22) (20, 40, 50, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-23) (20, 40, 50, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-24) (20, 40, 60, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-25) (20, 40, 60, 'ETH-USD')],
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-14-26) names=['sma_timeperiod', 'ema_timeperiod', 'wma_timeperiod', 'symbol'])
 
[/code]

 1. 


# Compression[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#compression "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_10_0.svg)

 * Serialized VBT objects may sometimes take a lot of disk space. With this update, there's now support for a variety of compression algorithms to make files as light as possible! ![🪶](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fab6.svg)

Save data without and with compression
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-1)>>> data = vbt.RandomOHLCData.pull("RAND", start="2022", end="2023", timeframe="1 minute")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-3)>>> file_path = data.save()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-4)>>> print(vbt.file_size(file_path))
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-5)21.0 MB
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-7)>>> file_path = data.save(compression="blosc")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-8)>>> print(vbt.file_size(file_path))
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-15-9)13.3 MB
 
[/code]


# Faster loading[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#faster-loading "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_10_0.svg)

 * If your pipeline doesn't need accessors, Plotly graphs, and most of other optional functionalities, you can disable the auto-import feature entirely to bring down the loading time of VBT to under a second ![⏳](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/23f3.svg)

Define importing settings in vbt.ini
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-16-1)[importing]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-16-2)auto_import = False
 
[/code]

Measure the loading time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-17-1)>>> start = utc_time()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-17-2)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-17-3)>>> end = utc_time()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-17-4)>>> end - start
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-17-5)0.580937910079956
 
[/code]


# Configuration files[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#configuration-files "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_9_0.svg)

 * VectorBT® PRO extends [configparser](https://docs.python.org/3/library/configparser.html) to define its own configuration format that lets the user save, introspect, modify, and load back any complex in-house object. The main advantages of this format are readability and round-tripping: any object can be encoded and then decoded back without information loss. The main features include nested structures, references, parsing of literals, as well as evaluation of arbitrary Python expressions. Additionally, you can now create a configuration file for VBT and put it into the working directory - it will be used to update the default settings whenever the package is imported!

Define global settings in vbt.ini
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-1)[plotting]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-2)default_theme = dark
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-4)[portfolio]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-5)init_cash = 5000
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-7)[data.custom.binance.client_config]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-8)api_key = YOUR_API_KEY
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-9)api_secret = YOUR_API_SECRET
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-11)[data.custom.ccxt.exchanges.binance.exchange_config]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-12)apiKey = &data.custom.binance.client_config.api_key
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-18-13)secret = &data.custom.binance.client_config.api_secret
 
[/code]

Verify that the settings have been loaded correctly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-19-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-19-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-19-3)>>> vbt.settings.portfolio["init_cash"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-19-4)5000
 
[/code]


# Serialization[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#serialization "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_9_0.svg)

 * Just like machine learning models, every native VBT object can be serialized and saved to a binary file - it's never been easier to share data and insights! Another benefit is that only the actual content of each object is serialized, and not its class definition, such that the loaded object uses only the most up-to-date class definition. There's also a special logic implemented that can help you "reconstruct" objects if VBT has introduced some breaking API changes ![🏗](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3d7.svg)

Backtest each month of data and save the results for later
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-1)>>> data = vbt.YFData.pull("BTC-USD", start="2022-01-01", end="2022-06-01")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-3)>>> def backtest_month(close):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-4)... return vbt.PF.from_random_signals(close, n=10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-6)>>> month_pfs = data.close.resample(vbt.offset("M")).apply(backtest_month)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-7)>>> month_pfs
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-8)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-9)2022-01-01 00:00:00+00:00 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-10)2022-02-01 00:00:00+00:00 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-11)2022-03-01 00:00:00+00:00 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-12)2022-04-01 00:00:00+00:00 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-13)2022-05-01 00:00:00+00:00 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-14)Freq: MS, Name: Close, dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-15)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-16)>>> vbt.save(month_pfs, "month_pfs") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-18)>>> month_pfs = vbt.load("month_pfs") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-19)>>> month_pfs.apply(lambda pf: pf.total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-20)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-21)2022-01-01 00:00:00+00:00 -0.048924
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-22)2022-02-01 00:00:00+00:00 0.168370
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-23)2022-03-01 00:00:00+00:00 0.016087
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-24)2022-04-01 00:00:00+00:00 -0.120525
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-25)2022-05-01 00:00:00+00:00 0.110751
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-20-26)Freq: MS, Name: Close, dtype: float64
 
[/code]

 1. 2. 


# Data parsing[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#data-parsing "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Tired of passing open, high, low, and close as separate time series? Portfolio class methods have been extended to take a data instance instead of close and extract the contained OHLC data automatically - a small but timesaving feature!

Run the example above using the new approach
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-21-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020-01", end="2020-03")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-21-2)>>> pf = vbt.PF.from_random_signals(data, n=10)
 
[/code]


# Index dictionaries[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#index-dictionaries "Permanent link")

Manually constructing arrays and setting their data with Pandas is often painful. Gladly, there is a new functionality that provides a much needed help! Any broadcastable argument can become an index dictionary, which contains instructions on where to set values in the array and does the filling job for you. It knows exactly which axis has to be modified and doesn't create a full array if not necessary - with much love to RAM ![❤](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2764.svg)

1) Accumulate daily and exit on Sunday vs 2) accumulate weekly and exit on month end
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-2)>>> tile = pd.Index(["daily", "weekly"], name="strategy") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-3)>>> pf = vbt.PF.from_orders(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-4)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-5)... size=vbt.index_dict({ 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-6)... vbt.idx(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-7)... vbt.pointidx(every="day"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-8)... vbt.colidx("daily", level="strategy")): 100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-9)... vbt.idx(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-10)... vbt.pointidx(every="sunday"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-11)... vbt.colidx("daily", level="strategy")): -np.inf, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-12)... vbt.idx(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-13)... vbt.pointidx(every="monday"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-14)... vbt.colidx("weekly", level="strategy")): 100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-15)... vbt.idx(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-16)... vbt.pointidx(every="monthend"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-17)... vbt.colidx("weekly", level="strategy")): -np.inf,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-18)... }),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-19)... size_type="value",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-20)... direction="longonly",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-21)... init_cash="auto",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-22)... broadcast_kwargs=dict(tile=tile)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-24)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-25)strategy symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-26)daily BTC-USD 0.702259
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-27) ETH-USD 0.782296
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-28)weekly BTC-USD 0.838895
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-29) ETH-USD 0.524215
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-22-30)Name: sharpe_ratio, dtype: float64
 
[/code]

 1. 2. 3. 4. 


# Slicing[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#slicing "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Similarly to selecting columns, each VBT object is now capable of slicing rows, using the exact same mechanism as in Pandas ![🔪](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f52a.svg) This makes it supereasy to analyze and plot any subset of simulated data, without the need of re-simulation!

Analyze multiple date ranges of the same portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-2)>>> pf = vbt.PF.from_holding(data, freq="d")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-4)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-5)1.116727709477293
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-7)>>> pf.loc[:"2020"].sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-8)1.2699801554196481
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-10)>>> pf.loc["2021": "2021"].sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-11)0.9825161170278687
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-13)>>> pf.loc["2022":].sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-23-14)-1.0423271337174647
 
[/code]

 1. 2. 3. 


# Column stacking[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#column-stacking "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Complex VBT objects of the same type can be easily stacked along columns. For instance, you can combine multiple totally-unrelated trading strategies into the same portfolio for analysis. Under the hood, the final object is still represented as a monolithic multi-dimensional structure that can be processed even faster than merged objects separately ![🫁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fac1.svg)

Analyze two trading strategies separately and then jointly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-1)>>> def strategy1(data):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-2)... fast_ma = vbt.MA.run(data.close, 50, short_name="fast_ma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-3)... slow_ma = vbt.MA.run(data.close, 200, short_name="slow_ma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-4)... entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-5)... exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-6)... return vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-7)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-8)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-9)... exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-10)... size=100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-11)... size_type="value",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-12)... init_cash="auto"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-15)>>> def strategy2(data):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-16)... bbands = vbt.BBANDS.run(data.close, window=14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-17)... entries = bbands.close_crossed_below(bbands.lower)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-18)... exits = bbands.close_crossed_above(bbands.upper)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-19)... return vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-20)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-21)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-22)... exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-23)... init_cash=200
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-25)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-26)>>> data1 = vbt.BinanceData.pull("BTCUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-27)>>> pf1 = strategy1(data1) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-28)>>> pf1.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-29)0.9100317671866922
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-30)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-31)>>> data2 = vbt.BinanceData.pull("ETHUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-32)>>> pf2 = strategy2(data2) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-33)>>> pf2.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-34)-0.11596286232734827
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-35)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-36)>>> pf_sep = vbt.PF.column_stack((pf1, pf2)) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-37)>>> pf_sep.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-38)0 0.910032
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-39)1 -0.115963
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-40)Name: sharpe_ratio, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-41)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-42)>>> pf_join = vbt.PF.column_stack((pf1, pf2), group_by=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-43)>>> pf_join.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-24-44)0.42820898354646514
 
[/code]

 1. 2. 3. 4. 


# Row stacking[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#row-stacking "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Complex VBT objects of the same type can be easily stacked along rows. For instance, you can append new data to an existing portfolio, or even concatenate in-sample portfolios with their out-of-sample counterparts ![🧬](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9ec.svg)

Analyze two date ranges separately and then jointly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-1)>>> def strategy(data, start=None, end=None):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-2)... fast_ma = vbt.MA.run(data.close, 50, short_name="fast_ma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-3)... slow_ma = vbt.MA.run(data.close, 200, short_name="slow_ma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-4)... entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-5)... exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-6)... return vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-7)... data.close[start:end], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-8)... entries[start:end], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-9)... exits[start:end], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-10)... size=100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-11)... size_type="value",
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-12)... init_cash="auto"
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-15)>>> data = vbt.BinanceData.pull("BTCUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-17)>>> pf_whole = strategy(data) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-18)>>> pf_whole.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-19)0.9100317671866922
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-20)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-21)>>> pf_sub1 = strategy(data, end="2019-12-31") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-22)>>> pf_sub1.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-23)0.7810397448678937
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-24)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-25)>>> pf_sub2 = strategy(data, start="2020-01-01") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-26)>>> pf_sub2.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-27)1.070339534746574
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-28)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-29)>>> pf_join = vbt.PF.row_stack((pf_sub1, pf_sub2)) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-30)>>> pf_join.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-25-31)0.9100317671866922
 
[/code]

 1. 2. 3. 4. 


# Index alignment[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#index-alignment "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * There is no more limitation of each Pandas array being required to have the same index. Indexes of all arrays that should broadcast against each other are automatically aligned, as long as they have the same data type.

Predict ETH price with BTC price using linear regression
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-1)>>> btc_data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-2)>>> btc_data.wrapper.shape
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-3)(2817, 7)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-5)>>> eth_data = vbt.YFData.pull("ETH-USD") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-6)>>> eth_data.wrapper.shape
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-7)(1668, 7)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-9)>>> ols = vbt.OLS.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-10)... btc_data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-11)... eth_data.close
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-13)>>> ols.pred
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-14)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-15)2014-09-17 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-16)2014-09-18 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-17)2014-09-19 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-18)2014-09-20 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-19)2014-09-21 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-20)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-21)2022-05-30 00:00:00+00:00 2109.769242
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-22)2022-05-31 00:00:00+00:00 2028.856767
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-23)2022-06-01 00:00:00+00:00 1911.555689
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-24)2022-06-02 00:00:00+00:00 1930.169725
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-25)2022-06-03 00:00:00+00:00 1882.573170
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-26-26)Freq: D, Name: Close, Length: 2817, dtype: float64
 
[/code]

 1. 2. 


# Numba datetime[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#numba-datetime "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_3.svg)

 * There is no support for datetime indexes (and any other Pandas objects) in Numba. There are also no built-in Numba functions for working with datetime. So, how to connect data to time? VBT closes this loophole by implementing a collection of functions to extract various information from each timestamp, such as the current time and day of the week to determine whether the bar happens during trading hours.

Tutorial

Learn more in the [Signal development](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development) tutorial.

Plot the percentage change from the start of the month to now
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-2)... def month_start_pct_change_nb(arr, index):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-3)... out = np.full(arr.shape, np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-4)... for col in range(arr.shape[1]):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-5)... for i in range(arr.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-6)... if i == 0 or vbt.dt_nb.month_nb(index[i - 1]) != vbt.dt_nb.month_nb(index[i]):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-7)... month_start_value = arr[i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-8)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-9)... out[i, col] = (arr[i, col] - month_start_value) / month_start_value
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-10)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-11)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-12)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], start="2022", end="2023")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-13)>>> pct_change = month_start_pct_change_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-14)... vbt.to_2d_array(data.close), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-15)... data.index.vbt.to_ns() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-17)>>> pct_change = data.symbol_wrapper.wrap(pct_change)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-27-18)>>> pct_change.vbt.plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/numba_datetime.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/numba_datetime.dark.svg#only-dark)


# Periods ago[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#periods-ago "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_3.svg)

 * Instead of writing Numba functions, comparing values at different bars can be also done in a vectorized manner with Pandas. The problem is that there are no-built in functions to easily shift values based on timedeltas, neither there are rolling functions to check whether an event happened during a period time in the past. This gap is closed by various new accessor methods.

Tutorial

Learn more in the [Signal development](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development) tutorial.

Check whether the price dropped for 5 consecutive bars
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-1)>>> data = vbt.YFData.pull("BTC-USD", start="2022-05", end="2022-08")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-2)>>> mask = (data.close < data.close.vbt.ago(1)).vbt.all_ago(5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-3)>>> fig = data.plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-4)>>> mask.vbt.signals.ranges.plot_shapes(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-5)... plot_close=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-6)... fig=fig, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-7)... shape_kwargs=dict(fillcolor="orangered")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-28-9)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/periods_ago.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/periods_ago.dark.svg#only-dark)


# Safe resampling[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#safe-resampling "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_1_2.svg)

 * The [look-ahead bias](https://www.investopedia.com/terms/l/lookaheadbias.asp) is an ongoing threat when working with array data, especially on multiple time frames. Using Pandas alone is strongly discouraged because it's not aware that financial data mainly involves bars where timestamps are opening times and events can happen at any time between bars, and thus falsely assumes that timestamps denote the exact time of an event. In VBT, there is an entire collection of functions and classes for resampling and analyzing data in a safe way!

Tutorial

Learn more in the [MTF analysis](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis) tutorial.

Calculate SMA on multiple time frames and display on the same chart
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-1)>>> def mtf_sma(close, close_freq, target_freq, timeperiod=5):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-2)... target_close = close.vbt.realign_closing(target_freq) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-3)... target_sma = vbt.talib("SMA").run(target_close, timeperiod=timeperiod).real 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-4)... target_sma = target_sma.rename(f"SMA ({target_freq})")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-5)... return target_sma.vbt.realign_closing(close.index, freq=close_freq) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-7)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2023")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-8)>>> fig = mtf_sma(data.close, "D", "daily").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-9)>>> mtf_sma(data.close, "D", "weekly").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-10)>>> mtf_sma(data.close, "D", "monthly").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-29-11)>>> fig.show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/safe_resampling.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/safe_resampling.dark.svg#only-dark)


# Resamplable objects[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#resamplable-objects "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_1_2.svg)

 * Not only you can resample time series, but also complex VBT objects! Under the hood, each object comprises of a bunch of array-like attributes, thus resampling here simply means aggregating all the accompanied information in one go. This is very convenient when you want to simulate on higher frequency for best accuracy, and then analyze on lower frequency for best speed.

Tutorial

Learn more in the [MTF analysis](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis) tutorial.

Plot the monthly return heatmap of a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-1)>>> import calendar
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-3)>>> data = vbt.YFData.pull("BTC-USD", start="2018", end="2023")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-4)>>> pf = vbt.PF.from_random_signals(data, n=100, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-5)>>> mo_returns = pf.resample("M").returns 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-6)>>> mo_return_matrix = pd.Series(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-7)... mo_returns.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-8)... index=pd.MultiIndex.from_arrays([
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-9)... mo_returns.index.year,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-10)... mo_returns.index.month
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-11)... ], names=["year", "month"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-12)... ).unstack("month")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-13)>>> mo_return_matrix.columns = mo_return_matrix.columns.map(lambda x: calendar.month_abbr[x])
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-14)>>> mo_return_matrix.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-15)... is_x_category=True,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-16)... trace_kwargs=dict(zmid=0, colorscale="Spectral")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-30-17)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/monthly_return_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/monthly_return_heatmap.dark.svg#only-dark)


# Formatting engine[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#formatting-engine "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_2.svg)

 * VectorBT® PRO is a very extensive library that defines thousands of classes, functions, and objects. Thus, when working with any of them, you may want to "see through" the object to gain a better understanding of its attributes and contents. Gladly, there is a new formatting engine that can accurately format any in-house object as a human-readable string. Did you know that the API documentation is partially powered by this engine? ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)

Introspect a data instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2021")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-3)>>> vbt.pprint(data) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-4)YFData(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-5) wrapper=ArrayWrapper(...),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-6) data=symbol_dict({
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-7) 'BTC-USD': <pandas.core.frame.DataFrame object at 0x7f7f1fbc6cd0 with shape (366, 7)>
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-8) }),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-9) single_key=True,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-10) classes=symbol_dict(),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-11) fetch_kwargs=symbol_dict({
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-12) 'BTC-USD': dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-13) start='2020',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-14) end='2021'
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-15) )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-16) }),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-17) returned_kwargs=symbol_dict({
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-18) 'BTC-USD': dict()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-19) }),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-20) last_index=symbol_dict({
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-21) 'BTC-USD': Timestamp('2020-12-31 00:00:00+0000', tz='UTC')
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-22) }),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-23) tz_localize=datetime.timezone.utc,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-24) tz_convert='UTC',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-25) missing_index='nan',
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-26) missing_columns='raise'
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-27))
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-28)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-29)>>> vbt.pdir(data) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-30) type path
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-31)attr 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-32)align_columns classmethod vectorbtpro.data.base.Data
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-33)align_index classmethod vectorbtpro.data.base.Data
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-34)build_feature_config_doc classmethod vectorbtpro.data.base.Data
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-35)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-36)vwap property vectorbtpro.data.base.Data
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-37)wrapper property vectorbtpro.base.wrapping.Wrapping
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-38)xs function vectorbtpro.base.indexing.PandasIndexer
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-39)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-40)>>> vbt.phelp(data.get) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-41)YFData.get(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-42) columns=None,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-43) symbols=None,
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-44) **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-45)):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-31-46) Get one or more columns of one or more symbols of data.
 
[/code]

 1. 2. 3. 


# Meta methods[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#meta-methods "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Many methods such as rolling apply are now available in two flavors: regular (instance methods) and meta (class methods). Regular methods are bound to a single array and do not have to take metadata anymore, while meta methods are not bound to any array and act as micro-pipelines with their own broadcasting and templating logic. Here, VBT closes one of the key limitations of Pandas - the inability to apply a function on multiple arrays at once.

Compute the rolling z-score on one array and the rolling correlation coefficient on two arrays
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-2)... def zscore_nb(x): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-3)... return (x[-1] - np.mean(x)) / np.std(x)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-5)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2021")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-6)>>> data.close.rolling(14).apply(zscore_nb, raw=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-7)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-8)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-9) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-10)2020-12-27 00:00:00+00:00 1.543527
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-11)2020-12-28 00:00:00+00:00 1.734715
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-12)2020-12-29 00:00:00+00:00 1.755125
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-13)2020-12-30 00:00:00+00:00 2.107147
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-14)2020-12-31 00:00:00+00:00 1.781800
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-15)Freq: D, Name: Close, Length: 366, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-17)>>> data.close.vbt.rolling_apply(14, zscore_nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-18)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-19) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-20)2020-12-27 00:00:00+00:00 1.543527
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-21)2020-12-28 00:00:00+00:00 1.734715
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-22)2020-12-29 00:00:00+00:00 1.755125
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-23)2020-12-30 00:00:00+00:00 2.107147
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-24)2020-12-31 00:00:00+00:00 1.781800
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-25)Freq: D, Name: Close, Length: 366, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-26)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-27)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-28)... def corr_meta_nb(from_i, to_i, col, a, b): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-29)... a_window = a[from_i:to_i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-30)... b_window = b[from_i:to_i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-31)... return np.corrcoef(a_window, b_window)[1, 0]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-32)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-33)>>> data2 = vbt.YFData.pull(["ETH-USD", "XRP-USD"], start="2020", end="2021")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-34)>>> vbt.pd_acc.rolling_apply( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-35)... 14, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-36)... corr_meta_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-37)... vbt.Rep("a"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-38)... vbt.Rep("b"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-39)... broadcast_named_args=dict(a=data.close, b=data2.close)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-40)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-41)symbol ETH-USD XRP-USD
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-42)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-43)2020-01-01 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-44)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-45)2020-12-27 00:00:00+00:00 0.636862 -0.511303
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-46)2020-12-28 00:00:00+00:00 0.674514 -0.622894
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-47)2020-12-29 00:00:00+00:00 0.712531 -0.773791
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-48)2020-12-30 00:00:00+00:00 0.839355 -0.772295
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-49)2020-12-31 00:00:00+00:00 0.878897 -0.764446
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-50)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-32-51)[366 rows x 2 columns]
 
[/code]

 1. 2. 3. 4. 5. 


# Array expressions[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#array-expressions "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * When combining multiple arrays, they often need to be properly aligned and broadcasted before the actual operation. Using Pandas alone won't do the trick because Pandas is too strict in this regard. Luckily, VBT has an accessor class method that can take a regular Python expression, identify all the variable names, extract the corresponding arrays from the current context, broadcast them, and only then evaluate the actual expression (also using [NumExpr](https://github.com/pydata/numexpr)!) ![⌨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2328.svg)

Evaluate a multiline array expression based on a Bollinger Bands indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-3)>>> low = data.low
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-4)>>> high = data.high
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-5)>>> bb = vbt.talib("BBANDS").run(data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-6)>>> upperband = bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-7)>>> lowerband = bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-8)>>> bandwidth = (bb.upperband - bb.lowerband) / bb.middleband
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-9)>>> up_th = vbt.Param([0.3, 0.4]) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-10)>>> low_th = vbt.Param([0.1, 0.2])
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-11)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-12)>>> expr = """
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-13)... narrow_bands = bandwidth < low_th
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-14)... above_upperband = high > upperband
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-15)... wide_bands = bandwidth > up_th
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-16)... below_lowerband = low < lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-17)... (narrow_bands & above_upperband) | (wide_bands & below_lowerband)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-18)... """
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-19)>>> mask = vbt.pd_acc.eval(expr)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-20)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-21)low_th up_th symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-22)0.1 0.3 BTC-USD 344
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-23) ETH-USD 171
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-24) 0.4 BTC-USD 334
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-25) ETH-USD 158
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-26)0.2 0.3 BTC-USD 444
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-27) ETH-USD 253
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-28) 0.4 BTC-USD 434
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-29) ETH-USD 240
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-33-30)dtype: int64
 
[/code]


# Resource management[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#resource-management "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * New profiling tools to measure the execution time and memory usage of any code block ![🧰](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9f0.svg)

Profile getting the Sharpe ratio of a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-3)>>> with (
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-4)... vbt.Timer() as timer, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-5)... vbt.MemTracer() as mem_tracer
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-6)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-7)... print(vbt.PF.from_random_signals(data.close, n=100).sharpe_ratio)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-8)0.33111243921865163
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-10)>>> print(timer.elapsed())
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-11)74.15 milliseconds
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-13)>>> print(mem_tracer.peak_usage())
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-34-14)459.7 kB
 
[/code]


# Templates[¶](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#templates "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

It's super-easy to extend classes, but VBT revolves around functions, so how do we enhance them or change their workflow? The easiest way is to introduce a tiny function (i.e., callback) that can be provided by the user and called by the main fucntion at some point in time. But this would require the main function to know which arguments to pass to the callback and what to do with the outputs. Here's a better idea: allow most arguments of the main function to become callbacks and then execute them to reveal the actual values. Such arguments are called "templates" and such a process is called "substitution". Templates are especially useful when some arguments (such as arrays) should be constructed only once all the required information is available, for example, once other arrays have been broadcast. Also, each such substitution opportunity has its own identifier such that you can control when a template should be substituted. In VBT, templates are first-class citizens and are integrated into most functions for an unmatched flexibility! ![🧞](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9de.svg)

Design a template-enhanced resampling functionality
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-1)>>> def resample_apply(index, by, apply_func, *args, template_context={}, **kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-2)... grouper = index.vbt.get_grouper(by) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-3)... results = {}
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-4)... with vbt.ProgressBar() as pbar:
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-5)... for group, group_idxs in grouper: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-6)... group_index = index[group_idxs]
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-7)... context = {"group": group, "group_index": group_index, **template_context} 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-8)... final_apply_func = vbt.substitute_templates(apply_func, context, eval_id="apply_func") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-9)... final_args = vbt.substitute_templates(args, context, eval_id="args")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-10)... final_kwargs = vbt.substitute_templates(kwargs, context, eval_id="kwargs")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-11)... results[group] = final_apply_func(*final_args, **final_kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-12)... pbar.update()
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-13)... return pd.Series(results)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-15)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-16)>>> resample_apply(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-17)... data.index, "Y", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-18)... lambda x, y: x.corr(y), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-19)... vbt.RepEval("btc_close[group_index]"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-20)... vbt.RepEval("eth_close[group_index]"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-21)... template_context=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-22)... btc_close=data.get("Close", "BTC-USD"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-23)... eth_close=data.get("Close", "ETH-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-35-25)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

Group 7/7
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-1)2017 0.808930
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-2)2018 0.897112
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-3)2019 0.753659
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-4)2020 0.940741
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-5)2021 0.553255
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-6)2022 0.975911
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-7)2023 0.974914
 [](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#__codelineno-36-8)Freq: A-DEC, dtype: float64
 
[/code]

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/productivity.py.txt)