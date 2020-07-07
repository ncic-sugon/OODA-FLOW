class wgspic(dsl.ContainerOp):
    def __init__(self, validate=None):
        super(wgspic, self).__init__(
            name='wgs-picard-1',
            image='10.0.1.91:80/library/wgs-picard:latest',
            command=['./root/app/wgs_picard1.sh'],
            arguments=[
                '--validate', validate
            ],
            file_outputs={'pic': '/output.txt'}
        )