import kfp
from kfp import compiler
import kfp.dsl as dsl
from kubernetes import client as k8s_client


class startOp(dsl.ContainerOp):
  """对文件中的数据进行验证"""
  def __init__(self):
    super(startOp, self).__init__(
      name='Start',
      image='oodaflow:example',
      command=['sh', '-c'],
      arguments = [
          "cd /home && ./run191.sh"
        ],
      #file_outputs={
      #  'start': '/output.txt',
       # }  
    )
@dsl.pipeline(name='OODA-one-test', description='shows how to define dsl.Condition.')
def time_stat():
    
    start = startOp().add_volume(k8s_client.V1Volume(name='start', host_path=k8s_client.V1HostPathVolumeSource(path="/lib/modules"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/lib/modules', name='start'))
    start.add_volume(k8s_client.V1Volume(name='dev', host_path=k8s_client.V1HostPathVolumeSource(path="/dev"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/dev', name='dev'))
    start.add_node_selector_constraint('kubernetes.io/hostname', '10.18.127.19')
    start.add_resource_limit("cambricon.com/mlu", "4")

compiler.Compiler().compile(time_stat, 'ooda-test.tar.gz')
