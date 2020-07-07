# -*- coding: utf-8 -*-
import time, os, sys
from datetime import datetime
import kfp
from kfp import compiler
import kfp.dsl as dsl
import kfp.gcp as gcp
from kubernetes import client as k8s_client

print('start exp!!!!')


class ai_detection(dsl.ContainerOp):
    def __init__(self, pre_input, detection_camb_id, user_name):
        super(ai_detection, self).__init__(
            name="ai_detection",
            image="10.18.95.8:80/library/camb_arm_execute:v5",
            command=[u'bash', u'-c'],
            arguments=['bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s aircraft && date > /root/data.txt' % (
            user_name, detection_camb_id), 'echo %s' % pre_input],
            file_outputs={u'data': u'/root/data.txt'},
        )


class picture_modify(dsl.ContainerOp):
    def __init__(self, pre_input, picture_modify_id, user_name, detection_camb_id):
        super(picture_modify, self).__init__(
            name="picture_modify",
            image="10.18.95.8:80/library/camb_arm_execute:v5",
            command=[u'bash', u'-c'],
            arguments=[
                'python3 /root/camb/copy_ret.py --job_id=%s --user_name=%s --log_id=%s && date > /root/data.txt' % (
                picture_modify_id, user_name, detection_camb_id), 'echo %s' % pre_input],
            file_outputs={u'data': u'/root/data.txt'},
        )


class data_collect(dsl.ContainerOp):
    def __init__(self, classify_data_path, classification_job_id, user_name):
        super(data_collect, self).__init__(
            name="data_collect",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=[u'bash', u'-c'],
            arguments=["bash /root/classify_data.sh %s %s %s && date > /root/data.txt" % (
            classify_data_path, classification_job_id, user_name)],
            file_outputs={u'data': u'/root/data.txt'},
        )


class ai_classify(dsl.ContainerOp):
    def __init__(self, pre_input, classify_camb_id, user_name):
        super(ai_classify, self).__init__(
            name="ai_classify",
            image="10.18.95.8:80/library/camb_arm_execute:v5",
            command=[u'bash', u'-c'],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s resnet && date > /root/data.txt" % (
            user_name, classify_camb_id), "echo %s" % pre_input],
            file_outputs={u'data': u'/root/data.txt'},
        )


class data_adjust(dsl.ContainerOp):
    def __init__(self, pre_input, detection_data_path, detection_job_id, user_name):
        super(data_adjust, self).__init__(
            name="data_adjust",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=[u'bash', u'-c'],
            arguments=['bash /root/detection_data.sh %s %s %s && date > /root/data.txt' % (
            detection_data_path, detection_job_id, user_name), 'echo %s' % pre_input],
            file_outputs={u'data': u'/root/data.txt'},
        )


