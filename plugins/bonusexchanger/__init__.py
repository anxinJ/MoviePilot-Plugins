import threading
from typing import List, Tuple, Dict, Any

from app.helper.sites import SitesHelper
from app.log import logger
from app.plugins import _PluginBase

state_lock = threading.Lock()

class BonusExchanger(_PluginBase):
    # 插件名称
    plugin_name = "茉莉兑换器"
    # 插件描述
    plugin_desc = "兑换上传、下载..."
    # 插件图标
    plugin_icon = "BonusExchanger.png"
    # 插件版本
    plugin_version = "0.1.2"
    # 插件作者
    plugin_author = "anxinJ"
    # 作者主页
    author_url = "https://github.com/anxinJ"
    # 插件配置项ID前缀
    plugin_config_prefix = "bonusexchanger_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 2

    # preivate property
    exchange_sites = ""
    exchange_type = ""
    request_frequence = ""
    _enabled = False
    _notify = False
    _onlyonce = False

    def init_plugin(self, config: dict = None):
        logger.info(f"Hello, BonusExchanger! config {config}")
        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")
            self._onlyonce = config.get("onlyonce")
            self.exchange_sites = config.get("exchange_sites")
            self.exchange_type = config.get("exchange_type")
            self.request_frequence = config.get("request_frequence")

        if self._enabled:
            # 读取兑换站点
            exchange_sites = self.exchange_sites.split("\n")
            logger.info(f"兑换站点：{exchange_sites}")
            logger.info(f"兑换类型：{self.exchange_type}")
            logger.info(f"请求频率：{self.request_frequence}")
            if not exchange_sites:
                return

        if self._onlyonce:
            logger.info(f"茉莉兑换服务启动，立即运行一次")
            # 关闭一次性开关
            self._onlyonce = False
            self.update_config({
                "enabled": self._enabled,
                "notify": self._notify,
                "onlyonce": False,
                "exchange_sites": self.exchange_sites,
                "exchange_type": self.exchange_type,
                "request_frequence": self.request_frequence
            })

    def __update_config(self):
        """
        更新配置
        """
        self.update_config(
            {
                "enabled": self._enabled,
                "notify": self._notify,
                "onlyonce": self._onlyonce,
                "exchange_sites": self.exchange_sites,
                "exchange_type": self.exchange_type,
                "request_frequence": self.request_frequence
            }
        )

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        pass

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        # site_options = [{"title": site.get("name"), "value": site.get("id")}
        #                 for site in self.siteshelper.get_indexers()]
        return [
            {
                "component": "VForm",
                "content": [
                    {
                        "component": "VRow",
                        "content": [
                            {
                                "component": "VCol",
                                "props": {"cols": 12, "md": 4},
                                "content": [
                                    {
                                        "component": "VSwitch",
                                        "props": {
                                            "model": "enabled",
                                            "label": "启用插件",
                                        },
                                    }
                                ],
                            },
                            {
                                "component": "VCol",
                                "props": {"cols": 12, "md": 4},
                                "content": [
                                    {
                                        "component": "VSwitch",
                                        "props": {
                                            "model": "notify",
                                            "label": "发送通知",
                                        },
                                    }
                                ],
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 4
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'onlyonce',
                                            'label': '立即运行一次',
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VSelect',
                                        'props': {
                                            'multiple': True,
                                            'chips': True,
                                            'clearable': True,
                                            'model': 'exchange_sites',
                                            'label': '兑换站点',
                                            # 'items': site_options
                                            'items': ['a']
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "component": "VRow",
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                },
                                "content": [
                                    {
                                        "component": "VAlert",
                                        "props": {
                                            "type": "info",
                                            "variant": "tonal",
                                            "text": "茉莉兑换为测试功能，请谨慎开启。",
                                        },
                                    }
                                ],
                            },
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                },
                                "content": [
                                    {
                                        "component": "VAlert",
                                        "props": {
                                            "type": "info",
                                            "variant": "tonal",
                                            "text": "不同站点之间兑换类型可能不一致，导致兑换错误。等待适配站点",
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                ],
            }
        ], {
            "enabled": False,
            "onlyonce": False,
            "notify": False,
            "exchange_sites": "",
            "exchange_type": "upload",
            "request_frequence": 11
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        try:
            self._enabled = False
        except Exception as e:
            print(str(e))
