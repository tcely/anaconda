#
# zFCP module
#
# Copyright (C) 2018 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from blivet.zfcp import zfcp

from pyanaconda.core.configuration.anaconda import conf
from pyanaconda.dbus import DBus
from pyanaconda.modules.common.base import KickstartBaseModule
from pyanaconda.anaconda_loggers import get_module_logger
from pyanaconda.modules.common.constants.objects import ZFCP
from pyanaconda.modules.storage.zfcp.discover import ZFCPDiscoverTask
from pyanaconda.modules.storage.zfcp.zfcp_interface import ZFCPInterface

log = get_module_logger(__name__)


class ZFCPModule(KickstartBaseModule):
    """The zFCP module."""

    def __init__(self):
        super().__init__()
        self.reload_module()
        self._zfcp_data = list()

    def publish(self):
        """Publish the module."""
        DBus.publish_object(ZFCP.object_path, ZFCPInterface(self))

    def reload_module(self):
        """Reload the zfcp module."""
        log.debug("Start up the zFCP module.")
        zfcp.startup()

    def discover_with_task(self, device_number, wwpn, lun):
        """Discover a zFCP device.

        :param device_number: a device number
        :param wwpn: a worldwide port name
        :param lun: an FCP LUN number
        :return: a task
        """
        return ZFCPDiscoverTask(device_number, wwpn, lun)

    def write_configuration(self):
        """Write the configuration to sysroot."""
        log.debug("Write zFCP configuration.")
        zfcp.write(conf.target.system_root)

    def process_kickstart(self, data):
        """Process the kickstart data."""
        self._zfcp_data = data.zfcp.zfcp

    def setup_kickstart(self, data):
        """Setup the kickstart data."""
        data.zfcp.zfcp = self._zfcp_data
