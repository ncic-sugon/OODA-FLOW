class data_adjust(dsl.ContainerOp):
    def __init__(self, pre_input, detection_data_path, detection_job_id, user_name):
        super(data_adjust, self).__init__(
            name="data_adjust",
            image="10.0.1.91:80/library/dataset_base:v1",
            command=["bash", "-c"],
            arguments=["bash /root/detection_data.sh %s %s %s && date > /root/data.txt" % (detection_data_path, detection_job_id, user_name),"echo %s" % pre_input],
            file_outputs={
                "data": "/root/data.txt"
            })

