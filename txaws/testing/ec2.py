# Copyright (C) 2009 Canonical Ltd
# Copyright (C) 2009 Duncan McGreggor <oubiwann@adytum.us>
# Licenced under the txaws licence available at /LICENSE in the txaws source.

from datetime import datetime

from twisted.internet.defer import succeed, fail
from twisted.python.failure import Failure
from twisted.web.error import Error

from txaws.ec2.model import Keypair, SecurityGroup

class FakeEC2Client(object):

    def __init__(self, creds, endpoint, instances=None, keypairs=None,
                 volumes=None, key_material="", security_groups=None,
                 snapshots=None):
        self.creds = creds
        self.endpoint = endpoint
        self.instances = instances or []
        self.keypairs = keypairs or []
        self.keypairs_deleted = []
        self.volumes = volumes or []
        self.volumes_deleted = []
        self.key_material = key_material
        self.security_groups = security_groups or []
        self.security_groups_deleted = []
        self.snapshots = snapshots or []
        self.snapshots_deleted = []

    def describe_instances(self):
        return succeed(self.instances)

    def describe_keypairs(self):
        return succeed(self.keypairs)

    def create_keypair(self, name):
        keypair = Keypair(name, "fingerprint", self.key_material)
        return succeed(keypair)

    def delete_keypair(self, name):
        self.keypairs_deleted.append(name)
        return succeed(True)

    def describe_security_groups(self, names=None):
        return succeed(self.security_groups)

    def create_security_group(self, name, description):
        self.security_groups.append(SecurityGroup(name, description))
        return succeed(True)

    def delete_security_group(self, name):
        self.security_groups_deleted.append(name)
        return succeed(True)

    def describe_volumes(self, *volume_ids):
        return succeed(self.volumes)

    def create_volume(self, availability_zone, size=None, snapshot_id=None):
        return succeed(self.volumes[0])

    def attach_volume(self, volume_id, instance_id, device):
        return succeed({"status": u"attaching",
                        "attach_time": datetime(2007, 6, 6, 11, 10, 00)})

    def delete_volume(self, volume_id):
        self.volumes_deleted.append(volume_id)
        return succeed(True)

    def describe_snapshots(self, *snapshot_ids):
        return succeed(self.snapshots)

    def create_snapshot(self, volume_id):
        return succeed(self.snapshots[0])

    def delete_snapshot(self, volume_id):
        self.snapshots_deleted.append(volume_id)
        return succeed(True)


class FakePageGetter(object):

    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

    def get_page(self, url, *args, **kwds):
        return succeed(self.payload)

    def get_page_with_exception(self, url, *args, **kwds):

        try:
            raise Error(self.status, "There's been an error", self.payload)
        except:
            failure = Failure()
        return fail(failure)

