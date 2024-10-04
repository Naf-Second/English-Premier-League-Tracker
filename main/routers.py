class ReadWriteRouter:
    def db_for_read(self, model, **hints):
        """Route all read operations to the read-only database."""
        return 'default'

    def db_for_write(self, model, **hints):
        """Route all write operations to the writable database."""
        return 'write_db'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations only on the writable database."""
        if db == 'default':
            return False  # Disable migrations on the read-only database
        return True  # Allow migrations on the writable database
