class picture_modify(dsl.ContainerOp):
    def __init__(self, pre_input, picture_modify_id, user_name, detection_camb_id):
        super(picture_modify, self).__init__(
            name="picture_modify",
            image="10.0.1.91:80/library/camb_arm_execute:v2",
            command=["bash", "-c"],
            arguments=['python3 /root/camb/copy_ret.py --job_id=%s --user_name=%s --log_id=%s && date > /root/data.txt' % (picture_modify_id, user_name, detection_camb_id), 'echo %s' % pre_input],
            file_outputs={
                "data": "/root/data.txt"
            })

