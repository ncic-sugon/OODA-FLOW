class wgssplit(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgssplit, self).__init__(
            name='wgs-split-first',
            image='10.0.1.91:80/library/wgs-split:latest',
            command=['./root/app/split.sh'],
            arguments=[
                '--validate', validate
            ],
            file_outputs={'split': '/output.txt'}
        )
