class Config():
    
    def __init__(self):
        self._resources = None
        self.arate = 8000
        self.resources_env_var = 'GENTLE_RESOURCES_ROOT'

    @property
    def resources(self):
        from resources import Resources
        if self._resources is None: self._resources = Resources()
        return self._resources

# global instance
config = Config()
