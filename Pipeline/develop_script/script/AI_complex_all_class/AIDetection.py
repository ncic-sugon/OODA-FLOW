class ai_detection(dsl.ContainerOp):
    def __init__(self, pre_input, detection_camb_id, user_name):
        super(ai_detection, self).__init__(
            name="ai_detection",
            image="10.18.95.8:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s aircraft && date > /root/data.txt" % (user_name, detection_camb_id), "echo %s" % pre_input],
            file_outputs={
                "data": "/root/data.txt"
            })

