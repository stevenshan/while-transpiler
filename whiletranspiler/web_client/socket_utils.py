def socket_decorator(sio):
    """
    Wrapper for `sio.on` to define socket actions.
    """

    def socket_on(*args, **kwargs):
        def socket_response(func):
            """
            Decorator to wrap socket actions
            """

            def _func(sid, *args, **kwargs):
                def emit(*_args, **_kwargs):
                    _kwargs["room"] = sid
                    sio.emit(*_args, **_kwargs)

                return func(emit, *args, **kwargs)

            return sio.on(*args, **kwargs)(_func)

        return socket_response

    return socket_on
