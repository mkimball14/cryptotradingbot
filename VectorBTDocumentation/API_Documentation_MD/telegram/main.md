telegram

#  telegram module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram "Permanent link")

Messaging using Python Telegram Bot.

* * *

## self_decorator function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L51-L57 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.self_decorator "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-0-1)self_decorator(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-0-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-0-3))
    

Pass bot object to func command.

* * *

## send_action function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L34-L48 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.send_action "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-1-1)send_action(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-1-2)    action
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-1-3))
    

Sends `action` while processing func command.

Suitable only for bound callbacks taking arguments `self`, `update`, `context` and optionally other.

* * *

## LogHandler class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L81-L94 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.LogHandler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-1)LogHandler(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-2)    callback,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-3)    pass_update_queue=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-4)    pass_job_queue=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-5)    pass_user_data=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-6)    pass_chat_data=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-7)    run_async=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-2-8))
    

Handler to log user updates.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `abc.ABC`
  * `telegram.ext.handler.Handler`
  * `typing.Generic`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### check_update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L84-L94 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.LogHandler.check_update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-3-1)LogHandler.check_update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-3-2)    update
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-3-3))
    

This method is called to determine if an update should be handled by this handler instance. It should always be overridden.

**Note**

Custom updates types can be handled by the dispatcher. Therefore, an implementation of this method should always check the type of :attr:`update`.

**Args**

update (:obj:`str` | :class:`telegram.Update`): The update to be tested. **Returns**

Either :obj:`None` or :obj:`False` if the update should not be handled. Otherwise an object that will be passed to :meth:`handle_update` and :meth:`collect_additional_context` when the update gets handled.

* * *

## TelegramBot class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L96-L392 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-4-1)TelegramBot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-4-2)    giphy_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-4-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-4-4))
    

Telegram bot.

See [Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot).

`**kwargs` are passed to `telegram.ext.updater.Updater` and override settings under `bot` in [telegram](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.telegram "vectorbtpro._settings.telegram").

**Usage**

Let's extend [TelegramBot](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot "vectorbtpro.utils.telegram.TelegramBot") to track cryptocurrency prices:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-1)import ccxt
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-2)import logging
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-3)from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-5)from telegram.ext import CommandHandler
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-6)from telegram import __version__ as TG_VER
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-8)try:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-9)    from telegram import __version_info__
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-10)except ImportError:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-11)    __version_info__ = (0, 0, 0, 0, 0)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-13)if __version_info__ >= (20, 0, 0, "alpha", 1):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-14)    raise RuntimeError(f"This example is not compatible with your current PTB version {TG_VER}")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-16)# Enable logging
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-17)logging.basicConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-18)    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-19))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-20)logger = logging.getLogger(__name__)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-21)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-22)class MyTelegramBot(vbt.TelegramBot):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-23)    @property
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-24)    def custom_handlers(self):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-25)        return (CommandHandler('get', self.get),)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-27)    @property
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-28)    def help_message(self):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-29)        return "Type /get [symbol] [exchange id (optional)] to get the latest price."
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-31)    def get(self, update, context):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-32)        chat_id = update.effective_chat.id
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-33)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-34)        if len(context.args) == 1:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-35)            symbol = context.args[0]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-36)            exchange = 'binance'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-37)        elif len(context.args) == 2:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-38)            symbol = context.args[0]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-39)            exchange = context.args[1]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-40)        else:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-41)            self.send_message(chat_id, "This command requires symbol and optionally exchange id.")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-42)            return
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-43)        try:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-44)            ticker = getattr(ccxt, exchange)().fetchTicker(symbol)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-45)        except Exception as e:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-46)            self.send_message(chat_id, str(e))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-47)            return
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-48)        self.send_message(chat_id, str(ticker['last']))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-49)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-50)if __name__ == "__main__":
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-51)    bot = MyTelegramBot(token='YOUR_TOKEN')
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-5-52)    bot.start()
    

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Configured.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Configured.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Configured.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Configured.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Configured.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Configured.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.config.Configured.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.config.Configured.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.config.Configured.pipe")
  * [Configured.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.config.Configured.config")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.config.Configured.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.config.Configured.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.config.Configured.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Configured.prettify")
  * [Configured.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Configured.rec_state")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.config.Configured.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.config.Configured.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.config.Configured.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.config.Configured.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.config.Configured.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.config.Configured.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.config.Configured.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.config.Configured.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.config.Configured.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.config.Configured.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.config.Configured.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.config.Configured.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.config.Configured.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.config.Configured.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Configured.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Configured.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Configured.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Configured.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Configured.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Configured.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Configured.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Configured.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Configured.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Configured.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Configured.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Configured.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Configured.pprint")



