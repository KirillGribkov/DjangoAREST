from django.apps import AppConfig
import os
import threading
import asyncio


class HomepageConfig(AppConfig):
    name = 'homepage'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=self.start_async_loop, daemon=True).start()

    def start_async_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        from homepage.task import update_city
        loop.run_until_complete(update_city())