@dsl.pipeline(name='a', description='.')
def pipeline_a():
    classify_data_path = "/root/AID"
    detection_data_path = "/root/aircraft"
    user_name = "admin"
    detection_job_id = "20200514-detection"
    classification_job_id = "20200514-classify"
    classify_camb_id = "20200514-camb-classify"
    detection_camb_id = "20200514-camb-detection"
    picture_modify_id = "20200514-camb-picture_modify"
    a_data_collect = data_collect(classify_data_path, classification_job_id, user_name).add_volume(
        k8s_client.V1Volume(name='a', host_path=k8s_client.V1LocalVolumeSource(path='/home/newnfs'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/newnfs', name='a'))

    a_data_collect.add_node_selector_constraint('beta.kubernetes.io/arch', 'amd64')

    a_ai_classify = ai_classify(a_data_collect.output, classify_camb_id, user_name).add_volume(
        k8s_client.V1Volume(name='a', host_path=k8s_client.V1LocalVolumeSource(path='/home/newnfs'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/newnfs', name='a'))
    a_ai_classify.add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')
    device_name = "dev-cambricon"
    a_ai_classify.add_volume(k8s_client.V1Volume(name='aaa', host_path=k8s_client.V1LocalVolumeSource(
        path='/sys/kernel/debug'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/sys/kernel/debug', name='aaa'))
    a_ai_classify.add_volume(k8s_client.V1Volume(name='bbb', host_path=k8s_client.V1LocalVolumeSource(
        path='/tmp/.X11-unix'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/tmp/.X11-unix', name='bbb'))
    a_ai_classify.add_volume(k8s_client.V1Volume(name='ccc', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/v8.2_arm'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/Cambricon-Test-v8.2_arm', name='ccc'))
    a_ai_classify.add_volume(k8s_client.V1Volume(name='ddd', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/arm_v8.0/v8.0_arm/ARM64-v8.0/arm64/congcan'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/congcan', name='ddd'))
    a_ai_classify.add_volume(k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
        path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0"))
    a_ai_classify.add_resource_limit("cambricon.com/mlu", 1)


    a_data_adjust = data_adjust(a_ai_classify.output, detection_data_path, detection_job_id, user_name).add_volume(
        k8s_client.V1Volume(name='a', host_path=k8s_client.V1LocalVolumeSource(path='/home/newnfs'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/newnfs', name='a'))
    a_data_adjust.add_node_selector_constraint('beta.kubernetes.io/arch', 'amd64')


    a_ai_detection = ai_detection(a_data_adjust.output, detection_camb_id, user_name).add_volume(
        k8s_client.V1Volume(name='a', host_path=k8s_client.V1LocalVolumeSource(path='/home/newnfs'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/newnfs', name='a'))
    a_ai_detection.add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')
    device_name = "dev-cambricon"
    a_ai_detection.add_volume(k8s_client.V1Volume(name='aaa', host_path=k8s_client.V1LocalVolumeSource(
        path='/sys/kernel/debug'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/sys/kernel/debug', name='aaa'))
    a_ai_detection.add_volume(k8s_client.V1Volume(name='bbb', host_path=k8s_client.V1LocalVolumeSource(
        path='/tmp/.X11-unix'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/tmp/.X11-unix', name='bbb'))
    a_ai_detection.add_volume(k8s_client.V1Volume(name='ccc', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/v8.2_arm'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/Cambricon-Test-v8.2_arm', name='ccc'))
    a_ai_detection.add_volume(k8s_client.V1Volume(name='ddd', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/arm_v8.0/v8.0_arm/ARM64-v8.0/arm64/congcan'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/congcan', name='ddd'))
    a_ai_detection.add_volume(k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
        path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0"))
    a_ai_detection.add_resource_limit("cambricon.com/mlu", 1)
    a_picture_modify = picture_modify(a_ai_detection.output, picture_modify_id, user_name,
                                      detection_camb_id).add_volume(
        k8s_client.V1Volume(name='a', host_path=k8s_client.V1LocalVolumeSource(path='/home/newnfs'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/newnfs', name='a'))

    a_picture_modify.add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')

    device_name = "dev-cambricon"
    a_picture_modify.add_volume(k8s_client.V1Volume(name='aaa', host_path=k8s_client.V1LocalVolumeSource(
        path='/sys/kernel/debug'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/sys/kernel/debug', name='aaa'))
    a_picture_modify.add_volume(k8s_client.V1Volume(name='bbb', host_path=k8s_client.V1LocalVolumeSource(
        path='/tmp/.X11-unix'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/tmp/.X11-unix', name='bbb'))
    a_picture_modify.add_volume(k8s_client.V1Volume(name='ccc', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/v8.2_arm'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/Cambricon-Test-v8.2_arm', name='ccc'))
    a_picture_modify.add_volume(k8s_client.V1Volume(name='ddd', host_path=k8s_client.V1LocalVolumeSource(
        path='/mnt/xfs/project/camb/arm_v8.0/v8.0_arm/ARM64-v8.0/arm64/congcan'))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/congcan', name='ddd'))
    a_picture_modify.add_volume(k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
        path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0"))
    a_picture_modify.add_resource_limit("cambricon.com/mlu", 1)


if __name__ == '__main__':
    compiler.Compiler().compile(pipeline_a, __file__ + '.tar.gz')