* * *

### chat_ids class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L245-L249 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.chat_ids "Permanent link")

Chat ids that ever interacted with this bot. A chat id is added upon receiving the "/start" command.

* * *

### chat_migration_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L360-L368 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.chat_migration_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-6-1)TelegramBot.chat_migration_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-6-2)    update,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-6-3)    context
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-6-4))
    

Chat migration callback.

* * *

### custom_handlers class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L239-L243 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.custom_handlers "Permanent link")

Custom handlers to add. Override to add custom handlers. Order counts.

* * *

### dispatcher class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L229-L232 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.dispatcher "Permanent link")

Dispatcher.

* * *

### error_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L377-L382 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.error_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-7-1)TelegramBot.error_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-7-2)    update,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-7-3)    context,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-7-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-7-5))
    

Error callback.

* * *

### help_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L354-L358 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.help_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-8-1)TelegramBot.help_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-8-2)    update,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-8-3)    context
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-8-4))
    

Help command callback.

* * *

### help_message class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L348-L352 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.help_message "Permanent link")

Message to be sent upon "/help" command. Override to define your own message.

* * *

### log_handler class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L234-L237 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.log_handler "Permanent link")

Log handler.

* * *

### running class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L389-L392 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.running "Permanent link")

Whether the bot is running.

* * *

### send method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L285-L301 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-1)TelegramBot.send(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-2)    kind,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-3)    chat_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-5)    log_msg=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-9-7))
    

Send message of any kind to `chat_id`.

* * *

### send_giphy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L318-L324 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send_giphy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-1)TelegramBot.send_giphy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-2)    chat_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-3)    text,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-5)    giphy_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-10-7))
    

Send GIPHY from text to `chat_id`.

* * *

### send_giphy_to_all method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L326-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send_giphy_to_all "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-1)TelegramBot.send_giphy_to_all(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-2)    text,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-4)    giphy_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-11-6))
    

Send GIPHY from text to all in [TelegramBot.chat_ids](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.chat_ids "vectorbtpro.utils.telegram.TelegramBot.chat_ids").

* * *

### send_message method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L308-L311 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send_message "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-1)TelegramBot.send_message(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-2)    chat_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-3)    text,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-12-6))
    

Send text message to `chat_id`.

* * *

### send_message_to_all method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L313-L316 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send_message_to_all "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-13-1)TelegramBot.send_message_to_all(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-13-2)    text,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-13-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-13-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-13-5))
    

Send text message to all in [TelegramBot.chat_ids](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.chat_ids "vectorbtpro.utils.telegram.TelegramBot.chat_ids").

* * *

### send_to_all method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L303-L306 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.send_to_all "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-14-1)TelegramBot.send_to_all(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-14-2)    kind,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-14-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-14-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-14-5))
    

Send message of any kind to all in [TelegramBot.chat_ids](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.chat_ids "vectorbtpro.utils.telegram.TelegramBot.chat_ids").

* * *

### start method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L251-L278 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-15-1)TelegramBot.start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-15-2)    in_background=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-15-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-15-4))
    

Start the bot. `**kwargs` are passed to `telegram.ext.updater.Updater.start_polling` and override settings under `bot` in [telegram](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.telegram "vectorbtpro._settings.telegram").

* * *

### start_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L340-L346 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.start_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-16-1)TelegramBot.start_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-16-2)    update,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-16-3)    context
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-16-4))
    

Start command callback.

* * *

### start_message class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L334-L338 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.start_message "Permanent link")

Message to be sent upon "/start" command. Override to define your own message.

* * *

### started_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L280-L283 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.started_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-17-1)TelegramBot.started_callback()
    

Callback once the bot has been started. Override to execute custom commands upon starting the bot.

* * *

### stop method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L384-L387 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.stop "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-18-1)TelegramBot.stop()
    

Stop the bot.

* * *

### unknown_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L370-L375 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.unknown_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-19-1)TelegramBot.unknown_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-19-2)    update,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-19-3)    context
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#__codelineno-19-4))
    

Unknown command callback.

* * *

### updater class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/telegram.py#L224-L227 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot.updater "Permanent link")

Updater.
