class ai_classify(dsl.ContainerOp):
    def __init__(self, pre_input, classify_camb_id, user_name):
        super(ai_classify, self).__init__(
            name="ai_classify",
            image="10.18.95.8:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s resnet && date > /root/data.txt" % (user_name, classify_camb_id), "echo %s" % pre_input],
            file_outputs={
                "data": "/root/data.txt"
            })

