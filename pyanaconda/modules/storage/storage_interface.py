#
# DBus interface for the storage.
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
from pyanaconda.dbus.property import emits_properties_changed
from pyanaconda.modules.common.constants.services import STORAGE
from pyanaconda.modules.common.base import KickstartModuleInterface
from pyanaconda.dbus.interface import dbus_interface
from pyanaconda.dbus.typing import *  # pylint: disable=wildcard-import
from pyanaconda.modules.common.containers import PartitioningContainer, TaskContainer
from pyanaconda.modules.storage.partitioning.constants import PartitioningMethod


@dbus_interface(STORAGE.interface_name)
class StorageInterface(KickstartModuleInterface):
    """DBus interface for Storage module."""

    def connect_signals(self):
        """Connect the signals."""
        super().connect_signals()
        self.watch_property(
            "CreatedPartitioning", self.implementation.created_partitioning_changed
        )
        self.watch_property(
            "AppliedPartitioning", self.implementation.applied_partitioning_changed
        )

    def ResetWithTask(self) -> ObjPath:
        """Reset the storage model.

        :return: a path to a task
        """
        return TaskContainer.to_object_path(
            self.implementation.reset_with_task()
        )

    @emits_properties_changed
    def CreatePartitioning(self, method: Str) -> ObjPath:
        """Create a new partitioning.

        Allowed values:
            AUTOMATIC
            CUSTOM
            MANUAL
            INTERACTIVE
            BLIVET

        :param method: a partitioning method
        :return: a path to a partitioning
        """
        return PartitioningContainer.to_object_path(
            self.implementation.create_partitioning(PartitioningMethod(method))
        )

    @property
    def CreatedPartitioning(self) -> List[ObjPath]:
        """List of all created partitioning modules.

        :return: a list of DBus paths
        """
        return PartitioningContainer.to_object_path_list(
            self.implementation.created_partitioning
        )

    @emits_properties_changed
    def ApplyPartitioning(self, partitioning: ObjPath):
        """Apply the partitioning.

        :param partitioning: a path to a partitioning
        """
        self.implementation.apply_partitioning(
            PartitioningContainer.from_object_path(partitioning)
        )

    @property
    def AppliedPartitioning(self) -> ObjPath:
        """The applied partitioning.

        :return: a DBus path or an empty string
        """
        partitioning = self.implementation.applied_partitioning

        if not partitioning:
            return ObjPath("")

        return PartitioningContainer.to_object_path(partitioning)

    def WriteConfigurationWithTask(self) -> ObjPath:
        """Write the storage configuration with a task.

        FIXME: This is a temporary workaround.

        :return: an installation task
        """
        return TaskContainer.to_object_path(
            self.implementation.write_configuration_with_task()
        )
