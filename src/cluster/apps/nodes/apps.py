from django.apps import AppConfig


class NodesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nodes"

    def ready(self):
        import threading

        from .tasks import update_status_nodes  # Import the function only here

        # Start the thread only after the app is fully loaded
        thread = threading.Thread(target=update_status_nodes, daemon=True)
        thread.start()
