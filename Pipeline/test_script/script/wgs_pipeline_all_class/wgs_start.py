class wgsstart(dsl.ContainerOp):
    """validation for file"""

    def __init__(self,validate=None):
        super(wgsstart, self).__init__(
            name='time-start',
            image='10.0.1.91:80/library/wgs-start-end:latest',
            command=['./root/app/start.sh'],
            arguments=[
                '--validate', validate
            ],
            file_outputs={'start': '/output.txt',}
        )
