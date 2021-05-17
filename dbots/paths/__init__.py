class Path:
    def __init__(
        self,
        method: str,
        url: str,
        require_auth: bool = False,
        response_type: type = None,
        url_params: list[str] = None,
        params: list[str] = None,
        caching=None,
    ):
        if not url_params:
            url_params = []
        if not params:
            params = []
        self._method = method
        self._url = url
        self.response_type = response_type
        self._url_params = url_params
        self._params = params
        self.caching = caching
        self.require_auth = require_auth

    def build(self, base_url, **kwparams):
        url = base_url + self._url
        for url_param in self._url_params:
            if url_param in kwparams:
                url = url.replace(url_param, str(kwparams[url_param]))
        kwargs = {}
        if self._params:
            kwargs["json"] = {}
            for param in kwparams:
                if param in self._params:
                    if kwparams[param] is not None:
                        kwargs["json"][param] = kwparams[param]
        args = (self._method, url)
        return args, kwargs
