class data_collect(dsl.ContainerOp):
    def __init__(self, classify_data_path, classification_job_id, user_name):
        super(data_collect, self).__init__(
            name="data_collect",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=["bash", "-c"],
            arguments=["bash /root/classify_data.sh %s %s %s && date > /root/data.txt" % (classify_data_path, classification_job_id, user_name)],
            file_outputs={
                "data": "/root/data.txt"
            })


