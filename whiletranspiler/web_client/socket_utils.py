def socket_decorator(sio):
    def socket_response(func):
        """
        Decorator to wrap socket actions
        """

        def _func(sid, *args, **kwargs):
            def emit(*_args, **_kwargs):
                _kwargs["room"] = sid
                sio.emit(*_args, **_kwargs)

            return func(emit, *args, **kwargs)

        return _func

    return socket_response
